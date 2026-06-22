# Contributing to {{PLUGIN_NAME}}

Thanks for considering a contribution. The plugin is open source under the Apache License 2.0, which means anyone is free to fork it and modify it for their own purposes. This document describes the *project norm* — what kinds of contributions are likely to be welcomed into the upstream repository at [{{OWNER}}/{{PLUGIN_NAME}}](https://github.com/{{OWNER}}/{{PLUGIN_NAME}}). It is not a legal restriction on what you may do with the code; it is editorial guidance on what is likely to be merged.

## Contribution scope

| Category | Examples | Reception |
|---|---|---|
| Welcomed without question | Bug reports; bug fixes against existing skills; corrections to broken examples; typo and grammar fixes in prose; clarifications that do not alter behaviour. | Open a PR. If the change is small and self-evidently correct, it is usually merged quickly. |
| Accepted but discussed first | New skills; changes to an existing skill's behaviour, scope, or trigger boundary; new shared `lib/` modules. | Open an issue first to align on intent before writing code. A PR without prior discussion may still land, but expect feedback rounds. |
| Unlikely to be merged but free to fork | Changes that alter the plugin's positions or restructure the architecture in a way that conflicts with the standard. | The Apache 2.0 licence makes forking explicit and lawful. If you want a different design, build it in your fork. |

## Inbound licensing

By submitting a contribution, you agree it is licensed under Apache 2.0 by virtue of Apache License 2.0 §5 *Submission of Contributions*, which states that any contribution intentionally submitted for inclusion in the work shall be under the terms of that licence unless you explicitly state otherwise. No separate contributor licence agreement is required.

## How to contribute

1. **Open an issue first** for anything in the *discussed* row above. For *welcomed* items, you can open a PR directly. Use the issue tracker at <https://github.com/{{OWNER}}/{{PLUGIN_NAME}}/issues>.
2. **Bug reports** should follow the template under `.github/ISSUE_TEMPLATE/bug.md` — which skill, which input, observed versus expected outcome.
3. **One concern per PR.** Smaller PRs land faster.
4. **Run the audit before committing.** `uv run scripts/audit.py` runs the scriptable standard checks. Install the pre-commit hook with `pip install pre-commit && pre-commit install` so it fires automatically; CI re-runs it on every push and PR.

## Adding a structural audit check

When you add a hand-maintained index that must mirror files on disk, add a matching symmetry check in `scripts/audit.py` (the marked extension point) so the index cannot rot silently.

## Style and language conventions

- All identifiers and comments in English.
- Each skill's `SKILL.md` opens with a self-contained intro paragraph — it doubles as the `/help` text.
- Shared rules live in `lib/` and are referenced, never duplicated.

## Questions

Open an issue. Discussion happens in the open.
