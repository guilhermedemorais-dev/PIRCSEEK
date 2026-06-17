# PIRCSEEK

PIRCSEEK e um buscador local de contexto para CLIs de IA.

O nome une `PIRC`, a metodologia de recuperacao progressiva de contexto, com
`SEEK`, do verbo procurar/buscar. A ideia central e simples: humanos usam Google
para achar informacao; LLMs e CLIs como Codex e Claude devem usar o PIRCSEEK
para achar contexto local antes de gastar tokens lendo skills, MCPs, memorias,
docs e arquivos de projeto.

PIRCSEEK nao executa a tarefa. Ele localiza o contexto certo, informa custo
estimado de tokens e entrega caminhos para o CLI executar melhor.

## Documentacao

- [PRD](docs/PRD.md): visao de produto, usuarios, problemas, requisitos e sucesso.
- [FUNCTIONAL_SPEC](docs/FUNCTIONAL_SPEC.md): fluxos funcionais, entidades, estados e regras.
- [SPEC](docs/SPEC.md): especificacao tecnica SDD com CLI, schema, API, ranking e erros.
- [DATA_MODEL](docs/DATA_MODEL.md): contratos de dados, validacoes e exemplos.
- [API_SPEC](docs/API_SPEC.md): endpoints locais do painel.
- [ARCHITECTURE](docs/ARCHITECTURE.md): arquitetura local e decisoes rejeitadas.
- [DESIGN_SYSTEM](docs/DESIGN_SYSTEM.md): direcao visual, tokens, componentes e estados.
- [USER_FLOWS](docs/USER_FLOWS.md): fluxos principais e edge cases.
- [ERROR_HANDLING](docs/ERROR_HANDLING.md): codigos de erro e comportamento por interface.
- [CLI_DELEGATION_TOOL](docs/CLI_DELEGATION_TOOL.md): wrapper local para chamar Codex/Claude com prompt salvo e log.
- [TEST_PLAN](docs/TEST_PLAN.md): plano TDD com testes que devem guiar o codigo.
- [TRACEABILITY](docs/TRACEABILITY.md): matriz requisito -> especificacao -> teste.
- [DELEGATION_PLAN](docs/DELEGATION_PLAN.md): divisao estrategica entre Codex, Claude Code e validacoes.
- [Prompts operacionais](docs/prompts/README.md): prompts prontos para Codex e Claude executarem checkpoints.
- [IMPLEMENTATION_PLAN](docs/IMPLEMENTATION_PLAN.md): checkpoints de entrega.
- [BACKLOG](docs/BACKLOG.md): backlog inicial priorizado.
- [GLOSSARIO](docs/GLOSSARIO.md): termos do projeto.

## Decisoes fechadas

- Tudo local em uma pasta.
- Sem Docker no MVP.
- Web search fora do MVP; cada CLI usa suas proprias ferramentas web.
- SQLite local em `.picr/picr.db` para gestao do painel.
- JSONL como indice barato para LLMs.
- Markdown como conteudo completo e legivel.
- Python para CLI, indexacao, busca, logs e servidor local do painel.
- Painel HTML local para o usuario gerenciar categorias, skills, MCPs, memorias,
  prompts, projetos e ferramentas.
- O plugin principal continua executando trabalho; PIRCSEEK e camada auxiliar de
  busca e contexto.

## Estado

Documentacao de escopo e especificacao criada. Implementacao ainda nao iniciada.
