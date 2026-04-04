# Histórico do Capítulo 5

Este arquivo preserva contexto editorial e informações removidas da documentação operacional do capítulo.

## Reorganização documental

Durante a refatoração da documentação:

- `README.md` passou a concentrar estrutura, setup, execução e importância do capítulo;
- `AGENTS.md` passou a conter apenas orientações curtas para agentes;
- `gerenciamento-e-versionamento-de-prompts.md` passou a ser a aula principal;
- `history.md` passou a concentrar memória editorial e decisões de organização.

## Estrutura inicial preservada

Pelo histórico do git, o capítulo foi introduzido em `2025-09-22` com uma estrutura mais autocontida, incluindo:

- `.env.example`
- `requirements.txt`
- `AGENTS.md`
- `README.md`
- `src/`
- `prompts/`
- `tests/`

Essa configuração refletia um capítulo com setup local próprio mais explícito.

## Contexto preservado

- O capítulo sempre tratou prompt como software, com versionamento, revisão e testes.
- A implementação local usa `prompts/registry.yaml` como índice central para prompts versionados.
- A integração com LangSmith permaneceu como caminho opcional de sincronização e publicação.

## Arquivos e convenções que existiram antes

Em `2026-03-21`, o commit `b279f5d` removeu do capítulo:

- `.env.example`
- `requirements.txt`

Esse detalhe vale ser mantido porque parte do material antigo ainda pressupõe setup por capítulo com esses arquivos presentes.

Os logs do Codex também preservam uma refatoração em `2026-04-03` em que `lessons.md` foi substituído por `gerenciamento-e-versionamento-de-prompts.md` durante a aplicação do skill `studify-transcript`. O conteúdo final foi mantido, mas esse evento ajuda a explicar eventuais diferenças bruscas entre versões do material.

## Contexto removido do AGENTS

O `AGENTS.md` anterior acumulava setup, comandos, detalhes de arquitetura interna e descrição extensa do framework de testes. Esse conteúdo foi redistribuído para o `README.md` e para a aula principal, reduzindo redundância.

O `AGENTS.md` original também trazia:

- comandos completos de setup;
- comandos de teste com `pytest`;
- detalhes de `PromptRegistry`, `PromptInfo` e da arquitetura de testes por fixtures;
- observações explícitas sobre o uso de LangChain `1.0.0a5`.

Esses pontos são potencialmente úteis mais tarde e, por isso, ficam preservados aqui como contexto do desenho original do capítulo.

## Observação de stack

O capítulo continua usando uma stack mais nova de LangChain e LangGraph do que os capítulos introdutórios do curso. Esse contraste é parte do contexto pedagógico e foi preservado.
