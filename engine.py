#!/usr/bin/env python3
"""WordPress publishing engine — reusable auth + template + JSON data."""
import requests, re, json, sys, os

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

def get_or_create_category(s, h, name, slug):
    cats = s.get(f"{REST}/categories?search={name}", headers=h).json()
    if cats and isinstance(cats, list) and len(cats) > 0:
        return cats[0]["id"]
    r = s.post(f"{REST}/categories", headers=h, json={"name": name, "slug": slug})
    return r.json()["id"] if r.status_code == 201 else 1

def get_or_create_tags(s, h, tag_names):
    ids = []
    for t in tag_names:
        ex = s.get(f"{REST}/tags?search={t}", headers=h).json()
        if ex and isinstance(ex, list) and len(ex) > 0:
            ids.append(ex[0]["id"])
        else:
            r = s.post(f"{REST}/tags", headers=h, json={"name": t})
            if r.status_code == 201:
                ids.append(r.json()["id"])
    return ids

def publish(s, h, post, template):
    cat_id = get_or_create_category(s, h, post["category"], post["category_slug"])
    html = template.replace("{CONTENT}", post["body"])
    data = {"title": post["title"], "content": html, "status": "publish", "categories": [cat_id]}
    r = s.post(f"{REST}/posts", headers=h, json=data)
    if r.status_code == 201:
        pid = r.json()["id"]
        url = r.json()["link"]
        tags = get_or_create_tags(s, h, post.get("tags", []))
        if tags:
            s.post(f"{REST}/posts/{pid}", headers=h, json={"tags": tags})
        print(f"  ✅ [{post['category']}] {post['title'][:50]}... → {url}")
        return True
    else:
        print(f"  ❌ {r.status_code}: {r.text[:150]}")
        return False

def ping_google():
    """Notify Google about sitemap update"""
    url = f"https://www.google.com/ping?sitemap={SITE}/sitemap_index.xml"
    try:
        r = requests.get(url, timeout=10)
        return r.status_code == 200
    except:
        return False


if __name__ == "__main__":
    data_file = sys.argv[1] if len(sys.argv) > 1 else "posts_data.json"
    base = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base, "template.html")) as f:
        template = f.read()
    with open(os.path.join(base, data_file)) as f:
        posts = json.load(f)
    s, h = login()
    ok = sum(publish(s, h, p, template) for p in posts)
    print(f"\nDone: {ok}/{len(posts)} published")
