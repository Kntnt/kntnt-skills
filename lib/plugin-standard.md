# The Kntnt plugin standard

The canonical shape of a Kntnt plugin for Claude Code and Cowork. This is the single source of truth: `plugin-maker` **generates** a plugin from it, `scripts/audit.py` **verifies** a plugin against it, and the README's authoring notes **describe** it. If those three drift, the standard rots — so they all derive from here.

Authoring **one** skill is governed by `${CLAUDE_PLUGIN_ROOT}/lib/skill-conventions.md`; this file governs the **plugin** around the skills.

## The shape

```
<plugin-name>/
├── .claude-plugin/
│   ├── plugin.json          # manifest: name, version, description, author, homepage, repository, license, keywords
│   └── marketplace.json     # single-plugin marketplace pointing at <owner>/<name>
├── .github/
│   ├── ISSUE_TEMPLATE/bug.md
│   └── workflows/audit.yml  # CI: runs audit.py (+ tests, when present)
├── .claude/
│   └── settings.json        # permissions: allow Bash(uv:*)
├── commands/
│   └── help.md              # typed-only /<plugin>:help command
├── scripts/
│   ├── help.py              # renders /help from plugin.json + each SKILL.md (verbatim across plugins)
│   └── audit.py             # scriptable standard checks (see Audit below)
├── skills/
│   └── <skill>/SKILL.md     # one directory per skill, ≥ 1
├── lib/                     # CONDITIONAL — shared content the skills read
├── docs/                    # CONDITIONAL — human documentation
├── tests/                   # CONDITIONAL — only when a non-trivial script ships
├── .gitignore
├── .pre-commit-config.yaml  # runs audit.py (+ tests) before each commit
├── CHANGELOG.md             # Keep a Changelog + SemVer
├── CONTRIBUTING.md
├── LICENSE                  # Apache-2.0
├── NOTICE                   # copyright + third-party attribution
└── README.md
```

## Mandatory core

Every Kntnt plugin has all of these. Absent any one, it is not on-standard:

`.claude-plugin/plugin.json` · `.claude-plugin/marketplace.json` · `.github/ISSUE_TEMPLATE/bug.md` · `.github/workflows/audit.yml` · `.claude/settings.json` · `commands/help.md` · `scripts/help.py` · `scripts/audit.py` · `skills/<name>/SKILL.md` (≥ 1) · `.gitignore` · `.pre-commit-config.yaml` · `CHANGELOG.md` · `CONTRIBUTING.md` · `LICENSE` · `NOTICE` · `README.md`

## Conditional parts

Generated only when warranted — never as empty scaffolding:

- **`lib/`** — when skills share content modules (rules, protocols, templates, vendored references). Most plugins have it; a single trivial skill may not. Skills read it as `${CLAUDE_PLUGIN_ROOT}/lib/…`.
- **`docs/`** — **human** documentation (architecture, authoring, versioning), only when there is real architecture to explain. The rare case: of the themed Kntnt plugins only the largest carries `docs/`. README plus `CONTRIBUTING.md` usually suffice.
- **`tests/`** — only when the plugin ships a **non-trivial script** worth testing (a renderer, a scaffolder, an orchestrator). A pure-prompt plugin gets **no** `tests/`. The `help.py`/`audit.py` boilerplate is not itself test-targeted.
- **extra `scripts/`** — only when the plugin genuinely needs them.

## Two documentation layers, two audiences

- **`docs/` is for humans** — prose people read.
- **`AGENTS.md` + `agents.d/` is for the agent** — on-demand context, with the `CLAUDE.md → @AGENTS.md` bridge. This layer is produced by the `agents-md` skill, which creates nothing unless something is load-bearing and non-discoverable. Do not hand-write it; run `agents-md` (the finish step below) and let it decide.

## Identity is parameterised; structure and licence are fixed

The **structure** above and the **Apache-2.0** licence are the standard — fixed. The **identity** stamped into the files is a parameter, so anyone can generate their own on-standard plugin. Resolve each token, then confirm it in the interview:

| Token | Meaning | Default source (in order) |
| --- | --- | --- |
| `{{PLUGIN_NAME}}` | plugin + repo name | the working-directory name |
| `{{PLUGIN_DESCRIPTION}}` | one-line description | from the interview |
| `{{AUTHOR_NAME}}` | author | `git config user.name` |
| `{{AUTHOR_EMAIL}}` | author email | `git config user.email` |
| `{{AUTHOR_URL}}` | author's website (for `plugin.json` `author.url` and `marketplace.json` `owner.url`) | from the interview; else the repo URL |
| `{{OWNER}}` | GitHub owner/org | `gh` auth login/org; sibling `kntnt-*` repos; else `{{AUTHOR_NAME}}` |
| `{{KEYWORDS}}` | `plugin.json` keywords array contents (quoted, comma-separated) | from the interview |
| `{{YEAR}}` | copyright year | the current year |
| `{{DATE}}` | initial release date in `CHANGELOG.md` (`YYYY-MM-DD`) | the current date |

