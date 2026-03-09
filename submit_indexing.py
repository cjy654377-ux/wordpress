#!/usr/bin/env python3
"""Google Sitemap Ping + Bing IndexNow 일괄 제출"""
import requests, re, json, os, hashlib, sys

SITE = "https://rhythmicaleskimo.com"
REST = f"{SITE}/wp-json/wp/v2"
USER = "cjy654377@gmail.com"
PASS = "Dkflekd1!!"
BASE = os.path.dirname(os.path.abspath(__file__))


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
        print("ERROR: nonce not found")
        sys.exit(1)
    return s, {"X-WP-Nonce": m.group(1)}


def get_all_post_urls(s, h):
    urls = []
    pg = 1
    while True:
        r = s.get(f"{REST}/posts?per_page=100&page={pg}&status=publish", headers=h)
        if r.status_code != 200:
            break
        batch = r.json()
        if not batch:
            break
        for p in batch:
            urls.append(p["link"])
        pg += 1
    return urls


def ping_google():
    print("[Google] Sitemap ping...")
    url = f"https://www.google.com/ping?sitemap={SITE}/sitemap_index.xml"
    r = requests.get(url, timeout=15)
    if r.status_code == 200:
        print("  OK: Google notified")
    else:
        print(f"  FAIL: {r.status_code}")


def setup_indexnow_key():
    """Generate IndexNow key and save to site root via WP upload"""
    key = hashlib.md5(SITE.encode()).hexdigest()[:32]
    return key


def submit_indexnow(urls):
    key = setup_indexnow_key()
    print(f"\n[IndexNow] Submitting {len(urls)} URLs to Bing/Yandex...")
    print(f"  Key: {key}")

    # IndexNow API
    payload = {
        "host": "rhythmicaleskimo.com",
        "key": key,
        "keyLocation": f"{SITE}/{key}.txt",
        "urlList": urls
    }

    # Bing IndexNow
    try:
        r = requests.post("https://api.indexnow.org/indexnow",
                          json=payload, timeout=30,
                          headers={"Content-Type": "application/json"})
        print(f"  IndexNow response: {r.status_code}")
        if r.status_code in (200, 202):
            print("  OK: URLs submitted to Bing/Yandex")
        else:
            print(f"  Response: {r.text[:200]}")
    except Exception as e:
        print(f"  Error: {e}")

    # Note about key file
    print(f"\n  [!] IndexNow key file needed at: {SITE}/{key}.txt")
    print(f"      Content: {key}")
    print(f"      Upload this via WP Media or FTP")

    return key


def main():
    s, h = login()
    urls = get_all_post_urls(s, h)
    print(f"Found {len(urls)} published posts\n")

    # 1. Google ping
    ping_google()

    # 2. IndexNow (Bing/Yandex)
    key = submit_indexnow(urls)

    # 3. Save URL list for manual Search Console submission
    url_file = os.path.join(BASE, "all_urls.txt")
    with open(url_file, "w", encoding="utf-8") as f:
        for u in urls:
            f.write(u + "\n")
    print(f"\nAll URLs saved to: all_urls.txt ({len(urls)} URLs)")
    print("Use these for manual Google Search Console URL inspection")


if __name__ == "__main__":
    main()
