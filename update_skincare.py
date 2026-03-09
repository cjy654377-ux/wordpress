#!/usr/bin/env python3
import os, sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import login, REST

POST_ID = 76
BASE = os.path.dirname(os.path.abspath(__file__))

def main():
    s, h = login()
    with open(os.path.join(BASE, "article_skincare_v2.html"), encoding="utf-8") as f:
        content = f.read()
    r = s.post(f"{REST}/posts/{POST_ID}", headers=h, json={
        "content": content,
        "excerpt": "The complete 10-step Korean skincare routine with budget product picks under $15, simplified routines for beginners, and the 3-step minimum that actually works."
    })
    if r.status_code == 200:
        print(f"OK Updated -> {r.json()['link']}")
    else:
        print(f"FAIL {r.status_code}")

if __name__ == "__main__":
    main()