The homepage and repository URLs are not separate tokens — they are always `https://github.com/{{OWNER}}/{{PLUGIN_NAME}}`. The licence is always Apache-2.0 with a `NOTICE`. Someone who wants a different licence changes two files; it is not a generation parameter.

## The help command

`commands/help.md` is a typed-only command (`disable-model-invocation: true`, `model: sonnet`) whose whole output is rendered by `scripts/help.py`. `help.py` reads `plugin.json` for the header and each `skills/<name>/SKILL.md` for its intro paragraph, then emits the formatted block — so the help can never drift from the actual skills. **`help.py` is generic and vendored verbatim** between plugins; only its module docstring names the plugin. This is why every `SKILL.md` must carry a clean intro paragraph (see `skill-conventions.md`).

## Audit

`scripts/audit.py` is a standard-library PEP 723 script, run with `uv run scripts/audit.py`, exit 0 when clean and 1 otherwise. It is the hard gate in pre-commit and CI. Three tiers:

1. **Universal checks — always emitted.** `plugin.json` is well-formed and carries `name`/`version`/`description`; `version` matches the latest non-`[Unreleased]` `## [x]` heading in `CHANGELOG.md`; `marketplace.json` is well-formed; every `skills/<name>/` contains a `SKILL.md`; skill names are consistent across `plugin.json`/marketplace/help. These apply to *every* Kntnt plugin, this one included.
2. **Structural sync checks — inferred aggressively.** Whenever the plugin keeps a hand-maintained index that must mirror files on disk (a `lib/.../_index.md` ↔ its sibling files, a `CANONICAL_ORDER` ↔ its modules), generate the symmetry check both directions. These indexes rot silently; a check is cheap insurance.
3. **Judgment checks — a documented extension point.** Invariants that need human judgment (is this prose genuinely self-contained?) are left as a clearly-marked place to add checks, noted in `CONTRIBUTING.md`. Do not auto-generate guesses here.

## Pre-commit and CI

`.pre-commit-config.yaml` runs `audit.py` (and `tests/`, when present) before each commit; `.github/workflows/audit.yml` re-runs the same on push and PR. Both invoke through `uv`, which provisions the pinned Python from each script's PEP 723 metadata — hence `.claude/settings.json` allows `Bash(uv:*)`.

## Versioning

[Semantic Versioning](https://semver.org/) and [Keep a Changelog](https://keepachangelog.com/). A new plugin starts at `0.1.0` with an `## [Unreleased]` section above it. Pre-1.0 (major `0`): ignore backwards-compatibility — no deprecations, no migrations. `plugin.json`'s `version` must always equal the latest released CHANGELOG heading (the audit enforces it).

## Modes: greenfield and augment

`plugin-maker` detects which mode by looking for `.claude-plugin/plugin.json`:

- **Greenfield** (no manifest / empty dir) — generate the whole shell, author each skill via `skill-maker`, then the finish sequence.
- **Augment** (manifest present) — interview only the new skill, author it via `skill-maker`, then do the plugin-level rewiring: a new `CHANGELOG` entry, the skill added to the README skill list and `marketplace.json` description, any new structural `audit` checks, a version bump. (`help` needs no edit — it reads `SKILL.md` live.) Re-run `agents-md`.

## The finish sequence

After scaffolding (greenfield) or rewiring (augment), in order:

1. **Self-verify** — run the generated `audit.py` (and `tests/`, if any); fix until green. Never declare done on a red audit.
2. **Run `agents-md`** on the plugin to produce the AI layer (`AGENTS.md`/`agents.d/`/`CLAUDE.md`) — or let it decline.
3. **`git init` + initial commit** (greenfield) — the standard assumes git; initialise one and commit a clean baseline.
4. **Stop and hand off.** Report what was created, the audit result, and the next steps: review the diff, `gh repo create`, then `/release`. Do **nothing** outward-facing — no repo creation, no push, no release. `marketplace.json` still points at the intended `{{OWNER}}/{{PLUGIN_NAME}}`; that is metadata, fine before the repo exists.
