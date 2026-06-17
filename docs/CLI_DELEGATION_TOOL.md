# CLI Delegation Tool

`tools/delegate_cli.py` resolve o problema de acionar outro CLI local a partir de
um prompt salvo, com comando padronizado, dry-run e log. Para Claude Code, o
fluxo preferido e visivel/interativo.

## Objetivo

Permitir que o workflow chame:

- `codex exec`
- `claude` em terminal visivel
- `claude --print` somente quando headless for explicitamente liberado

sem colar prompt manualmente, mantendo escopo, logs e auditoria.

## Uso seguro primeiro

Sempre rode `--dry-run` antes de executar de verdade.

```bash
python3 tools/delegate_cli.py \
  --cli codex \
  --prompt-file docs/prompts/codex-c1-lead.md \
  --cwd /home/guimp/PIRCSEEK \
  --dry-run
```

## Chamar Codex CLI

```bash
python3 tools/delegate_cli.py \
  --cli codex \
  --prompt-file docs/prompts/codex-c1-lead.md \
  --cwd /home/guimp/PIRCSEEK
```

Comando gerado internamente:

```text
codex exec --cd /home/guimp/PIRCSEEK --sandbox workspace-write --ask-for-approval never -
```

O prompt e enviado por stdin para evitar problemas com prompt grande em argv.

## Abrir Claude visivel na tela

Este e o fluxo padrao para delegar implementacao ao Claude. Ele abre um terminal
real com o Claude trabalhando na tela.

```bash
python3 tools/delegate_cli.py \
  --cli claude \
  --mode visible \
  --prompt-file docs/prompts/claude-c1-implementation.md \
  --cwd /home/guimp/PIRCSEEK
```

O terminal fica aberto no final para o usuario revisar a saida.

## Chamar Claude em modo headless

Modo headless existe apenas para automacao controlada. Execucao real com
`claude --print` fica bloqueada por padrao para evitar que Claude trabalhe em
segundo plano sem o usuario ver.

```bash
python3 tools/delegate_cli.py \
  --cli claude \
  --prompt-file docs/prompts/claude-c1-implementation.md \
  --cwd /home/guimp/PIRCSEEK \
  --allow-headless-claude
```

Comando gerado internamente nesse modo:

```text
claude --print --permission-mode acceptEdits --output-format text "<prompt>"
```

## Abrir Codex visivel na tela

```bash
python3 tools/delegate_cli.py \
  --cli codex \
  --mode visible \
  --prompt-file docs/prompts/codex-c1-lead.md \
  --cwd /home/guimp/PIRCSEEK
```

Em modo visivel, o Codex usa aprovacao `on-request` por padrao.

## Logs

Por padrao, logs vao para:

```text
.picr/logs/delegations/
```

Cada log registra:

- CLI usado;
- CWD;
- prompt file;
- tokens estimados;
- comando;
- stdout;
- stderr;
- return code.

## Limites

- A ferramenta nao decide arquitetura.
- A ferramenta nao valida a qualidade do diff.
- Codex ainda precisa revisar a saida.
- Se `codex` ou `claude` falhar por auth/rede/politica, o log registra a falha.
- `--ask-for-approval never` no Codex evita travar em automacao, mas comandos que
  precisem aprovacao podem falhar.
- `--mode visible` depende de `gnome-terminal` ou do terminal configurado em
  `--terminal`.
- Claude headless sem `--allow-headless-claude` retorna
  `FAIL headless_claude_blocked`.
