#!/usr/bin/env python3
# NAVIGATOR static site generator — Learning Studio theme. Output: ./site
import os, re, json, shutil, html, datetime, markdown

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(ROOT, "site")
SRC_MD = "/mnt/user-data/outputs"

SITE = {
  "name":"Navigator",
  "url":"https://navigator.blog",
  "tagline":"Learn from the greats — and the ones who built beside them.",
  "desc":"Navigator is an open, no-login learning studio for how the world's greatest people and companies think, build, and decide — with usable tools, deep guides, and a living newsletter. Free for leaders, employees, students, and managers in every industry.",
  "email":"wvijay@icloud.com","author":"Vijay",
}
PAGES=[]
def relativize(content, depth):
    """Rewrite root-absolute /links and /assets to correct relative paths.
    Uses CLEAN directory URLs (…/people/steve-jobs/) with NO index.html, which
    is what Cloudflare Pages / GitHub Pages / Netlify serve. (Preview locally with
    a static server, e.g. `python3 -m http.server`, not by double-clicking a file.)"""
    prefix="../"*depth
    def href_repl(m):
        g=m.group(1)
        if g=="": return f'href="{prefix or "./"}"'
        return f'href="{prefix}{g}"'
    content=re.sub(r'href="/([^"]*)"', href_repl, content)
    content=re.sub(r'src="/([^"]*)"', lambda m:f'src="{prefix}{m.group(1)}"', content)
    return content

CLUSTER_HEX={"people":"#FB8B24","biz":"#06A6A0","strat":"#4361EE","learn":"#2FBF71","tools":"#F0544F","news":"#9B5DE5","brand":"#0C5460"}

STRAT=[("Mental Models","/mental-models/"),("Decision Tools","/decision-tools/"),
       ("Business Models","/business-models/"),("Frameworks","/frameworks/"),("Moats","/moats/")]
LEARN=[("Book Summaries","/books/"),("Reading Lists","/reading-lists/"),
       ("Guides","/guides/"),("Quote Collections","/quotes/")]

def theta_brand(cls=""):
    return f'<a class="brand {cls}" href="/"><span class="theta">&#920;</span>&nbsp;NAVIGATOR</a>'

def avatar(initials, cluster="brand", size=None, img=None):
    # colourful designed tile; if img path provided it is used, else initials
    c=CLUSTER_HEX.get(cluster,"#0C5460")
    style=f'background:linear-gradient(135deg,{c},{shade(c)});'
    if size: style+=f'width:{size};height:{size};'
    inner=f'<img src="{img}" alt="{html.escape(initials)}">' if img else html.escape(initials)
    return f'<div class="avatar" style="{style}">{inner}</div>'

def shade(hexv):
    # darken/rotate a hex for gradient end
    m={"#FB8B24":"#F0544F","#06A6A0":"#4361EE","#4361EE":"#0C5460","#2FBF71":"#06A6A0",
       "#F0544F":"#FF6FB5","#9B5DE5":"#0C5460","#0C5460":"#06A6A0"}
    return m.get(hexv,"#06A6A0")

def head(title, desc, path, kind="website", jsonld=None):
    canon=SITE["url"].rstrip("/")+path
    org={"@context":"https://schema.org","@type":"Organization","name":SITE["name"],"url":SITE["url"],"email":SITE["email"],"description":SITE["desc"]}
    website={"@context":"https://schema.org","@type":"WebSite","name":SITE["name"],"url":SITE["url"],
      "potentialAction":{"@type":"SearchAction","target":SITE["url"]+"/search/?q={q}","query-input":"required name=q"}}
    ld=('<script type="application/ld+json">'+json.dumps(jsonld)+'</script>') if jsonld else ''
    return f'''<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} · {SITE["name"]}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canon}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="author" content="{SITE["author"]}">
<meta name="theme-color" content="#0C5460">
<meta property="og:type" content="{kind}"><meta property="og:site_name" content="{SITE["name"]}">
<meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canon}"><meta property="og:image" content="{SITE["url"]}/assets/img/og.svg">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{html.escape(title)}">
<meta name="twitter:description" content="{html.escape(desc)}">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400..600&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/styles.css">
<script type="application/ld+json">{json.dumps(org)}</script>
<script type="application/ld+json">{json.dumps(website)}</script>
{ld}
</head><body>'''

def nav():
    def drop(label,items):
        links=''.join(f'<a href="{u}">{n}</a>' for n,u in items)
        return f'<div class="drop"><button aria-haspopup="true">{label} &#9662;</button><div class="drop-menu">{links}</div></div>'
    ds=''.join(f'<a href="{u}">{n}</a>' for n,u in STRAT); dl=''.join(f'<a href="{u}">{n}</a>' for n,u in LEARN)
    return f'''<div class="topbar">A new breakdown every week &mdash; <a href="/newsletter/">read the newsletter &rarr;</a></div>
<header class="site-header"><div class="wrap nav">
{theta_brand()}
<nav class="nav-links" aria-label="Primary">
<a href="/people/">People</a><a href="/businesses/">Businesses</a>{drop("Strategies",STRAT)}{drop("Learn",LEARN)}
<a href="/ai/">AI</a><a href="/tools/">Tools</a><a href="/newsletter/">Newsletter</a><a href="/about/">About</a></nav>
<button class="menu-btn" id="menuBtn" aria-label="Open menu"><svg viewBox="0 0 24 24" fill="none" stroke-width="2.4"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg></button>
</div></header>
<div class="drawer" id="drawer"><div class="drawer-panel">
<button class="drawer-close" data-close aria-label="Close menu">&times;</button>
<a href="/people/">People</a><a href="/businesses/">Businesses</a><a href="/tools/">Tools</a><a href="/newsletter/">Newsletter</a>
<details class="drawer-group" open><summary>Strategies</summary>{ds}</details>
<details class="drawer-group"><summary>Learn</summary>{dl}</details>
<a href="/ai/">Artificial Intelligence</a>
<a href="/paths/">Learning Paths</a><a href="/recommend/">What should I study?</a>
<a href="/about/">About</a><a href="/contact/">Contact</a>
<button class="btn ghost" id="a11yToggle" style="margin-top:12px">Aa Readable font</button>
</div></div>'''

def footer():
    return f'''<footer class="site-footer"><div class="wrap">
<div class="cols">
<div>{theta_brand()}<p style="max-width:42ch;color:#cdc2ea;margin-top:.6em">{SITE["tagline"]} Open, free, no login &mdash; a learning studio for anyone who wants to learn from the best.</p></div>
<div><h4>Explore</h4><a href="/people/">People</a><br><a href="/businesses/">Businesses</a><br><a href="/mental-models/">Mental Models</a><br><a href="/tools/">Tools</a><br><a href="/newsletter/">Newsletter</a></div>
<div><h4>Site</h4><a href="/about/">About</a><br><a href="/contact/">Contact</a><br><a href="/privacy/">Privacy</a> &middot; <a href="/terms/">Terms</a><br><a href="/cookies/">Cookies</a> &middot; <a href="/refund/">Refund</a><br><a href="/accessibility/">Accessibility</a> &middot; <a href="/disclaimer/">Disclaimer</a><br><a href="/credits/">Credits</a></div>
</div>
<div class="fine">&copy; {datetime.date.today().year} {SITE["name"]}. An educational resource &mdash; not professional advice. Contact: {SITE["email"]}</div>
</div></footer>
<script src="/assets/js/main.js"></script><script src="/assets/js/filter.js"></script><script src="/assets/js/wiki.js"></script><script src="/assets/js/books.js"></script></body></html>'''

def head_band(chip_cls,chip_label,title,crumb=""):
    crumb_html=f'<nav class="crumbs">{crumb}</nav>' if crumb else ''
    return f'''<div class="head-band hb-{chip_cls}"><div class="wrap">{crumb_html}<span class="eyebrow">{chip_label}</span><h1>{html.escape(title)}</h1></div></div>'''

def newsletter_cta():
    return ('<div class="newsletter-cta">'
      '<h3>Get the Navigator newsletter</h3><p style="max-width:48ch;margin:.4em auto 1.1em">New breakdowns of how the greats think, build, and decide &mdash; on LinkedIn and mirrored here.</p>'
      '<a class="btn" href="/newsletter/">Read the newsletter &rarr;</a></div>')

def write(path,content,priority="0.7",freq="monthly"):
    if path.endswith(".xml") or path.endswith(".txt"):
        full=os.path.join(OUT,path.strip("/"))
    else:
        full=os.path.join(OUT,path.strip("/"),"index.html")
        depth=len([s for s in path.strip("/").split("/") if s])
        content=relativize(content, depth)
    os.makedirs(os.path.dirname(full),exist_ok=True)
    open(full,"w").write(content)
    if not (path.endswith(".xml") or path.endswith(".txt")):
        PAGES.append((path if path.endswith("/") else path+"/",priority,freq))

