# Histórico do Capítulo 3

Este arquivo preserva contexto editorial e decisões tomadas na organização do capítulo.

## Estado inicial observado

Quando a documentação deste capítulo foi organizada, a pasta tinha a aula principal, mas ainda não tinha documentação de apoio consolidada.

Os logs do Codex preservam uma fase intermediária em que o capítulo chegou a usar:

- `lesson.md` como versão reorganizada da aula;
- exemplos markdown-first com nomes como:
  - `1-bugfix-antes-e-depois.md`
  - `2-template-prompt-tecnico.md`
  - `3-system-vs-user-prompt.md`
  - `4-zero-shot-vs-few-shot.md`
  - `5-custo-latencia-qualidade.md`

Essa estrutura foi depois substituída pela convenção atual, em que:

- `estrutura-basica-dos-prompts.md` permanece como aula canônica;
- os exemplos passaram a usar arquivos `.py` com nomes em inglês e foco mais executável.

Houve ainda uma fase posterior em que os exemplos `.py` existiam, mas eram fracos do ponto de vista didático porque apenas imprimiam prompts estáticos. Esse portfólio foi então refeito para ficar mais alinhado ao padrão do capítulo 1:

- comparação entre variantes reais de prompt;
- execução efetiva contra LLM;
- observação de saída, escopo, formato e trade-offs;
- utilitário local para exibir prompt, resposta e métricas.

## Decisões preservadas

- `estrutura-basica-dos-prompts.md` permaneceu como arquivo canônico da aula.
- `README.md` passou a responder pela visão geral, estrutura e uso do capítulo.
- `AGENTS.md` passou a conter apenas orientações curtas para agentes.
- `history.md` passou a registrar a memória de reorganização.

## Portfólio de exemplos

O capítulo permaneceu com foco conceitual. Por isso, a documentação passou a tratar `examples/` como apoio didático, e não como uma stack executável mais ampla do que a pasta realmente oferece.

## Arquivos e nomes antigos que podem importar depois

Pelo histórico do git:

- em `2026-03-25`, o arquivo de visão geral foi criado com o nome incorreto `README.md.md`;
- em `2026-03-28`, o commit `fd8aee3` corrigiu esse nome para `README.md`.

Esse detalhe é pequeno, mas vale ser preservado porque explica referências antigas ou buscas por um arquivo com dupla extensão.

## Guardrail preservado

Foi evitada a criação de um nome genérico concorrente, como `lesson.md`, já que a convenção do capítulo já estava bem representada em `estrutura-basica-dos-prompts.md`.

Mesmo assim, os logs mostram que `lesson.md` existiu temporariamente durante a reorganização do capítulo. Esse nome não foi mantido justamente para evitar competir com o arquivo canônico.
