---
name: create-agentsmd
description: 'Prompt for generating a repository instruction file such as AGENTS.md, GEMINI.md, or CLAUDE.md, with bilingual output support and stronger repository analysis'
---

# Create High-Quality Repository Instruction File

You are a code agent. Your task is to create or improve a complete, accurate repository instruction file at the correct project root so coding agents can work effectively in the codebase.

Read [references/common-conventions.md](references/common-conventions.md) only when you need comparison examples for common conventions or examples of unusual project traits. Treat that file as reference material, never as repository truth.

## Target File Rules

- Default output filename: `AGENTS.md`
- If the user specifies another filename, use that exact filename, for example `GEMINI.md`, `CLAUDE.md`, or another agent-facing Markdown file.
- If the user specifies a subproject or package scope, create the file at that scope root instead of the repository root.
- If the project is a monorepo and additional nested instruction files are clearly useful, use the same target filename in subprojects unless the user asks for a different naming scheme.
- When the target filename is `AGENTS.md`, align with the public guidance at `https://agents.md/`.
- When the target filename is not `AGENTS.md`, keep the same technical depth and structure unless the user explicitly requests tool-specific wording.

Refer to the final output as the "instruction file" until the target filename is known, then use the exact filename consistently.

## Output Language Rules

- Supported output languages: `English` and `Brazilian Portuguese (pt-BR)`.
- If the user explicitly requests one of them, use that language.
- If the user does not specify a language, preserve the user's language when it is English or Brazilian Portuguese.
- If the user language is ambiguous, inspect existing repository docs and instruction files and use the dominant documentation language.
- If the language is still ambiguous after inspection, default to `English`.
- Keep commands, file paths, package names, identifiers, environment variables, and code symbols unchanged.
- Translate headings, explanations, and examples into the selected output language.
- Do not mix English and Brazilian Portuguese in the same generated file unless quoting repository text or preserving a literal identifier.
- If the repository itself is bilingual, mention that as a project characteristic rather than mixing output styles.

## Purpose

The instruction file is a focused technical guide for coding agents. It should complement human-facing docs such as `README.md`, not repeat them blindly.

The file should help an agent answer questions like:

- What is this project and how is it structured?
- How do I install, run, build, test, lint, and debug it?
- Which primary technologies are actually used here, including frameworks, databases, infrastructure, and important specialized dependencies?
- Which directories, packages, layers, or services matter most?
- What coding, logging, dependency injection, configuration, and workflow conventions should I follow?
- Which commit, PR, CI, and release patterns are expected?
- What is unusual in this repository compared with common conventions for this stack?

## Core Principles

- Be evidence-based. Prefer repository evidence over assumptions.
- Be actionable. Include commands an agent can actually run.
- Be specific. Use real paths, scripts, tools, and file names.
- Be scoped. Include only sections that are relevant to this project.
- Be honest. Mark gaps or uncertainty instead of inventing conventions.
- Be reusable. Capture durable project conventions, not temporary task notes.
- Use examples when they clarify a convention, but do not fabricate repository-specific examples.
- Compare the repository against common conventions only to improve clarity, not to force the project into a generic template.
- Surface material assumptions separately in the chat or terminal response instead of hiding them inside the generated instruction file.

## Inputs

Use these sources when present:

- Existing instruction files such as `AGENTS.md`, `GEMINI.md`, `CLAUDE.md`, or equivalents
- `README.md`, contribution docs, architecture docs, runbooks, ADRs, and onboarding notes
- Build manifests, package manifests, lockfiles, and workspace configuration
- CI/CD workflows and deployment scripts
- Application configuration, environment templates, and startup wiring
- Test configuration, fixtures, and representative tests
- Git history, PR templates, issue templates, and repository automation
- User instructions about filename, scope, sections, language, or preferred level of detail
- [references/common-conventions.md](references/common-conventions.md) for examples and comparison points only

## Workflow

1. Determine scope, target filename, and output language.

