#!/usr/bin/env python3
"""CTR-optimize WordPress post titles for SEO."""
import requests, re, sys, json, html as htmlmod

SITE = "https://rhythmicaleskimo.com"
REST = f"{SITE}/wp-json/wp/v2"
USER = "cjy654377@gmail.com"
PASS = "Dkflekd1!!"

def login():
    s = requests.Session()
    s.cookies.set("wordpress_test_cookie", "WP+Cookie+check")
    s.post(f"{SITE}/wp-login.php", data={
        "log": USER, "pwd": PASS, "wp-submit": "Log In",
        "redirect_to": "/wp-admin/", "testcookie": "1"
    }, allow_redirects=True)
    page = s.get(f"{SITE}/wp-admin/post-new.php").text
    m = re.search(r'"nonce":"([a-f0-9]+)"', page)
    if not m:
        print("ERROR: nonce not found"); sys.exit(1)
    return s, {"X-WP-Nonce": m.group(1)}

def get_all_posts(s, h):
    posts = []
    page = 1
    while True:
        r = s.get(f"{REST}/posts?per_page=100&page={page}&status=publish", headers=h)
        if r.status_code != 200:
            break
        batch = r.json()
        if not batch:
            break
        for p in batch:
            posts.append({
                "id": p["id"],
                "title": htmlmod.unescape(p["title"]["rendered"]),
                "slug": p["slug"],
            })
        page += 1
    return posts

def update_title(s, h, post_id, new_title):
    r = s.post(f"{REST}/posts/{post_id}", headers=h, json={"title": new_title})
    if r.status_code == 200:
        print(f"  OK  ID:{post_id} → {new_title}")
        return True
    else:
        print(f"  FAIL ID:{post_id} ({r.status_code}): {r.text[:100]}")
        return False

