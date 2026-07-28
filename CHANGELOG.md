# Changelog

All notable changes to this project are documented here. The format follows [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Changed

- **`/fabulous` is now `/delegation`, and the mode is settable at three scopes.** The skill directory moved from `skills/fabulous/` to `skills/delegation/`; the noun replaces the adjective, so `/delegation --on` and "delegation mode is on" use the same word. Session scope stays the default and the only togglable one (state in `kntnt-skills-delegation.json` in the session's scratchpad, replacing `fabulous.json`), and `--user` / `--project` make the mode standing by writing it as a managed block — fenced in `<!-- kntnt-skills:delegation -->` comments — at the end of the context file the host already loads: `~/.claude/CLAUDE.md` for the user, the project's own `AGENTS.md` / `CLAUDE.md` (created and bridged when absent) for the project. Persistent scopes never toggle, always confirm the exact file and insertion first, and warn that a project's context file is normally committed, so every clone gets the mode. `--status` reports all three scopes, the verdict and any drift from the installed `lib/delegation-mode.md`; a session `--off` suspends the standing block rather than removing it.
- **The working-mode text moved out of the skill into `lib/delegation-mode.md`** — self-contained, host-neutral and free of any mechanism, because it is copied verbatim into users' context files and read by non-Claude agents. `SKILL.md` no longer restates it. The wording is sharpened where testing showed it did not bite: thinking is *never* delegated (understanding, diagnosis, the decision, the brief, verification, the final answer), and doing it yourself is right only when that *costs less than* brief + the agent's fresh-context reading + report.
- **The audit's `lib/` guard is derived from the references instead of a hand-kept list.** Check `(d)` no longer enumerates the vendored Matt Pocock files: it scans every `.md` under `skills/`, `commands/` and `lib/` for `${CLAUDE_PLUGIN_ROOT}/lib/…` paths and asserts each target exists — a directory when the reference ends in `/`, a file otherwise — naming the referencing file in the finding. The hand-kept list guarded eight files while missing two that skills genuinely read (`lib/protocols/interview.md`, `lib/templates/`), so renaming either broke a skill silently — the exact failure the guard exists to prevent. The derived check covers all ten, and a new shared module is guarded the moment a skill reads it, with no edit to `audit.py`. Only this direction: a `lib/` file that no path names is not dead, so the reverse check is deliberately not generated.
- **`lib/plugin-standard.md` names the reference↔files check as a tier-2 example**, so `plugin-maker` emits the same guard for the next plugin instead of leaving it to rot in this repo's `audit.py` alone. Tier 2's "both directions" rule gains the carve-out the example needs — the reverse is not generated where it would fire on healthy files — and `lib/templates/audit.py`'s extension-point comment, which is what `plugin-maker` actually copies, now says the same and points at deriving the index rather than hand-keeping it.
- **`agents-md` now recognises managed blocks.** A block fenced by `<!-- <plugin>:<skill> -->` … `<!-- /<plugin>:<skill> -->` is owned by that skill: gates, compression and conflict detection do not apply, and it is never edited, compressed, moved or deleted — only reported. Without this, two skills in the same plugin would fight over the same file.

### Added

- **Audit check `(e)`** – the `lib/` files that must exist although no skill names their path: `vendor/matt-pocock/LICENSE` (a licence obligation nobody reads at runtime) and `vendor/matt-pocock/writing-great-skills/GLOSSARY.md` (pointed at in prose, never as a path). A tier-2 structural check covering exactly what the derived check `(d)` cannot see, with the reason it cannot be derived recorded beside each entry — which is what stops the list growing back into a hand-kept mirror of `lib/`.

### Removed

- **The `previousModel` / `previousEffort` memo** that `/fabulous` wrote when turned on, and with it the effort-detection procedure (`CLAUDE_CODE_EFFORT_LEVEL` → `.claude/settings.local.json` → `.claude/settings.json` → `~/.claude/settings.json`). Under scoping the memo would exist when the mode was turned on by command and be missing when it came from a context file — the same effective state with the memo sometimes present, and an absence discovered exactly when it is needed. Check `/status` **before** switching model or effort instead. As before, the skill never switches either and never suggests it.

## [0.7.1] – 2026-07-24

### Changed

- **`/fabulous` state is now per-session.** The state file moved from `~/.claude/fabulous.json` to `fabulous.json` in the session's scratchpad directory, so the mode can never leak into another session — a fresh session always starts OFF (in an environment without a scratchpad, the state is held in conversation alone). The mode's boundary is sharpened: it governs only choices the user leaves open — an explicit instruction naming the executor ("do this yourself", "spawn a subagent", "use haiku") always wins, ON or OFF — and turning OFF now explicitly renders the working-mode text inert history rather than merely dropping it.

## [0.7.0] – 2026-07-24

### Added

- **`/fabulous`** – toggles the fabulous working mode: the agent orchestrates (thinks, plans, briefs, verifies) while subagents execute on the lowest model judged able to do the job at the inherited effort level (ladder haiku < sonnet < opus < fable, never a model stronger than the delegating agent itself) — except when doing the job itself is cheaper than brief + agent reading + report. `/fabulous` toggles, `--on`/`--off` force a state, `--status` reports. Turning it on notes the current model and effort in `~/.claude/fabulous.json`; turning it off reports and clears them. The skill only confirms its state — it never switches model or effort (a skill cannot run interactive commands) and never prompts the user to; running `/model` / `/effort` is the user's own move.

## [0.6.0] – 2026-06-26

### Changed

- **`agents-md` is now model-invocable.** The `disable-model-invocation: true` flag is removed and the `description` rewritten in the explicit-only style (the trigger boundary is now the sole guard), so `init` can invoke it by qualified name (`kntnt-skills:agents-md`). It still fires only on explicit invocation and never on a bare mention of AGENTS.md/CLAUDE.md. `skill-conventions.md` notes the pattern: a skill that must be both explicit-only and reachable by another skill keeps a model-invoked, ruthlessly explicit description rather than the flag.
- **`plugin-maker` now lays its common base by invoking `kntnt-code-skills:init`** (git, the `agents-md` skeleton, the coding standard, a licence, the generic README/CHANGELOG/CONTRIBUTING/NOTICE, and `.gitignore`), then layers the plugin-specific files on top. Its boundary is relaxed: it **may** make the initial commit and create the GitHub repository (through `init`'s questions), but still **stops before `/release`**.

### Added

- **`agents-md --force`** lays the canonical skeleton (`CLAUDE.md` = `@AGENTS.md`, an `AGENTS.md` with the Ground rules block and an empty `## References`, and an `agents.d/` with a `.gitkeep`) on a project where ordinary discovery would write nothing — the seam `init` uses to seed a new project. On a project that already warrants content, `--force` is a normal run.

## [0.5.1] – 2026-06-22

### Changed

- **`NOTICE`** now credits the caveman-compression idea (Julius Brussee) and the observation that a minimal rule set can outperform a long one (Kuba Guzik), in a section kept separate from the bundled third-party code.

## [0.5.0] – 2026-06-22

### Added

- **`/skill-maker`** – authors one complete skill to the Kntnt standard. It interviews the user one question at a time, applies Matt Pocock's skill-writing craft together with Kntnt's house conventions, and writes the `SKILL.md` (and any shared `lib/` it needs). User-invoked; built to be driven standalone or by `/plugin-maker`.
- **`/plugin-maker`** – scaffolds a whole Claude Code / Cowork plugin to the Kntnt standard. It resolves the author identity, interviews the plugin's design, generates the standard file shell from `lib/templates/` with the identity filled in, authors each skill through the `skill-maker` process, wires up the help command, audit, README and changelog, then runs `agents-md`, initialises git and stops before anything outward-facing. Handles greenfield (an empty folder) and augment (adding a skill to an existing plugin) by detecting `.claude-plugin/plugin.json`.
- **`lib/plugin-standard.md`, `lib/skill-conventions.md`, `lib/protocols/interview.md`** – the single source of truth the two new skills generate from and the audit verifies against: the canonical plugin shape and conditional-file rules, the house skill conventions, and the shared interview protocol.
- **`lib/vendor/matt-pocock/`** – Matt Pocock's `writing-great-skills` (`SKILL.md` + `GLOSSARY.md`) and `grilling` skill, vendored verbatim under the MIT licence with attribution (see the directory's `LICENSE` and the `NOTICE` file). They are the craft and interview references the two new skills build on.
- **`lib/templates/`** – the token-parameterised boilerplate `plugin-maker` copies and fills (manifest, marketplace, README, CONTRIBUTING, CHANGELOG, LICENSE, NOTICE, `.gitignore`, pre-commit, CI workflow, issue template, settings, the help command, a verbatim `help.py`, and a tier-1 `audit.py` skeleton).
- **Standard infrastructure for this plugin itself** – `scripts/audit.py` (the universal checks plus a structural check that the vendored files are present), `CONTRIBUTING.md`, `.github/ISSUE_TEMPLATE/bug.md`, `.github/workflows/audit.yml`, `.pre-commit-config.yaml` and `.claude/settings.json`, bringing `kntnt-skills` up to the standard the new skills enforce.

### Changed

- **`README.md`** now documents all four skills, adds an Audit badge, notes the vendored Matt Pocock content, and records that `uv` is now used for both `/help` and the audit.
- **`.gitignore`** adopts the standard base (macOS, editor and Python-cache entries) alongside the existing local eval-workspace entry.
- **`skills/agents-md/SKILL.md`** prose reflowed to one physical line per paragraph (the project's Markdown convention); no content or behaviour change. `skills/caveman/SKILL.md` and `lib/caveman.md` already conformed.

## [0.4.0] – 2026-06-20

### Added

- **`/help`** – a typed-only command (`/kntnt-skills:help [skill-name]`) and its renderer `scripts/help.py`: a manpage-style overview of the plugin's skills, or one skill's details. The command is disabled for model invocation, so it runs only when typed; `scripts/help.py` renders the whole block from the plugin's own `.claude-plugin/plugin.json` and each `skills/<name>/SKILL.md`, so the help can never drift from the actual skills. It follows the same pattern and shares the same renderer logic as `/kntnt-code-skills:help`. The renderer is a standalone PEP 723 script run via `uv`.

### Changed

- **`README.md`** now documents the `/help` command (in the skills list and a usage subsection) and records that `uv` is required, but only for `/help`; the previous blanket "no external dependencies" note is corrected accordingly.

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

[Unreleased]: https://github.com/Kntnt/kntnt-skills/compare/v0.7.1...HEAD
[0.7.1]: https://github.com/Kntnt/kntnt-skills/releases/tag/v0.7.1
[0.7.0]: https://github.com/Kntnt/kntnt-skills/releases/tag/v0.7.0
[0.6.0]: https://github.com/Kntnt/kntnt-skills/releases/tag/v0.6.0
[0.5.1]: https://github.com/Kntnt/kntnt-skills/releases/tag/v0.5.1
[0.5.0]: https://github.com/Kntnt/kntnt-skills/releases/tag/v0.5.0
[0.4.0]: https://github.com/Kntnt/kntnt-skills/releases/tag/v0.4.0
[0.3.0]: https://github.com/Kntnt/kntnt-skills/releases/tag/v0.3.0
[0.2.0]: https://github.com/Kntnt/kntnt-skills/releases/tag/v0.2.0
