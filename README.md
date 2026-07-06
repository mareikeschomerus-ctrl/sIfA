# sIfA — Statement of Intellectual Fellowship and Accountability

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20285993.svg)](https://doi.org/10.5281/zenodo.20285993)

A browser-based tool for declaring how AI tools contributed to a piece of research, mapped onto the 14 CRediT contributor roles. Produces a structured table and a single-page visualisation ("the sIfA figure") that can be attached to a publication, report, or institutional disclosure.

> **sIfA** stands for **Statement of Intellectual Fellowship and Accountability**.
> "Fellowship" signals that AI tools are treated as named collaborators in the work, not invisible utilities. "Accountability" keeps responsibility for the published work with the human author, who is making the disclosure deliberately and transparently.

The tool is a single self-contained HTML file. No install, no server, no build step required for end users.

---

## Why sIfA exists

AI use in research is expanding faster than the conventions for declaring it. Free-text disclosures tend to be inconsistent and hard to compare across papers. sIfA gives authors a shared, structured format anchored in a standard that journals already understand — the [CRediT Contributor Roles Taxonomy](https://credit.niso.org), a NISO-maintained list of 14 contributor roles used across academic publishing.

By naming AI tools alongside human contributors and recording, per role, *what they did* and *how extensively the work depended on them*, sIfA invites authors to think of AI use as a contribution to be credited, not a footnote to be downplayed. The human author still signs off on the work — that is the "accountability" half of the name.

---

## Table of contents

- [For researchers](#for-researchers)
  - [Quick start](#quick-start)
  - [How the tool is structured](#how-the-tool-is-structured)
  - [Two ways to fill it in](#two-ways-to-fill-it-in)
  - [Engagement levels and AI extent](#engagement-levels-and-ai-extent)
  - [Saving and exporting](#saving-and-exporting)
  - [Worked example](#worked-example)
  - [What is *not* sent anywhere](#what-is-not-sent-anywhere)
- [For developers](#for-developers)
  - [Repository layout](#repository-layout)
  - [Running and editing](#running-and-editing)
  - [Architecture in one paragraph](#architecture-in-one-paragraph)
  - [State model](#state-model)
  - [Adding or changing roles](#adding-or-changing-roles)
  - [Build: how the offline file is generated](#build-how-the-offline-file-is-generated)
  - [Known limitations](#known-limitations)
- [Citation](#citation)
- [License](#license)
- [Acknowledgements](#acknowledgements)

---

## For researchers

### Quick start

1. Download the latest `Make your sIfA vX.X.html` from the [Releases](../../releases) page (or open `Make your sIfA vX.X (offline).html` if you'll be working without internet).
2. Open the file in any modern browser by double-clicking it. Chrome, Edge, Safari and Firefox all work.
3. Choose one of two entry modes at the top of the page — fill the table directly, or run the conversational agent.
4. Export the result as an SVG (for the figure), or save your in-progress state as a `.sifa.json` file you can reopen later.

That's the whole loop. The tool is a single HTML page; no install, no account, no upload.

### How the tool is structured

The interface is a single page with three parts:

- **A header** with action buttons — Save, Load, Reset, export options, the About panel.
- **A table** with one row per CRediT contributor role (14 rows by default). Each row records who performed the role, how AI was used in it, the tool used, and an audit-trail note.
- **A figure** — the "sIfA figure" — that renders as a brain-shaped silhouette with one axis for all recorded contributor roles, dividing evenly across them (a completely blank sIfA falls back to showing every active role rather than an empty chart). The orange field is the human contribution; the purple inner shape is the AI contribution; small purple sparkles mark the extent of AI involvement on each role's axis.

Both the table and the figure can be exported, either together as one composite SVG or as figure-only.

### Two ways to fill it in

- **Direct entry.** Click any cell and type. Each role row supports multiple contributors. For each contributor you can record an engagement level (Sole / Lead / Equal / Support) and, separately, the extent of AI use on that role.
- **Agent interview.** Click the AI Agent option to be walked through every role with a series of plain-language questions: who contributed, at what level, whether AI was used, with what tool, and how extensively. The agent enforces the role-rules (see below) and lets you skip roles that do not apply. The result lands in the same editable table, so you can revise anything afterwards.

If the standard 14 CRediT roles do not fit your project, the **Set up my own taxonomy** button at the top of the table (labelled **Edit my taxonomy** once you're using one) opens a modal where you can define your own role labels, add a role to a taxonomy you're already using — CRediT or custom — without retyping the rest, or start a blank taxonomy from scratch. Each role can carry its own short definition, shown as a tooltip in the table; CRediT roles' definitions can be edited too. The agent flow respects the custom taxonomy too.

For the full role definitions and worked examples of the research tasks that map to each role, see NISO's CRediT documentation at [credit.niso.org](https://credit.niso.org).

### Engagement levels and AI extent

Two scales are recorded separately, and it is worth keeping them distinct:

| Engagement level | What it means |
| --- | --- |
| **Sole** | One contributor — no one else worked on this role. Cannot coexist with other levels in the same row. |
| **Lead** | One contributor is the principal owner of this role; others, if any, are Support. |
| **Equal** | Two or more contributors split this role equally. All must be Equal. |
| **Support** | A contributor whose involvement was secondary. There must be at least one Lead, Equal, or Sole contributor on the same row. |

| AI extent | What it means |
| --- | --- |
| **0** | No AI used for this role. |
| **1** | Some AI use — the AI assisted but did not drive the work. |
| **2** | Extensive AI use — the AI did substantial work that was then reviewed and validated by the human author. |

Two important rules are enforced by the tool:

- A row that lists *only Support contributors* is invalid. Every role must have at least one Lead, Equal, or Sole contributor before you can export.
- A Sole contributor is mutually exclusive with everyone else on the same row.

### Saving and exporting

- **💾 Save sIfA** — saves your full state to a `.sifa.json` file. On Chromium-based browsers (Chrome, Edge, Arc, Opera) this opens a real "Save as…" dialog so you can choose a location; other browsers fall back to a regular download. The on-disk format is documented in [`docs/SCHEMA.md`](docs/SCHEMA.md), with a formal JSON Schema at [`docs/sifa.schema.json`](docs/sifa.schema.json). Note that this is distinct from the JSON metadata embedded inside an exported SVG: the SVG payload is a one-shot snapshot for downstream tooling, while `.sifa.json` is the canonical, round-trippable save format.
- **📂 Load sIfA** — reopens any previously saved `.sifa.json`. Full saves (`sifa-tool-state`) replace the current draft; portfolio-only saves (`sifa-portfolio`) merge their entries into whatever portfolio is already open.
- **💾 Save Portfolio** — available inside the portfolio panel. Writes a slimmer `.sifa.json` containing only the saved entries, without the current draft — useful for archiving or sharing a portfolio independently of an in-progress sIfA.
- **Autosave** — the tool quietly snapshots your work to browser local storage on every change, so reopening the file restores where you left off. A yellow banner appears when state has been restored; it offers a **↻ Start fresh** button to wipe the autosave and start over.
- **⬇ Export** — two SVG modes are available: *Table & Figure* (a composite suitable for supplementary documents) and *Figure only* (the standalone sIfA figure with citation footer). JPEG renderings are also available.
- **Export as CSV** — for pasting into a manuscript's contributor statement section or a spreadsheet.

### Worked example

A short, fictional sIfA for a paper on community health workers in three African countries:

| Role | Contributors | AI extent | Tool | How AI was used / audit trail |
| --- | --- | --- | --- | --- |
| Conceptualization | A. Okonkwo (Lead), B. Mensah (Equal) | 1 | ChatGPT | Used in early brainstorming to surface comparable studies; framing decided by authors. Chat log retained. |
| Investigation | A. Okonkwo (Lead), C. Otieno (Support) | 0 | — | Fieldwork; no AI involvement. |
| Formal Analysis | B. Mensah (Lead) | 2 | Claude | Coded interview transcripts with Claude; outputs reviewed manually and re-coded where the model misread tone. Export of model annotations retained. |
| Writing – original draft | A. Okonkwo (Lead) | 1 | ChatGPT | Drafted introduction paragraphs from author bullet notes; substantially rewritten by author. |
| Writing – review & editing | A. Okonkwo (Equal), B. Mensah (Equal), C. Otieno (Equal) | 1 | Grammarly | Language polish on final draft. |

All other CRediT roles in this fictional project were either not applicable or had no AI involvement. The exported sIfA figure would show an orange brain silhouette with five small purple sparkles — one per role above — at distances proportional to the AI extent for each role.

### What is *not* sent anywhere

The tool runs entirely in your browser. Nothing is uploaded, no analytics, no server. Specifically:

- Your contributor names, tools, and audit-trail notes never leave your computer.
- The autosave is in *your* browser's local storage, scoped to your machine.
- Closing the tab does not delete your work — autosave keeps it across sessions. To wipe it, click **↺ Reset**, or use the **↻ Start fresh** button in the restore banner.
- A downloaded `.sifa.json` file is yours to keep, share, or attach as a supplementary file.

---

## For developers

### Repository layout

```
.
├── Make your sIfA vX.X.html           # Online build — loads React/Babel from CDN
├── Make your sIfA vX.X (offline).html # Offline build — React/Babel inlined (~3 MB)
├── embed-libraries.py                 # Build script — produces the offline file
├── update-example.py                  # Refreshes the embedded example SVG inside both builds
├── example.svg                        # Canonical worked-example figure used by the About panel
├── archive/                           # Older versioned builds, kept for reference
├── README.md
├── LICENSE
├── CHANGELOG.md
├── CONTRIBUTING.md
├── CITATION.cff
├── docs/
│   ├── SCHEMA.md                      # .sifa.json format — friendly overview
│   └── sifa.schema.json               # JSON Schema (draft 2020-12) for .sifa.json
└── .github/
    └── ISSUE_TEMPLATE/
```

### Running and editing

There is no build pipeline for development. The HTML file loads React 18 and Babel Standalone from a CDN and transpiles the JSX in the browser:

```bash
# Just open the file
open "Make your sIfA vX.X.html"

# Or serve it (useful when iterating on CORS-sensitive features)
python3 -m http.server 8000
# then visit http://localhost:8000/Make%20your%20sIfA%20vX.X.html
```

To edit, open the `<script type="text/babel">` block inside `Make your sIfA vX.X.html`, change what you want, and refresh the browser. Babel Standalone re-transpiles on every page load.

For production / distribution there is an offline build that inlines React and Babel directly into the HTML so the file works without any internet connection — useful for low-connectivity research contexts. See [Build](#build-how-the-offline-file-is-generated).

### Architecture in one paragraph

A single React functional component (`App`) holds the entire tool's state. The tool ships as one HTML file with React, Babel Standalone, and the component source loaded inline. The figure is rendered as an SVG inside React. Exports are produced by serialising that SVG (and, for the composite mode, prepending a hand-built SVG of the table) into a Blob, then handing it to either a download link or the File System Access API. There is no backend, no router, no bundler, and no external state store.

### State model

The main editable state lives in one object keyed by role ID:

```js
const data = {
  conceptualization: {
    contributors: [
      { name: 'A. Okonkwo', level: 'Lead',  tool: 'ChatGPT', reason: '…', extent: 1 },
      { name: 'B. Mensah',  level: 'Equal', tool: '',        reason: '',  extent: 0 }
    ],
    tool: '',              // role-level fallback (used when no contributors are set)
    reason: '',
    extent: 0,             // computed from contributors when contributors > 0
    skipped: false         // user explicitly hid this row
  },
  // ...one entry per active role
};
```

Other top-level state:

- `activeRoles` — the currently active role set. Default is the 14 CRediT roles; if a custom taxonomy is in use, this becomes the user's roles instead.
- `taxonomyMode` — `'credit'` or `'custom'`.
- `portfolio` — saved comparison entries (a separate feature for aggregating multiple sIfAs).
- `figureFont` — `'montserrat' | 'georgia' | 'inter'`.
- `restoredNotice` — whether the "↻ Restored your previous sIfA" banner is showing.

The autosave runs as a `useEffect` whose dependency list is exactly the user-editable state. The key is `STORAGE_KEY = 'sifa_autosave_v1'`. Bumping this key (e.g. on a breaking schema change) effectively resets autosaves for all users.

The on-disk `.sifa.json` save format is a serialised superset of this in-memory state. See [`docs/SCHEMA.md`](docs/SCHEMA.md) for the human overview and [`docs/sifa.schema.json`](docs/sifa.schema.json) for the formal schema.

### Adding or changing roles

The 14 CRediT roles live in the `ROLES` array near the top of the source. Each entry has an `id`, `label`, `def` (definition), and three colours (`bg`, `accent`, `border`). To add a role:

```js
const ROLES = [
  // ...
  { id: 'my_new_role',
    label: 'My New Role',
    def: 'One-line definition shown in the tooltip.',
    bg: '#…', accent: '#…', border: '#…' },
];
```

Anything keyed off `id` (the table, the agent flow, the figure axes, CSV export) picks up the new role automatically.

For *custom* taxonomies (defined by the end user at runtime), `buildCustomRoles(labels)` constructs fresh role objects from a list of free-text labels, assigning colours from `CUSTOM_COLORS` in rotation; the agent flow uses this for a brand-new taxonomy. The in-table "Set up my own taxonomy" / "Edit my taxonomy" button instead funnels through `mergeCustomRoles(entries, currentRoles)`, which preserves the `id` (and therefore all existing data) for any role that's unchanged — including CRediT roles, whose real ids don't always match what `buildCustomRoles` would slugify from the label — and only mints a new id/colour for genuinely new rows.

### Build: how the offline file is generated

`embed-libraries.py` is a small Python script that:

1. Reads `Make your sIfA vX.X.html`.
2. Downloads (or reads from cache) the React production build, React-DOM, and Babel Standalone.
3. Inlines all three into `<script>` tags in place of the CDN `<script src=…>` references.
4. Writes `Make your sIfA vX.X (offline).html`.

Both files contain the same JSX. The offline build is roughly 17× larger (around 3 MB vs 180 KB) due to the inlined React + Babel.

`update-example.py` is a companion script that refreshes the worked example shown inside the About panel. Open the latest build, fill in the example you want frozen, export *Table & Figure · SVG*, save it as `example.svg` next to the script, then run `python3 update-example.py` to rewrite the `EXAMPLE_SVG` block inside both the online and offline HTML files.

### Known limitations

- The tool runs Babel Standalone in the browser. This is fine for a single-file app at this size but adds a 1–2 second cold-start cost on slower machines.
- The File System Access API used for "Save as…" only exists in Chromium-based browsers. Firefox and Safari fall back to a normal download to the Downloads folder.
- Autosaves are scoped to one browser on one machine. There is no sync. Use **💾 Save sIfA** to produce a portable `.sifa.json`.
- The conversational agent uses simple keyword matching for yes/no parsing — not an LLM — so unusual phrasings ("nope nope nope") may not be detected. Falling back to clicking the visible buttons is always reliable.
- CSV export escapes quotes minimally. Audit-trail notes containing many quotation marks may need a manual pass.

---

## Citation

If you use sIfA in published work, please cite it using the form below. The DOI resolves via Zenodo and always points to the latest release.

> Schomerus, Mareike. *sIfA Tool (Tool to create a Statement of Intellectual Fellowship and Accountability).* Version 1.3. 2026. Busara. https://doi.org/10.5281/zenodo.20285993

A machine-readable version of the same information is in [`CITATION.cff`](CITATION.cff), which GitHub uses to populate the "Cite this repository" button.

For ready-to-paste attribution text in different contexts — papers, figure captions, slide decks, project websites — see [`HOW_TO_CITE.md`](HOW_TO_CITE.md).

The underlying contributor-role taxonomy is the [NISO CRediT standard](https://credit.niso.org); please credit it separately in any extended documentation of how a sIfA was compiled.

---

## License

Released under the **Apache License 2.0** — see [`LICENSE`](LICENSE) for the full text and [`NOTICE`](NOTICE) for the attribution notice that travels with redistributions.

In short: you can use, modify, and distribute sIfA freely, including in commercial settings, provided that:

- You include a copy of the licence with any redistribution.
- You preserve the copyright, patent, trademark, and attribution notices (including the contents of the `NOTICE` file).
- You note in any modified files that you changed them.

Apache 2.0 also grants you an explicit patent licence — a small extra protection over MIT — and uses a `NOTICE` mechanism so attribution remains visible to downstream users, not buried inside source code.

---

## Acknowledgements

The fellowship/accountability framing was developed alongside Busara's wider work on responsible AI use in social-science research. The CRediT taxonomy is maintained by NISO and used by most major academic publishers.
