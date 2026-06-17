#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>
#
# SPDX-License-Identifier: Apache-2.0

"""
Reproduce the YAML frontmatter bug in commitizen's built-in Markdown format.

The built-in ``Markdown`` changelog format has no YAML frontmatter awareness.
Its ``RE_TITLE`` regex matches ``#`` lines inside frontmatter as headings,
causing ``search_version`` to extract false versions (e.g. ``2.0`` from
``Apache-2.0``).

Three methods:

  1. **Regex analysis** — show ``RE_TITLE`` matching frontmatter and
     ``search_version`` returning a false version.
  2. **_find_incremental_rev simulation** — demonstrate that
     ``SequenceMatcher`` fails to match the false version tag ``v2.0`` against
     real tags, causing ``NoRevisionError``.
  3. **get_metadata() API call** — call commitizen's
     ``Markdown.get_metadata()`` directly against a frontmatter-bearing
     changelog file.

Usage:

    uv run python scripts/reproduce_bug.py               # all three steps
    uv run python scripts/reproduce_bug.py --step 1      # run only step 1
    uv run python scripts/reproduce_bug.py --step 3      # run only step 3 (API)
    uv run python scripts/reproduce_bug.py --unattended   # skip pauses (CI/CD)
    uv run python scripts/reproduce_bug.py --clean       # remove temp files
    uv run python scripts/reproduce_bug.py --help        # this message
"""

import argparse
import re
import shutil
from difflib import SequenceMatcher
from pathlib import Path

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.rule import Rule
from rich.table import Table
from rich.text import Text

# ---------------------------------------------------------------------------
# Globals
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
TMP_DIR = REPO_ROOT / "tmp"

# REUSE-IgnoreStart
SAMPLE = (
    "---\n"
    "# SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>\n"
    "#\n"
    "# SPDX-License-Identifier: Apache-2.0\n"
    "\n"
    "icon: lucide/git-commit-vertical\n"
    "---\n"
    "\n"
    "# Changelog\n"
    "\n"
    "All notable changes to this project will be documented in this file.\n"
)
# REUSE-IgnoreEnd

RE_TITLE = re.compile(r"^(?P<level>#+) (?P<title>.*)$")
RE_VERSION = re.compile(r"\d+\.\d+(\.\d+)?")

console = Console()

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _style(line: str, bold: bool = False, color: str | None = None) -> Text:
    """Return a styled ``Text`` object."""
    st = Text(line)
    if bold:
        st.stylize("bold")
    if color:
        st.stylize(color)
    return st


DIVIDER = "─" * console.width if console.width else 50


def _pause(unattended: bool) -> None:
    """Pause between steps unless in unattended mode."""
    if unattended:
        return
    console.print(f"\n[dim]{DIVIDER}[/dim]")
    try:
        Prompt.ask("[yellow]Press Enter to continue[/yellow]", default="")
    except EOFError:
        pass
    except KeyboardInterrupt:
        console.print()
        console.print("[bold yellow]Aborted by user[/bold yellow]")
        raise SystemExit(1) from None


# ---------------------------------------------------------------------------
# Step 1 – regex root cause
# ---------------------------------------------------------------------------