- Use the filename requested by the user.
- If no filename is provided, default to `AGENTS.md`.
- Resolve whether the file belongs at repository root or a subproject root.
- Resolve whether the output should be in English or Brazilian Portuguese using the language rules above.

2. Read existing guidance before drafting.

- Check for existing instruction files and nearby docs before writing new content.
- Reuse valid project terminology and command names.
- If an instruction file already exists, update and improve it instead of replacing useful content blindly.

3. Detect the project shape and primary technologies.

- Determine whether the project is a single package, monorepo, service collection, library, CLI, web app, mobile app, desktop app, or mixed repository.
- Identify the primary languages, frameworks, package managers, runtime entry points, and test layers.
- Build a technology inventory that includes frameworks, databases, ORMs, queues, caches, cloud SDKs, authentication libraries, validation libraries, file-processing libraries, document-parsing libraries, testing tools, build tools, deployment tooling, and observability tooling when they are materially used.

4. Gather evidence from code, config, automation, and history.

- Inspect startup or composition roots, manifests, test configs, lint or format configs, CI pipelines, environment files, and deployment scripts.
- Read enough representative source files to confirm the real architecture, dependency usage, and naming conventions.
- Read dependency manifests together with representative code usage so the technology inventory reflects actual usage, not only installed packages.
- Inspect recent Git history to infer commit and workflow conventions.

5. Extract project conventions and peculiarities.

- Document build, run, test, lint, format, debug, release, and deployment patterns.
- Document logging, dependency injection, configuration, error handling, secrets, migrations, and architectural conventions when evidenced.
- Compare observed patterns with common conventions so you can call out both the familiar parts and the unusual parts explicitly.
- Capture important directory boundaries and "do not edit" areas such as generated code, vendor files, or build outputs.
- Identify peculiarities such as nonstandard directory layouts, custom wrappers, unusual bootstrapping, mixed runtime styles, legacy holdovers, or repository-specific rules that differ from the most common conventions for that stack.

6. Write the instruction file.

- Use only relevant sections.
- Prefer concise bullets and short command examples.
- Include warnings, gotchas, and repository-specific pitfalls when useful.
- Include a `Primary Technologies` section and a `Project Peculiarities` section whenever there is enough evidence to make them useful.
- When a convention benefits from an example, add a short example pattern, but only if it matches repository evidence or is clearly labeled as a common convention example.

7. Validate before finishing.

- Verify that listed commands, paths, package names, and file names exist.
- If a command cannot be verified, either test it or mark it as unverified.
- Verify that important technologies in the final file are backed by evidence.
- Verify that the generated content is consistently in the selected language.

8. Report assumptions in the chat or terminal response.

- Do not write the assumptions section into the generated instruction file unless the user explicitly asks for that.
- Report assumptions caused by missing user inputs, inaccessible or unreadable files, unreachable logic, ambiguous repository evidence, or unverified commands.
- Rank assumptions from lowest certainty to highest certainty.
- If there are no material assumptions, say so explicitly.

## Repository Discovery Strategy

Always start broad, then narrow:

- Find root-level manifests and workspace markers first.
- Find startup or composition roots next.
- Then inspect tests, CI, deployment, and representative feature code.
- Prefer `rg --files` and targeted file reads over scanning every file manually.

### Suggested Discovery Commands

Use targeted searches like these and adapt them to the repository:

- General: `rg --files -g 'README.md' -g 'CONTRIBUTING.md' -g '.env*' -g 'Dockerfile' -g '.github/workflows/*'`
- C#/.NET: `rg --files -g '*.sln' -g '*.csproj' -g 'Directory.Build.*' -g 'appsettings*.json' -g 'web.config' -g 'Program.cs' -g 'Startup.cs'`
- JS/TS: `rg --files -g 'package.json' -g 'pnpm-workspace.yaml' -g 'turbo.json' -g 'nx.json' -g 'tsconfig*.json' -g 'vite.config.*' -g 'next.config.*'`
- HTML or frontend templates: `rg --files -g '*.html' -g 'templates/**' -g 'views/**' -g 'layouts/**' -g 'partials/**' -g 'tailwind.config.*'`
- Python: `rg --files -g 'pyproject.toml' -g 'requirements*.txt' -g 'pytest.ini' -g 'tox.ini' -g 'noxfile.py' -g 'manage.py' -g 'alembic.ini'`
- Java: `rg --files -g 'pom.xml' -g 'build.gradle*' -g 'settings.gradle*' -g 'application*.yml' -g 'application*.properties'`
- Git conventions: `git log --oneline --decorate -n 30` and `git log --format='%h %s' -n 50`
- Workflow conventions: inspect `.github/workflows/*`, release scripts, pre-commit config, and package-specific CI files

### General Evidence To Inspect First

- `.git`, `.github/workflows`, `.gitlab-ci.yml`, `azure-pipelines.yml`, `Jenkinsfile`, `.circleci/config.yml`
- `README.md`, `CONTRIBUTING.md`, `docs/`, `adr/`, `architecture/`
- `Dockerfile`, `docker-compose*.yml`, `compose.yml`, deployment manifests
- `.env*`, environment templates, secrets examples, runtime config directories
- Lint and format configs
- Existing instruction files and local docs in subprojects

## Technology Inventory Strategy

The `Primary Technologies` section should capture the technologies that materially shape the repository.

- Do not stop at the top-level framework or database.
- Include specialized libraries when they clearly influence implementation, for example XML, CSV, Excel, PDF, image, audio, video, archive, storage, parser, crawler, or file-manipulation dependencies.
- Prefer technologies evidenced by both dependency manifests and actual code usage.
- When a dependency is listed but there is no visible usage, either omit it or mark it as present but unverified in usage.
- Do not dump every transitive dependency. Focus on direct dependencies and materially used libraries that help an agent understand how the project works.

Capture technologies across categories such as:

- Language and runtime
- Application framework
- Package manager and workspace tooling
- Database, ORM, query builder, or migration tool
- Messaging, cache, search, or background processing
- Authentication, authorization, and validation
- Logging, telemetry, and observability
- File, document, media, or data-format processing libraries
- Testing, linting, formatting, static analysis, and type checking
- Build, bundling, containerization, deployment, and infrastructure tooling

When helpful, present `Primary Technologies` as a compact table:

`Category | Technology | Evidence | Purpose`

### C# and .NET Search Priorities

Inspect these first when C# is present:

- `*.sln`, `*.csproj`, `Directory.Build.props`, `Directory.Build.targets`, `global.json`, `NuGet.config`, `packages.config`
- `Program.cs`, `Startup.cs`, `Global.asax`, `App_Start/*`, `launchSettings.json`
- `appsettings*.json`, `web.config`, `app.config`, config transforms
- Test projects such as `*.Tests`, `*.Test`, `*.IntegrationTests`, `*.FunctionalTests`
- `Properties/launchSettings.json`, `Controllers/`, `Endpoints/`, `Pages/`, `Areas/`, `BackgroundServices/`, `HostedServices/`
- Migration folders, EF `DbContext`, repository classes, message handlers, jobs

Look for these patterns explicitly:

- Logging: `ILogger`, Serilog, NLog, log4net, custom logging wrappers
- Dependency injection: `builder.Services`, `services.Add*`, Autofac modules, StructureMap, SimpleInjector, Ninject, service locators
- Configuration binding: options classes, `IOptions<>`, config sections, custom config providers
- Architecture: controller-to-service-to-repository flow, CQRS handlers, MediatR, clean architecture layers, legacy static helpers

### JavaScript and TypeScript Search Priorities

Inspect these first when JS or TS is present:

- `package.json`, lockfiles, `pnpm-workspace.yaml`, `turbo.json`, `nx.json`, workspace config
- `tsconfig*.json`, `jsconfig.json`, bundler config such as `vite.config.*`, `webpack.*`, `rollup.config.*`
- Framework config such as `next.config.*`, `nuxt.config.*`, `astro.config.*`, `svelte.config.*`
- `src/`, `app/`, `pages/`, `packages/`, `apps/`, `services/`, `libs/`
- Test config such as `vitest.config.*`, `jest.config.*`, `playwright.config.*`, `cypress.config.*`
- Lint and format config such as ESLint, Prettier, Biome, Rome

