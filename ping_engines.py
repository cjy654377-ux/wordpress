#!/usr/bin/env python3
"""Search engine sitemap ping + IndexNow submission for rhythmicaleskimo.com"""
import requests, re, sys, uuid, time

SITE = "https://rhythmicaleskimo.com"
SITEMAP = f"{SITE}/sitemap_index.xml"
USER = "cjy654377@gmail.com"
PASS = "Dkflekd1!!"

# All 58 post URLs
URLS = [
    f"{SITE}/bts-blood-sweat-tears-lyrics-meaning-demian-abraxas-the-art-of-temptation/",
    f"{SITE}/bts-fake-love-lyrics-meaning-the-pain-of-erasing-yourself-to-be-loved/",
    f"{SITE}/bts-black-swan-lyrics-meaning-when-music-becomes-your-first-death/",
    f"{SITE}/bts-spring-day-%eb%b4%84%eb%82%a0-lyrics-meaning-the-deepest-k-pop-song-ever-written/",
    f"{SITE}/bts-arirang-world-tour-2026-complete-city-by-city-date-guide-and-how-to-get-tickets/",
    f"{SITE}/5-must-watch-k-dramas-before-boyfriend-on-demand-premieres-on-netflix/",
    f"{SITE}/25-essential-korean-phrases-every-bts-fan-needs-for-the-arirang-world-tour-2026/",
    f"{SITE}/how-the-iran-war-is-hitting-south-korea-oil-prices-won-currency-and-what-ordinary-koreans-face-next/",
    f"{SITE}/top-7-k-beauty-trends-dominating-2026-pdrn-exosomes-and-the-science-behind-korean-skincares-revolution/",
    f"{SITE}/boyfriend-on-demand-jisoos-netflix-k-drama-everyone-is-talking-about-complete-guide/",
    f"{SITE}/bts-arirang-comeback-2026-everything-you-need-to-know-about-the-album-world-tour-and-netflix-concert/",
    f"{SITE}/12-ways-the-iran-war-is-reshaping-the-world-right-now-oil-shocks-cyber-war-nuclear-fears-and-the-largest-refugee-crisis-in-history/",
    f"{SITE}/oil-prices-surge-8-as-iran-conflict-threatens-strait-of-hormuz-global-economic-shockwave-begins/",
    f"{SITE}/us-israel-launch-massive-strikes-on-iran-supreme-leader-khamenei-killed-130-cities-attacked/",
    f"{SITE}/fifa-world-cup-2026-everything-you-need-to-know-about-the-biggest-tournament-ever/",
    f"{SITE}/milano-cortina-2026-winter-paralympics-complete-guide-to-the-games-march-6-15/",
    f"{SITE}/19000-flights-delayed-middle-east-aviation-crisis-strands-travelers-worldwide/",
    f"{SITE}/markets-in-turmoil-war-fears-ai-bubble-concerns-rattle-global-stock-markets/",
    f"{SITE}/trump-bans-anthropic-openai-gets-200m-pentagon-deal-the-ai-arms-race-heats-up/",
    f"{SITE}/pakistan-declares-open-war-on-afghanistan-everything-you-need-to-know/",
    f"{SITE}/iran-strikes-back-missiles-hit-israel-and-gulf-states-as-regional-war-escalates/",
    f"{SITE}/strait-of-hormuz-shutdown-how-irans-blockade-could-trigger-a-global-energy-crisis/",
    f"{SITE}/us-israel-strikes-on-iran-operation-epic-fury-everything-you-need-to-know-live-updates/",
    f"{SITE}/how-to-read-korean-hangul-in-30-minutes-the-fastest-method-that-actually-works/",
    f"{SITE}/hybe-insight-museum-big-4-entertainment-tours-the-ultimate-k-pop-pilgrimage-in-seoul/",
    f"{SITE}/olive-young-shopping-guide-top-15-k-beauty-products-under-15-that-actually-work/",
    f"{SITE}/myeongdong-street-food-map-the-12-best-stalls-with-exact-locations-2026/",
    f"{SITE}/top-10-k-drama-cafes-in-seoul-you-can-actually-visit-in-2026/",
    f"{SITE}/learn-korean-through-k-dramas-30-essential-phrases-youll-actually-use/",
    f"{SITE}/your-first-k-pop-concert-in-korea-the-ultimate-survival-guide/",
    f"{SITE}/the-10-step-korean-skincare-routine-a-complete-beginners-guide-for-2026/",
    f"{SITE}/seouls-hidden-alley-restaurants-7-places-only-locals-know-about/",
    f"{SITE}/where-to-visit-filming-locations-of-when-life-gives-you-tangerines-in-jeju/",
    f"{SITE}/korean-drinking-food-anju-the-best-bar-snacks-to-order-with-soju-and-beer/",
    f"{SITE}/jeju-island-food-guide-7-unique-dishes-you-can-only-eat-on-koreas-tropical-island/",
    f"{SITE}/korean-convenience-store-food-ranking-top-20-must-try-items-at-cu-gs25-and-7-eleven/",
    f"{SITE}/soju-guide-for-beginners-how-to-drink-koreas-national-spirit-like-a-local/",
    f"{SITE}/busan-food-guide-8-dishes-you-can-only-find-in-koreas-coastal-city/",
    f"{SITE}/korean-temple-food-the-zen-buddhist-cuisine-you-never-knew-existed/",
    f"{SITE}/korean-fried-chicken-guide-why-kfc-means-something-different-in-korea/",
    f"{SITE}/jeonju-bibimbap-vs-seoul-bibimbap-whats-the-difference-and-where-to-eat/",
    f"{SITE}/gwangjang-market-food-guide-seouls-oldest-market-and-its-legendary-eats/",
    f"{SITE}/how-to-order-food-in-korean-25-essential-phrases-every-traveler-needs/",
    f"{SITE}/korean-bbq-etiquette-12-rules-every-first-timer-needs-to-know/",
    f"{SITE}/budgets-meals-in-korea-10-tv-featured-restaurants-where-you-can-eat-for-under-10/",
    f"{SITE}/the-ultimate-guide-to-korean-street-food-15-must-try-snacks-and-where-to-find-them/",
    f"{SITE}/korean-food-show-guide-what-is-2tv-%ec%83%9d%ec%83%9d%ec%a0%95%eb%b3%b4-and-why-every-foodie-should-watch-it/",
    f"{SITE}/top-10-must-try-korean-soups-for-winter-from-tv-show-kitchens-to-your-travel-list/",
    f"{SITE}/han-hye-jins-hongcheon-food-trip-buckwheat-noodles-mind-blowing-tofu-pine-nut-hotteok/",
    f"{SITE}/pohang-halmae-jip-70-year-old-3rd-generation-ox-head-soup-in-yeongcheon-market/",
    f"{SITE}/haengju-chueotang-comedian-kim-mi-ryeos-go-to-loach-soup-at-haengju-fortress/",
    f"{SITE}/imja-triple-style-fresh-monkfish-soup-with-free-liver-service-in-gangnam/",
    f"{SITE}/gukbo-1st-unlimited-korean-beef-noodle-soup-bossam-for-10-in-bucheon/",
    f"{SITE}/seomyeon-sondubu-jip-grandmas-handmade-tofu-set-meal-in-chuncheon/",
    f"{SITE}/jun-%ec%a4%80-mind-blowing-king-rib-seafood-stone-plate-jjajang-in-daegu/",
    f"{SITE}/yasanhaechon-singer-seol-woon-dos-favorite-fresh-cod-soup-in-yangpyeong/",
    f"{SITE}/world-bap-all-you-can-eat-korean-buffet-for-only-6-in-gwangju/",
    f"{SITE}/bangi-gullim-mandu-ttegul-giant-hand-rolled-dumpling-hot-pot-in-seoul-songpa-gu/",
    f"{SITE}/post-procedure-korean-skincare-what-korean-dermatologists-recommend-after-botox-lasers-peels/",
    f"{SITE}/korean-peptide-serums-the-science-behind-koreas-anti-aging-revolution/",
    f"{SITE}/the-complete-korean-skincare-routine-for-oily-skin-7-steps-that-actually-work/",
    f"{SITE}/korean-scalp-care-the-k-beauty-secret-to-thicker-healthier-hair/",
    f"{SITE}/best-korean-sunscreens-2026-dermatologist-approved-spf-for-every-skin-type/",
    f"{SITE}/pdrn-skincare-explained-why-salmon-dna-is-koreas-hottest-beauty-ingredient-in-2026/",
    f"{SITE}/medicube-age-r-review-2026-is-koreas-viral-at-home-beauty-device-worth-it/",
    f"{SITE}/cherry-blossom-season-in-korea-2026-the-complete-bloom-forecast-best-spots-and-travel-guide/",
    f"{SITE}/when-life-gives-you-tangerines-cast-complete-guide-to-every-actor-and-character-in-the-hit-k-drama/",
]

