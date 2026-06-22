---
name: skill-maker
description: Author one complete skill to the Kntnt standard — interview the user, apply Matt Pocock's skill-writing craft and Kntnt's house conventions, then write the SKILL.md (and any lib/ it needs). User-invoked — /skill-maker or /kntnt-skills:skill-maker, optionally with a name or plan. Not triggered by a bare "make a skill". Used standalone, or by plugin-maker for each skill in a new plugin.
disable-model-invocation: true
---

# skill-maker

Author one complete, on-standard skill from a plan that can be anything from a bare name to a detailed specification. The skill interviews you to settle every load-bearing decision, then writes a `SKILL.md` (and any shared `lib/` it needs) that follows Matt Pocock's craft for predictable skills and Kntnt's house conventions on top. It builds a single skill; to scaffold a whole plugin around one or more skills, use `/plugin-maker`, which drives this skill for each one.

## Read first, every run

These three files are the source of truth — read them before interviewing or writing. Subagents do not auto-load them; when authoring through a subagent, paste their content into its prompt.

1. `${CLAUDE_PLUGIN_ROOT}/lib/vendor/matt-pocock/writing-great-skills/SKILL.md` and its `GLOSSARY.md` — the general craft: predictability, leading words, information hierarchy, progressive disclosure, pruning, failure modes.
2. `${CLAUDE_PLUGIN_ROOT}/lib/skill-conventions.md` — the Kntnt house conventions. **Where the two conflict, this one wins.**
3. `${CLAUDE_PLUGIN_ROOT}/lib/protocols/interview.md` — how to run the interview.

## Process

1. **Locate the target.** Decide where the skill lands: which plugin and which `skills/<name>/` directory. Standalone, that is the current plugin (or one named in the plan); under `plugin-maker`, it is the plugin being built. The directory name is the skill's `name`.

2. **Interview.** Run `lib/protocols/interview.md` with the skill-level question domain from `skill-conventions.md`: purpose and **leading word**; **invocation type** (model-invoked vs `disable-model-invocation`); the **trigger boundary** (what fires it, what must not); **shape** (steps vs reference vs both) and **completion criteria**; **progressive disclosure** (inline vs `lib/`/sibling files); shared `lib/` modules it reads. Adapt to the plan's richness — confirm what the plan states, grill the gaps — and stop when every load-bearing decision is settled.

3. **Author.** Write `skills/<name>/SKILL.md` per `skill-conventions.md`: frontmatter (`name`, a `description` that is a real trigger boundary, `disable-model-invocation` only for typed-only utilities), the H1, then the **intro paragraph that doubles as the `/help` text** (self-contained, no leading heading or fragment), then the body. Put any shared rule in `lib/` and reference it as `${CLAUDE_PLUGIN_ROOT}/lib/…` rather than inlining it twice. Compress to caveman density (`${CLAUDE_PLUGIN_ROOT}/lib/caveman.md`).

4. **Verify.** Run the finished-skill checklist in `skill-conventions.md`: name matches the directory; the description is a trigger boundary, not a paraphrase; a bare action word does not fire it (unless the broad-scope exception is deliberate and documented); the intro stands alone as help; no rule is duplicated out of `lib/`; any loop is bounded; the prose is pruned of no-ops.

5. **Report.** Name the file(s) written and the key decisions (invocation type, trigger boundary, shape). Standalone, remind the user that if this skill joined an existing plugin, the plugin-level wiring (`CHANGELOG`, README skill list, `marketplace.json`, any new `audit` check) still needs updating — or to run `/plugin-maker` in the plugin for the augment flow that does it.

## Invocation

- `/skill-maker` — interview from scratch.
- `/skill-maker <name or plan>` — seed the interview with a name or a fuller plan; the richer the plan, the fewer questions.

When `plugin-maker` calls this process for each skill of a new plugin, steps 1 and 5 are handled by `plugin-maker` (it sets the target and owns the plugin-level wiring); this skill's job there is steps 2–4 per skill.
