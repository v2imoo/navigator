# Navigator — Build Progress & Resume State

Use this to resume in a fresh chat. Paste it in and say "continue from PROGRESS.md."

## ✅ DONE (v1 shipped in the bundle)
- **Design system** — `assets/css/styles.css` (fonts: Fraunces/Newsreader/Public Sans/IBM Plex Mono/Atkinson Hyperlegible; colour wayfinding by cluster; responsive).
- **Compass logo** (inline SVG) + favicon.
- **Responsive nav** — desktop dropdowns + mobile drawer with accordion groups (no overlap). `assets/js/main.js`.
- **Generator** — `build.py` (SEO/AEO/GEO head, JSON-LD, sitemap, robots, llms.txt, MD→HTML).
- **Home** (living) with FAQ schema; **About** (mission-first); **Contact** (wvijay@icloud.com); **legal**: privacy/terms/cookies/refund/accessibility/disclaimer/credits.
- **Newsletter** index (living) + seed article `welcome-navigator` + documented 3-file publish workflow.
- **Tools hub** + 2 working tools with PNG/CSV download + share: **Decision Matrix**, **Moat Analyzer** (`assets/js/tools.js`).
- **Flagship concept pages (live):** Airbnb (business), The Bitter Lesson (mental model), AI-Assisted Pre-Mortem (decision tool), Usage-Based/AI-Metered (business model), Vertical AI Agents (framework), Co-Intelligence (book), AI-Native Operator (reading list), Keep Judgment When the Model Is Confident (guide), AI & the Future of Work (quotes).
- **Category index pages (live):** business-models, frameworks, moats, books, reading-lists, guides, quotes.
- **Hub stubs:** people, businesses, mental-models, decision-tools, paths, recommend.
- **37 pages, full sitemap.** Cloudflare `_headers`, `404.html`.

## ⏳ PENDING (next batches — add MD → register in build.py → rerun)
1. **Populate concept pages** per category to full depth:
   - Mental Models: build out the ~1045 across 12 categories (start with a "top 100" most-used).
   - Decision Tools: the remaining 43 (Active Listening & Stockdale already written earlier as references).
   - Business Models: individual pages for all ~55 (index done).
   - Frameworks: individual pages (index done).
   - Moats: split the 7 Powers into individual `/moats/<power>/` pages (category page done).
   - Books / Reading Lists / Guides / Quotes: more individual entries (indexes + 1 flagship each done).
2. **People profiles** — Story/Playbook/Quotes, incl. the **hidden number-twos** rail; use `all-people-categorized.md`, `hidden-number-twos.md`, `master-roster-combined.md`, `supplement-newage-and-india.md`.
3. **Businesses** — more company profiles (Airbnb live) from `all-businesses-categorized.md`.
4. **More tools** — Pricing-Model Chooser, Pre-Mortem worksheet, Mental-Model Finder, Opportunity Finder (scaffolded on the hub).
5. **Learning Paths** + **Recommend** engine (sequencing + tag-matching), built last.
6. **Images** — swap monogram/placeholder approach for public-domain/Wikimedia portraits & logos where available; keep attribution only on `/credits`.
7. **Set real domain** in `build.py` `SITE["url"]` and rerun.


## THEME / BRAND (v2)
- Domain: **navigator.blog** (set in build.py SITE['url']).
- Logo: text **Θ Navigator** (theta in a gradient circle) — compass removed.
- Fonts: Baloo 2 (display), Lexend (body/UI, education-readability), Space Mono (labels), Atkinson Hyperlegible (a11y).
- Look: bright 'learning-studio' — off-white paper, colourful cluster wayfinding, rounded cards, coloured header bands, hero avatar collage, playful buttons.
- Images: colourful avatar/initial tiles now; drop-in slot for Wikimedia photos/logos later — place files in assets/img/people/<slug>.(jpg|webp) and assets/img/logos/<slug>.svg, then reference; attribution only on /credits.

## HOW TO CONTINUE EFFICIENTLY
- Content is authored as Markdown (same voice/format as the shipped flagships), then registered in `build.py` via `render_md_page(md_file, route, chip_cls, chip_label, breadcrumb)` and the site rebuilt.
- Keep each publish/newsletter to the **2-replace + 1-add** contract.
- All source flagships live in `/mnt/user-data/outputs/*.md`; the master plan is `NAVIGATOR-concept-and-blueprint.md`.

