#!/usr/bin/env python3
"""Add internal links FROM existing posts TO 5 newly published posts (batch 2)."""

import requests, re, json, time, random

SITE = "https://rhythmicaleskimo.com"
REST = f"{SITE}/wp-json/wp/v2"

# Login
s = requests.Session()
s.cookies.set("wordpress_test_cookie", "WP+Cookie+check")
s.post(f"{SITE}/wp-login.php", data={
    "log": "cjy654377@gmail.com", "pwd": "Dkflekd1!!",
    "wp-submit": "Log In", "redirect_to": "/wp-admin/", "testcookie": "1"
}, allow_redirects=True)
page = s.get(f"{SITE}/wp-admin/post-new.php").text
m = re.search(r'"nonce":"([a-f0-9]+)"', page)
h = {"X-WP-Nonce": m.group(1)}
print(f"Logged in, nonce: {h['X-WP-Nonce']}")

# New posts — targets for internal links
NEW_POSTS = [
    {
        "id": 1177,
        "title": "Dr. Melaxin Multi Balm",
        "slug": "dr-melaxin-multi-balm-review-tiktoks-botox-in-a-stick-2026",
        "url": "/dr-melaxin-multi-balm-review-tiktoks-botox-in-a-stick-2026/",
        "category": "kbeauty",
        "source_ids": [76, 537, 357, 541, 547, 539, 545, 543, 182, 1063, 1103, 1107],
        "keywords": ["balm", "wrinkle", "anti-aging", "peptide", "lifting", "firming", "botox", "skincare", "moistur", "cream", "serum", "collagen"],
        "link_templates": [
            'For a travel-friendly anti-aging solution, check out the viral <a href="{url}">Dr. Melaxin Multi Balm</a> that TikTok calls "botox in a stick."',
            'The <a href="{url}">Dr. Melaxin Multi Balm</a> is another peptide-packed product making waves in the K-beauty world.',
            'If you prefer a stick-type format, the <a href="{url}">Dr. Melaxin Multi Balm review</a> explains why this product went viral.',
            'Speaking of innovative formats, the <a href="{url}">Dr. Melaxin Multi Balm</a> delivers anti-aging peptides in a convenient stick.',
        ],
    },
    {
        "id": 1178,
        "title": "Can This Love Be Translated?",
        "slug": "can-this-love-be-translated-k-drama-review-2026",
        "url": "/can-this-love-be-translated-k-drama-review-2026/",
        "category": "kdrama",
        "source_ids": [606, 464, 393, 1074, 1075, 1110, 1117],
        "keywords": ["drama", "romance", "love", "Netflix", "K-drama", "series", "watch", "episode", "cast", "show"],
        "link_templates": [
            'For another heartfelt romance, <a href="{url}">Can This Love Be Translated?</a> explores what happens when language barriers meet genuine connection.',
            'If you enjoy cross-cultural love stories, <a href="{url}">Can This Love Be Translated?</a> is a must-watch this spring.',
            'The new K-drama <a href="{url}">Can This Love Be Translated?</a> adds a fresh twist to the romance genre with its language-barrier premise.',
            'Romance fans should also check out <a href="{url}">Can This Love Be Translated?</a>, one of spring 2026\'s standout K-dramas.',
        ],
    },
    {
        "id": 1181,
        "title": "Undercover Miss Hong",
        "slug": "undercover-miss-hong-netflix-biggest-k-drama-hit-2026-review",
        "url": "/undercover-miss-hong-netflix-biggest-k-drama-hit-2026-review/",
        "category": "kdrama",
        "source_ids": [606, 464, 393, 1074, 1075, 1110, 1117, 1178],
        "keywords": ["drama", "Netflix", "K-drama", "series", "action", "thriller", "watch", "episode", "show", "hit"],
        "link_templates": [
            'Meanwhile, <a href="{url}">Undercover Miss Hong</a> has become Netflix\'s biggest K-drama hit of 2026 with its genre-bending action comedy.',
            'For something with more action, <a href="{url}">Undercover Miss Hong</a> is breaking Netflix records worldwide.',
            'If you want a K-drama that mixes action with comedy, <a href="{url}">Undercover Miss Hong</a> delivers on every front.',
            'Netflix\'s record-breaking <a href="{url}">Undercover Miss Hong</a> proves K-dramas can dominate the global action-comedy genre.',
        ],
    },
    {
        "id": 1184,
        "title": "Spring Cabbage Bibimbap",
        "slug": "spring-cabbage-bibimbap-koreas-viral-recipe-2026",
        "url": "/spring-cabbage-bibimbap-koreas-viral-recipe-2026/",
        "category": "food",
        "source_ids": [44, 180, 53, 65, 74, 48, 57, 55, 61, 67, 69, 1120],
        "keywords": ["bibimbap", "rice", "vegetable", "seasonal", "spring", "recipe", "dish", "food", "Korean cuisine", "cook", "ingredient", "market"],
        "link_templates": [
            'For a seasonal twist on a classic, try the viral <a href="{url}">spring cabbage bibimbap</a> that has taken Korean social media by storm.',
            'If you love Korean rice dishes, the <a href="{url}">spring cabbage bibimbap</a> is 2026\'s most-searched recipe for good reason.',
            'Speaking of seasonal specialties, <a href="{url}">spring cabbage bibimbap</a> has become Korea\'s viral comfort food this March.',
            'The humble bibimbap gets a seasonal upgrade — see why <a href="{url}">spring cabbage bibimbap</a> is trending across Korea.',
        ],
    },
    {
        "id": 1188,
        "title": "BTS The Return Documentary",
        "slug": "bts-the-return-netflix-documentary-guide-march-2026-what-to-expect-arirang",
        "url": "/bts-the-return-netflix-documentary-guide-march-2026-what-to-expect-arirang/",
        "category": "kpop",
        "source_ids": [409, 411, 413, 404, 394, 361, 566, 1067, 1069],
        "keywords": ["BTS", "documentary", "Netflix", "reunion", "comeback", "return", "ARMY", "Arirang", "military", "concert", "album"],
        "link_templates": [
            'For the full story behind their comeback, the <a href="{url}">BTS: The Return Netflix documentary</a> captures every emotional moment of their reunion.',
            'ARMY can relive the reunion journey through the <a href="{url}">BTS: The Return documentary on Netflix</a>.',
            'The <a href="{url}">BTS: The Return documentary</a> provides the definitive behind-the-scenes look at their historic comeback.',
            'To understand the full emotional weight of this era, watch the <a href="{url}">BTS: The Return Netflix documentary</a>.',
        ],
    },
]

