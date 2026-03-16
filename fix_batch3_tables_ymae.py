#!/usr/bin/env python3
"""
Fix Batch 3: Responsive table wrappers + "You Might Also Enjoy" sections
"""

import requests, re, json, time, html

SITE = "https://rhythmicaleskimo.com"
REST = f"{SITE}/wp-json/wp/v2"

# --- Login ---
s = requests.Session()
s.cookies.set("wordpress_test_cookie", "WP+Cookie+check")
s.post(f"{SITE}/wp-login.php", data={
    "log": "cjy654377@gmail.com", "pwd": "Dkflekd1!!",
    "wp-submit": "Log In", "redirect_to": "/wp-admin/", "testcookie": "1"
}, allow_redirects=True)
page = s.get(f"{SITE}/wp-admin/post-new.php").text
m = re.search(r'"nonce":"([a-f0-9]+)"', page)
if not m:
    print("ERROR: Could not get nonce. Login failed?")
    exit(1)
h = {"X-WP-Nonce": m.group(1)}
print(f"Logged in. Nonce: {h['X-WP-Nonce'][:8]}...")

# --- Fetch ALL posts ---
def fetch_all_posts():
    posts = []
    page_num = 1
    while True:
        r = s.get(f"{REST}/posts", params={
            "per_page": 100, "page": page_num, "status": "publish",
            "_fields": "id,title,content,slug,link,categories"
        }, headers=h)
        if r.status_code != 200:
            break
        batch = r.json()
        if not batch:
            break
        posts.extend(batch)
        page_num += 1
    return posts

print("Fetching all posts...")
all_posts = fetch_all_posts()
print(f"Fetched {len(all_posts)} posts.")

# --- Fetch categories ---
def fetch_all_categories():
    cats = []
    page_num = 1
    while True:
        r = s.get(f"{REST}/categories", params={
            "per_page": 100, "page": page_num,
            "_fields": "id,name,slug"
        }, headers=h)
        if r.status_code != 200:
            break
        batch = r.json()
        if not batch:
            break
        cats.extend(batch)
        page_num += 1
    return {c["id"]: c for c in cats}

cats = fetch_all_categories()
print(f"Fetched {len(cats)} categories: {[c['name'] for c in cats.values()]}")

# Build category -> posts mapping
cat_posts = {}
for p in all_posts:
    for cid in p.get("categories", []):
        cat_posts.setdefault(cid, []).append(p)

def update_post(post_id, content):
    r = s.post(f"{REST}/posts/{post_id}", headers=h, json={"content": content})
    return r.status_code == 200

# ============================================================
# TASK 1: Add responsive table wrappers
# ============================================================
print("\n" + "="*60)
print("TASK 1: Responsive table wrappers")
print("="*60)

def wrap_tables(content):
    """Wrap bare <table>...</table> with overflow-x div. Skip already-wrapped."""
    # Pattern: find <table...>...</table> blocks
    # We need to check if they're already inside overflow-x div

    changed = False

    # Find all table blocks
    # Use a function-based replacement to check context
    def replace_table(match):
        nonlocal changed
        full_match = match.group(0)
        start_pos = match.start()

        # Check if already wrapped: look backwards for overflow-x div
        # Look at the ~200 chars before this table
        before = content[max(0, start_pos - 200):start_pos]

        # Check if there's an unclosed div with overflow-x before this table
        if re.search(r'<div[^>]*overflow-x[^>]*>\s*$', before):
            return full_match  # Already wrapped

        changed = True
        return f'<div style="overflow-x:auto;max-width:100%;">{full_match}</div>'

    # Match <table...>...</table> (non-greedy, DOTALL)
    new_content = re.sub(
        r'<table\b[^>]*>.*?</table>',
        replace_table,
        content,
        flags=re.DOTALL
    )

    return new_content, changed

task1_updated = 0
task1_tables_wrapped = 0

for p in all_posts:
    content = p["content"]["rendered"]

    # Skip posts with no tables
    if "<table" not in content:
        continue

    # Count tables before
    tables_before = len(re.findall(r'<table\b', content))

    new_content, changed = wrap_tables(content)

    if changed:
        # Count how many we wrapped
        wrapped_count = new_content.count('overflow-x:auto;max-width:100%') - content.count('overflow-x:auto;max-width:100%')
        task1_tables_wrapped += wrapped_count

        title = html.unescape(p["title"]["rendered"])
        print(f"  Wrapping {wrapped_count} table(s) in: {title} (ID:{p['id']})")

        if update_post(p["id"], new_content):
            task1_updated += 1
            # Update local copy for Task 2
            p["content"]["rendered"] = new_content
        else:
            print(f"    ERROR updating post {p['id']}")

        time.sleep(0.3)

