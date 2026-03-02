#!/usr/bin/env python3
"""Publish March 3 batch 2 articles (5 Dramas + BTS Tour Guide)."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import login, REST, get_or_create_category, get_or_create_tags

BASE = os.path.dirname(os.path.abspath(__file__))

s, h = login()
print("Logged in.")

with open(os.path.join(BASE, "template.html")) as f:
    template = f.read()

def upload_img(filepath, fname):
    with open(filepath, "rb") as f:
        r = s.post(f"{REST}/media", headers={**h, "Content-Disposition": f"attachment; filename={fname}"},
                   data=f, params={"title": fname.replace(".png","").replace("_"," ")})
    if r.status_code == 201:
        mid = r.json()["id"]
        print(f"  Uploaded image: {fname} (ID={mid})")
        return mid
    print(f"  Image upload failed: {r.status_code}")
    return None

articles = [
    {
        "html_file": "article_5dramas_before_bod.html",
        "img_file": "featured_5dramas_bod.png",
        "title": "5 Must-Watch K-Dramas Before Boyfriend on Demand Premieres on Netflix",
        "category": "K-Drama",
        "category_slug": "k-drama",
        "excerpt": "Boyfriend on Demand drops on Netflix March 6, 2026 with Jisoo and 8 virtual boyfriends. Before you watch, binge these 5 essential K-Dramas that share its themes of virtual romance, webtoon worlds, and AI love stories.",
        "tags": ["Boyfriend on Demand", "Jisoo", "Netflix", "K-Drama", "Snowdrop", "W Two Worlds", "Reply 1988", "Korean Drama 2026"]
    },
    {
        "html_file": "article_bts_tour_guide.html",
        "img_file": "featured_bts_tour_guide.png",
        "title": "BTS Arirang World Tour 2026: Complete City-by-City Date Guide and How to Get Tickets",
        "category": "K-Pop",
        "category_slug": "k-pop",
        "excerpt": "The BTS Arirang World Tour spans 82 dates across 34 cities from April to October 2026. Complete guide with every tour date, venue, ticket prices by tier, and essential tips for international ARMY fans.",
        "tags": ["BTS", "BTS Arirang", "World Tour 2026", "ARMY", "Concert Tickets", "K-Pop", "BTS Tour Dates", "Weverse"]
    }
]

for art in articles:
    with open(os.path.join(BASE, art["html_file"])) as f:
        body = f.read()
    content = template.replace("{CONTENT}", body)
    cat_id = get_or_create_category(s, h, art["category"], art["category_slug"])
    tag_ids = get_or_create_tags(s, h, art["tags"])
    img_id = upload_img(os.path.join(BASE, art["img_file"]), art["img_file"])
    data = {
        "title": art["title"],
        "content": content,
        "status": "publish",
        "categories": [cat_id],
        "tags": tag_ids,
        "excerpt": art["excerpt"],
    }
    if img_id:
        data["featured_media"] = img_id
    r = s.post(f"{REST}/posts", headers=h, json=data)
    if r.status_code == 201:
        pid = r.json()["id"]
        url = r.json()["link"]
        print(f"  Published: {art['title'][:50]}... → ID={pid} {url}")
    else:
        print(f"  FAIL: {r.status_code} {r.text[:200]}")

print("\nDone!")
