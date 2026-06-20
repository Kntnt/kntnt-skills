---
name: caveman
description: Apply caveman compression (maximum meaning per token, no loss of facts, code, numbers or register) to all of this agent's output, or one-shot to a given text or file. User-invoked — /caveman or /caveman --on (compress all output from now on), /caveman --off (stop, resume normal output), /caveman <ref> (one-shot a single file by path/URL/name/description, or inline text pasted below), /caveman --file=<path> (one-shot an explicit file). The one-shot forms never change the on/off state. Shares its definition of "caveman" with agents-md via lib/caveman.md.
disable-model-invocation: true
---

# caveman

Apply caveman compression — maximum meaning per token, zero meaning lost — to this agent's output, or to a text you point at. *What* caveman is lives in `${CLAUDE_PLUGIN_ROOT}/lib/caveman.md`; this skill only decides *where* to apply it. Read that file first, every run.

## The argument decides the mode

| Invocation | Mode | Effect |
| --- | --- | --- |
| `/caveman` or `/caveman --on` | ON | Compress all your output from now on. |
| `/caveman --off` | OFF | Stop. Resume normal output. |
| `/caveman <ref>` | one-shot | Compress what `<ref>` points to. Does **not** change ON/OFF. |
| `/caveman --file=<path>` | one-shot | Compress that file. Does **not** change ON/OFF. |

`--on` / `--off` and a one-shot (`<ref>` or `--file=`) are mutually exclusive. If both are given, do neither — say so and ask which was meant.

## ON — `/caveman`, `/caveman --on`

Read `${CLAUDE_PLUGIN_ROOT}/lib/caveman.md`. Adopt it as a **standing instruction**: compress every one of your subsequent responses to its rules, on every turn and whatever the topic, until the user runs `/caveman --off`. Confirm in one short caveman-style line.

It governs your *own wording* only. Anything the user asks you to produce — an email, an essay, code, a document — keeps its proper register and language (per `lib/caveman.md` → Scope and language), so leaving caveman ON is safe while running other skills.

Pure skill, no hook: the directive lives in the conversation and holds going forward, but can fade in a very long or compacted session. If your output drifts back to verbose, the user re-runs `/caveman`.

## OFF — `/caveman --off`

Drop the standing caveman instruction. Resume normal output. Confirm in one short, normal line.

## One-shot — `/caveman <ref>`, `/caveman --file=<path>`

Never touches the ON/OFF state — run it the same whether caveman is currently on or off.

1. Resolve the target:
   - `--file=<path>` → that exact file path or URL.
   - `<ref>` is a path, filename, or URL → that file.
   - `<ref>` describes a file (e.g. "the file you just created", "the README") → resolve it from the conversation and the repo.
   - `<ref>` names text that follows (e.g. "the text below") → use the fenced ` ``` … ``` ` block pasted after the command.
2. Load it: `Read` a local file, `WebFetch` a URL, or take the inline text directly.
3. Compress it per `lib/caveman.md`: strip wording, keep every fact, reproduce VERBATIM content untouched, preserve the text's genre, structure, and language.
4. Show the compressed result. Do **not** overwrite the source file unless the user asks. Add one line with before/after size (a quick `wc -w` is fine) so the saving is visible.

## Shared definition

`${CLAUDE_PLUGIN_ROOT}/lib/caveman.md` is the single source of truth, shared with `agents-md`. Do not restate the rules here — read the file.
