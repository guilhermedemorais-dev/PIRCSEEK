#!/usr/bin/env python3
"""Run local AI CLIs with a saved prompt and auditable logs."""

from __future__ import annotations

import argparse
import json
import math
import os
import shlex
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


SUPPORTED_CLIS = {"codex", "claude"}


def estimate_tokens(text: str) -> int:
    return int(math.ceil(len(text) / 4)) if text else 0


def read_prompt(prompt_file: str | None, prompt: str | None) -> str:
    if prompt_file:
        return Path(prompt_file).read_text(encoding="utf-8")
    if prompt:
        return prompt
    raise SystemExit("FAIL prompt_required: use --prompt-file or --prompt")


def timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def safe_label(value: str) -> str:
    allowed = []
    for char in value.lower():
        if char.isalnum() or char in {"-", "_"}:
            allowed.append(char)
        elif char.isspace() or char in {"/", "."}:
            allowed.append("-")
    label = "".join(allowed).strip("-")
    return label[:80] or "delegation"


def build_command(args: argparse.Namespace) -> list[str]:
    if args.cli not in SUPPORTED_CLIS:
        raise SystemExit(f"FAIL unsupported_cli: {args.cli}")

    binary = shutil.which(args.cli)
    if not binary:
        raise SystemExit(f"FAIL cli_not_found: {args.cli}")

    cwd = str(Path(args.cwd).resolve())

    if args.cli == "codex":
        command = [
            binary,
            "exec",
            "--cd",
            cwd,
            "--sandbox",
            args.codex_sandbox,
            "--ask-for-approval",
            args.codex_approval,
        ]
        if args.codex_json:
            command.append("--json")
        command.append("-")
        return command

    command = [
        binary,
        "--print",
        "--permission-mode",
        args.claude_permission_mode,
        "--output-format",
        args.claude_output_format,
    ]
    if args.claude_allowed_tools:
        command.extend(["--allowedTools", args.claude_allowed_tools])
    return command


def enforce_execution_policy(args: argparse.Namespace) -> None:
    if args.cli == "claude" and args.mode == "print" and not args.dry_run and not args.allow_headless_claude:
        raise SystemExit(
            "FAIL headless_claude_blocked: use --mode visible, "
            "or pass --allow-headless-claude explicitly for non-interactive runs"
        )


def build_visible_inner_command(args: argparse.Namespace, prompt_path: Path) -> str:
    cwd = shlex.quote(str(Path(args.cwd).resolve()))
    prompt = f"$(cat {shlex.quote(str(prompt_path))})"

    if args.cli == "codex":
        binary = shlex.quote(shutil.which("codex") or "codex")
        return (
            f"cd {cwd} && "
            f"{binary} -C {cwd} -s {shlex.quote(args.codex_sandbox)} "
            f"-a {shlex.quote(args.visible_codex_approval)} \"{prompt}\"; "
            "status=$?; echo; echo '[delegate_cli] codex exited with status' $status; "
            "echo 'Press Enter to close...'; read _"
        )

    binary = shlex.quote(shutil.which("claude") or "claude")
    allowed_tools = ""
    if args.claude_allowed_tools:
        allowed_tools = f" --allowedTools {shlex.quote(args.claude_allowed_tools)}"
    return (
        f"cd {cwd} && "
        f"{binary} --permission-mode {shlex.quote(args.claude_permission_mode)}"
        f"{allowed_tools} \"{prompt}\"; "
        "status=$?; echo; echo '[delegate_cli] claude exited with status' $status; "
        "echo 'Press Enter to close...'; read _"
    )


