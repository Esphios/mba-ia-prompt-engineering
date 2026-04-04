# AGENTS.md

## Escopo

Esta pasta contém versões genéricas e reutilizáveis das técnicas do capítulo 1. Aqui ficam os scripts parametrizados, o runner central e o advisor de sugestão de técnica.

## Instruções para agentes

- Preserve a orientação a reuso dos scripts desta pasta.
- Antes de editar o `README.md` local, verifique se a mudança é específica de `generic/` ou se pertence ao capítulo como um todo.
- Não descreva os scripts desta pasta como se fossem apenas cópias dos arquivos em `examples/`.
- Mantenha coerência entre:
  - `README.md`
  - `prompt_runner.py`
  - `suggest_prompt_technique.py`
  - `prompt_advisor.py`
- Se uma mudança estrutural afetar a relação entre `generic/` e `examples/`, reflita isso também na documentação da raiz do capítulo.

## Observações importantes

- `prompt_runner.py` lista, sugere e executa técnicas.
- `suggest_prompt_technique.py` expõe apenas a parte de sugestão.
- `prompt_advisor.py` concentra o catálogo de técnicas, preparação do problema e geração das recomendações.
- `common.py` é o utilitário compartilhado desta trilha, distinto de `..\utils.py`.
