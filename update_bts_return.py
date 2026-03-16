import requests, re

SITE = "https://rhythmicaleskimo.com"
REST = f"{SITE}/wp-json/wp/v2"
POST_ID = 1188

s = requests.Session()
s.cookies.set("wordpress_test_cookie", "WP+Cookie+check")
s.post(f"{SITE}/wp-login.php", data={
    "log": "cjy654377@gmail.com",
    "pwd": "Dkflekd1!!",
    "wp-submit": "Log In",
    "redirect_to": "/wp-admin/",
    "testcookie": "1"
}, allow_redirects=True)

page = s.get(f"{SITE}/wp-admin/post-new.php").text
m = re.search(r'"nonce":"([a-f0-9]+)"', page)
nonce = m.group(1)
h = {"X-WP-Nonce": nonce}

with open("/Users/choijooyong/wordpress/article_bts_return.html", "r") as f:
    content = f.read()

resp = s.post(f"{REST}/posts/{POST_ID}", headers=h, json={"content": content})
print(f"Update status: {resp.status_code}")
if resp.status_code in (200, 201):
    print(f"URL: {resp.json()['link']}")
else:
    print(resp.text[:500])
