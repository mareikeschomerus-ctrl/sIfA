"""
build.py — regenerates index.html from content.md
Run: python3 build.py
"""

import base64, re, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SVG_PATH = os.path.join(HERE, "..", "example.svg")
CONTENT_PATH = os.path.join(HERE, "content.md")
OUTPUT_PATH = os.path.join(HERE, "index.html")


def load_fields(path):
    fields = {}
    with open(path, encoding="utf-8") as f:
        text = f.read()
    for m in re.finditer(r'\[FIELD:\s*(\w+)\](.*?)\[END\]', text, re.DOTALL):
        key = m.group(1).strip()
        value = m.group(2).strip()
        fields[key] = value
    return fields


def load_svg_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def load_disclosure_svg_b64(here):
    path = os.path.join(here, "website.sifa.json.svg")
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def build(fields, svg_b64, disclosure_b64=None):
    # Helper: highlight part of hero headline
    if disclosure_b64:
        disclosure_section = f"""<section class="disclosure-section">
  <div class="container-wide">
    <h2>sIfA Statement</h2>
    <p class="disclosure-note">This is the sIfA disclosure for the creation of this website only — it records how humans and AI interacted in building these pages, not in the sIfA tool itself. Generated with <a href="{fields["github_url"]}" style="color:var(--purple-mid);">sIfA v1.3</a>.</p>
    <div class="disclosure-figure">
      <img src="data:image/svg+xml;base64,{disclosure_b64}" alt="sIfA statement for the creation of this website">
    </div>
  </div>
</section>"""
    else:
        disclosure_section = ""

    headline = fields["hero_headline"]
    highlight = fields["hero_headline_highlight"]
    headline_html = headline.replace(highlight, f'<span>{highlight}</span>', 1)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{fields["page_title"]}</title>
  <meta name="description" content="{fields["page_description"]}">
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

    :root {{
      --purple-deep:  #3B1D7F;
      --purple-mid:   #6E55D6;
      --purple-light: #8C78E0;
      --orange:       #DD5510;
      --orange-dark:  #C2410C;
      --slate-900:    #0F172A;
      --slate-700:    #334155;
      --slate-500:    #64748B;
      --slate-200:    #E2E8F0;
      --slate-50:     #F8FAFC;
      --white:        #FFFFFF;
    }}

    html {{ scroll-behavior: smooth; }}

    body {{
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Inter, Helvetica, Arial, sans-serif;
      font-size: 18px;
      line-height: 1.65;
      color: var(--slate-700);
      background: var(--white);
    }}

    nav {{
      position: sticky; top: 0; z-index: 100;
      background: var(--purple-deep);
      padding: 0.75rem 2rem;
      display: flex; align-items: center; justify-content: space-between;
    }}
    .nav-brand {{
      color: var(--white);
      font-size: 1.1rem; font-weight: 700; letter-spacing: 0.04em;
      text-decoration: none;
    }}
    .nav-left {{ display: flex; align-items: center; gap: 1.25rem; }}
    .nav-busara-logo {{
      height: 30px; width: auto; opacity: 1;
      transition: opacity 0.15s;
      filter: brightness(0) invert(1);
    }}
    .nav-busara-logo:hover {{ opacity: 0.8; }}
    .nav-links {{ display: flex; gap: 1.75rem; }}
    .nav-links a {{
      color: rgba(255,255,255,0.8);
      text-decoration: none; font-size: 0.9rem;
      transition: color 0.15s;
    }}
    .nav-links a:hover {{ color: var(--white); }}

    section {{ padding: 4rem 1.5rem; }}
    .container {{ max-width: 820px; margin: 0 auto; }}
    .container-wide {{ max-width: 1060px; margin: 0 auto; }}

    .hero {{
      background: linear-gradient(135deg, var(--purple-deep) 0%, #1E0F5C 100%);
      color: var(--white);
      padding: 5rem 1.5rem 4rem;
      text-align: center;
    }}
    .hero-eyebrow {{
      display: inline-block;
      background: rgba(255,255,255,0.12);
      border: 1px solid rgba(255,255,255,0.25);
      border-radius: 2rem;
      padding: 0.3rem 1rem;
      font-size: 0.82rem; font-weight: 600; letter-spacing: 0.08em;
      text-transform: uppercase; color: rgba(255,255,255,0.85);
      margin-bottom: 1.5rem;
    }}
    .hero h1 {{
      font-size: clamp(2rem, 5vw, 3.25rem);
      font-weight: 800; line-height: 1.15;
      margin-bottom: 1.25rem;
    }}
    .hero h1 span {{ color: #F4A26B; }}
    .hero-sub {{
      font-size: 1.15rem; max-width: 600px; margin: 0 auto 2.5rem;
      color: rgba(255,255,255,0.82); line-height: 1.6;
    }}
    .download-pair {{
      display: flex; gap: 1.25rem; justify-content: center; flex-wrap: wrap;
      margin-bottom: 0;
    }}
    .download-option {{
      display: flex; flex-direction: column; align-items: center; gap: 0.5rem;
    }}
    .btn-download {{
      display: inline-flex; align-items: center; gap: 0.6rem;
      background: var(--orange);
      color: var(--white);
      font-size: 1rem; font-weight: 700;
      padding: 0.9rem 1.75rem;
      border-radius: 0.5rem;
      text-decoration: none;
      transition: background 0.15s, transform 0.1s;
      box-shadow: 0 4px 18px rgba(221,85,16,0.45);
      white-space: nowrap;
    }}
    .btn-download:hover {{ background: var(--orange-dark); transform: translateY(-1px); }}
    .btn-download-secondary {{
      background: transparent;
      border: 2px solid rgba(255,255,255,0.6);
      box-shadow: none;
    }}
    .btn-download-secondary:hover {{ background: rgba(255,255,255,0.1); transform: translateY(-1px); }}
    .download-note {{
      font-size: 0.8rem; color: rgba(255,255,255,0.6); text-align: center; max-width: 180px;
    }}
    .hero-footnote {{
      margin-top: 1rem;
      font-size: 0.85rem; color: rgba(255,255,255,0.6);
    }}
    .badge-row {{
      margin-top: 2.5rem; display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap;
    }}
    .badge-row a {{ display: inline-block; }}
    .badge-row img {{ height: 22px; }}

    .what-it-is {{ background: var(--slate-50); }}
    .what-it-is h2 {{
      font-size: 1.6rem; font-weight: 700;
      color: var(--slate-900); margin-bottom: 1rem;
    }}
    .what-it-is p {{ margin-bottom: 1rem; }}
    .what-it-is p:last-child {{ margin-bottom: 0; }}

    .steps {{ background: var(--white); }}
    .steps h2 {{
      font-size: 1.6rem; font-weight: 700;
      color: var(--slate-900); text-align: center; margin-bottom: 3rem;
    }}
    .steps-grid {{
      display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 2rem;
    }}
    .step {{
      border: 1px solid var(--slate-200);
      border-radius: 0.75rem;
      padding: 2rem 1.75rem;
    }}
    .step-num {{
      width: 2.5rem; height: 2.5rem;
      background: var(--purple-deep); color: var(--white);
      border-radius: 50%;
      display: flex; align-items: center; justify-content: center;
      font-weight: 800; font-size: 1rem;
      margin-bottom: 1rem;
    }}
    .step h3 {{ font-size: 1.05rem; font-weight: 700; margin-bottom: 0.5rem; color: var(--slate-900); }}
    .step p {{ font-size: 0.95rem; color: var(--slate-500); line-height: 1.5; }}

    .figure-section {{ background: var(--slate-50); }}
    .figure-section h2 {{
      font-size: 1.6rem; font-weight: 700;
      color: var(--slate-900); text-align: center; margin-bottom: 0.75rem;
    }}
    .figure-caption {{
      text-align: center; color: var(--slate-500); font-size: 0.95rem;
      max-width: 580px; margin: 0 auto 2.5rem;
    }}
    .figure-wrapper {{
      border: 1px solid var(--slate-200);
      border-radius: 0.75rem;
      overflow: hidden;
      background: var(--white);
      padding: 1.5rem;
      text-align: center;
    }}
    .figure-wrapper img {{ max-width: 100%; height: auto; display: block; margin: 0 auto; }}

    .who-section {{ background: var(--white); }}
    .who-section h2 {{
      font-size: 1.6rem; font-weight: 700;
      color: var(--slate-900); text-align: center; margin-bottom: 3rem;
    }}
    .who-grid {{
      display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 1.5rem;
    }}
    .who-card {{
      background: var(--slate-50);
      border-radius: 0.75rem;
      padding: 1.5rem;
    }}
    .who-card h3 {{
      font-size: 0.95rem; font-weight: 700;
      color: var(--purple-deep); margin-bottom: 0.5rem;
    }}
    .who-card p {{ font-size: 0.9rem; color: var(--slate-500); line-height: 1.5; }}

    .privacy-section {{
      background: linear-gradient(135deg, #1E0F5C, var(--purple-deep));
      color: var(--white); text-align: center;
    }}
    .privacy-section h2 {{ font-size: 1.5rem; font-weight: 700; margin-bottom: 1rem; }}
    .privacy-section p {{
      color: rgba(255,255,255,0.82); max-width: 560px; margin: 0 auto 0.75rem;
      font-size: 0.97rem;
    }}
    .privacy-list {{
      list-style: none; margin: 1.5rem auto 0; max-width: 480px; text-align: left;
    }}
    .privacy-list li {{
      padding: 0.4rem 0;
      color: rgba(255,255,255,0.8); font-size: 0.95rem;
      display: flex; align-items: flex-start; gap: 0.6rem;
    }}
    .privacy-list li::before {{ content: "✓"; color: #7DDBB8; font-weight: 700; flex-shrink: 0; }}

    .citation-section {{ background: var(--slate-50); }}
    .citation-section h2 {{
      font-size: 1.6rem; font-weight: 700;
      color: var(--slate-900); margin-bottom: 1.25rem;
    }}
    .cite-block {{
      background: var(--white);
      border-left: 4px solid var(--purple-mid);
      border-radius: 0 0.5rem 0.5rem 0;
      padding: 1.25rem 1.5rem;
      font-size: 0.95rem; color: var(--slate-700);
      font-style: italic; line-height: 1.7;
      margin-bottom: 1.25rem;
    }}
    .doi-link {{ color: var(--purple-mid); text-decoration: none; font-style: normal; font-weight: 600; }}
    .doi-link:hover {{ text-decoration: underline; }}
    .citation-note {{ font-size: 0.9rem; color: var(--slate-500); }}

    .disclosure-section {{ background: var(--slate-50); }}
    .disclosure-section h2 {{
      font-size: 1.6rem; font-weight: 700;
      color: var(--slate-900); margin-bottom: 0.75rem;
    }}
    .disclosure-note {{
      font-size: 0.95rem; color: var(--slate-500);
      max-width: 640px; margin-bottom: 2rem; line-height: 1.6;
    }}
    .disclosure-figure {{
      border: 1px solid var(--slate-200);
      border-radius: 0.75rem;
      background: var(--white);
      padding: 1.5rem;
      text-align: center;
    }}
    .disclosure-figure img {{ max-width: 100%; height: auto; display: block; margin: 0 auto; }}

    .licence-section {{ background: var(--white); }}
    .licence-section h2 {{
      font-size: 1.6rem; font-weight: 700;
      color: var(--slate-900); margin-bottom: 1rem;
    }}
    .licence-section p {{ margin-bottom: 0.75rem; font-size: 0.95rem; color: var(--slate-500); }}
    .licence-legal {{
      font-size: 0.82rem !important;
      color: var(--slate-500);
      line-height: 1.6;
      border-top: 1px solid var(--slate-200);
      padding-top: 0.75rem;
      margin-top: 0.75rem;
    }}

    footer {{
      background: var(--slate-900);
      color: rgba(255,255,255,0.6);
      padding: 2rem 1.5rem;
      text-align: center; font-size: 0.875rem;
    }}
    footer a {{ color: rgba(255,255,255,0.75); text-decoration: none; }}
    footer a:hover {{ color: var(--white); }}
    footer .footer-links {{
      display: flex; justify-content: center; gap: 1.5rem;
      flex-wrap: wrap; margin-bottom: 0.75rem;
    }}
    footer .footer-sep {{ color: rgba(255,255,255,0.3); }}

    @media (max-width: 600px) {{
      .nav-links {{ display: none; }}
      .steps-grid {{ grid-template-columns: 1fr; }}
      .who-grid {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>

<nav>
  <div class="nav-left">
    <a class="nav-brand" href="#">sIfA</a>
    <a href="https://busara.global" target="_blank" rel="noopener">
      <img class="nav-busara-logo" src="busara-logo.png" alt="Busara">
    </a>
  </div>
  <div class="nav-links">
    <a href="#how-it-works">How it works</a>
    <a href="#figure">Example</a>
    <a href="#who">Who is it for</a>
    <a href="#citation">Cite</a>
    <a href="{fields["github_url"]}">GitHub</a>
  </div>
</nav>

<section class="hero">
  <div class="container">
    <p class="hero-eyebrow">{fields["hero_eyebrow"]}</p>
    <h1>{headline_html}</h1>
    <p class="hero-sub">{fields["hero_subheading"]}</p>
    <div class="download-pair">
      <div class="download-option">
        <a class="btn-download" href="{fields["download_url_online"]}">
          &#8595;&nbsp;{fields["download_button_online_label"]}
        </a>
        <span class="download-note">{fields["download_button_online_note"]}</span>
      </div>
      <div class="download-option">
        <a class="btn-download btn-download-secondary" href="{fields["download_url_offline"]}">
          &#8595;&nbsp;{fields["download_button_offline_label"]}
        </a>
        <span class="download-note">{fields["download_button_offline_note"]}</span>
      </div>
    </div>
    <p class="hero-footnote">{fields["hero_footnote"]}</p>
    <div class="badge-row">
      <a href="{fields["zenodo_doi"]}">
        <img src="https://zenodo.org/badge/DOI/10.5281/zenodo.20285993.svg" alt="DOI badge">
      </a>
    </div>
  </div>
</section>

<section class="figure-section" id="figure">
  <div class="container-wide">
    <h2>{fields["figure_heading"]}</h2>
    <p class="figure-caption">{fields["figure_caption"]}</p>
    <div class="figure-wrapper">
      <img src="data:image/svg+xml;base64,{svg_b64}" alt="{fields["figure_alt"]}">
    </div>
  </div>
</section>

<section class="what-it-is">
  <div class="container">
    <h2>{fields["what_heading"]}</h2>
    <p>{fields["what_para_1"]}</p>
    <p>{fields["what_para_2"]}</p>
    <p>{fields["what_para_3"]}</p>
  </div>
</section>

<section class="steps" id="how-it-works">
  <div class="container">
    <h2>{fields["steps_heading"]}</h2>
    <div class="steps-grid">
      <div class="step">
        <div class="step-num">1</div>
        <h3>{fields["step1_heading"]}</h3>
        <p>{fields["step1_body"]}</p>
      </div>
      <div class="step">
        <div class="step-num">2</div>
        <h3>{fields["step2_heading"]}</h3>
        <p>{fields["step2_body"]}</p>
      </div>
      <div class="step">
        <div class="step-num">3</div>
        <h3>{fields["step3_heading"]}</h3>
        <p>{fields["step3_body"]}</p>
      </div>
    </div>
  </div>
</section>

<section class="who-section" id="who">
  <div class="container">
    <h2>{fields["who_heading"]}</h2>
    <div class="who-grid">
      <div class="who-card">
        <h3>{fields["who_card1_heading"]}</h3>
        <p>{fields["who_card1_body"]}</p>
      </div>
      <div class="who-card">
        <h3>{fields["who_card2_heading"]}</h3>
        <p>{fields["who_card2_body"]}</p>
      </div>
      <div class="who-card">
        <h3>{fields["who_card3_heading"]}</h3>
        <p>{fields["who_card3_body"]}</p>
      </div>
      <div class="who-card">
        <h3>{fields["who_card4_heading"]}</h3>
        <p>{fields["who_card4_body"]}</p>
      </div>
      <div class="who-card">
        <h3>{fields["who_card5_heading"]}</h3>
        <p>{fields["who_card5_body"]}</p>
      </div>
    </div>
  </div>
</section>

<section class="privacy-section">
  <div class="container">
    <h2>{fields["privacy_heading"]}</h2>
    <p>{fields["privacy_intro"]}</p>
    <ul class="privacy-list">
      <li>{fields["privacy_bullet_1"]}</li>
      <li>{fields["privacy_bullet_2"]}</li>
      <li>{fields["privacy_bullet_3"]}</li>
      <li>{fields["privacy_bullet_4"]}</li>
    </ul>
  </div>
</section>

<section class="citation-section" id="citation">
  <div class="container">
    <h2>{fields["citation_heading"]}</h2>
    <p style="font-size:0.9rem;color:var(--slate-500);margin-bottom:0.5rem;">Cite the tool:</p>
    <div class="cite-block">{fields["citation_text"]}</div>
    <p style="font-size:0.9rem;color:var(--slate-500);margin-bottom:0.5rem;margin-top:1.5rem;">Cite the paper:</p>
    <div class="cite-block">{fields["paper_citation"]}</div>
    <p class="citation-note">{fields["citation_note"]}</p>
  </div>
</section>

{disclosure_section}

<footer>
  <div class="footer-links">
    <a href="{fields["github_url"]}">GitHub repository</a>
    <span class="footer-sep">·</span>
    <a href="{fields["zenodo_doi"]}">Zenodo record</a>
    <span class="footer-sep">·</span>
    <a href="{fields["github_url"]}/blob/main/CHANGELOG.md">Changelog</a>
    <span class="footer-sep">·</span>
    <a href="{fields["github_url"]}/blob/main/LICENSE">Apache 2.0 licence</a>
  </div>
  <p>{fields["footer_credit"]}</p>
</footer>

</body>
</html>"""


def main():
    if not os.path.exists(CONTENT_PATH):
        print(f"Error: content.md not found at {CONTENT_PATH}")
        sys.exit(1)
    if not os.path.exists(SVG_PATH):
        print(f"Error: example.svg not found at {SVG_PATH}")
        sys.exit(1)

    fields = load_fields(CONTENT_PATH)
    svg_b64 = load_svg_b64(SVG_PATH)
    disclosure_b64 = load_disclosure_svg_b64(HERE)
    html = build(fields, svg_b64, disclosure_b64)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Built index.html ({len(html):,} bytes)")
    print(f"Open it with: open \"{OUTPUT_PATH}\"")


if __name__ == "__main__":
    main()
