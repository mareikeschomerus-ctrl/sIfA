# Changelog

All notable changes to the sIfA tool are documented in this file. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project follows [Semantic Versioning](https://semver.org/) from v1.0 onwards.

## [Unreleased]

### Added
- **Project name.** A new "Project: …" button in the toolbar (next to 🎨 Colours) lets you tag the current sIfA with a free-text project label. It's saved with the file (`projectName`) and carried automatically onto portfolio entries when you add to or refresh them from the draft, so a portfolio can hold sIfAs from several projects without re-typing which is which. Shown under each entry's summary in the Portfolio panel.

### Changed
- **💾 Save sIfA and 💾 Save Portfolio now overwrite the same file on repeat saves**, instead of prompting for a new filename every time. The first save still opens a normal "Save as…" dialog; the tool remembers that file handle — persisted via IndexedDB, so it survives a page reload, not just the current tab session — and writes straight to it on every subsequent save, in browsers that support the File System Access API (Chromium-based). After a reload, the browser may ask for one quick "Allow access to [filename]?" click before the first save (its own security gate, not a full re-pick of the file); after that it's silent again for the rest of that session. Loading a *different* `.sifa.json` resets this, since you're then working on a different document. Browsers without that API (e.g. Safari, Firefox) keep the previous download-a-new-file-each-time behaviour, which is a platform limitation rather than a tool choice.
- **Figure: internal brain "sulci" texture lines removed.** The five faint curved fissure lines that ran across the brain shape (mostly horizontal) were reported as confusing rather than illustrative and have been dropped. The organic ring texture and outline remain.
- **Figure: role-to-centre lines strengthened.** Each axis now has a solid line running from the centre "0" out toward its label, coloured to match that role's own accent colour (same colour as its label text and data marker), replacing the previous near-invisible white line that stopped well short of the label and was clipped inside the brain shape. Makes it much clearer which label belongs to which axis and data point.
- **Figure: AI blob widened and strengthened.** A lone value of 1 sitting between two axes at 0 used to collapse to a thin spike that the soft blur all but erased. Each axis now contributes a small angular "shoulder" either side of its data point (capped so it can never overlap a neighbouring axis, however many roles are active) instead of a single point, and fill/stroke opacity on the blob and its glow layers are higher — so an isolated value now reads as a clear, wide patch while the edges stay soft.

## [1.3] — 2026-07-05

### Added
- **"0" scale badge at the centre of the figure**, matching the existing "1" and "2" badges on the rings — the centre point (no AI use) is now explicitly labelled rather than left to be inferred.
- **Add a role to a taxonomy already in use.** "Edit my taxonomy" / "Set up my own taxonomy" now always pre-fills with whatever roles are currently active — the full CRediT list, an existing custom list, or one just reloaded from a `.sifa.json` — so appending one new role no longer means retyping the rest. This also means CRediT can now be extended with extra custom roles directly, rather than only being replaced outright. Saving still switches the taxonomy mode to custom, since a mixed CRediT-plus-extra list is no longer pure CRediT; the modal explains this before you commit.
- **"Start a new taxonomy" button.** When the taxonomy picker opens pre-filled from CRediT (offered as a starting point), a new button clears the list to a blank slate for anyone who'd rather build their own from scratch rather than edit the CRediT list down.
- **Describe a role as you add it.** Adding a new role at the bottom of the taxonomy picker now opens its definition field immediately, so a description can be entered in the same step rather than as a separate follow-up click. Definitions can also be added or edited for CRediT roles, not just custom ones.
- **Extent boxes redesigned.** The clickable 1/2 extent boxes (per contributor, and the standalone role-level selector) are bigger. Selecting level 2 still colours both boxes (as before), but now only the box matching the selected level shows its number — selecting "2" no longer shows a "1" in the first box. Where extent is zero, the live table shows a plain white box labelled "0" alongside the 1/2 boxes; the exported table/figure shows a plain "0" as text instead (no box, since nothing there is clickable). The contributor's name is no longer repeated in the extent column — it lines up with the name already shown in "Performed by". The exported table/figure's small extent-summary squares get the same bigger/numbered treatment (rounding a blended average to the nearer whole level for display).
- **"Extent of AI Use" renamed to "Extent of AI interaction"**, with a brief always-visible key — "0 none · 1 some · 2 extensive" — added under the header in both the live table and the exported table/figure.

### Changed
- **Exported figure crop actually fixed — take four.** The `getBBox()` measurement added last round was measuring the wrong thing: it was called on the whole chart, which includes a full-canvas white background rectangle, so the measured box was always the full 620×620 canvas regardless of how little was actually drawn — the crop was effectively a no-op. The chart's real content (brain shape, blob, badges, labels) is now wrapped in its own group and measured on its own, excluding that background rect, so the crop finally reflects what's actually there. The two earlier passes (a fixed-offset guess, then a still-too-generous fixed crop) are superseded by this.
- **Exported table redesigned to be more minimalist.** The dark title/header bars are gone in favour of a clean white background with black text; the subtitle ("AI interaction across contributor roles") now sits on the same line as the main title, in a smaller regular weight, instead of its own stacked line underneath. The column header row (Role / Performed by / Extent / etc.) is now shaded a light grey, one shade darker than the alternating row stripe below it, so it still reads clearly as a header against a mostly-white table. Row backgrounds are plain white with every other row tinted a light grey for readability, replacing the previous per-role pastel tint (the coloured accent bar and role-label colour still carry that signal) — both greys are fully neutral (equal R/G/B) so there's no colour cast. The AI region's boundary in the figure is now a soft, blurred edge rather than a hard purple outline.
- **Extent column narrowed, How-was-AI widened again.** The "0 none · 1 some · 2 extensive" key under the Extent header wasn't wrapping, which forced the whole column wider than its two small boxes need. It now wraps one level per line (0 / 1 / 2), so the column only needs to fit two boxes plus a short title; the freed-up width goes to "How was AI used", which carries the most text of any column.
- **Exported figure caption condensed.** The caption line under the chart no longer repeats the 0/1/2 scale explanation (now redundant with the on-chart badges and the table's "Extent of AI interaction" key) and reads simply "AI interaction across contributor roles"; the legend/disclaimer/CRediT-attribution block beneath the figure has tighter line spacing throughout. Applies to the composite table+figure export, the figure-only export, and the PDF/JPEG builds.
- **Figure axes only show roles that have been filled in**, dividing evenly across just those — reverting the v1.2 change that always plotted every non-skipped role regardless of whether anything had been entered. Falls back to showing all active roles if the sIfA is still completely blank, so a fresh figure doesn't render with zero axes. Applies everywhere the figure appears: the live chart panel, all exports (SVG, PDF, JPEG, composite table+figure), and the portfolio comparison chart.
- **Exported table column widths rebalanced.** "How was AI used?" typically carries the most text of any column but previously had less room than Tool/Service; the exported table/figure now gives it the most space, with Tool/Service narrowed accordingly. (The live on-screen table was already flexible here and is unchanged.)
- **Grey text changed to black throughout the app** — headers, tooltips, contributor labels, level tags, timestamps, disclaimers, and all exported SVG/PDF text. Deliberately-coloured elements (the 14 CRediT role accents, the custom-taxonomy colour palette, the mono/rainbow figure colour schemes) are unaffected, since those are colour choices rather than muted body text.
- **Updated worked example.** The embedded example in the About panel is regenerated from a fresh export, so it reflects the current table/figure design (minimalist table, cropped figure, etc.) rather than the v1.2-era layout.
- **"Desc" button relabelled "define"** on the taxonomy picker's per-role definition toggle, to read more clearly as an action on any role, CRediT included.

### Fixed
- **Silent data loss when rebuilding the CRediT list by hand.** Roles are matched internally by an ID slugified from the label. Three of the fourteen CRediT labels don't slugify back to the ID the tool actually uses ("Project Administration", "Writing – original draft", "Writing – review & editing"), so retyping the full CRediT list to add one extra role would have silently discarded any data already entered against those three roles. The taxonomy picker now carries each role's real ID through the edit, so unedited roles keep their data regardless of label/slug mismatches.

## [1.2] — 2026-06-05

### Added
- **All previously entered contributor names offered as autofill chips.** When a contributor name field is empty, every unique name already used elsewhere in the table appears as a clickable chip below the field — not just the first name. Cuts repeated typing across roles without limiting choice.
- **Orphan-reason prompt when a contributor is added.** If text has already been entered in the "How was AI used / Audit trail" column before any contributor is named, clicking "+ Add contributor" now surfaces a small inline prompt asking whether to assign that text to the new contributor or keep it as a general note. The text is never silently discarded.
- **Custom taxonomy role descriptions.** When setting up your own taxonomy, each role now has an optional description field (toggled with a "▼ desc" button per row). The description is stored in the role's `def` field and shown as a hover tooltip on the role name in the table — the same mechanism CRediT roles already use.
- **Portfolio inline link in About panel.** The word "portfolio" in the "save your work" paragraph is now a clickable link that opens the Portfolio panel directly.

### Changed
- **All contributor roles always shown in the figure.** The radar figure now includes every non-skipped role regardless of whether AI usage was declared. Previously only roles with data appeared on the axes; the remaining axes were added as a fallback only when nothing at all was filled in. Axes are always divided evenly across all active roles.
- **About panel: collapsed by default with prominent header.** The panel ships closed so the table is immediately visible on first load. The header has a dark background and carries a clearly labelled **▼ Expand / ▲ Collapse** button immediately adjacent to the title, so new users can find and open it without hunting for a small arrow.
- **sIfA brand badge enlarged.** The toolbar badge is larger and bolder (24 px / weight 900, version number at 85 % opacity) so the tool name is immediately legible.
- **Updated worked example.** The embedded example in the About panel is regenerated to show all 14 CRediT axes in the figure while keeping the same real sIfA data as before (Mareike Schomerus, sIfA Tool project).
- **PDF print layout improved.** The print stylesheet now targets A4 landscape, removes fixed viewport-height constraints so content flows to full length, prevents mid-row page breaks, ensures textareas render their content rather than clipping it, and hides interactive chrome (toolbar, autofill chips, prompts) from the printed output.

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
