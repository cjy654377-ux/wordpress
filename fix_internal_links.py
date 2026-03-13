#!/usr/bin/env python3
"""Fix broken internal links in 20 expanded posts."""
import re, sys, difflib
sys.path.insert(0, "/Users/choijooyong/wordpress")
from engine import login, REST

# All 56 posts: ID → actual slug
SLUG_MAP = {
    612: "/30-korean-words-phrases-youll-hear-in-boyfriend-on-demand-the-ultimate-k-drama-vocabulary-guide/",
    609: "/korea-cherry-blossom-season-2026-complete-guide-to-dates-festivals-best-spots-travel-tips/",
    606: "/boyfriend-on-demand-jisoos-netflix-k-drama-complete-guide-cast-review-cameos-everything-you-need-to-know/",
    566: "/bts-arirang-album-the-cultural-meaning-behind-every-song-han-heung-and-600-years-of-korean-soul/",
    549: "/post-procedure-korean-skincare-what-korean-dermatologists-recommend-after-botox-lasers-peels/",
    547: "/korean-peptide-serums-the-science-behind-koreas-anti-aging-revolution/",
    545: "/medicube-age-r-review-2026-is-koreas-viral-at-home-beauty-device-worth-it/",
    543: "/korean-scalp-care-the-k-beauty-secret-to-thicker-healthier-hair/",
    541: "/pdrn-skincare-explained-why-salmon-dna-is-koreas-hottest-beauty-ingredient-in-2026/",
    539: "/the-complete-korean-skincare-routine-for-oily-skin-7-steps-that-actually-work/",
    537: "/best-korean-sunscreens-2026-dermatologist-approved-spf-for-every-skin-type/",
    464: "/when-life-gives-you-tangerines-cast-guide-iu-park-bo-gum-the-real-married-couple-2025/",
    413: "/bts-blood-sweat-tears-lyrics-meaning-demian-abraxas-the-art-of-temptation/",
    411: "/bts-fake-love-lyrics-meaning-the-pain-of-erasing-yourself-to-be-loved/",
    409: "/bts-black-swan-lyrics-meaning-when-music-becomes-your-first-death/",
    404: "/bts-spring-day-%eb%b4%84%eb%82%a0-lyrics-meaning-the-deepest-k-pop-song-ever-written/",
    394: "/bts-arirang-world-tour-2026-complete-city-by-city-date-guide-and-how-to-get-tickets/",
    393: "/5-must-watch-k-dramas-before-boyfriend-on-demand-premieres-on-netflix/",
    361: "/25-essential-korean-phrases-every-bts-fan-needs-for-the-arirang-world-tour-2026/",
    359: "/how-the-iran-war-is-hitting-south-korea-oil-prices-won-currency-and-what-ordinary-koreans-face-next/",
    357: "/top-7-k-beauty-trends-dominating-2026-pdrn-exosomes-and-the-science-behind-korean-skincares-revolution/",
    186: "/how-to-read-korean-hangul-in-30-minutes-the-fastest-method-that-actually-works/",
    184: "/hybe-insight-museum-big-4-entertainment-tours-the-ultimate-k-pop-pilgrimage-in-seoul/",
    182: "/olive-young-shopping-guide-top-15-k-beauty-products-under-15-that-actually-work/",
    180: "/myeongdong-street-food-map-the-12-best-stalls-with-exact-locations-2026/",
    178: "/top-10-k-drama-cafes-in-seoul-you-can-actually-visit-in-2026/",
    80: "/learn-korean-through-k-dramas-30-essential-phrases-youll-actually-use/",
    78: "/your-first-k-pop-concert-in-korea-the-ultimate-survival-guide/",
    76: "/the-10-step-korean-skincare-routine-a-complete-beginners-guide-for-2026/",
    74: "/seouls-hidden-alley-restaurants-7-places-only-locals-know-about/",
    72: "/where-to-visit-filming-locations-of-when-life-gives-you-tangerines-in-jeju/",
    69: "/korean-drinking-food-anju-the-best-bar-snacks-to-order-with-soju-and-beer/",
    67: "/jeju-island-food-guide-7-unique-dishes-you-can-only-eat-on-koreas-tropical-island/",
    65: "/korean-convenience-store-food-ranking-top-20-must-try-items-at-cu-gs25-and-7-eleven/",
    63: "/soju-guide-for-beginners-how-to-drink-koreas-national-spirit-like-a-local/",
    61: "/busan-food-guide-8-dishes-you-can-only-find-in-koreas-coastal-city/",
    59: "/korean-temple-food-the-zen-buddhist-cuisine-you-never-knew-existed/",
    57: "/korean-fried-chicken-guide-why-kfc-means-something-different-in-korea/",
    55: "/jeonju-bibimbap-vs-seoul-bibimbap-whats-the-difference-and-where-to-eat/",
    53: "/gwangjang-market-food-guide-seouls-oldest-market-and-its-legendary-eats/",
    51: "/how-to-order-food-in-korean-25-essential-phrases-every-traveler-needs/",
    48: "/korean-bbq-etiquette-12-rules-every-first-timer-needs-to-know/",
    46: "/budgets-meals-in-korea-10-tv-featured-restaurants-where-you-can-eat-for-under-10/",
    44: "/the-ultimate-guide-to-korean-street-food-15-must-try-snacks-and-where-to-find-them/",
    42: "/korean-food-show-guide-what-is-2tv-%ec%83%9d%ec%83%9d%ec%a0%95%eb%b3%b4-and-why-every-foodie-should-watch-it/",
    40: "/top-10-must-try-korean-soups-for-winter-from-tv-show-kitchens-to-your-travel-list/",
    29: "/han-hye-jins-hongcheon-food-trip-buckwheat-noodles-mind-blowing-tofu-pine-nut-hotteok/",
    27: "/pohang-halmae-jip-70-year-old-3rd-generation-ox-head-soup-in-yeongcheon-market/",
    25: "/haengju-chueotang-comedian-kim-mi-ryeos-go-to-loach-soup-at-haengju-fortress/",
    23: "/imja-triple-style-fresh-monkfish-soup-with-free-liver-service-in-gangnam/",
    21: "/gukbo-1st-unlimited-korean-beef-noodle-soup-bossam-for-10-in-bucheon/",
    19: "/seomyeon-sondubu-jip-grandmas-handmade-tofu-set-meal-in-chuncheon/",
    17: "/jun-%ec%a4%80-mind-blowing-king-rib-seafood-stone-plate-jjajang-in-daegu/",
    15: "/yasanhaechon-singer-seol-woon-dos-favorite-fresh-cod-soup-in-yangpyeong/",
    13: "/world-bap-all-you-can-eat-korean-buffet-for-only-6-in-gwangju/",
    11: "/bangi-gullim-mandu-ttegul-giant-hand-rolled-dumpling-hot-pot-in-seoul-songpa-gu/",
}

