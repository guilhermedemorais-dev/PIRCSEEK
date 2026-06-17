# Prompt: Codex CLI - Lideranca Tecnica C1

```text
Voce e o technical lead do projeto PIRCSEEK.

CWD esperado: /home/guimp/PIRCSEEK

Objetivo:
Executar o Checkpoint 1 como lider tecnico, seguindo SDD e TDD. Primeiro leia:
- docs/PRD.md
- docs/FUNCTIONAL_SPEC.md
- docs/SPEC.md
- docs/DATA_MODEL.md
- docs/ERROR_HANDLING.md
- docs/TEST_PLAN.md
- docs/TRACEABILITY.md
- docs/DELEGATION_PLAN.md
- docs/QA_CHECKLIST.md

Tarefa Codex:
1. Auditar o escopo do Checkpoint C1 no docs/DELEGATION_PLAN.md.
2. Criar ou ajustar testes TDD iniciais para:
   - init cria workspace .picr
   - doctor retorna OK/WARN/FAIL
   - path traversal e bloqueado
   - schema_version existe
3. Nao implementar a solucao completa se os testes ainda nao existirem.
4. Se implementar algo, manter escopo pequeno e documentar o motivo.
5. Nao alterar docs fora do necessario.
6. Nao executar Claude automaticamente.
7. Ao final, retornar:
   - arquivos criados/alterados
   - testes criados
   - comando de teste
   - status Banco/API/Frontend
   - proximo prompt recomendado para Claude

Regras:
- PIRCSEEK e buscador local de contexto, nao agente executor.
- Sem Docker.
- Sem internet.
- SQLite local em .picr/picr.db.
- JSONL e saida para LLM.
- Markdown e conteudo completo.
- Search nao deve imprimir Markdown inteiro por default.
- Qualquer conclusao precisa de evidencia de teste.
```
