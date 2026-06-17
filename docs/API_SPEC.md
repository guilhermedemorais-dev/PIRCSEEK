# API Spec: PIRCSEEK Local Server

## 1. Base

Servidor local:

```text
http://127.0.0.1:8787
```

Nao expor em `0.0.0.0` no MVP.

## 2. Padrao de resposta

Sucesso:

```json
{"data":{}}
```

Erro:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "slug invalido",
    "field": "slug"
  }
}
```

## 3. Endpoints

### GET /api/health

Resposta:

```json
{"data":{"status":"ok","app":"PIRCSEEK","version":"0.1.0"}}
```

### GET /api/doctor

Resposta:

```json
{
  "data": {
    "status": "WARN",
    "checks": [
      {"name":"db_open","status":"OK","message":"SQLite abre"},
      {"name":"markdown_paths_valid","status":"WARN","message":"2 paths ausentes"}
    ]
  }
}
```

### GET /api/categories

Resposta:

```json
{"data":[{"id":"cat_skills","slug":"skills","name":"Skills","active":true}]}
```

### POST /api/categories

Payload:

```json
{
  "name": "Skills",
  "slug": "skills",
  "description": "Procedimentos reutilizaveis para CLIs de IA.",
  "prompt_md": "Use esta categoria quando..."
}
```

### PATCH /api/categories/:id

Payload parcial. Deve validar os mesmos campos.

### GET /api/items

Query:

- `category`
- `active`
- `q`

### POST /api/items

Payload:

```json
{
  "category_slug": "skills",
  "title": "Database Fix",
  "summary": "Como localizar contexto de banco antes de corrigir bug.",
  "content": "Texto completo",
  "tags": ["database", "sql"],
  "aliases": ["banco", "db"],
  "sensitive": false,
  "exportable": true
}
```

### PATCH /api/items/:id

Payload parcial. Recalcula tokens quando `content` ou `summary` mudar.

### GET /api/search

Query:

- `q`: obrigatorio;
- `limit`: default 10;
- `category`: opcional.

Resposta:

```json
{
  "data": {
    "query": "corrigir banco",
    "total_tokens_est": 420,
    "results": [
      {
        "id": "item_skills_database_fix",
        "category": "skills",
        "title": "Database Fix",
        "summary": "Como localizar contexto de banco antes de corrigir bug.",
        "path": "content/skills/database-fix.md",
        "tokens_est": 420,
        "score": 18,
        "match_reasons": ["tag:database"]
      }
    ]
  }
}
```

### POST /api/reindex

Reexporta JSONL.

### GET /api/logs

Lista logs paginados.

### POST /api/logs

Payload:

```json
{
  "query": "corrigir banco",
  "cli": "codex",
  "result_ids": ["item_skills_database_fix"],
  "opened_ids": ["item_skills_database_fix"],
  "tokens_est": 420,
  "outcome": "ok",
  "notes": ""
}
```

## 4. Codigos HTTP

| Codigo | Uso |
|---|---|
| 200 | GET/PATCH/POST com sucesso |
| 201 | criacao bem-sucedida |
| 400 | validacao |
| 404 | recurso inexistente |
| 409 | conflito, slug duplicado |
| 500 | erro interno |
