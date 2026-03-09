#!/usr/bin/env python3
"""Apply affiliate links using engine.py login method."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import login
from insert_affiliate_links import TARGET_SLUGS, PRODUCT_DB, insert_links, already_has_affiliate
import requests, time

SITE = "https://rhythmicaleskimo.com"
REST = f"{SITE}/wp-json/wp/v2"

s, h = login()
print("Login OK")

# Fetch all posts
all_posts = []
page = 1
while True:
    r = s.get(f"{REST}/posts?per_page=100&page={page}", headers=h)
    if r.status_code != 200:
        break
    batch = r.json()
    if not batch:
        break
    all_posts.extend(batch)
    page += 1

print(f"Fetched {len(all_posts)} posts")

updated = 0
for post in all_posts:
    slug = post["slug"]
    if slug not in TARGET_SLUGS:
        continue
    
    pid = post["id"]
    title = post["title"]["rendered"]
    content = post["content"]["rendered"]
    
    if already_has_affiliate(content):
        print(f"  SKIP (already has links): {title[:55]}...")
        continue
    
    new_content, count = insert_links(content)
    if count == 0:
        print(f"  SKIP (no matches): {title[:55]}...")
        continue
    
    r = s.post(f"{REST}/posts/{pid}", headers=h, json={"content": new_content})
    if r.status_code == 200:
        print(f"  UPDATED: {title[:55]}... ({count} links)")
        updated += 1
    else:
        print(f"  FAILED ({r.status_code}): {title[:55]}...")
    time.sleep(0.3)

print(f"\n=== Done: {updated} posts updated ===")
