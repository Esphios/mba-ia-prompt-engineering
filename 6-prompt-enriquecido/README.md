# Capítulo 6: Prompt Enriquecido

Este capítulo trata de enriquecimento de query e expansão iterativa de resposta. Ele é importante porque mostra como melhorar a entrada antes da execução e como refinar a saída quando a primeira resposta ainda está incompleta.

## Estrutura da pasta

| Caminho | Papel |
| --- | --- |
| `prompt-enriquecido.md` | aula principal do capítulo |
| `history.md` | memória editorial, divergências corrigidas e contexto removido |
| `0-No-expansion.py` | baseline sem enriquecimento |
| `1-ITER_RETGEN.py` | expansão iterativa de resposta |
| `2-query-enrichment.py` | enriquecimento interativo da pergunta |
| `AGENTS.md` | orientações curtas para agentes |

## O que estudar aqui

O capítulo aprofunda:

- query enrichment;
- Query2Doc;
- HyDE;
- ITER-RETGEN;
- relação entre custo, latência e múltiplas chamadas;
- diferença entre teoria de retrieval e simplificação didática em script.

Para a explicação completa, leia `prompt-enriquecido.md`.

## Como executar

```powershell
python .\0-No-expansion.py
python .\1-ITER_RETGEN.py
python .\2-query-enrichment.py
```

Os scripts dependem de `OPENAI_API_KEY` disponível no ambiente.

## Observação estrutural

Na árvore atual deste capítulo, os exemplos executáveis ficam na raiz. Não existe uma pasta `examples/`.

## Importância do capítulo

Este capítulo mostra que parte do ganho de qualidade em sistemas com LLM não vem apenas de responder melhor, mas de perguntar melhor e de refinar respostas de forma explícita.
