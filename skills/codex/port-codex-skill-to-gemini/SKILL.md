---
name: port-codex-skill-to-gemini
description: Convert a Codex skill folder into a Gemini-compatible skill folder and produce a clear conversion report that preserves shared SKILL.md content, calls out metadata loss, and explains what was copied, excluded, or adapted. Use when Codex needs a report-oriented Codex-to-Gemini conversion for Gemini CLI or Gemini skill directories.
---

# Purpose

Use this skill when the user wants Codex to convert a Codex skill into a Gemini skill.

This skill is Codex-native. It runs from Codex, inspects a source Codex skill folder, copies the shared Agent Skills content into a Gemini-compatible destination, excludes Codex-only runtime metadata, and then performs a final optimization pass on the generated Gemini `SKILL.md`.

# When To Prefer This Skill

Prefer this skill over `$port-codex-skill` when the user wants:

- a clearer conversion report
- stronger callouts about lossy or uncertain metadata mapping
- a Gemini-targeted destination and an explicit audit of what changed

# What to Inspect

A source Codex skill typically contains:

- `SKILL.md` as the required manifest and instruction file
- optional helper files such as `.py`, `.sh`, `.json`, images, docs, `references/`, or `assets/`
- optional `agents/openai.yaml`, which is Codex-specific

If available, use these references to align the conversion:

- the source Codex skill folder itself
- other current Codex skills for folder conventions
- an existing Gemini porter skill such as `skills/gemini/port-codex-skill/`

If those repo-local references are not present, rely on the source skill and standard Agent Skills conventions.

# Output Target

Prefer writing to one of these target directories:

- repo-local: `skills/gemini/<skill-name>/`
- Gemini CLI local: `.gemini/skills/<skill-name>/`
- user-level: `~/.gemini/skills/<skill-name>/`

Keep the same skill directory name unless the user explicitly requests a rename.

# Conversion Rules

## Preserve as-is

Preserve these from the Codex skill when present:

- YAML frontmatter `name`
- YAML frontmatter `description`
- the Markdown instruction body unless a Gemini-specific incompatibility exists
- helper scripts and support assets
- relative references that still make sense inside the copied skill folder

## Codex-specific handling

If `agents/openai.yaml` exists:

- do not copy it into the Gemini skill unless the user explicitly asks to keep it as a reference note
- inspect it for useful information before excluding it
- import useful `interface` metadata into the generated Gemini `SKILL.md` as a plain Markdown reference section instead of Gemini-native config
- if it contains `policy.allow_implicit_invocation`, mention that this was Codex-only metadata and was not carried over as Gemini-native metadata
- if it contains interface display fields, treat `SKILL.md` frontmatter as the Gemini source of truth

## Placeholder handling

Do not rewrite placeholders unless the source skill clearly depends on Codex-only placeholder syntax that Gemini will not understand.

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

1. Identify the source Codex skill directory and the Gemini target directory.
2. Read `SKILL.md`.
3. Check whether `agents/openai.yaml` exists.
4. Inventory helper and support files.
5. Create the Gemini target directory.
6. Run `scripts/convert_codex_skill_to_gemini.py` when Python is available.
7. Confirm whether source `agents/openai.yaml` contains recoverable interface metadata.
8. Preserve that metadata by importing it into a dedicated `Imported Metadata` section inside the generated Gemini `SKILL.md`.
9. Inspect the generated Gemini `SKILL.md`.
10. Run a final optimization pass using `$enrich-prompt` on the generated Gemini `SKILL.md` instructions.
11. Apply only justified improvements from that optimization pass.
12. Summarize:
   - source path
   - target path
   - files copied
   - files excluded
   - metadata imported
   - any lossy or uncertain parts

# Final Optimization Pass

Use `$enrich-prompt` again after the structural conversion to tighten the Gemini `SKILL.md`.

Constrain that pass as follows:

- preserve the `name`
- preserve the `description` unless it still contains a concrete Codex-only reference that should become Gemini or agent-neutral wording
- preserve the imported metadata section as a plain reference block if one was created
- preserve the core workflow and support-file references
- do not add unsupported Gemini metadata
- prefer light-touch improvements over stylistic rewrites
- keep the converted skill operationally equivalent to the source skill

Use the enrichment pass to improve clarity, trigger accuracy, and execution readiness, not to invent new capabilities.

# Validation Checklist

Before finishing, verify:

- target `SKILL.md` exists
- target frontmatter contains `name` and `description`
- referenced helper files still exist at the same relative paths
- recoverable source `interface` metadata was imported into the body when present
- no Codex-only config is being treated as Gemini-native behavior
- the final optimization pass preserved the source skill's intent
- any assumptions are called out explicitly

# Execution Preference

If Python is available, use the bundled helper script:

```bash
python scripts/convert_codex_skill_to_gemini.py --source "<codex-skill-dir>" --target "<gemini-skill-dir>"
```

If Python is not available, perform the conversion manually using the same rules.
