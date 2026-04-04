# `examples/` - Estruturação de Prompts

Esta pasta reúne exemplos executáveis derivados diretamente de `..\estrutura-basica-dos-prompts.md`.

O objetivo do portfólio é seguir um padrão mais próximo do capítulo 1: comparar prompts reais, executar as variantes contra um LLM e tornar observável por que a estrutura do prompt muda o resultado.

## Como executar

```powershell
python .\3-estrutura-basica-dos-prompts\examples\1-bugfix-scope.py
python .\3-estrutura-basica-dos-prompts\examples\2-system-user-separation.py
python .\3-estrutura-basica-dos-prompts\examples\3-prompt-structure-template.py
python .\3-estrutura-basica-dos-prompts\examples\4-zero-shot-vs-few-shot.py
python .\3-estrutura-basica-dos-prompts\examples\5-cost-latency-quality.py
```

Os scripts dependem de `OPENAI_API_KEY` no ambiente e usam a stack Python já presente na raiz do repositório.

## Conteúdo da pasta

| Arquivo | Papel |
| --- | --- |
| `1-bugfix-scope.py` | comparação entre pedido ambíguo e prompt com escopo delimitado |
| `2-system-user-separation.py` | separação entre regras globais e tarefa local |
| `3-prompt-structure-template.py` | template completo de prompt técnico |
| `4-zero-shot-vs-few-shot.py` | comparação entre zero-shot e few-shot |
| `5-cost-latency-quality.py` | trade-off entre custo, latência e qualidade |
| `utils.py` | utilitário local para exibir prompt, resposta e métricas |
