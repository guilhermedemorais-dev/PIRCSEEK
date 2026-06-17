# Architecture: PIRCSEEK

## 1. Decisao arquitetural

PIRCSEEK usa arquitetura local, simples e auditavel:

- SQLite local para estado operacional.
- Markdown para conteudo completo.
- JSONL para metadados consumidos por LLMs.
- Python para CLI, API local, busca, indexacao e doctor.
- HTML/CSS/JS para painel local.

## 2. Diagrama de contexto

```text
Usuario
  -> Painel local
      -> API Python
          -> SQLite
          -> Markdown
          -> JSONL

Codex / Claude / outro CLI
  -> picr search
      -> JSONL + SQLite + rg
      -> paths/resumos/tokens
  -> abre Markdown relevante
  -> executa tarefa
  -> picr log
```

## 3. Fluxo de persistencia

```text
Salvar item
  -> valida payload
  -> grava SQLite
  -> escreve Markdown completo
  -> exporta subindice JSONL
  -> atualiza 00-index.jsonl
```

SQLite e fonte operacional. JSONL e artefato exportado. Markdown e fonte humana
completa.

## 4. Componentes

| Componente | Responsabilidade | Nao deve fazer |
|---|---|---|
| `db.py` | conexao, schema, migrations | regra de UI |
| `models.py` | validacao de entidades | acesso ao filesystem |
| `markdown_store.py` | ler/escrever Markdown seguro | ranking |
| `indexer.py` | exportar JSONL | buscar web |
| `search.py` | montar resultados | executar tarefas |
| `ranking.py` | pontuacao deterministica | alterar banco |
| `doctor.py` | diagnostico local | reparar automaticamente |
| `server.py` | API localhost | expor rede externa |
| `dashboard/` | interface humana | conter regra critica sem backend |

## 5. Dados e privacidade

- Tudo fica local.
- Itens sensiveis podem existir no SQLite/Markdown.
- Itens sensiveis com `exportable=false` nao entram no JSONL.
- JSONL e tratado como material que LLM pode ler.
- Logs registram metadados, nao conteudo completo.

## 6. Performance esperada MVP

Alvo inicial:

- ate 5.000 itens sem embeddings;
- busca textual em menos de 1s para indices pequenos/medios;
- JSONL principal abaixo de 1.500 tokens sempre que possivel;
- subindice por categoria abaixo de 3.000 tokens quando possivel.

Quando passar disso, considerar paginacao, filtros obrigatorios ou indice mais
sofisticado. Embeddings continuam fora do MVP.

## 7. Decisoes rejeitadas

| Decisao rejeitada | Motivo |
|---|---|
| Docker no MVP | custo operacional sem ganho |
| Somente JSONL | ruim para painel editar e logar |
| Somente SQLite | LLM leria formato ruim/indireto |
| Auto-resumo agressivo | risco de quebrar contexto |
| Busca web propria | fora do foco; CLIs ja possuem ferramentas |
| Agente executor | PIRCSEEK deve buscar, nao implementar |
