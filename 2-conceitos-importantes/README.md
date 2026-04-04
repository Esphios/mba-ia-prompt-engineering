# Capítulo 2: Conceitos Importantes

Este capítulo reúne a base conceitual que sustenta decisões de Prompt Engineering além da redação do prompt. Ele é importante porque conecta o trabalho com LLMs a custo, latência, janela de contexto, cache e processamento em lote.

## Estrutura da pasta

| Caminho | Papel |
| --- | --- |
| `conceitos-importantes.md` | aula principal do capítulo |
| `history.md` | detalhes temporais, exemplos removidos e contexto editorial |
| `examples/` | scripts que ilustram os conceitos |
| `AGENTS.md` | orientações curtas para agentes |

## O que estudar aqui

O capítulo aprofunda temas como:

- janela de contexto;
- diferença entre contexto e parâmetros;
- relação entre tokens, custo e latência;
- truncamento, sumarização e sliding window;
- prompt caching;
- batch prompting;
- trade-offs de escolha de modelo.

Para a explicação completa, leia `conceitos-importantes.md`.

## Como usar os exemplos

Os exemplos existem para tornar visíveis decisões de arquitetura e operação. Eles não substituem a aula principal.

```powershell
python .\examples\1-context-window-budget.py
python .\examples\2-context-management-strategies.py
python .\examples\3-cache-and-batch-patterns.py
python .\examples\4-model-choice-tradeoffs.py
```

## Importância do capítulo

Este é o capítulo que impede Prompt Engineering de virar apenas redação de instruções. Ele introduz as restrições reais que passam a orientar capítulos mais práticos do curso.
