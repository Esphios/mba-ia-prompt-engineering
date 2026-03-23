---
name: sanitize-prompt
description: Sanitize a raw user prompt before any enrichment by removing noise, extracting intent, clarifying output expectations, and separating explicit constraints, implied constraints, and missing information. Use when Gemini receives a rough, ambiguous, verbose, duplicated, or underspecified prompt and needs a clean prompt intake artifact.
---

# Sanitize Prompt

Use this skill as the intake step before rewriting or enriching a prompt.

## Imported Metadata

Preserve the following source metadata as reference only. Gemini does not consume it as native config.

- `Display name`: `Sanitize Prompt`
- `Short description`: `Higieniza a entrada do prompt`
- `Suggested prompt`: `Use $sanitize-prompt para limpar e estruturar este prompt antes de qualquer enriquecimento.`

## Workflow

1. Read the raw prompt and any adjacent user context.
2. Preserve the user's language unless the user explicitly asks for a rewrite in another language.
3. Remove:
   - filler text
   - repeated instructions
   - contradictory wording when one interpretation is clearly dominant
   - irrelevant style noise
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
2. `Desired output`
3. `Explicit constraints`
4. `Implied constraints`
5. `Missing information`
6. `Safe assumptions`
7. `Sanitized prompt`

Keep each section brief and operational.

## Guardrails

- Do not invent domain facts.
- Do not add role prompting, examples, reasoning scaffolding, or multi-step workflows.
- Do not silently discard meaningful constraints.
- If the original prompt is already clean, return a light-touch sanitized version with minimal changes.

