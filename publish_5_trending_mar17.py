#!/usr/bin/env python3
"""Publish 5 trending posts — March 17, 2026."""
import requests, re, json, sys, os

SITE = "https://rhythmicaleskimo.com"
REST = f"{SITE}/wp-json/wp/v2"
BASE = os.path.dirname(os.path.abspath(__file__))

# Login
s = requests.Session()
s.cookies.set("wordpress_test_cookie", "WP+Cookie+check")
login = s.post(f"{SITE}/wp-login.php", data={
    "log": "cjy654377@gmail.com",
    "pwd": "Dkflekd1!!",
    "wp-submit": "Log In",
    "redirect_to": "/wp-admin/",
    "testcookie": "1"
}, allow_redirects=True)
print(f"Login: {login.status_code}")

page = s.get(f"{SITE}/wp-admin/post-new.php").text
m = re.search(r'"nonce":"([a-f0-9]+)"', page)
if not m:
    m = re.search(r'_wpnonce=([a-f0-9]+)', page)
if not m:
    print("ERROR: nonce not found"); sys.exit(1)
nonce = m.group(1)
h = {"X-WP-Nonce": nonce}
print(f"Nonce: {nonce}")

# Template
with open(os.path.join(BASE, "template.html")) as f:
    template = f.read()

def get_or_create_category(name, slug):
    cats = s.get(f"{REST}/categories?search={name}", headers=h).json()
    if cats and isinstance(cats, list):
        for c in cats:
            if c["slug"] == slug:
                return c["id"]
    r = s.post(f"{REST}/categories", headers=h, json={"name": name, "slug": slug})
    if r.status_code == 201:
        return r.json()["id"]
    # fallback: search again
    cats = s.get(f"{REST}/categories?slug={slug}", headers=h).json()
    return cats[0]["id"] if cats else 1

def get_or_create_tags(tag_names):
    ids = []
    for t in tag_names:
        ex = s.get(f"{REST}/tags", headers=h, params={"search": t, "per_page": 5}).json()
        found = False
        for tag in ex:
            if tag["name"].lower() == t.lower():
                ids.append(tag["id"])
                found = True
                break
        if not found:
            r = s.post(f"{REST}/tags", headers=h, json={"name": t})
            if r.status_code in (200, 201):
                ids.append(r.json()["id"])
    return ids

def upload_image(filepath, filename, alt_text):
    with open(filepath, "rb") as f:
        data = f.read()
    r = s.post(
        f"{REST}/media",
        headers={**h, "Content-Disposition": f'attachment; filename="{filename}"', "Content-Type": "image/png"},
        data=data,
        params={"alt_text": alt_text}
    )
    if r.status_code in (200, 201):
        img_id = r.json()["id"]
        print(f"  📷 Image uploaded: {filename} (ID: {img_id})")
        return img_id
    else:
        print(f"  ❌ Image upload failed: {r.status_code}")
        return None

def publish_post(post_info):
    print(f"\n--- Publishing: {post_info['title'][:60]}... ---")

    # Upload featured image
    img_id = upload_image(
        os.path.join(BASE, post_info["image_file"]),
        post_info["image_filename"],
        post_info["image_alt"]
    )

    # Read article HTML
    with open(os.path.join(BASE, post_info["article_file"])) as f:
        content = f.read()

    # Wrap in template
    html = template.replace("{CONTENT}", content)

    # Category
    cat_id = get_or_create_category(post_info["category"], post_info["category_slug"])

    # Tags
    tag_ids = get_or_create_tags(post_info["tags"])

    # Create post
    post_data = {
        "title": post_info["title"],
        "content": html,
        "status": "publish",
        "categories": [cat_id],
        "tags": tag_ids,
        "excerpt": post_info["excerpt"],
        "slug": post_info["slug"]
    }
    if img_id:
        post_data["featured_media"] = img_id

    r = s.post(f"{REST}/posts", headers=h, json=post_data)
    if r.status_code in (200, 201):
        post = r.json()
        print(f"  ✅ Published! ID: {post['id']}")
        print(f"  🔗 {post['link']}")
        # Save response
        with open(os.path.join(BASE, f"post_{post['id']}.json"), "w") as f:
            json.dump(post, f, indent=2, ensure_ascii=False)
        return True
    else:
        print(f"  ❌ Failed: {r.status_code} — {r.text[:200]}")
        return False


# ===== POST DEFINITIONS =====

