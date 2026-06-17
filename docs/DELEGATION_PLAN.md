# Delegation Plan: PIRCSEEK

## 1. Objetivo

Construir PIRCSEEK mais rapido sem gastar tokens demais e sem perder controle de
qualidade. Codex coordena, especifica, revisa e valida. Claude Code implementa
checkpoints pequenos e bem delimitados.

## 2. Status local dos CLIs

Verificado neste ambiente:

- `codex`: disponivel em `/home/guimp/.npm-global/bin/codex`, versao `0.139.0`.
- `claude`: disponivel em `/home/guimp/.local/bin/claude`, versao `2.1.177`.

Autenticacao e permissao de envio de conteudo privado devem ser revalidadas antes
de cada delegacao real.

## 3. Regras de delegacao

- Delegar apenas tarefas com escopo fechado.
- Uma tarefa por chamada.
- Maximo recomendado: 5 arquivos diretamente alterados por chamada.
- Aceite por chamada: 1 a 3 criterios objetivos.
- Claude nao faz review final.
- Codex nao edita os mesmos arquivos enquanto Claude estiver trabalhando.
- Codex revisa diff, roda testes e decide se segue, corrige ou reabre tarefa.
- Se Claude falhar por rede/politica/auth, registrar blocker e nao repetir em loop.
- Prompt para Claude deve apontar caminhos de docs, nao colar documentacao inteira.
- Para acionar Claude, usar `tools/delegate_cli.py --mode visible` com prompt
  salvo, dry-run inicial e log em `.picr/logs/delegations/`.
- Claude headless so pode ser usado com `--allow-headless-claude` e justificativa
  operacional explicita.

## 4. Especialidades

### Codex

- planejamento;
- especificacao;
- arquitetura;
- TDD/testes de aceite;
- revisao de diff;
- QA/security;
- integracao entre checkpoints;
- decisao de pronto tecnico.

### Claude Code

- implementacao repetitiva e localizada;
- CRUD;
- CLI commands;
- endpoints;
- HTML/CSS/JS do painel quando design system ja esta definido;
- ajustes orientados por testes;
- exemplos/scripts pequenos.

## 5. Checkpoints e tarefas

### C1: CLI e workspace

| Task | Owner | Escopo | Arquivos permitidos | Aceite |
|---|---|---|---|---|
| C1.1 Testes init/doctor | Codex | Criar testes base | `tests/` | testes falham antes do codigo |
| C1.2 CLI skeleton | Claude | Implementar `picr.py` e roteamento argparse | `tools/picr.py`, `tools/picr_core/cli.py` | `picr --help` funciona |
| C1.3 Workspace init | Claude | Criar `.picr/`, dirs e schema meta | `tools/picr_core/db.py`, `schema.py` | `picr init --root tmp` cria estrutura |
| C1.4 Doctor minimo | Claude | Checks de workspace/db/python/rg | `tools/picr_core/doctor.py` | retorna OK/WARN/FAIL |
| C1.5 Review gate | Codex | Revisar diff e rodar testes | todos alterados | C1 aprovado ou rework |

### C2: Categorias e itens

| Task | Owner | Escopo | Arquivos permitidos | Aceite |
|---|---|---|---|---|
| C2.1 Testes schema/validacao | Codex | Testes slug, categoria, item | `tests/` | cobre invalidos e duplicados |
| C2.2 Models/validation | Claude | Validadores e helpers | `tools/picr_core/models.py` | validacoes da SPEC passam |
| C2.3 Category commands | Claude | add/list/update basico | `cli.py`, `db.py` | categoria persiste |
| C2.4 Item commands | Claude | add/list + Markdown | `markdown_store.py`, `db.py`, `cli.py` | item gera Markdown |
| C2.5 Security gate | Codex | Path traversal/sensitive/exportable | tests + review | sem path escape |

### C3: Indexacao e busca

