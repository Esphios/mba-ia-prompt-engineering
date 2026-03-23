---
name: port-codex-skill
description: Convert a Codex skill folder into a Gemini-compatible skill folder by preserving shared SKILL.md content, translating Codex-specific metadata when possible, and removing unsupported Codex-only files.
---

# Purpose

Use this skill when the user wants to convert a Codex skill into a Gemini skill.

Codex and Gemini both use the open Agent Skills pattern centered on `SKILL.md`, so most conversions are structural rather than conceptual. The main work is to:

1. Read the source Codex skill folder.
2. Preserve the shared skill name, description, instructions, and support files.
3. Ignore or summarize Codex-only configuration such as `agents/openai.yaml`.
4. Write the converted skill into a Gemini-compatible target folder.
5. Report any lossy conversions clearly.

# What to Inspect

A Codex skill typically contains:

- `SKILL.md` as the required manifest and instruction file
- optional helper files such as `.py`, `.sh`, `.json`, images, docs
- optional `agents/openai.yaml`, which is Codex-specific

# Output Target

Prefer writing to one of these target directories:

- repo-local: `.gemini/skills/<skill-name>/`
- user-level: `~/.gemini/skills/<skill-name>/`

Keep the same skill directory name unless the user explicitly requests a rename.

# Conversion Rules

## Preserve as-is

Preserve these from the Codex skill when present:

- YAML frontmatter `name`
- YAML frontmatter `description`
- the Markdown instruction body
- helper scripts and support assets
- relative references that still make sense inside the copied skill folder

## Codex-specific handling

If `agents/openai.yaml` exists:

- do not copy it into the Gemini skill unless the user explicitly asks to keep it as a reference note
- inspect it for useful information
- if it contains `policy.allow_implicit_invocation`, mention that this was Codex-only metadata and was not carried over as native Gemini metadata
- if it contains interface display fields, prefer the `SKILL.md` frontmatter as the source of truth for Gemini

## Placeholder handling

Do not rewrite placeholders unless the source skill clearly depends on an agent-specific placeholder syntax that Gemini will not understand.

For Codex-origin skills using normal Agent Skills content in `SKILL.md`, preserve the body unless there is a concrete incompatibility.

## Support files

Copy support files alongside the converted skill unless they are clearly Codex-only control files.

Examples to preserve:

- `.py`
- `.sh`
- `.json`
- `.yaml`
- `.txt`
- `.md`
- `.png`
- `.jpg`
- `.pdf`

Examples to exclude by default:

- `agents/openai.yaml`
- other files that are purely Codex runtime metadata with no execution or documentation value

# Required Workflow

When invoked, follow this exact process:

1. Identify the source Codex skill directory.
2. Read `SKILL.md`.
3. Check whether `agents/openai.yaml` exists.
4. Inventory helper/support files.
5. Create the Gemini target directory.
6. Write the converted `SKILL.md`.
7. Copy supported helper/support files.
8. Exclude Codex-only config files.
9. Summarize:
   - source path
   - target path
   - files copied
   - files excluded
   - any lossy or uncertain parts

# Validation Checklist

Before finishing, verify:

- target `SKILL.md` exists
- target frontmatter contains `name` and `description`
- referenced helper files still exist at the same relative paths
- no Codex-only config is being treated as Gemini-native behavior
- any assumptions are called out explicitly

# Execution Preference

If Python is available, use the bundled helper script `convert_codex_skill.py`.

Preferred command pattern:

```bash
python3 convert_codex_skill.py --source "<codex-skill-dir>" --target "<gemini-skill-dir>"
```

If Python is not available, perform the conversion manually using the same rules.
