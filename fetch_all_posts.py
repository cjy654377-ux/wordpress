#!/usr/bin/env python3
"""Fetch all posts and check excerpt status."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import login, REST

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
            exc = p.get("excerpt", {}).get("rendered", "").strip()
            # strip HTML tags
            import re
            exc_text = re.sub(r'<[^>]+>', '', exc).strip()
            all_posts.append({
                "id": p["id"],
                "title": p["title"]["rendered"],
                "slug": p["slug"],
                "link": p["link"],
                "excerpt": exc_text[:100] if exc_text else "",
                "has_excerpt": bool(exc_text and len(exc_text) > 30),
            })
        pg += 1

    # Save to JSON
    base = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base, "all_posts_status.json"), "w", encoding="utf-8") as f:
        json.dump(all_posts, f, ensure_ascii=False, indent=2)

    no_exc = [p for p in all_posts if not p["has_excerpt"]]
    has_exc = [p for p in all_posts if p["has_excerpt"]]
    print(f"Total: {len(all_posts)} posts")
    print(f"With excerpt: {len(has_exc)}")
    print(f"Missing excerpt: {len(no_exc)}")
    print()
    for p in all_posts:
        status = "OK" if p["has_excerpt"] else "MISSING"
        print(f"[{status}] {p['id']} | {p['title'][:60]}")

if __name__ == "__main__":
    main()
