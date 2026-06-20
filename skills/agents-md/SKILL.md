---
name: agents-md
description: Create, shrink, or delete AGENTS.md / CLAUDE.md so an agent loads the fewest possible tokens and nothing misleading. Aggressively minimizes always-loaded context — writes nothing when nothing earns a place, compresses what stays, splits the rest into small on-demand agents.d/ files. User-invoked — /agents-md (repo), /agents-md <path>, /agents-md --global, --max-iterations=N, --no-claude-md, --only-claude-md.
disable-model-invocation: true
---

# agents-md

Express what an agent genuinely needs from `CLAUDE.md` / `AGENTS.md` / `agents.d/` in
the fewest tokens possible — and write nothing it doesn't need. Every token in an
always-loaded file is paid on **every** session forever, and dilutes the instructions
that matter. So the bar is brutal and the default is **nothing**.

Two independent failures to attack — most runs commit one or both:

- **Existence.** A file (or line) that carries no load-bearing, non-discoverable
  fact should not exist. Creating an AGENTS.md just to have one is a regression.
- **Expression.** A fact worth keeping, written in 40 words when 8 suffice, wastes
  the other 32 every session. **Relocating verbose prose into `agents.d/` is not a
  win** — the tokens still exist; an on-demand read still pays them. The win is
  fewer tokens, period: hardest in the always-loaded file, but also in total.

This skill is subtractive and compressive. It deletes, compresses, and splits far
more than it adds.

---

## The shape

```
CLAUDE.md     # exactly `@AGENTS.md`. Nothing else. The bridge Claude Code needs.
AGENTS.md     # always-loaded canon. The few facts EVERY session ALWAYS needs.
agents.d/     # many small on-demand files, one concern each. Loaded only when needed.
docs/         # human docs. Pointed to, never copied into.
```

Why this shape:

- **Claude Code reads `CLAUDE.md`, not `AGENTS.md`** — it only sees AGENTS.md via
  the `@AGENTS.md` import. A repo with only AGENTS.md is invisible to Claude. So the
  bridge is required. Write it as a real file (not a symlink — symlinks need admin
  on Windows); if an existing CLAUDE.md is already a symlink to AGENTS.md, leave it.
- **`@`-import loads in full at launch — NOT progressive disclosure.** Use it only
  for `CLAUDE.md → AGENTS.md`. Everything on-demand uses plain relative links from
  the References index, which the agent follows only when a task needs them.
- **AGENTS.md is the portable canon** every tool (Codex, Cursor, Copilot, Claude)
  reads. Project context lives here, not in CLAUDE.md.

---

## Three gates

Run every candidate fact through these in order. Most material dies at gate 1 or 2;
whatever survives is squeezed at gate 3.

### Gate 1 — Should anything exist at all?

A fact earns a place in an always-loaded file only if it passes **all five**:

1. **Universal** — true for every kind of session in this repo.
2. **Non-discoverable** — the agent cannot trivially derive it from code, config, or
   the file tree.
3. **Non-rotting** — no reference to a specific file/symbol/line that breaks when
   code changes.
4. **Stable fact, not preference/procedure** — preferences and multi-step procedures
   belong in a skill or an `agents.d/` file, not the always-loaded file.
5. **Load-bearing** — removing it causes a mistake the agent cannot recover from on
   its own.

**If nothing passes, create nothing.** A repo whose every fact is discoverable from
its code, config, and an accurate README does not need AGENTS.md or CLAUDE.md — and
must not get them. The Ground rules block alone is **not** sufficient reason to
create the pair (see Ground rules below).

**Delete files that fail this gate.** If an existing CLAUDE.md/AGENTS.md carries
nothing load-bearing — boilerplate, a codebase overview, restated README, discoverable
commands — propose deleting it outright, not "optimizing" it down to a stub. An empty
authoritative file is still an always-loaded cost and a thing to maintain.

