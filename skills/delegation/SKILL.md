---
name: delegation
description: Turn delegation mode on or off — the agent orchestrates, subagents execute — for this session, this project or your user account. `/delegation`; scopes `--user`, `--project`; states `--on`, `--off`, `--status`.
disable-model-invocation: true
---

# delegation

Turn delegation mode on or off: while it is on, the agent orchestrates — thinks, plans, briefs, verifies — and subagents execute on the cheapest model judged able to do the job. `/delegation` toggles it for the current session; `--on` and `--off` force a state, and `--status` reports all three scopes. Add `--user` or `--project` to make it standing: the skill writes the instruction as a managed block into the context file your agent already loads — your global `CLAUDE.md` for `--user`, the project's own for `--project`, which is normally committed, so everyone who clones the repo gets the mode too. It shows you the target file and the exact insertion and waits for your yes before writing anything. The skill never switches your model or effort and never suggests it — running `/model` and `/effort` is your own move.

## What the mode says

`${CLAUDE_PLUGIN_ROOT}/lib/delegation-mode.md` — the single source of truth, copied verbatim into every managed block. Read it; never restate or paraphrase it.

## Semantics

- **ON** — delegation **must** happen as `lib/delegation-mode.md` says.
- **not ON** — delegation **may** happen; judge for yourself, exactly as with the plugin uninstalled.

No third state. This skill only ever *adds* a standing instruction, never suppresses your own judgement. Sole exception: session `--off`, which suspends **this plugin's own** instruction for the current session; it does not forbid delegation in general.

## Command surface

| Invocation | Effect |
| --- | --- |
| `/delegation` | Toggle **for this session**. Session is the only togglable scope. |
| `/delegation --on` \| `--off` | Force the session state. |
| `/delegation --user --on` \| `--off` | Write / remove the block in the host's global context file (confirm first), and adopt / suspend for this session immediately. |
| `/delegation --project --on` \| `--off` | Same for the project, with the shared-repo warning in the confirmation. |
| `/delegation --status` | Report all three scopes, the verdict, any staleness. |
| `/delegation --user` \| `--project` `--status` | Report that scope alone. |
| `/delegation --user` \| `--project` with no state flag | Incomplete. Change nothing, say what is missing, ask for `--on` or `--off`. |

- **Persistent scopes never toggle.** Flipping a file in `~/.claude`, or a committed file in a shared repo, off an inferred current state is the wrong default. `--user` and `--project` take `--on`, `--off` or `--status`, never a bare toggle.
- **No scope flag means session — except `--status`**, which then covers all three scopes. Deliberate, not a bug.
- **Bare words work, order does not matter.** `user`, `project`, `session`, `on`, `off`, `status` are mutually distinct: `/delegation user on`, `/delegation --user on`, `/delegation --user --on` and `/delegation --on --user` are all valid.
- **Natural language stays narrow.** Only "is it on?" → `--status`. Refuse anything vaguer rather than guess — "turn it on everywhere" versus "for this project" is exactly the guess that writes the wrong file.
- **Conflicting flags change nothing**: two scope flags, two state flags, or a state flag with `--status` → name the ambiguity, ask which was meant.
- **Mutations confirm in one line**, naming the scope's new state and the effective state, and calling out any disagreement between them.
- **Never switch model or effort, never suggest it.** `/model` and `/effort` are the user's own move. `/status` reports what they have now, so it answers "what do I restore to?" only when consulted **before** switching.

## Where each scope lives

| Scope | State |
| --- | --- |
| session | The conversation, plus `kntnt-skills-delegation.json` in the session's scratchpad directory (the path named in the system prompt), so `--status` survives a compaction. Content: `{ "active": true }` or `{ "active": false }`, nothing else. No scratchpad → conversation only. |
| project | The managed block in the project's context file. |
| user | The managed block in the host's global context file (`~/.claude/CLAUDE.md` for Claude Code), created if absent. No `AGENTS.md`, no `agents.d/`, no include — there is no cross-agent global convention. |

## How the mode takes effect

