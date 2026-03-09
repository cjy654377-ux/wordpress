#!/usr/bin/env python3
"""Update Hangul reading guide article."""
import os, sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import login, REST

POST_ID = 186
NEW_TITLE = "How to Read Korean (Hangul) in 30 Minutes: The Fastest Method That Actually Works"
NEW_EXCERPT = "Learn all 24 Hangul letters with visual mnemonics, syllable block rules, and practice words you already know. From zero to reading Korean in one sitting."
BASE = os.path.dirname(os.path.abspath(__file__))

def main():
    s, h = login()
    with open(os.path.join(BASE, "article_hangul_v2.html"), encoding="utf-8") as f:
        content = f.read()
    r = s.post(f"{REST}/posts/{POST_ID}", headers=h, json={
        "title": NEW_TITLE, "content": content, "excerpt": NEW_EXCERPT
    })
    if r.status_code == 200:
        print(f"OK Updated -> {r.json()['link']}")
    else:
        print(f"FAIL {r.status_code}: {r.text[:200]}")

if __name__ == "__main__":
    main()
