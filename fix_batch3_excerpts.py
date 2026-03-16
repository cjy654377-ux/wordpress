#!/usr/bin/env python3
"""Fix quality issues: excerpts, FAQ schema on 566, long titles."""

import requests, re, json, html, time

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
    print("ERROR: Could not extract nonce. Login may have failed.")
    exit(1)
h = {"X-WP-Nonce": m.group(1)}
print(f"Logged in. Nonce: {h['X-WP-Nonce'][:8]}...")

# --- Fetch all posts ---
def fetch_all_posts():
    posts = []
    page_num = 1
    while True:
        r = s.get(f"{REST}/posts", params={"per_page": 100, "page": page_num, "status": "publish"}, headers=h)
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
print(f"Total posts: {len(all_posts)}")

# ============================================================
# TASK 1: Add excerpts to posts missing them
# ============================================================
print("\n=== TASK 1: Fix missing excerpts ===")

def strip_html(text):
    """Remove HTML tags and decode entities."""
    text = re.sub(r'<[^>]+>', '', text)
    text = html.unescape(text)
    return text.strip()

def generate_excerpt(content_html, max_len=160):
    """Generate excerpt from first meaningful paragraph."""
    # Find first <p> with actual text content
    paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', content_html, re.DOTALL)
    for p in paragraphs:
        text = strip_html(p).strip()
        # Skip empty, very short, or image-only paragraphs
        if len(text) < 30:
            continue
        # Truncate at word boundary
        if len(text) <= max_len:
            return text
        truncated = text[:max_len]
        # Find last space to end at word boundary
        last_space = truncated.rfind(' ')
        if last_space > 80:
            truncated = truncated[:last_space]
        return truncated.rstrip('.,;:!?') + "..."
    return None

excerpt_fixed = 0
excerpt_skipped = 0
for post in all_posts:
    excerpt_text = strip_html(post.get("excerpt", {}).get("rendered", ""))
    if excerpt_text:
        continue  # Already has excerpt

    content_html = post.get("content", {}).get("rendered", "")
    new_excerpt = generate_excerpt(content_html)
    if not new_excerpt:
        print(f"  SKIP ID:{post['id']} - no suitable paragraph found")
        excerpt_skipped += 1
        continue

    r = s.post(f"{REST}/posts/{post['id']}", headers=h, json={"excerpt": new_excerpt})
    if r.status_code == 200:
        excerpt_fixed += 1
        print(f"  OK ID:{post['id']} excerpt: {new_excerpt[:60]}...")
    else:
        print(f"  FAIL ID:{post['id']} status={r.status_code}")
    time.sleep(0.3)

print(f"Excerpts: {excerpt_fixed} added, {excerpt_skipped} skipped")

# ============================================================
# TASK 2: Fix FAQ Schema on ID:566
# ============================================================
print("\n=== TASK 2: Fix FAQ schema on ID:566 ===")

