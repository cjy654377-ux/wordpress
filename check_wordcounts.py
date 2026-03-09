#!/usr/bin/env python3
"""Check word counts for all posts via WP API."""
import os, sys, re, json
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import login, REST

def strip_html(text):
    return re.sub(r'<[^>]+>', '', text).strip()

def main():
    s, h = login()
    all_posts = []
    pg = 1
    while True:
        r = s.get(f"{REST}/posts?per_page=100&page={pg}&status=publish", headers=h)
        if r.status_code != 200:
            break
        batch = r.json()
        if not batch:
            break
        for p in batch:
            content = strip_html(p["content"]["rendered"])
            words = len(content.split())
            all_posts.append({
                "id": p["id"],
                "title": re.sub(r'&#\d+;', '', p["title"]["rendered"])[:60],
                "words": words,
                "link": p["link"],
            })
        pg += 1

    all_posts.sort(key=lambda x: x["words"])

    print(f"{'ID':>5} | {'Words':>5} | Title")
    print("-" * 80)
    for p in all_posts:
        flag = "<<< THIN" if p["words"] < 800 else ""
        print(f"{p['id']:>5} | {p['words']:>5} | {p['title'][:55]} {flag}")

    thin = [p for p in all_posts if p["words"] < 800]
    print(f"\nTotal: {len(all_posts)} posts, THIN (<800 words): {len(thin)}")

    base = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base, "wordcounts.json"), "w", encoding="utf-8") as f:
        json.dump(all_posts, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
