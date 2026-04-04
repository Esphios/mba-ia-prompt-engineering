# Tipos de Prompt - Versões Genéricas

Esta pasta reúne versões genéricas das técnicas apresentadas no capítulo 1. Os scripts foram pensados para reaproveitamento com tarefas diferentes, com menos acoplamento aos exemplos originais e com uma implementação mais fiel quando a técnica exige múltiplas etapas.

## Papel desta pasta

Use `generic/` quando o objetivo for:

- testar técnicas com tarefas arbitrárias;
- rodar scripts parametrizados via CLI;
- pedir sugestão de técnica antes da execução;
- transformar o capítulo em kit prático, e não apenas em demonstração.

Se a intenção for acompanhar a sequência da aula com scripts mais diretos, prefira `..\examples\`.

## Visão geral

| Tipo | Script |
| --- | --- |
| Role Prompting | `0-role-prompting.py` |
| Zero-shot | `1-zero-shot.py` |
| One-shot / Few-shot | `2-one-few-shot.py` |
| Chain of Thought | `3-cot.py` |
| Self-Consistency | `3.1-self-consistency.py` |
| Tree of Thought | `4-tot.py` |
| Skeleton of Thought | `5-sot.py` |
| ReAct | `6-react.py` |
| Prompt Chaining | `7-prompt-chaining.py` |
| Least-to-Most | `8-least-to-most.py` |
| Runner | `prompt_runner.py` |
| Sugeridor | `suggest_prompt_technique.py` |
| Utilitários compartilhados | `common.py`, `prompt_advisor.py` |

## Fluxos de uso

### Executar um script diretamente

```powershell
python .\generic\1-zero-shot.py --task "Explique recursão em termos simples."
```

### Executar via runner

```powershell
python .\generic\prompt_runner.py run `
  --technique zero-shot `
  --task "Explique recursão em termos simples."
```

### Pedir sugestões antes de rodar

```powershell
python .\generic\suggest_prompt_technique.py `
  --task "Preciso comparar três arquiteturas para um serviço com alto volume e escolher a melhor."
```

### Pedir sugestões pelo runner

```powershell
python .\generic\prompt_runner.py suggest `
  --task "Preciso depurar uma API e analisar evidências passo a passo."
```

### Listar as técnicas disponíveis

```powershell
python .\generic\prompt_runner.py list
```

## Componentes principais

### `prompt_runner.py`

Interface única para:

- listar técnicas;
- sugerir técnicas;
- executar scripts da pasta.

### `suggest_prompt_technique.py`

Interface focada apenas em sugestão. Ela usa o advisor para analisar o problema, higienizar a entrada, enriquecer a descrição e recomendar as melhores técnicas.

### `prompt_advisor.py`

Catálogo central das técnicas, das heurísticas de preparação do problema e da geração de recomendações.

### `common.py`

Utilitário compartilhado desta trilha, separado de `..\utils.py`.

## Argumentos mais usados por script

| Script | Argumentos principais |
| --- | --- |
| `0-role-prompting.py` | `--task`, `--task-file`, `--role`, `--role-file`, `--model`, `--temperature` |
| `1-zero-shot.py` | `--task`, `--task-file`, `--model`, `--temperature` |
| `2-one-few-shot.py` | `--task`, `--task-file`, `--instruction`, `--example`, `--example-file`, `--model`, `--temperature` |
| `3-cot.py` | `--task`, `--task-file`, `--answer-label`, `--model`, `--temperature` |
| `3.1-self-consistency.py` | `--task`, `--task-file`, `--samples`, `--answer-label`, `--model`, `--temperature` |
| `4-tot.py` | `--problem`, `--problem-file`, `--criterion`, `--max-depth`, `--branch-factor`, `--beam-width`, `--finalists`, `--model`, `--temperature` |
| `5-sot.py` | `--task`, `--task-file`, `--bullet-range`, `--model`, `--temperature` |
| `6-react.py` | `--task`, `--task-file`, `--context`, `--context-file`, `--model`, `--temperature` |
| `7-prompt-chaining.py` | `--task`, `--task-file`, `--step`, `--step-model`, `--output-file`, `--temperature` |
| `8-least-to-most.py` | `--task`, `--task-file`, `--model`, `--temperature` |

## Diferenças em relação à trilha didática

- Aqui a prioridade é reuso, não fidelidade à narrativa da aula.
- Alguns scripts implementam de forma mais explícita a natureza multi-etapas da técnica.
- `prompt_runner.py` e `suggest_prompt_technique.py` não têm equivalentes na trilha `examples/`.

Para a explicação conceitual detalhada de cada técnica, consulte `..\tipos-de-prompts.md`.
