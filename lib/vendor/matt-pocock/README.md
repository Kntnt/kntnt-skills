# Vendored: Matt Pocock's skills

The files under this directory are **vendored verbatim** from Matt Pocock's
skills repository and are used by the `skill-maker` and `plugin-maker` skills as
their underlying craft and interview references. They are **not** Kntnt's work.

- **Source:** <https://github.com/mattpocock/skills>
- **Licence:** MIT — see [`LICENSE`](LICENSE) in this directory (© 2026 Matt Pocock).
- **Why vendored:** the MIT licence permits redistribution with attribution, so
  copying the files in keeps `kntnt-skills` self-contained (no runtime dependency
  on whether the upstream skills happen to be installed) and deterministic.

## Contents

| Path | Upstream | Role |
| --- | --- | --- |
| `writing-great-skills/SKILL.md` | `skills/.../writing-great-skills/SKILL.md` | The principles of writing a predictable skill. |
| `writing-great-skills/GLOSSARY.md` | `skills/.../writing-great-skills/GLOSSARY.md` | Definitions of the bold terms used by the SKILL. |
| `grilling/SKILL.md` | `skills/productivity/grilling/SKILL.md` | The relentless one-question-at-a-time interview protocol. |

## Boundary

These files are the **general craft**. Kntnt's **house conventions** live in
`lib/skill-conventions.md` and `lib/plugin-standard.md` (Apache-2.0, Kntnt's own
work). Where the two overlap or conflict, the house conventions win — they are
the standard this plugin exists to apply.

## Re-syncing

To update to a newer upstream version, replace the files in place from
<https://github.com/mattpocock/skills> and keep the `LICENSE` and this note
intact. Do not edit the vendored files otherwise — keeping them verbatim is what
makes the attribution clean and the re-sync trivial.
