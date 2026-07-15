# The `.sifa.json` file format

A `.sifa.json` file is the portable save format for the *Make your sIfA* tool. It captures everything the tool needs to reopen a Statement of Intellectual Fellowship and Accountability exactly as it was when it was saved — the active role taxonomy, every contributor on every role, the figure font choice, and any saved portfolio entries.

A formal JSON Schema describing the format lives at [`sifa.schema.json`](./sifa.schema.json) in this directory. It is written against JSON Schema **draft 2020-12** and can be used with any compatible validator (for example `ajv`, `python-jsonschema`, `check-jsonschema`).

This document is a friendly overview. The schema file itself is the source of truth.

---

## Two artefacts, two purposes

The tool produces **two** machine-readable JSON shapes, and it is worth keeping them straight because they look superficially similar:

- **The embedded SVG metadata** lives inside each exported sIfA figure (and inside the Table+Figure composite). It is a *per-export snapshot* — a frozen record of how the figure was generated, attached to the figure so a reader can recover the underlying data months or years later, even if the original `.sifa.json` is lost. It is intended for downstream tooling that wants to consume a sIfA figure as data.
- **The `.sifa.json` file** is the tool's *editable working state*. It round-trips: the tool writes it on save and reads it back on load. It comes in two flavours (see the next section).

The shapes are deliberately different. The embedded SVG metadata is flatter and includes a couple of human-readable fields (`schema`, `extentScale`) that explain the figure to a reader; `.sifa.json` is stricter, versioned, and validated against `sifa.schema.json`. A future change may add a small converter so an SVG-embedded payload can be lifted back into a `.sifa.json` on demand, but for now the two formats are independent and *only* `.sifa.json` is the canonical save format.

---

## Two file kinds: full state vs. portfolio-only

A `.sifa.json` file is identified by its `kind` field. The schema accepts two values:

- **`"sifa-tool-state"`** — written by the toolbar's **💾 Save sIfA** action. Captures the complete editable state: active role taxonomy, the current draft, the saved portfolio, and the figure font. On load, this *replaces* the current draft. Use it when you want a single file that travels with a paper or sits in a research-data archive.
- **`"sifa-portfolio"`** — written by **💾 Save Portfolio** inside the portfolio panel. Contains only the portfolio entries — no current draft, no taxonomy mode, no figure font. On load, the entries are *merged* into whatever portfolio is already open, and the current draft is left alone. Use it when you want to archive or share a collection of sIfAs without dragging an in-progress draft along, or to combine portfolios from multiple researchers into one.

The schema is structured as a top-level `oneOf` so either kind validates without false positives. A file claiming to be `"sifa-tool-state"` but missing `data` is rejected, as is a file claiming to be `"sifa-portfolio"` with no `portfolio` array.

---

## Why a schema

Three reasons:

1. **Interchange.** A `.sifa.json` can travel between researchers, into supplementary materials, or into a research-data archive. Without a schema there is no way for anyone but the original tool to know what shape to expect.
2. **Tool-checking.** When the tool loads a file, it can validate against the schema and refuse files it does not understand instead of partially loading something corrupt.
3. **Forward planning.** Future versions of the tool will add fields. Versioning the schema makes it explicit what is required, what is optional, and what counts as a breaking change.

---

## What a minimal valid file looks like

```json
{
  "version": 1,
  "kind": "sifa-tool-state",
  "savedAt": "2026-05-17T14:32:00.000Z",
  "activeRoles": [
    { "id": "conceptualization", "label": "Conceptualization", "def": "Ideas; formulation or evolution of overarching research goals and aims." }
  ],
  "taxonomyMode": "credit",
  "data": {
    "conceptualization": {
      "contributors": [
        { "name": "A. Okonkwo", "level": "Lead", "tool": "ChatGPT", "reason": "Brainstorming only", "extent": 1 }
      ],
      "extent": 1
    }
  }
}
```

A real file produced by the tool has all 14 CRediT roles in `activeRoles` and a matching key in `data` for each — but the schema only insists on at least one role being present, so smaller fixtures and test cases stay valid.

