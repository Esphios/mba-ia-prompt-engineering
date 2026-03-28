---
name: brainstorm-tot
description: Brainstorm at least 3 materially different solution paths for a problem, build concise skeletons for each path, and run a bounded Tree of Thought comparison to select the best option, strongest alternatives, assumptions, and fallback branches. Use when Gemini should explore multiple approaches before committing to a plan, design, fix, prompt, or workflow. Always sanitize the initial problem first, and enrich it with the prompt skills when that improves the quality of the exploration.
---

# Brainstorm ToT

Use this skill when the user wants option exploration before commitment.
This skill is for decision-quality branching, not for generating one linear answer immediately.

## Imported Metadata

Preserve the following source metadata as reference only. Gemini does not consume it as native config.

- `Display name`: `Brainstorm ToT`
- `Short description`: `Explore options with scored Tree of Thought`
- `Suggested prompt`: `Use $brainstorm-tot to sanitize this problem, explore multiple solution paths, and select the best one with Tree of Thought.`

## Workflow

1. Sanitize the problem first.
Always apply `$sanitize-prompt` logic before any branching.
If the request is noisy, contradictory, vague, or overloaded, produce a clean intake artifact first.

2. Enrich only when it improves exploration quality.
Use `$enrich-prompt` when the problem is underspecified, high-stakes, structurally weak, or would clearly benefit from a better role, output contract, or prompting strategy.
Do not force enrichment if the sanitized problem is already clear.

3. Define the exploration settings.
Set:
- branch count: at least 3 materially different paths
- beam width: keep only the strongest 2 or more branches per round when pruning is needed
- depth: default 3, unless the user asks for another depth
- score dimensions: use the default rubric from [references/score-and-depth-model.md](references/score-and-depth-model.md) unless the user provides a custom one
- output mode: concise by default, deeper analysis only when requested

4. Generate candidate paths.
Create paths that differ in strategy, sequencing, trade-offs, or operating assumptions.
Do not create cosmetic variants of the same idea.

5. Build a skeleton for each path.
For every candidate path, produce a compact skeleton, usually 4 to 6 bullets, with:
- core idea
- why it might work
- key steps
- prerequisites or dependencies
- main risks
- expected upside
- kill criteria or failure signals

6. Run Tree of Thought selection.
Use bounded exploration, not open-ended branching.
Read [references/score-and-depth-model.md](references/score-and-depth-model.md) before final selection.
Use its depth model, pruning rules, score rubric, and fallback logic unless the user provides a custom alternative.

7. Keep previous-depth winners valid.
If a branch from an earlier depth still beats deeper descendants, keep it as a valid final answer.
Do not force the deepest branch to win only because it is newer.

8. Score explicitly.
Make the criteria explicit before choosing a winner.
Use the default weighted score from [references/score-and-depth-model.md](references/score-and-depth-model.md) unless the user provides a custom rubric.

9. Prefer diversity before precision.
Early branches should maximize strategic diversity.
Later depths should maximize clarity and decision quality.

10. Stop when the decision is good enough.
The goal is not exhaustive search.
The goal is a defensible choice with visible alternatives and assumptions.

## Output Contract

Return:

1. `Sanitized problem`
2. `Enriched framing`
   - say whether enrichment was applied
   - if not applied, say `Skipped`
3. `Exploration settings`
   - branch count
   - depth used
   - scoring rubric
4. `Candidate paths`
   - one compact section per path with its skeleton
5. `Tree summary by depth`
   - short summary of what survived each depth
6. `Best path`
   - winner, score, and why it won
7. `Best alternatives`
   - strongest non-winning options and when to prefer them
8. `Assumptions`
9. `Open questions`
10. `Depth fallback`
   - include any earlier-depth version that remains a valid final answer because of its score or simplicity advantage

## Guardrails

- Never skip sanitization.
- Do not generate fewer than 3 paths unless the user explicitly asks for fewer.
- Do not count minor wording changes as separate paths.
- Do not expose raw hidden chain-of-thought.
Summarize branch logic, trade-offs, and score reasoning instead.
- Do not over-enrich a problem that is already clear.
- Do not keep expanding depth when branch quality plateaus.
- If one path dominates early and deeper exploration adds no value, say so.
- If the user asks only for brainstorming, you may stop before final selection, but still present skeletons and the current best candidates.
- Treat this as a tree search with generation, evaluation, pruning, refinement, and final decision.

## Decision Heuristics

- Prefer broad strategic differences at depth 1.
- Prefer execution realism at depth 2.
- Prefer decision clarity at depth 3.
- Bias toward reversible paths when uncertainty is high.
- Bias toward high-upside paths when the user explicitly optimizes for leverage rather than certainty.
- Penalize branches that depend on missing facts, hidden approvals, or fragile assumptions.
- If two paths are close, prefer the one that is easier to test cheaply.

## Examples of Good Triggers

- "Brainstorm three ways to solve this architecture problem and pick the best one."
- "Give me multiple implementation paths, compare them, and recommend one."
- "Use Tree of Thought to explore options before writing code."
- "I want alternatives, assumptions, and a winner, not just one answer."
- "Create a plan, but first branch out and compare approaches."

## Reference

Read [references/score-and-depth-model.md](references/score-and-depth-model.md) whenever you need the full score rubric, depth semantics, pruning behavior, fallback policy, or score interpretation guidance.