def step1_regex_analysis():
    """Demonstrate the regex root cause."""

    # ── regex summary ──────────────────────────────────────────────────────
    tbl = Table(box=box.SIMPLE, show_header=False)
    tbl.add_column(style="cyan")
    tbl.add_column(style="white")
    tbl.add_row("RE_TITLE",  f"  {RE_TITLE.pattern!r}")
    tbl.add_row("RE_VERSION", f"  {RE_VERSION.pattern!r}")
    console.print(tbl)
    console.print()

    # ── matching lines ─────────────────────────────────────────────────────
    console.print("[bold]Lines matched by RE_TITLE (after .strip().lower()):[/bold]")
    console.print()

    results_tbl = Table(box=box.SIMPLE, show_header=True)
    results_tbl.add_column("Line", style="dim")
    results_tbl.add_column("Content", style="yellow")
    results_tbl.add_column("Version found", style="bold red", justify="center")

    false_version = None
    for i, line in enumerate(SAMPLE.splitlines(keepends=True)):
        stripped = line.strip().lower()
        m = RE_TITLE.match(stripped)
        if not m:
            continue
        title = m.group("title")
        ver = RE_VERSION.search(title)
        if ver:
            false_version = ver.group()
            results_tbl.add_row(
                str(i + 1),
                title,
                Text(ver.group(), style="bold red"),
            )
        else:
            results_tbl.add_row(str(i + 1), title, "—")

    console.print(results_tbl)

    if false_version:
        console.print()
        panel = Panel(
            Text.assemble(
                ("🐛 ", "bold"),
                ("BUG CONFIRMED", "bold red"),
                (": RE_TITLE matches frontmatter", ""),
            ),
            border_style="red",
        )
        console.print(panel)
        console.print()

        console.print("[bold]Root cause:[/bold]")
        reasons = Table(box=box.SIMPLE, show_header=False)
        reasons.add_column("", style="dim")
        reasons.add_column(style="white")
        reasons.add_row(
            "❶",
            f"[cyan]RE_TITLE[/cyan] [white]=[/white] [yellow]{RE_TITLE.pattern!r}[/yellow]\n"
            "    matches lines inside YAML frontmatter as headings",
        )
        reasons.add_row(
            "❷",
            f"[cyan]RE_VERSION[/cyan] [white]=[/white] [yellow]{RE_VERSION.pattern!r}[/yellow]\n"
            f"    extracts [bold red]{false_version!r}[/bold red] from [white]'Apache-2.0'[/white]",
        )
        console.print(reasons)


# ---------------------------------------------------------------------------
# Step 2 – SequenceMatcher simulation
# ---------------------------------------------------------------------------


def step2_sequence_matcher_simulation():
    """
    Simulate what commitizen's ``_find_incremental_rev`` does when it
    receives the false version 'v2.0' and tries to match it against
    real tags like 'v0.1.0'.
    """
    SIMILARITY_THRESHOLD = 0.89
    false_tag = "v2.0"
    real_tags = ["v0.1.0"]

    # ── parameters ─────────────────────────────────────────────────────────
    params = Table(box=box.SIMPLE, show_header=False)
    params.add_column(style="cyan")
    params.add_column(style="white")
    params.add_row("False tag",       f"[bold red]{false_tag!r}[/bold red]")
    params.add_row("Real tags",       f"{real_tags}")
    params.add_row("Similarity thresh.", str(SIMILARITY_THRESHOLD))
    console.print(params)
    console.print()

    # ── comparison ─────────────────────────────────────────────────────────
    comp = Table(box=box.SIMPLE, show_header=True)
    comp.add_column("Tag comparison", style="cyan")
    comp.add_column("Ratio", justify="center")
    comp.add_column("Verdict", style="bold")

    for tag in real_tags:
        stripped_tag = tag.lstrip("v")
        ratio = SequenceMatcher(None, false_tag, stripped_tag).ratio()
        verdict = (
            Text("✓ WOULD MATCH", style="bold green")
            if ratio >= SIMILARITY_THRESHOLD
            else Text("✗ NO MATCH", style="bold red")
        )
        comp.add_row(
            f"SequenceMatcher({false_tag!r}, {stripped_tag!r})",
            f"{ratio:.4f}",
            verdict,
        )

    console.print(comp)
    console.print()

    # ── result ─────────────────────────────────────────────────────────────
    console.print(
        "[bold]Result:[/bold] No tag matches → "
        "[bold yellow]_find_incremental_rev[/bold yellow] raises "
        "[bold red]NoRevisionError[/bold red] (exit code 16)."
    )
    console.print()

    console.print(Panel(
        Text.assemble(
            ("🐛 ", "bold"),
            ("BUG CONFIRMED", "bold red"),
            (": NoRevisionError due to false version", ""),
        ),
        border_style="red",
    ))


