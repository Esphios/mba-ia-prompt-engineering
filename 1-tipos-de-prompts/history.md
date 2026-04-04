# Histórico do Capítulo 1

Este arquivo preserva contexto editorial e informações removidas da documentação principal do capítulo.

## Normalização documental

Durante a reorganização do capítulo:

- `README.md` passou a concentrar visão geral, estrutura e how-to;
- `AGENTS.md` passou a conter apenas orientações curtas para agentes;
- `tipos-de-prompts.md` permaneceu como a aula principal;
- `history.md` passou a registrar contexto antigo e decisões de reorganização.

## Estruturas anteriores preservadas

Pelo histórico do git, o capítulo começou com layout plano na raiz, sem a separação atual entre `examples/` e `generic/`. Os scripts como `0-Role-prompting.py`, `1-zero-shot.py` e `7-Prompt-channing.py` ficavam diretamente em `1-tipos-de-prompts/`.

Em `2026-03-22`, o commit `27c8caf` reorganizou esse layout:

- os scripts originais foram movidos para `examples/`;
- foi criada a trilha `generic/`;
- o `AGENTS.md` que existia na raiz passou para `examples/AGENTS.md`.

## Relação entre `examples/` e `generic/`

Um dos problemas anteriores era tratar as duas trilhas como se fossem redundantes. A documentação atual passa a preservar explicitamente que:

- `examples/` é a trilha didática mais próxima da aula;
- `generic/` é a trilha voltada a reuso, CLI e operação mais flexível.

## Arquivos e convenções que existiram antes

O histórico do git também preserva que:

- em `2025-09-29`, o capítulo recebeu `requirements.txt`, `.env.example` e o script `8-Least-to-most.py`;
- em `2026-03-21`, o commit `b279f5d` removeu `requirements.txt` e `.env.example` do capítulo;
- no mesmo período, `utils.py` e vários scripts foram ajustados junto da mudança de configuração de ambiente.

Outro ponto que pode ser útil depois:

- em `2026-03-22`, antes da separação definitiva entre `examples/` e `generic/`, existiram três variantes adicionais de ToT na raiz:
  - `4.1-ToT-algorithm.py`
  - `4.2-ToT-best-so-far.py`
  - `4.3-ToT-generic.py`
- esses arquivos foram removidos no mesmo commit que consolidou a trilha genérica.

## Observações preservadas

- `examples/7-Prompt-channing.py` continua gerando `prompt_chaining_result.md`.
- `utils.py` continua sendo o utilitário compartilhado da trilha `examples/`.
- `generic/prompt_runner.py` continua sendo o ponto central da trilha genérica.

## Contexto removido do README e do AGENTS

Foram retirados da documentação operacional textos longos de reorganização, listas internas de criação de arquivos e referências a nomes que não existiam na árvore atual, como `lessons.md` e `lessons.history.md`.

Os logs do Codex também mostram uma fase intermediária, anterior à normalização final, em que a raiz do capítulo chegou a usar os nomes:

- `lessons.md`
- `lessons.history.md`

Esses nomes não foram mantidos porque competiam com a convenção canônica baseada em `tipos-de-prompts.md` e com o papel atual de `history.md`.

## Ajustes de documentação em 2026-04-03

Durante a revisão do capítulo 1 feita em `2026-04-03`, a documentação foi reorganizada para reduzir sobreposição entre os níveis da pasta.

### O que saiu dos arquivos principais

- `tipos-de-prompts.md` deixou de concentrar descrição de estrutura de diretório, utilitários locais e relação operacional entre `examples/` e `generic/`;
- `generic/README.md` deixou de repetir a aula inteira, incluindo blocos extensos com definição, usos, limitações e pseudo-código de cada técnica.

Esse conteúdo não foi apagado do projeto. Ele foi redistribuído assim:

- a navegação do capítulo ficou concentrada no `README.md` da raiz;
- a visão operacional de `generic/` ficou no `generic/README.md`;
- a aula principal ficou mais focada em conceito, critérios de escolha e comparação entre técnicas;
- este `history.md` registra a decisão editorial e preserva a memória de que o `generic/README.md` já funcionou como uma segunda aula paralela.

### Inconsistências corrigidas

- `examples/AGENTS.md` apontava para `..\lessons.history.md`, embora a convenção atual do capítulo use `..\history.md`;
- a documentação do capítulo misturava visão estrutural, how-to e teoria profunda em mais de um arquivo principal;
- a relação entre `examples/` e `generic/` aparecia repetida em excesso, mas nem sempre no arquivo mais apropriado.
