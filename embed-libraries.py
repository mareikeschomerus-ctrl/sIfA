#!/usr/bin/env python3
"""
embed-libraries.py
──────────────────
Builds the offline sIfA HTML by downloading React 18, ReactDOM 18, and Babel
Standalone 7 from the CDN and inlining them into the online HTML, producing
a fully self-contained file that works with no internet connection.

Each inlined library is wrapped in a comment block that preserves its
copyright + MIT licence header — required because the sIfA Tool is released
under Apache 2.0 and bundles MIT-licensed dependencies. Full licence texts
are also kept in THIRD_PARTY_LICENSES.md at the repo root.

Usage
─────
    python3 embed-libraries.py                  # auto-detect latest source
    python3 embed-libraries.py --source FILE    # override source HTML
    python3 embed-libraries.py --dest FILE      # override output filename

By default the script:
  1. Finds the latest "Make your sIfA vX.X.html" in the current folder
     (excluding "(offline)" builds).
  2. Writes the matching "Make your sIfA vX.X (offline).html".
"""

import argparse
import re
import sys
import urllib.request
from pathlib import Path

LIBS = [
    {
        "name": "react.production.min.js",
        "url":  "https://cdnjs.cloudflare.com/ajax/libs/react/18.2.0/umd/react.production.min.js",
        "title": "React v18.2.0",
        "copyright": "Copyright (c) Meta Platforms, Inc. and affiliates.",
        "homepage": "https://github.com/facebook/react",
    },
    {
        "name": "react-dom.production.min.js",
        "url":  "https://cdnjs.cloudflare.com/ajax/libs/react-dom/18.2.0/umd/react-dom.production.min.js",
        "title": "ReactDOM v18.2.0",
        "copyright": "Copyright (c) Meta Platforms, Inc. and affiliates.",
        "homepage": "https://github.com/facebook/react",
    },
    {
        "name": "babel.min.js",
        "url":  "https://cdnjs.cloudflare.com/ajax/libs/babel-standalone/7.23.2/babel.min.js",
        "title": "Babel Standalone v7.23.2",
        "copyright": "Copyright (c) 2014-present Sebastian McKenzie and other contributors.",
        "homepage": "https://github.com/babel/babel",
    },
]

LICENCE_NOTE = (
    "Licensed under the MIT License. Full licence text reproduced in\n"
    "       THIRD_PARTY_LICENSES.md at the root of this distribution."
)


def find_latest_source(folder: Path) -> Path:
    """Pick the highest-versioned 'Make your sIfA vX.X.html' that is NOT an offline build."""
    candidates = []
    for p in folder.glob("Make your sIfA v*.html"):
        if "(offline)" in p.name:
            continue
        m = re.search(r"v(\d+(?:\.\d+)?)", p.name)
        if m:
            try:
                version = tuple(int(x) for x in m.group(1).split("."))
                candidates.append((version, p))
            except ValueError:
                continue
    if not candidates:
        sys.exit("Error: no 'Make your sIfA vX.X.html' source file found in this folder.")
    candidates.sort()
    return candidates[-1][1]


def derive_dest(src: Path) -> Path:
    """Insert ' (offline)' before the .html extension."""
    return src.with_name(src.stem + " (offline).html")


def fetch(lib):
    print(f"  Downloading {lib['name']} …", end=" ", flush=True)
    req = urllib.request.Request(lib["url"], headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = r.read().decode("utf-8")
    print(f"✓  ({len(data) // 1024} KB)")
    return data


def wrap_with_licence(lib, js: str) -> str:
    """Wrap inlined JS in a <script> tag with a preserved attribution header."""
    header = (
        f"/* ──────────────────────────────────────────────────────────────\n"
        f"   {lib['title']}\n"
        f"   {lib['copyright']}\n"
        f"   {lib['homepage']}\n"
        f"\n"
        f"       {LICENCE_NOTE}\n"
        f"   ────────────────────────────────────────────────────────────── */"
    )
    return f"<script>\n{header}\n{js}\n</script>"


def embed(html: str, libs_with_js):
    for lib, js in libs_with_js:
        pattern = r'<script\s+src="[^"]*' + re.escape(lib["name"]) + r'[^"]*"></script>'
        replacement = wrap_with_licence(lib, js)
        new_html, n = re.subn(pattern, lambda _: replacement, html)
        if n == 0:
            print(f"  ⚠  Could not find a <script src> tag for {lib['name']} — skipping.")
        else:
            html = new_html
            print(f"  Embedded {lib['name']} ✓")
    return html


def main():
    here = Path(__file__).resolve().parent

    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--source", type=Path, default=None,
                    help="Online HTML to use as source (default: latest 'Make your sIfA vX.X.html' in this folder).")
    ap.add_argument("--dest", type=Path, default=None,
                    help="Output filename (default: derived from source, e.g. 'Make your sIfA v1.1 (offline).html').")
    args = ap.parse_args()

    src = args.source if args.source else find_latest_source(here)
    if not src.exists():
        sys.exit(f"Error: source file {src} not found.")
    dest = args.dest if args.dest else derive_dest(src)

    print(f"\nSource: {src.name}")
    print(f"Output: {dest.name}\n")

    print("Fetching libraries:")
    libs_with_js = [(lib, fetch(lib)) for lib in LIBS]

    print("\nEmbedding:")
    html = src.read_text(encoding="utf-8")
    html = embed(html, libs_with_js)

    dest.write_text(html, encoding="utf-8")
    size_kb = dest.stat().st_size // 1024
    print(f"\n✅  Done!  →  {dest.name}  ({size_kb} KB)")
    print("    Open that file in any browser — no internet connection needed.\n")


if __name__ == "__main__":
    main()
