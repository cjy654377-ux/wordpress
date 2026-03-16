#!/usr/bin/env python3
"""Fix quality issues on 5 recently published posts on rhythmicaleskimo.com."""

import requests, re, json, html, sys
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

# ─── Login ───────────────────────────────────────────────────────────────────
SITE = "https://rhythmicaleskimo.com"
REST = f"{SITE}/wp-json/wp/v2"
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
    sys.exit(1)
h = {"X-WP-Nonce": m.group(1)}
print(f"Logged in. Nonce: {h['X-WP-Nonce'][:8]}...")

# ─── Post IDs and new titles ────────────────────────────────────────────────
POST_IDS = [1103, 1107, 1110, 1117, 1120]

NEW_TITLES = {
    1103: "Biodance Bio-Collagen Mask Review [2026 TikTok Hit]",
    1107: "Korean Glass Hair: 7-Step K-Beauty Routine [2026]",
    1110: "Climax (\ud074\ub77c\uc774\ub9c9\uc2a4) K-Drama Review: Cast & Plot 2026",
    1117: "Mad Concrete Dreams K-Drama: Cast & Episodes [2026]",
    1120: "Dujjonku: Korea's Viral Dubai Cookie [2026 Guide]",
}

# ─── AI phrase replacements ──────────────────────────────────────────────────
AI_REPLACEMENTS = [
    (r'\bdive into\b', 'explore'),
    (r'\bDive into\b', 'Explore'),
    (r'\bin this comprehensive\b', 'in this'),
    (r'\bIn this comprehensive\b', 'In this'),
    (r'\bcomprehensive guide\b', 'full guide'),
    (r'\bComprehensive guide\b', 'Full guide'),
    (r'\bComprehensive Guide\b', 'Full Guide'),
]

# ─── CSS classes for inline style replacement ────────────────────────────────
TABLE_STYLE_CSS = """<style>
.kdrama-table{width:100%;border-collapse:collapse;margin:1em 0}
.kdrama-table th{background:#1a1a2e;color:#fff;padding:10px 14px;text-align:left;font-weight:600}
.kdrama-table td{padding:10px 14px;border-bottom:1px solid #e0e0e0}
.kdrama-table tr:nth-child(even) td{background:#f8f8fc}
.kdrama-table tr:hover td{background:#eef}
</style>
"""


def fetch_post(pid):
    r = s.get(f"{REST}/posts/{pid}?context=edit", headers=h)
    r.raise_for_status()
    return r.json()


def update_post(pid, data):
    r = s.post(f"{REST}/posts/{pid}", headers=h, json=data)
    r.raise_for_status()
    return r.json()