# ── CTR-optimized title mappings ──
# Rules: ≤60 chars, numbers, year 2026, emotion triggers, brackets
# Only posts that NEED changes (already ≤60 and good → skip)
TITLE_UPDATES = {
    # ═══ GSC-EXPOSED POSTS (highest priority) ═══

    # GSC: "abraxas bts meaning", "bts blood sweat and tears meaning"
    413: "BTS Blood Sweat & Tears: Abraxas Meaning Explained",
    # 51 chars. Keywords front-loaded. Was 89 chars.

    # GSC: "when life gives you tangerines filming locations"
    72: "When Life Gives You Tangerines: 8 Jeju Locations",
    # 49 chars. Kept "8" (original count), added Jeju. Was 105 chars.

    # GSC: "how to read hangul", "learn hangul in 30 minutes"
    186: "How to Read Hangul in 30 Minutes [Free Guide 2026]",
    # 51 chars. Matches exact search query. Was 81 chars.

    # GSC: "learn korean through k dramas"
    80: "Learn Korean via K-Dramas: 30 Phrases [2026 Guide]",
    # 51 chars. Was 77 chars.

    # ═══ K-BEAUTY (high CPC) ═══

    76: "10-Step Korean Skincare Routine: Beginner Guide 2026",
    # 52 chars. Was 79.

    357: "7 K-Beauty Trends 2026: PDRN, Exosomes & More",
    # 46 chars. Was 112.

    537: "Best Korean Sunscreens 2026: Top SPF Picks [Guide]",
    # 51 chars. Was 75.

    539: "Korean Skincare for Oily Skin: 7 Steps That Work",
    # 49 chars. Was 78.

    541: "PDRN Skincare: Why Salmon DNA Is Korea's #1 Trend",
    # 50 chars. Was 90.

    543: "Korean Scalp Care: K-Beauty Secret for Thick Hair",
    # 50 chars. Was 65.

    545: "Medicube AGE-R Review 2026: Worth the Hype? [Test]",
    # 51 chars. Was 82.

    547: "Korean Peptide Serums: Anti-Aging Science Explained",
    # 51 chars. Was 77.

    549: "Post-Procedure K-Skincare: Dermatologist Tips 2026",
    # 51 chars. Was 101.

    182: "Olive Young Top 15 Products Under $15 [2026 Guide]",
    # 51 chars. Was 81.

    # ═══ BTS / K-POP ═══

    404: "BTS Spring Day Lyrics: The Deepest K-Pop Song Ever",
    # 51 chars. Was 71 (ok but adding emphasis).

    409: "BTS Black Swan Meaning: When Music Becomes Death",
    # 49 chars. Was 66.

    411: "BTS Fake Love Meaning: The Pain of Erasing Yourself",
    # 52 chars. Was 70.

    566: "BTS ARIRANG Album Meaning: Han, Heung & 600 Years",
    # 51 chars. Was 100.

    394: "BTS Arirang Tour 2026: Dates, Cities & Ticket Guide",
    # 52 chars. Was 84.

    361: "25 Korean Phrases for BTS Arirang World Tour [2026]",
    # 51 chars. Was 79.

    184: "HYBE Insight & Big 4 Tours: K-Pop Pilgrimage Seoul",
    # 51 chars. Was 92.

    78: "First K-Pop Concert in Korea: Ultimate Guide [2026]",
    # 52 chars. Was 62.

    # ═══ K-DRAMA ═══

    606: "Boyfriend on Demand: Jisoo K-Drama Guide [Netflix]",
    # 51 chars. Was 125.

    612: "30 Korean Phrases in Boyfriend on Demand [K-Drama]",
    # 51 chars. Was 110.

    393: "5 K-Dramas to Watch Before Boyfriend on Demand",
    # 47 chars. Was 69.

    464: "When Life Gives You Tangerines Cast: Full Guide",
    # 48 chars. Was 110.

    178: "Top 10 K-Drama Cafes in Seoul You Can Visit [2026]",
    # 51 chars. Was 60 (add year + brackets).

    # ═══ TRAVEL & FOOD ═══

    44: "Korean Street Food Guide: 15 Must-Try Snacks [Map]",
    # 51 chars. Was 84.

    42: "Korean Food Show Guide: What Is 2TV 생생정보통?",
    # 41 chars. Was 92.

    40: "10 Must-Try Korean Soups for Winter [2026 Guide]",
    # 49 chars. Was 83.

    46: "Budget Meals in Korea: 10 Spots Under $10 [TV Pick]",
    # 52 chars. Was 82.

    48: "Korean BBQ Etiquette: 12 Rules for First-Timers",
    # 48 chars. Was 62.

    51: "How to Order Food in Korean: 25 Essential Phrases",
    # 50 chars. Was 71.

    53: "Gwangjang Market Food Guide: Seoul's Legendary Eats",
    # 52 chars. Was 80.

    55: "Jeonju vs Seoul Bibimbap: What's the Difference?",
    # 49 chars. Was 80.

    57: "Korean Fried Chicken Guide: Why KFC Means More Here",
    # 52 chars. Was 71.

    59: "Korean Temple Food: Zen Cuisine You Never Knew",
    # 47 chars. Was 67.

    61: "Busan Food Guide: 8 Dishes Only Found Here [2026]",
    # 50 chars. Was 74.

    63: "Soju Guide: How to Drink Korea's Spirit Like a Local",
    # 53 chars. Was 81.

    65: "Korean Convenience Store Ranking: Top 20 Must-Buys",
    # 51 chars. Was 87.

    67: "Jeju Food Guide: 7 Dishes Only Found on the Island",
    # 51 chars. Was 89.

    69: "Korean Anju Guide: Best Bar Snacks with Soju & Beer",
    # 52 chars. Was 76.

    74: "Seoul's Hidden Restaurants: 7 Spots Locals Love",
    # 49 chars. Was 71.

    180: "Myeongdong Street Food: 12 Best Stalls Map [2026]",
    # 50 chars. Was 74.

    609: "Korea Cherry Blossoms 2026: Dates, Spots & Tips",
    # 48 chars. Was 99.

    # ═══ INDIVIDUAL RESTAURANT POSTS ═══
    # These are niche — shorten for clarity

    11: "Giant Dumpling Hot Pot in Seoul Songpa-gu [Hidden]",
    # 51 chars. Was 81.

    13: "All-You-Can-Eat Korean Buffet for $6 in Gwangju",
    # 48 chars. Was 64.

    15: "Best Fresh Cod Soup in Yangpyeong [Celebrity Pick]",
    # 51 chars. Was 80.

    17: "King Rib Jjajang in Daegu: Mind-Blowing Seafood",
    # 48 chars. Was 68.

    19: "Grandma's Handmade Tofu in Chuncheon [Must Visit]",
    # 50 chars. Was 74.

    21: "Unlimited Beef Soup & Bossam for $10 in Bucheon",
    # 48 chars. Was 78.

    23: "Fresh Monkfish Soup in Gangnam [Free Liver Dish]",
    # 49 chars. Was 74.

    25: "Celebrity's Go-To Loach Soup at Haengju Fortress",
    # 49 chars. Was 85.

    27: "70-Year-Old Ox Head Soup in Yeongcheon Market",
    # 46 chars. Was 81.

    29: "Hongcheon Food Trip: Buckwheat Noodles & Tofu",
    # 46 chars. Was 102.

    # ═══ WORLD NEWS / OTHER ═══

    359: "Iran War Impact on South Korea: Oil, Won & Economy",
    # 51 chars. Was 102.
}

