# Plano de Implementacao: PIRCSEEK

## Checkpoint 0: Documentacao corrigida

Entregas:

- PRD;
- Functional Spec;
- Technical Spec SDD;
- arquitetura;
- data model;
- API spec;
- error handling;
- design system;
- user flows;
- plano TDD;
- matriz de rastreabilidade;
- backlog;
- glossario.

Aceite:

- documentos explicam como construir o software;
- metodologia SDD/TDD aparece como processo, nao como texto decorativo.
- cada requisito P0 possui spec e teste mapeado.

## Checkpoint 1: CLI e estrutura local

Delegacao:

- Codex: criar testes iniciais, revisar arquitetura e validar `doctor`.
- Claude Code: implementar CLI minimo e modulos locais dentro do escopo definido.
- Gate: Codex roda testes e revisa diff antes de seguir.

Entregas:

- `tools/picr.py`;
- `tools/picr_core/`;
- `.picr/` inicial;
- comando `init`;
- comando `doctor`;
- testes de init e doctor.

Aceite:

- roda sem Docker;
- cria estrutura;
- doctor reporta OK/WARN/FAIL;
- path traversal bloqueado;
- schema version registrado.

## Checkpoint 2: Categorias e itens

Delegacao:

- Codex: definir testes de schema, validacao e edge cases.
- Claude Code: implementar schema SQLite, repositories e comandos CRUD.
- Gate: Codex valida path traversal, persistencia e JSON de erro.

Entregas:

- SQLite schema;
- `category add/list`;
- `item add/list`;
- geracao Markdown;
- validacoes de slug, resumo, tags, sensivel/exportavel;
- testes de categoria e item.

Aceite:

- cria categoria;
- cria item;
- gera arquivo Markdown.
- rejeita entrada invalida com erro acionavel.

## Checkpoint 3: Indexacao e busca

Delegacao:

- Codex: definir testes de ranking, JSONL e anti-quebra de contexto.
- Claude Code: implementar indexer, token estimate, search e ranking.
- Gate: Codex verifica que search nao imprime Markdown inteiro por default.

Entregas:

- `index`;
- `search`;
- export JSONL;
- ranking simples;
- token estimate;
- testes de JSONL e ranking.

Aceite:

- busca retorna resultados com tokens;
- JSONL valido;
- item inativo/exportable=false nao sai no indice.
- search nao imprime Markdown inteiro por default.
- ranking deterministico passa nos testes.

## Checkpoint 4: Logs

Delegacao:

- Codex: definir comportamento de logs e impacto no ranking.
- Claude Code: implementar logs SQLite/JSONL e comandos.
- Gate: Codex valida que logs nao salvam conteudo completo.

Entregas:

- `log`;
- logs SQLite;
- logs JSONL;
- outcome;
- testes de log.

Aceite:

- query e resultado ficam registrados;
- tokens estimados aparecem no log.
- outcome `ok` influencia ranking futuro conforme spec.

## Checkpoint 5: Painel local

Delegacao:

- Codex: validar design system, UX, estados e API contract.
- Claude Code: implementar servidor local, endpoints e UI basica.
- Gate: Codex faz QA visual/runtime e responsividade.

Entregas:

- servidor local;
- HTML/CSS/JS;
- design system implementado em CSS;
- busca;
- categorias;
- itens;
- logs;
- doctor no painel.

Aceite:

- abre em `127.0.0.1`;
- salva categoria e item;
- reindexa;
- busca no painel.
- estados loading, empty, error, validation e success existem.
- layout nao sobrepoe texto em desktop/mobile.

## Checkpoint 6: Integracao com CLIs

Delegacao:

- Codex: definir protocolo final de uso por CLI e revisar seguranca.
- Claude Code: criar exemplos/scripts auxiliares se necessario.
- Gate: Codex valida fluxo Codex/Claude com tarefa local pequena.

Entregas:

- exemplos para Codex;
- exemplos para Claude CLI;
- instrucao curta para plugins;
- comandos prontos de consulta.

Aceite:

- um CLI consegue consultar PIRCSEEK e abrir apenas paths recomendados.
- logs diferenciam `codex`, `claude` e outros CLIs.
