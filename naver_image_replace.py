#!/usr/bin/env python3
"""Replace featured images using Naver image search."""
import requests, re, json, time, os

SITE = "https://rhythmicaleskimo.com"
REST = f"{SITE}/wp-json/wp/v2"
USER = "cjy654377@gmail.com"
PASS = "Dkflekd1!!"

# Post ID → Naver search keyword (Korean)
POSTS = {
    11: "왕만두전골",
    13: "한식뷔페",
    15: "대구탕",
    17: "해물짜장 돌판",
    19: "순두부정식",
    23: "아귀탕",
    25: "추어탕",
    27: "소머리국밥",
    29: "메밀국수 홍천",
    40: "한국 겨울 국물요리",
    44: "한국 길거리음식 포장마차",
    46: "생생정보통 맛집",
    48: "한국 고기구이 삼겹살",
    53: "광장시장 먹거리",
    55: "전주비빔밥",
    59: "사찰음식",
    63: "소주 건배",
    65: "한국 편의점 음식",
    74: "서울 골목식당",
    76: "한국 스킨케어 화장품",
    78: "케이팝 콘서트",
    80: "한국드라마 촬영지",
    178: "서울 카페 인테리어",
    180: "명동 길거리음식",
    182: "올리브영 매장",
    184: "하이브 인사이트 방문",
    186: "한글 자음모음",
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
    return s, {"X-WP-Nonce": m.group(1)}

def search_naver_image(query):
    """Search Naver images and return the first large image URL."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://search.naver.com/"
    }
    url = f"https://search.naver.com/search.naver?where=image&sm=tab_jum&query={requests.utils.quote(query)}"
    r = requests.get(url, headers=headers)

    # Extract image URLs from JSON data in page
    # Naver embeds image data in script tags
    matches = re.findall(r'"originalUrl":"(https?://[^"]+)"', r.text)
    if not matches:
        # Try thumbnail pattern
        matches = re.findall(r'"source":"(https?://[^"]+)"', r.text)
    if not matches:
        matches = re.findall(r'"url":"(https?://[^"]+\.(?:jpg|jpeg|png|webp))"', r.text)

    # Filter for good image URLs
    for img_url in matches[:10]:
        if any(x in img_url for x in ['.jpg', '.jpeg', '.png', '.webp']):
            if 'thumb' not in img_url.lower() and 'icon' not in img_url.lower():
                return img_url

    return matches[0] if matches else None

def download_image(url):
    """Download image from URL."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Referer": "https://search.naver.com/"
    }
    try:
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code == 200 and len(r.content) > 5000:
            return r.content
    except:
        pass
    return None

def upload_and_set(s, h, post_id, img_data, query):
    """Upload image to WordPress and set as featured."""
    fname = f"post-{post_id}-featured.jpg"

    r = s.post(f"{REST}/media", headers={
        **h,
        "Content-Disposition": f'attachment; filename="{fname}"',
        "Content-Type": "image/jpeg"
    }, data=img_data)

    if r.status_code == 201:
        mid = r.json()["id"]
        s.post(f"{REST}/media/{mid}", headers=h, json={"alt_text": query})
        r2 = s.post(f"{REST}/posts/{post_id}", headers=h, json={"featured_media": mid})
        return r2.status_code == 200
    return False

s, h = login()
success = 0
fail = 0

for post_id, query in POSTS.items():
    img_url = search_naver_image(query)
    if not img_url:
        print(f"  ❌ ID={post_id} '{query}': no image found")
        fail += 1
        continue

    img_data = download_image(img_url)
    if not img_data:
        print(f"  ❌ ID={post_id} '{query}': download failed")
        fail += 1
        continue

    ok = upload_and_set(s, h, post_id, img_data, query)
    if ok:
        print(f"  ✅ ID={post_id} '{query}' → {len(img_data)} bytes")
        success += 1
    else:
        print(f"  ❌ ID={post_id} '{query}': upload failed")
        fail += 1

    time.sleep(0.5)

print(f"\nDone: {success} replaced, {fail} failed")
