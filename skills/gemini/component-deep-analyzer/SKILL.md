---
name: component-deep-analyzer
description: Perform deep technical analysis of a software component and produce a structured report covering internals, business rules, data flow, dependencies, coupling, endpoints, integrations, tests, and risks. Use when Gemini needs to explain how a service, module, package, or bounded component works, analyze a component named in an architecture report, or create an evidence-based component deep-dive before refactoring or technical planning.
---

# Component Deep Analyzer

Use this skill to inspect a specific component or service boundary and produce a deep, evidence-based analysis report.
Stay in analysis mode: do not refactor, do not propose implementation changes, and do not modify project source files except when saving the final report requested by the task.

## Imported Metadata

Preserve the following source metadata as reference only. Gemini does not consume it as native config.

- `Display name`: `Component Deep Analyzer`
- `Short description`: `Deep component behavior analysis`
- `Suggested prompt`: `Use $component-deep-analyzer to inspect this component and produce a structured deep analysis report.`

## When To Use

- Explain how a service, module, package, or bounded component actually works.
- Deep-dive a component identified as critical by an architecture report.
- Map business rules, data flow, dependencies, endpoints, tests, and risk inside one boundary.

## Inputs

- Component or service directories specified by the user or identified from architecture reports.
- Source code files: implementation files, interfaces, tests, and configuration files.
- Component documentation such as API specs, README files, and inline documentation.
- Configuration files such as environment configs, feature flags, and deployment settings.
- Test files such as unit tests, integration tests, fixtures, and mocks.
- Dependency declarations such as import statements, dependency injection wiring, manifests, and module wiring.
- Optional architecture report to identify critical components for analysis.
- Optional user instructions that focus on specific business logic, integrations, or patterns.

If the user provides only a component name, attempt a best-effort resolution using repository structure, naming, and architecture reports, then state the resolved boundary explicitly.
If no component path, component name, or architecture report is available, request clarification on which component to analyze.

## Workflow

1. Detect the component scope and read repository guidance.
If the user provides a component path, analyze that boundary.
If the user provides only a component name, resolve it best-effort from repository structure, naming, and any architecture report, then state the assumed boundary explicitly.
Before drawing conclusions, read repository guidance such as `AGENTS.md`, `GEMINI.md`, `README.md`, and any component-local docs when present.

2. Gather component evidence.
Inspect implementation files, interfaces, configuration, tests, documentation, manifests, and relevant supporting files outside the component boundary such as shared schemas or shared tests.

3. Reconstruct the component behavior.
Map entry points, processing steps, validations, state changes, integrations, and outputs.
Separate observed behavior from inferred runtime behavior.
Map compile-time dependencies directly from code and configuration.
Map runtime dependencies and flows only when they are evidenced or strongly implied by concrete artifacts. Otherwise mark them as inferred.

4. Extract business rules and domain logic.
Document only material rules supported by code, tests, configuration, or documentation.
Use confidence indicators when the rule is implicit rather than explicit.

5. Analyze structure and dependencies.
Describe internal organization, direct dependencies, inferred runtime links, integration points, design patterns, and afferent and efferent coupling.
If exact counts are not feasible, provide best-effort estimates and explain the basis.
Analyze data models, schemas, and validation rules.

6. Assess quality and risk.
Review error handling, resilience patterns, security-relevant behavior, technical debt, tests, performance signals, and operational risks.
Document configuration management and environment-specific behavior when visible in the repository.

7. Produce the report.
Return a Markdown report named `Component Deep Analysis Report` using the structure below.

8. Save the report when required.
Save the full report to `/docs/agents/component-deep-analyzer/component-analysis-{component-name}-{YYYY-MM-DD-HH:mm:ss}.md` unless the user explicitly provides another path.
If no orchestrator agent exists, add a short plain-text status line after the report with the saved relative path.

## Evidence Rules

- Separate `Observed`, `Inferred`, and `Unknown` when the distinction matters.
- Ground business rules in code, tests, configuration, or documentation.
- Cite relative paths and line numbers for key findings.
- Explain the basis for coupling counts or estimates before presenting them.
- If runtime behavior is only implied, call that out instead of presenting it as confirmed.

## .NET Framework Guidance

When the analyzed component belongs to a .NET Framework solution, inspect these artifacts first:

