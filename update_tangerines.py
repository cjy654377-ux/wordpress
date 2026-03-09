#!/usr/bin/env python3
"""Update 'When Life Gives You Tangerines' filming locations article."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import login, SITE, REST

NEW_TITLE = "8 Filming Locations of 'When Life Gives You Tangerines' in Jeju You Can Actually Visit (2026)"
NEW_EXCERPT = "Visit the exact beaches, villages, and markets where IU filmed 'When Life Gives You Tangerines' in Jeju. Includes addresses, bus routes, admission fees, and a 3-day itinerary."
SLUG_KEYWORD = "when-life-gives-you-tangerines"

BASE = os.path.dirname(os.path.abspath(__file__))

def find_post(s, h):
    """Find existing post by slug keyword."""
    r = s.get(f"{REST}/posts?search=tangerines+filming+locations&per_page=10", headers=h)
    if r.status_code == 200:
        for p in r.json():
            if "tangerines" in p["slug"] and "jeju" in p["slug"]:
                return p["id"], p["link"]
    return None, None

def main():
    s, h = login()
    post_id, old_url = find_post(s, h)
    if not post_id:
        print("ERROR: Could not find the tangerines article")
        sys.exit(1)
    print(f"Found post ID: {post_id} → {old_url}")

    with open(os.path.join(BASE, "article_tangerines_jeju_v2.html"), encoding="utf-8") as f:
        new_content = f.read()

    data = {
        "title": NEW_TITLE,
        "content": new_content,
        "excerpt": NEW_EXCERPT,
    }

    r = s.post(f"{REST}/posts/{post_id}", headers=h, json=data)
    if r.status_code == 200:
        url = r.json()["link"]
        print(f"OK Updated successfully -> {url}")
        print(f"   Title: {NEW_TITLE}")
        print(f"   Excerpt: {NEW_EXCERPT[:80]}...")
    else:
        print(f"FAIL Update failed: {r.status_code}")
        print(r.text[:300])

if __name__ == "__main__":
    main()
