#!/usr/bin/env python3
# Extract all rosters -> data/*.json  (slug, name, category, blurb, author)
import re, json, os
OUT="/mnt/user-data/outputs"; D="data"
def slug(s):
    s=re.sub(r'\(.*?\)','',s).split(' / ')[0].split(' — ')[0]
    s=re.sub(r'[^a-zA-Z0-9 -]','',s).strip().lower()
    s=re.sub(r'\s+','-',s); s=re.sub(r'-+','-',s).strip('-')
    return "-".join(s.split('-')[:6])
def uniq(items):
    seen={}
    for it in items:
        s=it["slug"]
        if s in seen: seen[s]+=1; it["slug"]=f"{s}-{seen[s]}"
        else: seen[s]=0
    return items
def parse_categorized(path):
    cats={}; cur=None
    for ln in open(path):
        s=ln.rstrip("\n")
        if s.startswith("## "): cur=s[3:].strip(); cats[cur]=[]
        elif cur and s.strip() and not s.startswith(("#","(","-","*",">","Note",'"',"All ","Duplicates","---")):
            nm=s.strip()
            if 1<=len(nm)<=60 and not nm.endswith(":"): cats[cur].append(nm)
    return cats

def dump(name, items): json.dump(uniq(items), open(f"{D}/{name}.json","w"), ensure_ascii=False, indent=0)

# people / businesses
def catrows(cats):
    rows=[]
    for c,names in cats.items():
        for n in names: rows.append({"slug":slug(n),"name":n,"category":c,"blurb":""})
    return rows
dump("people", catrows(parse_categorized(f"{OUT}/all-people-categorized.md")))
dump("businesses", catrows(parse_categorized(f"{OUT}/all-businesses-categorized.md")))

# mental models (name + blurb + category)
t=open(f"{D}/mm.txt").read(); cut=t.find("Frequently Asked Questions"); t=t[:cut] if cut>0 else t
cats=["BUSINESS & STRATEGY","COMPUTER SCIENCE & ALGORITHMS","ECONOMICS & MARKETS","FINANCE & INVESTING",
"GENERAL THINKING & META-MODELS","HIGH PERFORMANCE & LEARNING","MATHEMATICS & PROBABILITY","MILITARY & CONFLICT",
"NATURAL SCIENCES","PHILOSOPHY, LAW & POLITICS","PSYCHOLOGY & BEHAVIOR","SYSTEMS & COMPLEXITY"]
catpat="|".join(re.escape(c) for c in cats); parts=re.split(f"({catpat})",t); rows=[]
for i in range(1,len(parts)-1,2):
    cat=parts[i]; seg=parts[i+1].strip()
    if not seg: continue
    m=re.search(r'[a-z][A-Z]',seg); name=(seg[:m.start()+1] if m else seg[:50]).strip()
    name=re.sub(r'\(.*?\)','',name).split(' / ')[0].strip(); name=" ".join(name.split()[:6])
    blurb=seg[len(name):].strip()
    # strip leading author-ish Caps run then keep sentence
    blurb=re.sub(r'^[A-Z][A-Za-z.\'\-]+(?:\s*[/&]\s*[A-Z][A-Za-z.\'\-]+| [A-Z][A-Za-z.\'\-]+){0,4}','',blurb).strip()
    blurb=blurb[:300]
    if name: rows.append({"slug":slug(name),"name":name,"category":cat.title(),"blurb":blurb})
dump("mental-models", rows)

# books (title + author + blurb)
b=open(f"{D}/books.txt").read(); segs=re.split(r'Attachment\.png\s*¬',b)[1:]; rows=[]
for seg in segs:
    seg=seg.strip()
    m=re.search(r'[a-z][A-Z]',seg); title=(seg[:m.start()+1] if m else seg[:50]).strip()
    rest=seg[len(title):]
    ma=re.match(r'([A-Z][A-Za-z.\'\-]+(?: [A-Z][A-Za-z.\'\-]+){0,3})',rest); author=ma.group(1) if ma else ""
    blurb=rest[len(author):].strip()[:300]
    if 1<len(title)<70: rows.append({"slug":slug(title),"name":title,"author":author,"blurb":blurb,"category":"Book"})
dump("books", rows)

# business models (#N Name — desc *examples*)
rows=[]
for ln in open(f"{OUT}/03-business-models-index.md"):
    m=re.search(r'#\d+\s*(.+?)\*\*\s*(?:\*\(2026-native\)\*)?\s*—\s*(.+)',ln) or re.search(r'#\d+\s+([^—*]+)—\s*(.+)',ln)
    if m:
        nm=m.group(1).replace("**","").strip(" *★"); desc=re.sub(r'\*','',m.group(2)).strip()
        rows.append({"slug":slug(nm),"name":nm,"blurb":desc[:260],"category":"Business Model"})
dump("business-models", rows)

# frameworks / guides / quotes  (- **Name** — desc)
def bullets(path, cat):
    rows=[]
    for ln in open(path):
        m=re.match(r'- \*\*(.+?)\*\*\s*(?:—\s*(.+))?',ln)
        if m:
            nm=m.group(1).split("—")[0].split(":")[0].strip(); desc=(m.group(2) or "").strip()
            rows.append({"slug":slug(nm),"name":nm,"blurb":re.sub(r'\*','',desc)[:260],"category":cat})
    return rows
dump("frameworks", bullets(f"{OUT}/04-frameworks-index.md","Framework"))
dump("guides", bullets(f"{OUT}/12-guides-index.md","Guide"))
dump("quotes", bullets(f"{OUT}/14-quote-collections-index.md","Quote Collection"))

print("data files written:")
for f in sorted(os.listdir(D)):
    if f.endswith(".json"):
        n=len(json.load(open(f"{D}/{f}"))); print(f"  {n:5d}  {f}")