def launch_visible(args: argparse.Namespace, prompt_text: str, log_dir: Path, metadata: dict[str, object]) -> int:
    terminal = shutil.which(args.terminal)
    if not terminal:
        raise SystemExit(f"FAIL terminal_not_found: {args.terminal}")

    run_dir = log_dir / timestamp()
    run_dir.mkdir(parents=True, exist_ok=True)
    prompt_path = run_dir / f"{safe_label(args.cli)}-prompt.md"
    script_path = run_dir / f"{safe_label(args.cli)}-visible.sh"
    prompt_path.write_text(prompt_text, encoding="utf-8")

    inner = build_visible_inner_command(args, prompt_path)
    script_path.write_text("#!/usr/bin/env bash\nset +e\n" + inner + "\n", encoding="utf-8")
    script_path.chmod(0o700)

    command = [terminal, "--", "bash", str(script_path)]
    payload = {
        **metadata,
        "mode": "visible",
        "terminal": args.terminal,
        "prompt_path": str(prompt_path),
        "script_path": str(script_path),
        "command": command,
    }
    log_path = write_log(log_dir, f"{args.cli}-visible", payload)

    if args.dry_run:
        print(json.dumps({**payload, "log_path": str(log_path)}, ensure_ascii=False, indent=2))
        return 0

    subprocess.Popen(command, cwd=str(Path(args.cwd).resolve()))
    print(json.dumps({**payload, "log_path": str(log_path), "launched": True}, ensure_ascii=False, indent=2))
    return 0


def write_log(log_dir: Path, label: str, payload: dict[str, object]) -> Path:
    log_dir.mkdir(parents=True, exist_ok=True)
    path = log_dir / f"{timestamp()}-{safe_label(label)}.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def run_delegate(args: argparse.Namespace) -> int:
    prompt_text = read_prompt(args.prompt_file, args.prompt)
    cwd = Path(args.cwd).resolve()
    log_dir = Path(args.log_dir or cwd / ".picr" / "logs" / "delegations")
    enforce_execution_policy(args)
    command = build_command(args)
    prompt_tokens_est = estimate_tokens(prompt_text)

    metadata = {
        "cli": args.cli,
        "cwd": str(cwd),
        "prompt_file": args.prompt_file,
        "prompt_tokens_est": prompt_tokens_est,
        "command": command,
        "mode": args.mode,
        "dry_run": args.dry_run,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    if args.mode == "visible":
        return launch_visible(args, prompt_text, log_dir, metadata)

    if args.dry_run:
        log_path = write_log(log_dir, f"{args.cli}-dry-run", metadata)
        print(json.dumps({**metadata, "log_path": str(log_path)}, ensure_ascii=False, indent=2))
        return 0

    run_kwargs = {
        "cwd": str(cwd),
        "text": True,
        "capture_output": True,
        "timeout": args.timeout,
    }

    try:
        if args.cli == "codex":
            result = subprocess.run(command, input=prompt_text, **run_kwargs)
        else:
            result = subprocess.run([*command, prompt_text], **run_kwargs)
    except subprocess.TimeoutExpired as exc:
        payload = {
            **metadata,
            "returncode": 124,
            "stdout": exc.stdout or "",
            "stderr": exc.stderr or "",
            "timeout": args.timeout,
            "error": "TIMEOUT_EXPIRED",
        }
        log_path = write_log(log_dir, f"{args.cli}-timeout", payload)
        print(f"FAIL TIMEOUT_EXPIRED after {args.timeout}s", file=sys.stderr)
        print(f"[delegate_cli] log: {log_path}", file=sys.stderr)
        return 124

    payload = {
        **metadata,
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }
    log_path = write_log(log_dir, f"{args.cli}-run", payload)

    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, file=sys.stderr, end="")
    print(f"\n[delegate_cli] log: {log_path}", file=sys.stderr)
    return result.returncode


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Delegate a prompt to a local AI CLI.")
    parser.add_argument("--cli", required=True, choices=sorted(SUPPORTED_CLIS))
    parser.add_argument("--prompt-file")
    parser.add_argument("--prompt")
    parser.add_argument("--cwd", default=os.getcwd())
    parser.add_argument("--log-dir")
    parser.add_argument("--timeout", type=int, default=1800)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--mode", default="print", choices=["print", "visible"])
    parser.add_argument("--terminal", default="gnome-terminal")

    parser.add_argument("--codex-sandbox", default="workspace-write")
    parser.add_argument("--codex-approval", default="never", choices=["untrusted", "on-request", "never"])
    parser.add_argument("--visible-codex-approval", default="on-request", choices=["untrusted", "on-request", "never"])
    parser.add_argument("--codex-json", action="store_true")

    parser.add_argument("--claude-permission-mode", default="acceptEdits")
    parser.add_argument("--claude-output-format", default="text", choices=["text", "json", "stream-json"])
    parser.add_argument("--claude-allowed-tools", default="")
    parser.add_argument("--allow-headless-claude", action="store_true")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return run_delegate(args)


if __name__ == "__main__":
    raise SystemExit(main())
