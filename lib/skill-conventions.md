# Kntnt skill conventions

The house conventions for authoring **one** skill. The general craft of writing a predictable skill is Matt Pocock's, vendored at `${CLAUDE_PLUGIN_ROOT}/lib/vendor/matt-pocock/writing-great-skills/SKILL.md` (with its `GLOSSARY.md`). **Read those first.** This file is the Kntnt layer on top — the conventions that make a skill part of *this* family. **Where the two overlap or conflict, this file wins.**

## Read order

1. `lib/vendor/matt-pocock/writing-great-skills/SKILL.md` + `GLOSSARY.md` — general craft: predictability, leading words, information hierarchy, progressive disclosure, pruning, failure modes.
2. This file — the house conventions below.

Subagents do not auto-load either file. When authoring through a subagent, read both and paste their content into the subagent's prompt.

## Plugin-anchored triggers (the default)

A Kntnt skill fires only on phrasing that **names the plugin or the skill explicitly** — `/skill`, the qualified `/plugin:skill`, or natural language that names the plugin together with the skill ("Kntnt's X skill", "the X skill from this plugin"). It must **not** fire on a bare action word. "write", "edit", "review", "release" are everyday words; a skill that triggers on them fires when the user meant nothing of the sort.

- The `description` frontmatter field **is** the trigger boundary. Write it so the model can tell a plugin-anchored invocation from a bare action word, and say what must *not* trigger it.
- This is the default even for a model-invoked skill: model-invokable, but plugin-anchored.
- One documented exception pattern exists in this family: a conservative, broad-scope skill (e.g. `proofread`) may also answer a clear, specific request aimed at a concrete target. Use it sparingly and document it.

## Invocation type

Two choices, per Matt's *Invocation* section — pick by who must reach the skill:

- **Model-invoked** (default) — keep a `description` with rich, plugin-anchored trigger phrasing; omit `disable-model-invocation`. Costs context load (the description sits in the window every turn), but the agent and other skills can reach it.
- **User-invoked** — set `disable-model-invocation: true`; the `description` becomes a one-line human-facing summary with the trigger lists stripped. Zero context load. Use it for typed-only utilities — the `help`, `caveman` pattern in this plugin — where the skill should never fire on its own and no other skill needs to reach it. (A skill that must stay explicit-only *and* be reachable by another skill — `agents-md`, which `init` invokes by qualified name — instead keeps a model-invoked, ruthlessly explicit `description` as its only guard.)

## The intro paragraph is the help contract

`scripts/help.py` renders each skill's **first non-empty paragraph after the `# ` heading and before the first `## ` heading** as that skill's help text. So every `SKILL.md` must open, right under its H1, with a clean, self-contained paragraph that reads well in isolation — it is simultaneously the skill's opening and its public help entry. Do not start the body with a heading, a list, or a fragment that only makes sense in context.

## SKILL.md shape

```
---
name: <kebab-case, = the skill directory name>
description: <trigger boundary (model-invoked) or one-line summary (user-invoked)>
disable-model-invocation: true   # only for user-invoked utilities
---

# <skill name>

<the intro paragraph — the help contract above>

<body: steps, reference, or both — per the information hierarchy>
```

## House conventions for the body

- **The user, not the author.** All skill-internal text addresses *the user*. The plugin is generic; the house voice lives in metadata (`plugin.json`, `NOTICE`), never embedded in instructions.
- **Reference shared modules by plugin root.** Read shared `lib/` content as `${CLAUDE_PLUGIN_ROOT}/lib/…`, the same form the bundled `scripts/` use — so a read resolves against the installed plugin, not the runtime working directory. Keep each meaning in one place (single source of truth); do not restate a rule that lives in `lib/`.
- **Tools, not algorithms.** Describe outcomes and rules; let the host solve the mechanics with its standard tools (Glob, Grep, Read, Edit, Write, Bash). Do not specify search heuristics or matching algorithms.
- **Token-aware.** Any subagent or review loop is bounded, not free — the `--max-iterations=N` pattern (a default of one round, an explicit ceiling) used elsewhere in this plugin. State the default and the ceiling.
- **Compress.** Skill prose is caveman-dense (`${CLAUDE_PLUGIN_ROOT}/lib/caveman.md`): imperatives over full sentences, no filler, protected tokens verbatim. Prune no-ops — a line the model already obeys by default pays load to say nothing.

## Finished-skill checklist

- `name` matches the directory; `description` is a real trigger boundary, not a paraphrase of the body.
- Plugin-anchored: a bare action word does not fire it (or the broad-scope exception is deliberate and documented).
- The intro paragraph stands alone as help text.
- Every shared rule is referenced from `lib/`, not duplicated.
- Any loop is bounded with a stated default and ceiling.
- The prose is pruned: no no-ops, no restatements, protected tokens intact.
