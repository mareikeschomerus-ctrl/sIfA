#!/usr/bin/env python3
"""update-example.py — replace the embedded EXAMPLE_SVG in the sIfA tool
HTML files with the current example.svg in this folder.

Workflow:
  1. Open the latest sIfA HTML, fill in the example you want frozen
     into the tool's "About" view, click "⬇ Table & Figure · SVG", and
     save the result next to this script as `example.svg`.
  2. Run:    python3 update-example.py
  3. Both `Make your sIfA vX.X.html` and the matching offline build
     get their `EXAMPLE_SVG = \\`...\\`;` line rewritten in place.

By default the script strips the embedded `<metadata>` block from the
SVG before inlining it — that block is per-export bookkeeping (its
CDATA + xmlns:sifa attributes are not preserved by the browser's HTML
parser when the SVG is dropped into the page via innerHTML), so it
would be dead weight in the source file. Pass --keep-metadata if you
ever want to preserve it anyway.

Flags:
  --svg PATH           Use a different source SVG (default: ./example.svg).
  --folder PATH        Folder holding the HTML files to patch.
                       Default: the directory containing this script.
  --pattern GLOB       Glob matching HTML files to patch within the folder.
                       Default: 'Make your sIfA v*.html' (online + offline).
  --keep-metadata      Keep the <metadata>…</metadata> block from the SVG.
  --dry-run            Show what would change without writing.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# ── Regex patterns (compiled once) ────────────────────────────────────
XML_DECL_RE   = re.compile(r"^\s*<\?xml[^>]*\?>\s*", re.IGNORECASE)
METADATA_RE   = re.compile(r"<metadata\b[^>]*>.*?</metadata>\s*", re.IGNORECASE | re.DOTALL)
XMLNS_SIFA_RE = re.compile(r"\s+xmlns:sifa=\"[^\"]*\"")
# Match the opening of the FIRST <svg> tag — used to strip width/height
# from the *root* SVG only (nested chart <svg> elements keep theirs so
# they sit inside the composite at the right size).
ROOT_SVG_OPEN_RE = re.compile(r"<svg\b([^>]*)>", re.IGNORECASE | re.DOTALL)
WIDTH_HEIGHT_RE  = re.compile(r"\s+(?:width|height)=\"[^\"]*\"", re.IGNORECASE)
# Collapse runs of whitespace that sit *between* tags (i.e. after a `>`
# and before the next `<`). This compresses the multi-line exported
# SVG into one line without touching whitespace inside attribute values.
INTERTAG_WS_RE = re.compile(r">\s+<")
LEADING_WS_RE  = re.compile(r"^\s+", re.MULTILINE)

# Matches the existing constant — single template-literal line in the
# source. We rely on the line starting with `const EXAMPLE_SVG = ` and
# the template literal ending with a backtick + semicolon + newline.
EXAMPLE_LINE_RE = re.compile(
    r"^const EXAMPLE_SVG\s*=\s*`[^\n]*`;\s*$",
    re.MULTILINE,
)


def normalise_svg(svg_text: str, *, keep_metadata: bool) -> str:
    """Strip XML declaration, optionally drop <metadata>, make the
    root <svg> responsive (no width/height attrs, with a
    `width:100%;height:auto` style), collapse inter-tag whitespace,
    and trim. Result is one line of SVG markup."""
    txt = svg_text
    txt = XML_DECL_RE.sub("", txt, count=1)
    if not keep_metadata:
        txt = METADATA_RE.sub("", txt, count=1)
        txt = XMLNS_SIFA_RE.sub("", txt, count=1)
    # Make the root <svg> scale with its container. The exported SVG
    # carries explicit width="…"/height="…" attributes (used when it is
    # opened standalone in a browser), but those attributes pin the
    # inlined version to its intrinsic pixel size — the table gets
    # clipped and the figure looks enormous. Strip them and add a
    # responsive style instead. Nested chart <svg> elements deeper in
    # the document keep their own sizing.
    root_match = ROOT_SVG_OPEN_RE.search(txt)
    if root_match:
        attrs = root_match.group(1)
        attrs = WIDTH_HEIGHT_RE.sub("", attrs)
        if "style=" not in attrs.lower():
            attrs = attrs.rstrip() + ' style="display:block;width:100%;height:auto"'
        replacement = f"<svg{attrs}>"
        txt = txt[: root_match.start()] + replacement + txt[root_match.end():]
    # Single-line everything between tags
    txt = LEADING_WS_RE.sub("", txt)
    txt = txt.replace("\n", " ")
    txt = INTERTAG_WS_RE.sub("><", txt)
    # Squeeze multiple spaces (anywhere left over) into one
    txt = re.sub(r" {2,}", " ", txt)
    return txt.strip()


def escape_for_template_literal(svg_one_line: str) -> str:
    """Escape characters that would break a JS template literal:
    backslashes, backticks, and `${` interpolation starts."""
    out = svg_one_line.replace("\\", "\\\\")
    out = out.replace("`", "\\`")
    out = out.replace("${", "\\${")
    return out


def patch_file(html_path: Path, new_line: str, *, dry_run: bool) -> tuple[bool, int, int]:
    """Rewrite the EXAMPLE_SVG line in `html_path` to `new_line`.
    Returns (changed, old_byte_len, new_byte_len)."""
    txt = html_path.read_text(encoding="utf-8")
    m = EXAMPLE_LINE_RE.search(txt)
    if not m:
        raise SystemExit(
            f"ERROR: could not find a single-line `const EXAMPLE_SVG = `...`;` "
            f"in {html_path.name}. Has the format changed?"
        )
    old_line = m.group(0)
    if old_line == new_line:
        return (False, len(old_line), len(new_line))
    if not dry_run:
        new_txt = txt[: m.start()] + new_line + txt[m.end():]
        html_path.write_text(new_txt, encoding="utf-8")
    return (True, len(old_line), len(new_line))


def main() -> int:
    here = Path(__file__).resolve().parent
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--svg", type=Path, default=here / "example.svg",
                    help="Source SVG (default: ./example.svg next to this script)")
    ap.add_argument("--folder", type=Path, default=here,
                    help="Folder containing the HTML files to patch (default: script directory)")
    ap.add_argument("--pattern", default="Make your sIfA v*.html",
                    help="Glob within the folder. Default catches the current "
                         "online + offline builds at the project root (archived "
                         "builds in archive/ are not touched). Override to "
                         "target a specific version if needed.")
    ap.add_argument("--keep-metadata", action="store_true",
                    help="Keep the <metadata> block from the SVG (default: strip it)")
    ap.add_argument("--dry-run", action="store_true",
                    help="Report what would change without writing")
    args = ap.parse_args()

    if not args.svg.exists():
        print(f"ERROR: source SVG not found: {args.svg}", file=sys.stderr)
        return 2

    svg_raw = args.svg.read_text(encoding="utf-8")
    svg_one = normalise_svg(svg_raw, keep_metadata=args.keep_metadata)
    svg_esc = escape_for_template_literal(svg_one)
    new_line = f"const EXAMPLE_SVG = `{svg_esc}`;"

    targets = sorted(args.folder.glob(args.pattern))
    if not targets:
        print(f"ERROR: no files match {args.pattern} in {args.folder}", file=sys.stderr)
        return 2

    print(f"Source : {args.svg}  ({len(svg_raw):,} bytes raw, "
          f"{len(svg_one):,} bytes minified)")
    print(f"Targets: {len(targets)} file(s) matching '{args.pattern}'")
    if args.keep_metadata:
        print("Mode   : keeping <metadata> block")
    if args.dry_run:
        print("Mode   : DRY RUN — no files will be written")
    print()

    summary = []
    for path in targets:
        changed, old_len, new_len = patch_file(path, new_line, dry_run=args.dry_run)
        verb = "would update" if (changed and args.dry_run) else ("updated" if changed else "unchanged")
        delta = new_len - old_len
        summary.append((path.name, verb, old_len, new_len, delta))

    width = max(len(s[0]) for s in summary)
    for name, verb, old_len, new_len, delta in summary:
        sign = "+" if delta > 0 else ""
        print(f"  {name:<{width}}  {verb:<13}  "
              f"EXAMPLE_SVG line: {old_len:,} → {new_len:,} bytes "
              f"({sign}{delta:,})")

    print()
    print("Done." if not args.dry_run else "Dry run complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
