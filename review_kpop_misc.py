#!/usr/bin/env python3
"""WordPress post quality review — 10 posts (K-Pop + misc)."""
import requests, re, json, sys
from collections import Counter

SITE = "https://rhythmicaleskimo.com"
REST = f"{SITE}/wp-json/wp/v2"
USER = "cjy654377@gmail.com"
PASS = "Dkflekd1!!"

POST_IDS = [184, 393, 409, 411, 413, 464, 566, 606, 609, 612]


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


def strip_html(html_text):
    return re.sub(r'<[^>]+>', '', html_text)


def word_count(html_text):
    return len(strip_html(html_text).split())


def count_h2(html_text):
    return len(re.findall(r'<h2[\s>]', html_text, re.IGNORECASE))


def count_internal_links(html_text):
    links = re.findall(r'href=["\']([^"\']+)["\']', html_text, re.IGNORECASE)
    return [l for l in links if 'rhythmicaleskimo.com' in l and '/wp-admin' not in l]


def has_faq_schema(html_text):
    return 'FAQPage' in html_text


def check_broken_links(session, internal_links):
    broken = []
    checked = set()
    for url in internal_links:
        if url in checked:
            continue
        checked.add(url)
        try:
            r = session.head(url, timeout=10, allow_redirects=True)
            if r.status_code >= 400:
                broken.append(f"{url} ({r.status_code})")
        except:
            broken.append(f"{url} (error)")
    return broken


def check_duplicate_content(html_text):
    issues = []
    text = strip_html(html_text)
    sentences = re.split(r'[.!?]\s+', text)
    long_sentences = [s.strip() for s in sentences if len(s.strip()) >= 50]
    sent_counter = Counter(long_sentences)
    for sent, cnt in sent_counter.items():
        if cnt > 1:
            issues.append(f"'{sent[:50]}...' x{cnt}")
    return issues


def check_long_paragraphs(html_text):
    paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', html_text, re.IGNORECASE | re.DOTALL)
    long = []
    for p in paragraphs:
        wc = len(strip_html(p).split())
        if wc >= 200:
            long.append(wc)
    return long


def main():
    s, h = login()
    results = []

    print("Fetching posts...")
    for pid in POST_IDS:
        r = s.get(f"{REST}/posts/{pid}?context=edit", headers=h)
        if r.status_code != 200:
            print(f"  FAIL: Post {pid} — {r.status_code}")
            results.append({'id': pid, 'error': f"HTTP {r.status_code}"})
            continue

        post = r.json()
        title = post['title']['raw'] if isinstance(post['title'], dict) else str(post['title'])
        content = post['content']['raw'] if isinstance(post['content'], dict) else str(post['content'])
        excerpt = post.get('excerpt', {})
        if isinstance(excerpt, dict):
            excerpt_text = excerpt.get('raw', excerpt.get('rendered', ''))
        else:
            excerpt_text = str(excerpt)

        wc = word_count(content)
        h2c = count_h2(content)
        ilinks = count_internal_links(content)
        faq = has_faq_schema(content)
        dup_issues = check_duplicate_content(content)
        long_paras = check_long_paragraphs(content)
        broken = check_broken_links(s, ilinks)
        has_excerpt = bool(strip_html(excerpt_text).strip())

        result = {
            'id': pid, 'title': title[:55], 'wc': wc, 'h2': h2c,
            'ilinks': len(ilinks), 'faq': faq, 'dup_issues': dup_issues,
            'long_paras': long_paras, 'broken_links': broken,
            'excerpt': has_excerpt, 'ilink_urls': ilinks,
        }
        results.append(result)
        print(f"  OK: {pid} — {title[:50]}... ({wc}w)")

    # Print results table
    print("\n" + "=" * 130)
    print("POST QUALITY REVIEW — 10 Posts")
    print("=" * 130)
    print(f"{'ID':>4} | {'Title':<50} | {'Words':>5} | {'H2':>3} | {'IntLnk':>6} | {'FAQ':>3} | {'Dup':>3} | {'LongP':>5} | {'BrkLnk':>6} | {'Excrpt':>6}")
    print("-" * 130)

    total_issues = []
    for r in results:
        if 'error' in r:
            print(f"{r['id']:>4} | ERROR: {r['error']}")
            continue

        wc_s = f"{r['wc']:>5}" + (" OK" if r['wc'] >= 2500 else " !!")
        h2_s = f"{r['h2']:>3}" + (" OK" if r['h2'] >= 4 else " !!")
        il_s = f"{r['ilinks']:>3}" + ("  OK" if r['ilinks'] >= 3 else "  !!")
        faq_s = " Y " if r['faq'] else " N!"
        dup_s = f"{len(r['dup_issues']):>3}" if r['dup_issues'] else " OK"
        lp_s = f"{len(r['long_paras']):>3}" + f"({r['long_paras'][0]}w)" if r['long_paras'] else "   OK"
        bl_s = f"{len(r['broken_links']):>6}" if r['broken_links'] else "    OK"
        ex_s = "     Y" if r['excerpt'] else "    N!"

        print(f"{r['id']:>4} | {r['title']:<50} | {wc_s} | {h2_s} | {il_s} | {faq_s} | {dup_s} | {lp_s:>5} | {bl_s} | {ex_s}")

        # Collect issues
        issues = []
        if r['wc'] < 2500: issues.append(f"Word count: {r['wc']} (need 2500+)")
        if r['h2'] < 4: issues.append(f"H2: {r['h2']} (need 4+)")
        if r['ilinks'] < 3: issues.append(f"Internal links: {r['ilinks']} (need 3+)")
        if not r['faq']: issues.append("No FAQ Schema")
        if r['dup_issues']:
            for d in r['dup_issues']:
                issues.append(f"Dup: {d}")
        if r['long_paras']: issues.append(f"Long paragraphs: {r['long_paras']}w")
        if r['broken_links']:
            for b in r['broken_links']:
                issues.append(f"Broken: {b}")
        if not r['excerpt']: issues.append("No excerpt")
        if issues:
            total_issues.append((r['id'], r['title'], issues))

    # Detail report
    if total_issues:
        print("\n" + "=" * 130)
        print("DETAILED ISSUES")
        print("=" * 130)
        for pid, title, issues in total_issues:
            print(f"\n[{pid}] {title}")
            for issue in issues:
                print(f"  - {issue}")

    # Summary
    valid = [r for r in results if 'error' not in r]
    print("\n" + "=" * 130)
    print("SUMMARY")
    print("=" * 130)
    print(f"Posts reviewed: {len(valid)}/{len(POST_IDS)}")
    print(f"Word count < 2500: {sum(1 for r in valid if r['wc'] < 2500)}")
    print(f"H2 < 4:            {sum(1 for r in valid if r['h2'] < 4)}")
    print(f"Internal links < 3:{sum(1 for r in valid if r['ilinks'] < 3)}")
    print(f"No FAQ Schema:     {sum(1 for r in valid if not r['faq'])}")
    print(f"Duplicate content: {sum(1 for r in valid if r['dup_issues'])}")
    print(f"Long paragraphs:   {sum(1 for r in valid if r['long_paras'])}")
    print(f"Broken links:      {sum(1 for r in valid if r['broken_links'])}")
    print(f"No excerpt:        {sum(1 for r in valid if not r['excerpt'])}")


if __name__ == "__main__":
    main()
