---
name: agents-md
description: Create or optimize AGENTS.md / CLAUDE.md so an agent loads the minimum it needs and nothing misleading. User-invoked — /agents-md (repo), /agents-md --global, /agents-md <path>.
disable-model-invocation: true
---

# agents-md

Create lean, portable agent context files, or distill existing ones down to what
actually earns its place. The guiding belief: **every line in an always-loaded
context file is a recurring cost and an instruction-budget tax. Default to empty;
admit a line only when it pays for itself.**

This skill is **subtractive by default**. It removes and relocates far more often
than it adds. The only thing it always *adds* is one short authoritative block
(see Ground rules below).

---

## The architecture this skill produces

```
CLAUDE.md          # exactly `@AGENTS.md` (+ rare Claude-only lines). The bridge.
AGENTS.md          # minimal, portable, cross-tool. Always loaded. The canon.
AGENTS.d/          # on-demand docs this skill lifts out of AGENTS.md/CLAUDE.md.
docs/              # human docs — left alone; only pointed to, never moved into.
```

Why this shape:

- **Claude Code reads `CLAUDE.md`, not `AGENTS.md`.** It only sees AGENTS.md via
  the `@AGENTS.md` import. So the bridge is required, not cosmetic. A repo with
  only an AGENTS.md is invisible to Claude until the bridge exists.
- **AGENTS.md is the portable canon** every tool (Codex, Cursor, Copilot, Claude)
  can read. Project context lives here, not in CLAUDE.md.
