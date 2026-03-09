#!/usr/bin/env python3
"""Publish BTS ARIRANG album analysis article with featured image."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import login, get_or_create_category, get_or_create_tags, SITE, REST

BASE = os.path.dirname(os.path.abspath(__file__))

# Read article HTML
with open(os.path.join(BASE, "article_bts_arirang_album.html")) as f:
    body = f.read()

# Read template
with open(os.path.join(BASE, "template.html")) as f:
    template = f.read()

html = template.replace("{CONTENT}", body)

s, h = login()

# Create category
cat_id = get_or_create_category(s, h, "K-Pop", "k-pop")

# Upload featured image
img_path = os.path.join(BASE, "featured_bts_arirang_album.png")
with open(img_path, "rb") as f:
    img_data = f.read()

media_headers = dict(h)
media_headers["Content-Disposition"] = "attachment; filename=featured_bts_arirang_album.png"
media_headers["Content-Type"] = "image/png"

media_resp = s.post(f"{REST}/media", headers=media_headers, data=img_data)
if media_resp.status_code == 201:
    featured_id = media_resp.json()["id"]
    print(f"✅ Featured image uploaded (ID: {featured_id})")
else:
    print(f"⚠️ Image upload failed ({media_resp.status_code}), publishing without image")
    featured_id = None

# Publish post
post_data = {
    "title": "BTS ARIRANG Album: The Cultural Meaning Behind Every Song — Han, Heung, and 600 Years of Korean Soul",
    "content": html,
    "status": "publish",
    "categories": [cat_id],
    "excerpt": "BTS names their comeback album after Korea's most sacred folk song. We break down the 600-year cultural weight behind ARIRANG, the han-to-heung emotional arc across all 14 tracks, and why the Gwanghwamun concert location is deeply symbolic. Includes complete tracklist analysis, military service timeline, and how to watch the Netflix live concert.",
}

if featured_id:
    post_data["featured_media"] = featured_id

r = s.post(f"{REST}/posts", headers=h, json=post_data)
if r.status_code == 201:
    post_id = r.json()["id"]
    url = r.json()["link"]

    # Add tags
    tags = get_or_create_tags(s, h, [
        "BTS", "BTS Arirang", "K-Pop", "BTS Album", "BTS Comeback 2026",
        "Korean Culture", "Arirang", "BTS SWIM", "Netflix BTS Concert",
        "BTS World Tour 2026", "Han and Heung", "Korean Music"
    ])
    if tags:
        s.post(f"{REST}/posts/{post_id}", headers=h, json={"tags": tags})

    print(f"✅ Published: {url}")
else:
    print(f"❌ Failed ({r.status_code}): {r.text[:300]}")
