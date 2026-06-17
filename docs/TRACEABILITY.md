# Traceability Matrix: PIRCSEEK

Esta matriz liga requisito, especificacao, teste e aceite. Nenhum item P0 deve
ser implementado sem linha nesta matriz.

| Req | Descricao | Spec | Teste | Aceite |
|---|---|---|---|---|
| RF-001 | Inicializar workspace | SPEC 3.1, FUNCTIONAL 2.1 | `test_init_creates_workspace` | `.picr`, SQLite e indices existem |
| RF-002 | Criar categoria | SPEC 3.3, FUNCTIONAL 2.2, DATA_MODEL 2 | `test_category_add_persists_and_reindexes` | categoria no SQLite e `00-index.jsonl` |
| RF-003 | Editar categoria | API_SPEC PATCH categories | `test_category_update_preserves_items` | dados atualizados sem apagar itens |
| RF-004 | Desativar categoria | DATA_MODEL 2 | `test_inactive_category_hidden_from_default_search` | categoria nao aparece na busca padrao |
| RF-005 | Criar item | SPEC 3.4, DATA_MODEL 3 | `test_item_add_writes_db_markdown_jsonl` | SQLite, Markdown e JSONL gerados |
| RF-006 | Editar item | API_SPEC PATCH items | `test_item_update_recalculates_tokens_and_reindexes` | tokens e indice atualizados |
| RF-007 | Item sensivel/exportavel | SPEC 9, DATA_MODEL 3 | `test_non_exportable_sensitive_item_not_in_jsonl` | nao exporta se `exportable=false` |
| RF-008 | Buscar contexto | SPEC 3.5, SPEC 6 | `test_search_returns_ranked_metadata_only` | ranking com path, score e tokens |
| RF-009 | Registrar log | DATA_MODEL 4 | `test_log_records_query_cli_tokens_outcome` | log salvo e visivel |
| RF-010 | Doctor | SPEC 3.2 | `test_doctor_warns_on_missing_markdown_path` | OK/WARN/FAIL correto |
| RF-011 | Painel salvar dados | API_SPEC, USER_FLOWS | `test_api_create_category_and_item` | salvar via API persiste |
| RF-012 | Dashboard tokens | DESIGN_SYSTEM, API_SPEC logs | `test_dashboard_token_metrics_endpoint` | tokens por busca/categoria |
| RF-013 | Detectar CLIs | SPEC 3.2 | `test_doctor_detects_optional_clis_without_fail` | ausente gera INFO/WARN, nao FAIL |
| RNF-003 | Localhost | SPEC 7, ARCHITECTURE | `test_server_binds_localhost_by_default` | nao abre em `0.0.0.0` por padrao |
| SEC-001 | Path traversal | SPEC 9, ERROR_HANDLING | `test_path_traversal_is_blocked` | erro `PATH_ESCAPE_BLOCKED` |
| SEC-002 | JSONL seguro | SPEC 5, DATA_MODEL | `test_jsonl_uses_relative_paths` | sem path absoluto |

## Regra de manutencao

Ao adicionar requisito:

1. adicionar no PRD;
2. detalhar em SPEC/FUNCTIONAL/API/DATA_MODEL conforme aplicavel;
3. adicionar teste no TEST_PLAN;
4. adicionar linha nesta matriz;
5. so entao implementar.