# ---------------------------------------------------------------------------
# Step 3 – API-level reproduction
# ---------------------------------------------------------------------------


def step3_get_metadata_programmatic():
    """
    Call commitizen's ``Markdown.get_metadata()`` directly against a
    frontmatter-bearing changelog to prove the bug programmatically.

    This avoids subprocess/env issues and shows the exact API-level failure.
    """
    tmp_work = TMP_DIR / "repro"
    if tmp_work.exists():
        shutil.rmtree(tmp_work)
    tmp_work.mkdir(parents=True)

    # REUSE-IgnoreStart
    changelog_content = (
        "---\n"
        "# SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>\n"
        "#\n"
        "# SPDX-License-Identifier: Apache-2.0\n"
        "---\n"
        "\n"
        "# Changelog\n"
        "\n"
        "All notable changes to this project will be documented in this file.\n"
    )
    # REUSE-IgnoreEnd

    pyproject_content = (
        "[tool.commitizen]\n"
        'tag_format = "v$version"\n'
    )

    changelog_path = tmp_work / "CHANGELOG.md"
    changelog_path.write_text(changelog_content)
    pyproject_path = tmp_work / "pyproject.toml"
    pyproject_path.write_text(pyproject_content)

    try:
        from commitizen.config.toml_config import TomlConfig
        from commitizen.changelog_formats.markdown import Markdown

        cfg = TomlConfig(data="", path=pyproject_path)
        md_format = Markdown(cfg)

        meta = md_format.get_metadata(str(changelog_path))

        console.print(f"[dim]Changelog file:[/dim] [cyan]{changelog_path}[/cyan]")
        console.print()

        # ── metadata table ─────────────────────────────────────────────────
        tbl = Table(box=box.SIMPLE, show_header=False)
        tbl.add_column("Field", style="cyan")
        tbl.add_column("Value", style="white")
        tbl.add_row("latest_version",     f"{meta.latest_version!r}")
        tbl.add_row("latest_version_tag", f"{meta.latest_version_tag!r}")
        tbl.add_row("latest_version_pos", str(meta.latest_version_position))
        console.print(tbl)
        console.print()

        if meta.latest_version == "2.0":
            panel = Panel(
                Text.assemble(
                    ("🐛 ", "bold"),
                    ("BUG CONFIRMED", "bold red"),
                    (": get_metadata() found ", ""),
                    ("'2.0'", "bold red"),
                    (" from frontmatter", ""),
                ),
                border_style="red",
            )
            console.print(panel)
            console.print()
            console.print(
                "The built-in [cyan]Markdown[/cyan] format does not skip YAML frontmatter.\n"
                "[yellow]search_version()[/yellow] extracted [bold red]'2.0'[/bold red] from "
                "[white]'Apache-2.0'[/white].\n"
                "[bold yellow]cz bump --changelog[/bold yellow] would try to find tag "
                "[bold red]'v2.0'[/bold red] and\n"
                "raise [bold red]NoRevisionError[/bold red] when it doesn't exist."
            )
        else:
            console.print("[yellow](unexpected version — changelog may not have been parsed)[/yellow]")

    except ImportError as e:
        console.print(f"[bold red]ImportError:[/bold red] {e}")
        console.print("[yellow]Run this script via[/yellow] `uv run python scripts/reproduce_bug.py`")
    except Exception as e:
        import traceback
        console.print(f"[bold red]Error:[/bold red] {e}")
        traceback.print_exc()

    console.print()
    console.print(
        f"[dim]Temp files kept at: {tmp_work}[/dim]\n"
        "[dim]Use[/dim] [bold]--clean[/bold] [dim]to remove them.[/dim]"
    )


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------


