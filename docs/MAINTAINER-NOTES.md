# sIfA Landing Page — Maintainer Notes

## Where the files live

| File | Location | What it is |
|---|---|---|
| `content.md` | `docs/content.md` | All page text — edit this in iA Writer |
| `build.py` | `docs/build.py` | Script that generates index.html from content.md |
| `index.html` | `docs/index.html` | The built page — never edit directly, always rebuild |
| `website.sifa.json.svg` | `docs/website.sifa.json.svg` | The sIfA disclosure figure for the website itself |
| `example.svg` | Root of repo | The sIfA example figure shown on the page — one level up from docs/ |

The live page is at: `https://mareikeschomerus-ctrl.github.io/sIfA`

---

## Editing the page text

1. Open `docs/content.md` in iA Writer
2. Edit the text between the `[FIELD: ...]` and `[END]` markers
3. Do not change the markers themselves
4. Save the file

---

## Rebuilding the page after edits

Always rebuild from the `docs/` folder:

```bash
cd "/Users/Mareike/Dropbox (Personal)/ Work/AI/sIfA AI contribution statement/docs"
python3 build.py
```

Check it looks right by opening `docs/index.html` in your browser before pushing.

---

## Pushing to GitHub

Run from the repo root (one level above `docs/`):

```bash
cd "/Users/Mareike/Dropbox (Personal)/ Work/AI/sIfA AI contribution statement"
git add docs/
git commit -m "your message here"
git push
```

Then watch the build at: `https://github.com/mareikeschomerus-ctrl/sIfA/actions`

Wait for a green tick on all three steps (build, report-build-status, deploy), then hard refresh the live page with **Cmd + Shift + R**.

---

## If deployment fails ("Deployment failed, try again later")

This is an intermittent GitHub Pages issue — not a problem with your files. Fix it with an empty commit:

```bash
cd "/Users/Mareike/Dropbox (Personal)/ Work/AI/sIfA AI contribution statement"
git commit --allow-empty -m "Retry deployment"
git push
```

This reliably clears it.

---

## Releasing a new version of the tool

When you publish a new version (e.g. v1.4), update two fields in `content.md`:

```
[FIELD: download_button_online_label]
Download online version
[END]

[FIELD: download_url_online]
https://github.com/mareikeschomerus-ctrl/sIfA/releases/latest/download/Make.your.sIfA.v1.4.html
[END]

[FIELD: download_url_offline]
https://github.com/mareikeschomerus-ctrl/sIfA/releases/latest/download/Make.your.sIfA.v1.4.offline.html
[END]
```

**On the offline filename:** GitHub's release-asset upload strips parentheses from
filenames entirely — it doesn't substitute them with anything, it just deletes them.
`Make your sIfA v1.4 (offline).html` becomes the asset `Make.your.sIfA.v1.4.offline.html`
(spaces become dots as usual, but `(` and `)` just vanish — no dot in their place). The
URL above already accounts for this; don't add `%28`/`%29` around "offline" or the
download link will 404 even though the release itself uploaded fine. Confirmed by testing
against the actual v1.4 release — the parenthesised URL 404s, this one 200s.

Then rebuild and push.

---

## Updating the sIfA disclosure figure for the website

If you redo the sIfA for the website itself:

1. Open the sIfA tool, load `website.sifa.json`, update and export as SVG
2. Save the new SVG as `docs/website.sifa.json.svg` (overwrite the old one)
3. Rebuild: `python3 build.py` from the `docs/` folder
4. Push

---

## GitHub authentication

Auth setup is documented once, centrally, in
`~/Dropbox (Personal)/ Work/exec-assistant/SETUP.md` (see "Fixing git
authentication properly, once") — check there rather than here so this
doesn't drift out of sync with the real state.

---

## GitHub Pages settings

If Pages ever stops working, check:
- `https://github.com/mareikeschomerus-ctrl/sIfA/settings/pages`
- Source: Deploy from a branch
- Branch: main, folder: /docs

Workflow permissions (if deployment keeps failing):
- `https://github.com/mareikeschomerus-ctrl/sIfA/settings/actions`
- Set to: Read and write permissions
