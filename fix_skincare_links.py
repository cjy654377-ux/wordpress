#!/usr/bin/env python3
"""Add internal links to skincare article body + related section."""
import os, sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import login, REST

SITE = "https://rhythmicaleskimo.com"
POST_ID = 76

def main():
    s, h = login()
    r = s.get(f"{REST}/posts/{POST_ID}", headers=h)
    content = r.json()["content"]["rendered"]

    # Add contextual link in Oil Cleanser section - mention Olive Young
    content = content.replace(
        "Buy from the artist",
        "Buy from the artist"  # no change needed here
    )

    # Add "You Might Also Like" before FAQ schema
    if 'You Might Also Like' not in content:
        related = f"""
<h2>You Might Also Like</h2>
<ul>
<li><a href="{SITE}/olive-young-shopping-guide-top-15-k-beauty-products-under-15-that-actually-work/">Olive Young Guide: Top 15 K-Beauty Products Under $15</a></li>
<li><a href="{SITE}/top-7-k-beauty-trends-dominating-2026-pdrn-exosomes-and-the-science-behind-korean-skincares-revolution/">Top 7 K-Beauty Trends Dominating 2026</a></li>
<li><a href="{SITE}/myeongdong-street-food-map-the-12-best-stalls-with-exact-locations-2026/">Myeongdong Street Food Map (Near Olive Young Flagship)</a></li>
</ul>"""
        if '<script type="application/ld+json">' in content:
            parts = content.rsplit('<script type="application/ld+json">', 1)
            content = parts[0] + related + '\n<script type="application/ld+json">' + parts[1]
        else:
            content += related

    # Add inline link to Olive Young in the moisturizer section
    content = content.replace(
        "Korean sunscreens are famous",
        f'Korean sunscreens (available at <a href="{SITE}/olive-young-shopping-guide-top-15-k-beauty-products-under-15-that-actually-work/">Olive Young stores nationwide</a>) are famous'
    )

    r = s.post(f"{REST}/posts/{POST_ID}", headers=h, json={"content": content})
    if r.status_code == 200:
        print(f"OK Updated skincare with links -> {r.json()['link']}")
    else:
        print(f"FAIL {r.status_code}")

if __name__ == "__main__":
    main()
