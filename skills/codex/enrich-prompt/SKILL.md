---
name: enrich-prompt
description: Enrich a user prompt after sanitization by selecting the most appropriate prompt-engineering principles from Chapter 1 generic techniques, then rewriting the prompt into a stronger version. Use when Codex must improve a prompt with explicit technique selection, role prompting, and Tree of Thought evaluation before deciding which principles to apply.
---

# Enrich Prompt

Always start by using `$sanitize-prompt` logic before any enrichment decision. Do not enrich raw input directly.

## Workflow

1. Run the sanitization step first.
2. Read [references/chapter1-generic-principles.md](references/chapter1-generic-principles.md) before selecting principles. Treat it as the decision basis extracted from `1-tipos-de-prompts/generic/README.md`.
3. Build a technique candidate set using all Chapter 1 principles:
   - role prompting
   - zero-shot
   - one-shot or few-shot
   - chain of thought
   - self-consistency
   - tree of thought
   - skeleton of thought
   - ReAct
   - prompt chaining
   - least-to-most
4. Use role prompting in every final rewrite. Choose one role that materially improves output quality.
5. Use Tree of Thought with 3 depths before deciding which principles to apply:
   - depth 1: generate materially different principle sets
   - depth 2: refine the strongest sets by fixing gaps, excess cost, and weak structure
   - depth 3: finalize and compare the best refined sets
6. Score each branch with this system:
   - intent fidelity: 0.25
   - output clarity and structure: 0.20
   - fit to task complexity: 0.15
   - cost and latency proportionality: 0.10
   - auditability: 0.10
   - ambiguity resilience: 0.10
   - execution readiness: 0.10
7. Pick the winning principle set and rewrite the sanitized prompt accordingly.
8. Prefer the smallest effective set of principles. Do not stack techniques just because they exist.

## Principle Selection Rules

Apply all principles as decision candidates, but only keep the ones justified by the task.

### Role Prompting

Always use it in the final rewrite. Keep the role concrete and task-relevant.

### Zero-shot

Prefer when the task is simple, direct, or high-scale and does not need examples or decomposition.

### One-shot / Few-shot

Use when output format or pattern-learning matters more than free-form reasoning.

### Chain of Thought

Use when the task requires decomposed reasoning, planning, or intermediate logic worth auditing.

### Self-Consistency

Use only when the task has objective answers and variance reduction is worth the extra cost.

### Tree of Thought

Use as the decision mechanism for selecting principles and candidate rewrites. It is mandatory for this skill for deciding which principles to apply.

### Skeleton of Thought

Use when the prompt should drive a long, structured answer such as a plan, article, checklist, or ADR.

### ReAct

Use when the target task depends on iterative investigation, observation, or evidence-driven action.

### Prompt Chaining

Use when the target task naturally breaks into sequential stages whose outputs feed later stages.

### Least-to-Most

Use when the user request is too large or ambiguous to solve well in one shot and should be decomposed from simple to complex.

## Decision Heuristics

- Be intentional about context, desired output, and auditability before choosing principles.
- Do not request detailed reasoning when the task does not need it.
- Prefer simpler prompts for simple or high-scale tasks.
- Treat model choice, token cost, and latency as real constraints.
- Do not assume more examples improve quality.
- If one stage feeds another, make structure and parsing explicit.
- Remember that prompt refinement is still necessary because the model can hallucinate or misread the task.

## Output Contract

Return:

1. `Intent inferred`
2. `Chosen role`
3. `Sanitized prompt`
4. `Rewritten prompt`
   - final enriched prompt in markdown and ready for use
5. `Principles used`
   - list each selected principle
6. `Why these principles`
   - explain why each selected principle survived scoring
7. `Why this version`
   - 2 to 4 short bullets tied to the winning branch

Optionally add `Missing information` when the quality of the enriched prompt still depends on unresolved gaps.

## Guardrails

- Never skip sanitization.
- Never claim that all principles should be used.
- Do not force chain-of-thought, ReAct, or self-consistency into trivial tasks.
- If the sanitized prompt is already strong, apply a light-touch enrichment.
- Preserve the user's domain vocabulary unless it is the source of ambiguity.
- Make output format explicit whenever format matters.

## Reference

Read [references/chapter1-generic-principles.md](references/chapter1-generic-principles.md) for the full decision basis extracted from `1-tipos-de-prompts/generic/README.md`.
