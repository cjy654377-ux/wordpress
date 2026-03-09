#!/usr/bin/env python3
"""IndexNow key file upload via WP REST API"""
import requests, re, sys

SITE = "https://rhythmicaleskimo.com"
USER = "cjy654377@gmail.com"
PASS = "Tony2026!!"
KEY = "3ccd6adccb62a948dd2e5d80ca8d3c5a"

s = requests.Session()
s.cookies.set("wordpress_test_cookie", "WP+Cookie+check")
s.post(f"{SITE}/wp-login.php", data={
    "log": USER, "pwd": PASS, "wp-submit": "Log In",
    "redirect_to": "/wp-admin/", "testcookie": "1"
}, allow_redirects=True)
page = s.get(f"{SITE}/wp-admin/post-new.php").text
m = re.search(r'"nonce":"([a-f0-9]+)"', page)
nonce = m.group(1)
h = {"X-WP-Nonce": nonce}

# Upload key as .txt file
r = s.post(f"{SITE}/wp-json/wp/v2/media", headers={
    **h,
    "Content-Disposition": f'attachment; filename="{KEY}.txt"',
    "Content-Type": "text/plain",
}, data=KEY.encode())

if r.status_code == 201:
    print(f"OK: Key file uploaded -> {r.json().get('source_url', 'unknown')}")
else:
    print(f"FAIL: {r.status_code} {r.text[:200]}")
    print("Alternative: Install 'IndexNow' plugin in WordPress")
