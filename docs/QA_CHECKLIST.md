# QA Checklist: PIRCSEEK

## Banco

- SQLite criado em `.picr/picr.db`.
- `schema_version` existe.
- Tabelas existem.
- Slugs duplicados sao bloqueados.
- Item nao referencia categoria inexistente.
- Logs nao salvam conteudo completo.

## API/Backend

- Servidor escuta em `127.0.0.1`.
- Endpoints retornam JSON padronizado.
- Erros possuem `code`, `message` e `field` quando aplicavel.
- Path traversal bloqueado.
- Reindexacao e idempotente.
- JSONL escrito de forma atomica.
- Doctor detecta indice quebrado.

## Frontend/UI

- Sidebar renderiza todos os modulos.
- Busca mostra loading, resultado, vazio e erro.
- Forms mostram validacao inline.
- Token status aparece na busca e nos itens.
- Item sensivel mostra alerta.
- Botao salvar desabilita durante envio.
- Layout desktop e mobile nao sobrepoe texto.
- Foco de teclado visivel.

## Workflow/Plugins

- PIRCSEEK retorna contexto, nao executa tarefa.
- Codex/Claude recebem paths e resumos.
- Search nao retorna Markdown completo por default.
- Logs diferenciam CLI usado.

## Security

- Nenhuma chamada web no MVP.
- Nenhum segredo exportado automaticamente.
- Itens `exportable=false` ficam fora do JSONL.
- Servidor local nao exposto externamente por padrao.

## Release gate

MVP nao pode ser marcado como pronto se:

- testes P0 falham;
- doctor tem FAIL;
- painel nao salva categoria/item;
- search nao retorna tokens;
- JSONL invalido;
- docs divergem do comportamento implementado.
