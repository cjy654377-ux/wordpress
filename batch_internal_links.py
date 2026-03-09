#!/usr/bin/env python3
"""Add internal links to high-value posts for SEO boost."""
import os, sys, re, json
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import login, REST

# Define link clusters: post_id -> list of (anchor_text, target_url) to append
LINK_CLUSTERS = {
    # Tangerines filming locations -> link to Jeju food, K-drama cafes
    72: [
        ("Jeju Island Food Guide: 7 Unique Dishes You Can Only Eat Here", "/jeju-island-food-guide-7-unique-dishes-you-can-only-eat-on-koreas-tropical-island/"),
        ("Top 10 K-Drama Cafes in Seoul You Can Actually Visit", "/top-10-k-drama-cafes-in-seoul-you-can-actually-visit-in-2026/"),
        ("Korean BBQ Etiquette: 12 Rules Every First-Timer Needs to Know", "/korean-bbq-etiquette-12-rules-every-first-timer-needs-to-know/"),
    ],
    # BTS BST lyrics -> link to other BTS lyrics
    413: [
        ("BTS Black Swan Lyrics Meaning", "/bts-black-swan-lyrics-meaning-when-music-becomes-your-first-death/"),
        ("BTS Fake Love Lyrics Meaning", "/bts-fake-love-lyrics-meaning-the-pain-of-erasing-yourself-to-be-loved/"),
        ("BTS Spring Day Lyrics Meaning", "/bts-spring-day-%eb%b4%84%eb%82%a0-lyrics-meaning-the-deepest-k-pop-song-ever-written/"),
    ],
    # BTS Black Swan -> other BTS
    409: [
        ("BTS Blood Sweat & Tears Lyrics Meaning", "/bts-blood-sweat-tears-lyrics-meaning-demian-abraxas-the-art-of-temptation/"),
        ("BTS Fake Love Lyrics Meaning", "/bts-fake-love-lyrics-meaning-the-pain-of-erasing-yourself-to-be-loved/"),
        ("BTS Spring Day Lyrics Meaning", "/bts-spring-day-%eb%b4%84%eb%82%a0-lyrics-meaning-the-deepest-k-pop-song-ever-written/"),
    ],
    # BTS Fake Love -> other BTS
    411: [
        ("BTS Blood Sweat & Tears Lyrics Meaning", "/bts-blood-sweat-tears-lyrics-meaning-demian-abraxas-the-art-of-temptation/"),
        ("BTS Black Swan Lyrics Meaning", "/bts-black-swan-lyrics-meaning-when-music-becomes-your-first-death/"),
        ("BTS Spring Day Lyrics Meaning", "/bts-spring-day-%eb%b4%84%eb%82%a0-lyrics-meaning-the-deepest-k-pop-song-ever-written/"),
    ],
    # BTS Spring Day -> other BTS
    404: [
        ("BTS Blood Sweat & Tears Lyrics Meaning", "/bts-blood-sweat-tears-lyrics-meaning-demian-abraxas-the-art-of-temptation/"),
        ("BTS Black Swan Lyrics Meaning", "/bts-black-swan-lyrics-meaning-when-music-becomes-your-first-death/"),
        ("BTS Fake Love Lyrics Meaning", "/bts-fake-love-lyrics-meaning-the-pain-of-erasing-yourself-to-be-loved/"),
    ],
    # BTS Arirang Tour -> concert guide, Korean phrases
    394: [
        ("25 Essential Korean Phrases for the Arirang Tour", "/25-essential-korean-phrases-every-bts-fan-needs-for-the-arirang-world-tour-2026/"),
        ("Your First K-Pop Concert in Korea: Survival Guide", "/your-first-k-pop-concert-in-korea-the-ultimate-survival-guide/"),
        ("BTS Arirang Comeback 2026: Album & Netflix Concert", "/bts-arirang-comeback-2026-everything-you-need-to-know-about-the-album-world-tour-and-netflix-concert/"),
    ],
    # K-Beauty -> Olive Young, Skincare routine
    357: [
        ("Olive Young Guide: Top 15 K-Beauty Products Under $15", "/olive-young-shopping-guide-top-15-k-beauty-products-under-15-that-actually-work/"),
        ("The 10-Step Korean Skincare Routine: Beginner's Guide", "/the-10-step-korean-skincare-routine-a-complete-beginners-guide-for-2026/"),
    ],
    # Korean BBQ -> Soju, Anju, Street Food
    48: [
        ("Soju Guide: How to Drink Korea's National Spirit", "/soju-guide-for-beginners-how-to-drink-koreas-national-spirit-like-a-local/"),
        ("Korean Drinking Food (Anju): Best Bar Snacks", "/korean-drinking-food-anju-the-best-bar-snacks-to-order-with-soju-and-beer/"),
        ("How to Order Food in Korean: 25 Essential Phrases", "/how-to-order-food-in-korean-25-essential-phrases-every-traveler-needs/"),
    ],
    # Myeongdong Street Food -> Gwangjang, Korean Street Food guide
    180: [
        ("Gwangjang Market Food Guide", "/gwangjang-market-food-guide-seouls-oldest-market-and-its-legendary-eats/"),
        ("Ultimate Guide to Korean Street Food: 15 Must-Try Snacks", "/the-ultimate-guide-to-korean-street-food-15-must-try-snacks-and-where-to-find-them/"),
        ("Seoul's Hidden Alley Restaurants: 7 Local-Only Spots", "/seouls-hidden-alley-restaurants-7-places-only-locals-know-about/"),
    ],
    # Hangul reading guide -> Learn Korean K-dramas, Order Food Korean
    186: [
        ("Learn Korean Through K-Dramas: 30 Essential Phrases", "/learn-korean-through-k-dramas-30-essential-phrases-youll-actually-use/"),
        ("How to Order Food in Korean: 25 Phrases", "/how-to-order-food-in-korean-25-essential-phrases-every-traveler-needs/"),
    ],
    # Boyfriend on Demand -> 5 Must Watch, K-Drama Cafes
    355: [
        ("5 Must-Watch K-Dramas Before Boyfriend on Demand", "/5-must-watch-k-dramas-before-boyfriend-on-demand-premieres-on-netflix/"),
        ("Top 10 K-Drama Cafes in Seoul", "/top-10-k-drama-cafes-in-seoul-you-can-actually-visit-in-2026/"),
    ],
}

