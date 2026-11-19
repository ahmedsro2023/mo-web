# OPSMO website

Static rebuild of opsmo.tech — every page and link of the original site, same copy, with a **light (white)** and **dark (black)** theme.

## Themes
- Toggle with the sun/moon button in the navigation. The choice is remembered.
- Direct links: add `?theme=dark` or `?theme=light` to any URL (e.g. `/?theme=dark`).

## Pages (40)
Home · Solutions (+10) · Platforms (+5) · Industries (+7) · Managed Services · Insights (+4 articles) · About · Founder · Approach · Packages · Contact · Book · Privacy · Terms

## Run locally
```
python3 -m http.server 8080   # then open http://localhost:8080
```

## Deploy
- **Vercel / Netlify:** import the repo, framework "Other", no build command, output directory `/`.
- **GitHub Pages:** Settings → Pages → Deploy from branch `main` / root. Paths are relative, so it also works under `/mo-web/`.

## Editing content
Content lives in `_src/` (Markdown files + Python data). Rebuild from the repo root with:
```
OUT=. python3 _src/build.py
```

## Before going live
1. Forms: set `FORM_ENDPOINT` in `assets/js/main.js` (e.g. Formspree) so Contact and Book submissions are received.
2. Photos are from Unsplash — replace with real OPSMO photos using the same file names in `assets/img/`.


## v5 — rebuild (Nov 2026)
- Whole site moved to the dark "systems boot" identity (Bricolage Grotesque / Geist / Geist Mono), light theme via the toggle or `?theme=light`.
- New section transition: a fire "seam" scans each section edge, content boots in with a clip reveal; page-to-page uses the View Transitions API.
- SEO: canonical, Open Graph/Twitter, JSON-LD (ProfessionalService, Person, BreadcrumbList, FAQPage, Article), `sitemap.xml`, `robots.txt`.
- Conversion: 3-path contact block on every page (call / WhatsApp / assessment), floating WhatsApp button, sticky mobile CTA bar.
- New `/success-stories/` page; LinkedIn videos load as official embeds on click.

Rebuild: `cd _src && OUT=.. python3 site5.py && cp -r assets ..` (assets live in `_src/assets`).
