# Contributing to kntnt-skills

Thanks for considering a contribution. The plugin is open source under the Apache License 2.0, which means anyone is free to fork it and modify it for their own purposes. This document describes the *project norm* — what kinds of contributions are likely to be welcomed into the upstream repository at [Kntnt/kntnt-skills](https://github.com/Kntnt/kntnt-skills). It is not a legal restriction on what you may do with the code; it is editorial guidance on what is likely to be merged.

## Contribution scope

kntnt-skills collects general-purpose skills that do not belong to a themed Kntnt plugin. A skill that grows beyond general-purpose use, or gathers enough siblings around a shared theme, may graduate into a specialised plugin of its own.

| Category | Examples | Reception |
|---|---|---|
| Welcomed without question | Bug reports; bug fixes against existing skills; corrections to broken examples; typo and grammar fixes in prose; clarifications that do not alter behaviour. | Open a PR. If the change is small and self-evidently correct, it is usually merged quickly. |
| Accepted but discussed first | A new general-purpose skill; changes to an existing skill's behaviour, scope, or trigger boundary; new shared `lib/` modules; changes to the plugin standard in `lib/plugin-standard.md`. | Open an issue first to align on intent before writing code. A PR without prior discussion may still land, but expect feedback rounds. |
| Unlikely to be merged but free to fork | Skills that belong to one of the themed Kntnt plugins; changes that alter the standard's positions or restructure the architecture in conflict with it. | The Apache 2.0 licence makes forking explicit and lawful. If you want a different design, build it in your fork. |

## Inbound licensing

By submitting a contribution, you agree it is licensed under Apache 2.0 by virtue of Apache License 2.0 §5 *Submission of Contributions*, which states that any contribution intentionally submitted for inclusion in the work shall be under the terms of that licence unless you explicitly state otherwise. No separate contributor licence agreement is required.

## Vendored third-party content

`lib/vendor/matt-pocock/` holds files copied verbatim from [Matt Pocock's skills](https://github.com/mattpocock/skills) under the MIT licence (see the `LICENSE` in that directory and the `NOTICE` file). **Do not edit the vendored files** — keeping them verbatim is what keeps the attribution clean and the re-sync trivial. To update them, replace them in place from upstream. Kntnt's own conventions that build on them live in `lib/skill-conventions.md` and `lib/plugin-standard.md`.

## How to contribute

1. **Open an issue first** for anything in the *discussed* row above. For *welcomed* items, you can open a PR directly. Use the issue tracker at <https://github.com/Kntnt/kntnt-skills/issues>.
2. **Bug reports** should follow the template under `.github/ISSUE_TEMPLATE/bug.md` — which skill, which input, observed versus expected outcome.
3. **One concern per PR.** Smaller PRs land faster.
4. **Run the audit before committing.** `uv run scripts/audit.py` runs the scriptable standard checks. Install the pre-commit hook with `pip install pre-commit && pre-commit install` so it fires automatically; CI re-runs it on every push and PR.

## Style and language conventions

- All identifiers and comments in English.
- Each skill's `SKILL.md` opens with a self-contained intro paragraph — it doubles as the `/help` text.
- Shared rules live in `lib/` and are referenced via `${CLAUDE_PLUGIN_ROOT}/lib/…`, never duplicated.

## Questions

Open an issue. Discussion happens in the open.
