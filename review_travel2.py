#!/usr/bin/env python3
"""WordPress post quality review — 14 posts (Travel & Food + misc)."""
import requests, re, json, sys
from html.parser import HTMLParser
from collections import Counter

SITE = "https://rhythmicaleskimo.com"
REST = f"{SITE}/wp-json/wp/v2"
USER = "cjy654377@gmail.com"
PASS = "Dkflekd1!!"

POST_IDS = [48, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 80, 180, 359]


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


def check_duplicate_content(html_text):
    issues = []
    h2s = re.findall(r'<h2[^>]*>(.*?)</h2>', html_text, re.IGNORECASE | re.DOTALL)
    h2_texts = [strip_html(h).strip() for h in h2s]
    h2_counter = Counter(h2_texts)
    for h2, cnt in h2_counter.items():
        if cnt > 1 and h2:
            issues.append(f"Dup H2: '{h2[:40]}' x{cnt}")
    text = strip_html(html_text)
    sentences = re.split(r'[.!?]\s+', text)
    long_sentences = [s.strip() for s in sentences if len(s.strip()) >= 50]
    sent_counter = Counter(long_sentences)
    for sent, cnt in sent_counter.items():
        if cnt > 1:
            issues.append(f"Dup sentence: '{sent[:50]}...' x{cnt}")
    return issues


def check_long_paragraphs(html_text):
    paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', html_text, re.IGNORECASE | re.DOTALL)
    long = []
    for p in paragraphs:
        text = strip_html(p)
        wc = len(text.split())
        if wc >= 200:
            long.append(wc)
    return long


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
        except Exception:
            broken.append(f"{url} (error)")
    return broken


def main():
    s, h = login()

    results = []
    all_internal_links = []

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
        has_excerpt = bool(strip_html(excerpt_text).strip())

        all_internal_links.append((pid, ilinks))

        result = {
            'id': pid,
            'title': title[:60],
            'wc': wc,
            'wc_ok': wc >= 2500,
            'h2': h2c,
            'h2_ok': h2c >= 4,
            'ilinks': len(ilinks),
            'ilinks_ok': len(ilinks) >= 3,
            'faq': faq,
            'dup_issues': dup_issues,
            'long_paras': long_paras,
            'broken_links': [],
            'excerpt': has_excerpt,
        }
        results.append(result)
        print(f"  OK: {pid} — {title[:50]}... ({wc} words)")

    print("\nChecking internal links...")
    for pid, links in all_internal_links:
        for r_item in results:
            if r_item['id'] == pid and 'error' not in r_item:
                broken = check_broken_links(s, links)
                r_item['broken_links'] = broken
                break

    # Print results table
    print("\n" + "=" * 130)
    print("POST QUALITY REVIEW — 14 Posts")
    print("=" * 130)

    header = f"{'ID':>4} | {'Title':<50} | {'Words':>5} | {'H2':>2} | {'IntLnk':>6} | {'FAQ':>3} | {'Dup':>3} | {'LongP':>5} | {'BrkLnk':>6} | {'Excrpt':>6}"
    print(header)
    print("-" * 130)

    total_issues = []

    for r in results:
        if 'error' in r:
            print(f"{r['id']:>4} | ERROR: {r['error']}")
            continue

        wc_flag = "OK" if r['wc_ok'] else "LOW"
        h2_flag = "OK" if r['h2_ok'] else "LOW"
        il_flag = "OK" if r['ilinks_ok'] else "LOW"
        faq_str = "Y" if r['faq'] else "N"
        dup_str = str(len(r['dup_issues'])) if r['dup_issues'] else "OK"
        lp_str = str(len(r['long_paras'])) if r['long_paras'] else "OK"
        bl_str = str(len(r['broken_links'])) if r['broken_links'] else "OK"
        exc_str = "Y" if r['excerpt'] else "N"

        print(f"{r['id']:>4} | {r['title']:<50} | {r['wc']:>5} {wc_flag:<3} | {r['h2']:>2} {h2_flag:<3} | {r['ilinks']:>3} {il_flag:<3} | {faq_str:>3} | {dup_str:>3} | {lp_str:>5} | {bl_str:>6} | {exc_str:>6}")

        post_issues = []
        if not r['wc_ok']: post_issues.append(f"Word count: {r['wc']} (need 2500+)")
        if not r['h2_ok']: post_issues.append(f"H2 tags: {r['h2']} (need 4+)")
        if not r['ilinks_ok']: post_issues.append(f"Internal links: {r['ilinks']} (need 3+)")
        if not r['faq']: post_issues.append("No FAQ Schema")
        if r['dup_issues']: post_issues.extend([f"Dup: {i}" for i in r['dup_issues']])
        if r['long_paras']: post_issues.append(f"Long paragraphs: {r['long_paras']} words each")
        if r['broken_links']: post_issues.extend([f"Broken link: {b}" for b in r['broken_links']])
        if not r['excerpt']: post_issues.append("No excerpt set")

        if post_issues:
            total_issues.append((r['id'], r['title'], post_issues))

    if total_issues:
        print("\n" + "=" * 130)
        print("DETAILED ISSUES")
        print("=" * 130)
        for pid, title, issues in total_issues:
            print(f"\n[{pid}] {title}")
            for issue in issues:
                print(f"  - {issue}")

    # Summary
    print("\n" + "=" * 130)
    print("SUMMARY")
    print("=" * 130)
    valid = [r for r in results if 'error' not in r]
    print(f"Total posts reviewed: {len(valid)}/{len(POST_IDS)}")
    print(f"Word count < 2500: {sum(1 for r in valid if not r['wc_ok'])}")
    print(f"H2 < 4: {sum(1 for r in valid if not r['h2_ok'])}")
    print(f"Internal links < 3: {sum(1 for r in valid if not r['ilinks_ok'])}")
    print(f"No FAQ Schema: {sum(1 for r in valid if not r['faq'])}")
    print(f"Duplicate content: {sum(1 for r in valid if r['dup_issues'])}")
    print(f"Long paragraphs (200w+): {sum(1 for r in valid if r['long_paras'])}")
    print(f"Broken links: {sum(1 for r in valid if r['broken_links'])}")
    print(f"No excerpt: {sum(1 for r in valid if not r['excerpt'])}")


if __name__ == "__main__":
    main()
