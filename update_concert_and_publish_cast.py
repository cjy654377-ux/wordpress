#!/usr/bin/env python3
"""Update K-pop concert guide + Publish Tangerines cast guide."""
import os, sys, json
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import login, REST, get_or_create_category, get_or_create_tags, ping_google

BASE = os.path.dirname(os.path.abspath(__file__))

def update_concert(s, h):
    """Update existing K-pop concert guide (ID 78)."""
    with open(os.path.join(BASE, "article_kpop_concert_v2.html"), encoding="utf-8") as f:
        content = f.read()
    r = s.post(f"{REST}/posts/78", headers=h, json={
        "content": content,
        "excerpt": "The complete survival guide to K-Pop concerts in Korea: how to buy tickets, what to bring, fan chant etiquette, venue guides, and essential tips for international fans."
    })
    if r.status_code == 200:
        print(f"OK Concert guide updated -> {r.json()['link']}")
    else:
        print(f"FAIL Concert: {r.status_code}")

def publish_cast(s, h):
    """Publish new Tangerines cast guide."""
    with open(os.path.join(BASE, "article_tangerines_cast.html"), encoding="utf-8") as f:
        content = f.read()

    cat_id = get_or_create_category(s, h, "K-Drama Guide", "k-drama-guide")
    tag_ids = get_or_create_tags(s, h, [
        "When Life Gives You Tangerines", "IU", "Park Bo-gum",
        "Netflix", "K-Drama", "K-Drama Cast Guide"
    ])

    data = {
        "title": "'When Life Gives You Tangerines' Cast Guide: IU, Park Bo-gum & the Real Married Couple (2025)",
        "content": content,
        "excerpt": "Complete cast guide for Netflix's highest-rated K-drama ever. Meet IU, Park Bo-gum, and the real-life married couple who play the older leads — plus awards, behind-the-scenes facts, and where to watch.",
        "status": "publish",
        "categories": [cat_id],
        "tags": tag_ids,
    }

    r = s.post(f"{REST}/posts", headers=h, json=data)
    if r.status_code == 201:
        url = r.json()["link"]
        pid = r.json()["id"]
        print(f"OK Cast guide published -> {url} (ID: {pid})")
        return url
    else:
        print(f"FAIL Cast: {r.status_code}: {r.text[:200]}")
        return None

def main():
    s, h = login()
    update_concert(s, h)
    cast_url = publish_cast(s, h)
    ping_google()
    print("Google sitemap pinged")

if __name__ == "__main__":
    main()
