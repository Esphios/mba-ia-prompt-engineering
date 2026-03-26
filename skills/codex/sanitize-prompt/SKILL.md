---
name: sanitize-prompt
description: Sanitize a raw user prompt before any enrichment by removing noise, extracting intent, clarifying output expectations, and separating explicit constraints, implied constraints, and missing information. Use when Codex receives a rough, ambiguous, verbose, duplicated, or underspecified prompt and needs a clean prompt intake artifact.
---

# Sanitize Prompt

Use this skill as the intake step before rewriting or enriching a prompt.

## Workflow

1. Read the raw prompt and any adjacent user context.
2. Preserve the user's language unless the user explicitly asks for a rewrite in another language.
Preserve placeholders, variable names, file paths, URLs, and domain terms unless they are clearly noise.
3. Remove:
   - filler text
   - repeated instructions
   - contradictory wording when one interpretation is clearly dominant
   - irrelevant style noise
If a conflict is still unresolved after cleanup, move it to `Missing information` instead of guessing.
4. Extract and label:
   - primary intent
   - target audience, if inferable
   - desired output
   - explicit constraints
   - implied constraints
   - missing information
   - safe reversible assumptions
5. Rewrite the prompt into a concise, self-contained sanitized version.
6. Do not enrich yet. Do not add advanced techniques here. This skill only prepares the prompt for later decision-making.

## Output Contract

Return:

1. `Primary intent`
2. `Target audience`
3. `Desired output`
4. `Explicit constraints`
5. `Implied constraints`
6. `Missing information`
7. `Safe assumptions`
8. `Sanitized prompt`

Keep each section brief and operational.

## Guardrails

- Do not invent domain facts.
- Do not remove placeholders or domain vocabulary that still carry meaning.
- Do not add role prompting, examples, reasoning scaffolding, or multi-step workflows.
- Do not silently discard meaningful constraints.
- If the original prompt is already clean, return a light-touch sanitized version with minimal changes.