SITE = "https://rhythmicaleskimo.com"
VALID_URLS = {SITE + slug for slug in SLUG_MAP.values()}
VALID_SLUGS = set(SLUG_MAP.values())

TARGET_IDS = [76, 549, 547, 539, 543, 537, 541, 545, 357, 394,
              74, 72, 464, 61, 182, 178, 361, 404, 78, 186]

def find_best_match(broken_slug):
    """Find the most similar valid slug using SequenceMatcher."""
    best, best_ratio = None, 0
    for valid in VALID_SLUGS:
        ratio = difflib.SequenceMatcher(None, broken_slug, valid).ratio()
        if ratio > best_ratio:
            best_ratio = ratio
            best = valid
    return best, best_ratio

def main():
    s, h = login()
    print(f"Logged in. Processing {len(TARGET_IDS)} posts...\n")

    total_fixed = 0
    total_posts_changed = 0

    for pid in TARGET_IDS:
        r = s.get(f"{REST}/posts/{pid}?context=edit", headers=h)
        if r.status_code != 200:
            print(f"  ERROR: Could not fetch post {pid}: {r.status_code}")
            continue

        post = r.json()
        title = post["title"]["raw"][:60]
        content = post["content"]["raw"]

        # Find all internal links
        pattern = r'href="https://rhythmicaleskimo\.com(/[^"]*)"'
        matches = re.findall(pattern, content)

        if not matches:
            continue

        changes = []
        new_content = content

        for slug in matches:
            full_url = SITE + slug
            if full_url in VALID_URLS:
                continue  # Link is valid

            # Broken link found — find best match
            best, ratio = find_best_match(slug)
            if best and ratio > 0.4:
                old_url = SITE + slug
                new_url = SITE + best
                new_content = new_content.replace(old_url, new_url)
                changes.append((slug, best, f"{ratio:.0%}"))

        if changes:
            # Update post
            r2 = s.post(f"{REST}/posts/{pid}", headers=h,
                        json={"content": new_content})
            if r2.status_code == 200:
                total_posts_changed += 1
                total_fixed += len(changes)
                print(f"[ID:{pid}] {title}")
                for old, new, ratio in changes:
                    print(f"  {old}")
                    print(f"  → {new}  ({ratio})")
                print()
            else:
                print(f"  ERROR updating {pid}: {r2.status_code}")

    print(f"\n=== DONE ===")
    print(f"Posts updated: {total_posts_changed}")
    print(f"Links fixed:   {total_fixed}")

if __name__ == "__main__":
    main()