## STATUS (v3 — full site generated)
- **2,310 pages generated** — every reserved URL exists, themed, cross-linked, no 404s, no broken images.
- Data-driven: data/*.json (13 rosters) + build.py + flagship MD. Rebuild: `python3 build.py`.
- 9 DEEP flagships live (Airbnb, Bitter Lesson, AI-Pre-Mortem, Usage-Based pricing, Vertical AI Agents, Co-Intelligence, AI-Native Operator list, Keep-Judgment guide, AI-Future quotes) + 2 working tools (Decision Matrix, Moat Analyzer).
- All other items = complete concise pages (thesis + core idea + Connected rail + newsletter CTA) — deepen in batches.
- Static search (/search/), recommend (/recommend/), full indexes for all 13 types, sitemap.xml, search-index.json.
- See CONTINUATION.md to resume in a new chat.

## PENDING (deepen in batches — never breaks the live site)
1. Books + Reading Lists → full templates + OpenLibrary covers.
2. Tool dashboards batch 2 (Eisenhower, Impact-Effort, Pricing-Model Chooser, Mental-Model Finder, What-should-I-study).
3. Mental Models top-100 → full 11-section pages.
4. People + Businesses → Story/Playbook/Quotes + hidden-number-twos rail + photos/logos.
5. Decision Tools (44) → full 9-section pages. Moats (7) → per-Power deep pages.
6. Paths → sequenced steps + progress; Recommend → tag-matched engine.

## STATUS (v4 — interactive indexes + Wikipedia images + AI + more tools)
- **2,312 pages.** All index pages are now INTERACTIVE card grids (search + category/A–Z filter), not text lists.
- **Real images from Wikipedia**, loaded client-side (assets/js/wiki.js): people portraits + company logos on index cards, hero portraits on profile pages; lazy-loaded, graceful monogram fallback (never broken). Works on the deployed site.
- **People/Business profile pages** are longer & structured: hero portrait + thesis + Story + Playbook + (verified-quotes slot) + Connected. Deep flagship: **Jeff Bezos** (934w, original prose) alongside **Airbnb**.
- **Artificial Intelligence** is a top-level menu + /ai/ hub with the two arms: **/ai/ai-for-you/** and **/ai/ai-plus-you/** (expanded, ready to deepen/replace).
- **Tools now 5 live:** Decision Matrix, Moat Analyzer, Eisenhower Matrix, Impact–Effort Matrix, Pricing-Model Chooser — all client-side, downloadable, no login. Collection is designed to keep expanding.
- assets/js/filter.js powers the index filtering; assets/js/wiki.js the images.

## PENDING (deepen in batches — never breaks the live site)
1. Deepen more People/Business profiles into full Story·Playbook·Quotes (add verified quotes only).
2. AI arms → deep practical playbooks (user is writing; replace in place).
3. More tools (SWOT, RACI, Cost-Benefit, Decision Tree, Mental-Model Finder, What-should-I-study) — expand unlimited.
4. Books + Reading Lists → full templates + OpenLibrary covers (add ISBN to data/books.json).
5. Mental Models top-100 → full 11-section pages; Decision Tools 44 → full 9-section; Moats 7 → per-Power deep.
6. Paths sequencing + Recommend tag-matched engine.

## STATUS (v5 — deeper profiles, more tools, book covers)
- **2,315 pages.** New deep profiles: Warren Buffett, Steve Jobs, Charlie Munger (People) + NVIDIA (Businesses) — original Story/Playbook/Quotes, ~700-840 words each. Now 5 deep people + 2 deep businesses.
- **Tools now 9 live:** Decision Matrix, Decision Tree (EV), Eisenhower, Impact-Effort, Moat Analyzer, Pricing-Model Chooser, SWOT Builder, RACI Matrix, Mental-Model Finder. Tools hub groups them Decide / Strategise / Organise.
- **Book covers from OpenLibrary** (assets/js/books.js) on all 100 book cards + book pages; lazy, graceful fallback.
- People index now features 6 deep dives; Businesses features 2.

## PENDING (deepen in batches)
1. More deep profiles (next: Munger done; add Sam Walton, Coco Chanel, Reed Hastings, Costco, LVMH...).
2. AI arms → deep practical playbooks (user writing; replace in place).
3. More tools (Cost-Benefit, OODA, Scenario Planner, Unit-Economics, Second-Order Mapper).
4. Books/Reading Lists → full 9-section templates.
5. Mental Models top-100 → full 11-section; Decision Tools 44 → full 9-section; Moats 7 → per-Power.
6. Paths sequencing + Recommend engine.

## FIX (v6 — clean URLs for Cloudflare/GitHub Pages)
- Root cause of site-wide 404s: internal links ended in `index.html`, which Cloudflare Pages 404s (it serves clean URLs like /people/steve-jobs/).
- `relativize()` now emits CLEAN directory URLs (no index.html). All 2,312 pages regenerated. Verified 0 index.html internal links.
- Image scripts (wiki.js via MediaWiki Action API origin=*, books.js via OpenLibrary) also updated.
- ACTION: redeploy the full `site/` once (links are baked into every page). After this, updates stay additive.
- Preview locally with a static server (`cd site && python3 -m http.server 8000`), not by double-clicking files.
