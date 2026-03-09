#!/usr/bin/env python3
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import login, get_or_create_category, get_or_create_tags
import json, requests

base = os.path.dirname(os.path.abspath(__file__))
SITE = "https://rhythmicaleskimo.com"
REST = f"{SITE}/wp-json/wp/v2"

with open(os.path.join(base, "template.html")) as f:
    template = f.read()
with open(os.path.join(base, "posts_kbeauty7.json")) as f:
    posts = json.load(f)

def publish_with_excerpt(s, h, post, template):
    cat_id = get_or_create_category(s, h, post["category"], post["category_slug"])
    html = template.replace("{CONTENT}", post["body"])
    data = {
        "title": post["title"],
        "content": html,
        "status": "publish",
        "categories": [cat_id],
    }
    if post.get("excerpt"):
        data["excerpt"] = post["excerpt"]
    r = s.post(f"{REST}/posts", headers=h, json=data)
    if r.status_code == 201:
        pid = r.json()["id"]
        url = r.json()["link"]
        tags = get_or_create_tags(s, h, post.get("tags", []))
        if tags:
            s.post(f"{REST}/posts/{pid}", headers=h, json={"tags": tags})
        print(f"  ✅ [{post['category']}] {post['title'][:60]}... → {url}")
        return True
    else:
        print(f"  ❌ {r.status_code}: {r.text[:200]}")
        return False

s, h = login()
ok = sum(publish_with_excerpt(s, h, p, template) for p in posts)
print(f"\nDone: {ok}/{len(posts)} published")
