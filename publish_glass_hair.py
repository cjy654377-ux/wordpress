#!/usr/bin/env python3
"""Publish Korean Glass Hair article with featured image."""
import os, sys, json, requests, re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import login, get_or_create_category, get_or_create_tags

SITE = "https://rhythmicaleskimo.com"
REST = f"{SITE}/wp-json/wp/v2"
base = os.path.dirname(os.path.abspath(__file__))

# Load template and article
with open(os.path.join(base, "template.html")) as f:
    template = f.read()
with open(os.path.join(base, "article_glass_hair.html")) as f:
    article_body = f.read()

# Login
s, h = login()
print("Logged in successfully.")

# Get K-Beauty category
cat_id = get_or_create_category(s, h, "K-Beauty", "k-beauty")
print(f"K-Beauty category ID: {cat_id}")

# Upload featured image
img_path = os.path.join(base, "featured_glass_hair.png")
with open(img_path, "rb") as f:
    img_data = f.read()

img_resp = s.post(
    f"{REST}/media",
    headers={**h, "Content-Disposition": "attachment; filename=featured-glass-hair-2026.png"},
    data=img_data,
    params={"alt_text": "Korean glass hair trend 2026 - mirror-shine hair routine", "title": "Korean Glass Hair Trend 2026"}
)
if img_resp.status_code == 201:
    media_id = img_resp.json()["id"]
    print(f"Featured image uploaded: ID {media_id}")
else:
    print(f"Image upload failed: {img_resp.status_code} {img_resp.text[:200]}")
    media_id = None

# Build HTML
html = template.replace("{CONTENT}", article_body)

# Create tags
tags = get_or_create_tags(s, h, [
    "glass hair", "Korean hair care", "K-beauty", "hair routine",
    "Korean beauty", "glass hair routine", "UNOVE", "Moremo",
    "Mise en Scene", "hair treatment", "Korean hair products"
])

# Publish post
post_data = {
    "title": "Korean Glass Hair Trend 2026: The 7-Step Routine Behind Korea's Shiniest Hair",
    "content": html,
    "status": "publish",
    "categories": [cat_id],
    "tags": tags,
    "excerpt": "Master the Korean glass hair trend with this complete 7-step routine guide. From scalp scaling to cool-air blow drying, discover the exact products and techniques Korean women use to achieve mirror-shine hair — plus honest price comparisons and salon vs. at-home tips."
}
if media_id:
    post_data["featured_media"] = media_id

r = s.post(f"{REST}/posts", headers=h, json=post_data)
if r.status_code == 201:
    post_id = r.json()["id"]
    post_url = r.json()["link"]
    print(f"\nPublished successfully!")
    print(f"Post ID: {post_id}")
    print(f"URL: {post_url}")
else:
    print(f"Publish failed: {r.status_code}")
    print(r.text[:500])
