#!/usr/bin/env python3
import requests, re
SITE='https://rhythmicaleskimo.com'
REST=f'{SITE}/wp-json/wp/v2'
s=requests.Session()
s.cookies.set('wordpress_test_cookie','WP+Cookie+check')
s.post(f'{SITE}/wp-login.php',data={
    'log':'cjy654377@gmail.com','pwd':'Dkflekd1!!',
    'wp-submit':'Log In','redirect_to':'/wp-admin/','testcookie':'1'
},allow_redirects=True)
page=s.get(f'{SITE}/wp-admin/post-new.php').text
m=re.search(r'"nonce":"([a-f0-9]+)"',page)
h={'X-WP-Nonce':m.group(1)}
posts=[]
pg=1
while pg<5:
    r=s.get(f'{REST}/posts?per_page=100&page={pg}&_fields=id,title,slug',headers=h)
    if r.status_code!=200:
        break
    batch=r.json()
    if not batch:
        break
    posts+=batch
    pg+=1

# Check overlap with proposed topics
keywords = {
    'BTS ARIRANG': ['arirang','bts album'],
    'Cherry Blossom': ['cherry blossom','벚꽃','sakura'],
    'Biodance': ['biodance','bio-collagen'],
    'Mad Concrete Dreams': ['mad concrete','미친 콘크리트'],
    'Glass Hair': ['glass hair'],
}

print(f"=== 전체 {len(posts)}개 포스트 ===\n")
for p in posts:
    slug = p['slug']
    title = p['title']['rendered'].lower()
    print(f"  ID:{p['id']} {slug[:70]}")

print(f"\n=== 중복 체크 ===")
for topic, kws in keywords.items():
    matches = []
    for p in posts:
        slug = p['slug'].lower()
        title = p['title']['rendered'].lower()
        for kw in kws:
            if kw in slug or kw in title:
                matches.append(f"  ID:{p['id']} {p['slug'][:60]}")
                break
    if matches:
        print(f"\n⚠️ {topic} — 겹침 발견:")
        for m in matches:
            print(m)
    else:
        print(f"\n✅ {topic} — 겹침 없음")
