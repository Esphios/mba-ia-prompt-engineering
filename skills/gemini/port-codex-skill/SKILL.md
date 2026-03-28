---
name: port-codex-skill
description: Convert a Codex skill folder into a Gemini-compatible skill folder with a light-touch, folder-level port that preserves shared SKILL.md content, keeps useful support files, and removes unsupported Codex-only metadata. Use when Gemini needs a straightforward Codex-to-Gemini conversion without an extended conversion report.
---

# Port Codex Skill

Use this skill when the user wants to convert a Codex skill into a Gemini-compatible skill folder.

The goal is not just to copy files. The result should preserve the original skill's intent, exclude Codex-only runtime metadata, and leave the generated Gemini `SKILL.md` cleaner and more execution-ready than the source.

## Imported Metadata

Preserve the following source metadata as reference only. Gemini does not consume it as native config.

- `Display name`: `Port Codex Skill`
- `Short description`: `Lightweight Codex-to-Gemini port`
- `Suggested prompt`: `Use $port-codex-skill to convert this Codex skill into a Gemini skill and report any lossy conversions.`

## When To Prefer This Skill

Prefer this skill for the lightweight or default conversion path.
If the user specifically wants a more explicit conversion report or stronger callouts about lossy metadata handling, prefer `$port-codex-skill-to-gemini`.

## Inputs

- Source Codex skill directory.
- Optional target Gemini directory.
- Source `SKILL.md`.
- Optional `agents/openai.yaml`.
- Optional helper files such as scripts, docs, references, assets, and tests.

## Output Target

Prefer writing to one of these target directories:

- repo-local: `skills/gemini/<skill-name>/`
- Gemini CLI local: `.gemini/skills/<skill-name>/`
- user-level: `~/.gemini/skills/<skill-name>/`

Keep the same skill directory name unless the user explicitly requests a rename.

## Conversion Rules

### Preserve

Preserve these from the Codex skill when present:

- YAML frontmatter `name`
- YAML frontmatter `description`
- the instruction body unless there is a concrete Gemini incompatibility
- helper scripts and support assets
- relative references that still make sense inside the copied skill folder

### Exclude by default

Exclude Codex-only runtime metadata unless the user explicitly asks to keep it as reference material:

- `agents/openai.yaml`
- other files that are purely Codex runtime metadata with no documentation or execution value

### Metadata handling

If `agents/openai.yaml` exists:

- inspect it before excluding it
- preserve only useful information that would otherwise be lost
- prefer the `SKILL.md` frontmatter as the Gemini source of truth
- mention omitted metadata in the final summary when it affected the conversion

### Support files

Copy support files alongside the converted skill when they contribute to execution, documentation, or validation.

Typical files to preserve:

- `.py`
- `.sh`
- `.json`
- `.yaml`
- `.txt`
- `.md`
- `.png`
- `.jpg`
- `.pdf`
- `references/`
- `assets/`
- `scripts/`

### Placeholder handling

Do not rewrite placeholders unless the source skill clearly depends on agent-specific syntax that Gemini will not understand.

## Required Workflow

1. Resolve the source Codex skill directory and the target Gemini directory.
2. Read `SKILL.md`.
3. Check whether `agents/openai.yaml` exists.
4. Inventory helper and support files.
5. Create the target directory.
6. Run the bundled helper script `convert_codex_skill.py` when Python is available and the script is present.
7. Manually finish the conversion as needed:
   - preserve the original capability and workflow
   - keep relative references valid
   - exclude Codex-only runtime metadata
8. Run a light-touch prompt optimization pass on the generated Gemini `SKILL.md`:
   - sanitize the instructions first
   - enrich only where it improves trigger clarity, workflow clarity, output contract, or guardrails
   - do not invent new capabilities
9. Validate the converted skill.
10. Summarize:
   - source path
   - target path
   - files copied
   - files excluded
   - metadata intentionally omitted or summarized
   - any lossy or uncertain parts

## Validation Checklist

Before finishing, verify:

- target `SKILL.md` exists
- target frontmatter contains `name` and `description`
- referenced helper files still exist at the same relative paths
- no Codex-only config is being treated as Gemini-native behavior
- the generated `SKILL.md` still matches the source skill's intent
- any assumptions are called out explicitly

## Execution Preference

If Python is available, use the bundled helper script:

```bash
python convert_codex_skill.py --source "<codex-skill-dir>" --target "<gemini-skill-dir>"
```

If Python is not available, perform the conversion manually using the same rules.
