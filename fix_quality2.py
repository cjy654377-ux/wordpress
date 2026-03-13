#!/usr/bin/env python3
"""Fix 4 quality issues: excerpts, broken internal links, word count, long paragraphs."""
import requests, re, sys, html as html_mod
sys.path.insert(0, "/Users/choijooyong/wordpress")
from engine import login, REST

s, h = login()
print("Logged in.\n")

# ── Issue 1: Fix missing excerpts for all 56 posts ──
print("=" * 60)
print("ISSUE 1: Fix missing excerpts")
print("=" * 60)

all_posts = []
page = 1
while True:
    r = s.get(f"{REST}/posts?per_page=100&page={page}&status=publish", headers=h)
    if r.status_code != 200:
        break
    batch = r.json()
    if not batch:
        break
    all_posts.extend(batch)
    page += 1

print(f"Total posts found: {len(all_posts)}")

excerpt_fixed = 0
for p in all_posts:
    exc = p.get("excerpt", {}).get("rendered", "").strip()
    # Check if excerpt is empty or just default auto-generated (contains full content)
    exc_text = re.sub(r'<[^>]+>', '', exc).strip()
    if len(exc_text) < 10:
        content = p["content"]["rendered"]
        # Extract first <p> tag content
        m = re.search(r'<p[^>]*>(.*?)</p>', content, re.DOTALL)
        if m:
            text = re.sub(r'<[^>]+>', '', m.group(1)).strip()
            text = html_mod.unescape(text)
            if len(text) > 155:
                # Cut at word boundary
                text = text[:155].rsplit(' ', 1)[0] + '...'
            if len(text) > 10:
                r2 = s.post(f"{REST}/posts/{p['id']}", headers=h, json={"excerpt": text})
                if r2.status_code == 200:
                    print(f"  OK ID:{p['id']} — excerpt set ({len(text)} chars)")
                    excerpt_fixed += 1
                else:
                    print(f"  FAIL ID:{p['id']} — {r2.status_code}")

print(f"\nExcerpts fixed: {excerpt_fixed}\n")

# ── Issue 2: Fix broken internal links (6 posts) ──
print("=" * 60)
print("ISSUE 2: Fix broken internal links")
print("=" * 60)

link_fixes = {
    51: {
        "search": r'gwangjang-market-food-guide-[^"\']*street-food/',
        "replace": "gwangjang-market-food-guide-seouls-oldest-market-and-its-legendary-eats/"
    },
    55: {
        "search": r'gwangjang-market-food-guide-[^"\']*street-food/',
        "replace": "gwangjang-market-food-guide-seouls-oldest-market-and-its-legendary-eats/"
    },
    59: {
        "search": r'top-10-must-try-korean-soups[^"\']*/',
        "replace": "top-10-must-try-korean-soups-for-winter-from-tv-show-kitchens-to-your-travel-list/"
    },
    65: {
        "search": r'budgets-meals-in-korea-10-tv-featured[^"\']*/',
        "replace": "budgets-meals-in-korea-10-tv-featured-restaurants-where-you-can-eat-for-under-10/"
    },
    566: {
        "search": r'/bts-arirang-comeback-2026-everything-you-need-to-know-about-the-album-world-tour-and-netflix-concert/',
        "replace": "/bts-arirang-world-tour-2026-complete-city-by-city-date-guide-and-how-to-get-tickets/"
    },
    612: {
        "search": r'/boyfriend-on-demand-jisoos-netflix-k-drama-everyone-is-talking-about-complete-guide/',
        "replace": "/boyfriend-on-demand-jisoos-netflix-k-drama-complete-guide-cast-review-cameos-everything-you-need-to-know/"
    },
}

