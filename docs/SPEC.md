# Technical Spec: PIRCSEEK

## 1. Runtime

- Linguagem: Python 3.
- Banco: SQLite via `sqlite3`.
- UI: HTML/CSS/JavaScript sem build obrigatório no MVP.
- Servidor local: Python stdlib (`http.server`) ou camada minima equivalente.
- Busca local: `rg` quando disponivel; fallback Python.
- Rede: nenhuma chamada externa no MVP.

## 2. Estrutura de diretorios

```text
PIRCSEEK/
  tools/
    picr.py
    picr_core/
      __init__.py
      cli.py
      db.py
      schema.py
      models.py
      markdown_store.py
      indexer.py
      search.py
      ranking.py
      tokens.py
      logs.py
      doctor.py
      server.py
  dashboard/
    index.html
    app.js
    style.css
  tests/
    test_tokens.py
    test_slug.py
    test_db.py
    test_indexer.py
    test_search.py
    test_doctor.py
    test_api.py
  docs/
  .picr/
    picr.db
    00-index.jsonl
    indexes/
    content/
    logs/
```

## 3. CLI contract

Todos os comandos devem aceitar `--root <path>` para testes e uso em projetos
diferentes. Default: diretorio atual.

### 3.1 `init`

```bash
python3 tools/picr.py init [--root .] [--force]
```

Saidas:

- `OK initialized <path>`
- `WARN already_initialized <path>`
- `FAIL <code> <message>`

### 3.2 `doctor`

```bash
python3 tools/picr.py doctor [--root .] [--json]
```

Checks:

- `workspace_exists`
- `db_open`
- `schema_version`
- `main_index_valid`
- `subindexes_valid`
- `markdown_paths_valid`
- `rg_available`
- `python_available`
- `codex_available`
- `claude_available`

Status:

- `OK`: tudo essencial valido.
- `WARN`: funcional, mas ha degradacao.
- `FAIL`: impossivel confiar no indice.

### 3.3 `category add`

```bash
python3 tools/picr.py category add --name "Skills" --slug skills --description "..."
```

Validacoes:

- slug unico;
- slug regex `^[a-z0-9][a-z0-9-]{1,62}$`;
- name entre 2 e 80 caracteres;
- description max 500 caracteres.

### 3.4 `item add`

```bash
python3 tools/picr.py item add \
  --category skills \
  --title "Database Fix" \
  --summary "Como localizar contexto de banco antes de corrigir bug." \
  --tags "database,sql,bugfix" \
  --content-file /tmp/item.md
```

Validacoes:

- categoria ativa existe;
- titulo 3 a 120 caracteres;
- resumo 20 a limite da categoria;
- tags max 12;
- path final fica dentro de `.picr/content/<category>/`.

### 3.5 `search`

```bash
python3 tools/picr.py search "corrigir bug banco" --limit 5 --format text
python3 tools/picr.py search "corrigir bug banco" --format json
```

Contrato JSON:

```json
{
  "query": "corrigir bug banco",
  "total_tokens_est": 1230,
  "results": [
    {
      "id": "10.003",
      "category": "skills",
      "title": "Database Fix",
      "summary": "Como localizar contexto de banco antes de corrigir bug.",
      "path": ".picr/content/skills/database-fix.md",
      "tokens_est": 420,
      "score": 18,
      "match_reasons": ["tag:database", "summary:banco"]
    }
  ]
}
```

Proibido:

- imprimir conteudo Markdown completo por default;
- retornar path absoluto no JSONL exportado;
- inventar resultado quando score zero.

## 4. SQLite schema

### 4.1 `schema_meta`

```sql
CREATE TABLE schema_meta (
  key TEXT PRIMARY KEY,
  value TEXT NOT NULL
);
```

Registro obrigatorio:

- `schema_version = 1`

### 4.2 `categories`

```sql
CREATE TABLE categories (
  id TEXT PRIMARY KEY,
  slug TEXT NOT NULL UNIQUE,
  name TEXT NOT NULL,
  description TEXT NOT NULL DEFAULT '',
  prompt_md TEXT NOT NULL DEFAULT '',
  display_order INTEGER NOT NULL DEFAULT 100,
  max_summary_chars INTEGER NOT NULL DEFAULT 220,
  max_item_tokens INTEGER NOT NULL DEFAULT 1200,
  active INTEGER NOT NULL DEFAULT 1,
  exportable INTEGER NOT NULL DEFAULT 1,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
```

### 4.3 `items`