# Reuse existing IndexNow key from previous upload
INDEXNOW_KEY = "3ccd6adccb62a948dd2e5d80ca8d3c5a"

def ping_google():
    print("=" * 60)
    print("[1] Google Sitemap Ping")
    print("=" * 60)
    try:
        r = requests.get(f"https://www.google.com/ping?sitemap={SITEMAP}", timeout=15)
        print(f"  Status: {r.status_code}")
        print(f"  Note: Google deprecated this endpoint in 2023, but still returns 200")
    except Exception as e:
        print(f"  ERROR: {e}")

def ping_bing():
    print("\n" + "=" * 60)
    print("[2] Bing Sitemap Ping")
    print("=" * 60)
    try:
        r = requests.get(f"https://www.bing.com/ping?sitemap={SITEMAP}", timeout=15)
        print(f"  Status: {r.status_code}")
    except Exception as e:
        print(f"  ERROR: {e}")

def submit_indexnow():
    print("\n" + "=" * 60)
    print("[3] IndexNow API Submission (Bing/Yandex)")
    print(f"  Key: {INDEXNOW_KEY}")
    print(f"  URLs: {len(URLS)}")
    print("=" * 60)

    # First, ensure key file exists on site root via WordPress
    # Try uploading key file via WP plugin page (if IndexNow plugin installed)
    # or directly via REST API
    ensure_key_file()

    payload = {
        "host": "rhythmicaleskimo.com",
        "key": INDEXNOW_KEY,
        "keyLocation": f"{SITE}/{INDEXNOW_KEY}.txt",
        "urlList": URLS
    }

    try:
        r = requests.post(
            "https://api.indexnow.org/indexnow",
            json=payload,
            headers={"Content-Type": "application/json; charset=utf-8"},
            timeout=30
        )
        print(f"  Status: {r.status_code}")
        if r.status_code == 200:
            print("  Result: OK - URLs accepted")
        elif r.status_code == 202:
            print("  Result: Accepted - URLs queued for processing")
        elif r.status_code == 422:
            print("  Result: Unprocessable - key validation failed")
            print(f"  Response: {r.text[:300]}")
        else:
            print(f"  Response: {r.text[:300]}")
    except Exception as e:
        print(f"  ERROR: {e}")

