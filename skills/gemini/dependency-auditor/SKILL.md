---
name: dependency-auditor
description: Audit a project's dependencies and produce a structured report covering direct dependency versions, latest stable releases, maintenance status, vulnerabilities, licenses, critical usage concentration, and verification gaps. Use when Gemini needs to assess dependency health, identify outdated or risky libraries, review security exposure in third-party packages, or create an evidence-based dependency audit before release or modernization work.
---

# Dependency Auditor

Use this skill to inspect dependency manifests and produce an evidence-based dependency audit report.
Stay in analysis mode: do not upgrade packages, do not prescribe migrations, and do not modify project source files except when saving the final report requested by the task.

## When To Use

- Assess dependency health before release, modernization, or security review.
- Identify outdated, deprecated, unsupported, or vulnerable direct dependencies.
- Review license posture, maintenance risk, and critical usage concentration.

## Inputs

- Dependency manifests and lockfiles such as `package.json`, `package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`, `requirements.txt`, `Pipfile.lock`, `poetry.lock`, `go.mod`, `Cargo.toml`, `pom.xml`, `build.gradle`, and `composer.json`.
- Detected languages, frameworks, and tools from the repository.
- Optional user instructions that focus on security, licensing, or specific ecosystems.

If no dependency files are detected, explicitly request the file path or confirm whether to proceed with limited information.

## Workflow

1. Detect the audit scope and read repository guidance.
If the user specifies a folder or ecosystem, audit only that scope. Otherwise audit the whole project.
Before drawing conclusions, read repository guidance such as `AGENTS.md`, `GEMINI.md`, `README.md`, and any dependency-management docs when present.

2. Gather dependency evidence.
Inspect manifests, lockfiles, and dependency-related repository metadata across all relevant ecosystems.
Build an inventory of direct dependencies only unless the user explicitly asks for transitive analysis.

3. Determine declared versions.
Read current versions from repository files first.
Do not infer declared versions from external sources.

4. Validate external facts.
When internet or MCP access is available, validate latest stable versions, maintenance signals, known advisories, and licenses using authoritative sources such as official package registries, vendor advisories, release pages, or official repositories.
If validation is unavailable or incomplete, move affected packages to `Unverified Dependencies`.

5. Assess dependency risk.
Identify outdated, deprecated, unsupported, unmaintained, vulnerable, or high-concentration dependencies.
Separate verified findings from partially verified or unverified findings.
Consider packages unmaintained for more than one year as risky only when registry or repository evidence supports that conclusion.
Highlight breaking-change risk in newer versions only when authoritative release notes or versioning signals support that conclusion.

6. Trace critical usage.
Identify up to 10 critical files where risky dependencies concentrate or touch important system flows.
Use relative paths and explain why each file is operationally important.

7. Produce the report.
Return a Markdown report named `Dependency Audit Report` using the structure below.

8. Save the report when required.
Save the full report to `/docs/agents/dependency-auditor/dependencies-report-{YYYY-MM-DD-HH:mm:ss}.md` unless the user explicitly provides another path.
If no orchestrator agent exists, add a short plain-text status line after the report with the saved relative path.

## Verification Rules

- Treat repository manifests and lockfiles as the source of truth for declared versions.
- Use authoritative external sources for latest versions, advisories, maintenance signals, and licenses when available.
- Separate `Verified`, `Partially Verified`, and `Unverified` findings when needed.
- If internet or registry access is unavailable, explicitly state the limitation and avoid guessing.
- Cite the basis for each high-severity finding.

## .NET Framework Guidance

When the project is a .NET Framework solution, treat these dependency sources as primary:

- `packages.config`
- `*.csproj` `<Reference>` entries, `<HintPath>`, and project-to-project references
- `app.config` and `web.config` assembly bindings and binding redirects
- solution-level `packages/` folders and NuGet restore metadata when present

For .NET Framework dependency audits, distinguish:

- NuGet package dependencies versus project references
- framework assemblies versus third-party assemblies
- GAC or machine-level assumptions versus repository-contained dependencies
- direct references in `packages.config` versus manually referenced DLLs committed to the repository

Pay attention to common .NET Framework dependency risk signals:

- outdated `System.Web`-era libraries, MVC or Web API packages, OWIN packages, WCF-related packages, JSON serializers, logging frameworks, DI containers, and old EF packages
- manually copied DLLs, vendor binaries, or private `lib/` folders with unclear provenance
- binding redirects masking version drift
- mismatches between `packages.config`, actual referenced DLL versions, and deployed expectations
- packages targeting only old framework versions or abandoned maintainers

When identifying critical files, prioritize:

- composition roots such as `Global.asax`, `Startup.cs`, `App_Start/*`
- central configuration files such as `web.config` and `app.config`
- shared infrastructure libraries and base classes
- controllers, services, or repository layers that concentrate risky package usage

## Output Structure

Produce these sections in order:

1. `Summary`
State the audited ecosystems, scope, and main findings.

2. `Critical Issues`
Highlight security vulnerabilities, deprecated dependencies, unsupported packages, and materially risky version gaps.
Include CVE identifiers only when verified.

3. `Dependencies`
Present direct dependencies with:
`Dependency | Ecosystem | Current Version | Latest Stable Version | Status | Verification Basis`

4. `Risk Analysis`
Present evidence-based risks with:
`Severity | Dependency | Issue | Details | Evidence`

5. `Unverified Dependencies`
Include this section only when some dependencies could not be fully verified.
Use:
`Dependency | Current Version | Reason Not Verified`

6. `Critical File Analysis`
Analyze up to 10 critical files that rely on risky dependencies.

7. `Integration Notes`
Summarize how risky or business-critical dependencies are used in the project and where the integration appears.

Always use relative paths when referencing files inside the report.
Keep the report descriptive and evidence-driven. Do not add upgrade recommendations unless the user explicitly asks for them outside this skill's normal scope.

## Ambiguity Handling

- If multiple ecosystems are present, audit each one separately and state this in the summary.
- If external registries or advisory sources cannot be reached, state the limitation clearly and move affected packages to `Unverified Dependencies`.
- If version information is missing from repository files, document the missing evidence instead of guessing the version.
- If lockfiles are missing, state the increased reproducibility and verification risk.
- If the user did not specify a folder to audit, audit the entire project. Otherwise audit only the folder provided.
- If a dependency name maps to multiple possible packages, resolve it using the manifest ecosystem and namespace before reporting.
- If a .NET Framework project references assemblies directly without NuGet metadata, report them as manually managed dependencies and explain the verification limitation.

## Error Format

When meaningful analysis is impossible, return:

```text
Status: ERROR

Reason: Provide a clear explanation of why the audit could not be performed.

Suggested Next Steps:

* Provide the path to the dependency manifest
* Grant workspace read permissions
* Confirm which ecosystem should be audited
```

## Guardrails

- Do not modify the codebase, except for saving the final report file when required.
- Do not run upgrade commands or prescribe migrations.
- Do not fabricate versions, licenses, advisories, maintenance status, or CVE identifiers.
- Do not present transitive dependencies as direct dependencies unless the user explicitly asked for them.
- Do not use vague language such as `probably safe` or `should be fine`.
- Do not use emojis or stylized characters.
- Do not provide time estimates or decorative output.
