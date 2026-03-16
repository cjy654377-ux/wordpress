#!/usr/bin/env python3
"""Add internal links FROM existing posts TO 5 newly published posts."""

import requests, re, json, time

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
        "id": 1103,
        "title": "Biodance Bio-Collagen Mask Review",
        "url": "/biodance-bio-collagen-mask-review-why-this-3-sheet-mask-broke-tiktok-in-2026/",
        "category": "kbeauty",
        "source_ids": [76, 537, 357, 541, 547, 539, 545, 543, 182, 1063],
        "keywords": ["mask", "sheet mask", "collagen", "skincare routine", "skincare", "hydrat", "moisture", "glow", "skin barrier", "serum"],
        "anchor": "Biodance Bio-Collagen Mask review",
        "link_templates": [
            'For a budget-friendly option that delivers visible results, check out our <a href="{url}">Biodance Bio-Collagen Mask review</a>.',
            'Speaking of effective treatments, the <a href="{url}">Biodance Bio-Collagen Mask</a> has become a viral favorite for good reason.',
            'If you want an affordable collagen boost, the <a href="{url}">Biodance Bio-Collagen Mask</a> is worth trying.',
            'The <a href="{url}">Biodance Bio-Collagen Mask</a> is another excellent addition to any hydration-focused routine.',
            'For a TikTok-viral product that actually delivers, see our <a href="{url}">Biodance Bio-Collagen Mask review</a>.',
        ],
    },
    {
        "id": 1107,
        "title": "Korean Glass Hair 7-Step Routine",
        "url": "/korean-glass-hair-trend-2026-the-7-step-routine-behind-koreas-shiniest-hair/",
        "category": "kbeauty",
        "source_ids": [76, 537, 357, 541, 547, 539, 545, 543, 182, 1063],
        "keywords": ["hair", "scalp", "shine", "glossy", "beauty routine", "K-beauty trend", "beauty trend", "treatment", "salon"],
        "anchor": "Korean glass hair routine",
        "link_templates": [
            'The glass skin philosophy extends beyond your face — discover the <a href="{url}">Korean glass hair trend</a> that is taking over salons in 2026.',
            'If you love the glass skin look, you will want to explore the <a href="{url}">Korean glass hair routine</a> for equally stunning results.',
            'Korean beauty innovation goes beyond skincare — the <a href="{url}">glass hair trend</a> is the latest proof.',
            'For the complete K-beauty experience, pair your skincare with the viral <a href="{url}">Korean glass hair routine</a>.',
            'The pursuit of "glass" beauty now includes hair — see our guide to the <a href="{url}">Korean glass hair trend</a>.',
        ],
    },
    {
        "id": 1110,
        "title": "Climax K-Drama Review",
        "url": "/climax-%ed%81%b4%eb%9d%bc%ec%9d%b4%eb%a7%89%ec%8a%a4-k-drama-review-2026-cast-plot-why-its-the-most-talked-about-show-this-spring/",
        "category": "kdrama",
        "source_ids": [606, 464, 393, 1074, 1075],
        "keywords": ["drama", "thriller", "suspense", "binge", "watch", "series", "show", "K-drama", "Netflix", "streaming", "spring 2026"],
        "anchor": "Climax K-drama review",
        "link_templates": [
            'For another must-watch this spring, check out our <a href="{url}">Climax K-drama review</a> — it is the most talked-about show of the season.',
            'If you enjoy edge-of-your-seat storytelling, <a href="{url}">Climax</a> is another spring 2026 drama you should not miss.',
            'Looking for your next binge? Our <a href="{url}">Climax review</a> covers why this drama has everyone talking.',
            'Spring 2026 is stacked with great dramas — <a href="{url}">Climax</a> is leading the conversation.',
            'Do not miss <a href="{url}">Climax</a>, easily one of the most gripping K-dramas of spring 2026.',
        ],
    },
    {
        "id": 1117,
        "title": "Mad Concrete Dreams K-Drama Review",
        "url": "/mad-concrete-dreams-%eb%af%b8%ec%b9%9c-%ec%bd%98%ed%81%ac%eb%a6%ac%ed%8a%b8-k-drama-review-2026-cast-plot-episodes-why-its-the-years-most-intense-thriller/",
        "category": "kdrama",
        "source_ids": [606, 464, 393, 1074, 1075],
        "keywords": ["drama", "thriller", "intense", "crime", "watch", "series", "show", "K-drama", "gritty", "action"],
        "anchor": "Mad Concrete Dreams review",
        "link_templates": [
            'For fans of darker storylines, <a href="{url}">Mad Concrete Dreams</a> delivers the most intense thriller of 2026.',
            'If you crave raw intensity in your K-dramas, our <a href="{url}">Mad Concrete Dreams review</a> explains why this is the one to watch.',
            'The year\'s most intense K-drama thriller might be <a href="{url}">Mad Concrete Dreams</a> — read our full review.',
            'For something grittier, <a href="{url}">Mad Concrete Dreams</a> pushes K-drama storytelling to its limits.',
            'Thriller fans should also check out <a href="{url}">Mad Concrete Dreams</a>, 2026\'s most intense K-drama.',
        ],
    },
    {
        "id": 1120,
        "title": "Dujjonku Dubai Cookie",
        "url": "/dujjonku-koreas-viral-dubai-chocolate-cookie-taking-over-tiktok-where-to-buy-in-2026/",
        "category": "food",
        "source_ids": [44, 180, 53, 65, 74, 48, 57],
        "keywords": ["snack", "dessert", "sweet", "chocolate", "cookie", "treat", "food", "viral", "TikTok", "street food", "bakery", "pastry"],
        "anchor": "Dujjonku Dubai chocolate cookie",
        "link_templates": [
            'For the latest viral Korean snack sensation, do not miss the <a href="{url}">Dujjonku Dubai chocolate cookie</a> that has taken over TikTok.',
            'Speaking of must-try treats, the <a href="{url}">Dujjonku Dubai chocolate cookie</a> is Korea\'s hottest dessert trend right now.',
            'No Korean food adventure is complete without trying the viral <a href="{url}">Dujjonku Dubai chocolate cookie</a>.',
            'Add the <a href="{url}">Dujjonku Dubai chocolate cookie</a> to your must-eat list — it is the most viral Korean snack of 2026.',
            'If you have a sweet tooth, the <a href="{url}">Dujjonku Dubai cookie</a> craze is something you need to experience.',
        ],
    },
]