posts = [
    {
        "title": "BLACKPINK DEADLINE Album Review: How the Comeback Shattered Every K-Pop Record in 2026",
        "slug": "blackpink-deadline-album-review-comeback-records-2026",
        "article_file": "article_blackpink_deadline.html",
        "image_file": "featured_blackpink_deadline.png",
        "image_filename": "blackpink-deadline-album-review-2026.png",
        "image_alt": "BLACKPINK DEADLINE Album Review 2026 - Record-Breaking Comeback",
        "category": "K-Pop & Entertainment",
        "category_slug": "k-pop-entertainment",
        "excerpt": "BLACKPINK's DEADLINE EP sold 1.46 million copies on day one, shattering K-pop girl group records. Deep dive into all 5 tracks, chart performance, and what makes this comeback historic.",
        "tags": ["BLACKPINK", "DEADLINE", "K-Pop Comeback", "GO", "YG Entertainment", "K-Pop 2026", "BLACKPINK Comeback"]
    },
    {
        "title": "Spicule Skincare: K-Beauty's $20 Microneedling Revolution That's Taking Over TikTok in 2026",
        "slug": "spicule-skincare-k-beauty-microneedling-revolution-2026",
        "article_file": "article_spicule_skincare.html",
        "image_file": "featured_spicule_skincare.png",
        "image_filename": "spicule-skincare-k-beauty-trend-2026.png",
        "image_alt": "Spicule Skincare K-Beauty Microneedling Alternative 2026",
        "category": "K-Beauty & Skincare",
        "category_slug": "k-beauty-skincare",
        "excerpt": "Spicule skincare searches are up 119% in 2026. These microscopic sponge-derived needles deliver microneedling results at a fraction of the cost. Complete guide to products, usage, and results.",
        "tags": ["K-Beauty", "Spicule Skincare", "Microneedling", "VT Reedle Shot", "Korean Skincare 2026", "Glass Skin", "Skin Barrier"]
    },
    {
        "title": "Still Shining (여전히 빛나는) K-Drama Review: Netflix's Most Visually Stunning Romance of 2026",
        "slug": "still-shining-k-drama-review-netflix-2026",
        "article_file": "article_still_shining.html",
        "image_file": "featured_still_shining.png",
        "image_filename": "still-shining-k-drama-review-2026.png",
        "image_alt": "Still Shining K-Drama Review 2026 - Park Jin Young Kim Min Ju Netflix",
        "category": "K-Drama Guide",
        "category_slug": "k-drama-guide",
        "excerpt": "Still Shining stars Park Jin Young and Kim Min Ju in a slow-burn romance about loss and reconnection. IMDB 8.1, NME 4 stars. Full review of Netflix's most visually arresting K-drama of 2026.",
        "tags": ["Still Shining", "K-Drama", "Netflix K-Drama", "Park Jin Young", "Kim Min Ju", "JTBC Drama", "K-Drama 2026"]
    },
    {
        "title": "Korean Convenience Store Food Guide 2026: 25 Must-Try Items Tourists Are Actually Buying",
        "slug": "korean-convenience-store-food-guide-2026-must-try",
        "article_file": "article_convenience_store_food.html",
        "image_file": "featured_convenience_store_food.png",
        "image_filename": "korean-convenience-store-food-guide-2026.png",
        "image_alt": "Korean Convenience Store Food Guide 2026 - CU GS25 Must Try Items",
        "category": "Korea Travel & Food",
        "category_slug": "korea-travel-food",
        "excerpt": "Foreign sales at Korean convenience stores jumped over 100% in 2026. From viral Dujjonku cookies to triangle kimbap, here are the 25 must-try items at CU, GS25, 7-Eleven, and Emart24.",
        "tags": ["Korean Food", "Convenience Store", "Korea Travel", "CU", "GS25", "Korean Snacks", "Seoul Food Guide"]
    },
    {
        "title": "ILLIT 'Press Start' Concert Review & MAMIHLAPINATAPAI: Everything We Know About Their April Comeback",
        "slug": "illit-press-start-concert-review-mamihlapinatapai-comeback-2026",
        "article_file": "article_illit_press_start.html",
        "image_file": "featured_illit_press_start.png",
        "image_filename": "illit-press-start-concert-mamihlapinatapai-2026.png",
        "image_alt": "ILLIT Press Start Concert Review and MAMIHLAPINATAPAI Comeback 2026",
        "category": "K-Pop & Entertainment",
        "category_slug": "k-pop-entertainment",
        "excerpt": "ILLIT's sold-out first concert 'Press Start' in Seoul was a 120-minute spectacle. Plus: everything about their upcoming album MAMIHLAPINATAPAI dropping April 30 with lead single 'It's Me'.",
        "tags": ["ILLIT", "Press Start", "MAMIHLAPINATAPAI", "K-Pop Concert", "HYBE", "K-Pop 2026", "ILLIT Concert"]
    }
]

# ===== PUBLISH ALL =====
print("=" * 60)
print("Publishing 5 Trending Posts — March 17, 2026")
print("=" * 60)

success = 0
for post in posts:
    if publish_post(post):
        success += 1

print(f"\n{'=' * 60}")
print(f"Result: {success}/{len(posts)} posts published successfully")
print("=" * 60)

# Ping Google
try:
    r = requests.get(f"https://www.google.com/ping?sitemap={SITE}/sitemap_index.xml", timeout=10)
    print(f"Google ping: {'✅' if r.status_code == 200 else '❌'}")
except:
    print("Google ping: ❌ (timeout)")
