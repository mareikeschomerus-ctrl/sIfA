# Changelog

All notable changes to the sIfA tool are documented in this file. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project follows [Semantic Versioning](https://semver.org/) from v1.0 onwards.

## [1.1] — 2026-05-19

### Added
- **"Generative?" sub-question in the AI-use column.** The combined column header now exposes three hoverable sub-questions — *How was AI used?*, *Generative or non-generative?*, *Audit trail?* — each with its own tooltip explaining what to record. Encourages users to distinguish between AI generating new content and AI shaping or improving existing work.
- **Tool autocomplete via `<datalist>`.** Once a tool or service name (e.g. "Claude Sonnet 4.5") has been entered in one row, it appears as a suggestion in the *Tool / Service* field of every other row. Cuts repeated typing across the 14 roles.
- **Autosave-nudge banner.** After roughly 20 minutes of active editing without writing out a `.sifa.json`, a gentle banner reminds the user to save a portable copy. Dismisses on save or load.
- **Portfolio: overwrite-from-draft and load-into-draft.** Saved portfolio entries can now be (a) overwritten with the current draft via a small ⟳ button, and (b) loaded back into the working draft. Both actions are gated by a confirmation dialog so a stray click cannot replace or lose work.
- **Print stylesheet.** `@page { size: A4; margin: 12mm }` plus `break-inside: avoid` rules for the figure container and portfolio entries, so "Save as PDF" from the browser produces a clean A4 layout without splitting the figure across pages.

### Changed
- **About panel collapsed by default.** The 47-KB embedded example SVG is no longer parsed on first paint; it is only built when the user opens the panel. Reduces initial render cost noticeably on slower devices.
- **Tighter figure viewBox.** The chart viewBox is now `-25 0 670 620` (was 620 wide). The figure fills the panel rather than leaving blank space on the right.
- **Accessibility.** `aria-label` coverage expanded from 3 inputs to 11 — table cells, portfolio action buttons, and tool-suggestion inputs now announce themselves to screen readers. Default browser focus outlines suppressed in favour of the existing custom focus styles.

### Fixed
- **CSV export missing per-contributor data.** The *Tool / Service* and *How was AI used* columns in the exported CSV were silently empty because the function still read the legacy role-level `d.tool` / `d.reason` fields. They now come from `d.contributors[]`, with a fallback to the legacy fields for `.sifa.json` state imported from earlier versions.

- **CSV restructured into one row per contributor.** Each contributor in a role now sits on its own row so the per-contributor explanations are easy to follow downstream. The *CRediT Role* and the *Average extent of AI use across contributors* values appear once per role (on the first contributor row, blank on continuation rows), so the file opens as a grouped table — like merged cells in a spreadsheet — without losing any per-contributor detail. Roles with no contributors emit a single row carrying the legacy fields.

- **CSV columns rebuilt to mirror the questionnaire flow.** Column order is now *CRediT Role · Performed by · Extent of AI use per contributor · Average extent of AI use across contributors · How was AI used · Tool / Service*. The role *Definition* column and the redundant *Extent Label* column were dropped (definitions are still in the tool's tooltips, and the numeric extent plus the figure carry the same information). The previously stale *Extent (1-5)* header is gone.

- **Extent values formatted to one decimal place.** Per-contributor extents and the role-level average are both written as `0.0` / `1.0` / `1.5` etc., so downstream readers see a consistent numeric format rather than a mix of integers and long floating-point tails from the averaging step.

## [1.0] — 2026-05-16

First stable release. Consolidates the run of polish and bug-fix iterations through v0.9 into a citable, production-ready build.

### Added
- **Timestamped export filenames.** Every SVG and JPEG download now carries a `YYYY-MM-DD_HHmm` stamp (e.g. `sIfA Figure 2026-05-16_2104.svg`), so re-downloads no longer overwrite or get confused with older files.
- **Visible "Generated" line inside exported SVGs.** A small grey timestamp at the bottom of the citation block lets the reader verify when an export was produced.
- **"Citation —" prefix on the export footer.** The citation line in both composite and figure-only exports is explicitly labelled.

### Changed
- **Composite export columns rebalanced.** The *Extent of AI Use* column was narrowed and the saved space given to *Tool / Service*, so common service names ("Claude Sonnet 4.5", "Claude Opus 4.7") no longer get clipped. The *How was AI used?* header was shortened to two short lines (*How was AI used? / Audit trail?*) so it fits cleanly inside its column.
- **Footer text wraps dynamically.** Both export modes now use a word-wrap helper with conservative character limits, so long URLs in the footer always stay inside the figure regardless of font.
- **About panel rewritten.** New "What is sIfA?" copy, restructured "About sIfA" section leading with the Saleh & Schomerus (2026) reference, updated "Rights" with the GitHub URL inline, and the canonical citation rewritten to APA form.

### Fixed
- **× skip button is reachable for every role.** Previously, long role labels (Conceptualization, Project Administration) pushed the × out of the cell's hit area. The × is now absolutely positioned in the top-right corner of each role cell.

## [0.9] — 2026-05-15

### Added
- **Autofill for repeat contributors.** When a contributor name field is empty and a name has already been entered elsewhere in the table, a small role-coloured "↩ Use *[name]*" chip appears below the field. One click fills the name.
- **Start fresh button in the restore banner.** The yellow "↻ Restored your previous sIfA" banner now offers a one-click way to clear the autosave and reload the page. Confirmation prompt prevents accidental clicks.
- **Save as… dialog.** On Chromium-based browsers, 💾 Save sIfA now opens a real "Save as…" file picker via the File System Access API. Firefox and Safari fall back to the existing download flow.

### Changed
- **Licence changed from MIT to Apache 2.0.** Provides clearer attribution semantics via the new `NOTICE` file and adds an explicit patent grant. Existing usage rights remain comparably permissive — see `LICENSE` and `NOTICE` for details.
- **Figure colour palette.** Brain fill moved to a deeper, more saturated burnt orange (`#DD5510`) with higher fill opacity (0.46 → 0.72) so the colour holds against the white background. AI blob shifted to a cooler, less saturated purple (`#6E55D6` fill, `#5341BC` stroke). Sparkle palette adjusted to match.
- **Figure decorative lines** — sulci, organic rings, and axis spokes — increased in opacity and stroke width for better visibility.
- **AI sparkles** rendered slightly larger (radius 10 → 11) with bolder, more opaque strokes.
- **Extent-scale rings** (dashed markers at AI levels 1 and 2) drawn substantially bolder.

## [0.8] — 2026-05-12

### Added
- **Custom taxonomy modal.** "Use your own taxonomy" button at the top of the table opens a picker for defining custom role labels, accessible without going through the agent. The shared `buildCustomRoles` helper now powers both paths.
- **Figure-only SVG export** alongside the existing composite Table + Figure export. Standalone figure includes its own citation footer.
- **Three font choices** for the sIfA figure: Montserrat (default), Georgia, Inter.
- **Audit trail column** — auto-growing textarea that wraps long entries.

### Changed
- Engagement level vocabulary settled on **Sole / Lead / Equal / Support** ("Support", not "Supporting").
- Extent scale narrowed to 0–2 (was previously a wider 0–5 scale that researchers found hard to map onto practice).
- Radar legend wording standardised: *"Outer ring = Human · Centre = AI · Each axis = one contributor role"*.

## [0.7] — 2026-05-06

### Added
- **Downloadable `.sifa.json` save / load.** State can be exported to a portable file and reloaded later.
- **localStorage autosave** so reopening the file restores the last session.

## [0.6] — 2026-05-06

### Added
- Multiple contributors per role row, each with their own engagement level and AI extent.
- Per-role validation: rows with only Support contributors flagged before export.

## [0.5] — 2026-05-05

### Changed
- Major rework of the figure rendering — moved from a circular radar plot to the brain-shaped silhouette that distinguishes outer ring (human) from inner blob (AI).

## [0.4] — 2026-05-05

### Added
- Conversational agent flow alongside direct table entry.

## [0.3] — 2026-05-05

### Added
- Offline build (`Make your sIfA vX.X (offline).html`) with React, ReactDOM, and Babel Standalone inlined.
- `embed-libraries.py` build script.

## [0.2] — 2026-04-30

### Added
- CSV export.
- Per-role tooltips with the NISO CRediT definitions.

## [0.1] — 2026-04-27

Initial public draft. The 14 CRediT roles as a fillable table, with tool / reason / extent fields per role and an early radar-style figure.

## [0] — 2026-04-24

Internal prototype. Single HTML page, React functional component, table-only entry.