links_fixed = 0
for pid, fix in link_fixes.items():
    r = s.get(f"{REST}/posts/{pid}?context=edit", headers=h)
    if r.status_code != 200:
        print(f"  FAIL ID:{pid} — cannot fetch ({r.status_code})")
        continue
    content = r.json()["content"]["raw"]
    new_content, count = re.subn(fix["search"], fix["replace"], content)
    if count > 0:
        r2 = s.post(f"{REST}/posts/{pid}", headers=h, json={"content": new_content})
        if r2.status_code == 200:
            print(f"  OK ID:{pid} — {count} link(s) fixed")
            links_fixed += 1
        else:
            print(f"  FAIL ID:{pid} — update failed ({r2.status_code})")
    else:
        # Try broader search for the slug
        print(f"  SKIP ID:{pid} — pattern not found, checking content...")
        # Show what internal links exist
        found = re.findall(r'href="[^"]*rhythmicaleskimo\.com([^"]*)"', content)
        if not found:
            found = re.findall(r'href="(/[^"]*)"', content)
        if found:
            for link in found[:5]:
                print(f"    Found link: {link}")

print(f"\nInternal links fixed: {links_fixed}\n")

# ── Issue 3: Word count — add ~50 words to 2 posts ──
print("=" * 60)
print("ISSUE 3: Add ~50 words to short posts")
print("=" * 60)

word_additions = {
    184: {
        "search": '</div>\n\n<!-- FAQ Section -->',
        "addition": """<div class="content-section">
<h3>Photography Tips for Your Visit</h3>
<p>HYBE Insight is a photographer's dream, but there are a few things to keep in mind. Flash photography is prohibited in most exhibition areas to protect the displays and maintain the immersive atmosphere. However, natural and ambient lighting creates stunning photo opportunities throughout the space. The hologram rooms and interactive displays are particularly photogenic — arrive early for the best shots without crowds in the background.</p>
</div>

<!-- FAQ Section -->"""
    },
    413: {
        "search": '</div>\n\n<!-- FAQ Section -->',
        "addition": """<div class="content-section">
<h3>The Song's Lasting Impact on K-Pop</h3>
<p>Blood Sweat &amp; Tears didn't just mark a turning point for BTS — it fundamentally shifted what was possible in K-pop music videos. The song proved that idol groups could tackle complex philosophical and literary themes without alienating their audience. In the years since its release, countless K-pop acts have cited this era as inspiration for their own artistic explorations, making it one of the most influential releases in the genre's history.</p>
</div>

<!-- FAQ Section -->"""
    },
}

words_fixed = 0
for pid, fix in word_additions.items():
    r = s.get(f"{REST}/posts/{pid}?context=edit", headers=h)
    if r.status_code != 200:
        print(f"  FAIL ID:{pid} — cannot fetch ({r.status_code})")
        continue
    content = r.json()["content"]["raw"]
    if fix["search"] in content:
        new_content = content.replace(fix["search"], fix["addition"], 1)
        r2 = s.post(f"{REST}/posts/{pid}", headers=h, json={"content": new_content})
        if r2.status_code == 200:
            old_wc = len(re.sub(r'<[^>]+>', '', content).split())
            new_wc = len(re.sub(r'<[^>]+>', '', new_content).split())
            print(f"  OK ID:{pid} — {old_wc}w → {new_wc}w (+{new_wc - old_wc}w)")
            words_fixed += 1
        else:
            print(f"  FAIL ID:{pid} — update failed ({r2.status_code})")
    else:
        print(f"  SKIP ID:{pid} — search pattern not found, trying alternative...")
        # Try to find the FAQ section with different patterns
        faq_patterns = [
            '<!-- FAQ Section -->',
            '<!-- FAQ',
            '<div class="faq-section"',
            '<h2>Frequently Asked',
            '<h2>FAQ',
        ]
        found = False
        for pat in faq_patterns:
            if pat in content:
                new_content = content.replace(pat, fix["addition"].replace('<!-- FAQ Section -->', pat).replace(fix["search"].replace('\n\n<!-- FAQ Section -->', ''), '') if '<!-- FAQ Section -->' not in pat else content.replace(pat, fix["addition"].split('\n\n')[-1].replace('<!-- FAQ Section -->', '') + '\n\n' + pat), 1)
                # Simpler approach: just insert before FAQ
                new_content = content.replace(pat, fix["addition"].replace(fix["search"], pat), 1)
                r2 = s.post(f"{REST}/posts/{pid}", headers=h, json={"content": new_content})
                if r2.status_code == 200:
                    old_wc = len(re.sub(r'<[^>]+>', '', content).split())
                    new_wc = len(re.sub(r'<[^>]+>', '', new_content).split())
                    print(f"  OK ID:{pid} — {old_wc}w → {new_wc}w (+{new_wc - old_wc}w)")
                    words_fixed += 1
                    found = True
                    break
        if not found:
            # Last resort: append before closing
            print(f"  INFO ID:{pid} — inserting before last </div>")
            # Find last major section closing
            addition_html = fix["addition"].replace(fix["search"], "").replace("<!-- FAQ Section -->", "")
            last_div = content.rfind('</article>')
            if last_div == -1:
                last_div = content.rfind('</div>')
            if last_div > 0:
                new_content = content[:last_div] + addition_html + "\n\n" + content[last_div:]
                r2 = s.post(f"{REST}/posts/{pid}", headers=h, json={"content": new_content})
                if r2.status_code == 200:
                    old_wc = len(re.sub(r'<[^>]+>', '', content).split())
                    new_wc = len(re.sub(r'<[^>]+>', '', new_content).split())
                    print(f"  OK ID:{pid} — {old_wc}w → {new_wc}w (+{new_wc - old_wc}w)")
                    words_fixed += 1