# ---------- markdown pages ----------
MD_EXT=["tables","fenced_code","sane_lists"]
def md_clean(text):
    lines=text.split("\n"); out=[]; title=None; desc=None
    for ln in lines:
        s=ln.strip()
        if title is None and s.startswith("# "): title=s[2:].strip(); continue
        if s.startswith("**Two-link footer") or s.startswith("*Two-link footer") or s.startswith("*Route:*"): continue
        if desc is None and s.startswith(">"): desc=re.sub(r'[*>#`]','',s).strip()
        out.append(ln)
    body="\n".join(out)
    if not desc:
        m=re.search(r'\n([A-Z][^\n]{60,200})\n',body); desc=(m.group(1) if m else SITE["desc"])
    desc=re.sub(r'[*`_#>\[\]]','',desc)[:180]
    return title or "Untitled",desc,body

def render_md_page(md_file,path,chip_cls,chip_label,crumb):
    raw=open(os.path.join(SRC_MD,md_file)).read()
    title,desc,body=md_clean(raw)
    body_html=markdown.markdown(body,extensions=MD_EXT)
    art={"@context":"https://schema.org","@type":"Article","headline":title,"description":desc,
         "author":{"@type":"Person","name":SITE["author"]},"publisher":{"@type":"Organization","name":SITE["name"]},
         "mainEntityOfPage":SITE["url"]+path,"inLanguage":"en"}
    doc=head(title,desc,path,"article",art)+nav()
    doc+=head_band(chip_cls,chip_label,title,crumb)
    doc+=f'<main class="wrap"><div class="read"><article class="doc">{body_html}</article>{newsletter_cta()}</div></main>'
    doc+=footer(); write(path,doc,"0.8")

# ---------- home ----------
def cat_card(cluster,label,symbol,title,desc,url):
    return (f'<a class="card" href="{url}"><div class="ico bg-{cluster}">{symbol}</div>'
            f'<span class="chip {cluster}">{label}</span><h3>{title}</h3><p>{desc}</p></a>')

def render_home():
    faq={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
      {"@type":"Question","name":"What is Navigator?","acceptedAnswer":{"@type":"Answer","text":"Navigator is a free, open, no-login learning studio for how the world's greatest people and companies think, build, and decide — with usable interactive tools, deep guides, and a living newsletter, for anyone in any industry."}},
      {"@type":"Question","name":"Do I need an account?","acceptedAnswer":{"@type":"Answer","text":"No. Everything is open and directly accessible without any login, account, or paywall. Tools run in your browser and save to your own device only."}},
      {"@type":"Question","name":"Who is it for?","acceptedAnswer":{"@type":"Answer","text":"Leaders, employees, students, managers, founders, and lifelong learners in every industry who want to learn from the best and apply it with practical tools."}}]}
    tiles=''.join([
      avatar("&#920;","brand"),avatar("SJ","people"),avatar("CC","news"),
      avatar("WB","biz"),avatar("AN","strat"),avatar("BF","learn")])
    doc=head(SITE["name"]+" — "+SITE["tagline"],SITE["desc"],"/","website",faq)+nav()
    doc+=f'''<main>
<section class="hero"><div class="wrap"><div class="hero-grid">
<div>
<span class="kicker">The open learning studio</span>
<h1>Learn how the greats <span class="hl">think, build &amp; decide.</span></h1>
<p class="lead">{SITE["desc"]}</p>
<div class="cta-row"><a class="btn" href="/people/">Start exploring &rarr;</a><a class="btn tools" href="/tools/">Use a tool</a><a class="btn ghost" href="/newsletter/">Read the newsletter</a></div>
<div class="trust">
<span class="chiplet"><b>100%</b> free &amp; open</span>
<span class="chiplet"><b>No</b> login, ever</span>
<span class="chiplet"><b>9</b> knowledge libraries</span>
<span class="chiplet"><b>Tools</b> you actually use</span>
</div>
</div>
<div class="hero-collage">{tiles}</div>
</div></div></section>

<div class="wrap">

<section class="section">
<span class="sec-eyebrow">Start with a question</span>
<h2>What are you trying to figure out?</h2>
<p style="color:var(--ink-soft);max-width:60ch">Every path pulls together people, companies, models, and tools &mdash; so you learn the way the best actually learned: by connecting the dots.</p>
<div class="grid c4" style="margin-top:18px">
<a class="path" href="/businesses/"><div class="num">01</div><h3>Build something enduring</h3><p>Study founders, companies, moats, and how durable advantage is really made.</p></a>
<a class="path" href="/decision-tools/"><div class="num">02</div><h3>Make a hard decision</h3><p>Use proven decision tools and see how great operators actually chose.</p></a>
<a class="path" href="/mental-models/"><div class="num">03</div><h3>Sharpen your judgment</h3><p>Borrow the thinking lenses behind careers, reversals, and big calls.</p></a>
<a class="path" href="/business-models/"><div class="num">04</div><h3>Understand an industry</h3><p>Trace business models and strategic moves and how they change over time.</p></a>
</div>
</section>

<section class="section">
<span class="sec-eyebrow">Explore the library</span>
<h2>Nine ways to learn</h2>
<div class="grid c3" style="margin-top:18px">
{cat_card("people","People","&#9679;","The greats &amp; hidden number-twos","Founders, operators, investors &mdash; and the executors who built beside the famous names.","/people/")}
{cat_card("biz","Businesses","&#9670;","How companies really work","Story, playbook, and a business breakdown for the companies that shaped the modern world.","/businesses/")}
{cat_card("strat","Mental Models","&#9650;","Decision-making lenses","~1,045 thinking tools across 12 categories, for cutting through any problem.","/mental-models/")}
{cat_card("strat","Decision Tools","&#9632;","Step-by-step methods","44 structured tools for framing, stress-testing, and making the call.","/decision-tools/")}
{cat_card("strat","Moats","&#11041;","Durable advantage","Helmer's 7 Powers &mdash; what makes an advantage last, and how to build one.","/moats/")}
{cat_card("strat","Business Models","&#9671;","How value is captured","~55 revenue engines and monetization patterns, with real company examples.","/business-models/")}
{cat_card("learn","Guides","&#9733;","How-to for thinking","Practical, evidence-based guides on focus, learning, decisions, and judgment.","/guides/")}
{cat_card("learn","Books &amp; Lists","&#9634;","Reusable frameworks","Deep book summaries and curated reading lists &mdash; ideas you keep, not forget.","/books/")}
{cat_card("tools","Tools","&#10022;","Use it, don't just read it","Interactive tools that give you a downloadable, shareable result. No login.","/tools/")}
</div>
</section>

<section class="band">
<span class="sec-eyebrow">Why bother?</span>
<h2>Why study the greats?</h2>
<p class="big">Warren Buffett read through his local library before he turned twenty. The people who built the most enduring companies were fanatical students of the people who came before them.</p>
<p style="color:var(--ink-soft)">Nobody is born great &mdash; they <em>become</em> great, and the education that gets them there used to take decades to assemble. Navigator exists so it doesn't have to: an open, patient place to learn the patterns behind how the best think, build, and decide &mdash; and then actually use them.</p>
</section>

<section class="section">
<span class="sec-eyebrow">The difference</span>
<h2>Use it, don't just read it</h2>
<div class="grid c3" style="margin-top:18px">
{cat_card("tools","Tool","&#10022;","Decision Matrix","Weight your criteria, score your options, download a ranked answer.","/tools/decision-matrix/")}
{cat_card("tools","Tool","&#11041;","Moat Analyzer","Score a business on the 7 Powers; download a defensibility profile.","/tools/moat-analyzer/")}
{cat_card("tools","Tool","&#10024;","More tools","Pricing chooser, pre-mortem, model finder &mdash; the workshop is growing.","/tools/")}
</div>
</section>

<section class="section">
<span class="sec-eyebrow">This week</span>
<h2>From the newsletter</h2>
<div class="grid c3" style="margin-top:18px">
<a class="card" href="/newsletter/welcome-navigator/"><div class="card-media bg-news">&#920;</div><span class="chip news">Newsletter</span><h3>Welcome to Navigator</h3><p>Why this exists, what's inside, and how to use an open library with tools.</p></a>
<a class="card" href="/mental-models/the-bitter-lesson/"><div class="card-media bg-strat">&#9650;</div><span class="chip strat">Mental Model</span><h3>The Bitter Lesson</h3><p>Why scale beats cleverness &mdash; and where your moat should really live.</p></a>
<a class="card" href="/businesses/airbnb/"><div class="card-media bg-biz">&#9670;</div><span class="chip biz">Business</span><h3>Airbnb</h3><p>The trust company that learned to sell the whole trip &mdash; to 2026.</p></a>
</div>
</section>
{newsletter_cta()}
</div></main>'''
    doc+=footer(); write("/",doc,"1.0","weekly")

# ---------- simple pages ----------
def simple(path,title,desc,body_html,chip=("news","")):
    doc=head(title,desc,path)+nav()+head_band(chip[0],chip[1] or title,title)
    doc+=f'<main class="wrap"><div class="read"><article class="doc">{body_html}</article></div></main>'+footer()
    write(path,doc)

