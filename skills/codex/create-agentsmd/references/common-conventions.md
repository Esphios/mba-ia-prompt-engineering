# Common Conventions Reference

Use this file only as comparison material while generating repository instruction files.

- These examples are not repository facts.
- Do not copy examples into the final output unless repository evidence supports them.
- Translate examples into English or Brazilian Portuguese as needed, but keep literal commands and identifiers unchanged.

## What This Reference Is For

Use this reference when you need:

- a quick reminder of what a common convention usually looks like
- example wording for a convention section
- examples of project peculiarities that differ from stack defaults
- examples of technology categories worth capturing in `Primary Technologies`

## Common Git and Commit Conventions

Examples:

- Conventional Commits: `feat(api): add health endpoint`
- Ticket-prefixed commits: `ABC-123 fix invoice parser`
- Scoped fixes: `fix(feed): handle empty episode list`
- Branch names: `feature/abc-123-add-health-endpoint`, `bugfix/feed-empty-state`, `release/1.4.0`

Useful comparison questions:

- Are commit subjects imperative and short?
- Are scopes tied to packages, services, or domains?
- Are ticket IDs mandatory, optional, or absent?
- Are merges usually squashed, rebased, or preserved?

## Common Workflow and CI Conventions

Examples:

- Run `lint`, `test`, and `build` before merge.
- Run selective checks for one package in a monorepo instead of the whole workspace.
- Require migrations when schema-affecting changes are introduced.
- Gate releases on version bumps, changelog generation, package publish, or deployment approvals.

Useful comparison questions:

- Does local developer workflow mirror CI exactly?
- Are checks global or package-specific?
- Are there environment-specific jobs, release branches, or deployment approval steps?

## Common Logging Conventions

Examples:

- .NET: `ILogger<T>` injected into services and controllers
- Node.js: centralized logger module such as `pino` or `winston`
- Python: module-level `logging.getLogger(__name__)`
- Java: `LoggerFactory.getLogger(...)` through SLF4J

Useful comparison questions:

- Is logging standardized or wrapped by custom helpers?
- Are correlation IDs, structured fields, or audit logs part of the pattern?
- Is logging configured centrally or scattered through features?

## Common Dependency Injection Conventions

Examples:

- .NET: `Program.cs` or `Startup.cs` registers services in `builder.Services`
- NestJS: modules and providers define dependency wiring
- Python FastAPI: dependencies provided through `Depends(...)`
- Spring: `@Configuration`, `@Bean`, component scanning

Useful comparison questions:

- Is there a clear composition root?
- Is the project using a framework-standard container or a custom service locator?
- Are dependencies injected consistently or mixed with static helpers and manual construction?

## Common Configuration Conventions

Examples:

- .NET: `appsettings.json` plus `appsettings.{Environment}.json`
- Node.js: `.env`, `.env.local`, and a typed config wrapper
- Python: Pydantic settings, Django settings modules, or `.env` loaders
- Java: `application.yml` plus environment profiles

Useful comparison questions:

- Where are config defaults defined?
- What overrides them in local, test, and production environments?
- Are secrets file-based, environment-based, or pulled from an external provider?

## Common Architecture Conventions

Examples:

- `controller -> service -> repository`
- `route -> handler -> use case -> adapter`
- feature folders grouped by domain
- monorepo packages split into `apps/`, `packages/`, `libs/`, or `services/`

Useful comparison questions:

- Is the repository layered, feature-based, or mixed?
- Where are boundaries enforced and where are they blurred?
- Which directories are generated, vendored, or not meant for manual edits?

## Primary Technologies Inventory Examples

Typical categories:

- Language or runtime
- Framework
- Package manager or workspace tooling
- Database
- ORM or migration tool
- Messaging, cache, or search
- Authentication or validation
- Logging or observability
- File, document, media, or data-format processing
- Testing, linting, formatting, or type checking
- Build, container, deployment, or infrastructure tooling

Example entries:

- `Database | PostgreSQL | docker-compose.yml, migration files | primary application database`
- `File Processing | CsvHelper | package manifest plus parser service | CSV import and export`
- `File Processing | Sharp | package.json plus image service | image resize and optimization`
- `Document Processing | iText | csproj plus PDF generator service | PDF generation`

Useful comparison questions:

- Which technologies shape implementation decisions?
- Which direct dependencies are specialized enough that an agent should know about them?
- Which technologies are installed but not visibly used?

## Peculiarity Examples

These are examples of traits worth calling out when they differ from common expectations:

- tests live in `specs/` instead of `tests/`
- configuration is loaded from XML or a database rather than standard environment files
- a legacy service locator is mixed into an otherwise DI-based application
- generated code is committed inside normal source folders
- frontend assets are built by a backend project
- migrations live in a separate package or repository
- commit scopes follow Jira components instead of package names
- docs are in Brazilian Portuguese while code and identifiers are in English
- the real startup path goes through custom scripts instead of the framework default entry point

When documenting a peculiarity, explain:

- what the common expectation would be
- what this repository does instead
- why that difference matters for safe changes
