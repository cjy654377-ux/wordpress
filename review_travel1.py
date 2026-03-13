#!/usr/bin/env python3
"""WordPress post quality review — 14 Travel & Food posts."""
import requests, re, json, sys
from html.parser import HTMLParser
from collections import Counter

SITE = "https://rhythmicaleskimo.com"
REST = f"{SITE}/wp-json/wp/v2"
USER = "cjy654377@gmail.com"
PASS = "Dkflekd1!!"

POST_IDS = [11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 40, 42, 44, 46]


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
    text = strip_html(html_text)
    sentences = re.split(r'[.!?]\s+', text)
    long_sentences = [s.strip() for s in sentences if len(s.strip()) >= 50]
    sent_counter = Counter(long_sentences)
    for sent, cnt in sent_counter.items():
        if cnt > 1:
            issues.append(f"'{sent[:60]}...' x{cnt}")
    return issues


def check_long_paragraphs(html_text):
    paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', html_text, re.IGNORECASE | re.DOTALL)
    long = []
    for p in paragraphs:
        wc = len(strip_html(p).split())
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

    print("Fetching 14 Travel & Food posts...")
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
            'ilinks': len(ilinks), 'faq': faq,
            'dup_issues': dup_issues, 'long_paras': long_paras,
            'broken_links': broken, 'excerpt': has_excerpt,
        }
        results.append(result)
        bl_note = f" | {len(broken)} broken" if broken else ""
        print(f"  OK: {pid} — {wc}w, {h2c} H2, {len(ilinks)} links{bl_note}")

    # Print results table
    print("\n" + "=" * 130)
    print("TRAVEL & FOOD POST QUALITY REVIEW — 14 Posts")
    print("=" * 130)
    print(f"{'ID':>4} | {'Title':<50} | {'Words':>5} | {'H2':>3} | {'Links':>5} | {'FAQ':>3} | {'Dup':>3} | {'LongP':>5} | {'Brkn':>4} | {'Excrpt':>6} | {'Pass':>4}")
    print("-" * 130)

    total_issues = []
    pass_count = 0

    for r in results:
        if 'error' in r:
            print(f"{r['id']:>4} | ERROR: {r['error']}")
            continue

        checks = 0
        total = 8

        wc_ok = r['wc'] >= 2500
        if wc_ok: checks += 1

        h2_ok = r['h2'] >= 4
        if h2_ok: checks += 1

        il_ok = r['ilinks'] >= 3
        if il_ok: checks += 1

        if r['faq']: checks += 1
        if not r['dup_issues']: checks += 1
        if not r['long_paras']: checks += 1
        if not r['broken_links']: checks += 1
        if r['excerpt']: checks += 1

        wc_s = f"{r['wc']}" + ("" if wc_ok else "*")
        h2_s = f"{r['h2']}" + ("" if h2_ok else "*")
        il_s = f"{r['ilinks']}" + ("" if il_ok else "*")
        faq_s = "Y" if r['faq'] else "N*"
        dup_s = "OK" if not r['dup_issues'] else f"{len(r['dup_issues'])}*"
        lp_s = "OK" if not r['long_paras'] else f"{len(r['long_paras'])}*"
        bl_s = "OK" if not r['broken_links'] else f"{len(r['broken_links'])}*"
        ex_s = "Y" if r['excerpt'] else "N*"

        all_pass = checks == total
        if all_pass: pass_count += 1

        print(f"{r['id']:>4} | {r['title']:<50} | {wc_s:>5} | {h2_s:>3} | {il_s:>5} | {faq_s:>3} | {dup_s:>3} | {lp_s:>5} | {bl_s:>4} | {ex_s:>6} | {checks}/{total}")

        # Collect issues
        post_issues = []
        if not wc_ok: post_issues.append(f"Word count: {r['wc']} (need 2500+)")
        if not h2_ok: post_issues.append(f"H2 count: {r['h2']} (need 4+)")
        if not il_ok: post_issues.append(f"Internal links: {r['ilinks']} (need 3+)")
        if not r['faq']: post_issues.append("No FAQ Schema")
        if r['dup_issues']:
            for d in r['dup_issues']:
                post_issues.append(f"Duplicate: {d}")
        if r['long_paras']:
            post_issues.append(f"Long paragraphs: {r['long_paras']}w")
        if r['broken_links']:
            for b in r['broken_links']:
                post_issues.append(f"Broken link: {b}")
        if not r['excerpt']:
            post_issues.append("No excerpt set")

        if post_issues:
            total_issues.append((r['id'], r['title'], post_issues))

    # Detail report
    if total_issues:
        print("\n" + "=" * 130)
        print("DETAILED ISSUES (* = failed check)")
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
    print(f"Total reviewed: {len(valid)}/{len(POST_IDS)}")
    print(f"All checks passed: {pass_count}/{len(valid)}")
    print(f"Word count < 2500: {sum(1 for r in valid if r['wc'] < 2500)}")
    print(f"H2 < 4: {sum(1 for r in valid if r['h2'] < 4)}")
    print(f"Internal links < 3: {sum(1 for r in valid if r['ilinks'] < 3)}")
    print(f"No FAQ Schema: {sum(1 for r in valid if not r['faq'])}")
    print(f"Duplicate content: {sum(1 for r in valid if r['dup_issues'])}")
    print(f"Long paragraphs: {sum(1 for r in valid if r['long_paras'])}")
    print(f"Broken links: {sum(1 for r in valid if r['broken_links'])}")
    print(f"No excerpt: {sum(1 for r in valid if not r['excerpt'])}")


if __name__ == "__main__":
    main()
