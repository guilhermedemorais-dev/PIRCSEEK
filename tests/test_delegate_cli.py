import importlib.util
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path
from unittest import mock


MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "delegate_cli.py"
SPEC = importlib.util.spec_from_file_location("delegate_cli", MODULE_PATH)
delegate_cli = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(delegate_cli)


class DelegateCliTests(unittest.TestCase):
    def test_estimate_tokens_rounds_up(self):
        self.assertEqual(delegate_cli.estimate_tokens(""), 0)
        self.assertEqual(delegate_cli.estimate_tokens("a" * 400), 100)
        self.assertEqual(delegate_cli.estimate_tokens("a" * 401), 101)

    @mock.patch("shutil.which", return_value="/usr/bin/codex")
    def test_build_codex_command_reads_prompt_from_stdin(self, _):
        args = Namespace(
            cli="codex",
            cwd="/tmp/project",
            codex_sandbox="workspace-write",
            codex_approval="never",
            codex_json=False,
        )
        command = delegate_cli.build_command(args)
        self.assertEqual(command[:4], ["/usr/bin/codex", "exec", "--cd", "/tmp/project"])
        self.assertEqual(command[-1], "-")
        self.assertIn("--ask-for-approval", command)

    @mock.patch("shutil.which", return_value="/usr/bin/claude")
    def test_build_claude_command_uses_print_mode(self, _):
        args = Namespace(
            cli="claude",
            cwd="/tmp/project",
            claude_permission_mode="acceptEdits",
            claude_output_format="text",
            claude_allowed_tools="",
        )
        command = delegate_cli.build_command(args)
        self.assertEqual(command[:2], ["/usr/bin/claude", "--print"])
        self.assertIn("--permission-mode", command)

    def test_read_prompt_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "prompt.md"
            path.write_text("hello", encoding="utf-8")
            self.assertEqual(delegate_cli.read_prompt(str(path), None), "hello")

    @mock.patch("shutil.which", return_value="/usr/bin/claude")
    def test_visible_claude_inner_command_uses_prompt_file(self, _):
        args = Namespace(
            cli="claude",
            cwd="/tmp/project",
            claude_permission_mode="plan",
            claude_allowed_tools="",
        )
        command = delegate_cli.build_visible_inner_command(args, Path("/tmp/prompt.md"))
        self.assertIn("claude", command)
        self.assertIn("cat /tmp/prompt.md", command)
        self.assertIn("Press Enter to close", command)

    def test_blocks_real_headless_claude_without_explicit_flag(self):
        args = Namespace(
            cli="claude",
            mode="print",
            dry_run=False,
            allow_headless_claude=False,
        )
        with self.assertRaises(SystemExit) as context:
            delegate_cli.enforce_execution_policy(args)
        self.assertIn("headless_claude_blocked", str(context.exception))


if __name__ == "__main__":
    unittest.main()