def print_summary():
    """Print a summary panel."""
    summary = Text.assemble(
        ("🐛 ", "bold"),
        ("Bug: ", ""),
        ("RE_TITLE", "cyan"),
        (" matches '#' lines inside YAML frontmatter as headings.\n", ""),
        ("search_version()", "yellow"),
        (" extracts ", ""),
        ("'2.0'", "bold red"),
        (" from ", ""),
        ("'Apache-2.0'", "white"),
        (".\n\n", ""),
        ("This causes:\n", ""),
        ("  ❶ ", ""),
        ("get_metadata()", "cyan"),
        (" → ", ""),
        ("latest_version = '2.0'", "bold red"),
        ("\n  ❷ ", ""),
        ("_find_incremental_rev('v2.0', tags)", "cyan"),
        (" → ", ""),
        ("NoRevisionError", "bold red"),
        ("\n  ❸ ", ""),
        ("cz bump --changelog", "bold yellow"),
        (" → fails with exit code ", ""),
        ("16", "bold red"),
        ("\n\n", ""),
        ("Fix: ", "bold green"),
        ("Custom commitizen.changelog_format plugin\n", ""),
        ("strips YAML frontmatter before ", ""),
        ("RE_TITLE", "cyan"),
        (" is applied.", ""),
    )

    console.print()
    console.print(Panel(summary, title="Summary", border_style="green"))
    console.print()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_parser():
    parser = argparse.ArgumentParser(
        description="Reproduce the YAML frontmatter bug in commitizen's "
                    "built-in Markdown changelog format.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "examples:\n"
            "  uv run python scripts/reproduce_bug.py               # all steps\n"
            "  uv run python scripts/reproduce_bug.py --step 1      # step 1 only\n"
            "  uv run python scripts/reproduce_bug.py --step 2      # step 2 only\n"
            "  uv run python scripts/reproduce_bug.py --step 3      # step 3 only\n"
            "  uv run python scripts/reproduce_bug.py --unattended  # skip pauses\n"
            "  uv run python scripts/reproduce_bug.py --clean       # remove temp files\n"
        ),
    )
    parser.add_argument(
        "--step", type=int, choices=[1, 2, 3],
        help="Run a single step (1=regex, 2=simulation, 3=API call)",
    )
    parser.add_argument(
        "--unattended", action="store_true",
        help="Skip 'Press Enter' pauses between steps (useful for CI/CD or scrolling)",
    )
    parser.add_argument(
        "--clean", action="store_true",
        help="Remove temporary files created by the script (tmp/repro/)",
    )
    return parser


def clean_temp():
    """Remove the temporary directory used by step 3."""
    tmp_work = TMP_DIR / "repro"
    if tmp_work.exists():
        shutil.rmtree(tmp_work)
        console.print(f"[green]✓[/green] Removed [cyan]{tmp_work}[/cyan]")
    else:
        console.print("[yellow]Nothing to clean[/yellow] — [dim]tmp/repro/[/dim] does not exist")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.clean:
        clean_temp()
        return

    steps = {
        1: ("Regex root cause", step1_regex_analysis),
        2: ("_find_incremental_rev simulation", step2_sequence_matcher_simulation),
        3: ("API-level reproduction (get_metadata)", step3_get_metadata_programmatic),
    }

    if args.step:
        title, func = steps[args.step]
        console.print()
        console.print(Rule(title=f"[bold]Bug reproduction[/bold] — Step {args.step}: {title}"))
        console.print()
        func()
        console.print()
        if args.step in (1, 2):
            print_summary()
    else:
        console.print()
        console.print(Rule(title="[bold]Bug reproduction: commitizen Markdown / YAML frontmatter[/bold]"))
        console.print()
        step_numbers = (1, 2, 3)
        for idx, num in enumerate(step_numbers):
            title, func = steps[num]
            console.print(Rule(title=f"[bold]Step {num}[/bold]: {title}", style="dim"))
            console.print()
            func()
            console.print()
            # Pause after every step except the last one
            if idx < len(step_numbers) - 1:
                _pause(args.unattended)
        print_summary()


if __name__ == "__main__":
    main()