Look for these patterns explicitly:

- Package manager and script conventions: npm, pnpm, yarn, bun
- Monorepo boundaries and package naming
- Logging: `pino`, `winston`, `bunyan`, `debug`, framework-specific logger wrappers
- Dependency injection or wiring: NestJS providers or modules, inversify, awilix, manual composition roots
- Configuration: `.env*`, runtime config modules, `process.env`, `import.meta.env`, typed config wrappers
- Architecture: feature folders, domain or service patterns, API clients, shared UI packages, state management conventions

### HTML and Frontend Template Search Priorities

When the project includes significant HTML or template-driven frontend structure, inspect:

- `index.html`, `public/`, `templates/`, `views/`, `layouts/`, `partials/`, `components/`
- Static site generators or template engines such as Jekyll, Hugo, Eleventy, Handlebars, EJS, Nunjucks
- CSS tooling and design-system markers such as Tailwind, Sass, PostCSS, design token files
- Asset pipelines, build output directories, and hydration or SSR boundaries

Look for these patterns explicitly:

- Shared layout and partial conventions
- Asset organization and generated output folders
- Accessibility and semantic HTML conventions if reflected in templates or lint rules
- Whether HTML is source-of-truth content, generated output, or server-rendered view layer

### Python Search Priorities

Inspect these first when Python is present:

- `pyproject.toml`, `requirements*.txt`, `poetry.lock`, `Pipfile`, `Pipfile.lock`, `setup.py`, `setup.cfg`
- `pytest.ini`, `tox.ini`, `noxfile.py`, `conftest.py`, `manage.py`
- Application entry points such as `main.py`, `app.py`, `wsgi.py`, `asgi.py`, CLI modules
- Framework structure such as Django apps, FastAPI routers, Flask app factory, Celery workers, Alembic migrations
- Virtual environment or tool config such as Ruff, Black, isort, mypy

Look for these patterns explicitly:

- Logging: `logging` module config, structlog, loguru, framework logging wrappers
- Dependency injection or provider patterns: FastAPI `Depends`, dependency-injector, app factory wiring, service container modules
- Configuration: Pydantic settings, environment modules, Django settings packages, `.env` loaders
- Architecture: routers or services or repositories, management commands, background jobs, task queues, notebooks versus production code

### Java Search Priorities

Inspect these first when Java is present:

- `pom.xml`, `build.gradle`, `build.gradle.kts`, `settings.gradle`, `gradle.properties`, Maven wrapper or Gradle wrapper files
- `src/main/java`, `src/test/java`, `src/main/resources`, `src/test/resources`
- `application.properties`, `application.yml`, profile-specific config files, Logback or Log4j configs
- Spring Boot startup classes, Micronaut or Quarkus bootstrap files, servlet config, persistence config
- Migration and persistence config such as Flyway, Liquibase, JPA, MyBatis

Look for these patterns explicitly:

- Logging: SLF4J, Logback, Log4j2, custom logger abstractions
- Dependency injection: Spring `@Configuration`, `@Bean`, component scanning, Guice, CDI
- Configuration: profiles, environment-specific property files, config servers, secrets patterns
- Architecture: controller-service-repository layering, hexagonal ports and adapters, message listeners, scheduled jobs

### Mixed Repositories

If the repository mixes stacks:

- Document each major runtime or package separately.
- Identify the handoff points between stacks such as API contracts, generated clients, shared schemas, or deployment scripts.
- Do not collapse distinct workflows into one vague command list.

## Pattern Recognition Checklist

The instruction file should describe important project patterns that an agent would otherwise need to rediscover. Only document patterns supported by evidence.

