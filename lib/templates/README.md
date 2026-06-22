# {{PLUGIN_NAME}}

[![License](https://img.shields.io/github/license/{{OWNER}}/{{PLUGIN_NAME}})](LICENSE)
[![Latest release](https://img.shields.io/github/v/release/{{OWNER}}/{{PLUGIN_NAME}})](https://github.com/{{OWNER}}/{{PLUGIN_NAME}}/releases/latest)
[![Audit](https://github.com/{{OWNER}}/{{PLUGIN_NAME}}/actions/workflows/audit.yml/badge.svg)](https://github.com/{{OWNER}}/{{PLUGIN_NAME}}/actions/workflows/audit.yml)

{{PLUGIN_DESCRIPTION}}

## Description

<!-- One or two paragraphs on what the plugin is for and the problem it solves. -->

### Available skills

{{SKILLS_OVERVIEW}}

## Requirements

The plugin runs in Claude Code or Cowork and needs support for slash commands, YAML frontmatter (including `disable-model-invocation`) and skills. The `/help` command renders its output with [uv](https://docs.astral.sh/uv/), which runs `scripts/help.py` (a standard-library-only PEP 723 script) and provisions Python 3.12+ from the script's own metadata; uv is needed only for `/help` and for the audit.

## Installation

Register the marketplace and install from within Claude Code or Cowork:

```
/plugin marketplace add {{OWNER}}/{{PLUGIN_NAME}}
/plugin install {{PLUGIN_NAME}}@{{PLUGIN_NAME}}
```

Alternatively, clone the repository directly into your plugin directory:

```bash
git clone git@github.com:{{OWNER}}/{{PLUGIN_NAME}}.git ~/.claude/plugins/{{PLUGIN_NAME}}
```

## Usage

Each skill is invoked by its slash command.

{{SKILLS_USAGE}}

### `/{{PLUGIN_NAME}}:help`

Run `/{{PLUGIN_NAME}}:help` for a manpage-style overview of the plugin's skills, or `/{{PLUGIN_NAME}}:help <skill-name>` for one skill's details. The command is typed-only (disabled for model invocation), so it never fires on its own. Its whole output is rendered by `scripts/help.py` from the plugin's own `.claude-plugin/plugin.json` and each `skills/<name>/SKILL.md`, so the help can never drift from the actual skills.

## Questions, bugs, and feature requests

Have a usage question or something to discuss? Please use [Discussions](https://github.com/{{OWNER}}/{{PLUGIN_NAME}}/discussions).

Found a bug or want to request a feature? Please [open an issue](https://github.com/{{OWNER}}/{{PLUGIN_NAME}}/issues). Search the existing issues first to avoid duplicates.

## Development

There is nothing to compile — the plugin is a set of Markdown files and small Python helper scripts. Install the pre-commit hook so the audit runs before each commit:

```bash
pip install pre-commit && pre-commit install
```

The audit ([`scripts/audit.py`](scripts/audit.py)) is a self-contained PEP 723 script, run with `uv run scripts/audit.py`; [`uv`](https://docs.astral.sh/uv/) provisions it automatically. The same script is the hard gate in CI.

## How you can contribute

Contributions are welcome, small or large. Before editing anything under `skills/` or `lib/`, read [`CONTRIBUTING.md`](CONTRIBUTING.md) — it covers which kinds of change are likely to be merged and how inbound licensing works.

## License

Licensed under the Apache License 2.0. The full licence text is in [`LICENSE`](LICENSE), and the copyright and attribution notice is in [`NOTICE`](NOTICE). Contributions are accepted under the same terms by virtue of Apache 2.0 §5.

## Changelog

Release notes for each version live in [`CHANGELOG.md`](CHANGELOG.md).

The project follows [Keep a Changelog](https://keepachangelog.com/) and [Semantic Versioning](https://semver.org/).
