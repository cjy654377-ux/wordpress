#!/usr/bin/env python3
"""Publish 5 March 3 articles with featured images."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import login, REST, get_or_create_category, get_or_create_tags

BASE = os.path.dirname(os.path.abspath(__file__))

def upload_img(s, h, filename):
    path = os.path.join(BASE, filename)
    with open(path, "rb") as f:
        data = f.read()
    r = s.post(f"{REST}/media",
        headers={**h, "Content-Disposition": f"attachment; filename={filename}",
                 "Content-Type": "image/png"},
        data=data)
    if r.status_code == 201:
        mid = r.json()["id"]
        print(f"  IMG {filename} -> ID {mid}")
        return mid
    print(f"  IMG FAIL: {r.status_code} {r.text[:100]}")
    return 0

s, h = login()
print("Logged in.")

with open(os.path.join(BASE, "template.html")) as f:
    template = f.read()
with open(os.path.join(BASE, "march3_data.json")) as f:
    articles = json.load(f)

for i, a in enumerate(articles):
    print(f"\n{'='*50}")
    print(f"[{i+1}/{len(articles)}] {a['title'][:60]}...")

    img_id = upload_img(s, h, a["img"])

    with open(os.path.join(BASE, a["html_file"])) as f:
        body = f.read()

    content = template.replace("{CONTENT}", body)
    cat_id = get_or_create_category(s, h, a["category"], a["category_slug"])
    tag_ids = get_or_create_tags(s, h, a["tags"])

    data = {
        "title": a["title"],
        "content": content,
        "excerpt": a["excerpt"],
        "status": "publish",
        "categories": [cat_id],
        "tags": tag_ids,
        "featured_media": img_id,
    }
    r = s.post(f"{REST}/posts", headers=h, json=data)
    if r.status_code == 201:
        pid = r.json()["id"]
        url = r.json()["link"]
        print(f"  Published! ID={pid}")
        print(f"  URL: {url}")
    else:
        print(f"  FAIL: {r.status_code} {r.text[:200]}")

print(f"\n{'='*50}")
print("Done! Visit: https://rhythmicaleskimo.com")