print(f"\nWord count fixes: {words_fixed}\n")

# ── Issue 4: Split long paragraph in ID:566 ──
print("=" * 60)
print("ISSUE 4: Split long paragraph (ID:566)")
print("=" * 60)

r = s.get(f"{REST}/posts/566?context=edit", headers=h)
if r.status_code == 200:
    content = r.json()["content"]["raw"]
    # Find paragraphs with 200+ words
    paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', content, re.DOTALL)
    split_done = False
    for para in paragraphs:
        plain = re.sub(r'<[^>]+>', '', para).strip()
        words = plain.split()
        if len(words) >= 200:
            print(f"  Found long paragraph: {len(words)} words")
            # Split at a sentence boundary near the middle
            sentences = re.split(r'(?<=[.!?])\s+', plain)
            mid = len(words) // 2
            running = 0
            split_idx = 0
            for i, sent in enumerate(sentences):
                running += len(sent.split())
                if running >= mid:
                    split_idx = i + 1
                    break
            if split_idx > 0 and split_idx < len(sentences):
                first_half = ' '.join(sentences[:split_idx])
                second_half = ' '.join(sentences[split_idx:])
                old_p = f'<p>{para}</p>' if f'<p>{para}</p>' in content else None
                if old_p is None:
                    # Try matching with attributes
                    for m in re.finditer(r'<p[^>]*>' + re.escape(para) + r'</p>', content):
                        old_p = m.group(0)
                        break
                if old_p is None:
                    # Direct search
                    old_p = para
                    new_p = f'{first_half}</p>\n\n<p>{second_half}'
                    new_content = content.replace(old_p, new_p, 1)
                else:
                    tag_start = old_p[:old_p.index('>')+1]
                    new_p = f'{tag_start}{first_half}</p>\n\n<p>{second_half}</p>'
                    new_content = content.replace(old_p, new_p, 1)

                r2 = s.post(f"{REST}/posts/566", headers=h, json={"content": new_content})
                if r2.status_code == 200:
                    print(f"  OK — split into {len(first_half.split())}w + {len(second_half.split())}w")
                    split_done = True
                else:
                    print(f"  FAIL — update failed ({r2.status_code})")
                break
    if not split_done:
        print("  No 200+ word paragraph found or split failed")
else:
    print(f"  FAIL — cannot fetch ID:566 ({r.status_code})")

print("\n" + "=" * 60)
print("ALL DONE")
print("=" * 60)
