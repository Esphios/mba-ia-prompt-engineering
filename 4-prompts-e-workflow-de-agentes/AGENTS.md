# AGENTS.md

This chapter is specification-driven. It does not contain an executable multi-agent system implementation; it contains Markdown specifications that define how a coordinator and specialist agents should behave when producing a full project-state report.

Use this file as the operational source of truth for AI agents working in this folder.

## Purpose

The goal of this chapter is to model a coordinator-led multi-agent workflow for generating an auditable project analysis composed of:

- one dependency report
- one architecture report
- one component report per architecturally significant component
- one `MANIFEST.md` maintained by the orchestrator
- one final `README-YYYY-MM-DD-HH:MM:SS.md` that indexes all generated reports

## What This Folder Contains

```text
4-prompts-e-workflow-de-agentes/
├── AGENTS.md
├── prompts-e-workflow-de-agentes.md
├── workflow-e-historico.md
├── agents/
│   ├── orchestrator.md
│   ├── architectural-analyzer.md
│   ├── component-deep-analyzer.md
│   └── dependency-auditor.md
└── commands/
    └── run-project-state-full-report.md
```

## Role Of Each File

- `AGENTS.md`
  Operational instructions for agents working in this chapter.
- `prompts-e-workflow-de-agentes.md`
  Study material that explains the concepts, prompt structures, and rationale behind the workflow.
- `workflow-e-historico.md`
  Preserved historical notes, editorial context, and complementary workflow memory from the previous `AGENTS.md`.
- `agents/orchestrator.md`
  Registry and manifest specialist. It does not coordinate task creation.
- `agents/architectural-analyzer.md`
  Produces the architecture report and the component list used downstream.
- `agents/component-deep-analyzer.md`
  Produces one deep-dive report per component.
- `agents/dependency-auditor.md`
  Produces the dependency audit report.
- `commands/run-project-state-full-report.md`
  Defines the execution flow that the coordinator should follow.

## Environment Assumptions

- No virtual environment is required.
- No `requirements.txt` or install step is required for this chapter itself.
- The material is intended for coordinator-style agent environments such as Claude Code.
- Optional MCP servers may be used by specialists when their specifications allow it, especially for dependency validation.

## Core Architecture

This folder models a coordinator-led architecture with strict separation of responsibilities.

### Coordinator

The coordinator:

- reads the command specification
- decides task order and parallelism
- invokes each specialist separately
- passes the required context to each specialist
- triggers the orchestrator after each completed specialist task
- validates final coverage before closing the workflow

### Orchestrator

The orchestrator:

- initializes the output structure
- creates and maintains `MANIFEST.md`
- registers completed reports
- validates paths, deduplicates entries, and tracks coverage
- never spawns or coordinates other agents

### Specialists

The specialists:

- analyze only their own scope
- produce descriptive reports
- do not coordinate the workflow
- do not modify the codebase

## Non-Negotiable Rules

### Agent separation

- Each agent must be invoked in its own task.
- The orchestrator must never spawn or schedule other agents.
- The coordinator must never delegate the full workflow to the orchestrator.

### Path discipline

- Follow each specification exactly.
- Do not invent folders such as `reports/`, `output/`, or `tmp/` unless explicitly required by the command or agent specification.
- Use normalized repository-root-relative paths that start with `/` when registering report locations in `MANIFEST.md` and README links.

### Output discipline

- Reports are descriptive, not prescriptive.
- Do not propose code changes, refactors, migrations, or upgrades.
- Do not fabricate vulnerabilities, versions, or evidence.
- Do not use vague language such as "probably safe" or "should be fine".
- Do not use emojis or stylized characters.
- Do not provide time estimates.

### Coverage discipline

- Every component listed by the architecture report must receive its own component analysis report.
- Coverage must be verified before finalization.
- Missing component reports must trigger additional component-analysis tasks.

### Manifest discipline

- Only the orchestrator writes `MANIFEST.md`.
- `MANIFEST.md` is the source of truth for generated outputs.
- The coordinator should treat missing or invalid manifest entries as workflow failures that need correction before finalization.