def render_about():
    body='''
<p class="thesis">Navigator exists to make the world's best thinking about how to build, lead, and decide <em>open to everyone</em> &mdash; no login, no paywall &mdash; and genuinely useful, not just readable.</p>
<h2>What we share</h2>
<p>The people who built the most consequential companies, movements, and ideas left behind patterns &mdash; ways of thinking, deciding, and operating that repeat across eras and industries. Most of that wisdom is locked inside expensive books, paywalled courses, or private notebooks. Navigator pulls it into one open place and does three things with it.</p>
<p><strong>First, we go deep.</strong> Every profile, model, and guide is written to be reference-grade &mdash; longer and more complete than a quick summary, with real examples, honest limits, and a clear "here's how to use this."</p>
<p><strong>Second, we make it usable.</strong> Where an idea can become a tool you operate &mdash; a decision matrix, a moat analyzer, a pre-mortem &mdash; it does. You don't just read about the method; you run it, and download the result.</p>
<p><strong>Third, we surface the hidden builders.</strong> History remembers the famous founder and forgets the operator who made it work. Navigator deliberately profiles the "number-twos" &mdash; the executors, co-founders, and strategists behind the celebrated names &mdash; because that's often where the most transferable lessons live.</p>
<h2>Who it's for</h2>
<p>Anyone who wants to get better at the work of thinking and building: founders and operators, employees levelling up, students, managers, and lifelong learners &mdash; in <em>any</em> industry.</p>
<h2>How it's made</h2>
<p>Navigator is built with human editorial judgment and AI used as a research-and-drafting tool. Humans decide what's covered, how it's structured, and what ships; AI helps extract facts and draft in our format; every page is reviewed and fact-checked. We write original prose, never reproduce copyrighted text, and check our work for originality before publishing.</p>
<h2>The promise</h2>
<p>Open, free, and useful &mdash; a compass for learning from the greats, pointed at whatever you're trying to build next.</p>
<div class="footer-links"><a href="/newsletter/">Newsletter</a><a href="/tools/">Tools</a><a href="/contact/">Contact</a></div>'''
    simple("/about/","About Navigator","What Navigator shares: open, deep, usable knowledge on how the greats think, build, and decide — for everyone, no login.",body,("news","About"))

def render_contact():
    body=f'''
<p class="thesis">Have a topic to suggest, a correction, a collaboration, or just want to say hello? I'd love to hear from you.</p>
<p style="font-size:1.35rem"><strong>Email:</strong> <a href="mailto:{SITE["email"]}">{SITE["email"]}</a></p>
<p>Good things to reach out about: a founder, company, model, or decision you'd like broken down; a mistake you spotted; a tool you wish existed here; or partnership and newsletter ideas.</p>
<div class="footer-links"><a href="/newsletter/">Newsletter</a><a href="/about/">About</a></div>'''
    simple("/contact/","Contact","Contact Navigator — suggest a topic, a correction, or a collaboration. Email wvijay@icloud.com.",body,("news","Say hello"))

LEGAL={
 "privacy":("Privacy Policy","<p>Navigator has <strong>no user accounts and no login</strong>. We don't ask you to register and don't collect personal profiles. Interactive tools run entirely in your browser; anything you save stays on <em>your own device</em> and is never sent to us. If privacy-respecting analytics or a CDN (e.g., Cloudflare) serve the site, standard technical logs may be processed by those providers to deliver and secure it. We don't sell data. Questions: wvijay@icloud.com.</p>"),
 "terms":("Terms of Use","<p>Navigator is provided for <strong>educational and informational purposes</strong>, \"as is,\" without warranties. You may read, share, and link to pages freely. Please don't republish substantial portions as your own. Tools are aids to thinking, not professional advice. Contact: wvijay@icloud.com.</p>"),
 "cookies":("Cookie Policy","<p>Navigator sets <strong>no marketing or tracking cookies</strong> and requires no login. Your browser may store preferences (like the readable-font toggle) locally. Privacy-respecting analytics or a CDN may set minimal technical cookies to deliver and secure the site. Clear them anytime in your browser.</p>"),
 "refund":("Refund Policy","<p>Navigator is <strong>free</strong> &mdash; there's nothing to purchase and therefore nothing to refund. If paid products are ever offered, a clear refund policy will be published here at that time.</p>"),
 "accessibility":("Accessibility","<p>Navigator aims for <strong>WCAG 2.1 AA</strong>: semantic HTML, keyboard-navigable menus and tools, sufficient colour contrast, descriptive alt text, and a one-tap <strong>readable-font toggle</strong> (Atkinson Hyperlegible) in the menu. Found a barrier? Email wvijay@icloud.com.</p>"),
 "disclaimer":("Disclaimer","<p>Navigator is an <strong>educational resource</strong>, not professional, legal, financial, medical, or investment advice. Content is written with care and reviewed, but may contain errors or become outdated. Do your own diligence and consult a qualified professional before high-stakes decisions.</p>"),
 "credits":("Credits","<p>Navigator's illustrations, avatar tiles, and logo are original work. Where a person photo or company logo is used, we prioritise <strong>public-domain and openly-licensed sources</strong> (e.g., Wikimedia Commons); any attribution a specific licence requires is listed here in one place, so individual pages stay clean. Believe an asset is used incorrectly? Email wvijay@icloud.com and we'll correct or remove it promptly.</p><p class=\"mono\" style=\"font-size:.85rem\">Fonts: Baloo 2, Lexend, Space Mono, Atkinson Hyperlegible &mdash; all open-source.</p>"),
}
def render_legal():
    for slug,(title,body) in LEGAL.items():
        simple(f"/{slug}/",title,f"{title} — Navigator.",body,("news",title))

# ---------- newsletter ----------
ARTICLES=[
 {"slug":"welcome-navigator","title":"Welcome to Navigator: an open workshop for learning from the greats",
  "date":"2026-08-11","summary":"Why Navigator exists, what's inside, and how to get the most from an open, no-login library with tools you can actually use.",
  "linkedin":"https://www.linkedin.com/",
  "body":'''<p class="thesis">Most knowledge about how the best people and companies actually operate is locked away &mdash; in expensive books, paywalled courses, or private notebooks. Navigator is the attempt to open it up, go deeper than a summary, and make it usable.</p>
<h2>What this is</h2>
<p>Navigator is a free, open, no-login library of how the world's greatest people and companies think, build, and decide. Three things make it different: it goes <strong>deep</strong> (reference-grade pages, not skims), it's <strong>usable</strong> (tools you operate and download results from), and it surfaces the <strong>hidden number-twos</strong> &mdash; the operators who built beside the famous names.</p>
<h2>How to use it</h2>
<p>Start anywhere. Browse the <a href="/mental-models/">mental models</a> and <a href="/moats/">moats</a>, run a <a href="/tools/">tool</a> on a real decision, or read a deep profile like <a href="/businesses/airbnb/">Airbnb</a>. Everything is open and directly linkable &mdash; no account, ever.</p>
<h2>The newsletter</h2>
<p>Each week I break down a founder, a company, a model, or a decision &mdash; published on LinkedIn and mirrored here so it lives in one open archive. Want to shape what's next? <a href="/contact/">Tell me what to cover</a>.</p>'''},
]
def render_newsletter():
    items=""
    for a in ARTICLES:
        items+=f'<a class="card" href="/newsletter/{a["slug"]}/"><div class="card-media bg-news">&#920;</div><span class="chip news">{a["date"]}</span><h3>{html.escape(a["title"])}</h3><p>{html.escape(a["summary"])}</p></a>'
    doc=head("Newsletter","Every Navigator article in one open archive — breakdowns of how the greats think, build, and decide.","/newsletter/")+nav()
    doc+=head_band("news","Newsletter","The Navigator newsletter","<a href=\"/\">Home</a> &rsaquo; Newsletter")
    doc+=f'<main class="wrap"><p class="lead" style="color:var(--ink-soft);max-width:60ch">New breakdowns of how the greats think, build, and decide &mdash; published on LinkedIn and mirrored here in one open, no-login archive. This index lists every article.</p><div class="grid c3" style="margin-top:18px">{items}</div>{newsletter_cta()}</main>'+footer()
    write("/newsletter/",doc,"0.9","weekly")
    for a in ARTICLES:
        art={"@context":"https://schema.org","@type":"Article","headline":a["title"],"datePublished":a["date"],"description":a["summary"],
             "author":{"@type":"Person","name":SITE["author"]},"publisher":{"@type":"Organization","name":SITE["name"]},
             "mainEntityOfPage":SITE["url"]+"/newsletter/"+a["slug"]+"/","inLanguage":"en"}
        d=head(a["title"],a["summary"],f"/newsletter/{a['slug']}/","article",art)+nav()
        d+=head_band("news",f"Newsletter &middot; {a['date']}",a["title"],'<a href="/">Home</a> &rsaquo; <a href="/newsletter/">Newsletter</a>')
        d+=f'<main class="wrap"><div class="read"><article class="doc">{a["body"]}<p style="margin-top:24px"><a class="btn ghost" href="{a["linkedin"]}" rel="noopener">&#8599; Originally published on LinkedIn</a></p></article>{newsletter_cta()}</div></main>'+footer()
        write(f"/newsletter/{a['slug']}/",d,"0.7")

