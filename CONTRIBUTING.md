# Contributing to sIfA

Thanks for thinking about contributing. sIfA is a small project with a deliberate scope — a single-file browser tool for declaring AI contribution to research. Contributions that keep it small, dependency-light, and usable offline are the most likely to land.

## Ways to contribute

- **Report a bug** — open an issue using the *Bug report* template. A screenshot of the figure or a copy of the failing `.sifa.json` is usually enough to reproduce.
- **Suggest a feature** — open an issue using the *Feature request* template. Frame it in terms of a real research workflow the feature would unblock, rather than a technical capability in isolation.
- **Improve the documentation** — typos, clearer phrasings, additional worked examples, translations of the README into other languages. All welcome.
- **Submit a code change** — see below.

## Development setup

There is no build step for day-to-day editing. The tool ships as one HTML file that loads React 18 and Babel Standalone from a CDN and transpiles JSX in the browser:

```bash
# Clone
git clone https://github.com/mareikeschomerus-ctrl/sIfA.git
cd sIfA

# Open the latest online build directly
open "Make your sIfA v1.0.html"

# Or serve it (useful when iterating on file-loading or CORS-sensitive features)
python3 -m http.server 8000
# then visit http://localhost:8000/Make%20your%20sIfA%20v1.0.html
```

To edit the tool itself, open `credit-tool.jsx` (or the `<script type="text/babel">` block inside the HTML), make your change, and refresh the browser.

When you are ready to ship, regenerate the offline build:

```bash
python3 embed-libraries.py "Make your sIfA v1.0.html"
# produces "Make your sIfA v1.0 (offline).html"
```

## Coding conventions

- **Single-file philosophy.** The whole app lives in one HTML file. Resist the urge to split into modules or pull in a bundler — the value proposition of sIfA is that any researcher can download one file and have a working tool.
- **No new dependencies without discussion.** React is the only runtime dependency. Anything that would add a `package.json` or a build step (Tailwind compiler, TypeScript, etc.) should be raised as an issue first.
- **Inline styles, not CSS classes.** Style with React inline `style={{}}` objects so the file stays self-contained. The `no-print` class is the one exception, used to hide UI chrome from print/PDF exports.
- **Comments explain the *why*.** The code is short enough that *what* is usually obvious from reading it. Use comments for design decisions, validation rules, and quirks of the SVG export that future-you will not remember.
- **Validate JSX before opening a PR.** A quick check with Babel's parser catches most issues:

  ```bash
  npx @babel/parser --plugins jsx credit-tool.jsx > /dev/null && echo OK
  ```

## Pull-request workflow

1. Fork the repo and create a topic branch off `main`.
2. Make your changes and test them in at least one Chromium-based browser (Chrome / Edge) and one non-Chromium browser (Firefox or Safari). The Save As dialog will only work in the former; the rest of the tool must work in both.
3. Update `CHANGELOG.md` under an `[Unreleased]` heading.
4. Open a PR with a short description of what changed and why, plus a screenshot if you changed anything visual.

Releases are tagged `vX.Y` and a matching `Make your sIfA vX.Y.html` (and offline variant) is attached to each GitHub Release.

## Filing a useful issue

If you can answer the following in your issue, it will save a round-trip:

- What did you do? (Steps to reproduce — clicks, keystrokes, file loaded.)
- What did you expect to happen?
- What actually happened?
- Browser and operating system?
- If possible, attach the `.sifa.json` that triggered the problem, or a screenshot of the figure.

## Code of conduct

Be civil and assume good faith. Researchers, journal editors, developers, and curious bystanders all read this repo. Direct disagreement is fine; personal attacks are not.

## Questions

If you are unsure whether something fits the scope or how to approach it, open a draft issue and ask before writing code. It saves everyone time.