## Canonical Workflow

### Phase 1: Orchestrator setup

The coordinator calls the orchestrator to:

- read and normalize user flags such as `--project-folder`, `--output-folder`, and `--ignore-folders`
- create only the required directories
- initialize `MANIFEST.md`

### Phase 2: Parallel primary analysis

The coordinator runs in parallel:

- `dependency-auditor`
- `architectural-analyzer`

After each completion, the coordinator calls the orchestrator to register the output in `MANIFEST.md`.

### Phase 3: Parallel component analysis

The coordinator:

- reads the architecture report
- extracts the list of components
- launches one `component-deep-analyzer` task per component
- verifies 100% component coverage

After each completion, the coordinator calls the orchestrator to register the output.

### Phase 4: Orchestrator finalization

The coordinator calls the orchestrator to:

- validate all tracked paths
- deduplicate entries
- confirm component coverage
- finalize `MANIFEST.md`

### Phase 5: Final README generation

The coordinator:

- reads `MANIFEST.md`
- validates the referenced paths
- generates `README-YYYY-MM-DD-HH:MM:SS.md` in the orchestrator directory

## Expected Output Structure

When an output folder is used, the logical structure should be:

```text
<output-folder>/
├── orchestrator/
│   ├── MANIFEST.md
│   └── README-YYYY-MM-DD-HH:MM:SS.md
├── architectural-analyzer/
│   └── architectural-report-YYYY-MM-DD-HH:MM:SS.md
├── component-deep-analyzer/
│   ├── component-analysis-<component-name>-YYYY-MM-DD-HH:MM:SS.md
│   └── ...
└── dependency-auditor/
    └── dependencies-report-YYYY-MM-DD-HH:MM:SS.md
```

If the command or agent specification requires a different exact filename pattern, that specification takes precedence.

## How To Use This Folder

### If you are an AI coordinator

1. Read `commands/run-project-state-full-report.md`.
2. Read the relevant files under `agents/`.
3. Apply the workflow exactly as specified.
4. Use `AGENTS.md` for cross-cutting rules and folder-level conventions.
5. Use `prompts-e-workflow-de-agentes.md` for conceptual understanding, not as the canonical operational instruction set.
6. Use `workflow-e-historico.md` only when historical context or prior workflow wording is helpful.

### If you are studying the material

- Read `prompts-e-workflow-de-agentes.md` first for the explanation.
- Use the files in `agents/` and `commands/` as concrete examples of the abstractions discussed in the lesson.
- Use this `AGENTS.md` to understand how those artifacts fit together operationally.
- Use `workflow-e-historico.md` when you want preserved context from the previous organization of the chapter.

## Practical Mapping

### Prompt-structure example

The lesson's explanation of persona, objective, inputs, outputs, criteria, ambiguity handling, negative instructions, and workflow is concretely represented in:

- `agents/dependency-auditor.md`

### Multi-agent workflow example

The lesson's explanation of phased orchestration is concretely represented in:

- `commands/run-project-state-full-report.md`
- `agents/orchestrator.md`
- `agents/architectural-analyzer.md`
- `agents/component-deep-analyzer.md`

### Manifest-as-source-of-truth example

The lesson's explanation of registry, tracking, and consolidation is concretely represented in:

- `agents/orchestrator.md`

### Historical context and workflow memory

The chapter's preserved historical and editorial context is documented in:

- `workflow-e-historico.md`

## Usage Examples

```bash
/run-project-state-full-report
/run-project-state-full-report --project-folder=my-project
/run-project-state-full-report --project-folder=my-project --output-folder=analysis-output
/run-project-state-full-report --ignore-folders=venv,node_modules,.git,dist
```

## Final Guidance

- Treat `AGENTS.md` as the folder's operational contract.
- Treat `prompts-e-workflow-de-agentes.md` as the study guide.
- Treat `workflow-e-historico.md` as the preserved historical and editorial context.
- When both discuss the same concept, prefer `AGENTS.md` for execution behavior and `prompts-e-workflow-de-agentes.md` for interpretation and learning.
