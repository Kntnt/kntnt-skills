# kntnt-skills

[![License](https://img.shields.io/github/license/Kntnt/kntnt-skills)](LICENSE)
[![Latest release](https://img.shields.io/github/v/release/Kntnt/kntnt-skills)](https://github.com/Kntnt/kntnt-skills/releases/latest)

kntnt-skills is a Claude Code plugin that collects Kntnt's general-purpose skills – the ones that are useful on their own but do not belong to any of the themed Kntnt plugins.

## Description

Kntnt maintains several skill plugins for Claude Code. Most are built around a single theme – writing, code, pillar pages – and each lives in its own repository. A few skills fit none of those themes yet still earn a place in the toolbox. This plugin is where they live.

Without a home of this kind, a standalone skill has two poor options: a repository of its own, which is heavy for a single skill, or burial inside a themed plugin it does not really belong to. kntnt-skills avoids both. It gives small, self-contained skills one installable home, and points you to the specialised plugins whenever one of them suits the job better.

### Available skills

- **`/agents-md`** – minimise the tokens an agent must load from `CLAUDE.md` / `AGENTS.md`. It keeps only what every session truly needs, compresses it hard, splits the rest into small on-demand `agents.d/` files, and creates nothing (or deletes existing files) when there is nothing load-bearing to keep.
- **`/caveman`** – apply caveman compression (maximum meaning per token, with no loss of facts, code, numbers or register) to everything the agent says, or one-shot to a single text or file. Turn it on with `/caveman` or `/caveman --on` and off with `/caveman --off`; compress one text or file with `/caveman <ref>` or `/caveman --file=<path>` without changing that on/off state. It shares its definition of "caveman" with `/agents-md` through `lib/caveman.md`.
- **`/help`** – a typed-only command (`/kntnt-skills:help [skill-name]`): a manpage-style overview of the plugin's skills, or one skill's details. Its output is rendered from the plugin's own `.claude-plugin/plugin.json` and `skills/<name>/SKILL.md` by `scripts/help.py`, so it never drifts from the actual skills.

### The Kntnt skill family

When your task is specifically about writing, code or pillar pages, one of the dedicated plugins will serve you better. Each is maintained in its own repository:

- [kntnt-text-skills](https://github.com/Kntnt/kntnt-text-skills) – writing, editing, proofreading and reviewing text against Kntnt's house style, in Swedish, British English and American English.
- [kntnt-code-skills](https://github.com/Kntnt/kntnt-code-skills) – coding standards across languages and frameworks, release and push workflows, and multi-agent orchestration that turns issues into implemented code.
- [kntnt-pillar-page-skills](https://github.com/Kntnt/kntnt-pillar-page-skills) – writing, structuring, reviewing and previewing pillar pages, built on top of kntnt-text-skills.

Reach for kntnt-skills for the useful things that fall outside those three.

## Requirements

kntnt-skills runs in Claude Code or Claude Cowork. It needs support for slash commands, YAML frontmatter (including `disable-model-invocation`) and skills. The two skills require no external services or dependencies. The `/help` command renders its output with [uv](https://docs.astral.sh/uv/), which runs `scripts/help.py` (a standard-library-only PEP 723 script) and provisions Python 3.12+ from the script's own metadata; uv is needed only for `/help`.

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
