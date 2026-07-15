# How to cite the sIfA Tool

Reusable attribution text for people who use the sIfA Tool in their own work. Pick the form that fits the context — a paper's reference list, a methods section, a slide-deck footer, a project website.

A few principles before the templates:

- The first time sIfA is mentioned in a piece of writing, spell out *Statement of Intellectual Fellowship and Accountability* in full. The full name carries the framing — fellowship signals that AI is named as a collaborator, accountability signals that the human author remains responsible — and the abbreviation makes more sense once a reader has seen it once.
- The underlying [CRediT Contributor Roles Taxonomy](https://credit.niso.org) is maintained by NISO and is independent of this tool. Credit it separately, alongside the sIfA citation, so neither obscures the other.
- The citation of the sIfA Tool itself stays the same regardless of how many authors a paper has. Individual contributors are named inside the sIfA, not in the tool's citation.

---

## Short citation (reference lists and bibliographies)

> Schomerus, M. (2026). *sIfA Tool — Statement of Intellectual Fellowship and Accountability* (Version 1.4) [Computer software]. Busara. https://doi.org/10.5281/zenodo.20285993

The DOI above is a *concept* DOI that always resolves to the latest version of the tool. Each released version also has its own version-specific DOI on Zenodo; use the concept DOI unless you need to pin to a precise version.

**BibTeX**

```bibtex
@software{Schomerus_sIfA_2026,
  author    = {Schomerus, Mareike},
  title     = {{sIfA Tool — Statement of Intellectual Fellowship and Accountability}},
  version   = {1.4},
  year      = {2026},
  month     = {7},
  publisher = {Busara},
  doi       = {10.5281/zenodo.20285993},
  url       = {https://github.com/mareikeschomerus-ctrl/sIfA}
}
```

A machine-readable equivalent lives in [`CITATION.cff`](CITATION.cff); GitHub uses it to populate the "Cite this repository" button.

---

## In-text mention (short form)

> The AI contribution statement for this paper was produced using the sIfA Tool (Schomerus, 2026).

---

## Methods or acknowledgements paragraph (full form)

> The structured statement of AI use accompanying this work was produced with the sIfA Tool — *Statement of Intellectual Fellowship and Accountability* (Schomerus, 2026), a browser-based tool that maps each contribution onto the 14 CRediT contributor roles maintained by NISO ([credit.niso.org](https://credit.niso.org)) and records, per role, who contributed, which AI tools were used, what they were used for, and how extensively the work depended on them. Responsibility for the contents of this paper rests with the human authors.

---

## Caption to the sIfA figure (when embedded in a paper or report)

> Figure X. Statement of Intellectual Fellowship and Accountability (sIfA) for this work, generated with the sIfA Tool v1.4 (Schomerus, 2026). The orange field represents human contribution; the inner purple shape represents AI contribution; each axis is one CRediT contributor role.

---

## Slide-deck or website footer (one-liner)

> sIfA generated with the sIfA Tool by Mareike Schomerus (Busara), released under the Apache License 2.0. https://doi.org/10.5281/zenodo.20285993.

---

## Acknowledgement of the underlying taxonomy (include alongside any sIfA citation)

> The contributor-role categories used in this statement are drawn from the CRediT Contributor Roles Taxonomy, a NISO standard available at https://credit.niso.org.

---

## A note on AI as a named contributor

A sIfA names AI tools (Claude, ChatGPT, Elicit, Grammarly, and so on) as contributors with their own rows of detail — what they were used for, how extensively, with what audit trail. This is intentional and central to the "fellowship" framing: AI is treated as a collaborator named in the work, not as an invisible utility used in the background.

When citing a paper that includes a sIfA, you do not need to cite the AI tools separately; the sIfA itself is the structured disclosure. If a journal or institution requires a separate AI-use statement in addition to the sIfA, the sIfA can be attached as a supplementary file or pasted into the contributor statement section verbatim.