Use [references/common-conventions.md](references/common-conventions.md) when you need examples of what "common" usually looks like for commits, workflows, logging, dependency injection, configuration, technology inventories, or unusual project traits. Use the reference only as comparison material.

### Git and Commit Patterns

Inspect recent history when available, for example the last 20 to 50 non-merge commits plus any PR template or contribution docs.

Look for:

- Conventional Commits such as `feat(scope): ...`, `fix: ...`, `chore: ...`
- Ticket-prefixed commits such as `ABC-123: ...` or `[ABC-123] ...`
- Scope naming conventions tied to packages, apps, or services
- Branch naming conventions such as `feature/*`, `bugfix/*`, `hotfix/*`, `release/*`
- Squash-merge versus merge-commit patterns
- Release tagging conventions and version bump patterns

Document only the patterns that appear consistently enough to be useful.

### Workflow and Automation Patterns

Inspect CI and repository automation to identify:

- Required quality gates such as lint, test, typecheck, build, audit, or package-specific checks
- Matrix builds by runtime version, OS, or package
- Release automation, publish steps, migrations, or deploy approvals
- Generated artifacts, cache dependencies, or pre-commit hooks
- Whether local workflows are expected to mirror CI exactly

If the workflow is split by package or service, say that explicitly and show how to run checks selectively.

### Development Guidelines To Detect

Actively search for these and record them when present:

- Logging framework and expected logger usage
- Dependency injection framework or composition root
- Configuration file locations and override order
- Secret handling patterns and `.env` conventions
- Test placement, naming, fixture, and mocking patterns
- Database migration commands and schema ownership
- API contract locations such as OpenAPI specs, protobufs, JSON schemas, generated clients
- Error handling patterns, retry policies, and validation libraries
- Background job and scheduler patterns
- Feature flags, permissions, tenant handling, or environment switches
- Code generation outputs or files that should not be edited manually
- Frontend routing, state management, design-system, and asset-pipeline conventions
- Important technology usage that is easy to miss, especially file, document, media, storage, parsing, or integration libraries

### Architecture and Directory Patterns

Document boundaries that influence safe edits, for example:

- Layered structure such as `api -> application -> domain -> infrastructure`
- Feature-based modules or package boundaries
- Shared libraries versus app-specific code
- Generated directories, vendored code, migration snapshots, build outputs
- Config, scripts, tooling, and infrastructure folders an agent should know about

### Project Peculiarities

End the repository analysis with a deliberate search for unusual traits.

- Compare observed repository patterns against common conventions for the detected stack.
- Document the differences that would surprise an experienced engineer joining that ecosystem.
- Prefer concrete peculiarities over vague statements such as `custom setup`.
- Explain the evidence and practical impact of each peculiarity.

Useful peculiarity categories include:

- unusual directory or module boundaries
- custom bootstrap or composition-root logic
- nonstandard environment or configuration loading
- legacy frameworks or mixed runtime models in one repository
- custom wrappers around logging, HTTP, storage, or file processing
- generated code committed alongside hand-written source
- testing or CI patterns that differ from common tool defaults
- bilingual or domain-specific terminology conventions

## Required Content Areas

Include the sections that are relevant to the project. Typical sections include:

- `Project Overview`
- `Primary Technologies`
- `Repository Structure`
- `Setup and Environment`
- `Development Commands`
- `Testing and Quality Gates`
- `Code Style and Conventions`
- `Architecture and Important Boundaries`
- `Logging, Observability, and Diagnostics`
- `Dependency Injection and Service Wiring`
- `Configuration and Secrets`
- `Data, Migrations, and Integrations`
- `Git, PR, and Release Conventions`
- `Project Peculiarities`
- `Monorepo Navigation`
- `Troubleshooting and Gotchas`

The best instruction files are selective. Do not force every section into every project.

## Output Template

Use this as a starting point and adapt it to the repository:

