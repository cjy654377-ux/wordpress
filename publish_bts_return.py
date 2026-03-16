import requests, re, json

SITE = "https://rhythmicaleskimo.com"
REST = f"{SITE}/wp-json/wp/v2"

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
print(f"Login status: {login.status_code}")

# Get nonce
page = s.get(f"{SITE}/wp-admin/post-new.php").text
m = re.search(r'"nonce":"([a-f0-9]+)"', page)
if not m:
    m = re.search(r'_wpnonce=([a-f0-9]+)', page)
if not m:
    print("ERROR: Could not find nonce")
    exit(1)
nonce = m.group(1)
h = {"X-WP-Nonce": nonce}
print(f"Nonce: {nonce}")

# Read article HTML
with open("/Users/choijooyong/wordpress/article_bts_return.html", "r") as f:
    content = f.read()

# K-Pop category ID = 96
KPOP_CAT = 96

# Upload featured image
img_path = "/Users/choijooyong/wordpress/featured_bts_return.png"
with open(img_path, "rb") as f:
    img_data = f.read()

upload = s.post(
    f"{REST}/media",
    headers={**h, "Content-Disposition": 'attachment; filename="bts-the-return-netflix-documentary-guide.png"', "Content-Type": "image/png"},
    data=img_data,
    params={"alt_text": "BTS The Return Netflix Documentary Guide - March 27 2026"}
)
print(f"Image upload: {upload.status_code}")
if upload.status_code not in (200, 201):
    print(upload.text[:500])
    exit(1)
img_id = upload.json()["id"]
print(f"Image ID: {img_id}")

# Create post
post_data = {
    "title": "BTS The Return: Netflix Documentary Guide [2026]",
    "content": content,
    "status": "publish",
    "categories": [KPOP_CAT],
    "featured_media": img_id,
    "excerpt": "BTS: The Return drops on Netflix March 27, 2026. This feature-length documentary by Bao Nguyen captures the band's reunion after military service and the making of ARIRANG.",
    "tags": [],
    "slug": "bts-the-return-netflix-documentary-guide-march-2026-what-to-expect-arirang"
}

# Create/find tags
tag_names = ["BTS", "Netflix", "BTS The Return", "ARIRANG", "K-Pop Documentary", "BTS Documentary", "BTS Comeback 2026"]
tag_ids = []
for tag_name in tag_names:
    # Search existing
    existing = s.get(f"{REST}/tags", headers=h, params={"search": tag_name, "per_page": 5}).json()
    found = False
    for t in existing:
        if t["name"].lower() == tag_name.lower():
            tag_ids.append(t["id"])
            found = True
            break
    if not found:
        r = s.post(f"{REST}/tags", headers=h, json={"name": tag_name})
        if r.status_code in (200, 201):
            tag_ids.append(r.json()["id"])
            print(f"Created tag: {tag_name}")
        else:
            print(f"Tag error for '{tag_name}': {r.status_code}")

post_data["tags"] = tag_ids
print(f"Tags: {tag_ids}")

# Publish
resp = s.post(f"{REST}/posts", headers=h, json=post_data)
print(f"Publish status: {resp.status_code}")

if resp.status_code in (200, 201):
    post = resp.json()
    print(f"\nPublished successfully!")
    print(f"Post ID: {post['id']}")
    print(f"URL: {post['link']}")
else:
    print(f"Error: {resp.text[:1000]}")