- **Session scope.** `--on` (or a toggle to on): read `${CLAUDE_PLUGIN_ROOT}/lib/delegation-mode.md`, adopt it as a standing instruction for the rest of the session, write `{ "active": true }`. `--off`: write `{ "active": false }` and treat the instruction as inert history — execute tasks yourself again, spawn subagents only when the user asks. Nothing curated is written at this scope, so nothing to confirm.
- **Persistent scopes.** The block in the context file **is** the standing instruction; the host loads it at session start. `--user --on` and `--project --on` additionally adopt it for the current session exactly as session `--on` does, so the mode does not wait for a restart. `--user --off` and `--project --off` likewise suspend it here and now.

## The managed block

Every persistent scope writes exactly this:

```markdown
<!-- kntnt-skills:delegation -->
<!-- Managed block. Do not edit by hand — run /delegation to change or remove it. -->
{the entire content of lib/delegation-mode.md, verbatim}
<!-- /kntnt-skills:delegation -->
```

- **Placement: last in the file**, one blank line from what precedes it, whatever the file contains — including after a `## References` index. One rule for every scope and host: no parsing, no heading to find, exact removal.
- **`--off` removes the whole block**, markers included, and nothing else.
- **`--on` over an existing block rewrites it** from the current `lib/delegation-mode.md`. So `--on` is idempotent and doubles as the refresh command.
- **Stale** = the lines between the managed-block comment and the closing marker differ from `${CLAUDE_PLUGIN_ROOT}/lib/delegation-mode.md`. `--status` reports it and names `/delegation <scope> --on` as the fix.
- **Two blocks in one file, or a marker without its pair**: change nothing, report, ask.

## Target file

**Binding constraint: the block must land in a file this host loads automatically in every session at that scope.** Claude Code does not read a project `AGENTS.md` unless a `CLAUDE.md` imports it; writing the block into an unbridged `AGENTS.md` yields a confirmed "on" and a mode that does not exist. You need not *detect* which host you are — you *are* the host; resolve the target yourself.

Project scope, in order:

1. The host already loads an agent-agnostic `AGENTS.md` (directly, or via a bridge such as a `CLAUDE.md` containing `@AGENTS.md`) → write to `AGENTS.md`.
2. `AGENTS.md` exists but this host does not load it → propose creating the bridge (Claude Code: `CLAUDE.md` containing exactly `@AGENTS.md`) in the same confirmed write, then write to `AGENTS.md`.
3. No `AGENTS.md`, but the host has its own project file (`CLAUDE.md`, `GEMINI.md`, …) → write there.
4. No context file at all → create the house pair: `AGENTS.md` with the title line `# <project> — agent guide` then the block, plus the host's bridge. Both files named in one confirmation. The user has asked for a standing instruction in as many words, so this is not `agents-md`'s "create nothing" case.

User scope: the host's global context file, created if absent.

## Project scope is shared, by construction

`AGENTS.md` and `CLAUDE.md` are committed in most repos, and a marker block inside them cannot be gitignored. Project scope therefore puts every clone of the repo in delegation mode, and every non-Claude agent that reads `AGENTS.md` gets the block too. Accepted, but **made visible**: the project-scope confirmation says in as many words that the file is normally committed and that everyone cloning the repo will get the mode.

## Confirmation

`--user` and `--project` show the exact target file, the exact insertion, and the bridge file when one must be created, then wait for a yes. Not because the write is dangerous, but because these files are hand-curated. Confirmation also absorbs any ambiguity in target selection: a wrong guess is redirected in one word before anything is written.

One guard on top: at project scope, when the target file already has uncommitted changes, say so, so the block is not mixed into work in progress. No backup file, in git or out — `--off` is an exact undo of `--on`, and project scope works outside git too.

## Precedence and `--status`

- User and project scope write the **identical** block, so there is no user-versus-project conflict. Either present means on.
- A session instruction given in this conversation (`/delegation --on` or `--off`) beats any standing block.
- **Verdict** = the session instruction if one was given this session; otherwise on if and only if the block is present in a file this host loads here.

Session `--off` **suspends obedience; it does not remove text from the context window.** The tokens are still paid, and after a compaction the standing block survives while the session instruction may not — so re-run `/delegation --off` if the agent starts delegating again.