A minimal **portfolio-only** file looks like this — it omits the current draft, taxonomy mode, and figure font, since those are properties of the working session rather than of the portfolio itself:

```json
{
  "version": 1,
  "kind": "sifa-portfolio",
  "savedAt": "2026-05-17T20:57:00.000Z",
  "portfolio": [
    {
      "id": 1747490000000,
      "name": "Paper draft, March 2026",
      "taxonomyMode": "credit",
      "roles": [
        { "id": "conceptualization", "label": "Conceptualization" }
      ],
      "data": {
        "conceptualization": {
          "contributors": [
            { "name": "A. Okonkwo", "level": "Lead", "extent": 1 }
          ],
          "extent": 1
        }
      }
    }
  ]
}
```

Loading this file merges the listed entries into whatever portfolio the tool already has open; the current draft is left alone. Ids that happen to clash with existing entries are regenerated on import.

---

## Top-level fields

Required-ness depends on which `kind` the file claims to be. The table below shows both columns.

| Field | `sifa-tool-state` | `sifa-portfolio` | Notes |
| --- | --- | --- | --- |
| `version` | yes | yes | Schema major version. Currently `1`. The tool refuses files whose `version` it cannot read. |
| `kind` | yes (`"sifa-tool-state"`) | yes (`"sifa-portfolio"`) | Discriminator. Lets a file be recognised even without its `.sifa.json` extension. |
| `savedAt` | yes | yes | ISO 8601 timestamp. Informational only. |
| `activeRoles` | yes | — | Ordered list of roles. With CRediT this is the 14 standard roles; with a custom taxonomy it is the user's roles. Order is the table order. |
| `taxonomyMode` | yes | — | `"credit"` or `"custom"`. |
| `data` | yes | — | Object keyed by role id, with one entry per role that has any content. |
| `portfolio` | no | yes (≥1 entry) | List of saved sIfAs bundled together for comparison. In `sifa-tool-state` files it is an optional companion to the current draft; in `sifa-portfolio` files it is the entire payload. |
| `figureFont` | no | — | `"montserrat"`, `"georgia"`, or `"inter"`. Defaults to `"montserrat"` when missing. |
| `projectName` | no | — | Free-text label set via the toolbar's **Project** button (e.g. `"Op-Ed"`, `"WorldBank consultancy"`). Empty string or absent means unset. Portfolio entries created or refreshed from the draft carry this value onto `portfolio[].projectName`. |

---

## Engagement levels and AI extent

Two scales travel inside every contributor entry, and the README covers them in full. In short:

- **`level`** is one of `Sole`, `Lead`, `Equal`, `Support`, or `null`. A row with only `Support` contributors is invalid at export time, but the schema allows it on disk so partially filled drafts can still be saved.
- **`extent`** is a number from `0` to `2` in `0.5` steps. `0` = no AI use; `1` = some AI use; `2` = extensive. Half-steps appear only in older files; new files written by the tool use whole numbers.

---

## Versioning policy

The `version` field is a **major** version. Bumping it means an older tool cannot reliably load a newer file.

- *Additive changes* (new optional fields, new enum entries in places that already permit unknown values) do **not** bump `version`. They are documented in the schema and in [`CHANGELOG.md`](../CHANGELOG.md).
- *Renames, removals, semantic shifts* (e.g. changing the extent scale from 0–2 to 0–5) **do** bump `version`, and the tool will surface a "this file was made with a newer version" message instead of partially loading.

A migration helper may be provided in the tool to upgrade older files in place.

---

## Validating a file

Pick a validator that speaks draft 2020-12. A couple of examples:

```bash
# Python (recommended for one-off checks)
pip install check-jsonschema
check-jsonschema --schemafile docs/sifa.schema.json my-sifa.sifa.json

# Node
npx ajv-cli validate -s docs/sifa.schema.json -d my-sifa.sifa.json --spec=draft2020
```

The schema is intentionally strict (`additionalProperties: false` on every object) so that typos in hand-edited files surface immediately rather than silently disappearing on load.
