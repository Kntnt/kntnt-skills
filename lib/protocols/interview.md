# Interview protocol

The shared way `skill-maker` and `plugin-maker` reach a design before they build: interview the user relentlessly, one question at a time, until every load-bearing decision is settled. This file is the *how*; the calling skill supplies the *what* (its own list of decisions to walk).

## Foundation

This protocol stands on Matt Pocock's grilling skill, vendored verbatim at `${CLAUDE_PLUGIN_ROOT}/lib/vendor/matt-pocock/grilling/SKILL.md`. **Read that file first** — it is the core behaviour. Everything below is the Kntnt layer on top of it.

## The loop

- **One question at a time.** Ask a single question, wait for the answer, then ask the next. Asking several at once is bewildering and breaks the dependency ordering.
- **Recommend an answer.** Every question carries your recommended answer and the reason for it. The user is deciding, not doing your thinking — make the default decision easy to accept or correct.
- **Walk the design tree.** Resolve decisions in dependency order: settle the question that unblocks the most downstream choices before the choices that depend on it. Name the dependency when it matters ("this determines the templates, so we settle it first").
- **Record as you go.** After each answer, restate the settled decision in one line so the growing design stays visible and the user can catch a drift early.

## Adapt to the plan's richness

The user's starting plan ranges from a bare name to a detailed specification. Match the interview to it:

- **Thin plan → grill hard** from first principles. Few decisions are made, so most of the tree is open.
- **Detailed plan → confirm and probe gaps.** Treat what the plan states as settled; spend questions only on what it leaves open, on contradictions, and on consequences the user may not have seen.
- **Never re-ask what the plan already answers.** Re-asking signals you did not read it.
- **Explore before asking.** If a question can be answered by reading the filesystem, the existing repo, or installed skills, read them instead of asking. Ask the user only what the artifacts cannot tell you.

## The stop-threshold

Stop interviewing when **every load-bearing decision is either resolved or explicitly deferred with a sensible default recorded** — not when every conceivable detail is nailed down. A decision is load-bearing when getting it wrong forces a rebuild; trivia that one edit can fix later is not.

Bias the whole interview toward *recommend-and-confirm* so a decisive user can move fast: a strong recommendation the user can wave through is worth more than an open-ended question. When the threshold is met, synthesise the design in one consolidated view, confirm it, and **then** build — do not drift on asking once understanding is shared.

## Supplying a question domain

The calling skill provides the list of decisions to walk — its *question domain*. This protocol provides the loop, the adaptivity, and the stop-threshold. `skill-maker` walks one skill's decisions; `plugin-maker` walks the plugin's decisions and then hands each skill to `skill-maker`, which walks the skill-level domain — so a multi-skill build feels like one continuous interview because every leg runs this same protocol.
