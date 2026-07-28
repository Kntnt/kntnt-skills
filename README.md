# kntnt-skills

[![License](https://img.shields.io/github/license/Kntnt/kntnt-skills)](LICENSE)
[![Latest release](https://img.shields.io/github/v/release/Kntnt/kntnt-skills)](https://github.com/Kntnt/kntnt-skills/releases/latest)
[![Audit](https://github.com/Kntnt/kntnt-skills/actions/workflows/audit.yml/badge.svg)](https://github.com/Kntnt/kntnt-skills/actions/workflows/audit.yml)

kntnt-skills is a Claude Code plugin that collects Kntnt's general-purpose skills – the ones that are useful on their own but do not belong to any of the themed Kntnt plugins.

## Description

Kntnt maintains several skill plugins for Claude Code. Most are built around a single theme – writing, code, pillar pages – and each lives in its own repository. A few skills fit none of those themes yet still earn a place in the toolbox. This plugin is where they live.

Without a home of this kind, a standalone skill has two poor options: a repository of its own, which is heavy for a single skill, or burial inside a themed plugin it does not really belong to. kntnt-skills avoids both. It gives small, self-contained skills one installable home, and points you to the specialised plugins whenever one of them suits the job better.

### Available skills

- **`/agents-md`** – minimise the tokens an agent must load from `CLAUDE.md` / `AGENTS.md`. It keeps only what every session truly needs, compresses it hard, splits the rest into small on-demand `agents.d/` files, and creates nothing (or deletes existing files) when there is nothing load-bearing to keep.
- **`/caveman`** – apply caveman compression (maximum meaning per token, with no loss of facts, code, numbers or register) to everything the agent says, or one-shot to a single text or file. Turn it on with `/caveman` or `/caveman --on` and off with `/caveman --off`; compress one text or file with `/caveman <ref>` or `/caveman --file=<path>` without changing that on/off state. It shares its definition of "caveman" with `/agents-md` through `lib/caveman.md`.
- **`/delegation`** – turn delegation mode on or off: while it is on, the agent orchestrates — thinks, plans, briefs, verifies — and subagents execute on the lowest model judged able to do the job (haiku, sonnet, opus or fable — never one stronger than the delegating agent itself), except when doing the job itself is cheaper. `/delegation` toggles the mode for the current session; `--user` and `--project` make it standing by writing the instruction as a managed block into the context file your agent already loads, and `--status` reports all three scopes. The mode governs only choices you leave open — an explicit "do this yourself" or "spawn a subagent" always wins.
- **`/skill-maker`** – author one complete skill to the Kntnt standard. It interviews you one question at a time, applies Matt Pocock's skill-writing craft and Kntnt's house conventions, and writes the `SKILL.md` (and any shared `lib/` it needs). Use it standalone to add a skill, or let `/plugin-maker` drive it for each skill of a new plugin.
- **`/plugin-maker`** – scaffold a whole Claude Code / Cowork plugin to the Kntnt standard. It interviews the design, lays the common project base by invoking `kntnt-code-skills:init` (git, the `agents-md` skeleton, the coding standard, a licence, the generic README/CHANGELOG/CONTRIBUTING/NOTICE and `.gitignore`), layers the plugin-specific files on top, authors each skill via `skill-maker`, wires up help, audit and README, re-runs `/agents-md`, and may make the initial commit and create the GitHub repo — stopping before `/release`. Works greenfield (an empty folder) or in augment mode (add a skill to an existing plugin).
- **`/help`** – a typed-only command (`/kntnt-skills:help [skill-name]`): a manpage-style overview of the plugin's skills, or one skill's details. Its output is rendered from the plugin's own `.claude-plugin/plugin.json` and `skills/<name>/SKILL.md` by `scripts/help.py`, so it never drifts from the actual skills.

### The Kntnt skill family

When your task is specifically about writing, code or pillar pages, one of the dedicated plugins will serve you better. Each is maintained in its own repository:

- [kntnt-text-skills](https://github.com/Kntnt/kntnt-text-skills) – writing, editing, proofreading and reviewing text against Kntnt's house style, in Swedish, British English and American English.
- [kntnt-code-skills](https://github.com/Kntnt/kntnt-code-skills) – coding standards across languages and frameworks, release and push workflows, and multi-agent orchestration that turns issues into implemented code.
- [kntnt-pillar-page-skills](https://github.com/Kntnt/kntnt-pillar-page-skills) – writing, structuring, reviewing and previewing pillar pages, built on top of kntnt-text-skills.

Reach for kntnt-skills for the useful things that fall outside those three.

## Requirements

kntnt-skills runs in Claude Code or Claude Cowork. It needs support for slash commands, YAML frontmatter (including `disable-model-invocation`) and skills. The skills require no external services or dependencies: Matt Pocock's skill-writing and grilling references that `skill-maker` and `plugin-maker` build on are vendored into the plugin under `lib/vendor/matt-pocock/`, so nothing extra need be installed. The `/help` command and the audit (`scripts/audit.py`) render and run through [uv](https://docs.astral.sh/uv/), which executes standard-library-only PEP 723 scripts and provisions Python 3.12+ from each script's own metadata; uv is needed only for `/help` and the audit.

## Installation

Register the marketplace and install from within Claude Code or Cowork:

```
/plugin marketplace add Kntnt/kntnt-skills
/plugin install kntnt-skills@kntnt-skills
```

Alternatively, clone the repository directly into your plugin directory:

```bash
git clone git@github.com:Kntnt/kntnt-skills.git ~/.claude/plugins/kntnt-skills
```

## Usage

Each skill is invoked by its slash command.

### `/agents-md`

Run `/agents-md` in a repository to shrink its root `CLAUDE.md` / `AGENTS.md` to the fewest tokens that still carry what every session needs; everything situational moves to small on-demand `agents.d/` files. Target something else with `/agents-md <path>` (a specific directory or file) or `/agents-md --global` (your global `~/.claude/CLAUDE.md`).

Flags:

- `--max-iterations=N` – depth of the build-and-review loop that compresses the files (default 2; above 3 it asks first).
- `--no-claude-md` – write only `AGENTS.md`, with no `CLAUDE.md` bridge (for tools that read `AGENTS.md` directly).
- `--only-claude-md` – write a single `CLAUDE.md` holding the content directly, with no `AGENTS.md`.

The skill is subtractive and compressive: it deletes, compresses and splits far more than it adds, and reports the before/after token counts so you can see the saving.

### `/caveman`

Turn caveman compression on for all of the agent's output with `/caveman` (or `/caveman --on`), and off again with `/caveman --off`. While on, the agent answers in maximum-meaning-per-token style without dropping facts, code, numbers, or the register of anything you ask it to write. It stays on for the rest of the session; if a very long conversation drifts back to verbose, run `/caveman` again.

Compress a single piece of text without touching that on/off state: `/caveman <ref>`, where `<ref>` is a filename, path, URL, a description of a file ("the file you just created") or a reference to text you paste below; or name a file explicitly with `/caveman --file=<path>`. The result is shown with its before/after size, never written over the source unless you ask.

Both skills draw their rules from `lib/caveman.md`, so `/caveman` and `/agents-md` compress the same way.

### `/delegation`

Run `/delegation` to toggle delegation mode for the current session, `/delegation --on` / `--off` to force a state, and `/delegation --status` to see where the mode stands. While on, the agent works as an orchestrator: it does the thinking — understanding, diagnosing, deciding, briefing, verifying — and delegates execution to subagents on the lowest model judged able to do the job — along the ladder haiku < sonnet < opus < fable, never a model stronger than the one the agent itself runs — except when doing the job itself costs less than the brief, the agent's fresh-context reading and the report together; when in doubt it delegates. The mode governs only choices you leave open: an explicit instruction naming the executor — "do this yourself", "spawn a subagent", "use haiku" — always wins, on or off.

The mode is settable at three scopes. Session is the default and the only togglable one: it lives in the conversation, plus a small state file in the session's scratchpad directory so `--status` survives a compaction, and a fresh session starts with whatever the standing scopes say. `/delegation --user --on` and `/delegation --project --on` make it standing by writing the instruction as a managed block, fenced in HTML comments, at the end of the context file your agent already loads — your global `~/.claude/CLAUDE.md` for `--user`, the project's own `AGENTS.md` or `CLAUDE.md` for `--project` (created, and bridged with a `CLAUDE.md` containing `@AGENTS.md`, when the project has none). Both show you the exact file and the exact insertion and wait for your yes; `--off` removes that block again and nothing else. **A project's context file is normally committed**, so setting project scope puts everyone who clones the repo in delegation mode — the confirmation says so, and warns as well when the target file already has uncommitted changes. The persistent scopes never toggle: they take `--on`, `--off` or `--status`, never a bare flip. `--status` is the one place where leaving the scope out does not mean the session — it then reports all three scopes, the resulting verdict, and whether a block has drifted from the installed `lib/delegation-mode.md` (refresh it with `/delegation <scope> --on`).

A session instruction beats any standing block, but `/delegation --off` **suspends the block rather than removing it**: the text is still in the context window, still paid for, and after a compaction the block survives while the session instruction may not — so run `/delegation --off` again if the agent starts delegating anyway. To keep the mode out of a repo entirely, do not set project scope; to drop it everywhere, run `--user --off` and `--project --off`.

The skill only ever confirms its state — it never switches model or effort (a skill cannot run interactive commands) and never prompts you to. Run `/model` and `/effort` yourself, and check `/status` **before** you switch: it reports what you have now, so it only tells you what to restore to if you asked it first.

This is a working mode, not a build run: it changes how the agent handles whatever you ask next. For an away-from-keyboard build that takes a repository's ready-for-agent issues and drives sub-agents through implement, verify and integrate, use [kntnt-code-skills](https://github.com/Kntnt/kntnt-code-skills)' `/orchestrate` instead.

### `/skill-maker`

Run `/skill-maker` to author one skill, or `/skill-maker <name or plan>` to seed it with anything from a bare name to a detailed plan. It interviews you to settle every load-bearing decision – the leading word, the invocation type, the trigger boundary, the steps-vs-reference shape, what goes in `lib/` – then writes `skills/<name>/SKILL.md` (plus any shared module) following Matt Pocock's craft and Kntnt's conventions. The general craft and the interview protocol are vendored into the plugin (`lib/vendor/matt-pocock/`), so the skill is self-contained.

### `/plugin-maker`

Run `/plugin-maker` in a folder – empty for a new plugin, or an existing plugin to add a skill – optionally with a plan: `/plugin-maker <plan>`. It resolves your author identity (from `git`, `gh` and sibling repos), interviews the plugin's design, lays the common base by invoking `kntnt-code-skills:init`, layers the plugin-specific files and the `lib/templates/` boilerplate on top, authors each skill through the `skill-maker` process, wires the plugin together, then re-runs `/agents-md`. It may make the initial commit and – through `init`'s own questions – create the GitHub repository, but it stops before `/release`: review the result, then release yourself.

### `/help`

Run `/kntnt-skills:help` for a manpage-style overview of the plugin's skills, or `/kntnt-skills:help <skill-name>` for one skill's details. The command is typed-only (disabled for model invocation), so it never fires on its own. Its whole output is rendered by `scripts/help.py` from the plugin's own `.claude-plugin/plugin.json` and each `skills/<name>/SKILL.md`, so the help can never drift from the actual skills.

## Questions, bugs, and feature requests

Have a usage question or something to discuss? Please use [Discussions](https://github.com/Kntnt/kntnt-skills/discussions).

Found a bug or want to request a feature? Please [open an issue](https://github.com/Kntnt/kntnt-skills/issues). Search the existing issues first to avoid duplicates.

## How you can contribute

Contributions are welcome, small or large – reporting a bug, requesting a feature, proposing a new general-purpose skill or improving the documentation. Open an issue to start a discussion, or submit a pull request. A skill that grows beyond general-purpose use, or gathers enough siblings around a shared theme, may graduate into a specialised plugin of its own.

## License

kntnt-skills is licensed under the Apache License 2.0. See [LICENSE](LICENSE) for the full text and [NOTICE](NOTICE) for attribution.

## Changelog

Release notes are in [CHANGELOG.md](CHANGELOG.md).

The project follows [Keep a Changelog](https://keepachangelog.com/) and [Semantic Versioning](https://semver.org/).