# Fetch all posts
print("\nFetching all posts...")
all_posts = []
page_num = 1
while True:
    resp = s.get(f"{REST}/posts", params={"per_page": 100, "page": page_num, "status": "publish"}, headers=h)
    if resp.status_code != 200:
        break
    batch = resp.json()
    if not batch:
        break
    all_posts.extend(batch)
    page_num += 1
print(f"Fetched {len(all_posts)} posts")

# Index posts by ID
posts_by_id = {p["id"]: p for p in all_posts}

# Track results
results = []
template_idx = {}  # track which template index to use per new post

def find_best_paragraph(content, keywords, target_url):
    """Find the best paragraph to insert a link after, based on keyword relevance."""
    # Already has link to this post?
    if target_url in content or target_url.replace("/", "&#047;") in content:
        return None, -1
    # Also check without trailing slash and URL-decoded
    url_check = target_url.rstrip("/")
    if url_check in content:
        return None, -1

    # Split into paragraphs (by </p> tags)
    # We look for </p> positions and score surrounding text
    parts = re.split(r'(</p>)', content)

    best_score = 0
    best_idx = -1

    for i in range(0, len(parts) - 1, 2):
        paragraph = parts[i]
        # Skip very short paragraphs, headings, lists, images
        text = re.sub(r'<[^>]+>', '', paragraph).strip()
        if len(text) < 80:
            continue
        # Skip if it's inside a heading or list
        if re.search(r'<h[1-6]', paragraph):
            continue
        # Skip first and last paragraphs
        para_index = i // 2
        total_paras = len(parts) // 2
        if para_index == 0 or para_index >= total_paras - 1:
            continue

        # Score by keyword matches
        lower_text = text.lower()
        score = sum(1 for kw in keywords if kw.lower() in lower_text)

        # Prefer paragraphs in the middle-to-later section
        position_ratio = para_index / max(total_paras, 1)
        if 0.3 <= position_ratio <= 0.8:
            score += 1

        if score > best_score:
            best_score = score
            best_idx = i

    if best_idx >= 0 and best_score >= 1:
        return parts, best_idx
    return None, -1


