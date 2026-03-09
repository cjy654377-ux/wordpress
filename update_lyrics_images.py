#!/usr/bin/env python3
"""BTS 가사 시리즈 대표이미지 교체 스크립트"""
import requests, re, os, sys

SITE = "https://rhythmicaleskimo.com"
REST = f"{SITE}/wp-json/wp/v2"
USER = "cjy654377@gmail.com"
PASS = "Dkflekd1!!"
BASE = os.path.dirname(os.path.abspath(__file__))

SLUG_IMAGE_MAP = {
    "spring-day": "featured_spring_day.png",
    "black-swan": "featured_black_swan.png",
    "fake-love": "featured_fake_love.png",
    "blood-sweat": "featured_bst.png",
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
        print("ERROR: nonce not found")
        sys.exit(1)
    return s, {"X-WP-Nonce": m.group(1)}


def get_all_posts(s, h):
    posts = []
    pg = 1
    while True:
        r = s.get(f"{REST}/posts?per_page=100&page={pg}&status=publish", headers=h)
        if r.status_code != 200:
            break
        batch = r.json()
        if not batch:
            break
        posts.extend(batch)
        pg += 1
    return posts


def upload_image(s, h, filepath, title):
    with open(filepath, "rb") as f:
        data = f.read()
    fname = os.path.basename(filepath)
    r = s.post(f"{REST}/media", headers={
        **h,
        "Content-Disposition": f'attachment; filename="{fname}"',
        "Content-Type": "image/png",
    }, data=data)
    if r.status_code == 201:
        mid = r.json()["id"]
        print(f"  Uploaded: {fname} -> media ID {mid}")
        return mid
    else:
        print(f"  Upload failed: {r.status_code} {r.text[:100]}")
        return None


def main():
    s, h = login()
    posts = get_all_posts(s, h)
    print(f"Total posts: {len(posts)}")

    for post in posts:
        slug = post["slug"]
        for keyword, image_file in SLUG_IMAGE_MAP.items():
            if keyword in slug:
                print(f"\nPost: {post['title']['rendered'][:60]}")
                print(f"  Slug: {slug}")
                filepath = os.path.join(BASE, image_file)
                mid = upload_image(s, h, filepath, post["title"]["rendered"])
                if mid:
                    r = s.post(f"{REST}/posts/{post['id']}", headers=h,
                               json={"featured_media": mid})
                    if r.status_code == 200:
                        print(f"  Featured image updated!")
                    else:
                        print(f"  Update failed: {r.status_code}")
                break


if __name__ == "__main__":
    main()
