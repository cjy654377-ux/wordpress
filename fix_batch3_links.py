#!/usr/bin/env python3
"""
Batch 3: Audit and fix internal links for the 11 newest posts.
1. Audit incoming links to each of the 11 newest posts from all other posts
2. Audit outgoing links from each of the 11 newest posts
3. Add incoming links where count < 3
4. Add outgoing links where count < 5
"""

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

# ── Step 1: Fetch ALL posts ──
print("\n=== Fetching all posts ===")
all_posts = []
page_num = 1
while True:
    r = s.get(f"{REST}/posts?context=edit&per_page=50&page={page_num}&status=publish", headers=h)
    if r.status_code != 200:
        break
    batch = r.json()
    if not batch:
        break
    all_posts.extend(batch)
    page_num += 1
    time.sleep(0.3)

print(f"Fetched {len(all_posts)} posts total")

# Build lookup
posts_by_id = {}
for p in all_posts:
    pid = p["id"]
    posts_by_id[pid] = {
        "id": pid,
        "title": p["title"]["raw"],
        "slug": p["slug"],
        "link": p["link"],
        "content": p["content"]["raw"],
        "categories": p.get("categories", []),
    }

# Identify the 11 newest posts (highest IDs)
sorted_ids = sorted(posts_by_id.keys(), reverse=True)
newest_11_ids = sorted_ids[:11]
newest_11_ids.sort()

print(f"\nNewest 11 post IDs: {newest_11_ids}")
for pid in newest_11_ids:
    print(f"  ID:{pid} — {posts_by_id[pid]['title'][:70]}")

# ── Step 2: Audit incoming links ──
print("\n=== AUDIT: Incoming links to newest 11 posts ===")

# For each of the 11 newest, count how many OTHER posts link to it
incoming_counts = {pid: [] for pid in newest_11_ids}  # pid -> list of source_ids

for pid in newest_11_ids:
    target_slug = posts_by_id[pid]["slug"]
    target_link = posts_by_id[pid]["link"]
    # Check all other posts' content for links to this post
    for other_id, other in posts_by_id.items():
        if other_id == pid:
            continue
        content = other["content"]
        # Check for slug in href
        if target_slug in content:
            # Verify it's actually in an <a href>
            if re.search(r'href="[^"]*' + re.escape(target_slug) + r'[^"]*"', content):
                incoming_counts[pid].append(other_id)

print(f"\n{'ID':<8} {'Incoming':<10} {'Title'}")
print("-" * 80)
for pid in newest_11_ids:
    count = len(incoming_counts[pid])
    marker = " *** NEEDS MORE" if count < 3 else ""
    print(f"{pid:<8} {count:<10} {posts_by_id[pid]['title'][:55]}{marker}")

# ── Step 3: Audit outgoing links ──
print("\n=== AUDIT: Outgoing internal links from newest 11 posts ===")

outgoing_counts = {pid: [] for pid in newest_11_ids}  # pid -> list of target_ids

for pid in newest_11_ids:
    content = posts_by_id[pid]["content"]
    # Find all internal links
    hrefs = re.findall(r'href="(https?://rhythmicaleskimo\.com/[^"]+)"', content)
    for href in hrefs:
        # Match to a post
        for other_id, other in posts_by_id.items():
            if other_id == pid:
                continue
            if other["slug"] in href:
                if other_id not in outgoing_counts[pid]:
                    outgoing_counts[pid].append(other_id)
                break

print(f"\n{'ID':<8} {'Outgoing':<10} {'Title'}")
print("-" * 80)
for pid in newest_11_ids:
    count = len(outgoing_counts[pid])
    marker = " *** NEEDS MORE" if count < 5 else ""
    print(f"{pid:<8} {count:<10} {posts_by_id[pid]['title'][:55]}{marker}")

# ── Step 4: Category mapping for relevance ──
# Category IDs (from memory): Korea Travel & Food(various), K-Beauty(various), K-Pop(various), K-Drama(various), Korean Language(various)
# We'll use category overlap + keyword matching for relevance

def get_category_label(cats):
    """Rough category label based on category IDs."""
    # We don't know exact IDs, so we'll use content-based matching
    return cats

