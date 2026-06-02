#!/usr/bin/env python3
"""Generate the UnSPACE portfolio: index.html + one page per project."""
import os, html, json

ROOT = os.path.dirname(os.path.abspath(__file__))

# ---- Shared fragments -------------------------------------------------
LOGO_SVG = (
    '<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
    '<rect x="6" y="6" width="88" height="88" stroke="#1a1a18" stroke-width="4"/>'
    '<line x1="50" y1="6" x2="50" y2="94" stroke="#1a1a18" stroke-width="4"/>'
    '<line x1="6" y1="50" x2="94" y2="50" stroke="#1a1a18" stroke-width="4"/>'
    '<line x1="50" y1="28" x2="94" y2="28" stroke="#1a1a18" stroke-width="4"/>'
    '<line x1="28" y1="50" x2="28" y2="94" stroke="#1a1a18" stroke-width="4"/>'
    '</svg>'
)

def header(active, depth=0):
    base = "../" if depth else ""
    def cls(name): return ' class="active"' if name == active else ''
    return f"""<header class="site-head">
    <div class="wrap">
      <a class="logo" href="{base}index.html" aria-label="UnSPACE home">
        {LOGO_SVG}
        <span class="mark-txt">UnSPACE</span>
      </a>
      <nav class="nav" id="nav">
        <a href="{base}index.html#work"{cls('work')}>Work</a>
        <a href="{base}index.html#recognition"{cls('recog')}>Recognition</a>
        <a href="{base}info.html"{cls('info')}>Info</a>
      </nav>
      <button class="nav-toggle" id="navToggle" aria-label="Open menu" aria-expanded="false">
        <span></span><span></span>
      </button>
    </div>
  </header>"""

def footer():
    return f"""<footer class="site-foot">
    <div class="wrap">
      <div class="foot-top">
        <h4>Where unconventional thinking meets meticulous craft.</h4>
        <div class="foot-col">
          <div class="lbl">Studio</div>
          <p>New York City</p>
          <p>Architecture &amp; Objectology</p>
        </div>
        <div class="foot-col">
          <div class="lbl">Connect</div>
          <a href="info.html#contact">Start a project</a>
          <a href="info.html">About the studio</a>
        </div>
      </div>
      <div class="foot-bottom">
        <span>&copy; 2025 UnSPACE</span>
        <span>Led by Rook Kim</span>
      </div>
    </div>
  </footer>"""

def head(title, depth=0, desc=""):
    base = "../" if depth else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(desc)}">
  <link rel="stylesheet" href="{base}assets/style.css">
