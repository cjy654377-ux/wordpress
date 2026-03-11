#!/usr/bin/env python3
"""Publish Iran War global markets analysis article."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import login, get_or_create_category, get_or_create_tags, SITE, REST

BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, "article_iran_war_markets.html")) as f:
    body = f.read()

with open(os.path.join(BASE, "template.html")) as f:
    template = f.read()

html = template.replace("{CONTENT}", body)

s, h = login()

cat_id = get_or_create_category(s, h, "World Financial Issues", "world-financial-issues")

# Upload featured image
img_path = os.path.join(BASE, "featured_iran_war_markets.png")
with open(img_path, "rb") as f:
    img_data = f.read()

media_headers = dict(h)
media_headers["Content-Disposition"] = "attachment; filename=featured_iran_war_markets.png"
media_headers["Content-Type"] = "image/png"

media_resp = s.post(f"{REST}/media", headers=media_headers, data=img_data)
featured_id = media_resp.json()["id"] if media_resp.status_code == 201 else None
if featured_id:
    print(f"✅ Featured image uploaded (ID: {featured_id})")
else:
    print(f"⚠️ Image upload failed ({media_resp.status_code})")

post_data = {
    "title": "How the 2026 Iran War Is Reshaping Global Markets: Oil, Gold, Stocks, and What Comes Next",
    "content": html,
    "status": "publish",
    "categories": [cat_id],
    "excerpt": "The Iran war sent Brent crude to $126, gold near $5,400, and stocks tumbling. With the Strait of Hormuz shut down, tariffs at 1930s levels, and the Fed holding rates, we break down what every investor needs to know — with data tables, scenario analysis, and actionable strategies.",
}

if featured_id:
    post_data["featured_media"] = featured_id

r = s.post(f"{REST}/posts", headers=h, json=post_data)
if r.status_code == 201:
    post_id = r.json()["id"]
    url = r.json()["link"]

    tags = get_or_create_tags(s, h, [
        "Iran War", "Oil Prices", "Gold", "Stock Market", "Federal Reserve",
        "Global Economy", "Recession", "Bitcoin", "Tariffs", "Investment",
        "Strait of Hormuz", "FOMC"
    ])
    if tags:
        s.post(f"{REST}/posts/{post_id}", headers=h, json={"tags": tags})

    print(f"✅ Published: {url}")
else:
    print(f"❌ Failed ({r.status_code}): {r.text[:300]}")
