#!/usr/bin/env python3
"""Fix 4 quality issues: HTML structure, duplicate content, excerpts, long paragraphs."""
import re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import login, REST

s, h = login()
print("Logged in successfully.\n")

def get_post(pid):
    r = s.get(f"{REST}/posts/{pid}?context=edit", headers=h)
    if r.status_code != 200:
        print(f"  ERROR fetching post {pid}: {r.status_code}")
        return None
    return r.json()

def update_post(pid, data):
    r = s.post(f"{REST}/posts/{pid}", headers=h, json=data)
    if r.status_code == 200:
        return True
    print(f"  ERROR updating post {pid}: {r.status_code} {r.text[:200]}")
    return False

# ============================================================
# ISSUE 1: Fix HTML structure errors (K-Beauty 8 posts)
# ============================================================
print("=" * 60)
print("ISSUE 1: HTML Structure Errors (K-Beauty)")
print("=" * 60)

kbeauty_ids = [76, 549, 547, 539, 543, 537, 541, 545]
issue1_fixed = 0

for pid in kbeauty_ids:
    post = get_post(pid)
    if not post:
        continue
    content = post["content"]["raw"]
    original = content
    fixes = []

    # Fix 1a: Find <p> tags that aren't properly closed
    # Strategy: ensure every <p...> has a matching </p>
    # Handle case where </div> appears before </p>

    # Fix nested </div> before </p> — close <p> before </div>
    pattern = r'(<p[^>]*>(?:(?!</p>).)*?)(</div>)'
    count_nesting = len(re.findall(pattern, content, re.DOTALL))
    if count_nesting > 0:
        content = re.sub(pattern, r'\1</p>\2', content, flags=re.DOTALL)
        fixes.append(f"  Fixed {count_nesting} nesting errors (</div> before </p>)")

    # Fix unclosed <p> tags: <p>...<p> without </p> between them
    # Find <p> that is followed by another <p> or block element without </p>
    def fix_unclosed_p(text):
        count = 0
        # Pattern: <p> content that hits another <p> without closing
        result = re.sub(
            r'(<p[^>]*>(?:(?!</p>|<p[ >]).)*?)(<p[ >])',
            lambda m: m.group(1) + '</p>' + m.group(2),
            text, flags=re.DOTALL
        )
        count = len(re.findall(r'(<p[^>]*>(?:(?!</p>|<p[ >]).)*?)(<p[ >])', text, re.DOTALL))
        return result, count

    content, unclosed_count = fix_unclosed_p(content)
    # Run twice to catch cascading issues
    content, unclosed_count2 = fix_unclosed_p(content)
    total_unclosed = unclosed_count + unclosed_count2
    if total_unclosed > 0:
        fixes.append(f"  Fixed {total_unclosed} unclosed <p> tags")

    # Fix <p> at end of content without </p>
    # Check if last <p> is unclosed
    last_p = content.rfind('<p')
    last_close_p = content.rfind('</p>')
    if last_p > last_close_p and last_p != -1:
        content = content.rstrip()
        if not content.endswith('</p>'):
            content += '</p>'
            fixes.append("  Fixed unclosed <p> at end of content")

    if content != original:
        if update_post(pid, {"content": content}):
            issue1_fixed += 1
            print(f"  Post {pid}: FIXED")
            for f in fixes:
                print(f)
        else:
            print(f"  Post {pid}: UPDATE FAILED")
    else:
        print(f"  Post {pid}: No HTML issues found")

print(f"\nIssue 1 Result: {issue1_fixed}/{len(kbeauty_ids)} posts fixed\n")

# ============================================================
# ISSUE 2: Remove duplicate content
# ============================================================
print("=" * 60)
print("ISSUE 2: Duplicate Content Removal")
print("=" * 60)

# 2a: FAQ answer text duplicated in body (K-Beauty posts)
issue2_fixed = 0

for pid in kbeauty_ids + [72, 464]:
    post = get_post(pid)
    if not post:
        continue
    content = post["content"]["raw"]
    original = content
    removals = []

    # Extract FAQ acceptedAnswer texts
    faq_answers = re.findall(
        r'"acceptedAnswer"\s*:\s*\{\s*"@type"\s*:\s*"Answer"\s*,\s*"text"\s*:\s*"([^"]{50,})"',
        content
    )

    for ans in faq_answers:
        # Clean the answer text for matching
        ans_clean = ans.strip()
        # Escape for regex
        ans_escaped = re.escape(ans_clean)
        # Find in body (outside of script/schema blocks)
        # Split content into schema and non-schema parts
        schema_pattern = r'<script\s+type="application/ld\+json">.*?</script>'
        schemas = re.findall(schema_pattern, content, re.DOTALL)
        non_schema = re.sub(schema_pattern, '___SCHEMA_PLACEHOLDER___', content, flags=re.DOTALL)

        # Check if answer text appears in non-schema part
        if ans_clean in non_schema:
            # Find the paragraph containing this text and check if it's a near-duplicate
            # Remove the duplicate paragraph from body
            # Match <p> containing the FAQ answer
            p_pattern = r'<p[^>]*>[^<]*' + re.escape(ans_clean[:80]) + r'[^<]*</p>'
            matches = re.findall(p_pattern, non_schema)
            if matches:
                for m in matches:
                    # Only remove if the paragraph is mostly just the FAQ answer
                    plain = re.sub(r'<[^>]+>', '', m).strip()
                    if len(plain) > 0 and len(ans_clean) / len(plain) > 0.7:
                        content = content.replace(m, '', 1)
                        removals.append(f"  Removed FAQ duplicate ({len(ans_clean)} chars)")
                        break

    # 2b: Check for identical sentences repeated (ID:72, 464)
    if pid in [72, 464]:
        # Find sentences that appear more than once
        sentences = re.findall(r'([A-Z][^.!?]{50,}[.!?])', content)
        seen = {}
        for sent in sentences:
            sent_clean = sent.strip()
            if sent_clean in seen:
                seen[sent_clean] += 1
            else:
                seen[sent_clean] = 1
        for sent, count in seen.items():
            if count >= 2:
                # Remove one occurrence (keep first, remove second)
                first_pos = content.find(sent)
                second_pos = content.find(sent, first_pos + len(sent))
                if second_pos != -1:
                    content = content[:second_pos] + content[second_pos + len(sent):]
                    removals.append(f"  Removed duplicate sentence ({len(sent)} chars)")

    if content != original:
        if update_post(pid, {"content": content}):
            issue2_fixed += 1
            print(f"  Post {pid}: FIXED")
            for r_ in removals:
                print(r_)
        else:
            print(f"  Post {pid}: UPDATE FAILED")
    else:
        print(f"  Post {pid}: No duplicates found")

