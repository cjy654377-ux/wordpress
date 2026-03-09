#!/usr/bin/env python3
"""Publish the comprehensive Iran war aftermath article."""
import requests, re, os, sys

SITE = "https://rhythmicaleskimo.com"
USER = "cjy654377@gmail.com"
PASS = "Dkflekd1!!"
BASE = os.path.dirname(os.path.abspath(__file__))

s = requests.Session()
s.cookies.set("wordpress_test_cookie", "WP+Cookie+check")
s.post(f"{SITE}/wp-login.php", data={
    "log": USER, "pwd": PASS, "wp-submit": "Log In",
    "redirect_to": f"{SITE}/wp-admin/", "testcookie": "1"
}, allow_redirects=True)
nonce = re.search(r'"nonce":"([a-f0-9]+)"', s.get(f"{SITE}/wp-admin/post-new.php").text)
if not nonce:
    print("ERROR: nonce not found"); sys.exit(1)
H = {"X-WP-Nonce": nonce.group(1)}
print(f"Logged in.")

# Upload image
with open(os.path.join(BASE, "featured_iran_aftermath.png"), "rb") as f:
    img_data = f.read()
r = s.post(f"{SITE}/wp-json/wp/v2/media",
    headers={**H, "Content-Disposition": "attachment; filename=featured-iran-aftermath.png", "Content-Type": "image/png"},
    data=img_data)
img_id = r.json()["id"] if r.status_code == 201 else 0
print(f"Image uploaded: ID={img_id}")

# Get/create category
cats = s.get(f"{SITE}/wp-json/wp/v2/categories?search=World+News", headers=H).json()
cat_id = cats[0]["id"] if cats and isinstance(cats, list) else 149

# Read article
with open(os.path.join(BASE, "article_iran_aftermath.html")) as f:
    content = f.read()

# Publish
data = {
    "title": "12 Ways the Iran War Is Reshaping the World Right Now: Oil Shocks, Cyber War, Nuclear Fears, and the Largest Refugee Crisis in History",
    "content": content,
    "excerpt": "The US-Israel military operation against Iran is triggering cascading global consequences — from oil surging 8% and 3,400 flights cancelled, to cyber warfare, nuclear proliferation fears, currency collapses, and what could become the largest refugee crisis in history. A comprehensive analysis of 12 secondary effects reshaping the world.",
    "status": "publish",
    "categories": [cat_id],
    "featured_media": img_id,
}
r = s.post(f"{SITE}/wp-json/wp/v2/posts", headers=H, json=data)
if r.status_code == 201:
    pid = r.json()["id"]
    url = r.json()["link"]
    print(f"Published! ID={pid}")
    print(f"URL: {url}")

    # Tags
    tag_names = ["Iran War", "Global Impact", "Oil Crisis", "Cyber Warfare", "Nuclear Proliferation",
                 "Refugee Crisis", "Strait of Hormuz", "Middle East", "World News", "Economic Impact",
                 "Supply Chain", "Geopolitics"]
    tag_ids = []
    for t in tag_names:
        tr = s.post(f"{SITE}/wp-json/wp/v2/tags", headers=H, json={"name": t})
        if tr.status_code == 201:
            tag_ids.append(tr.json()["id"])
        elif tr.status_code == 400:
            tid = tr.json().get("data", {}).get("term_id")
            if tid: tag_ids.append(tid)
    if tag_ids:
        s.post(f"{SITE}/wp-json/wp/v2/posts/{pid}", headers=H, json={"tags": tag_ids})
        print(f"Tags: {len(tag_ids)} set")
else:
    print(f"FAIL: {r.status_code} {r.text[:200]}")