# ---------- tools ----------
def render_tools_hub():
    doc=head("Tools — use the ideas, don't just read them","Free interactive tools for any industry: Decision Matrix, Moat Analyzer, and more. No login; download and share your results.","/tools/")+nav()
    doc+=head_band("tools","Tools","Use it, don't just read it","<a href=\"/\">Home</a> &rsaquo; Tools")
    def t(sym,title,desc,url,ready=True):
        badge='' if ready else ' <span class="pill">soon</span>'
        return f'<a class="card" href="{url}"><div class="ico bg-tools">{sym}</div><h3>{title}{badge}</h3><p>{desc}</p></a>'
    doc+=f'''<main class="wrap"><p class="lead" style="color:var(--ink-soft);max-width:62ch">Don't just read about a method &mdash; run it. Every tool works in your browser, needs no login, and lets you <strong>download or share your result</strong>. Built for leaders, employees, students, and managers in any industry.</p>
<div class="section-title"><span class="dot bg-tools"></span><h2 style="margin:0">Decide</h2></div>
<div class="grid c3">
{t("&#10022;","Decision Matrix","Weight your criteria, score your options, get a ranked, downloadable answer.","/tools/decision-matrix/")}
{t("&#9906;","Decision Tree (EV)","Enter options and probability-weighted outcomes; rank by expected value.","/tools/decision-tree/")}
{t("&#9709;","Eisenhower Matrix","Sort tasks into urgent/important quadrants; download the board.","/tools/eisenhower-matrix/")}
{t("&#9632;","Impact&ndash;Effort Matrix","Plot ideas by impact vs effort; quick wins light up.","/tools/impact-effort-matrix/")}
</div>
<div class="section-title"><span class="dot bg-tools"></span><h2 style="margin:0">Strategise</h2></div>
<div class="grid c3">
{t("&#11041;","Moat Analyzer","Score a business against Helmer's 7 Powers; download a defensibility radar.","/tools/moat-analyzer/")}
{t("&#9671;","Pricing-Model Chooser","Per-seat vs usage vs outcome &mdash; find the right pricing shape.","/tools/pricing-model-chooser/")}
{t("&#9723;","SWOT Builder","Map strengths, weaknesses, opportunities, threats; download the 2&times;2.","/tools/swot-builder/")}
</div>
<div class="section-title"><span class="dot bg-tools"></span><h2 style="margin:0">Organise &amp; think</h2></div>
<div class="grid c3">
{t("&#9783;","RACI Matrix","Make ownership unambiguous across tasks and people; export CSV.","/tools/raci-matrix/")}
{t("&#9650;","Mental-Model Finder","Describe your problem; get the thinking models that fit.","/tools/mental-model-finder/")}
</div>
<p class="count-note" style="margin-top:20px">More tools ship every batch &mdash; this collection keeps growing. Have a request? <a href="/contact/">Tell us</a>.</p>
</main>'''+footer()
    write("/tools/",doc,"0.9")

def render_tool_page(slug,title,desc,intro,tool_html,init_js,concept_html):
    doc=head(title,desc,f"/tools/{slug}/")+nav()
    doc+=head_band("tools","Interactive tool",title,'<a href="/">Home</a> &rsaquo; <a href="/tools/">Tools</a>')
    doc+=f'<main class="wrap"><div class="read"><p class="lead" style="color:var(--ink-soft)">{intro}</p>{tool_html}<article class="doc">{concept_html}</article>{newsletter_cta()}</div></main>'
    doc+=f'<script src="/assets/js/tools.js"></script><script>{init_js}</script>'+footer()
    write(f"/tools/{slug}/",doc,"0.8")

def render_stub(path,title,desc,chip,intro,cards_html):
    body=f'<p class="thesis">{intro}</p><div class="grid c2">{cards_html}</div>'
    simple(path,title,desc,body,chip)

def mini_card(cluster,label,sym,title,desc,url):
    return f'<a class="card" href="{url}"><div class="ico bg-{cluster}">{sym}</div><span class="chip {cluster}">{label}</span><h3>{title}</h3><p>{desc}</p></a>'