def ensure_key_file():
    """Upload IndexNow key file to site root via WordPress"""
    print("  Ensuring key file exists on site...")
    try:
        # Check if key file already accessible
        check = requests.get(f"{SITE}/{INDEXNOW_KEY}.txt", timeout=10)
        if check.status_code == 200 and INDEXNOW_KEY in check.text:
            print(f"  Key file already accessible at {SITE}/{INDEXNOW_KEY}.txt")
            return True
        print(f"  Key file not found (status {check.status_code}), attempting upload...")
    except:
        print("  Could not check key file, attempting upload...")

    # Login to WordPress and upload via media API
    try:
        s = requests.Session()
        s.cookies.set("wordpress_test_cookie", "WP+Cookie+check")
        s.post(f"{SITE}/wp-login.php", data={
            "log": USER, "pwd": PASS, "wp-submit": "Log In",
            "redirect_to": "/wp-admin/", "testcookie": "1"
        }, allow_redirects=True)
        page = s.get(f"{SITE}/wp-admin/post-new.php").text
        m = re.search(r'"nonce":"([a-f0-9]+)"', page)
        if not m:
            print("  WARNING: Could not get nonce for key file upload")
            return False
        nonce = m.group(1)

        r = s.post(f"{SITE}/wp-json/wp/v2/media", headers={
            "X-WP-Nonce": nonce,
            "Content-Disposition": f'attachment; filename="{INDEXNOW_KEY}.txt"',
            "Content-Type": "text/plain",
        }, data=INDEXNOW_KEY.encode())

        if r.status_code == 201:
            url = r.json().get("source_url", "unknown")
            print(f"  Key file uploaded: {url}")
            print(f"  NOTE: File is in /wp-content/uploads/, not site root.")
            print(f"  For IndexNow to work, install 'IndexNow' WP plugin or")
            print(f"  manually place {INDEXNOW_KEY}.txt in site root via FTP/cPanel.")
            return True
        else:
            print(f"  Upload failed: {r.status_code}")
            # May already exist
            if "already been uploaded" in r.text or r.status_code == 500:
                print("  File may already exist in media library")
            return False
    except Exception as e:
        print(f"  Upload error: {e}")
        return False

def ping_yandex():
    print("\n" + "=" * 60)
    print("[4] Yandex Sitemap Ping")
    print("=" * 60)
    try:
        r = requests.get(
            f"https://blogs.yandex.ru/pings/?status=success&url={SITEMAP}",
            timeout=15
        )
        print(f"  Status: {r.status_code}")
    except Exception as e:
        print(f"  ERROR: {e}")
        # Try alternative Yandex endpoint
        try:
            print("  Trying alternative endpoint...")
            r2 = requests.get(
                f"https://webmaster.yandex.com/ping?sitemap={SITEMAP}",
                timeout=15
            )
            print(f"  Alt status: {r2.status_code}")
        except Exception as e2:
            print(f"  Alt ERROR: {e2}")

if __name__ == "__main__":
    print(f"Search Engine Ping & IndexNow Submission")
    print(f"Site: {SITE}")
    print(f"Sitemap: {SITEMAP}")
    print(f"Total URLs: {len(URLS)}")
    print()

    ping_google()
    ping_bing()
    submit_indexnow()
    ping_yandex()

    print("\n" + "=" * 60)
    print("DONE")
    print("=" * 60)