```sql
CREATE TABLE items (
  id TEXT PRIMARY KEY,
  category_id TEXT NOT NULL,
  slug TEXT NOT NULL,
  title TEXT NOT NULL,
  summary TEXT NOT NULL,
  content_path TEXT NOT NULL,
  tags_json TEXT NOT NULL DEFAULT '[]',
  aliases_json TEXT NOT NULL DEFAULT '[]',
  tokens_est INTEGER NOT NULL DEFAULT 0,
  active INTEGER NOT NULL DEFAULT 1,
  exportable INTEGER NOT NULL DEFAULT 1,
  sensitive INTEGER NOT NULL DEFAULT 0,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  UNIQUE(category_id, slug),
  FOREIGN KEY (category_id) REFERENCES categories(id)
);
```

### 4.4 `routing_logs`

```sql
CREATE TABLE routing_logs (
  id TEXT PRIMARY KEY,
  query TEXT NOT NULL,
  cli TEXT NOT NULL DEFAULT '',
  result_ids_json TEXT NOT NULL DEFAULT '[]',
  opened_ids_json TEXT NOT NULL DEFAULT '[]',
  tokens_est INTEGER NOT NULL DEFAULT 0,
  outcome TEXT NOT NULL DEFAULT 'unknown',
  notes TEXT NOT NULL DEFAULT '',
  created_at TEXT NOT NULL
);
```

## 5. JSONL contracts

### 5.1 Main index

Arquivo: `.picr/00-index.jsonl`

```json
{"id":"cat_skills","slug":"skills","title":"Skills","summary":"Procedimentos reutilizaveis para CLIs de IA.","index_path":"indexes/skills.index.jsonl","items_count":12,"tokens_est":860,"active":true}
```

### 5.2 Category index

Arquivo: `.picr/indexes/<slug>.index.jsonl`

```json
{"id":"item_10_003","category":"skills","title":"Database Fix","summary":"Como localizar contexto de banco antes de corrigir bug.","path":"content/skills/database-fix.md","tags":["database","sql","bugfix"],"tokens_est":420,"sensitive":false}
```

## 6. Ranking

Normalizar query:

- lowercase;
- remover acentos;
- separar por tokens alfanumericos;
- descartar stopwords curtas.

Pontuacao:

| Match | Pontos |
|---|---:|
| slug da categoria | 12 |
| titulo | 10 |
| tag exata | 8 |
| alias | 7 |
| resumo | 5 |
| path | 3 |
| conteudo via rg | 2 |
| outcome ok anterior | max 5 |
| item sensivel | -5 se query nao menciona sensivel |

Empate:

1. maior score;
2. menor `tokens_est`;
3. mais recente;
4. titulo alfabetico.

## 7. API local

Base: `http://127.0.0.1:<port>`

| Metodo | Rota | Entrada | Saida |
|---|---|---|---|
| GET | `/api/health` | - | `{status, version}` |
| GET | `/api/doctor` | - | doctor JSON |
| GET | `/api/categories` | - | lista |
| POST | `/api/categories` | category payload | category |
| PATCH | `/api/categories/:id` | partial | category |
| GET | `/api/items?category=` | filtros | lista |
| POST | `/api/items` | item payload | item |
| PATCH | `/api/items/:id` | partial | item |
| GET | `/api/search?q=&limit=` | query | search result |
| POST | `/api/reindex` | - | status |
| GET | `/api/logs` | filtros | lista |
| POST | `/api/logs` | log payload | log |

Erros JSON:

```json
{"error":{"code":"VALIDATION_ERROR","message":"slug invalido","field":"slug"}}
```

## 8. Error codes

| Codigo | Quando ocorre | Acao esperada |
|---|---|---|
| `WORKSPACE_NOT_INITIALIZED` | `.picr/` ausente | rodar `picr init` |
| `DB_OPEN_FAILED` | SQLite nao abre | verificar permissao/corrupcao |
| `SCHEMA_VERSION_UNSUPPORTED` | schema desconhecido | migrar ou bloquear |
| `VALIDATION_ERROR` | payload invalido | corrigir campo |
| `DUPLICATE_SLUG` | slug ja existe | escolher outro |
| `PATH_ESCAPE_BLOCKED` | path sai de `.picr/` | bloquear operacao |
| `INDEX_INVALID_JSONL` | linha JSON invalida | reindexar |
| `CONTENT_PATH_MISSING` | Markdown ausente | doctor WARN/FAIL |

## 9. Security and local safety

- Bloquear path traversal (`../`, path absoluto indevido).
- Servidor por padrao em `127.0.0.1`, nao `0.0.0.0`.
- Nao executar comandos arbitrarios vindos do painel.
- Doctor pode detectar CLIs com `command -v`, mas nao deve executa-los alem de
  checks seguros de versao quando implementado.
- Logs nao salvam conteudo completo.
- JSONL exportado nao inclui item `exportable=false`.

## 10. Acceptance gates

Antes de implementar painel:

- schema testado;
- index/search testados;
- doctor testado.

Antes de declarar MVP:

- todos testes P0 passam;
- API local validada;
- painel validado manualmente;
- docs atualizadas.
