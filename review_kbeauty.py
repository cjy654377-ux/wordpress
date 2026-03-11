#!/usr/bin/env python3
"""K-Beauty 포스트 품질 리뷰 스크립트 — 10개 체크리스트 자동 검증"""
import requests, re, json, sys
from html.parser import HTMLParser

SITE = "https://rhythmicaleskimo.com"
REST = f"{SITE}/wp-json/wp/v2"
USER = "cjy654377@gmail.com"
PASS = "Dkflekd1!!"
POST_IDS = [76, 549, 547, 539, 543, 537, 541, 545]

# --- Auth ---
def login():
    s = requests.Session()
    s.cookies.set("wordpress_test_cookie", "WP+Cookie+check")
    s.post(f"{SITE}/wp-login.php", data={
        "log": USER, "pwd": PASS, "wp-submit": "Log In",
        "redirect_to": "/wp-admin/", "testcookie": "1"
    }, allow_redirects=True)
    page = s.get(f"{SITE}/wp-admin/post-new.php").text
    m = re.search(r'"nonce":"([a-f0-9]+)"', page)
    if not m:
        print("ERROR: nonce not found"); sys.exit(1)
    return s, {"X-WP-Nonce": m.group(1)}

# --- HTML tag balance checker ---
VOID_ELEMENTS = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}

def check_broken_html(html):
    """Check for unclosed tags and bad nesting. Returns list of issues."""
    issues = []
    stack = []

    class TagChecker(HTMLParser):
        def handle_starttag(self, tag, attrs):
            if tag.lower() not in VOID_ELEMENTS:
                stack.append(tag.lower())
        def handle_endtag(self, tag):
            tag = tag.lower()
            if tag in VOID_ELEMENTS:
                return
            if stack and stack[-1] == tag:
                stack.pop()
            elif tag in stack:
                # Mismatched nesting
                idx = len(stack) - 1 - stack[::-1].index(tag)
                unclosed = stack[idx+1:]
                if unclosed:
                    issues.append(f"Mismatched nesting: </{tag}> closes before {unclosed}")
                stack[idx:] = []
            else:
                issues.append(f"Extra closing tag: </{tag}>")
        def handle_data(self, data):
            pass

    try:
        TagChecker().feed(html)
    except Exception as e:
        issues.append(f"Parse error: {e}")

    if stack:
        # Filter out common false positives (WordPress often leaves some unclosed)
        real_unclosed = [t for t in stack if t not in ('html','head','body')]
        if real_unclosed:
            issues.append(f"Unclosed tags: {real_unclosed}")

    return issues

def check_duplicate_content(text):
    """Check for duplicate paragraphs/sentences (3+ sentences repeated)."""
    # Split into sentences
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 40]

    seen = {}
    duplicates = []
    for s in sentences:
        normalized = ' '.join(s.lower().split())
        if normalized in seen:
            seen[normalized] += 1
        else:
            seen[normalized] = 1

    for s, count in seen.items():
        if count >= 2:
            duplicates.append(f"'{s[:60]}...' x{count}")

    return duplicates

def check_long_paragraphs(html):
    """Find <p> tags with 200+ words."""
    paras = re.findall(r'<p[^>]*>(.*?)</p>', html, re.DOTALL)
    long_paras = []
    for i, p in enumerate(paras):
        stripped = re.sub(r'<[^>]+>', '', p)
        wc = len(stripped.split())
        if wc >= 200:
            long_paras.append((i+1, wc, stripped[:80]))
    return long_paras

def check_internal_links_alive(session, html):
    """HEAD-check internal links. Returns (total, broken_list)."""
    links = re.findall(r'href="(https?://rhythmicaleskimo\.com[^"]*)"', html)
    links = list(set(links))  # dedupe
    broken = []
    for url in links:
        try:
            r = session.head(url, timeout=10, allow_redirects=True)
            if r.status_code >= 400:
                broken.append((url, r.status_code))
        except Exception as e:
            broken.append((url, str(e)))
    return links, broken

