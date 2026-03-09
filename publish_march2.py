#!/usr/bin/env python3
"""Publish 2 Iran war + Oil crisis articles with featured images to WordPress."""
import requests, re, json, os, sys

SITE = "https://rhythmicaleskimo.com"
USER = "cjy654377@gmail.com"
PASS = "Dkflekd1!!"
BASE = os.path.dirname(os.path.abspath(__file__))

# Login
s = requests.Session()
s.cookies.set("wordpress_test_cookie", "WP+Cookie+check")
s.post(f"{SITE}/wp-login.php", data={
    "log": USER, "pwd": PASS, "wp-submit": "Log In",
    "redirect_to": f"{SITE}/wp-admin/", "testcookie": "1"
}, allow_redirects=True)
nonce = re.search(r'"nonce":"([a-f0-9]+)"', s.get(f"{SITE}/wp-admin/post-new.php").text)
if not nonce:
    print("ERROR: nonce not found"); sys.exit(1)
H = {"X-WP-Nonce": nonce.group(1)}
print(f"Logged in. Nonce: {nonce.group(1)[:8]}...")

def upload_img(filename):
    path = os.path.join(BASE, filename)
    with open(path, "rb") as f:
        data = f.read()
    slug = filename.replace(".png", "")
    r = s.post(f"{SITE}/wp-json/wp/v2/media",
        headers={**H, "Content-Disposition": f"attachment; filename={slug}.png", "Content-Type": "image/png"},
        data=data)
    if r.status_code == 201:
        mid = r.json()["id"]
        print(f"  IMG {filename} -> media ID {mid}")
        return mid
    print(f"  IMG FAIL {filename}: {r.status_code} {r.text[:100]}")
    return 0

def get_or_create_cat(name, slug):
    cats = s.get(f"{SITE}/wp-json/wp/v2/categories?search={name}", headers=H).json()
    if cats and isinstance(cats, list) and len(cats) > 0:
        return cats[0]["id"]
    r = s.post(f"{SITE}/wp-json/wp/v2/categories", headers=H, json={"name": name, "slug": slug})
    return r.json()["id"] if r.status_code == 201 else 1

def make_tags(names):
    ids = []
    for t in names:
        r = s.post(f"{SITE}/wp-json/wp/v2/tags", headers=H, json={"name": t})
        if r.status_code == 201:
            ids.append(r.json()["id"])
        elif r.status_code == 400:
            tid = r.json().get("data", {}).get("term_id")
            if tid: ids.append(tid)
    return ids

# Load metadata
with open(os.path.join(BASE, "news_march2.json")) as f:
    meta = json.load(f)

# Article HTML files
html_files = ["article_iran_strikes.html", "article_oil_crisis.html"]

cat_id = get_or_create_cat("World News", "world-news")
print(f"Category: World News (ID: {cat_id})")

for i, (m, hf) in enumerate(zip(meta, html_files)):
    print(f"\n{'='*50}")
    print(f"[{i+1}/2] {m['title'][:60]}...")

    # Upload featured image
    img_id = upload_img(m["img"])

    # Read article HTML
    with open(os.path.join(BASE, hf)) as f:
        content = f.read()

    # Publish
    data = {
        "title": m["title"],
        "content": content,
        "excerpt": m["excerpt"],
        "status": "publish",
        "categories": [cat_id],
        "featured_media": img_id,
    }
    r = s.post(f"{SITE}/wp-json/wp/v2/posts", headers=H, json=data)
    if r.status_code == 201:
        pid = r.json()["id"]
        url = r.json()["link"]
        print(f"  Published! ID={pid}")
        print(f"  URL: {url}")

        # Set tags
        tag_ids = make_tags(m["tags"])
        if tag_ids:
            s.post(f"{SITE}/wp-json/wp/v2/posts/{pid}", headers=H, json={"tags": tag_ids})
            print(f"  Tags: {len(tag_ids)} set")
    else:
        print(f"  FAIL: {r.status_code} {r.text[:200]}")

print(f"\n{'='*50}")
print("Done! Visit: https://rhythmicaleskimo.com")