</head>
<body>"""

# ---- Project data -----------------------------------------------------
# category: Unspace (spatial) | Objectology (product)
# shape: default(4:3) | tall(3:4) | wide(16:10)
PROJECTS = [
    {"slug":"broadway-1270","title":"1270 Broadway NYC Facade Redesign","cat":"Unspace","year":"2023",
     "summary":"A facade reimagined as an urban gesture — recomposing a historic Midtown frontage into a quietly assertive street presence.",
     "discipline":"Architecture · Facade","location":"Midtown, New York","shape":"default"},
    {"slug":"bowie-furniture","title":"Bowie Furniture","cat":"Objectology","year":"2022",
     "summary":"A folded-plane furniture study where a single continuous surface negotiates seat, support and sculpture.",
     "discipline":"Product · Furniture","location":"Studio series","shape":"default"},
    {"slug":"wearable-waterbag","title":"Wearable Waterbag","cat":"Objectology","year":"2021",
     "summary":"A modular hydration object — clustered spheres that read as both equipment and ornament.",
     "discipline":"Product · Wearable","location":"Concept","shape":"wide"},
    {"slug":"my-suit","title":"MY.SUIT","cat":"Unspace","year":"2019",
     "summary":"Retail architecture for a made-to-measure tailor, staging the ritual of fitting inside a restrained masonry envelope.",
     "discipline":"Architecture · Retail","location":"New York","shape":"tall"},
    {"slug":"namad-office-lobby","title":"NaMad Office Lobby","cat":"Unspace","year":"2020",
     "summary":"A lobby distilled to line and void — a black geometric frame suspended in light.",
     "discipline":"Interior · Workplace","location":"New York","shape":"tall"},
    {"slug":"lessroll","title":"Lessroll","cat":"Objectology","year":"2021",
     "summary":"A rethinking of an everyday dispenser, paring the mechanism down to its essential geometry.",
     "discipline":"Product · Industrial","location":"Concept","shape":"wide"},
    {"slug":"office-proposal","title":"Office Proposal","cat":"Unspace","year":"2022",
     "summary":"A workplace proposal weaving planting, threshold and circulation into a single legible sequence.",
     "discipline":"Interior · Workplace","location":"Proposal","shape":"default"},
    {"slug":"image-amplifier","title":"Image Amplifier","cat":"Objectology","year":"2020",
     "summary":"A timber enclosure that frames and amplifies the act of looking — furniture as optical instrument.",
     "discipline":"Product · Furniture","location":"Concept","shape":"default"},
    {"slug":"treehaus","title":"Treehaus","cat":"Unspace","year":"2021",
     "summary":"A retail and reading environment organized around a rhythm of vertical timber screens.",
     "discipline":"Interior · Retail","location":"New York","shape":"wide"},
    {"slug":"phone-glasses-holder","title":"Phone Glasses Holder","cat":"Objectology","year":"2022",
     "summary":"A minimal desk object holding phone and eyewear in a single confident profile.",
     "discipline":"Product · Industrial","location":"Concept","shape":"default"},
    {"slug":"my-suit-wall-street","title":"MY.SUIT Wall Street","cat":"Unspace","year":"2020",
     "summary":"A second MY.SUIT location translating the tailoring narrative into a sharper, downtown register.",
     "discipline":"Architecture · Retail","location":"Wall Street, NY","shape":"default"},
    {"slug":"mkt-market","title":"MKT Market","cat":"Unspace","year":"2021",
     "summary":"A market hall where reflection and glow dissolve the boundary between display and architecture.",
     "discipline":"Interior · Retail","location":"New York","shape":"wide"},
    {"slug":"prayer-space","title":"Prayer Space","cat":"Unspace","year":"2022",
     "summary":"A contemplative concrete room — light, mass and silence arranged for stillness.",
     "discipline":"Architecture · Sacred","location":"Concept","shape":"default"},
    {"slug":"sabine-farm","title":"Sabine Farm","cat":"Unspace","year":"2023",
     "summary":"A rural retreat set against a reflecting pool, framing the landscape through a calm horizontal datum.",
     "discipline":"Architecture · Residential","location":"Rural","shape":"default"},
    {"slug":"maxaroma","title":"Maxaroma","cat":"Unspace","year":"2023",
     "summary":"A flagship retail interior with a faceted, crystalline ceiling that choreographs movement below.",
     "discipline":"Interior · Retail","location":"New York","shape":"wide"},
]

# How many screenshot slots each project page should expose
SLOTS = {p["slug"]: 3 for p in PROJECTS}

# ---- Imagery: real, free Unsplash photos (Unsplash License, no attribution
# required) loaded directly from the Unsplash CDN. Each project maps to a
# cover + gallery shots themed to its discipline. -----------------------
def _u(photo_id, w, h):
    return (f"https://images.unsplash.com/photo-{photo_id}"
            f"?ixlib=rb-4.0.3&auto=format&fit=crop&w={w}&h={h}&q=80")

IMAGES = {
    "broadway-1270":        ["1486406146926-c627a92ad1ab", "1449157291145-7efd050a4d0e", "1496564203457-11bb12075d90", "1470723710355-95304d8aece4"],
    "bowie-furniture":      ["1567538096630-e0c55bd6374c", "1538688525198-9b88f6f53126", "1503602642458-232111445657", "1524758631624-e2822e304c36"],
    "wearable-waterbag":    ["1523275335684-37898b6baf30", "1542291026-7eec264c27ff", "1572635196237-14b3f281503f", "1606220588913-b3aacb4d2f46"],
    "my-suit":              ["1441986300917-64674bd600d8", "1567401893414-76b7b1e5a7a5", "1593030761757-71fae45fa0e7", "1582142306909-195724d33ffc"],
    "namad-office-lobby":   ["1497366216548-37526070297c", "1497366811353-6870744d04b2", "1524758631624-e2822e304c36", "1505873242700-f289a29e1e0f"],
    "lessroll":             ["1581092160562-40aa08e78837", "1581092918056-0c4c3acd3789", "1581093588401-fbb62a02f120", "1565891741441-64926e441838"],
    "office-proposal":      ["1497215728101-856f4ea42174", "1524758631624-e2822e304c36", "1542744173-8e7e53415bb0", "1531973576160-7125cd663d86"],
    "image-amplifier":      ["1538688525198-9b88f6f53126", "1567538096630-e0c55bd6374c", "1503602642458-232111445657", "1493663284031-b7e3aefcae8e"],
    "treehaus":             ["1556912172-45b7abe8b7e1", "1567401893414-76b7b1e5a7a5", "1441986300917-64674bd600d8", "1604014237800-1c9102c219da"],
    "phone-glasses-holder": ["1511707171634-5f897ff02aa9", "1556656793-08538906a9f8", "1572635196237-14b3f281503f", "1583394838336-acd977736f90"],
    "my-suit-wall-street":  ["1604014237800-1c9102c219da", "1593030761757-71fae45fa0e7", "1567401893414-76b7b1e5a7a5", "1582142306909-195724d33ffc"],
    "mkt-market":           ["1578916171728-46686eac8d58", "1542838132-92c53300491e", "1604719312566-8912e9227c6a", "1533900298318-6b8da08a523e"],
    "prayer-space":         ["1518005020951-eccb494ad742", "1473177104440-ffee2f376098", "1545987796-200677ee1011", "1438032005730-c779502df39b"],
    "sabine-farm":          ["1470770841072-f978cf4d019e", "1505691938895-1758d7feb511", "1449844908441-8829872d2607", "1518780664697-55e3ad937233"],
    "maxaroma":             ["1545179605-1296651e9d43", "1604014237800-1c9102c219da", "1556912172-45b7abe8b7e1", "1567401893414-76b7b1e5a7a5"],
}
PORTRAIT_URL = _u("1507003211169-0a1dd7228f2d", 1000, 1250)

def cover_url(slug):   return _u(IMAGES[slug][0], 1200, 900)
def shot_url(slug, i): return _u(IMAGES[slug][i], 1600, 1000)  # i = 1-based gallery index

RECOGNITION = {
    "awards": [
        ("A.R.E. Future of the Year Award", "2023", "Award"),
        ("Good Design Award", "2013", "Award"),
        ("A.R.E. Design Award", "2022", "Award"),
        ("IDA Design Awards", "2021", "Award"),
        ("Retail Design Blog", "—", "Publication"),
        ("Inhabitat", "—", "Publication"),
        ("VMSD Magazine", "—", "Publication"),
        ("FRAME", "—", "Publication"),
        ("Designers Party", "—", "Publication"),
        ("6B Editorial", "—", "Publication"),
    ],
    "clients": [
        "Treehaus", "Songhion Lee Art Studio", "Hunter Douglas",
        "Korean Cultural Center", "Aura Wellness Spa", "MY.SUIT",
        "XIOS New York", "INGO",
    ],
}

# ---- Build work grid --------------------------------------------------
def work_cards():
    out = []
    for i, p in enumerate(PROJECTS):
        shape = p["shape"]
        cls = "work-card" + (f" {shape}" if shape != "default" else "")
        # local image wins if present; otherwise real Unsplash CDN url
        img_rel = f"projects/{p['slug']}/cover.jpg"
        img_fs = os.path.join(ROOT, img_rel)
        src = img_rel if os.path.exists(img_fs) else cover_url(p["slug"])
        media = (f'<img src="{src}" alt="{html.escape(p["title"])}" loading="lazy" '
                 f'onerror="this.closest(\'.frame\').classList.add(\'img-fail\');this.remove();">'
                 f'<div class="ph-fallback"><span>{html.escape(p["title"])}</span>'
                 f'<small>{html.escape(p["cat"])}</small></div>')
        delay = (i % 2) * 90
        out.append(f"""        <a class="{cls} reveal" style="transition-delay:{delay}ms" href="projects/{p['slug']}.html">
          <div class="frame">{media}</div>
          <div class="work-meta">
            <span class="cat">{html.escape(p['cat'])}</span>
            <span class="title">{html.escape(p['title'])}</span>
            <span class="arrow">&#8599;</span>
          </div>
        </a>""")
    return "\n".join(out)

def recog_band():
    awards = "\n".join(
        f'          <li><span>{html.escape(n)}</span><span class="yr">{html.escape(y)}'
        f'</span></li>' if t=="Award" else
        f'          <li><span>{html.escape(n)}</span><span class="tag">{html.escape(t)}'
        f'</span></li>'
        for n,y,t in RECOGNITION["awards"]
    )
    clients = "\n".join(
        f'          <div class="cl">{html.escape(c)}</div>' for c in RECOGNITION["clients"]
    )
    return f"""  <section class="band" id="recognition">
    <div class="wrap">
      <div class="section-head reveal">
        <h2>Recognition</h2>
        <span class="idx">Awards · Press · Clients</span>
      </div>
      <p class="band-lede reveal">Work that has been awarded, published and trusted<span class="num">+</span></p>
      <div class="recog-split">
        <div class="recog-col reveal">
          <h3>Awards &amp; Publications</h3>
          <ul class="recog-list">
{awards}
          </ul>
        </div>
        <div class="recog-col reveal" style="transition-delay:120ms">
          <h3>Selected Clients</h3>
          <div class="clients-grid">
{clients}
          </div>
        </div>
      </div>
    </div>
  </section>"""

def build_index():
    page = head("UnSPACE — Creative Design Studio, New York",
                desc="UnSPACE is a New York City creative design studio led by Rook Kim, working across architecture, interiors and product design.")
    page += header("work")
    page += f"""
  <section class="hero">
    <div class="wrap hero-grid">
      <div>
        <div class="eyebrow reveal">New York City · Architecture &amp; Objectology</div>
        <h1 class="reveal" style="transition-delay:60ms">Space as a grand<br><em>geometric canvas.</em></h1>
      </div>
      <p class="hero-lede reveal" style="transition-delay:160ms">
        <span class="lead-mark">UnSPACE</span> is a creative design studio led by award-winning designer Rook Kim — weaving art, geometry and function into environments that feel both radically new and timelessly coherent.
      </p>
    </div>
  </section>

  <section class="section" id="work">
    <div class="wrap">
      <div class="section-head reveal">
        <h2>Selected Work</h2>
        <span class="idx">{len(PROJECTS)} Projects · 2019—2025</span>
      </div>
      <div class="work-grid">
{work_cards()}
      </div>
    </div>
  </section>