| Task | Owner | Escopo | Arquivos permitidos | Aceite |
|---|---|---|---|---|
| C3.1 Testes JSONL/ranking | Codex | Matriz de ranking | `tests/` | ranking deterministico |
| C3.2 Token estimator | Claude | `ceil(chars/4)` | `tokens.py` | unicode e arredondamento passam |
| C3.3 Indexer | Claude | `00-index` e subindices | `indexer.py` | JSONL valido |
| C3.4 Search/ranking | Claude | busca metadados + rg fallback | `search.py`, `ranking.py` | retorna metadata, nao Markdown |
| C3.5 Review gate | Codex | Validar anti-quebra de contexto | tests + review | search seguro |

### C4: Logs e metricas

| Task | Owner | Escopo | Arquivos permitidos | Aceite |
|---|---|---|---|---|
| C4.1 Testes logs | Codex | outcome e tokens | `tests/` | log persiste |
| C4.2 Log command | Claude | `picr log` | `logs.py`, `cli.py` | salva SQLite/JSONL |
| C4.3 Ranking boost | Claude | outcome ok influencia score | `ranking.py`, `search.py` | boost limitado a +5 |
| C4.4 QA gate | Codex | Verificar que logs nao salvam conteudo completo | tests + review | seguro |

### C5: API e painel

| Task | Owner | Escopo | Arquivos permitidos | Aceite |
|---|---|---|---|---|
| C5.1 Testes API | Codex | health/categories/items/search | `tests/` | contratos API passam |
| C5.2 Server local | Claude | rotas API stdlib | `server.py`, `cli.py` | bind `127.0.0.1` |
| C5.3 Dashboard shell | Claude | layout sidebar/top search | `dashboard/` | abre sem build |
| C5.4 CRUD UI | Claude | categorias/itens/logs | `dashboard/` | salvar funciona |
| C5.5 Visual QA | Codex | responsivo, estados, design system | screenshots/tests | sem overlap, estados cobertos |

### C6: Integracao com CLIs

| Task | Owner | Escopo | Arquivos permitidos | Aceite |
|---|---|---|---|---|
| C6.1 Protocol docs | Codex | contrato Codex/Claude | `docs/` | prompts curtos e claros |
| C6.2 Examples | Claude | exemplos de uso | `examples/`, `docs/` | comandos reais |
| C6.3 Smoke flow | Codex | consulta -> abrir path -> log | runtime local | fluxo validado |

## 6. Prompt padrao para Claude Code

Use este formato, preenchendo apenas o checkpoint atual:

```text
Voce esta implementando PIRCSEEK sob revisao do Codex.

Task: <C1.2 CLI skeleton>
Fonte de verdade:
- docs/PRD.md
- docs/SPEC.md
- docs/TEST_PLAN.md
- docs/TRACEABILITY.md

Escopo permitido:
- <arquivos permitidos>

Aceite:
- <criterio 1>
- <criterio 2>
- <criterio 3>

Regras:
- Nao altere arquivos fora do escopo.
- Nao implemente tarefas futuras.
- Nao adicione dependencias pesadas.
- Preserve comportamento local/offline.
- Retorne no maximo 12 linhas com arquivos alterados, testes executados e blockers.
```

## 7. Gates por camada

### Banco

- schema version existe;
- migrations idempotentes;
- constraints de slug e FK validadas;
- dados sensiveis respeitam `exportable`.

### API/Backend

- CLI retorna erros acionaveis;
- API local padroniza JSON;
- path traversal bloqueado;
- JSONL valido e atomico.

### Frontend/UI

- design system aplicado;
- estados loading/empty/error/success;
- validacao inline;
- responsivo sem overlap;
- painel nao esconde erro critico.

### Workflow/Plugins

- PIRCSEEK nao executa tarefa;
- retorna paths/resumos/tokens;
- logs distinguem CLI usado;
- Codex/Claude abrem apenas contexto necessario.

## 8. Quando nao delegar

Nao delegar para Claude:

- decisao de arquitetura;
- aprovacao final;
- revisao de seguranca;
- mudanca ampla de escopo;
- tarefa que exige enviar segredos ou conteudo sensivel externo;
- correcoes em arquivos que Codex esta editando no mesmo momento.
