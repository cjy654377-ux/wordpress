#!/usr/bin/env python3
"""Update 5 March 3 articles on WordPress after edits."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import login, REST

BASE = os.path.dirname(os.path.abspath(__file__))

s, h = login()
print("Logged in.")

with open(os.path.join(BASE, "template.html")) as f:
    template = f.read()

updates = [
    (353, "article_bts_arirang.html", "BTS Arirang"),
    (355, "article_boyfriend_demand.html", "Boyfriend on Demand"),
    (357, "article_kbeauty_2026.html", "K-Beauty 2026"),
    (359, "article_iran_korea.html", "Iran-Korea"),
    (361, "article_korean_bts.html", "Korean Phrases"),
]

for pid, html_file, label in updates:
    with open(os.path.join(BASE, html_file)) as f:
        body = f.read()
    content = template.replace("{CONTENT}", body)
    r = s.post(f"{REST}/posts/{pid}", headers=h, json={"content": content})
    if r.status_code == 200:
        print(f"  Updated: {label} (ID={pid})")
    else:
        print(f"  FAIL {label}: {r.status_code} {r.text[:100]}")

print("Done!")