def find_keywords_in_post(post_data):
    """Extract rough topic keywords from title and content."""
    title = post_data["title"].lower()
    content_lower = post_data["content"][:2000].lower()
    combined = title + " " + content_lower

    topics = set()
    if any(w in combined for w in ["skincare", "beauty", "serum", "moistur", "sunscreen", "spf", "k-beauty", "cleanser", "toner", "cream", "pdrn", "peptide", "collagen", "medicube", "melaxin"]):
        topics.add("kbeauty")
    if any(w in combined for w in ["bts", "k-pop", "kpop", "army", "idol", "album", "concert", "arirang", "blackpink", "aespa"]):
        topics.add("kpop")
    if any(w in combined for w in ["k-drama", "kdrama", "netflix", "drama series", "episode", "k-drama review"]):
        topics.add("kdrama")
    if any(w in combined for w in ["restaurant", "food", "dish", "bibimbap", "kimchi", "market", "street food", "recipe", "cook", "busan food", "seoul food", "tteok"]):
        topics.add("food")
    if any(w in combined for w in ["travel", "airport", "hotel", "itinerary", "temple", "palace", "jeju", "gyeongju", "neighborhood", "alley"]):
        topics.add("travel")
    if any(w in combined for w in ["hangul", "korean language", "learn korean", "phrase", "vocabulary"]):
        topics.add("language")
    if any(w in combined for w in ["finance", "insurance", "invest", "tax", "bank", "credit"]):
        topics.add("finance")
    return topics

# Pre-compute topics for all posts
post_topics = {}
for pid, pdata in posts_by_id.items():
    post_topics[pid] = find_keywords_in_post(pdata)

# ── Step 5: Add INCOMING links where count < 3 ──
print("\n=== ADDING INCOMING LINKS (target < 3 incoming) ===")

results_incoming = []
updated_posts_cache = {}  # Track content updates to avoid conflicts

def get_content(pid):
    """Get latest content, considering in-session updates."""
    if pid in updated_posts_cache:
        return updated_posts_cache[pid]
    return posts_by_id[pid]["content"]

def set_content(pid, content):
    updated_posts_cache[pid] = content

# Link templates by category
INCOMING_TEMPLATES = {
    "kbeauty": [
        'For another trending K-beauty product worth exploring, check out our guide to <a href="{url}">{title}</a>.',
        'If you\'re building a comprehensive K-beauty routine, <a href="{url}">{title_short}</a> is worth adding to your radar.',
        'Korean skincare enthusiasts should also read about <a href="{url}">{title_short}</a> for more product insights.',
        'Speaking of innovative Korean beauty products, <a href="{url}">{title_short}</a> has been generating serious buzz.',
    ],
    "kpop": [
        'For more on this era, read our coverage of <a href="{url}">{title_short}</a>.',
        'K-pop fans should also check out <a href="{url}">{title_short}</a> for the latest updates.',
        'To dive deeper into K-pop culture, our article on <a href="{url}">{title_short}</a> covers everything you need to know.',
        'ARMY and K-pop fans will also want to read about <a href="{url}">{title_short}</a>.',
    ],
    "kdrama": [
        'K-drama fans should also check out our review of <a href="{url}">{title_short}</a>.',
        'If you\'re looking for your next binge, <a href="{url}">{title_short}</a> is a strong contender.',
        'For another compelling series, read our take on <a href="{url}">{title_short}</a>.',
        'Speaking of must-watch K-dramas, <a href="{url}">{title_short}</a> has been capturing viewers worldwide.',
    ],
    "food": [
        'Food lovers should also explore our guide to <a href="{url}">{title_short}</a>.',
        'For more Korean culinary adventures, check out <a href="{url}">{title_short}</a>.',
        'If Korean cuisine fascinates you, our article on <a href="{url}">{title_short}</a> is a must-read.',
        'Speaking of delicious Korean dishes, <a href="{url}">{title_short}</a> is trending for good reason.',
    ],
    "travel": [
        'Travelers should also read our guide to <a href="{url}">{title_short}</a>.',
        'Planning a Korea trip? Don\'t miss our article on <a href="{url}">{title_short}</a>.',
        'For more destination ideas, check out <a href="{url}">{title_short}</a>.',
    ],
    "language": [
        'Language learners will also benefit from <a href="{url}">{title_short}</a>.',
        'To boost your Korean skills further, check out <a href="{url}">{title_short}</a>.',
    ],
    "default": [
        'You might also enjoy our article on <a href="{url}">{title_short}</a>.',
        'For related reading, check out <a href="{url}">{title_short}</a>.',
        'Readers interested in Korean culture should also explore <a href="{url}">{title_short}</a>.',
    ],
}

