#!/usr/bin/env python3
"""Publish 5 calculator posts with featured images to WordPress."""
import requests, re, json, os, sys

SITE = "https://rhythmicaleskimo.com"
REST = f"{SITE}/wp-json/wp/v2"
USER = "cjy654377@gmail.com"
PASS = "Tony2026!!"
BASE = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE, "calc_imgs")

def login():
    s = requests.Session()
    s.cookies.set("wordpress_test_cookie", "WP+Cookie+check")
    s.post(f"{SITE}/wp-login.php", data={
        "log": USER, "pwd": PASS, "wp-submit": "Log In",
        "redirect_to": "/wp-admin/", "testcookie": "1"
    }, allow_redirects=True)
    page = s.get(f"{SITE}/wp-admin/post-new.php").text
    m = re.search(r'"nonce":"([a-f0-9]+)"', page)
    if not m:
        print("ERROR: nonce not found"); sys.exit(1)
    return s, {"X-WP-Nonce": m.group(1)}

def get_or_create_category(s, h, name, slug):
    cats = s.get(f"{REST}/categories?search={name}", headers=h).json()
    if cats and isinstance(cats, list):
        for c in cats:
            if c["slug"] == slug:
                return c["id"]
    r = s.post(f"{REST}/categories", headers=h, json={"name": name, "slug": slug})
    return r.json()["id"] if r.status_code == 201 else 1

def upload_image(s, h, filepath, title):
    fname = os.path.basename(filepath)
    with open(filepath, "rb") as f:
        data = f.read()
    r = s.post(f"{REST}/media", headers={**h, "Content-Disposition": f'attachment; filename="{fname}"', "Content-Type": "image/png"}, data=data)
    if r.status_code == 201:
        mid = r.json()["id"]
        s.post(f"{REST}/media/{mid}", headers=h, json={"alt_text": title, "title": title})
        return mid
    print(f"  ❌ Image upload failed: {r.status_code}")
    return None

def get_or_create_tags(s, h, tag_names):
    ids = []
    for t in tag_names:
        ex = s.get(f"{REST}/tags?search={t}", headers=h).json()
        if ex and isinstance(ex, list) and len(ex) > 0:
            ids.append(ex[0]["id"])
        else:
            r = s.post(f"{REST}/tags", headers=h, json={"name": t})
            if r.status_code == 201:
                ids.append(r.json()["id"])
    return ids

s, h = login()
cat_id = get_or_create_category(s, h, "Web Utilities", "web-utilities")
print(f"Category: Web Utilities (ID={cat_id})")

with open(os.path.join(BASE, "template.html")) as f:
    template = f.read()

with open(os.path.join(BASE, "calc_data.json")) as f:
    posts = json.load(f)

for post in posts:
    # Upload featured image
    img_path = os.path.join(IMG_DIR, post["image"])
    media_id = upload_image(s, h, img_path, post["title"])

    # Build content
    html = template.replace("{CONTENT}", post["body"])

    data = {
        "title": post["title"],
        "content": html,
        "status": "publish",
        "categories": [cat_id],
        "featured_media": media_id or 0,
    }
    r = s.post(f"{REST}/posts", headers=h, json=data)
    if r.status_code == 201:
        pid = r.json()["id"]
        url = r.json()["link"]
        tags = get_or_create_tags(s, h, post.get("tags", []))
        if tags:
            s.post(f"{REST}/posts/{pid}", headers=h, json={"tags": tags})
        print(f"  ✅ {post['title'][:50]}... → {url}")
    else:
        print(f"  ❌ {r.status_code}: {r.text[:150]}")

print(f"\nDone: {len(posts)} calculator posts published")
