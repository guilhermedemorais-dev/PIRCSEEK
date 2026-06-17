# Data Model: PIRCSEEK

## 1. Regras globais

- IDs sao strings estaveis.
- Slugs sao unicos dentro do escopo correto.
- Paths salvos no banco sao relativos a `.picr/`.
- Todo timestamp usa ISO 8601 local ou UTC, definido na implementacao e mantido
  consistente.
- JSON em campos `*_json` deve ser array valido.

## 2. Category

```json
{
  "id": "cat_skills",
  "slug": "skills",
  "name": "Skills",
  "description": "Procedimentos reutilizaveis para CLIs de IA.",
  "prompt_md": "Use esta categoria quando...",
  "display_order": 10,
  "max_summary_chars": 220,
  "max_item_tokens": 1200,
  "active": true,
  "exportable": true,
  "created_at": "2026-06-17T00:00:00Z",
  "updated_at": "2026-06-17T00:00:00Z"
}
```

Validacoes:

- `slug`: `^[a-z0-9][a-z0-9-]{1,62}$`
- `name`: 2-80 chars
- `description`: 0-500 chars
- `max_summary_chars`: 80-500
- `max_item_tokens`: 100-10000

## 3. Item

```json
{
  "id": "item_skills_database_fix",
  "category_id": "cat_skills",
  "slug": "database-fix",
  "title": "Database Fix",
  "summary": "Como localizar contexto de banco antes de corrigir bug.",
  "content_path": "content/skills/database-fix.md",
  "tags": ["database", "sql", "bugfix"],
  "aliases": ["banco", "db", "migration"],
  "tokens_est": 420,
  "active": true,
  "exportable": true,
  "sensitive": false
}
```

Validacoes:

- categoria precisa existir e estar ativa;
- `title`: 3-120 chars;
- `summary`: 20 ate limite da categoria;
- `tags`: max 12, cada tag 1-32 chars;
- `aliases`: max 20;
- `content_path` nao pode sair de `.picr/content/`;
- se `sensitive=true`, painel deve exigir confirmacao para `exportable=true`.

## 4. RoutingLog

```json
{
  "id": "log_20260617_000001",
  "query": "corrigir erro no banco do Orion",
  "cli": "codex",
  "result_ids": ["item_skills_database_fix"],
  "opened_ids": ["item_skills_database_fix"],
  "tokens_est": 420,
  "outcome": "ok",
  "notes": "Resultado usado para localizar schema."
}
```

Validacoes:

- `outcome`: `ok`, `partial`, `failed`, `unknown`;
- `query`: obrigatoria;
- `tokens_est`: inteiro >= 0;
- `result_ids` e `opened_ids`: arrays.

## 5. Markdown item format

```markdown
# Database Fix

## Summary
Como localizar contexto de banco antes de corrigir bug.

## Metadata
- category: skills
- tags: database, sql, bugfix
- sensitive: false
- exportable: true

## Content
Texto completo.
```

Implementacao pode gerar frontmatter depois, mas MVP deve manter formato simples
e legivel.