{recog_band()}

{footer()}
  <script src="assets/reveal.js"></script>
</body>
</html>"""
    with open(os.path.join(ROOT, "index.html"), "w") as f:
        f.write(page)

# ---- Project subpages -------------------------------------------------
def build_project(i, p):
    slug = p["slug"]
    pdir = os.path.join(ROOT, "projects", slug)
    os.makedirs(pdir, exist_ok=True)

    prev_p = PROJECTS[i-1] if i > 0 else PROJECTS[-1]
    next_p = PROJECTS[(i+1) % len(PROJECTS)]

    # screenshot slots — hero (01) full width, 02+03 as a two-up pair
    n = SLOTS[slug]
    def fig(s, extra=""):
        rel = f"{slug}/{s:02d}.jpg"
        fs = os.path.join(ROOT, "projects", rel)
        src = f"{slug}/{s:02d}.jpg" if os.path.exists(fs) else shot_url(slug, s)
        return (f'<figure class="shot{extra} reveal">'
                f'<img src="{src}" alt="{html.escape(p["title"])} — view {s}" loading="lazy" '
                f'onerror="this.closest(\'.shot\').classList.add(\'img-fail\');this.remove();">'
                f'<div class="ph-fallback"><span>{html.escape(p["title"])}</span>'
                f'<small>{html.escape(p["cat"])} · {s:02d}</small></div></figure>')
    parts = [f'        {fig(1)}']
    if n >= 3:
        parts.append('        <div class="shot-pair">'
                     f'{fig(2)}{fig(3)}</div>')
    elif n == 2:
        parts.append(f'        {fig(2)}')
    shots_html = "\n".join(parts)

    body = head(f"{p['title']} — UnSPACE", depth=1, desc=p["summary"])
    body += header("work", depth=1)
    body += f"""
  <article class="proj">
    <div class="wrap">
      <a class="back reveal" href="../index.html#work">&#8592; Back to work</a>
      <header class="proj-head">
        <div class="proj-cat reveal">{html.escape(p['cat'])}</div>
        <h1 class="reveal" style="transition-delay:60ms">{html.escape(p['title'])}</h1>
        <p class="proj-summary reveal" style="transition-delay:120ms">{html.escape(p['summary'])}</p>
        <dl class="proj-facts reveal" style="transition-delay:180ms">
          <div><dt>Discipline</dt><dd>{html.escape(p['discipline'])}</dd></div>
          <div><dt>Location</dt><dd>{html.escape(p['location'])}</dd></div>
          <div><dt>Year</dt><dd>{html.escape(p['year'])}</dd></div>
        </dl>
      </header>

      <section class="shots">
{shots_html}
      </section>

      <nav class="proj-nav">
        <a class="reveal" href="{prev_p['slug']}.html">
          <span class="dir">&#8592; Previous</span>
          <span class="nm">{html.escape(prev_p['title'])}</span>
        </a>
        <a class="reveal nextlink" href="{next_p['slug']}.html">
          <span class="dir">Next &#8594;</span>
          <span class="nm">{html.escape(next_p['title'])}</span>
        </a>
      </nav>
    </div>
  </article>

