# User Flows: PIRCSEEK

## 1. Primeira execucao

```text
Abrir terminal
-> picr init
-> picr doctor
-> picr serve
-> abrir painel
```

Aceite:

- usuario entende status do sistema;
- se algo falhar, doctor informa correcao.

## 2. Criar categoria

```text
Painel
-> Categorias
-> Nova categoria
-> preencher nome/slug/descricao/prompt
-> salvar
-> categoria aparece na sidebar e no indice
```

Edge cases:

- slug duplicado;
- slug invalido;
- descricao vazia;
- prompt longo.

## 3. Criar skill/item

```text
Painel
-> escolher categoria
-> Novo item
-> preencher titulo/resumo/tags/conteudo
-> revisar tokens
-> salvar
-> item aparece na busca
```

Edge cases:

- resumo curto demais;
- conteudo excede limite;
- item sensivel e exportavel;
- falha ao escrever Markdown.

## 4. Buscar como humano

```text
Painel
-> Busca
-> digitar query
-> ver resultados ranqueados
-> abrir Markdown se necessario
-> copiar path/comando para CLI
```

Aceite:

- resultado mostra motivo do match;
- resultado mostra tokens;
- resultado mostra path.

## 5. Buscar como CLI

```text
Codex/Claude
-> picr search "corrigir banco orion" --format json
-> recebe paths/resumos/tokens
-> abre arquivos relevantes
-> executa tarefa
-> picr log --outcome ok
```

Aceite:

- JSON nao contem Markdown completo;
- path e relativo;
- resultado e deterministico.

## 6. Revisar logs

```text
Painel
-> Logs
-> filtrar por CLI/categoria/outcome
-> identificar queries sem resultado
-> criar categoria/item novo se necessario
```

Aceite:

- logs ajudam a melhorar o indice;
- logs nao vazam conteudo sensivel completo.
