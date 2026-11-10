# sIfA Landing Page — Maintainer Notes

## Where the files live

| File | Location | What it is |
|---|---|---|
| `content.md` | `docs/content.md` | All page text — edit this in iA Writer |
| `build.py` | `docs/build.py` | Script that generates index.html from content.md |
| `index.html` | `docs/index.html` | The built page — never edit directly, always rebuild |
| `website.sifa.json.svg` | `docs/website.sifa.json.svg` | The sIfA disclosure figure for the website itself |
| `example.svg` | Root of repo | The sIfA example figure shown on the page — one level up from docs/ |

The live page is at: `https://www.sifatool.org` (custom domain since 10 November 2026; the old `mareikeschomerus-ctrl.github.io/sIfA` address forwards there).

The domain is registered at IONOS, set to DNS (not forwarding). The A record for `@` and the record for `www` point at GitHub Pages (185.199.108.153). `docs/CNAME` holds `www.sifatool.org`: don't delete it, or the custom domain is dropped. Leave the MX/TXT records alone; they run email for sifatool.org.

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

The website's download buttons never need editing. They point at
version-free filenames on GitHub's "latest release":

```
https://github.com/mareikeschomerus-ctrl/sIfA/releases/latest/download/Make.your.sIfA.html
https://github.com/mareikeschomerus-ctrl/sIfA/releases/latest/download/Make.your.sIfA.offline.html
```

So **every release must upload four files**: the two versioned builds, plus a
copy of each under the version-free name. From the repo root, for version X.Y.Z:

```bash
mkdir -p /tmp/sifa-stable
cp "Make your sIfA vX.Y.Z.html" "/tmp/sifa-stable/Make your sIfA.html"
cp "Make your sIfA vX.Y.Z (offline).html" "/tmp/sifa-stable/Make your sIfA (offline).html"
gh release create vX.Y.Z --verify-tag --title "vX.Y.Z" --notes-file <notes> \
  "Make your sIfA vX.Y.Z.html" "Make your sIfA vX.Y.Z (offline).html" \
  "/tmp/sifa-stable/Make your sIfA.html" "/tmp/sifa-stable/Make your sIfA (offline).html"
```

If a release goes out without the two version-free copies, both website buttons
404 until they are added (`gh release upload vX.Y.Z <the two files>`).

The "Latest version: …" and "Released …" lines on the buttons fill themselves
in: `build.py` reads the latest release's tag and publication date from GitHub
when you rebuild. So after a release, rebuild and push the site once so the
buttons show the new number and date. If GitHub can't be reached, the build
falls back to the version inside the newest tool file (dated from its git tag)
and prints a warning.

**If you fix something after a release, cut a new version.** Re-uploading files
to an existing release leaves the git tag, the changelog and the Zenodo archive
describing different code from what people download (this happened with v1.4 —
see the v1.4.1 changelog entry).

**On the offline filename:** GitHub's release-asset upload strips parentheses from
filenames entirely — it doesn't substitute them with anything, it just deletes them.
`Make your sIfA (offline).html` becomes the asset `Make.your.sIfA.offline.html`
(spaces become dots as usual, but `(` and `)` just vanish — no dot in their place). The
URL above already accounts for this; don't add `%28`/`%29` around "offline" or the
download link will 404 even though the release itself uploaded fine. Confirmed by testing
against the actual v1.4 release — the parenthesised URL 404s, this one 200s.

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
