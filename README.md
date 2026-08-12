# Navigator — static site (GitHub + Cloudflare Pages)

Open, no-login library of how the greats think, build & decide. **The `site/` folder is the entire website** — pure static HTML/CSS/JS, no build step required to host.

## 1. Host it (GitHub + Cloudflare Pages)
1. Create a GitHub repo and upload the **contents of `site/`** to the repo root (so `index.html` is at the top).
2. In Cloudflare → **Pages** → **Connect to Git** → pick the repo.
3. Build settings: **Framework preset: None** · **Build command: (leave empty)** · **Output directory: `site`** (or `/` if you upload the contents of site/). No build needed.
4. Deploy. Add your custom domain in Pages → Custom domains.
5. **Important:** open `build.py` and change `SITE["url"]` to your real domain, then re-run `python3 build.py` so canonical URLs, sitemap, and Open Graph tags are correct. (Or, if hand-editing, update the domain in the generated files.)

That's it — it's live, fast, and free.

## 2. Publish a newsletter article (your 3-file workflow)
Every publish touches **exactly three files** — 2 replaced, 1 added — nothing else in the site changes:

**Option A — regenerate (recommended, safest):**
1. Add your article to the `ARTICLES` list in `build.py` (slug, title, date, summary, linkedin URL, body HTML).
2. Run `python3 build.py`.
3. Commit — git will show only: **`/index.html`** (home, updated to feature it), **`/newsletter/index.html`** (index, updated to list it), and the **new** `/newsletter/<slug>/index.html`. Upload those.

**Option B — pure manual (no Python):**
1. **ADD** `newsletter/<slug>/index.html` — copy an existing article file and edit the content.
2. **REPLACE** `newsletter/index.html` — add one card linking the new article.
3. **REPLACE** `index.html` — update the "Latest from the newsletter" card to point at it.

Either way: publish on LinkedIn, then mirror here. The rest of the library stays frozen and safe.

## 3. Add library pages later (the hundreds)
The site scales through the generator, not by hand:
- Drop new content as Markdown (same style as the flagship samples).
- Register it in `build.py` (`render_md_page(...)` with its route + cluster colour).
- Run `python3 build.py` — it regenerates pages + `sitemap.xml` automatically.
See `PROGRESS.md` for exactly what's done and what's pending, so a new session can resume instantly.

## 4. What's inside
- `site/` — the deployable website (this is what you host).
- `build.py` — the generator (SEO/AEO/GEO, nav, MD→HTML).
- `assets/` — source CSS/JS (also copied into `site/assets`).
- `content/` — reserved for future Markdown content.
- `PROGRESS.md` — build state & roadmap (for resuming across chats).

## 5. SEO / AEO / GEO built in
Per page: title, meta description, canonical, Open Graph, Twitter cards, robots. Site-wide: `sitemap.xml`, `robots.txt`, `llms.txt` (for generative engines), Organization + WebSite (with SearchAction) + Article + FAQ JSON-LD, semantic HTML, breadcrumbs, TL;DR-style answer blocks, and clean URLs. Accessible: AA contrast, keyboard nav, readable-font toggle.

Contact: **wvijay@icloud.com**
