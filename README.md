# PIRCSEEK

PIRCSEEK e um buscador local de contexto para LLMs, agentes e CLIs de IA.

O projeto nasce dos estudos de Guilherme de Morais sobre a metodologia
[`LLM-PICR-METHODOLOGY`](https://github.com/guilhermedemorais-dev/LLM-PICR-METHODOLOGY),
onde `PICR` significa `Progressive Indexed Context Retrieval`: uma forma de
fazer modelos de linguagem encontrarem o contexto correto de maneira
progressiva, indexada e sob demanda, em vez de carregar tudo no prompt.

O nome une:

- `PIRC`: a metodologia de recuperacao progressiva e indexada de contexto.
- `SEEK`: o verbo procurar, buscar.

Em termos diretos: humanos usam Google para encontrar informacao antes de agir.
LLMs e CLIs como Codex, Claude Code e outros devem usar o PIRCSEEK para
encontrar o contexto local correto antes de gastar tokens lendo skills, MCPs,
memorias, prompts, documentacao e arquivos de projeto.

## Problema

Agentes de IA locais tendem a desperdicar contexto por tres motivos:

1. carregam muitas skills e instrucoes antes de saber se elas sao necessarias;
2. procuram arquivos manualmente, lendo mais conteudo do que o necessario;
3. perdem memoria operacional entre tarefas, repetindo buscas e decisoes.

Isso aumenta custo de tokens, latencia, ruido no raciocinio e chance de
alucinacao. O problema nao e falta de contexto. O problema e contexto demais,
na ordem errada, sem ranking, sem resumo e sem memoria de resultado.

## Tese do projeto

PIRCSEEK implementa a ideia central do PICR:

> substituir maximo contexto por contexto correto.

O sistema nao tenta fazer o trabalho do Codex, Claude Code ou outros CLIs. Ele
atua como uma camada local de recuperacao, organizacao e roteamento de contexto.

O agente pergunta ao PIRCSEEK o que precisa saber. O PIRCSEEK retorna:

- categorias relevantes;
- itens candidatos;
- caminhos dos arquivos;
- resumos curtos;
- estimativa de tokens;
- score/ranking;
- historico de uso quando existir;
- indicacao de qual skill, MCP, prompt, memoria ou documento abrir.

O CLI continua responsavel por executar a tarefa. O PIRCSEEK reduz o custo de
descobrir qual contexto deve ser usado.

## Origem: LLM-PICR-METHODOLOGY

O repositorio
[`LLM-PICR-METHODOLOGY`](https://github.com/guilhermedemorais-dev/LLM-PICR-METHODOLOGY)
define a metodologia `Progressive Indexed Context Retrieval`.

O fluxo base da metodologia e:

1. interpretar a tarefa;
2. consultar um catalogo primario curto;
3. selecionar um catalogo de dominio;
4. ranquear candidatos;
5. ler somente o item escolhido;
6. executar;
7. registrar o resultado como memoria.

PIRCSEEK e a evolucao pratica dessa metodologia para uso diario em ambiente
local. A metodologia original pode funcionar com Obsidian, catalogos Markdown e
ferramentas simples de roteamento. O PIRCSEEK transforma esse conceito em um
produto local mais operacional:

- painel HTML para gestao humana;
- SQLite local para estado e consultas estruturadas;
- JSONL barato para leitura por LLM;
- Markdown para conteudo completo e auditavel;
- CLI Python para indexar, buscar, registrar e diagnosticar;
- logs de uso para memoria operacional;
- integracao com plugins e workflows de desenvolvimento.

## Relacao com Dev-workflow

PIRCSEEK foi pensado para funcionar junto com o repositorio
[`Dev-workflow`](https://github.com/guilhermedemorais-dev/Dev-workflow).

O `Dev-workflow` contem plugins publicos que padronizam desenvolvimento,
documentacao, UI/UX, seguranca, QA, pesquisa tecnica e delegacao entre agentes.
Os principais plugins previstos para operar com PIRCSEEK sao:

| Plugin | Papel no ecossistema |
| --- | --- |
| `dev-workflow-standard` | Workflow principal de desenvolvimento: PRD, pesquisa, spec, implementacao, revisao, testes, QA, seguranca e entrega por camadas. |
| `ui-ux-standard` | Padrao para design system, mockups, responsividade, acessibilidade, validacao visual e fluxos de interface. |
| `security-standard` | Revisao e hardening de seguranca proporcional ao risco da mudanca. |

A relacao correta e:

- `Dev-workflow` continua sendo o conjunto de plugins que executa e governa o
  trabalho.
- `PIRCSEEK` vira a camada de busca local, indice, memoria e recuperacao de
  contexto.
- Os plugins consultam o PIRCSEEK para encontrar a skill, regra, MCP, prompt,
  documento ou memoria correta antes de carregar conteudo grande.

Ou seja: PIRCSEEK nao substitui o workflow. Ele torna o workflow mais barato,
mais rapido e mais preciso.

## Como o PIRCSEEK funciona

O conceito operacional e parecido com um buscador local para agentes.

```text
Usuario
  pede uma tarefa ao Codex, Claude Code ou outro CLI
    |
    v
CLI de IA
  pergunta ao PIRCSEEK qual contexto usar
    |
    v
PIRCSEEK
  consulta memoria, indices, categorias, skills, MCPs, prompts e projetos
    |
    v
Resultado
  retorna paths, resumos, ranking e tokens estimados
    |
    v
CLI de IA
  abre apenas os arquivos necessarios e executa a tarefa
```

Exemplo pratico:

```text
Tarefa: "corrigir problema no banco de dados do projeto X"

Sem PIRCSEEK:
- o agente pode ler PRD inteiro;
- pode abrir skills erradas;
- pode procurar arquivos demais;
- pode esquecer decisoes anteriores;
- pode gastar tokens antes de entender onde agir.

Com PIRCSEEK:
- busca categoria "database";
- encontra skill de banco;
- encontra docs do projeto X;
- retorna paths de schema/migrations/spec;
- mostra resumo curto e tokens estimados;
- registra se a rota funcionou.
```

## O que pode ser catalogado

PIRCSEEK foi desenhado para categorias flexiveis. O usuario pode criar quantas
categorias precisar, sem ficar preso a uma taxonomia fixa.

Categorias previstas:

- skills;
- MCPs;
- memorias;
- prompts;
- regras de projeto;
- documentacao tecnica;
- repositorios GitHub;
- projetos locais;
- padroes de UI/UX;
- padroes de seguranca;
- comandos recorrentes;
- decisoes arquiteturais;
- runbooks;
- checklists de QA;
- exemplos de implementacao.

Cada item pode ter:

- titulo;
- resumo curto;
- categoria;
- tags;
- caminho do arquivo;
- tipo de conteudo;
- custo estimado em tokens;
- prioridade;
- sensibilidade;
- flag de exportacao para indice LLM;
- historico de uso.

## Por que nao usar apenas Obsidian

A metodologia PICR original considera Obsidian como uma forma humana de manter
um vault organizado. Isso continua valido.

Mas o objetivo do PIRCSEEK e diferente: criar uma camada operacional local para
CLIs de IA. O painel HTML e o indice local substituem a obrigatoriedade de usar
Obsidian.

Decisao do projeto:

- Obsidian pode ser usado como fonte ou inspiracao.
- Obsidian nao e dependencia obrigatoria.
- O sistema deve funcionar localmente com arquivos, SQLite, JSONL, Markdown e
  Python.

## Arquitetura local

PIRCSEEK deve rodar localmente, sem Docker no MVP.

Componentes planejados:

```text
PIRCSEEK/
  .picr/
    picr.db                  # SQLite local
    indexes/
      00-index.jsonl         # indice primario curto
      <categoria>.jsonl      # subindices por categoria
    logs/
      routing.jsonl          # memoria de rotas e resultados
      delegations/           # logs de chamadas Codex/Claude
    content/
      skills/
      mcps/
      memories/
      prompts/
      projects/
  docs/
  tools/
    delegate_cli.py          # ferramenta atual para delegar CLI com log
    picr.py                  # CLI principal planejado
  dashboard/
    index.html               # painel local planejado
```

### SQLite

Usado para estado local, CRUD do painel, filtros, historico e consultas
estruturadas. Fica dentro da pasta do projeto, em `.picr/picr.db`.

Nao exige Docker, servidor externo ou internet.

### JSONL

Usado como formato barato para LLMs. Cada linha contem um registro curto,
facil de ler sob demanda, sem carregar Markdown completo.

### Markdown

Usado para conteudo completo, humano, versionavel e auditavel.

### Python

Usado para CLI, indexacao, busca, estimativa de tokens, logs, diagnostico e
servidor local simples do painel.

## Economia de tokens

PIRCSEEK nao promete economia magica. A economia vem de reduzir leitura
desnecessaria.

O sistema deve evitar:

- carregar todas as skills;
- carregar todos os MCPs;
- ler documentacao inteira antes de classificar a tarefa;
- repetir busca que ja teve resultado bom;
- jogar historico grande no prompt;
- resumir agressivamente a ponto de quebrar contexto.

Regra pragmatica do projeto:

> o PIRCSEEK deve apontar o contexto, nao mutilar o contexto.

Por isso o `pack_context` agressivo nao e o centro do MVP. O foco e busca,
ranking, caminhos, resumos curtos e token accounting. Quando o agente precisar
de detalhe, ele abre o Markdown original.

## Painel local

O painel HTML planejado e parte importante do projeto porque o usuario precisa
gerenciar o sistema sem editar todos os arquivos manualmente.

O painel deve permitir:

- pesquisar como em um buscador;
- ver categorias no menu lateral;
- criar categorias personalizadas;
- registrar skills;
- registrar MCPs;
- registrar prompts;
- registrar memorias;
- registrar repositorios GitHub;
- registrar pastas de projetos locais;
- ver estimativa de tokens;
- ver quais CLIs estao instalados;
- ver logs de uso;
- editar conteudo em linguagem natural;
- salvar conteudo em formato otimizado para leitura por LLM.

O painel nao deve depender de internet para funcionar.

## Delegacao para Codex e Claude

O projeto tambem documenta e testa uma ferramenta auxiliar:

```text
tools/delegate_cli.py
```

Ela resolve um problema pratico: chamar CLIs locais com prompt salvo, log,
estimativa de tokens e modo visivel.

O fluxo correto para Claude Code e visivel/interativo:

```bash
python3 tools/delegate_cli.py \
  --cli claude \
  --mode visible \
  --prompt-file docs/prompts/claude-c1-implementation.md \
  --cwd /home/guimp/PIRCSEEK
```

Claude headless fica bloqueado por padrao. Para rodar sem tela, e necessario
explicitar:

```bash
--allow-headless-claude
```

Isso evita delegacao escondida quando o objetivo e ver o Claude trabalhando na
tela.

## Escopo do MVP

O MVP do PIRCSEEK deve entregar:

1. inicializacao local do workspace `.picr`;
2. schema SQLite;
3. CRUD de categorias e itens;
4. Markdown como fonte completa;
5. JSONL como indice LLM-friendly;
6. busca local por categoria, tag, titulo, resumo e fallback por `rg`;
7. ranking simples e auditavel;
8. estimativa de tokens;
9. logs de busca, rota e resultado;
10. painel HTML local;
11. diagnostico de ambiente;
12. deteccao de CLIs instalados;
13. integracao operacional com Codex/Claude via prompts curtos.

Fora do MVP:

- busca web propria;
- RAG vetorial complexo;
- LLM nativa embutida;
- Docker obrigatorio;
- microservicos;
- sincronizacao cloud;
- execucao autonoma de tarefas sem revisao do CLI principal.

## Status atual

Este repositorio esta no inicio da implementacao.

Ja existe:

- PRD completo;
- especificacao funcional;
- especificacao tecnica SDD;
- data model;
- API spec local;
- arquitetura;
- design system;
- user flows;
- error handling;
- plano TDD;
- matriz de rastreabilidade;
- plano de delegacao Codex/Claude;
- prompts operacionais;
- ferramenta `delegate_cli.py`;
- testes unitarios da ferramenta de delegacao.

Ainda falta implementar:

- CLI principal `picr`;
- SQLite real do PIRCSEEK;
- indexador principal;
- busca/ranking;
- painel HTML;
- CRUD operacional;
- dashboard de tokens;
- integracao completa com os plugins.

## Documentacao do projeto

| Documento | Finalidade |
| --- | --- |
| [PRD](docs/PRD.md) | Visao de produto, problema, usuarios, requisitos e sucesso. |
| [FUNCTIONAL_SPEC](docs/FUNCTIONAL_SPEC.md) | Fluxos funcionais, entidades, estados e regras. |
| [SPEC](docs/SPEC.md) | Especificacao tecnica SDD com CLI, schema, API, ranking e erros. |
| [DATA_MODEL](docs/DATA_MODEL.md) | Contratos de dados, validacoes e exemplos. |
| [API_SPEC](docs/API_SPEC.md) | Endpoints locais do painel. |
| [ARCHITECTURE](docs/ARCHITECTURE.md) | Arquitetura local e decisoes rejeitadas. |
| [DESIGN_SYSTEM](docs/DESIGN_SYSTEM.md) | Direcao visual, tokens, componentes e estados. |
| [USER_FLOWS](docs/USER_FLOWS.md) | Fluxos principais e edge cases. |
| [ERROR_HANDLING](docs/ERROR_HANDLING.md) | Codigos de erro e comportamento por interface. |
| [CLI_DELEGATION_TOOL](docs/CLI_DELEGATION_TOOL.md) | Wrapper local para Codex/Claude com prompt salvo e log. |
| [TEST_PLAN](docs/TEST_PLAN.md) | Plano TDD que deve guiar a implementacao. |
| [TRACEABILITY](docs/TRACEABILITY.md) | Matriz requisito -> especificacao -> teste. |
| [DELEGATION_PLAN](docs/DELEGATION_PLAN.md) | Divisao estrategica entre Codex, Claude Code e validacoes. |
| [Prompts operacionais](docs/prompts/README.md) | Prompts prontos para executar checkpoints. |
| [IMPLEMENTATION_PLAN](docs/IMPLEMENTATION_PLAN.md) | Checkpoints de entrega. |
| [BACKLOG](docs/BACKLOG.md) | Backlog inicial priorizado. |
| [GLOSSARIO](docs/GLOSSARIO.md) | Termos do projeto. |

## Como validar o estado atual

Por enquanto, a validacao automatizada cobre a ferramenta de delegacao.

```bash
python3 -m unittest discover -s tests
```

Resultado esperado:

```text
Ran 6 tests
OK
```

## Repositorios relacionados

- [`LLM-PICR-METHODOLOGY`](https://github.com/guilhermedemorais-dev/LLM-PICR-METHODOLOGY):
  estudo e metodologia base de recuperacao progressiva de contexto.
- [`Dev-workflow`](https://github.com/guilhermedemorais-dev/Dev-workflow):
  plugins de workflow, UI/UX e seguranca que devem consultar o PIRCSEEK como
  camada local de busca e memoria.

## Licenca

MIT.