- **`CLAUDE.md = @AGENTS.md`** via import, never a symlink (symlinks need admin on
  Windows and can't carry Claude-only lines without being torn down). Always write
  CLAUDE.md as a real file. If an existing CLAUDE.md is already a symlink to
  AGENTS.md, leave it — it works; don't clobber it.
- **`@`-import loads in full at launch — it is NOT progressive disclosure.** Use it
  only for `CLAUDE.md → AGENTS.md`. Everything on-demand uses plain relative links.

---

## The decision test (run on every line)

A line earns a place in an always-loaded file only if it passes **all five**:

1. **Universal** — true for every kind of session in this repo?
2. **Non-discoverable** — the agent cannot trivially derive it from code, config,
   or the file tree?
3. **Non-rotting** — no references to specific files, symbols, or implementation
   details that break when code changes?
4. **Stable fact, not preference/procedure** — preferences and multi-step
   procedures belong in a skill or in `AGENTS.d/`, not in the always-loaded file.
5. **Load-bearing** — would removing it cause a mistake the agent cannot recover
   from on its own?

Fail any → cut, or relocate. **Burden of proof is on removal as "discoverable":**
a line may be classified `CUT (discoverable)` only if you can cite the concrete
source ("build command is in `package.json` scripts.build"; "TypeScript is evident
from `tsconfig.json`"). No citation → classify `KEEP` or `ASK`, never a silent cut.
When in doubt about a hidden gotcha, KEEP and flag it. Be the kind of optimizer
that leaves behind something the user can trim, not one that deletes a landmine.

Never run `/init`-style generation. It produces exactly the bloated, redundant,
codebase-overview prose that degrades agent performance. Codebase overviews in
particular are wasted: agents explore faster than they read overviews.

---

## Invocation and target resolution

Explicit only. Three forms:

- `/agents-md` → current repo: the root `CLAUDE.md`/`AGENTS.md` (or
  `.claude/CLAUDE.md`). **Detect** nested `CLAUDE.md`/`AGENTS.md` in subdirectories
  and **report** them (and flag lines duplicated against the root), but only
  optimize the root unless a nested path is targeted explicitly.
- `/agents-md <path>` → that directory/file specifically (including a nested one).
- `/agents-md --global` → `~/.claude/CLAUDE.md`. See **Global mode** below.

### Mode detection (per targeted directory)

| State | Action |
| --- | --- |
| Neither file | CREATE: write `CLAUDE.md` = `@AGENTS.md` + a minimal `AGENTS.md` (floor = Ground rules section; see below). |
| Only `CLAUDE.md` | Move portable content → new `AGENTS.md`; rewrite `CLAUDE.md` to `@AGENTS.md` (+ any Claude-only residue). |
| Only `AGENTS.md` | ⚠️ Claude can't see it. Create `CLAUDE.md` = `@AGENTS.md`; optimize `AGENTS.md`. |
| Both | Optimize both; dedupe; portable CLAUDE.md content → AGENTS.md; CLAUDE.md shrinks to `@AGENTS.md` (+ residue). |

A nested directory that gets content follows the **same pair** (its own
`CLAUDE.md` = `@AGENTS.md` + `AGENTS.md`), because Claude won't read a nested
AGENTS.md without a nested bridge.

Running on an already-optimal target is a no-op — report "nothing to change."

---

## What goes where

**AGENTS.md** holds, and only holds:
- The `## Ground rules (authoritative)` block (always).
- Non-discoverable, universal facts (a `## Non-obvious` section) — e.g. "use `uv`,
  not `pip`"; a required env var; a build/test invocation not visible in config.
- A `## References` index: one line per on-demand doc, **"`path` — read when …"**.
  The index may point anywhere in the repo (`docs/`, `docs/adr/`, `AGENTS.d/`, a
  PRD), not just `AGENTS.d/`. The index is the spine of progressive disclosure.

**AGENTS.md never contains:** codebase overviews, discoverable commands, stack
descriptions, file-by-file maps, generic best practices, linter-enforced style,
or preferences.

**`AGENTS.d/`** (note the capitalization — mirrors `AGENTS.md`; keep it consistent,
since macOS is case-insensitive but Linux/CI is not) is the home for on-demand
content this skill (or another skill) lifts out of the always-loaded files and
that has no other natural home. **Invariant: every file in `AGENTS.d/` must have a
matching line in the AGENTS.md `## References` index** — without it there is no
auto-discovery and the file is invisible.

**`docs/` and domain/decision documents** (PRD, mission, vision, ADR, roadmap,
glossary) keep their own home. Two hard rules:
1. **Never duplicate.** Don't summarize an ADR or PRD into AGENTS.md — rot and
   duplication trap. Point, don't copy.
2. **Point, don't move (by default).** A `docs/` file with any human audience
   (linked from README, explanatory prose) stays in `docs/`; AGENTS.md just adds a
   "read when …" pointer. Only content with *no* human home belongs in `AGENTS.d/`.
   When you find a `docs/` file that looks purely agent-oriented, **propose** (in
   the end batch) moving it to `AGENTS.d/`, with full consequence analysis (every
   inbound link, e.g. `README.md:42`). If approved, move it **and rewrite every
   inbound reference** in the reconciliation pass — never a move that leaves a
   broken link.

**Claude-only residue in CLAUDE.md** defaults to empty. Three rules:
1. Claude-only + non-discoverable + universal + short → may sit as a line in
   CLAUDE.md under `@AGENTS.md`.
2. Claude-only but bulky/procedural (e.g. plan-mode workflow) → an `AGENTS.d/` file
   linked **from CLAUDE.md** (not from AGENTS.md — the portable file must not index
   Claude-specific things).
3. Claude-only but already covered by an installed skill → **delete**.

---

## Ground rules (the one standard rule this skill writes)

Write this block into **every** AGENTS.md the skill creates or optimizes, unless
the user explicitly says not to. It is the only opinionated thing the skill adds;
keep this standard set minimal. It lives per-project (not global) on purpose: a
collaborator who lacks the user's global config — and their agent — still gets the
protection, so nobody treats a stale README as authoritative.

```markdown
## Ground rules (authoritative)

These rules take precedence over any conflicting skill, README, or other guidance,
unless the user explicitly overrides them in the moment.

- Treat only this file, the files it references, and the actual code/state as
  authoritative. Do not rely on `README*` or other narrative docs unless they are
  referenced elsewhere in this file or the user explicitly points you to them.
```

The user may add their own pinned rules under this section. Anything in
`## Ground rules` is **authoritative/pinned** and changes how conflict detection
behaves (below).

---

## Canonical shape

**AGENTS.md is as short as possible.** Keep inline only what must be *always
loaded*: the Ground rules and genuinely non-obvious facts. The real test
is **always-needed vs situational**, not length — an always-needed universal fact
cannot move to `AGENTS.d/` (the agent might never read it on demand), so it stays
inline. Everything situational or elaborative becomes its own file in `AGENTS.d/`
with a one-line pointer in `## References`. **Never grow AGENTS.md with explanatory
paragraphs;** the only thing that grows is the index (one line per doc). If the
always-loaded part itself gets long, something in it is probably not universal —
re-test it.

The blocks below are **illustrative — never copy them literally.** Emit only lines
true for the target repo, use real values in place of `<…>`, and omit
`## Non-obvious` / `## References` entirely when they would be empty (never ship a
placeholder header).

CLAUDE.md is one line:

```
@AGENTS.md
```

AGENTS.md (floor = title + Ground rules; the two optional sections are shown only
to illustrate shape):

````markdown
# <project> — agent guide

## Ground rules (authoritative)

<the standard block verbatim — the single source of truth is the "Ground rules"
section above; do not reword it here>

## Non-obvious

Facts you need but cannot infer from the code, config, or file tree.
If it's discoverable, it doesn't belong here.

- <a required tool, service, env var, or convention — one per line>

## References

- `<path>` — read when <situation>
````

---

## Conflict and duplication detection (against skills)

This is the core of resolving "the skill said one thing, the context file another."

**Scan all installed skills** — project `.claude/skills/`, user `~/.claude/skills/`,
and plugin skills. Read every `description` first (cheap); for any skill whose
description overlaps a line/section in AGENTS.md/CLAUDE.md, deep-read its `SKILL.md`
to confirm.

**Trigger-coverage check (gate before any deletion):** a line may be removed as
"covered by a skill" only if the skill plausibly triggers in the contexts where
the line matters. Example: global coding standards vs a `coder` skill — the
standards only matter on code tasks, where `coder` triggers → safe to delete. A
rule that matters where the skill won't trigger → keep or relocate, don't delete.

Two outcomes, different severity:
- **Duplication** (context file says the *same* as a skill) → propose **deletion**
  from the context file, citing the skill ("covered by `coder`"). The skill is the
  better home: on-demand, no upfront budget cost.
- **Conflict** (context file says X, skill says not-X) → **default: the skill
  wins** — propose removing the line. Flag it prominently as a contradiction.

**Pinned override (inverts the default):** if the conflicting line is in
`## Ground rules (authoritative)`, the pinned rule wins instead. Never propose
deleting a pinned rule. Flag the other way: "skill X conflicts with a pinned rule —
the pinned rule wins; consider adjusting the skill."

Honesty about enforcement: precedence is **advisory**, not a hard engine. At
runtime, contradictory context "may be picked arbitrarily." The override works
because the Ground rules text *states* its precedence in visible prose. For hard
enforcement, tell the user they need a hook — out of this skill's scope.

---

## Global mode (`--global`)

`~/.claude/CLAUDE.md` is Claude-only; no other tool reads a global AGENTS.md, so
**there is no split globally** — the one exception to the `CLAUDE.md = @AGENTS.md`
rule. Keep it as a single Claude-only file and apply the decision test and conflict
detection **subtractively**: delete what a skill covers (with the trigger-coverage
check), keep what is genuinely universal *and* not skill-covered (e.g. a
"leave the machine state-neutral" working-environment rule). Do not add the Ground
rules block globally — it belongs per-project.

---

## Workflow (one autonomous pass, then one batch of questions)

1. **Inspect.** Read the targeted files; read `package.json`, config files, and the
   file tree to establish what is discoverable; enumerate installed skills; find
   nested context files and candidate docs (PRD/ADR/etc.).
2. **Classify everything you can** into: `KEEP` / `CUT (discoverable — cite source)`
   / `MOVE → AGENTS.d/` / `MERGE → AGENTS.md` / `DELETE (covered by skill — cite)` /
   `POINTER (add "read when…" to index)`. Decide the confident ones autonomously.
3. **Present the end package once:**
   - **(A) Confident changes** — the classification, each with rationale and cited
     source.
   - **(B) Batched questions** (use `AskUserQuestion`, all at once) — only the
     genuinely undecidable: fuzzy overlaps, "read when …" conditions that need the
     user's domain knowledge, proposed `docs/ → AGENTS.d/` moves, proposed PRD/ADR
     pointers.
   Never ask questions mid-flow.
4. **Answering the batch is approval** for the whole package. Run a
   **reconciliation pass** to apply downstream consequences of the answers (e.g.
   rewrite inbound links for an approved move). If reconciliation changes anything
   *outside* what was already shown, preview that delta and confirm before writing.
5. **Write, then report** what changed and why.

---

## Safety

Git-aware, asymmetric:
- **In a git repo:** no backup — git is the safety net. Write, then tell the user
  to review/commit. Warn if the target files already have uncommitted changes (keep
  the diff clean).
- **Not in git:** write only after showing the full before/after (the batch answers
  are the gate). No `.bak` files by default — they're clutter.
- **The global file (`~/.claude/CLAUDE.md`):** irreplaceable and rarely in git —
  default to writing one timestamped backup (`~/.claude/CLAUDE.md.bak-<date>`) and
  tell the user exactly where it is so they can delete it. Backup default-on for
  the global file only.

---

## Edge cases

- Existing `CLAUDE.md` symlinked to `AGENTS.md`: leave it; it already works.
- `.claude/CLAUDE.md` location: detect and respect it instead of `./CLAUDE.md`.
- `CLAUDE.local.md`: leave untouched unless explicitly targeted (personal,
  gitignored).
- Nested files in a monorepo: report and flag root-duplication; only optimize when
  targeted (`/agents-md <path>`). Mention `claudeMdExcludes` if other teams' files
  are noise.
