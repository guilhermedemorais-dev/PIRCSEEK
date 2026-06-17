# Design System: PIRCSEEK

## 1. Direcao visual

PIRCSEEK e uma ferramenta operacional local. A interface deve ser densa,
organizada, rapida de escanear e sem aparencia de landing page.

Evitar:

- hero marketing;
- gradientes decorativos;
- cards demais sem funcao;
- visual generico de IA;
- excesso de roxo/azul escuro;
- textos explicando obviedades dentro da UI.

## 2. Layout

Estrutura principal:

```text
Sidebar fixa | Top search/status | Conteudo
```

Breakpoints:

- desktop: sidebar 240px, conteudo fluido;
- tablet: sidebar 220px;
- mobile: sidebar recolhida em drawer.

## 3. Cores

Paleta inicial:

| Token | Hex | Uso |
|---|---|---|
| `--bg` | `#F7F7F4` | fundo geral |
| `--surface` | `#FFFFFF` | paineis e tabelas |
| `--text` | `#1F2933` | texto principal |
| `--muted` | `#667085` | texto secundario |
| `--border` | `#D7DAE0` | bordas |
| `--accent` | `#256D63` | acao primaria |
| `--accent-2` | `#B66A2C` | destaque pontual |
| `--danger` | `#B42318` | erro |
| `--warning` | `#B54708` | alerta |
| `--success` | `#027A48` | sucesso |

## 4. Tipografia

- Fonte sistema: `Inter`, `Segoe UI`, `Roboto`, `Arial`, sans-serif.
- Base: 14px.
- Tabela/lista: 13px.
- Titulo de pagina: 22px, peso 650.
- Titulo de secao: 16px, peso 650.
- Monospace: `ui-monospace`, `SFMono-Regular`, `Consolas`, monospace.

Nao escalar fonte com viewport.

## 5. Componentes

### Sidebar

Itens:

- Dashboard
- Busca
- Categorias
- Items
- Indices
- Skills
- MCPs
- Memoria
- Projetos
- Prompts
- Ferramentas
- Logs
- Configuracoes

Estado ativo deve ser visual, nao apenas cor.

### Top Search

Campo de busca sempre visivel no desktop.

Deve mostrar:

- input;
- seletor de categoria opcional;
- limite de resultados;
- contador de tokens estimado do resultado.

### Result List

Cada resultado mostra:

- titulo;
- categoria;
- resumo;
- tags;
- path;
- tokens;
- score;
- match reasons.

### Forms

Campos obrigatorios marcados.

Validacao inline:

- slug invalido;
- resumo longo;
- item sensivel exportavel;
- tags demais.

### Tables

Usar para categorias, items e logs.

Colunas devem ser densas:

- status;
- titulo/nome;
- categoria;
- tokens;
- atualizado;
- acoes.

## 6. Estados obrigatorios

Cada tela deve ter:

- loading;
- empty;
- error;
- success;
- dirty changes;
- validation errors.

## 7. Acessibilidade

- contraste minimo AA;
- foco visivel;
- navegacao por teclado em formularios;
- labels associados aos inputs;
- botoes com texto claro;
- nao depender apenas de cor para status.

## 8. Design tokens JSON

Implementacao futura deve refletir estes tokens em `dashboard/style.css`.

```json
{
  "colors": {
    "bg": "#F7F7F4",
    "surface": "#FFFFFF",
    "text": "#1F2933",
    "muted": "#667085",
    "border": "#D7DAE0",
    "accent": "#256D63",
    "accent2": "#B66A2C",
    "danger": "#B42318",
    "warning": "#B54708",
    "success": "#027A48"
  },
  "radius": {
    "sm": "4px",
    "md": "6px",
    "lg": "8px"
  },
  "spacing": {
    "xs": "4px",
    "sm": "8px",
    "md": "12px",
    "lg": "16px",
    "xl": "24px"
  }
}
```