```markdown
# {{TARGET_FILENAME}}

## Project Overview

[What the project does, major runtimes, and why the repository exists]

## Primary Technologies

| Category | Technology | Evidence | Purpose |
| --- | --- | --- | --- |
| Runtime | [technology] | [manifest or code path] | [why it matters] |
| Framework | [technology] | [manifest or code path] | [why it matters] |
| Database | [technology] | [config, migration, or code path] | [why it matters] |
| File Processing | [technology] | [manifest or code path] | [why it matters] |

## Repository Structure

- [Key directory or package]: [Purpose]
- [Key directory or package]: [Purpose]

## Setup and Environment

- Install dependencies: `[exact command]`
- Start local environment: `[exact command]`
- Required environment files: `[paths or filenames]`
- Important configuration roots: `[paths]`

## Development Commands

- Run app: `[exact command]`
- Build: `[exact command]`
- Lint or format: `[exact command]`
- Run focused package or service commands: `[exact command]`

## Testing and Quality Gates

- Run all tests: `[exact command]`
- Run targeted tests: `[exact command]`
- CI-required checks: `[exact commands]`
- Test locations or patterns: `[paths or naming conventions]`

## Code Style and Conventions

- [Naming, file organization, import or module rules]
- [Framework or architecture conventions]
- [Files or directories to avoid editing directly]
- [Short example of a common convention when it helps]

## Logging, DI, and Configuration

- Logging: [framework, wrappers, where configured]
- DI or service wiring: [composition root or module wiring]
- Config or secrets: [file locations, env var patterns, override order]

## Git and Workflow Conventions

- Commit style: [observed pattern]
- Branch or PR expectations: [observed pattern]
- Required checks before merge: `[commands]`
- Example when useful: `[common or observed example pattern]`

## Project Peculiarities

- [Concrete deviation from common conventions]
- [Why it matters for safe edits or correct operation]

## Additional Notes

- [Repository-specific gotchas]
- [Debugging tips]
- [Deployment or release notes if relevant]
```

## Terminal Assumptions Output

After creating or updating the instruction file, return a separate `Assumptions` section in the chat or terminal response only.

- Do not include this section inside the generated instruction file.
- Use the same language as the chat response unless the user asks otherwise.
- Order items from lowest certainty to highest certainty.
- Include only material assumptions that affected the analysis or the generated content.
- Good sources of assumptions include:
  - missing filename, scope, or language information that the user did not provide
  - missing or unreadable files
  - runtime behavior inferred from static evidence
  - dependency usage that appears likely but could not be confirmed
  - conventions inferred from partial Git or CI history
  - commands or workflows that could not be executed or verified

Use this compact format when assumptions exist:

- `[certainty: low] [assumption] | [why it was needed] | [basis or limitation]`
- `[certainty: medium] [assumption] | [why it was needed] | [basis or limitation]`
- `[certainty: high] [assumption] | [why it was needed] | [basis or limitation]`

If there are no material assumptions, output:

`Assumptions: none`

## Evidence Rules

- Prefer observed project evidence over generic best practices.
- Cite exact filenames, directories, scripts, package names, workflow names, and config keys when useful.
- Do not invent commands, branch policies, commit rules, or technology usage.
- Tie important technologies to manifest evidence, code usage, configuration, or automation.
- If a convention is inferred rather than explicit, say so in the instruction file.
- If you call something a peculiarity, make the comparison basis clear.
- If the repository lacks enough evidence for a section, omit it or add a short uncertainty note instead of fabricating content.
- Do not silently hide important uncertainty. Put material assumptions in the terminal assumptions output.

## Monorepo Rules

For monorepos:

- Create a top-level instruction file for shared rules and navigation.
- Add subproject instruction files only when the subprojects have distinct workflows or conventions.
- Use the same target filename in nested scopes unless the user asks otherwise.
- Explain how to run package-specific commands without implying that every command works from every directory.

## Final Notes

- The instruction file should reduce the amount of repo spelunking an agent has to do before making safe changes.
- Prioritize commands, boundaries, conventions, technologies, and pitfalls over marketing or product background.
- Treat the instruction file as living documentation. Improve it when the project evolves.