def make_title_short(title):
    """Shorten title for anchor text — remove year, site-specific suffixes."""
    short = re.sub(r'\s*[\(\[]\d{4}[\)\]]', '', title)
    short = re.sub(r'\s*\d{4}$', '', short)
    # If still too long, take first part
    if len(short) > 60:
        # Try to cut at a natural break
        for sep in [': ', ' — ', ' - ', ' | ']:
            if sep in short:
                short = short.split(sep)[0]
                break
    if len(short) > 70:
        short = short[:67] + "..."
    return short

def find_best_paragraph_for_insert(content, target_topics, exclude_slugs):
    """Find the best paragraph to insert a link after."""
    paragraphs = re.findall(r'(<p[^>]*>.*?</p>)', content, re.DOTALL)
    if not paragraphs:
        return None, None

    # Topic keywords for scoring
    topic_keywords = {
        "kbeauty": ["skincare", "beauty", "skin", "product", "routine", "serum", "cream", "ingredient", "moistur"],
        "kpop": ["music", "fan", "album", "song", "concert", "group", "member", "perform"],
        "kdrama": ["drama", "series", "watch", "show", "episode", "character", "story", "netflix"],
        "food": ["food", "dish", "restaurant", "cook", "recipe", "eat", "flavor", "ingredient", "market"],
        "travel": ["visit", "travel", "explore", "neighborhood", "district", "temple", "palace"],
        "language": ["learn", "word", "phrase", "speak", "language", "korean"],
    }

    keywords = []
    for t in target_topics:
        keywords.extend(topic_keywords.get(t, []))

    best_score = -1
    best_idx = -1

    for i, para in enumerate(paragraphs):
        if len(para) < 80:
            continue
        if i < 2 or i >= len(paragraphs) - 2:
            continue
        # Skip paragraphs that already have links to any of our targets
        has_existing = False
        for slug in exclude_slugs:
            if slug in para:
                has_existing = True
                break
        if has_existing:
            continue

        score = 0
        para_lower = para.lower()
        for kw in keywords:
            if kw in para_lower:
                score += 1

        if score > best_score:
            best_score = score
            best_idx = i

    if best_idx == -1:
        # Fallback: middle paragraph
        middle = len(paragraphs) // 2
        candidates = [i for i in range(max(2, len(paragraphs)//3), min(len(paragraphs)-2, 2*len(paragraphs)//3))
                      if len(paragraphs[i]) > 80]
        if candidates:
            best_idx = candidates[len(candidates) // 2]

    if best_idx == -1:
        return None, None

    return paragraphs[best_idx], best_score

# For each target post needing incoming links
needs_incoming = [(pid, incoming_counts[pid]) for pid in newest_11_ids if len(incoming_counts[pid]) < 3]
print(f"\n{len(needs_incoming)} posts need more incoming links")

template_counters = {}

for target_id, existing_sources in needs_incoming:
    target = posts_by_id[target_id]
    target_topics = post_topics[target_id]
    needed = 3 - len(existing_sources)

    print(f"\n--- Target: ID:{target_id} {target['title'][:50]} (has {len(existing_sources)}, need {needed} more) ---")

    # Find candidate source posts (same topic, not already linking)
    candidates = []
    for other_id, other in posts_by_id.items():
        if other_id == target_id:
            continue
        if other_id in existing_sources:
            continue
        # Check topic overlap
        other_topics = post_topics[other_id]
        overlap = target_topics & other_topics
        if overlap:
            candidates.append((other_id, len(overlap), other))

    # Sort by overlap score descending
    candidates.sort(key=lambda x: x[1], reverse=True)

    added = 0
    for cand_id, overlap_score, cand in candidates:
        if added >= needed:
            break

        content = get_content(cand_id)

        # Check if link already exists
        if target["slug"] in content:
            continue

        # Find best paragraph
        all_target_slugs = [posts_by_id[tid]["slug"] for tid in newest_11_ids]
        best_para, kw_score = find_best_paragraph_for_insert(content, target_topics, all_target_slugs)

        if best_para is None:
            continue

        # Choose template
        primary_topic = list(target_topics)[0] if target_topics else "default"
        templates = INCOMING_TEMPLATES.get(primary_topic, INCOMING_TEMPLATES["default"])
        counter_key = f"{target_id}_{primary_topic}"
        idx = template_counters.get(counter_key, 0) % len(templates)
        template_counters[counter_key] = idx + 1

        title_short = make_title_short(target["title"])
        link_sentence = templates[idx].format(
            url=target["link"],
            title=target["title"],
            title_short=title_short,
        )
        link_para = f"\n\n<p>{link_sentence}</p>"

        new_content = content.replace(best_para, best_para + link_para, 1)
        if new_content == content:
            continue

        # Update
        try:
            r2 = s.post(f"{REST}/posts/{cand_id}", headers=h, json={"content": new_content})
            if r2.status_code == 200:
                set_content(cand_id, new_content)
                added += 1
                cand_title = cand["title"][:40]
                print(f"  + ID:{cand_id} ({cand_title}) → ID:{target_id} (topic overlap: {overlap_score})")
                results_incoming.append({
                    "source_id": cand_id,
                    "source_title": cand["title"][:50],
                    "target_id": target_id,
                    "target_title": target["title"][:50],
                })
            else:
                print(f"  ! ID:{cand_id} — UPDATE FAILED (HTTP {r2.status_code})")
        except Exception as e:
            print(f"  ! ID:{cand_id} — ERROR: {e}")

        time.sleep(0.5)

    if added < needed:
        print(f"  (Could only add {added}/{needed} — not enough relevant sources)")

# ── Step 6: Add OUTGOING links where count < 5 ──
print("\n\n=== ADDING OUTGOING LINKS (source < 5 outgoing) ===")

results_outgoing = []

OUTGOING_TEMPLATES = {
    "kbeauty": [
        'For more K-beauty recommendations, see our guide to <a href="{url}">{title_short}</a>.',
        'If you want to explore further, our <a href="{url}">{title_short}</a> guide covers the essentials.',
        'Related reading: <a href="{url}">{title_short}</a> dives deeper into this topic.',
        'You can also check out our breakdown of <a href="{url}">{title_short}</a>.',
    ],
    "kpop": [
        'For more K-pop analysis, read our deep dive into <a href="{url}">{title_short}</a>.',
        'Related: our article on <a href="{url}">{title_short}</a> explores a similar theme.',
        'Fans will also appreciate our coverage of <a href="{url}">{title_short}</a>.',
        'Don\'t miss our related piece on <a href="{url}">{title_short}</a>.',
    ],
    "kdrama": [
        'For more K-drama picks, check out <a href="{url}">{title_short}</a>.',
        'Drama fans should also read our review of <a href="{url}">{title_short}</a>.',
        'Our article on <a href="{url}">{title_short}</a> covers another must-watch series.',
        'Looking for more? <a href="{url}">{title_short}</a> is another top recommendation.',
    ],
    "food": [
        'For more Korean food adventures, explore our <a href="{url}">{title_short}</a> guide.',
        'Hungry for more? Check out <a href="{url}">{title_short}</a>.',
        'Our <a href="{url}">{title_short}</a> article covers another culinary gem.',
        'Food lovers should also read about <a href="{url}">{title_short}</a>.',
    ],
    "travel": [
        'Planning more stops? Our <a href="{url}">{title_short}</a> guide has you covered.',
        'Travelers should also explore <a href="{url}">{title_short}</a>.',
        'For your next destination, check out <a href="{url}">{title_short}</a>.',
    ],
    "language": [
        'To continue learning, check out <a href="{url}">{title_short}</a>.',
        'Our <a href="{url}">{title_short}</a> guide is a great next step.',
    ],
    "default": [
        'Related reading: <a href="{url}">{title_short}</a>.',
        'You might also enjoy <a href="{url}">{title_short}</a>.',
        'Check out our article on <a href="{url}">{title_short}</a> for more.',
    ],
}

needs_outgoing = [(pid, outgoing_counts[pid]) for pid in newest_11_ids if len(outgoing_counts[pid]) < 5]
print(f"\n{len(needs_outgoing)} posts need more outgoing links")

out_template_counters = {}

for source_id, existing_targets in needs_outgoing:
    source = posts_by_id[source_id]
    source_topics = post_topics[source_id]
    needed = 5 - len(existing_targets)

    print(f"\n--- Source: ID:{source_id} {source['title'][:50]} (has {len(existing_targets)} outgoing, need {needed} more) ---")

    # Find candidate target posts
    candidates = []
    for other_id, other in posts_by_id.items():
        if other_id == source_id:
            continue
        if other_id in existing_targets:
            continue
        other_topics = post_topics[other_id]
        overlap = source_topics & other_topics
        if overlap:
            candidates.append((other_id, len(overlap), other))

    candidates.sort(key=lambda x: x[1], reverse=True)

    content = get_content(source_id)
    added = 0

    for cand_id, overlap_score, cand in candidates:
        if added >= needed:
            break

        # Check if link already exists
        if cand["slug"] in content:
            continue

        # Find best paragraph
        already_linked_slugs = [posts_by_id[tid]["slug"] for tid in existing_targets]
        best_para, kw_score = find_best_paragraph_for_insert(content, post_topics[cand_id], already_linked_slugs)

        if best_para is None:
            continue

        # Choose template
        primary_topic = list(post_topics[cand_id])[0] if post_topics[cand_id] else "default"
        templates = OUTGOING_TEMPLATES.get(primary_topic, OUTGOING_TEMPLATES["default"])
        counter_key = f"out_{source_id}_{primary_topic}"
        idx = out_template_counters.get(counter_key, 0) % len(templates)
        out_template_counters[counter_key] = idx + 1

        title_short = make_title_short(cand["title"])
        link_sentence = templates[idx].format(
            url=cand["link"],
            title=cand["title"],
            title_short=title_short,
        )
        link_para = f"\n\n<p>{link_sentence}</p>"

        new_content = content.replace(best_para, best_para + link_para, 1)
        if new_content == content:
            continue

        content = new_content  # Update local copy for subsequent inserts
        added += 1
        cand_title = cand["title"][:40]
        print(f"  + ID:{source_id} → ID:{cand_id} ({cand_title}) (topic: {primary_topic})")
        results_outgoing.append({
            "source_id": source_id,
            "source_title": source["title"][:50],
            "target_id": cand_id,
            "target_title": cand["title"][:50],
        })

    # Push all outgoing link additions for this post in one update
    if added > 0:
        try:
            r2 = s.post(f"{REST}/posts/{source_id}", headers=h, json={"content": content})
            if r2.status_code == 200:
                set_content(source_id, content)
                print(f"  => Saved {added} new outgoing links for ID:{source_id}")
            else:
                print(f"  ! SAVE FAILED for ID:{source_id} (HTTP {r2.status_code})")
                results_outgoing = [r for r in results_outgoing if r["source_id"] != source_id]
        except Exception as e:
            print(f"  ! ERROR saving ID:{source_id}: {e}")
            results_outgoing = [r for r in results_outgoing if r["source_id"] != source_id]
        time.sleep(0.5)
    else:
        print(f"  (Could only add {added}/{needed} — not enough relevant candidates)")

# ── Final Summary ──
print(f"\n{'='*70}")
print(f"FINAL SUMMARY")
print(f"{'='*70}")
print(f"\nINCOMING links added: {len(results_incoming)}")
for r in results_incoming:
    print(f"  ID:{r['source_id']:>5} ({r['source_title'][:35]:35s}) → ID:{r['target_id']} ({r['target_title'][:35]})")

print(f"\nOUTGOING links added: {len(results_outgoing)}")
for r in results_outgoing:
    print(f"  ID:{r['source_id']:>5} ({r['source_title'][:35]:35s}) → ID:{r['target_id']} ({r['target_title'][:35]})")

print(f"\nTOTAL: {len(results_incoming) + len(results_outgoing)} internal links added")
print(f"{'='*70}")
