# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Audit script for kntnt-skills.

Runs every scriptable check of the Kntnt plugin standard (the universal tier-1
checks) plus this plugin's own structural check: the vendored Matt Pocock files
that skill-maker and plugin-maker depend on must be present. Cognitive checks
(whether a skill's prose is self-contained, whether a trigger boundary is sound)
stay manual.

Exit code 0 when no findings are produced; exit code 1 otherwise. A tabulated
report is written to stdout in both cases.

The script resolves the repository root from its own location (scripts/audit.py),
so `uv run scripts/audit.py` works from anywhere in the worktree. Standard library
only — no third-party dependencies, so the PEP 723 block above pins only the
Python version.
"""

from __future__ import annotations

import json
import re
import sys
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

# Repository root resolved from this file's location: scripts/audit.py.
REPO_ROOT: Path = Path(__file__).resolve().parent.parent

PLUGIN_JSON: Path = REPO_ROOT / ".claude-plugin" / "plugin.json"
MARKETPLACE_JSON: Path = REPO_ROOT / ".claude-plugin" / "marketplace.json"
CHANGELOG: Path = REPO_ROOT / "CHANGELOG.md"
SKILLS_DIR: Path = REPO_ROOT / "skills"
VENDOR_DIR: Path = REPO_ROOT / "lib" / "vendor" / "matt-pocock"

# The vendored Matt Pocock files skill-maker and plugin-maker read. Their absence
# would silently break those skills, so the audit treats them as load-bearing.
VENDORED_FILES: tuple[str, ...] = (
    "LICENSE",
    "writing-great-skills/SKILL.md",
    "writing-great-skills/GLOSSARY.md",
    "grilling/SKILL.md",
)


@dataclass
class Finding:
    """One audit finding — a check name, a path, an optional line, a message."""

    check: str
    path: str
    line: int | None
    message: str


@dataclass
class CheckResult:
    """The result of running one named check."""

    name: str
    findings: list[Finding] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.findings


def read_text(path: Path) -> str:
    """Read a UTF-8 text file. Returns empty string when the file is missing."""

    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def relpath(path: Path) -> str:
    """Repository-relative path for reporting."""

    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def frontmatter_name(skill_md: Path) -> str | None:
    """Extract the `name:` field from a SKILL.md's YAML frontmatter, or None."""

    lines = read_text(skill_md).splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    for line in lines[1:]:
        if line.strip() == "---":
            break
        match = re.match(r"\s*name:\s*(.+?)\s*$", line)
        if match:
            return match.group(1).strip().strip("\"'")
    return None


def latest_changelog_version() -> str | None:
    """The first non-`[Unreleased]` `## [version]` heading in the changelog,
    or None when no released heading exists."""

    pattern = re.compile(r"^## \[([^\]]+)\]", flags=re.MULTILINE)
    for match in pattern.finditer(read_text(CHANGELOG)):
        name = match.group(1)
        if name.lower() == "unreleased":
            continue
        return name
    return None


def check_plugin_json_and_version() -> CheckResult:
    """(a) — plugin.json is well-formed, carries the required fields, and its
    `version` matches the latest non-`[Unreleased]` heading in CHANGELOG.md."""

    result = CheckResult(name="(a) plugin.json shape and CHANGELOG version match")
    try:
        data = json.loads(read_text(PLUGIN_JSON))
    except json.JSONDecodeError as exc:
        result.findings.append(
            Finding(result.name, relpath(PLUGIN_JSON), None, f"invalid JSON: {exc}")
        )
        return result
    if not isinstance(data, dict):
        result.findings.append(
            Finding(result.name, relpath(PLUGIN_JSON), None, "root is not an object")
        )
        return result
    for required in ("name", "version", "description"):
        if required not in data:
            result.findings.append(
                Finding(
                    result.name,
                    relpath(PLUGIN_JSON),
                    None,
                    f"missing required field '{required}'",
                )
            )
    plugin_version = str(data.get("version", "")).strip()
    latest = latest_changelog_version()
    if latest is None:
        result.findings.append(
            Finding(
                result.name, relpath(CHANGELOG), None, "no non-Unreleased heading found"
            )
        )
    elif plugin_version != latest:
        result.findings.append(
            Finding(
                result.name,
                relpath(PLUGIN_JSON),
                None,
                f"plugin.json version '{plugin_version}' does not match latest CHANGELOG version '{latest}'",
            )
        )
    return result


def check_marketplace_json() -> CheckResult:
    """(b) — marketplace.json is well-formed and lists a plugin whose name
    matches plugin.json's name, so the marketplace install path is coherent."""

    result = CheckResult(name="(b) marketplace.json shape and name match")
    try:
        market = json.loads(read_text(MARKETPLACE_JSON))
    except json.JSONDecodeError as exc:
        result.findings.append(
            Finding(result.name, relpath(MARKETPLACE_JSON), None, f"invalid JSON: {exc}")
        )
        return result
    try:
        plugin = json.loads(read_text(PLUGIN_JSON))
        plugin_name = str(plugin.get("name", "")).strip()
    except json.JSONDecodeError:
        plugin_name = ""
    plugins = market.get("plugins") if isinstance(market, dict) else None
    if not isinstance(plugins, list) or not plugins:
        result.findings.append(
            Finding(
                result.name,
                relpath(MARKETPLACE_JSON),
                None,
                "missing or empty 'plugins' array",
            )
        )
        return result
    names = {str(p.get("name", "")).strip() for p in plugins if isinstance(p, dict)}
    if plugin_name and plugin_name not in names:
        result.findings.append(
            Finding(
                result.name,
                relpath(MARKETPLACE_JSON),
                None,
                f"no plugin named '{plugin_name}' (from plugin.json) listed in marketplace.json",
            )
        )
    return result


def check_skill_dirs() -> CheckResult:
    """(c) — every directory under skills/ carries a SKILL.md whose frontmatter
    `name` matches the directory name, so /help and invocation stay coherent."""

    result = CheckResult(name="(c) skills/ directories and SKILL.md names")
    if not SKILLS_DIR.exists():
        result.findings.append(
            Finding(result.name, relpath(SKILLS_DIR), None, "skills/ directory missing")
        )
        return result
    skill_dirs = sorted(d for d in SKILLS_DIR.iterdir() if d.is_dir())
    if not skill_dirs:
        result.findings.append(
            Finding(result.name, relpath(SKILLS_DIR), None, "no skill directories found")
        )
        return result
    for d in skill_dirs:
        skill_md = d / "SKILL.md"
        if not skill_md.is_file():
            result.findings.append(
                Finding(result.name, relpath(skill_md), None, "missing SKILL.md")
            )
            continue
        name = frontmatter_name(skill_md)
        if name is None:
            result.findings.append(
                Finding(result.name, relpath(skill_md), None, "no `name:` in frontmatter")
            )
        elif name != d.name:
            result.findings.append(
                Finding(
                    result.name,
                    relpath(skill_md),
                    None,
                    f"frontmatter name '{name}' does not match directory '{d.name}'",
                )
            )
    return result


def check_vendored_files() -> CheckResult:
    """(d) — the vendored Matt Pocock files skill-maker and plugin-maker read are
    present. A structural (tier-2) check: their absence would silently break both
    skills, so the audit guards them."""

    result = CheckResult(name="(d) vendored Matt Pocock files present")
    for rel in VENDORED_FILES:
        path = VENDOR_DIR / rel
        if not path.is_file():
            result.findings.append(
                Finding(result.name, relpath(path), None, "missing vendored file")
            )
    return result


CHECKS: tuple[Callable[[], CheckResult], ...] = (
    check_plugin_json_and_version,
    check_marketplace_json,
    check_skill_dirs,
    check_vendored_files,
)


def format_report(results: list[CheckResult]) -> str:
    """Render a tabulated summary followed by a per-failing-check detail block."""

    name_width = max(len(r.name) for r in results)
    status_width = len("STATUS")
    header = f"{'CHECK'.ljust(name_width)}  {'STATUS'.ljust(status_width)}  COUNT"
    separator = "-" * len(header)
    lines = [header, separator]
    for r in results:
        status = "OK" if r.ok else "FAIL"
        lines.append(
            f"{r.name.ljust(name_width)}  {status.ljust(status_width)}  {len(r.findings)}"
        )
    lines.append(separator)
    total = sum(len(r.findings) for r in results)
    lines.append(
        f"{'TOTAL FINDINGS'.ljust(name_width)}  {''.ljust(status_width)}  {total}"
    )
    failing = [r for r in results if not r.ok]
    if failing:
        lines.append("")
        lines.append("Findings:")
        for r in failing:
            lines.append("")
            lines.append(f"## {r.name}")
            for f in r.findings:
                location = f.path if f.line is None else f"{f.path}:{f.line}"
                lines.append(f"  - {location} — {f.message}")
    return "\n".join(lines)


def main() -> int:
    """Run every check, print the report, return 0 on a clean run else 1."""

    results = [check() for check in CHECKS]
    print(format_report(results))
    return 0 if all(r.ok for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