**Burden of proof is on removal-as-discoverable.** Classify a line `CUT (discoverable)`
only with a cited source ("build cmd in `package.json` scripts.build"; "TS evident from
`tsconfig.json`"). No citation → `KEEP` or `ASK`, never a silent cut. When unsure about
a hidden gotcha, KEEP and flag it. Be the optimizer that leaves a landmine-free file the
user can trim further — not one that deletes a landmine.

Never run `/init`-style generation. It produces exactly the bloated codebase-overview
prose that degrades agents. Agents explore faster than they read overviews.

### Gate 2 — Where does each surviving fact live?

- **Always-needed by every session → inline in AGENTS.md.** It can't go on-demand
  because the agent might never load it. This is the only thing that stays inline.
  Keep this set tiny.
- **Situational / elaborative / procedural → its own `agents.d/` file**, with a
  one-line pointer in the References index. Default here, not inline.
- **Has a human audience already (PRD, ADR, design doc, glossary) → leave in `docs/`**,
  add only a "read when…" pointer. Never summarize it into AGENTS.md (rot + dup trap):
  point, don't copy. Propose a `docs/ → agents.d/` move only for a doc with *no* human
  audience, and if approved, rewrite every inbound link in the same pass.

The always-loaded set is **always-needed vs situational**, not short-vs-long. If the
inline part grows past a handful of facts, something in it is situational — retest it.

### Gate 3 — Express it in the fewest tokens

Everything written — inline facts, `agents.d/` files, References lines — is compressed
to caveman density (rules in `lib/caveman.md`). A fact kept is a fact stripped to its load-bearing
core. This is the gate the photo-drop run skipped: it moved 14 KB of prose into
`agents.d/` almost verbatim and the total grew. Compression is mandatory, not optional.

---

## Compression (caveman) rules

The shared definition lives in `${CLAUDE_PLUGIN_ROOT}/lib/caveman.md` — the caveman
core (CUT / KEEP / VERBATIM, "correctness beats brevity", language-agnostic). It governs
gate 3. Read it. **Subagents do not auto-load it** — read the file and paste its content
into each build subagent's prompt.

This skill writes one genre — terse agent-facing instruction Markdown — so on top of the
shared core it adds two context-file specializations:

- **Convert prose to imperatives.** Full sentences → fragments and imperatives ("Run
  tests before push"). Drop instruction-subjects — `you should X` / `remember to X` /
  `make sure to X` → `X`.
- **Before → after** (the density expected here):
  - "This plugin is currently in pre-1.0 development, and as long as the major version
    is 0, no decision should factor in backwards compatibility." → "Pre-1.0 (major `0`):
    ignore backwards-compat. No deprecations, no migrations."
  - "You should clone the reference repository next to this one and read it as the
    template before you write any code." → "Before coding, clone `<repo>` as template:
    `git clone … /tmp/<repo>`."

Everything else — what to drop, what to keep verbatim, never dropping a load-bearing
qualifier — is in `lib/caveman.md` and is not restated here.

---

## CLAUDE.md is exactly `@AGENTS.md`

One line, nothing else:

```
@AGENTS.md
```

No meta-notes ("keep this minimal…"), no Claude-only prose — those are themselves
always-loaded waste. If a fact is genuinely Claude-only and load-bearing, it goes in
AGENTS.md (portable files may carry a clearly-marked Claude note) or, if bulky, an
`agents.d/` file linked from CLAUDE.md. A Claude-only rule already covered by an
installed skill is deleted. Two exceptions to this `@AGENTS.md`-only rule: global mode
(below) and `--only-claude-md` (Invocation), which both put the canon directly in
CLAUDE.md with no AGENTS.md and no `@`-import.

---

## Ground rules (conditional, not automatic)

When AGENTS.md exists **for other reasons**, and the repo has narrative docs (README
etc.) an agent could wrongly treat as authoritative, add this block — compressed:

```markdown
## Ground rules (authoritative)

Precedence over any conflicting skill, README, or other doc unless the user overrides
in the moment.

- Authoritative: only this file, the files it references, and the actual code/state.
  Ignore `README*` and other narrative docs unless referenced here or pointed to.
```

It is **never the sole reason to create the pair** — that was the old mistake. The user
may add pinned rules under it; anything in `## Ground rules` is authoritative and
inverts conflict detection (below).

---

## agents.d/ — many small files, not few big ones

Granularity is a token lever. One concern per file (`releasing.md`, `toolchain.md`,
`testing.md`), so a task loads only what it needs and pays for nothing else. A task
cutting a release should not also load the test matrix. Prefer several 5–15-line files
over one 60-line file. Each file: a one-line "read when…" top line, then compressed
content. Directory name is lowercase `agents.d/` (the Unix `.d` convention); keep it
exact — Linux/CI is case-sensitive, and the References links must match.

**Invariant:** every file in `agents.d/` has a matching line in the AGENTS.md References
index. No index line → no discovery → invisible file. The index is the spine of
progressive disclosure.

---

## Canonical output

CLAUDE.md: the one line above. AGENTS.md floor is the title; the two sections appear
only when non-empty (never ship a placeholder header). Illustrative — emit only what is
true for the repo, compressed:

````markdown
# <project> — agent guide

## Ground rules (authoritative)
<the conditional block, only when warranted>

## Non-obvious
<facts no session can infer from code/config/tree — one compressed line each>
- use `uv`, not `pip`
- `<env var>` required for <thing>

## References
- `<path>` — read when <situation>
````

---

## Build + critical-review loop (subagents)

When there **is** content to write or compress (more than a trivial one-liner),
produce it through an adversarial loop rather than writing it yourself in one pass —
self-review in the same context converges on cosmetic edits and calls verbose prose
done. `--max-iterations=N` (default **2**) bounds it: N = max passes per job — one
build + up to N−1 critical send-backs. N=2 → one send-back; N=1 → accept the first
build. N is honoured as given (floor 1, no hard cap); but N>3 rarely pays off on
context files, so when N>3, warn the user (diminishing returns, rising token cost) and
confirm before running the loop.

1. **Plan.** Decide the file set: the AGENTS.md inline facts, the `agents.d/` split
   (one concern per file), the References index. This is gate 1/2 work — do it yourself.
2. **Build.** Spawn a subagent per file (independent files run in parallel), each given
   the source material, the contents of `lib/caveman.md` plus this skill's imperative-
   genre additions, and "return file content only, caveman-
   compressed, protected tokens intact."
3. **Critique.** Review each returned draft adversarially against: every line passes
   gate 1; caveman-compressed (no articles/filler/hedging; fragments; protected tokens
   verbatim); right granularity (one concern, not a dumping ground); token count down
   vs source. Assume it is too verbose until it reads stripped.
4. **Send back** any draft that fails, with specific notes ("still full sentences in
   §2; split releasing+toolchain"), until it passes or the iteration ceiling is hit.
5. **Write, measure, report** (below).

For a tiny change (delete a stub, fix one line, drop one section), skip the loop and do
it directly. The loop scales with the work.

---

## Conflict & duplication detection (vs skills)

Scan installed skills — project `.claude/skills/`, user `~/.claude/skills/`, plugins.
Read each `description` (cheap); deep-read a `SKILL.md` only when its description
overlaps a line in AGENTS.md/CLAUDE.md.

**Trigger-coverage gate before any delete:** remove a line as "covered by a skill" only
if the skill plausibly triggers where the line matters. Global coding standards vs a
`coder` skill that triggers on code tasks → safe to delete. A rule that matters where
the skill won't fire → keep or relocate.

- **Duplication** (file says the same as a skill) → propose delete, cite the skill
  ("covered by `coder`"). The skill is the better home: on-demand, zero upfront cost.
- **Conflict** (file says X, skill says not-X) → **skill wins by default**; propose
  removing the line, flag the contradiction.
- **Pinned override:** a conflicting line in `## Ground rules` wins instead — never
  propose deleting it; flag the skill for adjustment.

Precedence is advisory, not enforced: at runtime contradictory context may be picked
arbitrarily. The Ground rules text works by *stating* its precedence in prose. Hard
enforcement needs a hook — out of scope; tell the user.

---

## Invocation & modes

Explicit only:

- `/agents-md` → current repo root (`CLAUDE.md`/`AGENTS.md`, or `.claude/CLAUDE.md`).
  Detect and report nested context files (flag root-duplication); optimize only the
  root unless a nested path is targeted.
- `/agents-md <path>` → that directory/file (including a nested one).
- `/agents-md --global` → `~/.claude/CLAUDE.md` (see Global mode).
- `--max-iterations=N` → build-loop ceiling (default 2).
- `--no-claude-md` → write only `AGENTS.md`, no `CLAUDE.md` bridge. For repos read by
  AGENTS.md-native tools (Codex, Cursor) where you keep CLAUDE.md yourself. **Trade-off:
  Claude Code won't auto-load AGENTS.md without the bridge** — state this in the report.
- `--only-claude-md` → write a single `CLAUDE.md` holding the canon directly (not
  `@AGENTS.md`); no AGENTS.md, no bridge. Claude-only: trades cross-tool portability for
  one fewer file.

The two file-shape flags are mutually exclusive — reject if both are given. Neither
applies to `--global` (already CLAUDE.md-only). They change nothing but the always-loaded
filename and the bridge — gates, compression, `agents.d/`, and the References index are
identical: default = AGENTS.md + `@AGENTS.md` bridge; `--no-claude-md` = AGENTS.md alone;
`--only-claude-md` = CLAUDE.md alone (content inline). In the mode table below, read
"`CLAUDE.md`=`@AGENTS.md` + AGENTS.md" as the always-loaded file the active flag selects.

**Mode detection per targeted directory:**

| State | Action |
| --- | --- |
| Neither file | If gate 1 yields facts → create `CLAUDE.md`=`@AGENTS.md` + compressed AGENTS.md. **If gate 1 yields nothing → create nothing; report why.** |
| Only `CLAUDE.md` | Move portable content → AGENTS.md; `CLAUDE.md` → `@AGENTS.md`. If nothing survives gate 1 → propose deleting both. |
| Only `AGENTS.md` | Claude can't see it. Add `CLAUDE.md`=`@AGENTS.md`; compress AGENTS.md. |
| Both | Compress both; dedupe; CLAUDE.md → `@AGENTS.md`. Delete either if it fails gate 1. |

A nested directory that warrants content gets its own pair (Claude won't read a nested
AGENTS.md without a nested bridge). An already-optimal target is a no-op — say so.

---

## Global mode (`--global`)

`~/.claude/CLAUDE.md` is Claude-only; no other tool reads a global AGENTS.md, so there
is no split — keep it a single Claude-only file (the one exception to `CLAUDE.md =
@AGENTS.md`). Apply gates 1 and 3 and conflict detection subtractively: delete what a
skill covers (trigger-coverage gate), compress what stays, keep only what is universal
*and* not skill-covered (e.g. "leave the machine state-neutral"). No Ground rules block
globally — it is per-project.

---

## Measure & report

Token reduction is the deliverable, so measure it. Report, for the always-loaded set
(CLAUDE.md + AGENTS.md) and for the total (incl. agents.d/), the before/after size —
words or chars, a quick `wc -w` is fine:

```
always-loaded: 2180w → 240w   (-89%)
total:         2180w → 760w   (-65%)
```

**If total went up, the run failed** — content was relocated, not compressed. Go back
to gate 3. Then list what was deleted, compressed, split, and pointed-to, each with its
reason (cite sources for discoverable cuts).

---

## Safety

Git-aware, asymmetric:

- **In git:** no backup — git is the net. Write, tell the user to review/commit. Warn
  if targets already have uncommitted changes (keep the diff clean). Deletions are
  recoverable from git, so deleting a worthless file is safe — but still report it.
- **Not in git:** write/delete only after showing the before/after. No `.bak` clutter.
- **Global file (`~/.claude/CLAUDE.md`):** irreplaceable, rarely in git — write one
  timestamped backup (`~/.claude/CLAUDE.md.bak-<date>`) and tell the user where, so
  they can delete it. Backup default-on for the global file only.

---

## Edge cases

- CLAUDE.md symlinked to AGENTS.md: leave it; it works.
- `.claude/CLAUDE.md` location: detect and respect instead of `./CLAUDE.md`.
- `CLAUDE.local.md`: leave untouched unless explicitly targeted (personal, gitignored).
- Monorepo nested files: report, flag root-duplication; optimize only when targeted.
  Mention `claudeMdExcludes` if other teams' files are noise.
