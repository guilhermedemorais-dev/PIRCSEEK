# Functional Spec: PIRCSEEK

## 1. Entidades funcionais

### Workspace

Raiz local do PIRCSEEK. Contem `.picr/`.

Estados:

- `not_initialized`: `.picr/` nao existe.
- `initialized`: estrutura existe e SQLite abre.
- `degraded`: estrutura existe, mas algum indice/path esta quebrado.
- `invalid`: banco ausente/corrompido ou schema invalido.

### Categoria

Modulo de organizacao criado pelo usuario.

Campos funcionais:

- nome humano;
- slug unico;
- descricao;
- prompt base;
- limites de resumo e tokens;
- estado ativo/inativo;
- ordem no menu;
- exportavel ou nao.

### Item

Unidade pesquisavel dentro de categoria.

Campos funcionais:

- titulo;
- resumo;
- conteudo Markdown;
- tags;
- aliases;
- path relativo;
- tokens estimados;
- sensivel;
- exportavel;
- ativo;
- metadados de criacao/edicao.

### Log de roteamento

Registro de uso do buscador.

Campos funcionais:

- query;
- CLI;
- resultados retornados;
- itens abertos quando informado;
- tokens estimados;
- outcome;
- notas.

## 2. Fluxos principais

### 2.1 Inicializar

Pre-condicao: usuario esta em pasta do projeto PIRCSEEK.

Fluxo:

1. Usuario roda `picr init`.
2. Sistema verifica se `.picr/` existe.
3. Se nao existe, cria estrutura.
4. Cria SQLite e aplica schema.
5. Cria categorias base.
6. Exporta indices vazios.
7. Retorna status.

Erros:

- Se `.picr/` existe sem `--force`, nao sobrescrever.
- Se SQLite nao abre, retornar `FAIL_DB_OPEN`.

### 2.2 Criar categoria pelo painel

Fluxo:

1. Usuario abre painel.
2. Clica em Categorias.
3. Preenche nome, slug, descricao e prompt base.
4. Sistema valida slug.
5. Sistema salva no SQLite.
6. Sistema reexporta `00-index.jsonl`.
7. Categoria aparece no menu lateral.

Validacoes:

- nome obrigatorio;
- slug obrigatorio;
- slug unico;
- slug apenas `[a-z0-9-]`;
- descricao recomendada com minimo 20 caracteres.

### 2.3 Criar item

Fluxo:

1. Usuario escolhe categoria.
2. Preenche titulo, resumo, tags e conteudo.
3. Sistema calcula tokens do conteudo.
4. Sistema alerta se exceder limite da categoria.
5. Usuario salva.
6. Sistema salva SQLite.
7. Sistema escreve Markdown.
8. Sistema exporta subindice.

Regra importante:

- Exceder limite gera aviso, nao corte automatico.

### 2.4 Buscar

Fluxo:

1. Usuario ou CLI envia query.
2. Sistema normaliza termos.
3. Sistema busca em categorias ativas.
4. Sistema calcula score.
5. Sistema retorna lista curta com metadados.
6. Sistema nao retorna conteudo Markdown inteiro.

Saida minima:

- id;
- categoria;
- titulo;
- resumo;
- path;
- tags;
- tokens_est;
- score;
- motivo do match.

### 2.5 Registrar resultado

Fluxo:

1. CLI ou usuario informa outcome.
2. Sistema grava log.
3. Logs com `ok` melhoram ranking futuro.
4. Logs com `failed` reduzem confianca futura se repetidos.

## 3. Estados de UI

Cada tela deve cobrir:

- loading;
- empty;
- error;
- dirty form;
- save success;
- validation error;
- offline/local only notice.

## 4. Regras de negocio

- LLM consome JSONL e Markdown sob demanda, nao SQLite diretamente.
- Painel usa SQLite como fonte operacional.
- Markdown e fonte humana completa.
- JSONL e cache exportado; pode ser recriado.
- Itens sensiveis devem mostrar alerta visual.
- Itens nao exportaveis nao podem aparecer no JSONL.
- Logs nao devem salvar conteudo completo.
- Busca sem resultado deve sugerir criar categoria/item, nao inventar match.

## 5. Criterios de aceite por fluxo

| Fluxo | Aceite |
|---|---|
| Inicializar | `.picr/`, banco e indices existem |
| Criar categoria | Categoria aparece no painel e no indice principal |
| Criar item | Item aparece na busca e tem Markdown criado |
| Buscar | Resultado contem path, resumo, score e tokens |
| Logar | Log aparece no painel e altera metricas |
| Doctor | Problemas aparecem com codigo, causa e correcao |