print(f"\nTask 1 Summary: Updated {task1_updated} posts, wrapped {task1_tables_wrapped} tables.")

# ============================================================
# TASK 2: Add "You Might Also Enjoy" section
# ============================================================
print("\n" + "="*60)
print("TASK 2: 'You Might Also Enjoy' sections")
print("="*60)

# Re-fetch all posts to get fresh content after Task 1
print("Re-fetching posts for Task 2...")
all_posts = fetch_all_posts()
print(f"Fetched {len(all_posts)} posts.")

# Rebuild category mapping
cat_posts = {}
for p in all_posts:
    for cid in p.get("categories", []):
        cat_posts.setdefault(cid, []).append(p)

def get_related_posts(post, all_posts_list, count=3):
    """Find related posts in same categories, not already linked in content."""
    content = post["content"]["rendered"]
    post_cats = set(post.get("categories", []))

    # Collect candidate posts from same categories
    candidates = []
    seen_ids = {post["id"]}

    for cid in post_cats:
        for cp in cat_posts.get(cid, []):
            if cp["id"] not in seen_ids:
                seen_ids.add(cp["id"])
                # Check if this post's slug is already linked in content
                slug = cp["slug"]
                if slug and slug not in content:
                    # Score: prefer posts with more category overlap
                    cp_cats = set(cp.get("categories", []))
                    overlap = len(post_cats & cp_cats)
                    candidates.append((overlap, cp))

    # Sort by overlap descending, take top N
    candidates.sort(key=lambda x: -x[0])
    return [c[1] for c in candidates[:count]]

def add_ymae_section(content, related_posts):
    """Add 'You Might Also Enjoy' section before FAQ schema or at end."""

    # Build the section
    items = []
    for rp in related_posts:
        title = html.unescape(rp["title"]["rendered"])
        slug = rp["slug"]
        items.append(f'<li><a href="/{slug}/">{title}</a></li>')

    section = f'\n<h2>You Might Also Enjoy</h2>\n<ul>\n' + '\n'.join(items) + '\n</ul>\n'

    # Insert before FAQ schema script if present
    faq_pattern = r'(<script\s+type=["\']application/ld\+json["\'][^>]*>.*?"@type"\s*:\s*"FAQPage".*?</script>)'
    faq_match = re.search(faq_pattern, content, re.DOTALL)

    if faq_match:
        insert_pos = faq_match.start()
        new_content = content[:insert_pos] + section + '\n' + content[insert_pos:]
    else:
        new_content = content + section

    return new_content

task2_updated = 0
task2_skipped_no_related = 0

for p in all_posts:
    content = p["content"]["rendered"]
    title = html.unescape(p["title"]["rendered"])

    # Skip if already has "You Might Also Enjoy"
    if "You Might Also Enjoy" in content:
        continue

    # Find related posts
    related = get_related_posts(p, all_posts, count=3)

    if len(related) < 3:
        # Try to get at least some
        if len(related) == 0:
            task2_skipped_no_related += 1
            print(f"  SKIP (no related): {title} (ID:{p['id']})")
            continue

    new_content = add_ymae_section(content, related)

    related_titles = [html.unescape(r["title"]["rendered"])[:40] for r in related]
    print(f"  Adding YMAE to: {title[:50]} (ID:{p['id']}) -> {len(related)} links")

    if update_post(p["id"], new_content):
        task2_updated += 1
    else:
        print(f"    ERROR updating post {p['id']}")

    time.sleep(0.3)

print(f"\nTask 2 Summary: Added YMAE to {task2_updated} posts. Skipped {task2_skipped_no_related} (no related).")

# ============================================================
# FINAL SUMMARY
# ============================================================
print("\n" + "="*60)
print("FINAL SUMMARY")
print("="*60)
print(f"Task 1 - Table wrappers: {task1_updated} posts updated, {task1_tables_wrapped} tables wrapped")
print(f"Task 2 - YMAE sections:  {task2_updated} posts updated, {task2_skipped_no_related} skipped")
print(f"Total posts modified:    {task1_updated + task2_updated}")
print("Done!")