if __name__ == "__main__":
    print("=== CTR Title Optimizer ===\n")
    s, h = login()
    print("Logged in. Fetching posts...\n")
    posts = get_all_posts(s, h)
    print(f"Found {len(posts)} posts.\n")

    # Verify all title lengths
    print("── New Title Length Verification ──")
    errors = []
    for pid, new_t in sorted(TITLE_UPDATES.items()):
        tlen = len(new_t)
        status = "OK" if tlen <= 60 else "TOO LONG"
        if tlen > 60:
            errors.append((pid, new_t, tlen))
        old = next((p["title"] for p in posts if p["id"] == pid), "???")
        print(f"  {status:8s} [{tlen:2d}] ID:{pid:4d}  {new_t}")

    if errors:
        print(f"\n{len(errors)} titles still >60 chars! Fix before applying.")
        for pid, t, l in errors:
            print(f"  ID:{pid} [{l}]: {t}")
        if "--apply" in sys.argv:
            print("Aborting.")
            sys.exit(1)

    # Show unchanged posts
    updated_ids = set(TITLE_UPDATES.keys())
    unchanged = [p for p in posts if p["id"] not in updated_ids]
    if unchanged:
        print(f"\n── Unchanged Posts ({len(unchanged)}) ──")
        for p in sorted(unchanged, key=lambda x: x["id"]):
            tlen = len(p["title"])
            flag = "⚠>60" if tlen > 60 else "  OK"
            print(f"  {flag} [{tlen:2d}] ID:{p['id']:4d}  {p['title'][:70]}")

    print(f"\n── Summary ──")
    print(f"  Total posts: {len(posts)}")
    print(f"  To update: {len(TITLE_UPDATES)}")
    print(f"  Unchanged: {len(unchanged)}")

    if "--dry-run" in sys.argv:
        print("\n[DRY RUN] No changes made.")
        sys.exit(0)

    if "--apply" not in sys.argv:
        print("\nUse --apply to execute, --dry-run to preview.")
        sys.exit(0)

    # Apply updates
    print("\n── Applying Updates ──")
    ok = 0
    for pid, new_t in TITLE_UPDATES.items():
        if update_title(s, h, pid, new_t):
            ok += 1
    print(f"\nDone: {ok}/{len(TITLE_UPDATES)} updated.")
