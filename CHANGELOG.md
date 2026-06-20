# Changelog

All notable changes to this project are documented here. The format follows [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.3.0] – 2026-06-20

### Added

- **`/caveman`** – a new skill that applies caveman compression (maximum meaning per token, with no loss of facts, code, numbers or register) to all of the agent's output, toggled on with `/caveman` or `/caveman --on` and off with `/caveman --off`, or one-shot to a single text or file with `/caveman <ref>` or `/caveman --file=<path>`. The one-shot forms never change the on/off state.
- **`lib/caveman.md`** – a shared definition of what caveman compression means, now the single source of truth for both `/caveman` and `/agents-md`.

### Changed

- **`/agents-md` now reads its compression rules from the shared `lib/caveman.md`** instead of embedding its own copy, keeping only its context-file-specific additions (imperative instruction style and the before/after examples). Its behaviour is unchanged.

## [0.2.0] – 2026-06-20

### Added

- Two flags that control the output file shape: `--no-claude-md` (write only `AGENTS.md`, skip the `CLAUDE.md` bridge — for repos read by AGENTS.md-native tools where you manage `CLAUDE.md` yourself) and `--only-claude-md` (write a single `CLAUDE.md` holding the content directly, with no `AGENTS.md` — Claude-only, trading cross-tool portability for one fewer file). The two are mutually exclusive.

### Changed

- **`/agents-md` is now far more aggressive about minimizing tokens.** It treats two failures independently: *existence* (a file or line carrying nothing load-bearing should not exist) and *expression* (a kept fact is compressed to its core, not relocated verbatim). New three-gate flow — should anything exist at all (create nothing, and delete dead `CLAUDE.md`/`AGENTS.md`, when nothing passes the decision test); where each surviving fact lives; express it in the fewest tokens. Adds caveman-style compression rules, a subagent build-and-critique loop bounded by `--max-iterations=N` (default 2 = one build plus one critical send-back), a "many small single-concern files" granularity rule, and a mandatory before/after token measurement with the rule that if total tokens grew, the run failed. `CLAUDE.md` is now exactly `@AGENTS.md` (no meta-notes); the Ground rules block is conditional, never the sole reason to create the pair.
- **The on-demand directory is renamed `AGENTS.d/` → `agents.d/`** (lowercase, the Unix `.d` convention).

### Removed

- The plugin's own `CLAUDE.md` and `AGENTS.md` — they carried nothing load-bearing, exactly the case the improved skill now declines to create.

## [0.1.0] – 2026-06-19

### Added

- Initial release.
- **`/agents-md`** – create lean, portable agent context files, or distil an existing `AGENTS.md` / `CLAUDE.md` down to what earns its place. Runs on the current repository, a given path, or the global `~/.claude/CLAUDE.md`.
- Plugin manifest (`.claude-plugin/plugin.json`) and single-plugin marketplace (`.claude-plugin/marketplace.json`) so the plugin installs via `/plugin marketplace add Kntnt/kntnt-skills`.
- `README.md`, `LICENSE` (Apache-2.0), `NOTICE` and an agent guide (`AGENTS.md` with the `CLAUDE.md` bridge).

[Unreleased]: https://github.com/Kntnt/kntnt-skills/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/Kntnt/kntnt-skills/releases/tag/v0.3.0
[0.2.0]: https://github.com/Kntnt/kntnt-skills/releases/tag/v0.2.0