def fix_faq_jsonld(content, pid):
    """Extract FAQ JSON-LD from visible content and re-insert as proper script tag."""
    changes = []

    # Pattern 1: JSON-LD inside <p> tags
    # Pattern 2: Raw JSON-LD text (possibly HTML-encoded)
    # Pattern 3: Already in script tag but also duplicated in <p>

    # First, extract any existing proper script tags to preserve them
    existing_scripts = re.findall(r'<script\s+type="application/ld\+json">\s*(\{.*?\})\s*</script>', content, re.DOTALL)

    # Remove existing script tags (we'll re-add the best version)
    content = re.sub(r'<script\s+type="application/ld\+json">\s*\{.*?\}\s*</script>', '', content, flags=re.DOTALL)

    # Find JSON-LD in visible text (inside <p> tags or bare)
    # Could be HTML-encoded or raw
    json_ld_data = None

    # Pattern: <p> containing JSON-LD
    p_pattern = r'<p[^>]*>\s*(\{["\s]*@context["\s]*:[^<]+)\s*</p>'
    p_matches = re.findall(p_pattern, content, re.DOTALL)

    if not p_matches:
        # Try HTML-decoded version
        p_pattern2 = r'<p[^>]*>\s*(\{(?:&quot;|"|&#8220;|&#8221;)\s*@context.*?)\s*</p>'
        p_matches = re.findall(p_pattern2, content, re.DOTALL | re.IGNORECASE)

    if not p_matches:
        # Try finding raw JSON anywhere in content that looks like schema.org
        raw_pattern = r'(\{"@context"\s*:\s*"https?://schema\.org"[^}]*"@type"\s*:\s*"FAQPage".*?\}\s*\]\s*\})'
        p_matches = re.findall(raw_pattern, content, re.DOTALL)

    # Also look for HTML-entity encoded JSON
    if not p_matches:
        decoded_content = html.unescape(content)
        raw_pattern = r'(\{"@context"\s*:\s*"https?://schema\.org"[^}]*"@type"\s*:\s*"FAQPage".*?\}\s*\]\s*\})'
        raw_matches = re.findall(raw_pattern, decoded_content, re.DOTALL)
        if raw_matches:
            p_matches = raw_matches

    for match in p_matches:
        # Decode HTML entities
        decoded = html.unescape(match).strip()
        # Fix smart quotes to regular quotes
        decoded = decoded.replace('\u201c', '"').replace('\u201d', '"')
        decoded = decoded.replace('\u2018', "'").replace('\u2019', "'")

        try:
            json_ld_data = json.loads(decoded)
            changes.append("Extracted FAQ JSON-LD from visible text")
        except json.JSONDecodeError:
            # Try to clean up
            try:
                # Remove trailing content after the JSON
                brace_count = 0
                end_idx = 0
                for i, c in enumerate(decoded):
                    if c == '{':
                        brace_count += 1
                    elif c == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            end_idx = i + 1
                            break
                cleaned = decoded[:end_idx]
                json_ld_data = json.loads(cleaned)
                changes.append("Extracted and cleaned FAQ JSON-LD from visible text")
            except (json.JSONDecodeError, ValueError):
                pass

    # If we found it from existing scripts
    if not json_ld_data and existing_scripts:
        for script_json in existing_scripts:
            try:
                json_ld_data = json.loads(script_json)
                if json_ld_data.get("@type") == "FAQPage":
                    changes.append("Preserved existing FAQ JSON-LD script")
                    break
            except json.JSONDecodeError:
                pass

    # Remove the visible JSON-LD text from content
    # Remove <p> tags containing JSON-LD
    content = re.sub(r'<p[^>]*>\s*\{["\s]*@context[^<]*</p>', '', content, flags=re.DOTALL)
    content = re.sub(r'<p[^>]*>\s*\{(?:&quot;|&#8220;)[^<]*@context[^<]*</p>', '', content, flags=re.DOTALL | re.IGNORECASE)

    # Also remove bare JSON-LD that might not be in <p>
    content = re.sub(r'\{"@context"\s*:\s*"https?://schema\.org"[^}]*"@type"\s*:\s*"FAQPage".*?\}\s*\]\s*\}', '', content, flags=re.DOTALL)

    # Also try removing HTML-encoded versions
    content = re.sub(r'\{&quot;@context&quot;.*?FAQPage.*?\}\s*\]\s*\}', '', content, flags=re.DOTALL)

    # Clean up empty paragraphs left behind
    content = re.sub(r'<p[^>]*>\s*</p>', '', content)

    # Re-insert as proper script tag at the end
    if json_ld_data:
        json_str = json.dumps(json_ld_data, ensure_ascii=False)
        content = content.rstrip()
        content += f'\n<script type="application/ld+json">{json_str}</script>'
        changes.append("Re-inserted FAQ JSON-LD as proper <script> tag")
    else:
        changes.append("WARNING: Could not find/parse FAQ JSON-LD")

    return content, changes


def fix_affiliate_links_1103(content):
    """Fix YesStyle and Amazon affiliate links in ID:1103."""
    changes = []

    # Add rco parameter to YesStyle links
    def add_yesstyle_param(m):
        url = m.group(1)
        if 'rco=' not in url:
            if '?' in url:
                url += '&rco=RKBEAUTY01'
            else:
                url += '?rco=RKBEAUTY01'
            changes.append(f"Added rco= to YesStyle link")
        return f'href="{url}"'

    content = re.sub(r'href="(https?://(?:www\.)?yesstyle\.com[^"]*)"', add_yesstyle_param, content)

    # Fix rel attributes on affiliate links (YesStyle and Amazon)
    def fix_rel_attr(m):
        full_tag = m.group(0)
        href = m.group(1)

        is_affiliate = ('yesstyle.com' in href or 'amazon.com' in href or
                        'amzn.to' in href or 'tag=' in href)

        if not is_affiliate:
            return full_tag

        # Check if rel already correct
        if 'nofollow sponsored' in full_tag:
            return full_tag

        # Replace or add rel attribute
        if 'rel="' in full_tag:
            new_tag = re.sub(r'rel="[^"]*"', 'rel="nofollow sponsored noopener"', full_tag)
        else:
            new_tag = full_tag.replace('>', ' rel="nofollow sponsored noopener">', 1)

        if new_tag != full_tag:
            changes.append(f"Fixed rel= on affiliate link")
        return new_tag

    content = re.sub(r'<a\s[^>]*href="([^"]*)"[^>]*>', fix_rel_attr, content)

    return content, changes