SITE = "https://rhythmicaleskimo.com"


def build_related_section(links):
    items = "\n".join(
        f'<li><a href="{SITE}{url}">{text}</a></li>' for text, url in links
    )
    return f'\n<h2>You Might Also Like</h2>\n<ul>\n{items}\n</ul>'


def main():
    s, h = login()
    updated = 0

    for post_id, links in LINK_CLUSTERS.items():
        r = s.get(f"{REST}/posts/{post_id}", headers=h)
        if r.status_code != 200:
            print(f"SKIP {post_id}: fetch failed")
            continue

        post = r.json()
        content = post["content"]["rendered"]
        title = re.sub(r'&#\d+;', '', post["title"]["rendered"])[:50]

        if 'You Might Also Like' in content:
            print(f"SKIP {post_id}: already has related links | {title}")
            continue

        # Insert before FAQ schema if exists, otherwise append
        if '<script type="application/ld+json">' in content:
            parts = content.rsplit('<script type="application/ld+json">', 1)
            new_content = parts[0] + build_related_section(links) + '\n<script type="application/ld+json">' + parts[1]
        else:
            new_content = content + build_related_section(links)

        r = s.post(f"{REST}/posts/{post_id}", headers=h, json={"content": new_content})
        if r.status_code == 200:
            print(f"OK   {post_id}: +{len(links)} links | {title}")
            updated += 1
        else:
            print(f"FAIL {post_id}: {r.status_code} | {title}")

    print(f"\nDone: {updated} updated")


if __name__ == "__main__":
    main()
