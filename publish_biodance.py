#!/usr/bin/env python3
"""Publish Biodance Bio-Collagen Mask review article."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import login, get_or_create_category, get_or_create_tags, SITE, REST

base = os.path.dirname(os.path.abspath(__file__))

# Read template and article
with open(os.path.join(base, "template.html")) as f:
    template = f.read()
with open(os.path.join(base, "article_biodance.html")) as f:
    body = f.read()

html = template.replace("{CONTENT}", body)

s, h = login()
print("Logged in successfully.")

# Get K-Beauty category
cat_id = get_or_create_category(s, h, "K-Beauty", "k-beauty")
print(f"Category K-Beauty: ID {cat_id}")

# Create post
post_data = {
    "title": "Biodance Bio-Collagen Mask Review: Why This $3 Sheet Mask Broke TikTok in 2026",
    "content": html,
    "status": "publish",
    "categories": [cat_id],
    "excerpt": "The Biodance Bio-Collagen Real Deep Mask became TikTok's most viral K-beauty product in 2026. We break down the ingredients, real results, dermatologist opinions, and where to buy it for the best price."
}

r = s.post(f"{REST}/posts", headers=h, json=post_data)
if r.status_code != 201:
    print(f"ERROR creating post: {r.status_code} — {r.text[:300]}")
    sys.exit(1)

post_id = r.json()["id"]
post_url = r.json()["link"]
print(f"Post created: ID {post_id} → {post_url}")

# Add tags
tags = get_or_create_tags(s, h, [
    "Biodance", "K-Beauty", "Sheet Mask", "Collagen Mask", "TikTok Beauty",
    "Korean Skincare", "Hydrogel Mask", "Glass Skin", "Product Review"
])
if tags:
    s.post(f"{REST}/posts/{post_id}", headers=h, json={"tags": tags})
    print(f"Tags added: {len(tags)} tags")

# Upload featured image
img_path = os.path.join(base, "featured_biodance.png")
if os.path.exists(img_path):
    with open(img_path, "rb") as f:
        img_data = f.read()

    upload_headers = dict(h)
    upload_headers["Content-Disposition"] = "attachment; filename=featured-biodance-bio-collagen-mask-review.png"
    upload_headers["Content-Type"] = "image/png"

    r_img = s.post(f"{REST}/media", headers=upload_headers, data=img_data)
    if r_img.status_code == 201:
        media_id = r_img.json()["id"]
        # Set as featured image
        s.post(f"{REST}/posts/{post_id}", headers=h, json={"featured_media": media_id})
        print(f"Featured image uploaded: media ID {media_id}")
    else:
        print(f"Image upload failed: {r_img.status_code} — {r_img.text[:200]}")
else:
    print("WARNING: featured_biodance.png not found, skipping image upload")

print(f"\n=== PUBLISHED ===")
print(f"URL: {post_url}")
print(f"Post ID: {post_id}")
