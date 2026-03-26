# Diagramas de Sequencia

Este documento funciona como indice para diagramas de sequencia que descrevem os fluxos mais importantes do sistema.

Para regras de criacao, manutencao e estilo, consulte [DIRETRIZES.md](./DIRETRIZES.md).

## Organizacao

A documentacao pode ser organizada por dominio de negocio.
Arquivos com prefixo `fluxo-` podem reunir:

- um diagrama de alto nivel do caso de uso
- um ou mais diagramas detalhados de partes centrais do fluxo

## Exemplos de Fluxos

### Fluxos Principais

- [Fluxo de Autenticacao](./fluxo-autenticacao.md): login, validacao de token e renovacao de sessao.
- [Fluxo de Criacao de Entidade](./fluxo-criacao-entidade.md): persistencia de uma nova entidade principal.
- [Fluxo de Checkout](./fluxo-checkout.md): validacao de carrinho, pagamento e confirmacao.

### Integracoes e Background

- [Sincronizacao de Dados](./sincronizacao-dados.md): jobs ou workers que consomem APIs externas.
- [Geracao de Relatorios](./geracao-relatorios.md): enfileiramento, processamento e notificacao.
- [Job de Limpeza](./job-limpeza-dados.md): expiracao e limpeza de dados.

### Consultas e Operacoes Especificas

- [Busca Paginada](./busca-paginada.md): listagem com filtros e paginacao.
- [Redefinicao de Senha](./redefinicao-senha.md): emissao de token e troca segura de credenciais.
