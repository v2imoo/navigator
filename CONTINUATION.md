# NAVIGATOR — CONTINUATION (read this first in a new chat)

Paste this file into a new chat and say: **"Continue Navigator from CONTINUATION.md."**
Everything needed to keep generating the same-themed, working site is here. The site never breaks because **every reserved page already exists**; we only *deepen* pages and *add* newsletter articles.

## 1. What Navigator is
Open, no-login "learn from the greats" site at **navigator.blog** (GitHub + Cloudflare Pages, static, no build step to host). Logo: text **Θ Navigator**. Theme: bright "learning-studio" — fonts Baloo 2 (display) / Lexend (body) / Space Mono (labels) / Atkinson Hyperlegible (a11y); off-white paper, colour-coded clusters (People amber, Businesses teal, Strategies indigo, Learn green, Tools coral, Newsletter purple). All internal links are **relative** so it works locally and deployed.

## 2. The architecture (data-driven, resumable)
```
navigator/
  build.py            ← the generator: reads data/*.json + flagship MD → site/
  gen_data.py         ← rebuilds data/*.json from the source rosters (rarely needed)
  data/*.json         ← 13 rosters: people, businesses, mental-models, decision-tools,
                        business-models, frameworks, moats, books, reading-lists, guides,
                        quotes, tools, paths  (slug, name, category, blurb, author)
  assets/css/styles.css, assets/js/main.js, assets/js/tools.js
  site/               ← the DEPLOYABLE output (2,310 pages). Upload contents to GitHub.
  README.md PROGRESS.md CONTINUATION.md
```
Flagship long-form pages come from `/mnt/user-data/outputs/*.md` (e.g. `06-mental-models-sample.md` → The Bitter Lesson). They're registered in `build.py`'s `P=[…]` list and in `FEAT`/`SKIP`.

## 3. To (re)build the whole site
`cd navigator && python3 build.py`  → regenerates `site/` (2,310 pages) + `sitemap.xml` + `search-index.json`. Fast. Idempotent.

## 4. How to DEEPEN pages (the main ongoing work)
Two ways, both keep the site whole:
- **Concise → deep for one item:** write a long-form MD (same voice as the flagships) to `/mnt/user-data/outputs/`, then add one line to `build.py`'s `P=[…]` list (md file, route, cluster, chip, breadcrumb) and add the slug to `SKIP[type]` + a card to `FEAT[type]`. Rerun. That item is now deep; everything else stays.
- **Improve concise pages in bulk:** enrich the `blurb`/fields in `data/<type>.json` and rerun. Every item page uses the standard template (thesis → core idea → Connected rail → newsletter CTA), so better data = better pages automatically.

Build order still pending (deepen in batches; see PROGRESS.md): Books+Reading-Lists (covers via OpenLibrary), Tool dashboards batch, Mental-Models top-100, People/Businesses profiles (Story·Playbook·Quotes + hidden-number-twos), Paths sequencing, static search polish.

## 5. Interactive tools
`assets/js/tools.js` holds working tools (Decision Matrix, Moat Analyzer) with PNG/CSV download + share. To add one: write `initX(elId)` in tools.js, then in `build.py main()` call `render_tool_page("slug","Title","meta desc","intro",'<div id="x"></div>','initX(\"x\");',"explainer html")`. Add its slug to `SKIP["tools"]`. Tools are client-side, no login, downloadable results, original SVG/canvas (no copyright issues).

## 6. Images (copyright-safe)
People/companies use designed monogram tiles now. Drop-in later: place `assets/img/people/<slug>.jpg` or `assets/img/logos/<slug>.svg` and extend the avatar to use it; attribution only on `/credits`. Books: OpenLibrary covers `https://covers.openlibrary.org/b/isbn/{ISBN}-L.jpg` (free, no attribution) — add an ISBN field to `data/books.json` and render it. Never ship a broken image.

## 7. Newsletter = the ONLY live-replace flow (2 replace + 1 add)
Publishing an article changes just three files:
1. **REPLACE** `site/index.html` (home features the latest)
2. **REPLACE** `site/newsletter/index.html` (index lists it)
3. **ADD** `site/newsletter/<slug>/index.html` (the article)
In `build.py`, add the article dict to `ARTICLES=[…]` and rerun — git will show exactly those 3 changes. Publish on LinkedIn, mirror here. Nothing else in the library is touched.

## 8. Deploy
Upload the **contents of `site/`** to the GitHub repo root. Cloudflare Pages → Framework preset: None, Build command: empty, Output dir: `/`. Domain navigator.blog already set in `build.py` `SITE["url"]`.

## 9. Guardrails (keep quality/consistency)
- Original prose only; paraphrase quotes (<15 words, one per source, verify attribution).
- Relative links (build.py `relativize()` handles it) — never hardcode `/…` in new templates without it.
- Every page keeps: header band (cluster colour), Θ nav + responsive drawer, thesis, Connected rail, newsletter CTA, footer. Don't regress the theme.
- If a chat is near its limit: stop after a clean `python3 build.py`, hand over this file + PROGRESS.md, and the next chat resumes from the same `navigator/` folder.

**Status:** 2,310 pages live-complete (all reserved URLs exist, themed, cross-linked). Next: deepen in batches per PROGRESS.md.


## UPDATE v4 (current)
- Interactive indexes: `render_full_index` builds search + A–Z/category filtered card grids. People/Businesses cards use `data-wiki="<Name>"` → **assets/js/wiki.js** fetches the Wikipedia thumbnail at runtime (lazy, fallback to monogram). To add images anywhere, put `data-wiki="Exact Wikipedia Title"` on a `.card-media`/`.hero-portrait`.
- Profile pages: `render_item_page` gives people/businesses a hero portrait + Story/Playbook structure. Deepen one by writing a long MD (see `jeff-bezos.md`) and registering it in `P[]` + `FEAT[type]` + `SKIP[type]`.
- AI section: `render_ai()` builds `/ai/`, `/ai/ai-for-you/`, `/ai/ai-plus-you/`. Edit the `arms` list in `render_ai()` to deepen; nav already links it.
- Tools: 5 live in `assets/js/tools.js` (initDecisionMatrix, initMoatAnalyzer, initEisenhower, initImpactEffort, initPricingChooser). Add more by writing `initX` then a `render_tool_page(...)` call in `main()` and adding the slug to `SKIP["tools"]`.
- Quotes rule: never fabricate. Person pages show a "verified quotes being added" slot until real, short (<15w), attributed quotes are confirmed.


## UPDATE v5 (current)
- Book covers: `assets/js/books.js` reads `data-book="Title|Author"` and pulls the OpenLibrary cover at runtime (lazy, fallback to tile). Wired on book index cards + book item pages.
- Deep profiles now: Bezos, Buffett, Jobs, Munger, Airbnb, NVIDIA. Add more by writing an MD (see those files in /mnt/user-data/outputs/) and registering in `P[]` + `FEAT[type]` + `SKIP[type]`.
- Tools now 9 live in `assets/js/tools.js`: add init* fn -> `render_tool_page(...)` in main() -> add slug to `SKIP["tools"]` -> add a card in `render_tools_hub()`.
