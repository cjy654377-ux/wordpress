#!/usr/bin/env python3
"""Cross-link Tangerines cluster articles + concert guide internal links."""
import os, sys, re
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import login, REST

SITE = "https://rhythmicaleskimo.com"

LINKS_TO_ADD = {
    # Tangerines filming locations -> cast guide
    72: [
        ("'Tangerines' Cast Guide: IU, Park Bo-gum & the Real Married Couple",
         "/when-life-gives-you-tangerines-cast-guide-iu-park-bo-gum-the-real-married-couple-2025/"),
    ],
    # Cast guide -> filming locations
    464: [
        ("8 Filming Locations You Can Actually Visit in Jeju",
         "/where-to-visit-filming-locations-of-when-life-gives-you-tangerines-in-jeju/"),
        ("Top 10 K-Drama Cafes in Seoul",
         "/top-10-k-drama-cafes-in-seoul-you-can-actually-visit-in-2026/"),
    ],
    # Concert guide -> BTS tour, Korean phrases, K-pop pilgrimage
    78: [
        ("BTS Arirang World Tour 2026: Complete Date Guide",
         "/bts-arirang-world-tour-2026-complete-city-by-city-date-guide-and-how-to-get-tickets/"),
        ("25 Korean Phrases for the BTS Arirang Tour",
         "/25-essential-korean-phrases-every-bts-fan-needs-for-the-arirang-world-tour-2026/"),
        ("HYBE Insight Museum & Big 4 K-Pop Tours in Seoul",
         "/hybe-insight-museum-big-4-entertainment-tours-the-ultimate-k-pop-pilgrimage-in-seoul/"),
    ],
}


def main():
    s, h = login()
    updated = 0

    for post_id, links in LINKS_TO_ADD.items():
        r = s.get(f"{REST}/posts/{post_id}", headers=h)
        if r.status_code != 200:
            print(f"SKIP {post_id}: fetch failed")
            continue

        post = r.json()
        content = post["content"]["rendered"]
        title = re.sub(r'&#\d+;', '', post["title"]["rendered"])[:50]

        # Check if links already exist
        already = sum(1 for _, url in links if url in content)
        if already == len(links):
            print(f"SKIP {post_id}: all links exist | {title}")
            continue

        # Build new links (only missing ones)
        new_links = [(text, url) for text, url in links if url not in content]
        if not new_links:
            continue

        items = "\n".join(f'<li><a href="{SITE}{url}">{text}</a></li>' for text, url in new_links)
        section = f'\n<h2>You Might Also Like</h2>\n<ul>\n{items}\n</ul>'

        # Check if "You Might Also Like" exists, append to it
        if 'You Might Also Like' in content:
            # Add new items to existing section
            for text, url in new_links:
                link_html = f'<li><a href="{SITE}{url}">{text}</a></li>'
                content = content.replace('</ul>\n\n<script', f'{link_html}\n</ul>\n\n<script')
                if link_html not in content:
                    content = content.replace('</ul>', f'{link_html}\n</ul>', 1)
        else:
            if '<script type="application/ld+json">' in content:
                parts = content.rsplit('<script type="application/ld+json">', 1)
                content = parts[0] + section + '\n<script type="application/ld+json">' + parts[1]
            else:
                content += section

        r = s.post(f"{REST}/posts/{post_id}", headers=h, json={"content": content})
        if r.status_code == 200:
            print(f"OK   {post_id}: +{len(new_links)} links | {title}")
            updated += 1
        else:
            print(f"FAIL {post_id}: {r.status_code} | {title}")

    print(f"\nDone: {updated} updated")


if __name__ == "__main__":
    main()