- `*.csproj`, project references, `packages.config`, `AssemblyInfo.cs`
- `web.config`, `app.config`, config transforms, custom config sections, binding redirects
- `Global.asax`, `App_Start/*`, route registration, OWIN `Startup.cs`, filter registration, dependency injection bootstrapping
- MVC and Web API entry points such as controllers, model binders, filters, attributes, Areas, formatters
- Web Forms artifacts such as `.aspx`, `.ascx`, `.master`, and their code-behind files
- WCF artifacts such as `*.svc`, service contracts, data contracts, and generated clients
- Data access code such as `DbContext`, EDMX, repositories, unit-of-work implementations, LINQ queries, ADO.NET commands, stored procedure wrappers
- Background processing or integration code such as Windows services, timers, Quartz or Hangfire jobs, MSMQ handlers, scheduled tasks

For .NET Framework components, pay special attention to these common patterns:

- controller or page to application service to domain service to repository to database
- heavy use of configuration-driven behavior in `web.config` or `app.config`
- custom attributes, action filters, base controllers, helper classes, and static utilities that hide business rules or authorization behavior
- partial classes and code-behind patterns where behavior is split across generated and hand-written files
- mixed responsibilities inside legacy services, managers, facades, and repository classes

When mapping component boundaries, do not treat generated files, designer files, migrations, proxies, or code-behind companions as independent business components unless they clearly own behavior.

## Output Structure

Produce these sections in order:

1. `Executive Summary`
State the component purpose, system role, analyzed scope, key findings, and important limitations or assumptions.

2. `Data Flow Analysis`
Describe how data moves through the component from entry points to outputs or side effects.
Use separate flows when multiple entry points exist.

3. `Business Rules & Logic`
Include an overview table with:
`Rule Type | Rule Description | Location | Confidence`

For each material rule include:
`Overview`
`Evidence`
`Detailed description`
`Rule workflow`

4. `Component Structure`
Show the internal organization with a short tree and relative paths.

5. `Dependency Analysis`
Present internal and external dependencies.
Distinguish direct evidence from inferred runtime dependencies.

6. `Afferent and Efferent Coupling`
Adapt the unit of analysis to the language and paradigm, for example classes, interfaces, structs, modules, packages, handlers, or services.
Explain the counting basis before presenting the table.
Use:
`Component | Afferent Coupling | Efferent Coupling | Criticality | Basis`

7. `Endpoints`
Include this section only if the component exposes endpoints or message consumers.
Use a protocol-appropriate table.

8. `Integration Points`
Present APIs, databases, brokers, and cross-component services with:
`Integration | Type | Purpose | Protocol | Data Format | Error Handling`

9. `Design Patterns & Architecture`
Document only patterns and architectural decisions supported by evidence.

10. `Technical Debt & Risks`
Present evidence-based issues with:
`Risk Level | Component Area | Issue | Impact | Evidence`

11. `Test Coverage Analysis`
Assess tests located inside or outside the component boundary when relevant.
Use quantitative coverage only when explicit coverage artifacts exist. Otherwise provide a qualitative assessment.

Always use relative paths when referencing files inside the report.
Include line numbers when citing specific code locations.
Keep the report descriptive and evidence-driven. Do not add recommendations.

## Ambiguity Handling

- If multiple components are requested, analyze each separately with clear delineation.
- If business rules are implicit, document them with confidence indicators and supporting evidence.
- If external dependencies are mocked or stubbed, note this and distinguish intended contracts from runtime implementation.
- If test coverage evidence is missing, call that out as a risk instead of inventing coverage numbers.
- If the user provides an architecture report, prioritize components marked as critical.
- If patterns are ambiguous, document the competing interpretations and the evidence for each.
- If configuration varies by environment, document the variations found and their likely effect.
- If component boundaries are ambiguous, state the assumed boundary explicitly before presenting findings.
- If a .NET Framework component spreads behavior across markup, code-behind, configuration, filters, and base classes, aggregate those artifacts into the same behavioral analysis instead of analyzing only the obvious class file.
- If the component does not expose endpoints, omit the `Endpoints` section entirely.

## Error Format

When meaningful analysis is impossible, return:

```text
Status: ERROR

Reason: Provide a clear explanation of why the analysis could not be performed.

Suggested Next Steps:

* Provide the correct path or component name
* Grant workspace read permissions
* Specify which component from the architecture report to analyze
* Confirm the component boundaries and scope
```

## Guardrails

- Do not modify the codebase, except for saving the final report file when required.
- Do not provide refactoring recommendations or implementation guidance.
- Do not execute code, run tests, or claim runtime behavior that cannot be evidenced from repository artifacts.
- Do not present undocumented business rules as facts.
- Do not provide opinions on technology choices.
- Do not fabricate dependency versions, exact coupling counts, or coverage percentages when the repository does not provide them.
- Do not skip relevant test files or configuration files.
- Do not provide time estimates, recommendations, or decorative output.