def check_product_specifics(text):
    """Check if content has specific product names, prices, ingredients."""
    has_price = bool(re.search(r'\$\d+', text))
    has_ingredient = bool(re.search(r'(?i)(niacinamide|hyaluronic|retinol|vitamin c|salicylic|glycolic|ceramide|peptide|snail mucin|centella|mugwort|rice bran|green tea|propolis|collagen|AHA|BHA|PHA|PDRN|exosome)', text))
    # Check for Korean brand names
    has_brand = bool(re.search(r'(?i)(COSRX|Innisfree|Laneige|Sulwhasoo|Missha|Etude|Banila|Klairs|Beauty of Joseon|Medicube|Torriden|Anua|Round Lab|Isntree|Skin1004|Dr\.?\s*Jart|Amorepacific|Illiyoon|Purito|Some By Mi|Heimish|Neogen|TonyMoly|Holika|Peripera|Rom&nd|Biodance|VT Cosmetics)', text))
    return has_price, has_ingredient, has_brand

# --- Main ---
def main():
    s, h = login()
    print("Logged in. Fetching posts...\n")

    results = []
    all_internal_links_for_check = []

    for pid in POST_IDS:
        r = s.get(f"{REST}/posts/{pid}", headers=h)
        if r.status_code != 200:
            print(f"  ERROR: Post {pid} returned {r.status_code}")
            continue

        post = r.json()
        title = post['title']['rendered']
        content = post['content']['rendered']
        slug = post['slug']

        # 1. Word count
        stripped = re.sub(r'<[^>]+>', '', content)
        word_count = len(stripped.split())

        # 2. H2 count
        h2_count = len(re.findall(r'<h2', content, re.IGNORECASE))

        # 3. Internal links
        internal_links = re.findall(r'href="(https?://rhythmicaleskimo\.com[^"]*)"', content)
        internal_link_count = len(set(internal_links))

        # 4. FAQ Schema
        has_faq = 'FAQPage' in content

        # 5. Broken HTML
        html_issues = check_broken_html(content)

        # 6. Duplicate content
        duplicates = check_duplicate_content(stripped)

        # 7. Amazon affiliate
        has_amazon = 'rhythmicalesk-20' in content
        amazon_count = content.count('rhythmicalesk-20')

        # 8. Long paragraphs (mobile readability)
        long_paras = check_long_paragraphs(content)

        # 9. Broken internal links
        all_links, broken_links = check_internal_links_alive(s, content)

        # 10. Content quality - product specifics
        has_price, has_ingredient, has_brand = check_product_specifics(stripped)

        result = {
            'id': pid,
            'title': title[:60],
            'slug': slug,
            'word_count': word_count,
            'word_ok': word_count >= 2500,
            'h2_count': h2_count,
            'h2_ok': h2_count >= 4,
            'internal_links': internal_link_count,
            'internal_ok': internal_link_count >= 3,
            'has_faq': has_faq,
            'html_issues': html_issues,
            'duplicates': duplicates,
            'has_amazon': has_amazon,
            'amazon_count': amazon_count,
            'long_paras': long_paras,
            'broken_links': broken_links,
            'all_links_count': len(all_links),
            'has_price': has_price,
            'has_ingredient': has_ingredient,
            'has_brand': has_brand,
        }
        results.append(result)

        # Progress
        status = "OK" if all([result['word_ok'], result['h2_ok'], result['internal_ok'], result['has_faq'], not html_issues, not duplicates, result['has_amazon'], not long_paras, not broken_links]) else "ISSUES"
        print(f"  [{status}] ID:{pid} — {title[:50]}")

    # --- Summary Table ---
    print("\n" + "="*120)
    print("K-BEAUTY POST QUALITY REVIEW — SUMMARY TABLE")
    print("="*120)

    header = f"{'ID':>5} | {'Words':>6} | {'H2s':>3} | {'IntLinks':>8} | {'FAQ':>3} | {'HTML':>5} | {'Dups':>4} | {'Amzn':>5} | {'LongP':>5} | {'BrkLnk':>6} | {'Specs':>10}"
    print(header)
    print("-"*120)

    for r in results:
        word_s = f"{'PASS' if r['word_ok'] else 'FAIL'}({r['word_count']})"
        h2_s = f"{'OK' if r['h2_ok'] else 'FAIL'}({r['h2_count']})"
        il_s = f"{'OK' if r['internal_ok'] else 'FAIL'}({r['internal_links']})"
        faq_s = "YES" if r['has_faq'] else "NO"
        html_s = "OK" if not r['html_issues'] else f"ERR({len(r['html_issues'])})"
        dup_s = "OK" if not r['duplicates'] else f"DUP({len(r['duplicates'])})"
        amzn_s = f"YES({r['amazon_count']})" if r['has_amazon'] else "NO"
        longp_s = "OK" if not r['long_paras'] else f"FAIL({len(r['long_paras'])})"
        brk_s = "OK" if not r['broken_links'] else f"FAIL({len(r['broken_links'])})"
        specs = []
        if r['has_brand']: specs.append("B")
        if r['has_ingredient']: specs.append("I")
        if r['has_price']: specs.append("$")
        specs_s = ",".join(specs) if specs else "NONE"

        print(f"{r['id']:>5} | {word_s:>10} | {h2_s:>6} | {il_s:>8} | {faq_s:>3} | {html_s:>5} | {dup_s:>7} | {amzn_s:>7} | {longp_s:>5} | {brk_s:>6} | {specs_s:>10}")

    # --- Detailed Issues ---
    print("\n" + "="*120)
    print("DETAILED ISSUES")
    print("="*120)

    for r in results:
        issues = []
        if not r['word_ok']:
            issues.append(f"  Word count: {r['word_count']} (need 2500+)")
        if not r['h2_ok']:
            issues.append(f"  H2 tags: {r['h2_count']} (need 4+)")
        if not r['internal_ok']:
            issues.append(f"  Internal links: {r['internal_links']} (need 3+)")
        if not r['has_faq']:
            issues.append(f"  Missing FAQ Schema (FAQPage JSON-LD)")
        if r['html_issues']:
            for hi in r['html_issues']:
                issues.append(f"  HTML: {hi}")
        if r['duplicates']:
            for d in r['duplicates']:
                issues.append(f"  Duplicate: {d}")
        if not r['has_amazon']:
            issues.append(f"  No Amazon affiliate links (rhythmicalesk-20)")
        if r['long_paras']:
            for idx, wc, preview in r['long_paras']:
                issues.append(f"  Long paragraph #{idx}: {wc} words — '{preview}...'")
        if r['broken_links']:
            for url, code in r['broken_links']:
                issues.append(f"  Broken link: {url} → {code}")
        if not r['has_brand']:
            issues.append(f"  No specific brand names found")
        if not r['has_ingredient']:
            issues.append(f"  No specific ingredient names found")
        if not r['has_price']:
            issues.append(f"  No price information ($XX) found")

        if issues:
            print(f"\n[ID:{r['id']}] {r['title']}")
            for iss in issues:
                print(iss)
        else:
            print(f"\n[ID:{r['id']}] {r['title']} — ALL CHECKS PASSED")

    # --- Score ---
    print("\n" + "="*120)
    total_checks = len(results) * 10
    passed = 0
    for r in results:
        if r['word_ok']: passed += 1
        if r['h2_ok']: passed += 1
        if r['internal_ok']: passed += 1
        if r['has_faq']: passed += 1
        if not r['html_issues']: passed += 1
        if not r['duplicates']: passed += 1
        if r['has_amazon']: passed += 1
        if not r['long_paras']: passed += 1
        if not r['broken_links']: passed += 1
        if r['has_brand'] and r['has_ingredient']: passed += 1

    print(f"OVERALL SCORE: {passed}/{total_checks} checks passed ({100*passed//total_checks}%)")
    print("="*120)

if __name__ == "__main__":
    main()
