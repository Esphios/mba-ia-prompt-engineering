# Exemplos do Capítulo 2

Esta pasta reúne exemplos executáveis derivados de [conceitos-importantes.md](D:/Docs/Workspace/mba-ia-prompt-engineering/2-conceitos-importantes/conceitos-importantes.md).

Como os tópicos do capítulo podem ser demonstrados com scripts curtos em Python, o portfólio foi convertido de Markdown para Python com biblioteca padrão. Cada arquivo imprime um cenário didático e a leitura prática do conceito.

## Como executar

```powershell
python .\2-conceitos-importantes\examples\1-context-window-budget.py
python .\2-conceitos-importantes\examples\2-context-management-strategies.py
python .\2-conceitos-importantes\examples\3-cache-and-batch-patterns.py
python .\2-conceitos-importantes\examples\4-model-choice-tradeoffs.py
```

## Arquivos

| Arquivo | Demonstra |
| --- | --- |
| `1-context-window-budget.py` | soma de contexto e orçamento aproximado de tokens |
| `2-context-management-strategies.py` | truncamento, sumarização e sliding window |
| `3-cache-and-batch-patterns.py` | relação entre prompt caching e batch prompting |
| `4-model-choice-tradeoffs.py` | escolha de modelo com base em custo, latência e qualidade |