r = s.get(f"{REST}/posts/566?context=edit", headers=h)
if r.status_code == 200:
    raw_content = r.json()["content"]["raw"]

    # The FAQ is HTML-encoded with &#8220;/&#8221; (smart quotes) and <br /> tags
    # Find the block: starts with <p>{ containing FAQPage and ends with }</p>
    # Note: it spans across <p> tags due to WP auto-formatting
    faq_start_match = re.search(r'<p>\{<br />\s*&#8220;@context&#8221;', raw_content)

    if faq_start_match:
        start_idx = faq_start_match.start()
        # Find the end: closing brace followed by </p>
        # The JSON ends with }  ]  } then </p>
        end_match = re.search(r'\}\s*</p>', raw_content[start_idx + 100:])
        if end_match:
            # Find the LAST }  </p> pattern (the outermost closing brace)
            # Search for the pattern: ]<br />\n}</p>
            end_pattern = re.search(r'\]\s*(?:<br />\s*)*\}\s*</p>', raw_content[start_idx:])
            if end_pattern:
                end_idx = start_idx + end_pattern.end()
            else:
                end_idx = start_idx + end_match.end() + 100

            faq_block = raw_content[start_idx:end_idx]
            print(f"  Found FAQ block ({len(faq_block)} chars)")

            # Clean the block to extract valid JSON
            cleaned = faq_block
            # Remove HTML tags
            cleaned = re.sub(r'</?p[^>]*>', '', cleaned)
            cleaned = re.sub(r'<br\s*/?>', '', cleaned)
            # Decode HTML entities
            cleaned = html.unescape(cleaned)
            # Replace smart quotes with regular quotes
            cleaned = cleaned.replace('\u201c', '"').replace('\u201d', '"')
            cleaned = cleaned.replace('\u2018', "'").replace('\u2019', "'")
            # Clean whitespace
            cleaned = re.sub(r'\n\s+', ' ', cleaned)
            cleaned = cleaned.strip()

            try:
                # Remove any control characters that snuck in
                cleaned = re.sub(r'[\x00-\x1f\x7f]', ' ', cleaned)
                # Fix any remaining smart apostrophes
                cleaned = cleaned.replace('\u2017', "'")
                # Collapse multiple spaces
                cleaned = re.sub(r'  +', ' ', cleaned)
                faq_json = json.loads(cleaned)
                print(f"  Parsed FAQ with {len(faq_json.get('mainEntity', []))} questions")

                # Remove the visible FAQ block from content
                modified_content = raw_content[:start_idx] + raw_content[end_idx:]

                # Clean up empty paragraphs and excess newlines
                modified_content = re.sub(r'<p>\s*</p>', '', modified_content)
                modified_content = re.sub(r'\n{3,}', '\n\n', modified_content)

                # Add proper script tag at end of content
                script_tag = f'\n\n<script type="application/ld+json">\n{json.dumps(faq_json, ensure_ascii=False)}\n</script>'
                modified_content = modified_content.rstrip() + script_tag

                r3 = s.post(f"{REST}/posts/566", headers=h, json={"content": modified_content})
                if r3.status_code == 200:
                    print("  OK: FAQ schema fixed on ID:566")
                else:
                    print(f"  FAIL: status={r3.status_code} {r3.text[:200]}")
            except json.JSONDecodeError as e:
                print(f"  JSON parse error: {e}")
                print(f"  Cleaned text (first 500): {cleaned[:500]}")
        else:
            print("  Could not find end of FAQ block")
    else:
        # Check if already properly in script tag
        script_faqs = re.findall(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', raw_content, re.DOTALL)
        has_faq_script = any('FAQPage' in sf for sf in script_faqs)
        if has_faq_script:
            print("  FAQ already properly in <script> tag. No fix needed.")
        else:
            print("  WARNING: No FAQ JSON-LD found in ID:566")
else:
    print(f"  FAIL: Could not fetch ID:566, status={r.status_code}")

# ============================================================
# TASK 3: Shorten titles over 60 chars
# ============================================================
print("\n=== TASK 3: Shorten long titles ===")

title_ids = [1063, 1067, 1069, 1074]
titles_fixed = 0

for pid in title_ids:
    r = s.get(f"{REST}/posts/{pid}", headers=h)
    if r.status_code != 200:
        print(f"  FAIL: Could not fetch ID:{pid}")
        continue

    post = r.json()
    current_title = html.unescape(post["title"]["rendered"])
    print(f"  ID:{pid} ({len(current_title)} chars): {current_title}")

    if len(current_title) <= 60:
        print(f"    Already under 60 chars, skipping")
        continue

    # Generate shortened titles based on content
    short_titles = {
        1063: "Bloom Skin: Korea's New Glass Skin Secret for 2026",
        1067: "BTS SWIM Lyrics & Meaning: Full Breakdown (2026)",
        1069: "BTS 2026 Seoul Concert: Dates, Tickets & Guide",
        1074: "Siren's Kiss K-Drama: Cast, Plot & Review (2026)",
    }

    # Fallback: auto-shorten by trimming
    new_title = short_titles.get(pid)
    if not new_title or len(new_title) > 60:
        # Auto-generate: keep first 57 chars at word boundary
        words = current_title.split()
        shortened = ""
        for w in words:
            test = f"{shortened} {w}".strip() if shortened else w
            if len(test) > 57:
                break
            shortened = test
        new_title = shortened

    print(f"    New ({len(new_title)} chars): {new_title}")

    r2 = s.post(f"{REST}/posts/{pid}", headers=h, json={"title": new_title})
    if r2.status_code == 200:
        titles_fixed += 1
        # Also update slug to match new title
        print(f"    OK: Title updated")
    else:
        print(f"    FAIL: status={r2.status_code}")
    time.sleep(0.3)

print(f"Titles: {titles_fixed} shortened")

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "=" * 50)
print("SUMMARY")
print("=" * 50)
print(f"Task 1 - Excerpts: {excerpt_fixed} added, {excerpt_skipped} skipped")
print(f"Task 2 - FAQ Schema ID:566: checked/fixed")
print(f"Task 3 - Long titles: {titles_fixed} shortened")
print("Done!")
