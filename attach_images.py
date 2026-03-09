#!/usr/bin/env python3
"""Download images from Unsplash and set as featured images for all posts."""
import requests, re, json, sys, os, time

SITE = "https://rhythmicaleskimo.com"
REST = f"{SITE}/wp-json/wp/v2"
USER = "cjy654377@gmail.com"
PASS = "Dkflekd1!!"

# Post ID → search keyword mapping
SEARCH_TERMS = {
    80: "korean hangul writing",
    78: "kpop concert lightstick",
    76: "korean skincare products",
    74: "seoul alley restaurant night",
    72: "jeju island tangerine farm",
    69: "korean fried chicken beer",
    67: "jeju black pork",
    65: "korean convenience store food",
    63: "soju bottle korean",
    61: "busan seafood market",
    59: "korean temple food buddhist",
    57: "korean fried chicken crispy",
    55: "bibimbap korean rice bowl",
    53: "gwangjang market seoul food",
    51: "korean restaurant ordering",
    48: "korean bbq grill meat",
    46: "korean budget meal set",
    44: "korean street food tteokbokki",
    42: "korean tv food show",
    40: "korean soup winter hot",
    29: "buckwheat noodles makguksu",
    27: "korean ox bone soup",
    25: "korean spicy fish soup",
    23: "monkfish korean stew",
    21: "korean noodle soup kalguksu",
    19: "korean handmade tofu",
    17: "jjajangmyeon black bean noodle",
    15: "korean cod fish soup clear",
    13: "korean buffet banchan",
    11: "korean dumpling mandu",
}

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

def download_image(query):
    """Download from LoremFlickr (free, no API key needed)."""
    tags = query.replace(' ', ',')
    url = f"https://loremflickr.com/1200/630/{tags}"
    r = requests.get(url, allow_redirects=True, timeout=20)
    if r.status_code == 200 and len(r.content) > 10000:
        return r.content
    return None

def upload_to_wp(s, h, img_data, filename, title):
    """Upload image to WordPress media library."""
    r = s.post(
        f"{REST}/media",
        headers={**h, "Content-Disposition": f'attachment; filename="{filename}"'},
        files={"file": (filename, img_data, "image/jpeg")},
        data={"title": title, "alt_text": title}
    )
    if r.status_code == 201:
        return r.json()["id"]
    print(f"    Upload failed: {r.status_code}")
    return None

def main():
    s, h = login()
    print("Logged in. Starting image attachments...\n")

    ok = 0
    for post_id, query in SEARCH_TERMS.items():
        print(f"[{post_id}] query: {query}")

        img = download_image(query)
        if not img:
            print(f"  ⚠️ Download failed, trying fallback...")
            img = download_image(query.split()[0] + " korean food")
            if not img:
                print(f"  ❌ Skipped")
                continue

        fname = f"post-{post_id}-{query.replace(' ', '-')[:30]}.jpg"
        media_id = upload_to_wp(s, h, img, fname, query.title())
        if not media_id:
            continue

        r = s.post(f"{REST}/posts/{post_id}", headers=h, json={"featured_media": media_id})
        if r.status_code == 200:
            print(f"  ✅ Image set (media={media_id})")
            ok += 1
        else:
            print(f"  ❌ Failed to set: {r.status_code}")

        time.sleep(1)  # rate limit

    print(f"\nDone: {ok}/{len(SEARCH_TERMS)} images attached")

if __name__ == "__main__":
    main()
