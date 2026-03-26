# Diretrizes para Diagramas de Sequencia

Este documento define padroes para criacao e manutencao de diagramas em `docs/diagramas-de-sequencia`.
O objetivo e manter os diagramas claros, consistentes e uteis para leitura tecnica.

## Nomenclatura de Arquivos

- Use `kebab-case`.
- Use o idioma principal do projeto.
- Escolha um nome curto e especifico para o fluxo representado.

Exemplos:

- `processamento-de-pedido.md`
- `cadastro-de-usuario.md`
- `sincronizacao-diaria-dados.md`

## Estrutura Minima do Arquivo

Cada arquivo `.md` deve ter:

1. Titulo H1.
Padrao sugerido: `# Diagrama de Sequencia - <Nome do Fluxo>`

2. Breve descricao.
Explique o objetivo do fluxo, o contexto e os atores principais.

3. Um ou mais blocos `mermaid`.

## Padrao Mermaid

### Tema

Se o repositorio nao definir outro tema, use este bloco de inicializacao:

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#F4F4F4', 'primaryTextColor': '#333333', 'lineColor': '#546E7A', 'actorBkg': '#4285F4', 'actorTextColor': '#ffffff', 'participantBkg': '#4285F4', 'participantTextColor': '#ffffff'}}}%%
```

### Participantes e aliases

- Use `participant Alias as Nome Legivel`.
- O alias deve ser curto, estavel e sem caracteres especiais.
- O nome legivel deve ser especifico.
- Para UI, prefira a tela real em vez de rotulos genericos como `Frontend`.

Exemplos:

```mermaid
participant Ctrl as OrderController
participant CheckoutView as View: CheckoutPage
participant DB as Banco de Dados
```

Evite:

- aspas desnecessarias no nome exibido
- aliases com espacos ou hifens
- nomes vagos quando for possivel identificar o componente real

### Mensagens

- Use `autonumber`.
- Nao numere manualmente as mensagens.
- Seja especifico sobre a acao, por exemplo `POST /orders` ou `SalvarPedido(dto)`.

### Espacos e caracteres especiais

- Nao use `&nbsp;` ou outros espacos nao padrao.
- Evite caracteres que possam quebrar o parser do Mermaid sem necessidade.

### Ativacao

Use `activate` e `deactivate` quando isso deixar o fluxo mais claro.

## Multiplos Fluxos

Quando um metodo central e invocado por varios casos de uso:

1. Crie um diagrama detalhado do fluxo central.
2. Crie diagramas de alto nivel separados para cada ponto de entrada relevante.
3. Se um fluxo nao puder ser rastreado ate a origem, documente-o como `Fluxo Interno/Background`.

Nenhum fluxo relevante deve ser omitido apenas porque a origem e menos obvia.
