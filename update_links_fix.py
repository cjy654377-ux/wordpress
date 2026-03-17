#!/usr/bin/env python3
"""Update 3 posts with fixed internal links."""
import requests, re, sys, os

SITE = "https://rhythmicaleskimo.com"
REST = f"{SITE}/wp-json/wp/v2"
BASE = os.path.dirname(os.path.abspath(__file__))

s = requests.Session()
s.cookies.set("wordpress_test_cookie", "WP+Cookie+check")
s.post(f"{SITE}/wp-login.php", data={
    "log": "cjy654377@gmail.com", "pwd": "Dkflekd1!!",
    "wp-submit": "Log In", "redirect_to": "/wp-admin/", "testcookie": "1"
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
    {"post_id": 1347, "file": "article_blackpink_deadline.html", "name": "BLACKPINK"},
    {"post_id": 1351, "file": "article_still_shining.html", "name": "Still Shining"},
    {"post_id": 1355, "file": "article_illit_press_start.html", "name": "ILLIT"},
]

for u in updates:
    with open(os.path.join(BASE, u["file"])) as f:
        content = f.read()
    html = template.replace("{CONTENT}", content)
    r = s.post(f"{REST}/posts/{u['post_id']}", headers=h, json={"content": html})
    status = "OK" if r.status_code == 200 else f"FAIL {r.status_code}"
    print(f"  {status} — {u['name']} (ID: {u['post_id']})")