def fix_affiliate_links_1107(content):
    """Fix affiliate link rel attributes in ID:1107."""
    changes = []

    def fix_rel_attr(m):
        full_tag = m.group(0)
        href = m.group(1)

        is_affiliate = ('yesstyle.com' in href or 'amazon.com' in href or
                        'amzn.to' in href or 'tag=' in href)

        if not is_affiliate:
            return full_tag

        if 'nofollow sponsored' in full_tag:
            return full_tag

        if 'rel="' in full_tag:
            new_tag = re.sub(r'rel="[^"]*"', 'rel="nofollow sponsored noopener"', full_tag)
        else:
            new_tag = full_tag.replace('>', ' rel="nofollow sponsored noopener">', 1)

        if new_tag != full_tag:
            changes.append(f"Fixed rel= on affiliate link")
        return new_tag

    # Also add rco to YesStyle links
    def add_yesstyle_param(m):
        url = m.group(1)
        if 'rco=' not in url:
            if '?' in url:
                url += '&rco=RKBEAUTY01'
            else:
                url += '?rco=RKBEAUTY01'
            changes.append(f"Added rco= to YesStyle link")
        return f'href="{url}"'

    content = re.sub(r'href="(https?://(?:www\.)?yesstyle\.com[^"]*)"', add_yesstyle_param, content)
    content = re.sub(r'<a\s[^>]*href="([^"]*)"[^>]*>', fix_rel_attr, content)

    return content, changes


def reduce_inline_styles(content, pid):
    """Replace inline styles in tables with CSS classes for ID:1110 and 1117."""
    changes = []

    # Check if tables exist
    if '<table' not in content:
        return content, changes

    # Remove inline styles from th and td elements
    styled_count = 0

    def strip_cell_styles(m):
        nonlocal styled_count
        tag = m.group(1)  # th or td
        attrs = m.group(2)
        rest = m.group(3)

        if 'style="' in attrs:
            styled_count_before = styled_count
            new_attrs = re.sub(r'\s*style="[^"]*"', '', attrs)
            styled_count += 1
            return f'<{tag}{new_attrs}>{rest}'
        return m.group(0)

    content = re.sub(r'<(t[hd])([^>]*)>(.*?)</\1>', strip_cell_styles, content, flags=re.DOTALL)

    # Also strip styles from <tr> and <table>
    for tag in ['tr', 'table', 'thead', 'tbody']:
        def strip_tag_style(m, t=tag):
            nonlocal styled_count
            attrs = m.group(1)
            if 'style="' in attrs:
                styled_count += 1
                new_attrs = re.sub(r'\s*style="[^"]*"', '', attrs)
                return f'<{t}{new_attrs}>'
            return m.group(0)
        content = re.sub(f'<{tag}([^>]*)>', strip_tag_style, content)

    # Add class to tables
    content = re.sub(r'<table(?!\s+class=)', '<table class="kdrama-table"', content)
    # If table already has class, append
    content = re.sub(r'<table\s+class="(?!kdrama-table)([^"]*)"', r'<table class="kdrama-table \1"', content)

    if styled_count > 0:
        # Add CSS block at the beginning of content
        if 'kdrama-table' not in content.split('<table')[0]:
            content = TABLE_STYLE_CSS + content
        changes.append(f"Removed {styled_count} inline styles, added CSS classes")

    return content, changes


def add_table_overflow_wrappers(content):
    """Wrap tables with overflow div for mobile."""
    changes = []

    # Don't wrap if already wrapped
    def wrap_table(m):
        table_html = m.group(0)
        changes.append("Added overflow wrapper to table")
        return f'<div style="overflow-x:auto;max-width:100%;">{table_html}</div>'

    # Only wrap tables not already inside overflow divs
    # Check if table is preceded by the overflow div
    parts = content.split('<table')
    if len(parts) <= 1:
        return content, changes

    new_content = parts[0]
    for i, part in enumerate(parts[1:], 1):
        # Check if immediately preceded by overflow wrapper
        preceding = new_content[-80:] if len(new_content) > 80 else new_content
        if 'overflow-x:auto' in preceding and preceding.rstrip().endswith('>'):
            new_content += '<table' + part
        else:
            # Find the closing </table>
            table_end = part.find('</table>')
            if table_end != -1:
                table_end += len('</table>')
                table_content = '<table' + part[:table_end]
                after = part[table_end:]
                new_content += f'<div style="overflow-x:auto;max-width:100%;">{table_content}</div>{after}'
                changes.append("Added overflow wrapper to table")
            else:
                new_content += '<table' + part

    return new_content, changes


def fix_ai_phrases(content):
    """Replace AI-sounding phrases."""
    changes = []
    for pattern, replacement in AI_REPLACEMENTS:
        new_content = re.sub(pattern, replacement, content)
        if new_content != content:
            count = len(re.findall(pattern, content))
            changes.append(f"Replaced '{pattern}' x{count}")
            content = new_content
    return content, changes