# =========================== BUILD ===========================
def main():
    if os.path.exists(OUT): shutil.rmtree(OUT)
    os.makedirs(OUT)
    shutil.copytree(os.path.join(ROOT,"assets"),os.path.join(OUT,"assets"))
    # favicon + og (theta mark)
    favicon='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0C5460"/><stop offset="1" stop-color="#06A6A0"/></linearGradient></defs><circle cx="24" cy="24" r="22" fill="url(#g)"/><text x="24" y="34" font-family="Georgia,serif" font-size="30" fill="#fff" text-anchor="middle" font-weight="bold">&#920;</text></svg>'
    open(os.path.join(OUT,"assets","img","favicon.svg"),"w").write(favicon)
    og='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0C5460"/><stop offset="1" stop-color="#06A6A0"/></linearGradient></defs><rect width="1200" height="630" fill="#FFFDF6"/><circle cx="150" cy="150" r="90" fill="url(#g)"/><text x="150" y="188" font-family="Georgia,serif" font-size="120" fill="#fff" text-anchor="middle" font-weight="bold">&#920;</text><text x="290" y="175" font-family="Georgia,serif" font-size="86" fill="#2A2140" font-weight="bold">Navigator</text><text x="150" y="360" font-family="sans-serif" font-size="46" fill="#2A2140" font-weight="bold">Learn how the greats think, build &amp; decide.</text><text x="150" y="430" font-family="sans-serif" font-size="30" fill="#6a5f82">Open &middot; No login &middot; Tools you actually use &middot; navigator.blog</text></svg>'
    open(os.path.join(OUT,"assets","img","og.svg"),"w").write(og)

    render_home(); render_about(); render_contact(); render_legal(); render_newsletter(); render_tools_hub(); render_ai()

    render_tool_page("decision-matrix","Decision Matrix (weighted scoring)",
      "Free weighted decision-matrix tool. Score options across weighted criteria, get a ranked answer, download PNG or CSV. No login.",
      "Choose between options rationally: list your options and the criteria that matter (with weights), score each 0&ndash;10, and get a weighted ranking you can download and share.",
      '<div id="dm"></div>','initDecisionMatrix("dm");',
      '<h2>When to use it</h2><p>Any multi-criteria choice &mdash; a vendor, a hire, a roadmap, a job offer, a house. The matrix separates <em>what matters</em> (criteria and weights) from <em>how each option scores</em>, so the decision stops being a vibe and becomes a defensible number. Pair it with a <a href="/decision-tools/ai-assisted-pre-mortem/">pre-mortem</a> for high-stakes calls.</p>')
    render_tool_page("moat-analyzer","Moat Analyzer (7 Powers)",
      "Free moat-analysis tool based on Hamilton Helmer's 7 Powers. Score a business's defensibility and download a radar profile. No login.",
      "Score any business against the only seven durable sources of competitive advantage, and download a defensibility profile you can share.",
      '<div id="ma"></div>','initMoatAnalyzer("ma");',
      '<h2>How to read your score</h2><p>A high total across several Powers means a genuinely wide moat; a high score on one means a real but concentrated advantage to widen; a low score means you have a product, not yet a defended business. Learn the framework in depth on the <a href="/moats/">Moats</a> page.</p>')

    render_tool_page("eisenhower-matrix","Eisenhower Matrix",
      "Free Eisenhower Matrix tool. Sort your tasks by urgency and importance into Do / Schedule / Delegate / Eliminate — download the result. No login.",
      "Enter your tasks, mark each urgent and/or important, and see them sorted into the four quadrants — then download the board.",
      '<div id="ei"></div>','initEisenhower("ei");',
      '<h2>When to use it</h2><p>When your to-do list is long and everything feels urgent. The matrix forces the distinction between <em>urgent</em> (loud, time-pressured) and <em>important</em> (actually moves your goals). Most people over-invest in urgent-not-important work; this makes that visible. Pair with the <a href="/tools/impact-effort-matrix/">Impact–Effort</a> tool for prioritising projects.</p>')

    render_tool_page("impact-effort-matrix","Impact–Effort Matrix",
      "Free Impact–Effort matrix tool. Plot ideas by impact vs effort to find quick wins — download the chart. No login.",
      "List your ideas, rate each on impact and effort, and see them plotted on a 2×2 — quick wins (high impact, low effort) light up green.",
      '<div id="ie"></div>','initImpactEffort("ie");',
      '<h2>When to use it</h2><p>Prioritising a backlog, a roadmap, or a list of bets. Do the quick wins first, schedule the big projects, and be honest about the low-impact/high-effort work you should just drop. Pair with the <a href="/tools/decision-matrix/">Decision Matrix</a> when options need weighted criteria.</p>')

    render_tool_page("pricing-model-chooser","Pricing-Model Chooser",
      "Free pricing-model chooser. Answer three questions and get a recommended pricing shape — per-seat, usage-based, or outcome-based. No login.",
      "Answer three quick questions about how your product delivers value, who buys it, and how usage behaves, and get a recommended pricing model with the trade-offs.",
      '<div id="pc"></div>','initPricingChooser("pc");',
      '<h2>How to use it</h2><p>Pricing is strategy, not a number. The right <em>shape</em> — per-seat, usage, or outcome — depends on how value is delivered and who\'s buying. Read the deep dive on <a href="/business-models/usage-based-ai-metered/">usage-based / AI-metered pricing</a> for where software pricing is heading.</p>')

    render_tool_page("swot-builder","SWOT Builder",
      "Free SWOT analysis tool. Fill in Strengths, Weaknesses, Opportunities, and Threats and download the 2×2. No login.",
      "Map your Strengths, Weaknesses, Opportunities, and Threats in one 2×2 and download it as an image to share.",
      '<div id="sw"></div>','initSWOT("sw");',
      '<h2>When to use it</h2><p>Before a strategy offsite, a launch, or a big decision. Strengths and Weaknesses are <em>internal</em> and mostly in your control; Opportunities and Threats are <em>external</em>. The value isn\'t the four boxes — it\'s the actions that fall out of crossing them (use a strength to seize an opportunity; fix a weakness a threat could exploit).</p>')

    render_tool_page("raci-matrix","RACI Matrix",
      "Free RACI matrix tool. Assign Responsible, Accountable, Consulted, Informed across tasks and people; download as CSV. No login.",
      "List your tasks and people, then assign R / A / C / I in each cell to make ownership unambiguous — and export to CSV.",
      '<div id="ra"></div>','initRACI("ra");',
      '<h2>When to use it</h2><p>Any project where &ldquo;who owns this?&rdquo; is fuzzy. The one rule that saves projects: exactly <strong>one Accountable</strong> per row. Too many C\'s and I\'s slow everything down — be ruthless about who truly needs to be consulted versus merely informed.</p>')

    render_tool_page("decision-tree","Decision Tree (Expected Value)",
      "Free expected-value decision tree. Enter options and their probability-weighted outcomes and see them ranked by EV. No login.",
      "For each option, list outcomes as probability and value; the tool computes expected value and ranks your options.",
      '<div id="dt"></div>','initDecisionTree("dt");',
      '<h2>How to read it</h2><p>Expected value turns a fuzzy gamble into a number: the sum of each outcome\'s value weighted by its probability. The highest EV is a strong default — but never bet the farm on a positive EV whose downside you can\'t survive. Pair with a <a href="/decision-tools/ai-assisted-pre-mortem/">pre-mortem</a> to pressure-test the probabilities.</p>')

    render_tool_page("mental-model-finder","Mental-Model Finder",
      "Free mental-model finder. Describe your problem and get the thinking models that fit, linked to full explanations. No login.",
      "Describe your situation in a sentence and get matched to the mental models most likely to help — each linked to its page.",
      '<div id="mf"></div>','initModelFinder("mf");',
      '<h2>How it works</h2><p>The finder matches your words against a curated set of high-leverage models. It\'s a starting point, not the whole latticework — the full library of 1,000+ models lives on the <a href="/mental-models/">Mental Models</a> page. The goal is to build the habit of reaching for a model instead of reacting on instinct.</p>')

    # flagship DEEP concept pages (kept full-length from written MD)
    P=[("airbnb-navigator-profile-full.md","/businesses/airbnb/","biz","Business &middot; Travel",'<a href="/">Home</a> &rsaquo; <a href="/businesses/">Businesses</a> &rsaquo; Airbnb'),
       ("jeff-bezos.md","/people/jeff-bezos/","people","People",'<a href="/">Home</a> &rsaquo; <a href="/people/">People</a> &rsaquo; Jeff Bezos'),
       ("warren-buffett.md","/people/warren-buffett/","people","People",'<a href="/">Home</a> &rsaquo; <a href="/people/">People</a> &rsaquo; Warren Buffett'),
       ("steve-jobs.md","/people/steve-jobs/","people","People",'<a href="/">Home</a> &rsaquo; <a href="/people/">People</a> &rsaquo; Steve Jobs'),
       ("charlie-munger.md","/people/charlie-munger/","people","People",'<a href="/">Home</a> &rsaquo; <a href="/people/">People</a> &rsaquo; Charlie Munger'),
       ("nvidia-profile.md","/businesses/nvidia/","biz","Business",'<a href="/">Home</a> &rsaquo; <a href="/businesses/">Businesses</a> &rsaquo; NVIDIA'),
       ("06-mental-models-sample.md","/mental-models/the-bitter-lesson/","strat","Mental Model",'<a href="/">Home</a> &rsaquo; <a href="/mental-models/">Mental Models</a>'),
       ("07-decision-tools-sample.md","/decision-tools/ai-assisted-pre-mortem/","strat","Decision Tool",'<a href="/">Home</a> &rsaquo; <a href="/decision-tools/">Decision Tools</a>'),
       ("01-business-models-sample.md","/business-models/usage-based-ai-metered/","strat","Business Model",'<a href="/">Home</a> &rsaquo; <a href="/business-models/">Business Models</a>'),
       ("02-frameworks-sample.md","/frameworks/vertical-ai-agents/","strat","Framework",'<a href="/">Home</a> &rsaquo; <a href="/frameworks/">Frameworks</a>'),
       ("09-book-summaries-sample.md","/books/co-intelligence/","learn","Book Summary",'<a href="/">Home</a> &rsaquo; <a href="/books/">Book Summaries</a>'),
       ("11-reading-lists-sample.md","/reading-lists/ai-native-operator/","learn","Reading List",'<a href="/">Home</a> &rsaquo; <a href="/reading-lists/">Reading Lists</a>'),
       ("13-guides-sample.md","/guides/keep-judgment-when-model-is-confident/","learn","Guide",'<a href="/">Home</a> &rsaquo; <a href="/guides/">Guides</a>'),
       ("15-quote-collections-sample.md","/quotes/ai-future-of-work/","learn","Quote Collection",'<a href="/">Home</a> &rsaquo; <a href="/quotes/">Quotes</a>')]
    for md,path,cls,label,crumb in P:
        render_md_page(md,path,cls,label,crumb)

    # ALL reserved pages: full indexes + a complete page for every roster item
    render_all_content()

    # Cloudflare headers + 404
    open(os.path.join(OUT,"_headers"),"w").write("/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  X-Frame-Options: SAMEORIGIN\n/assets/*\n  Cache-Control: public, max-age=31536000, immutable\n")
    nf=head("Off the map","Page not found.","/404")+nav()+head_band("news","404","Off the map")+'<main class="wrap"><div class="read"><p class="lead">That page doesn\'t exist yet. Head back <a href="/">home</a> or explore the <a href="/tools/">tools</a>.</p></div></main>'+footer()
    open(os.path.join(OUT,"404.html"),"w").write(relativize(nf,0))
    urls="".join(f'<url><loc>{SITE["url"]}{p}</loc><changefreq>{cf}</changefreq><priority>{pr}</priority></url>' for p,pr,cf in PAGES)
    write("/sitemap.xml",f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
    write("/robots.txt",f"User-agent: *\nAllow: /\nSitemap: {SITE['url']}/sitemap.xml\n")
    write("/llms.txt",f"# {SITE['name']}\n\n> {SITE['tagline']}\n\n{SITE['desc']}\n\nOpen, no-login educational library. Sections:\n- /mental-models/ decision lenses (~1045)\n- /decision-tools/ 44 methods\n- /business-models/ /frameworks/ /moats/ strategy\n- /books/ /reading-lists/ /guides/ /quotes/ learning\n- /tools/ interactive tools\n- /newsletter/ weekly breakdowns\nContact: {SITE['email']}\n")
    print(f"Built {len(PAGES)} pages into {OUT}")

# ============================ DATA-DRIVEN MASS RENDER ============================
TYPES=[
 ("people","/people/","people","People","category","&#9679;"),
 ("businesses","/businesses/","biz","Business","category","&#9670;"),
 ("mental-models","/mental-models/","strat","Mental Model","category","&#9650;"),
 ("decision-tools","/decision-tools/","strat","Decision Tool",None,"&#9632;"),
 ("business-models","/business-models/","strat","Business Model",None,"&#9671;"),
 ("frameworks","/frameworks/","strat","Framework",None,"&#9698;"),
 ("moats","/moats/","strat","Moat","category","&#11041;"),
 ("books","/books/","learn","Book Summary",None,"&#9634;"),
 ("reading-lists","/reading-lists/","learn","Reading List","category","&#9733;"),
 ("guides","/guides/","learn","Guide",None,"&#9733;"),
 ("quotes","/quotes/","learn","Quote Collection",None,"&#10078;"),
 ("tools","/tools/","tools","Tool",None,"&#10022;"),
 ("paths","/paths/","strat","Learning Path",None,"&#9873;"),
]
TITLE={"people":"People","businesses":"Businesses","mental-models":"Mental Models","decision-tools":"Decision Tools","business-models":"Business Models","frameworks":"Frameworks","moats":"Moats","books":"Book Summaries","reading-lists":"Reading Lists","guides":"Guides","quotes":"Quote Collections","tools":"Tools","paths":"Learning Paths"}
FEAT={
 "people":[("Jeff Bezos","/people/jeff-bezos/","Regret minimization, customer obsession, and the flywheel — a full profile."),
           ("Warren Buffett","/people/warren-buffett/","Businesses over tickers, moats, and the patience to do nothing."),
           ("Steve Jobs","/people/steve-jobs/","Taste and integration as strategy — twice reshaping whole industries."),
           ("Charlie Munger","/people/charlie-munger/","The latticework of mental models and the discipline of inversion.")],
 "businesses":[("Airbnb","/businesses/airbnb/","The trust company that learned to sell the whole trip — founding to 2026."),
               ("NVIDIA","/businesses/nvidia/","Built the platform for the AI era before the wave was obvious.")],
 "mental-models":[("The Bitter Lesson","/mental-models/the-bitter-lesson/","Why scale beats cleverness — and where your moat should really live.")],
 "decision-tools":[("AI-Assisted Pre-Mortem","/decision-tools/ai-assisted-pre-mortem/","Assume it failed; red-team it with a model; ship a safer plan.")],
 "business-models":[("Usage-Based / AI-Metered","/business-models/usage-based-ai-metered/","The seat-to-usage repricing of software, from token to outcome.")],
 "frameworks":[("Vertical AI Agents","/frameworks/vertical-ai-agents/","Agents that do the work, not just assist — the 2026 opportunity.")],
 "books":[("Co-Intelligence","/books/co-intelligence/","Ethan Mollick on working with AI: the jagged frontier and four rules.")],
 "reading-lists":[("The AI-Native Operator","/reading-lists/ai-native-operator/","A curated syllabus for operating in the age of capable AI.")],
 "guides":[("Keep Judgment When the Model Is Confident","/guides/keep-judgment-when-model-is-confident/","Stay the human in the loop when the machine always sounds sure.")],
 "quotes":[("AI & the Future of Work","/quotes/ai-future-of-work/","The augment-vs-replace debate in verified quotes.")],
}
SKIP={
 "people":{"jeff-bezos","warren-buffett","steve-jobs","charlie-munger"},
 "businesses":{"airbnb","nvidia"},"mental-models":{"the-bitter-lesson"},"decision-tools":{"ai-assisted-pre-mortem"},
 "business-models":{"usage-based-ai-metered"},"frameworks":{"vertical-ai-agents"},"books":{"co-intelligence"},
 "reading-lists":{"ai-native-operator"},"guides":{"keep-judgment-when-model-is-confident"},
 "quotes":{"ai-future-of-work"},"tools":{"decision-matrix","moat-analyzer","eisenhower-matrix","impact-effort-matrix","pricing-model-chooser","swot-builder","raci-matrix","decision-tree","mental-model-finder"},
}
def _initials(name):
    ws=[w for w in re.sub(r'[^A-Za-z0-9 ]',' ',name).split() if w]
    if not ws: return "N"
    return (ws[0][:2] if len(ws)==1 else ws[0][0]+ws[1][0]).upper()

def _faq(pairs, path):
    qa="".join(f'<details class="faq-item"><summary>{q}</summary><div>{a}</div></details>' for q,a in pairs)
    ld={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":re.sub('<[^>]+>','',a)}} for q,a in pairs]}
    return f'<h2>Frequently asked</h2><div class="faq">{qa}</div><script type="application/ld+json">{json.dumps(ld)}</script>'

def render_item_page(x,key,base,cluster,chip,gf,sibs):
    name=x["name"]; s=x["slug"]; path=f"{base}{s}/"; blurb=(x.get("blurb") or "").strip()
    author=(x.get("author") or "").strip(); cat=x.get("category","") or TITLE[key]
    if key=="books": author=" ".join(author.split()[:2]) if author else ""
    E=html.escape; crumb=f'<a href="/">Home</a> &rsaquo; <a href="{base}">{TITLE[key]}</a>'
    thesis = blurb if blurb else (f"{name} — a {TITLE[key][:-1].lower()} in Navigator's collection.")
    sib="".join(f'<a class="card fcard pcard" href="{base}{y["slug"]}/" data-name="{E(y["name"].lower())}"><div class="card-media bg-{cluster}" {("data-wiki=\""+E(y["name"])+"\"") if cluster in ("people","biz") else ("data-book=\""+E(y["name"])+"\"" if key=="books" else "")}>{_initials(y["name"]) if cluster in ("people","biz") or key=="books" else chip}</div><span class="chip {cluster}">{chip}</span><h3>{E(y["name"])}</h3><p>{E((y.get("blurb") or "")[:80])}</p></a>' for y in sibs)
    connected=f'<div class="section-title"><span class="dot bg-{cluster}"></span><h2 style="margin:0">Connected</h2></div><div class="grid c3">{sib}</div>'
    footlinks=f'<div class="footer-links"><a href="{base}">All {TITLE[key]}</a><a href="/tools/">Tools</a><a href="/newsletter/">Newsletter</a></div>'
    art={"@context":"https://schema.org","@type":"Article","headline":name,"description":thesis[:160],
         "publisher":{"@type":"Organization","name":SITE["name"]},"mainEntityOfPage":SITE["url"]+path,"inLanguage":"en"}
    doc=head(name,thesis[:160],path,"article",art)+nav()+head_band(cluster,chip,name,crumb)

    if cluster in ("people","biz"):
        person = cluster=="people"
        story = (f"<p>{E(blurb)}</p>" if blurb else "") + (
            f"<p>{E(name)} is one of the <strong>{E(cat)}</strong> profiles in Navigator&rsquo;s library of people and companies worth studying closely. "
            f"The aim here is not trivia but transfer: to pull out the decisions, habits, and structural bets that you can actually apply to your own work.</p>"
            f"<p>As you read, treat this less like a biography and more like a case study. Ask what {E(name.split()[0])} understood early, what they were willing to be misunderstood about, and which advantages compounded quietly over years.</p>")
        if person:
            playbook=("<h2>The playbook &mdash; what to study</h2>"
              "<p>Every operator worth studying repeats a small number of moves. These are the lenses to read this profile through:</p><ul>"
              "<li><strong>The early bet.</strong> The non-obvious wager made before it was obvious &mdash; and what they saw that others missed.</li>"
              "<li><strong>What they refused to do.</strong> The disciplined <em>no</em>s usually matter more than the yeses. Where did they stay narrow when it would have been easy to sprawl?</li>"
              "<li><strong>The compounding advantage.</strong> The asset that got stronger over time &mdash; a brand, a network, a system, a reputation, a body of work.</li>"
              "<li><strong>Decisions under uncertainty.</strong> How they acted when the facts were incomplete and the stakes were high.</li>"
              "<li><strong>How they treated people.</strong> Who they hired, kept, and trusted &mdash; and the culture that resulted.</li></ul>")
            apply_h=("<h2>How to apply their approach</h2><ul>"
              "<li>Pick one decision you&rsquo;re facing this week and run it through their lens above.</li>"
              "<li>Write down the one thing they&rsquo;d refuse to do in your situation &mdash; then consider refusing it too.</li>"
              "<li>Name the compounding asset you could start building now that would look obvious in ten years.</li></ul>")
            quotes="<h2>In their own words</h2><p class=\"count-note\">Verified, correctly-attributed quotes are added here as we confirm sources &mdash; we don&rsquo;t publish quotes we can&rsquo;t verify.</p>"
            faq=_faq([(f"Who is {name}?", f"{E(name)} is a {E(cat).lower()} featured in Navigator&rsquo;s People library for the transferable lessons in how they think, build, and decide."),
                      (f"What can you learn from {name}?", "Read the profile for the early bet they made, the things they refused to do, and the advantage that compounded over time &mdash; then apply those lenses to your own decisions."),
                      ("How should I study a person like this?", "Treat the profile as a case study, not a biography: extract decisions and principles you can reuse, and pair it with the interactive tools and connected mental models.")], path)
            extra=playbook+apply_h+quotes
        else:
            playbook=("<h2>The playbook &mdash; how it really works</h2>"
              "<p>Behind every enduring company is a small set of structural choices. Read this profile for:</p><ul>"
              "<li><strong>The model.</strong> How the business creates, delivers, and captures value &mdash; and where the margin actually comes from.</li>"
              "<li><strong>The moat.</strong> Which durable advantage it holds: scale, network effects, switching costs, brand, counter-positioning, a cornered resource, or process power.</li>"
              "<li><strong>The turning points.</strong> The decisions and bets that changed the trajectory.</li>"
              "<li><strong>The flywheel.</strong> The self-reinforcing loop that makes each part strengthen the others.</li>"
              "<li><strong>What breaks it.</strong> The structural risks and the competitors circling.</li></ul>")
            apply_h=("<h2>How to apply the lessons</h2><ul>"
              "<li>Map your own business (or a business you admire) onto the model above.</li>"
              "<li>Identify which of the seven durable advantages you actually hold &mdash; and which you only think you hold.</li>"
              "<li>Name the flywheel you could push on this quarter.</li></ul>")
            quotes=""
            faq=_faq([(f"What is {name} known for?", f"{E(name)} is featured in Navigator&rsquo;s Businesses library as a case study in {E(cat).lower()} &mdash; how it makes money and why it&rsquo;s hard to displace."),
                      (f"What&rsquo;s {name}&rsquo;s moat?", "See the playbook above: the profile examines which durable advantages &mdash; scale, network, switching costs, brand, counter-positioning, cornered resource, or process &mdash; the business actually holds."),
                      ("How do I study a company well?", "Focus on the model, the moat, the flywheel, and what breaks it &mdash; then compare against peers using the Moat Analyzer tool.")], path)
            extra=playbook+apply_h
        body=(f'<article class="doc"><h2>Story</h2>{story}{extra}{connected}{faq}{footlinks}</article>')
        portrait=f'<div class="hero-portrait bg-{cluster}" data-wiki="{E(name)}">{_initials(name)}</div>'
        doc+=(f'<main class="wrap"><div class="read">'
              f'<div class="profile-head">{portrait}<div><p class="thesis" style="margin-top:0">{E(thesis)}</p>'
              f'<p class="mono" style="color:var(--ink-soft)">{E(cat)}</p></div></div>'
              f'{body}{newsletter_cta()}</div></main>')+footer()
    elif key=="books":
        head_tile=f'<div class="hero-portrait bg-{cluster}" style="width:132px;height:196px;border-radius:12px" data-book="{E(name)}">{_initials(name)}</div>'
        overview=f"<p>{E(blurb)}</p>" if blurb else ""
        overview+=(f"<p><em>{E(name)}</em>{(' by '+E(author)) if author else ''} is part of Navigator&rsquo;s reading library. "
                   f"This page frames what to look for and how to put the ideas to work &mdash; the summary is a guide to the book, not a replacement for it.</p>")
        secs=("<h2>What to look for</h2><ul>"
              "<li>The one central argument the author keeps returning to.</li>"
              "<li>The two or three ideas you could actually use this month.</li>"
              "<li>Where the book&rsquo;s advice would <em>not</em> apply &mdash; its limits.</li></ul>"
              "<h2>How to apply it</h2><ul>"
              "<li>Pick a single idea and design one small experiment around it this week.</li>"
              "<li>Write the book&rsquo;s thesis in one sentence in your own words &mdash; if you can&rsquo;t, re-read.</li>"
              "<li>Connect it to a decision you&rsquo;re facing and note what it would have you do differently.</li></ul>"
              "<h2>Who should read it</h2><p>Anyone working on the problems this book addresses &mdash; and anyone building the reading habit Navigator is designed around. Pair it with the connected titles below.</p>")
        faq=_faq([(f"What is {name} about?", f"{E(blurb) if blurb else E(name)+' is a book in Navigator&rsquo;s reading library.'} Read the page for what to look for and how to apply it."),
                  ("Is this a full summary?", "No &mdash; Navigator points you to the ideas and how to use them, and links licensed sources for the full text. It never reproduces the book."),
                  ("What should I read next?", "See the connected titles below and the reading lists they belong to.")], path)
        doc+=(f'<main class="wrap"><div class="read">'
              f'<div class="profile-head">{head_tile}<div><p class="thesis" style="margin-top:0">{E(thesis)}</p>'
              f'<p class="mono" style="color:var(--ink-soft)">{("by "+E(author)) if author else E(cat)}</p></div></div>'
              f'<article class="doc"><h2>Overview</h2>{overview}{secs}{connected}{faq}{footlinks}</article>'
              f'{newsletter_cta()}</div></main>')+footer()
    else:
        overview=f"<p>{E(blurb)}</p>" if blurb else f"<p>{E(name)} is part of Navigator&rsquo;s {E(cat)} collection.</p>"
        why=("<h2>Why it matters</h2><p>Good thinking is mostly a matter of reaching for the right lens at the right moment. "
             f"{E(name)} earns its place in the toolkit because it changes what you notice: it reframes a familiar situation so the important part becomes obvious and the noise falls away.</p>")
        howto=("<h2>How to apply it</h2><ol>"
               f"<li><strong>Name the situation.</strong> Write down the decision or problem where {E(name)} might apply.</li>"
               "<li><strong>Run it through the lens.</strong> Ask the one question this idea forces you to ask.</li>"
               "<li><strong>Act on what changes.</strong> If the lens changed your answer, change your plan &mdash; that&rsquo;s the whole point.</li></ol>")
        pit=("<h2>Common pitfalls</h2><ul>"
             "<li>Using it as a label instead of a tool &mdash; naming the model isn&rsquo;t the same as applying it.</li>"
             "<li>Reaching for it everywhere; every lens has a domain where it stops being useful.</li>"
             "<li>Stopping at insight instead of changing a decision.</li></ul>")
        faq=_faq([(f"What is {name}?", f"{E(blurb) if blurb else E(name)+' is part of Navigator&rsquo;s '+E(cat)+' collection.'}"),
                  (f"When should I use {name}?", "Use it when you&rsquo;re facing the kind of situation it was built for &mdash; see &ldquo;How to apply it&rdquo; above &mdash; and pair it with the connected ideas and tools."),
                  ("How does this connect to the rest of Navigator?", "It links into the wider graph of mental models, tools, people, and businesses &mdash; follow the connected cards below.")], path)
        if author: overview=f'<p class="mono" style="color:var(--ink-soft)">by {E(author)}</p>'+overview
        headtile=f'<div style="width:64px;flex:0 0 auto">{avatar(_initials(name),cluster)}</div>'
        doc+=(f'<main class="wrap"><div class="read">'
              f'<div style="display:flex;gap:16px;align-items:center;margin:2px 0 8px">{headtile}'
              f'<div class="mono" style="color:var(--ink-soft)">{E(cat)}</div></div>'
              f'<p class="thesis">{E(thesis)}</p>'
              f'<article class="doc"><h2>Overview</h2>{overview}{why}{howto}{pit}{connected}{faq}{footlinks}</article>'
              f'{newsletter_cta()}</div></main>')+footer()
    write(path,doc,"0.6")

def render_full_index(key,base,cluster,chip,gf,sym,items):
    title=TITLE[key]; img_cards = cluster in ("people","biz")
    feat="".join(f'<a class="card" href="{u}"><div class="card-media bg-{cluster}">{sym}</div><span class="chip {cluster}">Deep dive</span><h3>{html.escape(n)}</h3><p>{html.escape(b)}</p></a>' for n,u,b in FEAT.get(key,[]))
    featblock=f'<div class="section-title"><span class="dot bg-{cluster}"></span><h2 style="margin:0">Featured</h2></div><div class="grid c3">{feat}</div>' if feat else ""
    # category chips
    cats=[]
    for x in items:
        c=x.get("category","") or ""
        if c and c not in cats: cats.append(c)
    catchips="".join(f'<button class="chipbtn" data-cat="{html.escape(c)}">{html.escape(c.title())}</button>' for c in cats) if len(cats)>1 else ""
    # A-Z for people/biz
    az=""
    if img_cards:
        letters=sorted({(x["name"][:1].upper() if x["name"][:1].isalpha() else "#") for x in items})
        az='<div class="az">'+"".join(f'<button class="chipbtn" data-cat="{L}">{L}</button>' for L in letters)+'</div>'
    # cards
    cardhtml=[]
    for x in items:
        nm=x["name"]; L=nm[:1].upper() if nm[:1].isalpha() else "#"; cat=x.get("category","") or ""
        blurb=(x.get("blurb") or "")[:96]
        if img_cards:
            media=f'<div class="card-media bg-{cluster}" data-wiki="{html.escape(nm)}">{_initials(nm)}</div>'
            cls="card fcard pcard"
        elif key=="books":
            media=f'<div class="card-media bg-{cluster}" data-book="{html.escape(nm)}">{sym}</div>'
            cls="card fcard bookcard"
        else:
            media=f'<div class="card-media bg-{cluster}">{sym}</div>'
            cls="card fcard"
        cardhtml.append(f'<a class="{cls}" href="{base}{x["slug"]}/" data-name="{html.escape(nm.lower())}" data-cat="{html.escape(cat)}" data-letter="{L}">'
                        f'{media}<span class="chip {cluster}">{chip}</span><h3>{html.escape(nm)}</h3><p>{html.escape(blurb)}</p></a>')
    grid_cls="grid c4" if (img_cards or key=="books") else "grid c3"
    filterbar=(f'<div class="filterbar">'
               f'<input class="filter-input" data-filter-input placeholder="Search {len(items)} {html.escape(title.lower())}…">'
               f'{az}'
               + (f'<div class="chips">{catchips}</div>' if catchips else "")
               + f'<div class="count-note"><span data-filter-count>{len(items)}</span> of {len(items)} shown</div></div>')
    rec = ' &nbsp; <a href="/recommend/" style="font-family:var(--f-mono);font-size:.85rem">Get recommendations &rarr;</a>' if img_cards else ""
    desc=f"Browse all {len(items)} {title.lower()} in Navigator — open, no login, searchable, cross-linked. {SITE['tagline']}"
    doc=head(title,desc,base)+nav()+head_band(cluster,f"{title} &middot; {len(items)}",title,f'<a href="/">Home</a> &rsaquo; {title}')
    doc+=(f'<main class="wrap"><p class="lead" style="color:var(--ink-soft);max-width:64ch">All {len(items)} {title.lower()} — searchable and filterable, every page open and free.{rec}</p>'
          f'{featblock}<div data-filter-root>{filterbar}<div class="{grid_cls}">{"".join(cardhtml)}</div></div>{newsletter_cta()}</main>')+footer()
    write(base,doc,"0.8")

def render_ai():
    # /ai/ index
    d=head("Artificial Intelligence","Navigator's AI hub — two arms: AI for You (AI that works for your life, work, and balance) and AI + You (agents and agentic AI working alongside you for bigger, faster, deeper outcomes).","/ai/","website")+nav()
    d+=head_band("news","Artificial Intelligence","Artificial Intelligence",'<a href="/">Home</a> &rsaquo; AI')
    d+=('<main class="wrap">'
        '<p class="lead" style="color:var(--ink-soft);max-width:66ch">AI is the through-line of this decade. Navigator approaches it in two complementary ways &mdash; one where AI works <em>for</em> you, and one where you and AI work <em>together</em>.</p>'
        '<div class="two-arms" style="margin-top:18px">'
        '<a class="card" href="/ai/ai-for-you/"><div class="card-media bg-news">&#10022;</div><span class="chip news">Arm 1</span><h3>AI for You</h3>'
        '<p>AI that quietly does the work &mdash; for businesses, leaders, teams, students, and families. Reclaim time, sharpen focus, and raise both the quality and quantity of what you produce, aimed squarely at your goals.</p></a>'
        '<a class="card" href="/ai/ai-plus-you/"><div class="card-media bg-strat">&#9670;</div><span class="chip strat">Arm 2</span><h3>AI + You</h3>'
        '<p>You and AI as a team &mdash; agents, projects, and agentic workflows that hold more context, move faster, and take on complex research and output you couldn\'t do alone.</p></a>'
        '</div>'
        '<div class="band" style="margin-top:26px"><h2 style="margin-top:0">Why two arms?</h2>'
        '<p class="big">Most people ask one question about AI: &ldquo;will it replace me?&rdquo; Navigator asks two better ones: <strong>what can AI do for you</strong>, and <strong>what can you do with AI</strong> that neither could alone. The first is about leverage and life. The second is about capability and craft. Together they cover the whole opportunity.</p></div>'
        '<div class="section-title"><span class="dot bg-strat"></span><h2 style="margin:0">Go deeper</h2></div>'
        '<div class="grid c3">'
        '<a class="card" href="/mental-models/the-bitter-lesson/"><span class="chip strat">Mental Model</span><h3>The Bitter Lesson</h3><p>Why AI keeps getting more capable &mdash; and what that means for you.</p></a>'
        '<a class="card" href="/guides/keep-judgment-when-model-is-confident/"><span class="chip learn">Guide</span><h3>Keep judgment when the model is confident</h3><p>Stay the human in the loop.</p></a>'
        '<a class="card" href="/frameworks/vertical-ai-agents/"><span class="chip strat">Framework</span><h3>Vertical AI Agents</h3><p>Agents that do the work, not just assist.</p></a>'
        '</div>'
        + newsletter_cta() + '</main>')+footer()
    write("/ai/",d,"0.9")

    arms=[
     ("ai-for-you","AI for You","news","&#10022;",
      "AI that works <em>for</em> you &mdash; reclaiming time and attention so businesses, leaders, teams, students, and families can focus on what matters.",
      [("The idea","<p>The first arm of Navigator's AI thinking is simple: let AI carry the load it's good at, so you get your time, attention, and energy back for the things only you can do. Not AI as a gadget &mdash; AI as quiet leverage across your work and your life.</p>"),
       ("For businesses &amp; leaders","<p>Automate the repetitive, draft the first version, summarise the firehose, and surface the signal in your data &mdash; so leadership time goes to judgment, strategy, and people. The goal isn't more busywork done faster; it's raising the <strong>quality</strong> of decisions while increasing the <strong>quantity</strong> of good output.</p>"),
       ("For students &amp; learning","<p>A patient tutor that meets you where you are: explains a hard concept five ways, quizzes you, and adapts to your pace &mdash; used so it deepens understanding instead of outsourcing it. (Pair with our guide on keeping your own judgment.)</p>"),
       ("For families &amp; life balance","<p>Plan, organise, and offload the logistics that eat evenings and weekends, so more of your attention goes to the people and goals that actually matter. Quality <em>and</em> quantity of life, not just work.</p>"),
       ("The Navigator take","<p class=\"count-note\">This page is being expanded into a deep, practical playbook &mdash; specific workflows, prompts, and setups for each audience. What you see now is the frame; the depth is coming.</p>")]),
     ("ai-plus-you","AI + You","strat","&#9670;",
      "You and AI as a team &mdash; agents, projects, and agentic workflows that hold more context, move faster, and tackle complex research and output together.",
      [("The idea","<p>The second arm is collaboration, not delegation. You bring judgment, taste, and intent; AI brings breadth, speed, and tirelessness. Working together &mdash; through agents, structured projects, and agentic workflows &mdash; you can hold a larger context and reach outcomes neither of you could alone.</p>"),
       ("Agents &amp; agentic workflows","<p>Move beyond one-shot prompts to systems that plan, use tools, check their own work, and carry a task across many steps &mdash; with you steering at the key decision points. The human sets direction and guards the checkpoints; the agent does the legwork.</p>"),
       ("Projects &amp; larger context","<p>Structure work as ongoing projects where context accumulates &mdash; documents, data, prior decisions &mdash; so the collaboration gets smarter over time instead of starting cold each session.</p>"),
       ("Complex research &amp; output","<p>Cross-reference dozens of sources, synthesise, model scenarios, and produce first-draft deliverables at a scale that changes what a single person (or small team) can take on &mdash; with you validating the result.</p>"),
       ("The Navigator take","<p class=\"count-note\">This page is being expanded into a deep guide to working <em>with</em> AI &mdash; concrete agent setups, project structures, and research workflows. The frame is here; the depth is coming.</p>")]),
    ]
    for slug,title,cl,sym,lead,secs in arms:
        body="".join(f"<h2>{h}</h2>{c}" for h,c in secs)
        dd=head(title,re.sub('<[^>]+>','',lead),f"/ai/{slug}/","article")+nav()
        dd+=head_band(cl,"Artificial Intelligence",title,'<a href="/">Home</a> &rsaquo; <a href="/ai/">AI</a>')
        dd+=(f'<main class="wrap"><div class="read"><p class="thesis">{lead}</p><article class="doc">{body}'
             f'<div class="footer-links"><a href="/ai/">Back to AI</a><a href="/tools/">Tools</a><a href="/newsletter/">Newsletter</a></div></article>'
             f'{newsletter_cta()}</div></main>')+footer()
        write(f"/ai/{slug}/",dd,"0.7")

def render_all_content():
    searchidx=[]
    for key,base,cluster,chip,gf,sym in TYPES:
        p=os.path.join(ROOT,"data",key+".json")
        if not os.path.exists(p): continue
        items=json.load(open(p))
        if key!="tools":
            render_full_index(key,base,cluster,chip,gf,sym,items)  # tools keeps its custom hub
        bycat={}
        for x in items: bycat.setdefault(x.get("category","") or "",[]).append(x)
        skip=SKIP.get(key,set())
        for x in items:
            searchidx.append({"t":x["name"],"u":base+x["slug"]+"/","k":TITLE[key]})
            if x["slug"] in skip: continue
            sibs=[y for y in bycat.get(x.get("category","") or "",items) if y["slug"]!=x["slug"]][:6]
            if len(sibs)<3: sibs=[y for y in items if y["slug"]!=x["slug"]][:6]
            render_item_page(x,key,base,cluster,chip,gf,sibs)
    json.dump(searchidx,open(os.path.join(OUT,"search-index.json"),"w"),ensure_ascii=False)
    # recommend + search pages (linked from the menu — must not 404)
    simple("/recommend/","What should I study?","Tell us your role and goal and get people, companies, tools, and books to study — no login.",
      '<p class="thesis">Not sure where to start? Pick your goal and follow the trail.</p>'
      '<div class="grid c2">'
      '<a class="card" href="/paths/ai-native-operator/"><span class="chip strat">Path</span><h3>Operate in the AI era</h3><p>The AI-Native Operator path chains the essential models, tools, and reads.</p></a>'
      '<a class="card" href="/tools/"><span class="chip tools">Tools</span><h3>Make a real decision now</h3><p>Run the Decision Matrix or Moat Analyzer on something you\'re actually deciding.</p></a>'
      '<a class="card" href="/mental-models/"><span class="chip strat">Think</span><h3>Sharpen your judgment</h3><p>Browse 1,000+ mental models by category.</p></a>'
      '<a class="card" href="/businesses/"><span class="chip biz">Build</span><h3>Study how companies win</h3><p>Company breakdowns across every sector.</p></a>'
      '</div>',("strat","Recommend"))
    simple("/search/","Search","Search Navigator — people, companies, models, tools, books, and more.",
      '<p class="thesis">Type to filter across everything in Navigator.</p>'
      '<input id="q" placeholder="Search people, companies, models, tools…" style="font-family:var(--f-ui);font-size:1.1rem;padding:.7em 1em;border:2px solid var(--line);border-radius:12px;width:100%;background:#fff">'
      '<div id="res" style="margin-top:16px"></div>'
      '<script>fetch("/search-index.json").then(r=>r.json()).then(idx=>{const q=document.getElementById("q"),res=document.getElementById("res");'
      'function render(v){v=v.trim().toLowerCase();if(v.length<2){res.innerHTML="";return;}'
      'const hits=idx.filter(x=>x.t.toLowerCase().includes(v)).slice(0,60);'
      'res.innerHTML=hits.map(x=>`<a class="card" style="margin:8px 0" href="${x.u}"><span class="chip strat">${x.k}</span><h3 style="margin:.2em 0 0">${x.t}</h3></a>`).join("")||"<p>No matches.</p>";}'
      'q.addEventListener("input",e=>render(e.target.value));});</script>',("strat","Search"))

if __name__=="__main__": main()
