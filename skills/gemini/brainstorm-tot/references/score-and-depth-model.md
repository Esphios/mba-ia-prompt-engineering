# Score And Depth Model

Use this reference when applying the full decision mechanism for `$brainstorm-tot`.
Keep the main `SKILL.md` focused on triggering and workflow. Use this file for the detailed mechanics of scoring, pruning, and depth progression.

## Purpose

The goal is not to reward the most complicated branch.
The goal is to select the most defensible path under the current problem framing, while keeping strong alternatives and preserving earlier-depth winners when they remain better.

## Default Search Settings

- Branch factor: start with at least 3 materially different branches
- Beam width: usually keep the strongest 2 or more branches after each comparison round
- Default depth: 3
- Custom depth: allowed when requested by the user or when the problem clearly benefits from one more bounded refinement round

Use wider branching only when the problem truly has several distinct strategic options.
Do not manufacture diversity by renaming the same path.

## What Counts As A Different Branch

A branch is materially different when at least one of these changes:

- strategy
- sequencing
- source of leverage
- risk profile
- dependency footprint
- reversibility
- resource model
- assumption set

These do not count as materially different:

- cosmetic wording changes
- same plan with trivial ordering changes
- same architecture with minor parameter tweaks
- same idea with renamed labels

## Skeleton Contract Per Branch

Before deeper comparison, each branch should have a compact skeleton, usually 4 to 6 bullets, covering:

1. Core idea
2. Why it could work
3. Key steps
4. Dependencies or prerequisites
5. Main risks
6. Expected upside
7. Kill criteria or failure signals

The skeleton is the minimum auditable unit.
If the skeleton is weak, score the branch lower instead of compensating with speculative detail.

## Default Weighted Rubric

Use this rubric unless the user provides custom dimensions or weights.

| Dimension | Weight | What it measures |
| --- | ---: | --- |
| Problem fit | 0.25 | How directly the branch addresses the real problem |
| Feasibility | 0.20 | How realistic the branch is given constraints and execution complexity |
| Expected value | 0.15 | Upside if the branch works |
| Risk containment | 0.15 | How well the branch controls downside and failure modes |
| Reversibility | 0.10 | How cheaply the branch can be undone or tested incrementally |
| Evidence or assumption quality | 0.10 | How grounded the branch is in known facts versus fragile assumptions |
| Execution clarity | 0.05 | How understandable and actionable the next steps are |

Weights should sum to 1.00.
If the user gives custom weights that do not sum to 1.00, normalize them before comparison.

## Scoring Scale

Score each dimension on a 1 to 10 scale.

- 9 to 10: exceptionally strong
- 7 to 8: strong and credible
- 5 to 6: viable but with visible weaknesses
- 3 to 4: weak or risky
- 1 to 2: poor fit or largely indefensible

The weighted branch score is:

```text
weighted_score = sum(weight_i * score_i)
```

## Score Interpretation

- 8.5 to 10.0: clear leading option
- 7.5 to 8.4: strong option worth recommending
- 6.5 to 7.4: viable option with meaningful caveats
- 5.0 to 6.4: weak but still discussable
- below 5.0: usually prune unless diversity is still strategically useful

Never treat the score as the only decision input.
Use it together with branch diversity, uncertainty, and fallback quality.

## Depth Model

### Depth 1: Generate And Filter

Purpose:
- maximize strategic diversity
- surface the real option space
- remove duplicates and clearly weak branches

Actions:
- generate at least 3 candidate branches
- build a skeleton for each branch
- score lightly but explicitly
- prune duplicates and obvious non-contenders

Expected outcome:
- a set of distinct, auditable candidates

### Depth 2: Refine And Stress-Test

Purpose:
- improve the strongest branches
- make trade-offs explicit
- fix avoidable weaknesses before final choice

Actions:
- refine the top branches
- clarify sequencing
- expose dependencies and hidden assumptions
- adjust scope when a branch is overbuilt or under-specified

Expected outcome:
- fewer, stronger, better-defined branches

### Depth 3: Compare And Decide

Purpose:
- select the winner
- preserve the best alternatives
- produce a recommendation that can be defended

Actions:
- rescore the finalists with the full rubric
- compare winner versus alternatives explicitly
- decide whether an earlier-depth version still beats deeper descendants
- produce winner, alternatives, assumptions, and fallback

Expected outcome:
- one primary recommendation plus non-winning but valid alternatives

## Custom Depth Policy

If the user asks for a custom depth, extend the search in bounded rounds:

- Odd depths: compare, prune, and select
- Even depths: refine, split, or stress-test the best surviving branches

Additional depth is justified only when it adds meaningful differentiation.
Stop early if the search plateaus.

## Pruning Rules

Prune a branch when one or more of these conditions hold:

- it is materially redundant with a stronger branch
- it depends on unfixable assumptions
- it scores far below the viable range
- it adds no meaningful diversity
- it creates cost or complexity without compensating upside

Keep a lower-scoring branch only if it provides strategic diversity the stronger branches do not provide.

## Fallback Policy

Earlier-depth versions remain valid final outputs when they still outperform or clearly simplify deeper descendants.

Use an earlier-depth fallback when:

- the deeper descendant introduces unnecessary complexity
- the deeper descendant lowers reversibility too much
- refinement reduces clarity without increasing value
- the earlier version preserves a better risk-reward balance

Do not assume the newest branch is the best branch.

## Tie-Breaking Rules

If branches score similarly, prefer the branch that:

1. is easier to test cheaply
2. is more reversible
3. relies on fewer fragile assumptions
4. achieves useful progress sooner
5. preserves optionality for later decisions

## When To Stop

Stop when:

- one branch clearly dominates
- additional depth produces only cosmetic changes
- uncertainty is already captured in assumptions and alternatives
- the decision can already be defended to the user

Do not deepen the tree simply because a maximum depth exists.

## Recommended Output Fragments

When summarizing score reasoning, keep it concise and auditable:

- `Winner because`: 2 to 4 short bullets
- `Best alternatives`: 1 short paragraph or bullets per alternative
- `Assumptions`: only decision-relevant assumptions
- `Fallback`: mention the earlier-depth branch only when it remains genuinely competitive

## Custom Rubric Override

If the user supplies a custom rubric:

1. Use the user rubric instead of the default one
2. Normalize weights if necessary
3. State the custom dimensions in `Exploration settings`
4. Do not mix the default rubric into the final winner explanation unless explicitly asked

## Failure Modes To Watch

- too many branches that are not actually different
- hidden assumptions dominating the decision
- late-depth refinements that only add complexity
- scoring without explicit criteria
- false precision from numeric scores unsupported by reasoning
- losing a strong earlier branch just because the search went deeper
