# UnSPACE — Portfolio Website

A fully responsive, functional portfolio site for UnSPACE — a refined, editorial
design (warm cream paper, Fraunces + Newsreader serifs, italic headings).

## ▶ View it
Open **`index.html`** in any browser. No server or build step needed.
Works on desktop, tablet and mobile (fully responsive).

## Pages (17 HTML files)
- `index.html` — landing: hero, 15-project work grid, dark Recognition band
- `info.html` — studio bio + statement + working contact form
- `projects/<slug>.html` — a dedicated page per project, with image gallery + prev/next

## Imagery (60 images included)
- Every project ships with a **real cover photo + 3 gallery images** already in place
  under `projects/<slug>/` (`cover.jpg`, `01.jpg`, `02.jpg`, `03.jpg`).
- The **founder portrait** on the Info page loads from a free Unsplash URL
  (Unsplash License, no attribution required). Drop a local `assets/rook-kim.jpg`
  to override it.
- **Graceful fallback:** if any image ever fails to load (e.g. offline), it degrades
  to an on-brand tinted block with the project name — never a broken-image icon.

### Swapping any image
Just replace the file in `projects/<slug>/` with your own (keep the same name),
then re-run `python3 build.py`. Local files always take priority over remote URLs.

## Functional features
- Sticky blurred header, animated nav underlines
- Scroll-reveal animations (staggered), image hover zoom + arrow
- Responsive grid: 2-up → 1-up on mobile; mixed aspect ratios for editorial rhythm
- Contact form with submit confirmation (front-end demo — wire to your handler to deploy)

## Editing content
All text/data lives in `build.py`, then run `python3 build.py` to regenerate:
- `PROJECTS` — titles, categories, summaries, disciplines, years, tile shapes
- `RECOGNITION` — Awards/Publications + Clients in the dark band
- `IMAGES` — Unsplash photo IDs used as remote fallback per project
- `SLOTS` — gallery image count per project page

## Extras
- `figma-mockup/` — a 3-page PDF + PNG boards presenting the design system and
  page layouts in a Figma-style presentation (foundations, landing, project + info).

## Deploying
It's static HTML/CSS/JS — host anywhere (Netlify, Vercel, GitHub Pages, S3, any
web host). Just upload the whole folder.