print(f"\nIssue 2 Result: {issue2_fixed} posts fixed\n")

# ============================================================
# ISSUE 3: Set excerpts (4 posts)
# ============================================================
print("=" * 60)
print("ISSUE 3: Set Excerpts")
print("=" * 60)

excerpt_posts = {
    74: "Seoul's Hidden Alley Restaurants",
    61: "Busan Food Guide",
    182: "Olive Young Shopping Guide",
    178: "K-Drama Cafes in Seoul",
}
issue3_fixed = 0

for pid, label in excerpt_posts.items():
    post = get_post(pid)
    if not post:
        continue

    # Check if excerpt already set
    existing_excerpt = post.get("excerpt", {}).get("raw", "").strip()
    if existing_excerpt:
        print(f"  Post {pid} ({label}): Excerpt already set, skipping")
        continue

    content = post["content"]["raw"]

    # Extract first meaningful paragraph
    paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', content, re.DOTALL)
    excerpt = ""
    for p in paragraphs:
        # Strip HTML tags
        plain = re.sub(r'<[^>]+>', '', p).strip()
        if len(plain) > 40:  # Skip very short paragraphs (likely labels)
            excerpt = plain
            break

    if not excerpt:
        print(f"  Post {pid} ({label}): No suitable paragraph found")
        continue

    # Trim to 160 chars at word boundary
    if len(excerpt) > 160:
        excerpt = excerpt[:157]
        last_space = excerpt.rfind(' ')
        if last_space > 100:
            excerpt = excerpt[:last_space]
        excerpt += "..."

    if update_post(pid, {"excerpt": excerpt}):
        issue3_fixed += 1
        print(f"  Post {pid} ({label}): Excerpt set ({len(excerpt)} chars)")
        print(f"    \"{excerpt[:80]}...\"")
    else:
        print(f"  Post {pid} ({label}): UPDATE FAILED")

print(f"\nIssue 3 Result: {issue3_fixed}/{len(excerpt_posts)} excerpts set\n")

# ============================================================
# ISSUE 4: Split long paragraphs (3 posts)
# ============================================================
print("=" * 60)
print("ISSUE 4: Split Long Paragraphs (200+ words)")
print("=" * 60)

long_para_ids = [464, 182, 178]
issue4_fixed = 0

for pid in long_para_ids:
    post = get_post(pid)
    if not post:
        continue
    content = post["content"]["raw"]
    original = content
    split_count = [0]

    def split_long_paragraph(match):
        # Using list to allow mutation in closure
        full = match.group(0)
        inner = match.group(1)
        plain = re.sub(r'<[^>]+>', '', inner)
        words = plain.split()

        if len(words) < 200:
            return full

        # Find a good split point (after a period, near the middle)
        sentences = re.split(r'(?<=[.!?])\s+', inner)
        if len(sentences) < 2:
            return full

        # Split roughly in half by sentence count
        mid = len(sentences) // 2
        first_half = ' '.join(sentences[:mid])
        second_half = ' '.join(sentences[mid:])

        split_count[0] += 1
        return f'<p>{first_half}</p>\n\n<p>{second_half}</p>'

    content = re.sub(r'<p[^>]*>(.*?)</p>', split_long_paragraph, content, flags=re.DOTALL)

    if content != original:
        if update_post(pid, {"content": content}):
            issue4_fixed += 1
            print(f"  Post {pid}: Split {split_count[0]} long paragraph(s)")
        else:
            print(f"  Post {pid}: UPDATE FAILED")
    else:
        print(f"  Post {pid}: No paragraphs over 200 words found")

print(f"\nIssue 4 Result: {issue4_fixed}/{len(long_para_ids)} posts fixed\n")

# ============================================================
# Summary
# ============================================================
print("=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"  Issue 1 (HTML structure):    {issue1_fixed}/{len(kbeauty_ids)} posts")
print(f"  Issue 2 (Duplicates):        {issue2_fixed} posts")
print(f"  Issue 3 (Excerpts):          {issue3_fixed}/{len(excerpt_posts)} posts")
print(f"  Issue 4 (Long paragraphs):   {issue4_fixed}/{len(long_para_ids)} posts")
print("\nDone.")
