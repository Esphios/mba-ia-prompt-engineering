# `examples/` - Trilha Didática

Esta pasta contém a trilha mais próxima da aula original do capítulo 1. Os scripts aqui são demonstrações diretas das técnicas, com menos parametrização e mais foco em clareza conceitual.

## Quando usar esta pasta

Use `examples/` quando o objetivo for:

- acompanhar a sequência pedagógica da aula;
- comparar técnicas de forma direta;
- inspecionar exemplos curtos antes de partir para uma versão mais reutilizável.

Se a intenção for reaproveitar as técnicas com tarefas arbitrárias, a pasta mais adequada é `..\generic\`.

## Conteúdo da pasta

| Técnica | Script |
| --- | --- |
| Role Prompting | `0-Role-prompting.py` |
| Zero-shot | `1-zero-shot.py` |
| One-shot / Few-shot | `2-one-few-shot.py` |
| Chain of Thought | `3-CoT.py` |
| Self-Consistency | `3.1-CoT-Self-consistency.py` |
| Tree of Thought | `4-ToT.py` |
| Skeleton of Thought | `5-SoT.py` |
| ReAct | `6-ReAct.py` |
| Prompt Chaining | `7-Prompt-channing.py` |
| Least-to-Most | `8-Least-to-most.py` |

## Como executar

```powershell
python .\examples\0-Role-prompting.py
python .\examples\3-CoT.py
python .\examples\7-Prompt-channing.py
```

## Observações

- Esta trilha usa `..\utils.py` para formatação de saída.
- `7-Prompt-channing.py` grava `prompt_chaining_result.md`.
- Os nomes dos scripts preservam a convenção histórica da aula, inclusive capitalização e hífens.
