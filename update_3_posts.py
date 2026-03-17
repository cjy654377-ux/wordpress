#!/usr/bin/env python3
"""Update 3 posts with quality fixes — March 17, 2026."""
import requests, re, sys, os

SITE = "https://rhythmicaleskimo.com"
REST = f"{SITE}/wp-json/wp/v2"
BASE = os.path.dirname(os.path.abspath(__file__))

# Login
s = requests.Session()
s.cookies.set("wordpress_test_cookie", "WP+Cookie+check")
s.post(f"{SITE}/wp-login.php", data={
    "log": "cjy654377@gmail.com",
    "pwd": "Dkflekd1!!",
    "wp-submit": "Log In",
    "redirect_to": "/wp-admin/",
    "testcookie": "1"
}, allow_redirects=True)

page = s.get(f"{SITE}/wp-admin/post-new.php").text
m = re.search(r'"nonce":"([a-f0-9]+)"', page)
if not m:
    m = re.search(r'_wpnonce=([a-f0-9]+)', page)
if not m:
    print("ERROR: nonce not found"); sys.exit(1)
h = {"X-WP-Nonce": m.group(1)}

with open(os.path.join(BASE, "template.html")) as f:
    template = f.read()

updates = [
    {"post_id": 1353, "file": "article_convenience_store_food.html", "name": "Convenience Store Food"},
    {"post_id": 1355, "file": "article_illit_press_start.html", "name": "ILLIT Press Start"},
    {"post_id": 1349, "file": "article_spicule_skincare.html", "name": "Spicule Skincare"},
]

for u in updates:
    with open(os.path.join(BASE, u["file"])) as f:
        content = f.read()
    html = template.replace("{CONTENT}", content)
    r = s.post(f"{REST}/posts/{u['post_id']}", headers=h, json={"content": html})
    if r.status_code == 200:
        print(f"  ✅ Updated: {u['name']} (ID: {u['post_id']})")
    else:
        print(f"  ❌ Failed: {u['name']} — {r.status_code}: {r.text[:200]}")

print("\nDone!")
