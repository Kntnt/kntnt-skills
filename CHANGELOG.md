# Changelog

All notable changes to this project are documented here. The format follows [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.1.0] – 2026-06-19

### Added

- Initial release.
- **`/agents-md`** – create lean, portable agent context files, or distil an existing `AGENTS.md` / `CLAUDE.md` down to what earns its place. Runs on the current repository, a given path, or the global `~/.claude/CLAUDE.md`.
- Plugin manifest (`.claude-plugin/plugin.json`) and single-plugin marketplace (`.claude-plugin/marketplace.json`) so the plugin installs via `/plugin marketplace add Kntnt/kntnt-skills`.
- `README.md`, `LICENSE` (Apache-2.0), `NOTICE` and an agent guide (`AGENTS.md` with the `CLAUDE.md` bridge).
