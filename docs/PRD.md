# PRD: PIRCSEEK

## 1. Visao

PIRCSEEK e um buscador local de contexto para CLIs de IA. Ele permite que Codex,
Claude CLI e outros agentes encontrem o contexto correto antes de carregar
skills, MCPs, memorias, prompts, documentos e arquivos de projeto no prompt.

O produto existe para economizar tokens e reduzir erro operacional. Ele nao e um
agente executor. Ele e uma camada local de descoberta, organizacao e recuperacao
de contexto.

## 2. Tese do produto

Humanos usam buscadores para encontrar informacao antes de agir. LLMs devem usar
um buscador local para encontrar contexto de trabalho antes de raciocinar com
arquivos demais.

```text
Google -> humano pesquisando a web.
PIRCSEEK -> LLM pesquisando o ambiente local de trabalho.
```

## 3. Problema

Hoje, CLIs de IA tendem a:

- ler muitos arquivos sem saber se sao relevantes;
- carregar skills globais demais;
- repetir busca manual em projetos, memorias e docs;
- perder decisoes anteriores;
- depender de conversa longa para lembrar contexto;
- misturar busca, planejamento e execucao no mesmo prompt;
- gastar tokens antes de saber qual informacao realmente importa.

Isso gera custo, lentidao, ruido, alucinacao e implementacoes com bug herdado.

## 4. Solucao

PIRCSEEK entrega um fluxo local:

```text
1. Usuario pede tarefa ao Codex/Claude.
2. CLI consulta PIRCSEEK com a intencao da tarefa.
3. PIRCSEEK busca em indices locais.
4. PIRCSEEK retorna resultados ranqueados com path, resumo, categoria e tokens.
5. CLI abre apenas os arquivos recomendados que julgar necessarios.
6. CLI executa a tarefa.
7. PIRCSEEK registra a rota e o outcome para melhorar buscas futuras.
```

## 5. Usuarios e casos de uso

### Usuario primario

Guilherme, trabalhando com desenvolvimento, DevOps, QA, seguranca, automacoes e
LLM systems usando multiplos CLIs.

### Casos de uso MVP

| Caso | Descricao | Resultado esperado |
|---|---|---|
| Buscar contexto para bug | Usuario pede correcao; CLI consulta PIRCSEEK | Lista curta de arquivos e memorias relevantes |
| Cadastrar skill | Usuario escreve skill no painel | Markdown completo + JSONL indexado |
| Criar categoria | Usuario cria modulo novo, ex: GitHub repos | Categoria aparece no menu e em `00-index.jsonl` |
| Registrar MCP | Usuario cadastra quando usar um MCP | MCP pode aparecer em buscas futuras |
| Revisar logs | Usuario ve consultas e tokens | Dashboard mostra uso por CLI/categoria |
| Diagnosticar instalacao | Usuario roda doctor | Status OK/WARN/FAIL com acoes claras |

## 6. Escopo MVP

### Incluido

- CLI Python local.
- Painel HTML local com servidor Python em `127.0.0.1`.
- SQLite local em `.picr/picr.db`.
- Markdown completo em `.picr/content/`.
- JSONL exportado em `.picr/00-index.jsonl` e `.picr/indexes/`.
- Categorias configuraveis.
- Busca textual local com ranking deterministico.
- Uso de `rg` quando existir e fallback Python.
- Estimativa de tokens `ceil(chars / 4)`.
- Logs de roteamento e tokens.
- Doctor de saude local.
- Design system documentado para implementar painel consistente.

### Fora do MVP

- Busca web propria.
- Embeddings.
- Banco vetorial.
- Docker.
- Multiusuario.
- Login.
- Sincronizacao cloud.
- Auto-resumo agressivo.
- Agente autonomo executor.

## 7. Requisitos funcionais

| ID | Requisito | Prioridade | Aceite |
|---|---|---|---|
| RF-001 | Inicializar workspace `.picr` | P0 | `picr init` cria pastas, banco e indices sem sobrescrever dados |
| RF-002 | Criar categoria | P0 | Categoria salva, aparece no painel e em `00-index.jsonl` |
| RF-003 | Editar categoria | P0 | Alteracao persiste e reindexa sem perder itens |
| RF-004 | Desativar categoria | P1 | Categoria nao aparece para busca padrao, mas dados permanecem |
| RF-005 | Criar item | P0 | Item salva SQLite, Markdown e JSONL |
| RF-006 | Editar item | P0 | Markdown e indice refletem alteracao |
| RF-007 | Marcar item sensivel | P0 | Painel alerta e JSONL respeita `exportable` |
| RF-008 | Buscar contexto | P0 | Retorna resultados ranqueados com tokens e paths relativos |
| RF-009 | Registrar log | P0 | Query, CLI, resultados, tokens e outcome sao gravados |
| RF-010 | Doctor | P0 | Retorna OK/WARN/FAIL e problemas acionaveis |
| RF-011 | Painel salvar dados | P0 | CRUD local funciona sem internet |
| RF-012 | Dashboard de tokens | P1 | Mostra tokens por busca, CLI, categoria e item |
| RF-013 | Detectar CLIs | P1 | Lista Codex, Claude, rg, Python e paths quando presentes |
| RF-014 | Importar pasta local | P2 | Cria itens a partir de arquivos selecionados |

## 8. Requisitos nao funcionais

| ID | Requisito | Criterio |
|---|---|---|
| RNF-001 | Offline | Todas as funcoes MVP rodam sem internet |
| RNF-002 | Sem Docker | Nenhum comando MVP exige container |
| RNF-003 | Localhost | Servidor escuta em `127.0.0.1` por padrao |
| RNF-004 | Baixo token | Busca retorna metadados, nao Markdown inteiro |
| RNF-005 | Versionavel | Conteudo Markdown e indices podem ir para Git |
| RNF-006 | Recuperavel | Dados principais podem ser recriados do SQLite + Markdown |
| RNF-007 | Seguro por padrao | Itens sensiveis nao exportam se `exportable=false` |
| RNF-008 | Deterministico | Ranking igual para mesma base e mesma query |

## 9. Principios de decisao

- Se um resumo pode causar perda de informacao, retornar path em vez de cortar
  conteudo.
- Se uma categoria nova pode ser generica, permitir mesmo assim, mas exigir
  descricao, prompt base e limites.
- Se um arquivo e sensivel, nao exportar para JSONL por padrao.
- Se a busca nao encontrar resultado, retornar vazio com sugestao de categorias,
  nunca inventar.
- Se o indice estiver quebrado, doctor deve falhar antes de qualquer automacao.

## 10. Metricas

- `tokens_est_total` por busca.
- `results_count` por busca.
- `opened_items_count` informado por log.
- `outcome` por CLI.
- categorias mais usadas.
- itens mais usados.
- queries sem resultado.
- economia estimada: `all_indexed_tokens - returned_tokens`.

## 11. Definition of Done do MVP

- `picr init`, `doctor`, `category`, `item`, `index`, `search`, `log` funcionam.
- Painel local cria categoria e item.
- Busca no painel e no CLI retorna ranking com tokens.
- Markdown nao e cortado automaticamente.
- JSONL e valido linha a linha.
- Doctor identifica path quebrado e indice invalido.
- Testes P0 passam.
- Documentacao de uso corresponde ao comportamento real.