# Track which source posts already got a link to avoid duplicates
used_sources = {}  # source_id -> set of target_ids already linked

results = []

for target in NEW_POSTS:
    full_url = SITE + target["url"]
    print(f"\n{'='*60}")
    print(f"Target: {target['title']} (ID:{target['id']})")
    print(f"Sources: {target['source_ids']}")

    added = 0

    for src_id in target["source_ids"]:
        # Skip if this source already got a new-post link in this batch
        if src_id in used_sources and len(used_sources[src_id]) >= 1:
            print(f"  ID:{src_id} — SKIP (already got a link to {used_sources[src_id]})")
            continue

        # Fetch source post
        try:
            r = s.get(f"{REST}/posts/{src_id}?context=edit", headers=h)
            if r.status_code != 200:
                print(f"  ID:{src_id} — SKIP (HTTP {r.status_code})")
                continue
            post = r.json()
            content = post["content"]["raw"]
        except Exception as e:
            print(f"  ID:{src_id} — ERROR fetching: {e}")
            continue

        # Check if link already exists
        if target["slug"] in content:
            print(f"  ID:{src_id} — SKIP (link already exists)")
            continue

        # Find a relevant paragraph to insert after
        paragraphs = re.findall(r'(<p[^>]*>.*?</p>)', content, re.DOTALL)
        if not paragraphs:
            print(f"  ID:{src_id} — SKIP (no paragraphs found)")
            continue

        # Score paragraphs by keyword relevance
        best_score = 0
        best_idx = -1
        for i, para in enumerate(paragraphs):
            # Skip very short paragraphs, FAQ sections, or paragraphs with existing links to new posts
            if len(para) < 80:
                continue
            # Avoid the first 2 and last 2 paragraphs
            if i < 2 or i >= len(paragraphs) - 2:
                continue

            score = 0
            para_lower = para.lower()
            for kw in target["keywords"]:
                if kw.lower() in para_lower:
                    score += 1

            if score > best_score:
                best_score = score
                best_idx = i

        if best_score == 0 or best_idx == -1:
            # Fallback: pick a paragraph in the middle third
            middle_start = len(paragraphs) // 3
            middle_end = 2 * len(paragraphs) // 3
            candidates = [i for i in range(middle_start, middle_end) if len(paragraphs[i]) > 80]
            if candidates:
                best_idx = candidates[len(candidates) // 2]
            else:
                print(f"  ID:{src_id} — SKIP (no suitable paragraph)")
                continue

        # Choose a link template
        template_idx = added % len(target["link_templates"])
        link_sentence = target["link_templates"][template_idx].format(url=full_url)
        link_para = f"\n\n<p>{link_sentence}</p>"

        # Insert after the best paragraph
        insert_after = paragraphs[best_idx]
        # Only replace first occurrence to avoid issues
        new_content = content.replace(insert_after, insert_after + link_para, 1)

        if new_content == content:
            print(f"  ID:{src_id} — SKIP (replacement failed)")
            continue

        # Update the post
        try:
            r2 = s.post(f"{REST}/posts/{src_id}", headers=h, json={"content": new_content})
            if r2.status_code == 200:
                added += 1
                used_sources.setdefault(src_id, set()).add(target["id"])
                src_title = post.get("title", {}).get("raw", f"ID:{src_id}")[:50]
                print(f"  ID:{src_id} ({src_title}) — LINKED (kw score: {best_score})")
                results.append({
                    "source_id": src_id,
                    "source_title": src_title,
                    "target_id": target["id"],
                    "target_title": target["title"],
                })
            else:
                print(f"  ID:{src_id} — UPDATE FAILED (HTTP {r2.status_code})")
        except Exception as e:
            print(f"  ID:{src_id} — ERROR updating: {e}")

        time.sleep(0.5)  # Rate limiting

print(f"\n{'='*60}")
print(f"SUMMARY: Added {len(results)} internal links total")
print(f"{'='*60}")
for r in results:
    print(f"  {r['source_title'][:40]:40s} → {r['target_title']}")
