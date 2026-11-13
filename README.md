# OPSMO website (v2)

Static site — HTML, CSS and vanilla JS. No build step, no dependencies.

## Run locally
Open `index.html` in a browser, or:
```
python3 -m http.server 8080   # http://localhost:8080
```

## Deploy
- GitHub Pages: Settings → Pages → Deploy from branch `main` / root (public repo on the free plan).
- Vercel / Netlify: import the repo, framework "Other", no build command, output `/`.

## Before going live
1. Connect the contact form: set `FORM_ENDPOINT` in `assets/js/main.js` (e.g. Formspree).
2. Have Mohamed approve the track-record figures and the founder copy (taken from his LinkedIn).
3. Photos are from Unsplash (free licence). Swap in real OPSMO photos when available — same file names in `assets/img/`.
4. Add Privacy / Terms pages.
