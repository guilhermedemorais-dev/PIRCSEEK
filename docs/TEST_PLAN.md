# Test Plan: PIRCSEEK

O desenvolvimento deve seguir TDD: cada checkpoint comeca pelos testes do
comportamento esperado.

## 1. Matriz requisito -> teste

| Requisito | Teste minimo |
|---|---|
| RF-001 init | `test_init_creates_workspace` |
| RF-002 categoria | `test_category_add_persists_and_reindexes` |
| RF-003 editar categoria | `test_category_update_preserves_items` |
| RF-005 criar item | `test_item_add_writes_db_markdown_jsonl` |
| RF-008 busca | `test_search_returns_ranked_metadata_only` |
| RF-009 log | `test_log_records_query_cli_tokens_outcome` |
| RF-010 doctor | `test_doctor_warns_on_missing_markdown_path` |
| RNF local | `test_server_binds_localhost_by_default` |
| seguranca path | `test_path_traversal_is_blocked` |

## 2. Unit tests

### tokens

- `estimate_tokens("") == 0`
- 400 chars -> 100
- 401 chars -> 101
- unicode nao quebra

### slug

- remove acentos;
- troca espacos por hifen;
- bloqueia `../`;
- bloqueia path absoluto;
- rejeita vazio.

### validation

- categoria sem nome falha;
- slug duplicado falha;
- item sem categoria falha;
- item sensivel exportavel exige confirmacao/campo explicito;
- tags acima do limite falham.

### ranking

- titulo > tag > resumo > conteudo;
- outcome `ok` adiciona boost;
- empate usa menor token.

## 3. Integration tests

### workspace

```text
init
doctor
category add
item add
index
search
log
```

Validar:

- SQLite tem registros;
- Markdown existe;
- JSONL e valido;
- search encontra item;
- log e salvo.

### broken index

1. Criar item.
2. Apagar Markdown manualmente.
3. Rodar doctor.
4. Esperar `WARN CONTENT_PATH_MISSING`.

### export safety

1. Criar item `exportable=false`.
2. Reindexar.
3. Verificar que item nao aparece no JSONL.

## 4. API tests

- `GET /api/health`
- `GET /api/doctor`
- `POST /api/categories`
- `PATCH /api/categories/:id`
- `POST /api/items`
- `PATCH /api/items/:id`
- `GET /api/search`
- `POST /api/reindex`
- `POST /api/logs`

Cada teste deve validar codigo HTTP, schema JSON e persistencia.

## 5. UI acceptance tests

Antes de considerar painel pronto, validar manualmente ou com Playwright:

- sidebar renderiza;
- busca funciona;
- criar categoria;
- criar item;
- erro de slug aparece inline;
- tokens aparecem no resultado;
- estado vazio de logs aparece;
- mobile nao sobrepoe texto.

## 6. Anti-regression gates

Nao aceitar merge/checkpoint se:

- search imprime Markdown inteiro por default;
- JSONL tem path absoluto;
- path traversal passa;
- item `exportable=false` aparece em indice;
- doctor ignora path quebrado;
- painel salva sem validacao.

## 7. Commands

```bash
python3 -m unittest discover
python3 tools/picr.py init --root /tmp/picr-test
python3 tools/picr.py doctor --root /tmp/picr-test
python3 tools/picr.py search "database" --root /tmp/picr-test --format json
```

Se `pytest` for adotado:

```bash
python3 -m pytest
```