def fix_duplicate_internal_links(content, pid):
    """Deduplicate internal link anchor text when same URL appears in body and 'You Might Also Enjoy'."""
    changes = []

    # Find all internal links
    internal_links = re.findall(r'<a[^>]*href="(https?://rhythmicaleskimo\.com[^"]*)"[^>]*>([^<]*)</a>', content)

    # Group by URL
    url_occurrences = {}
    for url, text in internal_links:
        url_clean = url.rstrip('/')
        if url_clean not in url_occurrences:
            url_occurrences[url_clean] = []
        url_occurrences[url_clean].append(text)

    # Find duplicates with same anchor text
    for url, texts in url_occurrences.items():
        if len(texts) > 1:
            # Check if any share the exact same anchor text
            seen = set()
            for t in texts:
                if t in seen:
                    changes.append(f"Note: URL {url[-40:]} appears {len(texts)} times (different anchor text OK)")
                    break
                seen.add(t)

    return content, changes


def add_streaming_prices(content, pid):
    """Add streaming price info to K-drama posts."""
    changes = []

    price_note = ('<p><strong>Streaming prices:</strong> Viki Standard $4.99/mo \u00b7 '
                  'Netflix from $6.99/mo \u00b7 Disney+ $7.99/mo</p>')

    # Find "Where to Watch" section
    watch_pattern = r'(<h[23][^>]*>.*?[Ww]here\s+to\s+[Ww]atch.*?</h[23]>)'
    watch_match = re.search(watch_pattern, content, re.DOTALL)

    if watch_match:
        # Find the next heading after "Where to Watch" to insert before it
        pos = watch_match.end()
        next_heading = re.search(r'<h[23]', content[pos:])

        if next_heading:
            insert_pos = pos + next_heading.start()
            content = content[:insert_pos] + price_note + '\n' + content[insert_pos:]
            changes.append("Added streaming prices to 'Where to Watch' section")
        else:
            # Insert at end of section (before last closing tag or at end)
            content = content[:pos] + '\n' + price_note + content[pos:]
            changes.append("Added streaming prices after 'Where to Watch' heading")
    else:
        # Try alternate patterns
        watch_pattern2 = r'(where to watch|streaming|how to watch)'
        watch_match2 = re.search(watch_pattern2, content, re.IGNORECASE)
        if watch_match2:
            # Find the end of the paragraph containing this
            para_end = content.find('</p>', watch_match2.end())
            if para_end != -1:
                insert_pos = para_end + 4
                content = content[:insert_pos] + '\n' + price_note + content[insert_pos:]
                changes.append("Added streaming prices near watch info")
        else:
            changes.append("WARNING: No 'Where to Watch' section found")

    return content, changes


# ─── Main processing ─────────────────────────────────────────────────────────
print("\n" + "="*70)
print("FIXING 5 POSTS")
print("="*70)

for pid in POST_IDS:
    print(f"\n{'─'*60}")
    print(f"Processing ID:{pid} - {NEW_TITLES[pid]}")
    print(f"{'─'*60}")

    post = fetch_post(pid)
    content = post['content']['raw']
    title = post['title']['raw']
    all_changes = []

    # 1. Fix FAQ JSON-LD
    content, changes = fix_faq_jsonld(content, pid)
    all_changes.extend(changes)

    # 2. Title already handled via NEW_TITLES dict
    if title != NEW_TITLES[pid]:
        all_changes.append(f"Title: '{title[:50]}...' -> '{NEW_TITLES[pid]}'")

    # 3. Fix affiliate links
    if pid == 1103:
        content, changes = fix_affiliate_links_1103(content)
        all_changes.extend(changes)
    elif pid == 1107:
        content, changes = fix_affiliate_links_1107(content)
        all_changes.extend(changes)

    # 4. Reduce inline styles (K-drama posts)
    if pid in (1110, 1117):
        content, changes = reduce_inline_styles(content, pid)
        all_changes.extend(changes)

    # 5. Add table overflow wrappers
    if pid in (1103, 1107, 1110):
        content, changes = add_table_overflow_wrappers(content)
        all_changes.extend(changes)

    # 6. Check duplicate internal links
    if pid in (1103, 1107):
        content, changes = fix_duplicate_internal_links(content, pid)
        all_changes.extend(changes)

    # 7. Fix AI phrases (all posts)
    content, changes = fix_ai_phrases(content)
    all_changes.extend(changes)

    # 8. Add streaming prices (K-drama posts)
    if pid in (1110, 1117):
        content, changes = add_streaming_prices(content, pid)
        all_changes.extend(changes)

    # Clean up multiple blank lines
    content = re.sub(r'\n{3,}', '\n\n', content)

    # Update the post
    update_data = {
        'title': NEW_TITLES[pid],
        'content': content,
    }

    try:
        result = update_post(pid, update_data)
        print(f"  UPDATED successfully (ID:{result['id']})")
    except Exception as e:
        print(f"  ERROR updating: {e}")

    # Print changes
    for c in all_changes:
        print(f"  - {c}")

    if not all_changes:
        print("  - No changes detected")

print(f"\n{'='*70}")
print("DONE - All 5 posts processed")
print("="*70)
