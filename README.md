# kntnt-skills

[![License](https://img.shields.io/github/license/Kntnt/kntnt-skills)](LICENSE)
[![Latest release](https://img.shields.io/github/v/release/Kntnt/kntnt-skills)](https://github.com/Kntnt/kntnt-skills/releases/latest)

kntnt-skills is a Claude Code plugin that collects Kntnt's general-purpose skills – the ones that are useful on their own but do not belong to any of the themed Kntnt plugins.

## Description

Kntnt maintains several skill plugins for Claude Code. Most are built around a single theme – writing, code, pillar pages – and each lives in its own repository. A few skills fit none of those themes yet still earn a place in the toolbox. This plugin is where they live.

Without a home of this kind, a standalone skill has two poor options: a repository of its own, which is heavy for a single skill, or burial inside a themed plugin it does not really belong to. kntnt-skills avoids both. It gives small, self-contained skills one installable home, and points you to the specialised plugins whenever one of them suits the job better.

### Available skills

- **`/agents-md`** – minimise the tokens an agent must load from `CLAUDE.md` / `AGENTS.md`. It keeps only what every session truly needs, compresses it hard, splits the rest into small on-demand `agents.d/` files, and creates nothing (or deletes existing files) when there is nothing load-bearing to keep.

### The Kntnt skill family

When your task is specifically about writing, code or pillar pages, one of the dedicated plugins will serve you better. Each is maintained in its own repository:

- [kntnt-text-skills](https://github.com/Kntnt/kntnt-text-skills) – writing, editing, proofreading and reviewing text against Kntnt's house style, in Swedish, British English and American English.
- [kntnt-code-skills](https://github.com/Kntnt/kntnt-code-skills) – coding standards across languages and frameworks, release and push workflows, and multi-agent orchestration that turns issues into implemented code.
- [kntnt-pillar-page-skills](https://github.com/Kntnt/kntnt-pillar-page-skills) – writing, structuring, reviewing and previewing pillar pages, built on top of kntnt-text-skills.

Reach for kntnt-skills for the useful things that fall outside those three.

## Requirements

kntnt-skills runs in Claude Code or Claude Cowork. It needs support for slash commands, YAML frontmatter (including `disable-model-invocation`) and skills. No external services or dependencies are required.

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