{footer()}
  <script src="../assets/reveal.js"></script>
</body>
</html>"""
    with open(os.path.join(ROOT, "projects", f"{slug}.html"), "w") as f:
        f.write(body)

# ---- Info page --------------------------------------------------------
def build_info():
    body = head("Info — UnSPACE", desc="About UnSPACE and Rook Kim, and how to start a project.")
    body += header("info")
    body += f"""
  <section class="info">
    <div class="wrap">
      <div class="info-grid">
        <figure class="portrait reveal">
          <img src="PORTRAIT_SRC" alt="Rook Kim, founder of UnSPACE"
               onerror="this.closest('figure').classList.add('ph')">
          <figcaption>Rook Kim — Founder</figcaption>
        </figure>
        <div class="info-body reveal" style="transition-delay:90ms">
          <p class="lead"><em>UnSPACE</em> is a New York City–based creative design studio led by award-winning designer <strong>Rook Kim</strong>. Trained in architecture at Pratt Institute and Columbia University, Rook honed his craft at the Itami Jun Architectural Research Institute in Tokyo before founding <em>UnSPACE</em>.</p>
          <p>His work has earned multiple international design awards for its bold, experimental approach that consistently challenges convention.</p>
          <p>At the heart of UnSPACE's practice is a philosophy that treats space as a grand geometric canvas. By weaving art deeply into the design process, the studio breaks free from predictable motifs and introduces unfamiliar, thought-provoking elements that invite curiosity and questioning.</p>
        </div>
      </div>

      <div class="info-statement reveal">
        <p>Functionality is never an afterthought; it is the driving force that harnesses the inherent energy of a space. When art, geometry and function align, the result is an environment that feels both radically new and timelessly coherent.</p>
        <p>From cultural institutions and experimental residences to forward-thinking commercial environments, UnSPACE creates spaces that transcend trends and provoke lasting impressions. Each project is an exploration of scale, materiality and narrative — an architectural gesture that is as intellectually engaging as it is visually striking.</p>
        <p class="closer"><em>UnSPACE</em> — where unconventional thinking meets meticulous craft, and every space tells an unexpected story.</p>
      </div>

      <div class="contact" id="contact">
        <div class="section-head reveal"><h2>Contact</h2><span class="idx">Start a conversation</span></div>
        <form class="contact-form reveal" id="contactForm" novalidate>
          <input type="email" placeholder="Email" required aria-label="Email">
          <textarea placeholder="Message" rows="6" required aria-label="Message"></textarea>
          <button type="submit">Send</button>
          <p class="form-note" role="status" aria-live="polite"></p>
        </form>
      </div>
    </div>
  </section>

{footer()}
  <script src="assets/reveal.js"></script>
</body>
</html>"""
    portrait_local = os.path.join(ROOT, "assets", "rook-kim.jpg")
    portrait_src = "assets/rook-kim.jpg" if os.path.exists(portrait_local) else PORTRAIT_URL
    body = body.replace("PORTRAIT_SRC", portrait_src)
    with open(os.path.join(ROOT, "info.html"), "w") as f:
        f.write(body)

# ---- Run --------------------------------------------------------------
if __name__ == "__main__":
    build_index()
    for i, p in enumerate(PROJECTS):
        build_project(i, p)
    build_info()
    print(f"Built index.html, info.html and {len(PROJECTS)} project pages.")
