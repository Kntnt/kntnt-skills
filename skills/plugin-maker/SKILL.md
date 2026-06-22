---
name: plugin-maker
description: Scaffold a whole Claude Code / Cowork plugin to the Kntnt standard — interview the user, generate the standard shell from templates, author each skill via skill-maker, wire up help/audit/README/CHANGELOG, then run agents-md and stop before anything outward-facing. Handles greenfield (empty folder) and augment (add a skill to an existing plugin). User-invoked — /plugin-maker or /kntnt-skills:plugin-maker, optionally with a plan. Not triggered by a bare "make a plugin".
disable-model-invocation: true
---

# plugin-maker

Turn a plan — anything from a bare plugin name to a detailed specification — into a complete, on-standard Claude Code / Cowork plugin. The skill interviews you to settle the plugin's design, generates the standard file shell from templates with your identity filled in, authors each skill through `skill-maker`, wires up the help command, audit, README and changelog, then runs `agents-md` and hands off a local, audit-green, git-initialised repository — stopping before anything outward-facing. It works greenfield in an empty folder and in augment mode to add a skill to an existing plugin.

## Read first, every run

The standard is the source of truth — read it before doing anything. Subagents do not auto-load these; paste their content into any subagent prompt.

1. `${CLAUDE_PLUGIN_ROOT}/lib/plugin-standard.md` — the canonical plugin shape, the mandatory/conditional split, identity tokens, the audit tiers, versioning, the modes and the finish sequence.
2. `${CLAUDE_PLUGIN_ROOT}/lib/skill-conventions.md` and the vendored Matt Pocock files it points to — for the skills.
3. `${CLAUDE_PLUGIN_ROOT}/lib/protocols/interview.md` — how to interview.

## Mode detection

Look for `.claude-plugin/plugin.json` in the target directory:

- **absent / empty dir → greenfield** (full scaffold).
- **present → augment** (add a skill, rewire the plugin).

## Templates

The boilerplate lives in `${CLAUDE_PLUGIN_ROOT}/lib/templates/`. Copy each, substitute the `{{TOKEN}}`s (table in `plugin-standard.md`), and write it to its target path:

| Template | Target | Notes |
| --- | --- | --- |
| `plugin.json` | `.claude-plugin/plugin.json` | tokens; `version` `0.1.0` |
| `marketplace.json` | `.claude-plugin/marketplace.json` | tokens |
| `gitignore` | `.gitignore` | verbatim |
| `pre-commit-config.yaml` | `.pre-commit-config.yaml` | add a `tests` hook only when `tests/` exists |
| `settings.json` | `.claude/settings.json` | verbatim |
| `audit.yml` | `.github/workflows/audit.yml` | add a tests step only when `tests/` exists |
| `bug.md` | `.github/ISSUE_TEMPLATE/bug.md` | verbatim |
| `help-command.md` | `commands/help.md` | tokens |
| `help.py` | `scripts/help.py` | verbatim but for the docstring token |
| `audit.py` | `scripts/audit.py` | tier-1 generic; add tier-2 structural checks per the plugin |
| `LICENSE` | `LICENSE` | verbatim (Apache-2.0) |
| `NOTICE` | `NOTICE` | tokens; append third-party attribution when the plugin vendors anything |
| `CONTRIBUTING.md` | `CONTRIBUTING.md` | tokens |
| `CHANGELOG.md` | `CHANGELOG.md` | tokens; initial `0.1.0` entry |
| `README.md` | `README.md` | tokens; fill `{{SKILLS_OVERVIEW}}` and `{{SKILLS_USAGE}}` from the authored skills |

## Greenfield process

1. **Read** the references above.
2. **Resolve identity tokens** by the detection order in `plugin-standard.md` (`git config`, `gh`, sibling `kntnt-*` repos, the directory name). Hold them for confirmation in the interview — do not assume silently.
3. **Interview** per `interview.md` with the plugin-level question domain: name and **charter** (the theme, the one-line description, what is deliberately out of scope); the identity tokens; **which skills** it ships (name + one-liner each); whether the skills share **`lib/` modules**; whether `docs/` (human documentation) is warranted — the rare case. Adapt to the plan's richness; stop when the design is settled, and confirm it in one consolidated view.
4. **Scaffold the shell** — write every mandatory-core file from the templates with tokens substituted. Add conditional parts only when the interview warranted them (`lib/`, `docs/`, `tests/`, extra `scripts/`); never empty scaffolding.
5. **Author each skill** by running the `skill-maker` process (its steps 2–4) for each, with the target set to `skills/<name>/` here. Keep the interview continuous — it is the same protocol throughout.
6. **Wire the plugin together** — fill the README's `{{SKILLS_OVERVIEW}}` (one bullet per skill) and `{{SKILLS_USAGE}}` (a subsection per skill), the `plugin.json` keywords, and any tier-2 structural `audit` checks the structure now warrants (an index ↔ files symmetry). `help` needs no wiring — it reads the skills live.
7. **Finish** per `plugin-standard.md`: run `audit.py` (and `tests/`, if any) green; run `agents-md` on the plugin; `git init` + an initial commit; then stop and report the next steps (review the diff, `gh repo create`, `/release`). Do nothing outward-facing.

## Augment process

When a manifest is present:

1. **Read** the references and the existing plugin (its skills, `lib/`, README, `CHANGELOG`).
2. **Interview** only the new skill (the `skill-maker` domain).
3. **Author** it via the `skill-maker` process into `skills/<name>/`.
4. **Rewire** the plugin level: a new `CHANGELOG` entry under `## [Unreleased]`; the skill added to the README skill list and usage, and to the `marketplace.json` description if it enumerates skills; any new tier-2 `audit` check; a version bump per SemVer. `help` needs no edit.
5. **Finish**: audit green; re-run `agents-md`; commit; report. Stop before outward-facing steps.

## Invocation

- `/plugin-maker` — interview from scratch in the current directory.
- `/plugin-maker <plan>` — seed with a name or a fuller plan; the richer the plan, the fewer questions.

The boundary is firm: `plugin-maker` produces a complete, local, audit-green, git-initialised plugin and **stops**. It never creates the GitHub repository, pushes, or releases — those are `gh` and the `/release` workflow, run by you after you have reviewed the result.
