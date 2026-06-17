# Error Handling: PIRCSEEK

## 1. Principio

Erro deve ser acionavel. Toda falha deve responder:

- o que falhou;
- por que provavelmente falhou;
- qual acao corrigir.

## 2. Codigos

| Codigo | Causa | Correcao |
|---|---|---|
| `WORKSPACE_NOT_INITIALIZED` | `.picr/` ausente | rodar `picr init` |
| `DB_OPEN_FAILED` | SQLite ausente/corrompido/permissao | verificar arquivo ou recriar backup |
| `SCHEMA_VERSION_UNSUPPORTED` | schema diferente | rodar migracao ou bloquear |
| `VALIDATION_ERROR` | entrada invalida | corrigir campo informado |
| `DUPLICATE_SLUG` | slug ja existe | escolher slug unico |
| `PATH_ESCAPE_BLOCKED` | tentativa de path traversal | bloquear path |
| `CONTENT_WRITE_FAILED` | falha ao escrever Markdown | verificar permissao |
| `INDEX_INVALID_JSONL` | JSONL quebrado | rodar `picr index` |
| `CONTENT_PATH_MISSING` | item aponta para Markdown ausente | corrigir path ou recriar item |
| `SEARCH_NO_RESULTS` | nenhum score positivo | criar item/categoria ou ajustar query |

## 3. Comportamento por interface

### CLI

Formato:

```text
FAIL VALIDATION_ERROR slug invalido: use apenas letras, numeros e hifen
```

### API

Formato:

```json
{"error":{"code":"VALIDATION_ERROR","message":"slug invalido","field":"slug"}}
```

### Painel

Mostrar:

- mensagem curta;
- campo afetado;
- acao recomendada;
- sem stacktrace por padrao.

## 4. Regras anti-corrupcao

- Escrever JSONL em arquivo temporario e mover ao final.
- Nao apagar Markdown se update de SQLite falhar.
- Nao confirmar update se path final sair de `.picr/`.
- Reindexacao deve ser idempotente.
