---
name: fabulous
description: Toggle the fabulous working mode — the session's agent orchestrates, subagents execute. `/fabulous` toggles; `--on`, `--off`, `--status`.
disable-model-invocation: true
---

# fabulous

While ON, the agent orchestrates — understands, plans, decides, briefs, verifies — and subagents execute. State lives in `~/.claude/fabulous.json`, so the mode survives sessions. The skill never switches model or effort and never suggests it — running `/model` and `/effort` (Fable at high effort while ON, the noted values to restore) is the user's own move, assumed known.

## The argument decides the mode

| Invocation | Effect |
| --- | --- |
| `/fabulous` | Toggle: ON if the state file says off or is absent, else OFF. |
| `/fabulous --on` | Force ON. Already ON → re-assert the working mode; keep the noted model/effort untouched. |
| `/fabulous --off` | Force OFF. Already OFF → say so; change nothing. |
| `/fabulous --status` | Report ON/OFF and the noted model/effort. Changes nothing. |

Bare `on` / `off` / `status` work too; a natural-language "is it on?" is `--status`.

## State file

`~/.claude/fabulous.json` — missing file means OFF:

```json
{ "active": true, "previousModel": "<alias or full name>", "previousEffort": "<low|medium|high|xhigh|max>" }
```

## ON

1. **Note** — skip when the file already says `active: true` (a re-assert run). Model: from your own session context. Effort: `CLAUDE_CODE_EFFORT_LEVEL`, else `effortLevel` in `.claude/settings.local.json`, then `.claude/settings.json`, then `~/.claude/settings.json`, else omit it. Write the state file: `active: true` plus the noted values.
2. **Adopt** "The working mode" below as a standing instruction for every subsequent turn until OFF.
3. Confirm ON in one line — nothing else.

## OFF

1. Read the state file. Already OFF → say so, stop.
2. Drop the standing instruction; write `{ "active": false }`.
3. Confirm OFF in one line naming the values just cleared — nothing else.

## The working mode

While ON, on every task:

- **You think.** Understand the task, read what your decisions require (reading for your own decision-making is always allowed), decide the solution, write the brief. Verify the result and synthesise the answer yourself, whoever executed.
- **Subagents execute.** Ladder `haiku` < `sonnet` < `opus` < `fable`: delegate to the lowest model you judge able to do the job, never one stronger than your own (haiku picks haiku; sonnet picks haiku–sonnet; opus picks haiku–opus; fable picks any).
- **Do it yourself** only when your own spend (weighted by your model's quota multiplier — Fable draws 2×) is judged smaller than delegation's total: brief + the agent's fresh-context reading + report. Typical case: a change already specified character for character, where the brief would contain the whole change anyway.
- **When in doubt: delegate.**

Pure skill, no hook: the directive can fade in a long or compacted session and is absent in a fresh one even with state ON — `/fabulous --on` re-asserts it safely.