def insert_link(content, parts, best_idx, link_sentence):
    """Insert the link sentence after the best paragraph."""
    # Insert after the </p> tag
    close_tag_idx = best_idx + 1  # the </p> part
    parts[close_tag_idx] = parts[close_tag_idx] + f"\n<p>{link_sentence}</p>"
    return "".join(parts)


# Process each new post
for new_post in NEW_POSTS:
    target_url = new_post["url"]
    full_url = SITE + target_url
    keywords = new_post["keywords"]
    print(f"\n{'='*60}")
    print(f"Processing: {new_post['title']} (ID:{new_post['id']})")
    print(f"  Target URL: {target_url}")

    links_added = 0
    template_counter = 0

    for source_id in new_post["source_ids"]:
        if source_id not in posts_by_id:
            print(f"  SKIP ID:{source_id} — not found in published posts")
            continue

        post = posts_by_id[source_id]
        content = post["content"]["rendered"]

        # Fetch raw content for editing
        raw_resp = s.get(f"{REST}/posts/{source_id}", params={"context": "edit"}, headers=h)
        if raw_resp.status_code != 200:
            print(f"  SKIP ID:{source_id} — cannot fetch for edit (status {raw_resp.status_code})")
            continue
        raw_post = raw_resp.json()
        raw_content = raw_post["content"]["raw"]

        # Check if already linked
        if target_url in raw_content:
            print(f"  SKIP ID:{source_id} ({post['title']['rendered'][:40]}) — already has link")
            continue

        # Find best paragraph
        parts, best_idx = find_best_paragraph(raw_content, keywords, target_url)
        if parts is None or best_idx < 0:
            # Try with rendered content to verify
            if target_url in content:
                print(f"  SKIP ID:{source_id} ({post['title']['rendered'][:40]}) — already has link (rendered)")
                continue
            print(f"  SKIP ID:{source_id} ({post['title']['rendered'][:40]}) — no suitable paragraph found")
            continue

        # Pick a link template
        template = new_post["link_templates"][template_counter % len(new_post["link_templates"])]
        link_sentence = template.format(url=full_url)
        template_counter += 1

        # Insert link
        new_content = insert_link(raw_content, parts, best_idx, link_sentence)

        # Update post
        update_resp = s.post(f"{REST}/posts/{source_id}", headers=h, json={"content": new_content})
        if update_resp.status_code == 200:
            links_added += 1
            short_title = re.sub(r'<[^>]+>', '', post['title']['rendered'])[:50]
            print(f"  ADDED link in ID:{source_id} ({short_title})")
            results.append((source_id, short_title, new_post["id"], new_post["title"]))
        else:
            print(f"  FAIL ID:{source_id} — update status {update_resp.status_code}: {update_resp.text[:200]}")

        time.sleep(0.3)

    print(f"  => {links_added} links added for {new_post['title']}")

# Summary
print(f"\n{'='*60}")
print("SUMMARY")
print(f"{'='*60}")
print(f"Total links added: {len(results)}")
for src_id, src_title, tgt_id, tgt_title in results:
    print(f"  ID:{src_id} ({src_title}) --> ID:{tgt_id} ({tgt_title})")
