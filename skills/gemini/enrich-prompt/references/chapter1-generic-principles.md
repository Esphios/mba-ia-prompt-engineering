# Chapter 1 Generic Principles

This reference condenses the decision-relevant content from `1-tipos-de-prompts/generic/README.md` so the enrichment skill can choose principles with the same reasoning basis as the chapter material.

## Overview

The generic folder contains reusable versions of these techniques:

- role prompting
- zero-shot
- one-shot / few-shot
- chain of thought
- self-consistency
- tree of thought
- skeleton of thought
- ReAct
- prompt chaining
- least-to-most

The folder also includes `prompt_runner.py`, `suggest_prompt_technique.py`, `common.py`, and `prompt_advisor.py`. The decision pattern behind the folder is consistent: choose the lightest technique that fits the task, and use heavier orchestration only when the task structure justifies it.

## Global Principles

- Define context, desired output, and auditability before selecting any technique.
- Do not ask for detailed reasoning unless the task genuinely benefits from it.
- Simpler prompting is preferable for simple tasks and high-scale scenarios.
- Model choice affects behavior, token cost, latency, and the real benefit of each technique.
- More examples do not automatically improve results and may add ambiguity.
- When one stage feeds another, structure and parsing become requirements, not details.
- Prompt refinement remains necessary because the model can hallucinate or misread the task.

## Decision Notes By Technique

### Role Prompting

Use when:
- tone, audience, or technical depth matters
- a stable persona helps consistency
- context ambiguity should be reduced
- the task benefits from a clearly defined evaluator, teacher, reviewer, or planner role

Limitations:
- the role may weaken over long conversations
- later instructions can override the role
- the benefit may be small for very simple tasks
- stronger models may show less contrast than smaller ones

Decision guidance:
- keep the role short, explicit, and task-relevant
- do not use decorative personas
- for this skill, always keep one concrete role in the final rewritten prompt

### Zero-shot

Use when:
- the task is simple, direct, or common
- latency and cost matter
- you want a small prompt
- no examples are needed to define the target behavior

Limitations:
- weaker control over format and style
- more fragile on complex tasks
- wording changes can shift the result materially

Decision guidance:
- this is the default baseline for simple tasks
- a long prompt can still be zero-shot if it contains no examples
- prefer it in high-scale scenarios unless another technique is clearly justified

### One-shot / Few-shot

Use when:
- the model must imitate a response pattern
- the output format is easier to teach by demonstration
- the task depends on classification or templating consistency
- examples reduce variance better than abstract instructions

Limitations:
- quality depends heavily on example quality
- token cost grows quickly
- rigid or conflicting examples can bias the result badly

Decision guidance:
- use only enough examples to establish the pattern
- do not assume more examples help
- select it when demonstration matters more than free-form reasoning

### Chain of Thought

Use when:
- the task benefits from decomposition, intermediate logic, or explicit planning
- the reasoning path should be auditable
- the model tends to skip steps without guidance

Limitations:
- higher cost, latency, and verbosity
- plausible reasoning can still be wrong
- limited value for simple tasks

Decision guidance:
- choose it only when there is something meaningful to audit
- do not request it automatically for trivial prompts

### Self-Consistency

Use when:
- the task has an objective answer
- one reasoning path is unstable across runs
- multiple sampled paths are worth comparing

Limitations:
- multiplies cost and latency
- can still converge on the wrong answer
- does not repair a flawed base prompt

Decision guidance:
- reserve it for objective tasks where variance reduction is valuable
- avoid it for open-ended writing or cheap prompt enhancement

### Tree of Thought

Use when:
- multiple plausible principle sets or rewrites exist
- trade-offs matter and should be compared explicitly
- a single linear answer would likely be shallow

Limitations:
- more expensive and slower than simpler reasoning
- depends on clear evaluation criteria
- branches may collapse into similar options if poorly designed

Decision guidance:
- use explicit scoring criteria
- stop at a bounded search rather than endless branching
- in this skill, ToT is mandatory and runs for 3 depths

### Skeleton of Thought

Use when:
- the target answer should be long but well-structured
- the user wants plans, articles, ADRs, checklists, or documentation
- controlling structure before detail is beneficial

Limitations:
- a poor skeleton leads to a poor expansion
- ambiguous outlines can degrade the second stage
- adds extra steps and latency

Decision guidance:
- use it when structure is a first-order requirement
- avoid it if the target output is short or already tightly scoped

### ReAct

Use when:
- the task is investigative
- evidence gathering or debugging matters
- separating thought, action, and observation improves reliability

Limitations:
- high token cost and verbosity
- can simulate nonexistent actions or observations
- requires clear stopping conditions and evidence boundaries

Decision guidance:
- use only when the target task truly depends on iterative investigation
- avoid it for straightforward content generation

### Prompt Chaining

Use when:
- the task has real sequential phases
- one output naturally feeds the next
- different substeps may need different prompts or models
- intermediate outputs should be inspectable

Limitations:
- extra latency and orchestration complexity
- upstream errors propagate
- poor parsing breaks the chain

Decision guidance:
- choose it when the task is naturally pipeline-shaped
- make intermediate structures explicit

### Least-to-Most

Use when:
- the request is too large or ambiguous for a one-pass response
- complexity should be built progressively
- simpler clarifications should come before harder design decisions

Limitations:
- bad decomposition poisons later steps
- requires more coordination and calls
- excessive for small tasks

Decision guidance:
- prefer it when the task needs progressive decomposition from simple to complex
- review whether the decomposition is actually necessary before selecting it

## Notes About These Generic Versions

These generic implementations matter because they show how the chapter expects the technique to be used, not just named:

- self-consistency means real multiple samples plus voting
- tree of thought means tree search with generation, evaluation, expansion, pruning, and final decision
- skeleton of thought means explicit skeleton first, expansion second
- prompt chaining means real sequential execution, not just a long prompt with sections
- least-to-most means ordered subproblem solving, not just informal decomposition

For enrichment decisions, treat these stronger interpretations as the standard. Do not claim a principle is being used unless the rewritten prompt actually reflects its defining behavior.

## Scoring System For Enrichment

Use this weighted score when comparing ToT branches:

- intent fidelity: 0.25
- output clarity and structure: 0.20
- fit to task complexity: 0.15
- cost and latency proportionality: 0.10
- auditability: 0.10
- ambiguity resilience: 0.10
- execution readiness: 0.10

## ToT Depth Model

### Depth 1

Generate materially different candidate principle sets. Each set should include only the principles that plausibly fit the task.

### Depth 2

Refine the strongest sets by removing over-engineering, improving structure, and correcting poor cost-quality trade-offs.

### Depth 3

Compare the finalists against the weighted score, select the winning set, and then produce the final rewritten prompt.

## Selection Discipline

- Prefer the smallest principle set that materially improves the prompt.
- Do not select techniques because they are fashionable.
- Do not add reasoning-heavy techniques to simple prompts.
- If the user optimizes for scale, bias toward simpler techniques.
- If the task depends on pattern imitation, prefer few-shot over abstract instructions.
- If the task depends on investigation, consider ReAct.
- If the task depends on staged outputs, consider chaining.
- If the task depends on progressive decomposition, consider least-to-most.
- If the task needs structured long-form output, consider skeleton of thought.
- If the task has objective reasoning and high variance risk, consider self-consistency.
