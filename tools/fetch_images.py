#!/usr/bin/env python3
"""
Bake real images into the site so it needs NO runtime fetch.
Reads data/*.json, downloads people photos + company logos from Wikipedia and
book covers from OpenLibrary into site/assets/img/, named by a simple slug that
matches the site's JS. Re-runnable (skips files already present). Stdlib only.

Run locally:      python3 tools/fetch_images.py
Or via the included GitHub Action (no local tools needed).
"""
import json, os, re, time, urllib.request, urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
IMG  = os.path.join(ROOT, "site", "assets", "img")
UA   = "NavigatorImageBot/1.0 (reference site; contact via repo)"

def sslug(s):
    return re.sub(r'(^-|-$)', '', re.sub(r'[^a-z0-9]+', '-', s.lower()))

def _open(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=25)

def save(url, path):
    try:
        data = _open(url).read()
        if len(data) < 600:            # too small = placeholder/error
            return False
        with open(path, "wb") as f:
            f.write(data)
        return True
    except Exception:
        return False

def wiki_thumb(title, size=500):
    api = "https://en.wikipedia.org/w/api.php?" + urllib.parse.urlencode({
        "action": "query", "format": "json", "redirects": 1,
        "prop": "pageimages", "piprop": "thumbnail", "pithumbsize": size, "titles": title})
    try:
        d = json.load(_open(api))
        p = next(iter(d["query"]["pages"].values()))
        return p.get("thumbnail", {}).get("source")
    except Exception:
        return None

def ol_cover(title):
    api = "https://openlibrary.org/search.json?" + urllib.parse.urlencode(
        {"title": title, "limit": 1, "fields": "cover_i"})
    try:
        docs = json.load(_open(api)).get("docs", [])
        if docs and docs[0].get("cover_i"):
            return f'https://covers.openlibrary.org/b/id/{docs[0]["cover_i"]}-L.jpg'
    except Exception:
        pass
    return None

def load(name):
    p = os.path.join(DATA, name)
    return json.load(open(p)) if os.path.exists(p) else []

def run():
    os.makedirs(os.path.join(IMG, "wiki"), exist_ok=True)
    os.makedirs(os.path.join(IMG, "books"), exist_ok=True)
    got = miss = skip = 0

    # People -> photo ; Businesses -> logo/lead image (disambiguate query with "(company)")
    people   = [(x["name"], x["name"]) for x in load("people.json")]
    biz      = [(x["name"], x["name"] + " (company)") for x in load("businesses.json")]
    for name, query in people + biz:
        path = os.path.join(IMG, "wiki", sslug(name) + ".jpg")
        if os.path.exists(path):
            skip += 1; continue
        url = wiki_thumb(query) or wiki_thumb(name)
        if url and save(url, path): got += 1
        else: miss += 1
        time.sleep(0.08)

    # Books -> OpenLibrary cover
    for x in load("books.json"):
        path = os.path.join(IMG, "books", sslug(x["name"]) + ".jpg")
        if os.path.exists(path):
            skip += 1; continue
        url = ol_cover(x["name"])
        if url and save(url, path): got += 1
        else: miss += 1
        time.sleep(0.08)

    print(f"Done. downloaded={got}  missing={miss}  already-had={skip}")

if __name__ == "__main__":
    run()
