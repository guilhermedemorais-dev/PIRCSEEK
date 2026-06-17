# Prompt: Claude CLI - Implementacao C1

```text
Voce esta implementando PIRCSEEK sob revisao do Codex.

CWD esperado: /home/guimp/PIRCSEEK

Task:
Executar somente o Checkpoint C1 do docs/DELEGATION_PLAN.md, com foco em:
- C1.2 CLI skeleton
- C1.3 Workspace init
- C1.4 Doctor minimo

Fonte de verdade:
- docs/PRD.md
- docs/FUNCTIONAL_SPEC.md
- docs/SPEC.md
- docs/DATA_MODEL.md
- docs/ERROR_HANDLING.md
- docs/TEST_PLAN.md
- docs/TRACEABILITY.md
- docs/DELEGATION_PLAN.md

Escopo permitido:
- tools/picr.py
- tools/picr_core/__init__.py
- tools/picr_core/cli.py
- tools/picr_core/db.py
- tools/picr_core/schema.py
- tools/picr_core/doctor.py
- tests/ somente se precisar ajustar testes do checkpoint

Aceite:
1. `python3 tools/picr.py --help` funciona.
2. `python3 tools/picr.py init --root /tmp/pircseek-test` cria `.picr/`, `picr.db`, `indexes/`, `content/`, `logs/` e schema_version.
3. `python3 tools/picr.py doctor --root /tmp/pircseek-test` retorna status OK/WARN/FAIL com checks claros.
4. Path traversal deve ser bloqueado quando aplicavel.
5. Testes do checkpoint devem passar.

Regras:
- Nao implemente checkpoints C2-C6.
- Nao crie painel ainda.
- Nao adicione Docker.
- Nao adicione dependencias pesadas.
- Nao faca busca web.
- Nao altere arquitetura sem atualizar docs e avisar.
- Nao mexa em arquivos fora do escopo.
- Retorne no maximo 12 linhas com:
  - arquivos alterados
  - comandos executados
  - testes que passaram/falharam
  - blockers
```
