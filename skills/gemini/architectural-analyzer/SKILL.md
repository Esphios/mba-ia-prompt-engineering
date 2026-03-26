---
name: architectural-analyzer
description: Analyze the architecture of a codebase and produce a structured report with system overview, critical components, dependencies, coupling, integrations, risks, security, and infrastructure findings. Use when Gemini needs to understand a project's architecture, assess coupling or architectural debt, map service boundaries, review integration points, or create an evidence-based architectural report before refactoring or technical planning.
---

# Architectural Analyzer

Use this skill to inspect a codebase and produce a comprehensive, evidence-based architectural analysis report.
Stay in analysis mode: do not refactor, do not propose implementation changes, and do not modify project source files except when saving the final report requested by the task.

## When To Use

- Understand the system shape before refactoring or modernization.
- Map service boundaries, dependency direction, or coupling hotspots.
- Review architectural risk, integration points, and runtime concerns.
- Produce a reusable architecture report grounded in repository evidence.

## Inputs

- Source code files across all relevant directories and subdirectories.
- Configuration files such as `docker-compose.yml`, `Dockerfile`, `kubernetes/*.yaml`, `.env`, and similar runtime configuration.
- Build and deployment scripts such as `Makefile`, CI/CD workflows, and deployment scripts.
- Documentation files such as architecture diagrams, README files, and API documentation.
- Package management files such as `package.json`, `requirements.txt`, `pom.xml`, and `go.mod`.
- Database schemas, migration files, and data models when present.
- Optional user instructions that narrow the analysis to specific layers, components, or architectural concerns.

If no source code is detected but configuration or documentation is available, proceed with a limited-scope analysis and state the limitation explicitly.
If there is not enough source code, configuration, or documentation to support a meaningful analysis, use the error format below.

## Workflow

1. Confirm the scope and read repository guidance.
If the user specifies a folder, service, or module, analyze only that scope. Otherwise analyze the whole project.
Before drawing conclusions, read repository guidance such as `AGENTS.md`, `GEMINI.md`, `README.md`, architecture docs, and any scope-specific documentation when present.

2. Gather architectural evidence.
Inspect source code, configuration, manifests, infrastructure files, build and deployment scripts, database artifacts, and architecture-related documentation.

3. Identify architecturally significant components.
Prioritize modules that coordinate business flows, own shared state, expose system boundaries, integrate external systems, provide shared infrastructure, or have high fan-in or fan-out.

4. Map dependencies and coupling.
Use concrete evidence such as imports, module references, routing, service wiring, configuration bindings, database access paths, and message flows.
When exact coupling counts are not feasible, provide best-effort counts and state how they were derived.

5. Assess architecture quality.
Document architectural patterns, system boundaries, integration points, deployment and runtime evidence, security boundaries, single points of failure, bottlenecks, and architectural debt.
Distinguish observed facts from high-confidence inferences and unresolved ambiguities.
Analyze configuration management and environment-specific concerns.
Identify shared libraries, utilities, and common components.

6. Produce the report.
Return a Markdown report named `Architectural Analysis Report` using the structure below.

7. Save the report when required.
Save the full report to `/docs/agents/architectural-analyzer/architectural-report-{YYYY-MM-DD-HH:mm:ss}.md` unless the user explicitly provides another path.
If no orchestrator agent exists, add a short plain-text status line after the report with the saved relative path.

## Evidence Rules

- Separate `Observed`, `Inferred`, and `Unknown` when the distinction matters.
- Cite concrete artifacts such as files, line numbers, configs, route wiring, dependency declarations, and schemas.
- Explain the counting basis before presenting coupling metrics.
- Prefer direct repository evidence over naming-based assumptions.
- If runtime behavior cannot be confirmed statically, label it as an inference and explain why it is plausible.

## .NET Framework Guidance

When the project is a .NET Framework solution, treat these artifacts as primary architectural evidence:

- Solution and project structure: `.sln`, `*.csproj`, `Directory.Build.*`, `packages.config`, `AssemblyInfo.cs`
- Runtime and environment configuration: `web.config`, `app.config`, config transforms such as `Web.Release.config`, binding redirects, custom config sections
- Application startup and composition roots: `Global.asax`, `App_Start/*`, OWIN `Startup.cs`, route config, filter config, bundle config, dependency injection bootstrapping
- Web entry patterns: ASP.NET MVC controllers, ASP.NET Web API controllers, Razor views, Areas, Web Forms pages and code-behind, `HttpModule`, `HttpHandler`
- Service and integration boundaries: WCF `*.svc`, service contracts, client proxies, ASMX services, message consumers, scheduled jobs, Windows services
- Data access patterns: Entity Framework `DbContext`, EDMX, repositories, unit of work, LINQ queries, ADO.NET, stored procedure wrappers, typed datasets
- Cross-cutting infrastructure: logging, caching, authentication and authorization, custom attributes, action filters, exception filters, base controllers, shared libraries

For .NET Framework projects, explicitly map:

- project-to-project references versus NuGet package dependencies
- layered conventions such as Presentation, Application, Domain, Infrastructure, Shared
- MVC or Web API request flow from route to controller to service to repository to database
- legacy patterns such as service locators, static helpers, configuration-heavy wiring, and mixed web or UI plus business logic layers
- deployment dependencies such as IIS, Windows services, MSMQ, COM interop, GAC references, and file-system integrations

Do not assume modern ASP.NET Core conventions. Prefer the evidence actually present in legacy ASP.NET and .NET Framework artifacts.

## Output Structure

Produce these sections in order:

1. `Executive Summary`
High-level overview of the system architecture, stack, analyzed scope, key findings, and important limitations.

2. `System Overview`
Summarize project structure, main directories, and identified architectural patterns.
Include a short tree view when it helps.

3. `Critical Components Analysis`
Present a table of architecturally significant components with:
`Component | Type | Location | Afferent Coupling | Efferent Coupling | Architectural Role | Confidence`

4. `Dependency Mapping`
Provide a high-level textual dependency map.
Separate observed dependency links from inferred runtime relationships.

5. `Integration Points`
Present external systems, APIs, databases, queues, and third-party services with:
`Integration | Type | Location | Purpose | Risk Level`

6. `Architectural Risks & Single Points of Failure`
Present critical risks and bottlenecks with:
`Risk Level | Component | Issue | Impact | Details | Evidence`

7. `Technology Stack Assessment`
Summarize frameworks, libraries, platforms, and architectural patterns in use.

8. `Security Architecture and Risks`
Highlight major security-relevant architectural observations and boundaries.

9. `Infrastructure Analysis`
Include this section only when relevant deployment, container, runtime, or infrastructure evidence exists.

Before presenting afferent and efferent coupling metrics, briefly explain what these terms mean and how they were determined in this analysis.
Always use relative paths when referencing files inside the report.
Include line numbers when citing specific code locations.
Keep the report descriptive and evidence-driven. Do not add recommendations.

## Ambiguity Handling

- Document multiple architectural patterns separately when more than one is present.
- If infrastructure evidence is missing, say so and focus on code architecture.
- If documentation is scarce, make reasonable assumptions from code structure, naming, and configuration evidence, and label them as assumptions.
- If the project spans multiple services or modules, analyze each one and their interactions.
- If component relationships are unclear, state the uncertainty instead of presenting it as fact.
- If exact runtime behavior cannot be confirmed without execution, report the most likely flow as an inference and state the basis.
- If a .NET Framework solution mixes MVC, Web API, Web Forms, WCF, jobs, or class libraries, document each runtime style separately instead of collapsing them into one pattern.
- If source code is missing but configuration or documentation exists, proceed with a limited-scope analysis and say so explicitly.
- Return an error only when there is not enough source code, configuration, or documentation to support any meaningful analysis.

## Error Format

When meaningful analysis is impossible, return:

```text
Status: ERROR

Reason: Provide a clear explanation of why the analysis could not be performed.

Suggested Next Steps:

* Provide the path to the project source code
* Grant workspace read permissions
* Confirm which components or layers should be prioritized for analysis
* Specify any particular architectural concerns to focus on
```

## Guardrails

- Do not modify the codebase, except for saving the final report file when required.
- Do not provide refactoring recommendations or implementation guidance.
- Do not create or modify architectural diagrams programmatically.
- Do not assume architectural patterns without evidence in code, configuration, or documentation.
- Do not fabricate information. If confidence is limited, say so explicitly.
- Do not catalog every file; focus on architecturally significant elements.
- Do not provide detailed performance optimization suggestions.
- Do not present recommendations, improvements, or time estimates.
- Do not use emojis or decorative characters in the report.
