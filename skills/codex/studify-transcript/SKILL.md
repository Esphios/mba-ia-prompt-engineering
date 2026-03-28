---
name: studify-transcript
description: Transform rough lecture transcripts, class notes, or OCR-derived academic text into study-ready Markdown with clearer structure, preserved meaning, selective deduplication, and optional tables or Mermaid diagrams. Use when Codex needs to reorganize one or more lecture transcriptions into a cleaner document for review, revision, memorization, or teaching support without discarding relevant content.
---

# Studify Transcript

## Overview

Convert noisy or approximate lecture transcripts into Markdown that is easier to study.
Preserve relevant content, improve editorial structure, remove only clear redundancy, and add tables or Mermaid diagrams when they materially improve comprehension.

## Workflow

1. Identify the source shape.
Determine whether the input is one transcript, several transcripts, OCR text, or loosely structured notes.

2. Infer the study goal from the material.
Prefer a structure that helps revision: topics, subtopics, definitions, examples, processes, comparisons, and open ambiguities.

3. Extract the content units before rewriting.
Locate recurring themes, definitions, formulas, examples, chronological explanations, causal chains, and repeated teacher emphasis.

4. Consolidate redundancy carefully.
Merge repeated explanations into a single clearer formulation, but keep distinct nuances, caveats, exceptions, and examples.

5. Reorder for learning value, not transcript order.
Group related material even if the original lecture returned to the same idea multiple times.

6. Rewrite for clarity without changing meaning.
Convert oral phrasing, false starts, and fragmented speech into readable written language while preserving the original ideas.

7. Add structural aids only when useful.
Use tables for comparisons, classifications, steps, pros and cons, or terminology alignment.
Use Mermaid for flows, hierarchies, cycles, sequences, and conceptual relations.

8. Flag uncertainty explicitly.
If a passage is ambiguous, incomplete, or likely mis-transcribed, keep it and label it discreetly instead of guessing.

## Output Shape

Produce Markdown with this default structure unless the material strongly suggests a better one:

1. Title
Use the inferred course, unit, or topic name when possible.

2. Overview
Add a short high-level summary only if it is clearly supported by the source.

3. Main Sections
Organize by theme, not by transcript order.
Prefer descriptive headings and a consistent hierarchy.

4. Study Aids
Include, when justified by the source:
- Concept lists
- Definitions
- Step-by-step processes
- Comparison tables
- Mermaid diagrams

5. Ambiguities
Add a final `Pontos ambíguos ou incompletos` section when uncertainty remains in the source.

## Editorial Rules

- Preserve all relevant content.
- Remove only content that is clearly redundant or empty.
- Do not invent facts, examples, definitions, or transitions not grounded in the input.
- Keep domain vocabulary unless the source itself makes it unusable.
- Prefer concise editorial rewriting over paraphrase inflation.
- Preserve distinctions between similar concepts when the source treats them differently.
- Do not flatten disagreements, caveats, or alternative formulations into one statement unless they are truly duplicate.
- When the transcript contains lists scattered across different moments, consolidate them into one coherent list.
- When producing Portuguese output, ensure correct grammar, accents, and `ç` usage.

## Diagram And Table Heuristics

Use a table when the source compares items across common dimensions.

Use Mermaid when the source describes:
- Process flow
- Dependency or prerequisite chains
- Taxonomy or hierarchy
- Event sequence
- Feedback loop

Do not add a table or diagram just for decoration.

## Failure Modes To Avoid

- Deleting repeated content that actually contains different details.
- Preserving transcript noise that harms readability without adding information.
- Over-summarizing and losing examples or caveats.
- Reordering content so aggressively that logical dependencies disappear.
- Turning uncertain passages into confident prose.
- Adding generic study notes that were not present in the source.

## Example Triggers

- "Organize this lecture transcript into a study guide."
- "Turn these class notes into clean Markdown without losing content."
- "Rewrite this OCR transcript of a lesson for easier revision."
- "Structure these lecture transcriptions with headings, tables, and Mermaid where useful."

## Default Prompting Pattern

When using this skill, instruct Codex to:

- Analyze the transcript source
- Reorganize the material for study
- Preserve relevant content
- Remove only clear redundancy
- Use Markdown throughout
- Add tables or Mermaid only when they improve understanding
