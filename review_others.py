#!/usr/bin/env python3
"""WordPress post quality review — checks 12 posts against 10-point checklist."""
import requests, re, json, sys
from html.parser import HTMLParser
from collections import Counter

SITE = "https://rhythmicaleskimo.com"
REST = f"{SITE}/wp-json/wp/v2"
USER = "cjy654377@gmail.com"
PASS = "Dkflekd1!!"

POST_IDS = [357, 394, 74, 72, 464, 61, 182, 178, 361, 404, 78, 186]


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
    text = strip_html(html_text)
    words = text.split()
    return len(words)


def count_h2(html_text):
    return len(re.findall(r'<h2[\s>]', html_text, re.IGNORECASE))


def count_internal_links(html_text):
    links = re.findall(r'href=["\']([^"\']+)["\']', html_text, re.IGNORECASE)
    internal = [l for l in links if 'rhythmicaleskimo.com' in l and '/wp-admin' not in l]
    return internal


def has_faq_schema(html_text):
    return 'FAQPage' in html_text


def check_broken_html(html_text):
    issues = []
    # Check for common broken patterns
    # Unclosed tags (simple check)
    void_tags = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
    open_tags = re.findall(r'<([a-zA-Z][a-zA-Z0-9]*)\b[^/>]*(?<!/)>', html_text)
    close_tags = re.findall(r'</([a-zA-Z][a-zA-Z0-9]*)\s*>', html_text)
    open_count = Counter(t.lower() for t in open_tags if t.lower() not in void_tags)
    close_count = Counter(t.lower() for t in close_tags)
    for tag in open_count:
        diff = open_count[tag] - close_count.get(tag, 0)
        if diff > 1:
            issues.append(f"Unclosed <{tag}> x{diff}")
    # Bad HTML entities
    bad_entities = re.findall(r'&[^;\s]{0,10}(?=\s|<|$)', html_text)
    if bad_entities:
        issues.append(f"Bad entities: {len(bad_entities)}")
    return issues


def check_duplicate_content(html_text):
    issues = []
    # Duplicate H2 titles
    h2s = re.findall(r'<h2[^>]*>(.*?)</h2>', html_text, re.IGNORECASE | re.DOTALL)
    h2_texts = [strip_html(h).strip() for h in h2s]
    h2_counter = Counter(h2_texts)
    for h2, cnt in h2_counter.items():
        if cnt > 1 and h2:
            issues.append(f"Dup H2: '{h2[:40]}' x{cnt}")
    # Duplicate sentences (50+ chars)
    text = strip_html(html_text)
    sentences = re.split(r'[.!?]\s+', text)
    long_sentences = [s.strip() for s in sentences if len(s.strip()) >= 50]
    sent_counter = Counter(long_sentences)
    for sent, cnt in sent_counter.items():
        if cnt > 1:
            issues.append(f"Dup sentence: '{sent[:50]}...' x{cnt}")
    return issues


def check_long_paragraphs(html_text):
    """Check for paragraphs with 200+ words."""
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
        except Exception as e:
            broken.append(f"{url} (error)")
    return broken


def check_content_consistency(title, html_text):
    """Basic check: title words should appear in content."""
    title_words = set(title.lower().split())
    stop_words = {'the','a','an','in','on','at','to','for','of','and','or','is','are','was','were',
                  'how','what','why','when','where','who','your','you','this','that','it','its',
                  'with','from','by','as','be','has','have','had','do','does','did','will','would',
                  'can','could','should','may','might','must','shall','about','into','through',
                  'during','before','after','above','below','between','under','over','up','down',
                  'out','off','then','than','so','if','but','not','no','nor','only','very','just',
                  'also','both','each','every','all','any','few','more','most','other','some','such',
                  'my','our','their','his','her','we','they','us','them','me','him','10','best','top',
                  '2024','2025','2026','guide','ultimate','-','&','|','—','–'}
    key_words = title_words - stop_words
    text_lower = strip_html(html_text).lower()
    missing = [w for w in key_words if w not in text_lower]
    return missing


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
        title = post['title']['raw'] if isinstance(post['title'], dict) else post['title'].get('rendered', str(post['title']))
        content = post['content']['raw'] if isinstance(post['content'], dict) else post['content'].get('rendered', str(post['content']))
        excerpt = post.get('excerpt', {})
        if isinstance(excerpt, dict):
            excerpt_text = excerpt.get('raw', excerpt.get('rendered', ''))
        else:
            excerpt_text = str(excerpt)

        # 1. Word count
        wc = word_count(content)

        # 2. H2 count
        h2c = count_h2(content)

        # 3. Internal links
        ilinks = count_internal_links(content)

        # 4. FAQ Schema
        faq = has_faq_schema(content)

        # 5. Broken HTML
        html_issues = check_broken_html(content)

        # 6. Duplicate content
        dup_issues = check_duplicate_content(content)

        # 7. Long paragraphs (mobile readability)
        long_paras = check_long_paragraphs(content)

        # 8. Broken internal links (collect, check later)
        all_internal_links.append((pid, ilinks))

        # 9. Content consistency
        missing_kw = check_content_consistency(title, content)

        # 10. Excerpt
        has_excerpt = bool(strip_html(excerpt_text).strip())

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
            'html_issues': html_issues,
            'dup_issues': dup_issues,
            'long_paras': long_paras,
            'broken_links': [],  # filled later
            'missing_kw': missing_kw,
            'excerpt': has_excerpt,
        }
        results.append(result)
        print(f"  OK: {pid} — {title[:50]}... ({wc} words)")

    # Check broken internal links
    print("\nChecking internal links...")
    link_map = {}
    for pid, links in all_internal_links:
        for r_item in results:
            if r_item['id'] == pid and 'error' not in r_item:
                broken = check_broken_links(s, links)
                r_item['broken_links'] = broken
                break

    # Print results table
    print("\n" + "="*120)
    print("POST QUALITY REVIEW — 12 Posts")
    print("="*120)

    header = f"{'ID':>4} | {'Title':<45} | {'Words':>5} | {'H2':>2} | {'Int.Lnk':>7} | {'FAQ':>3} | {'HTML':>4} | {'Dup':>3} | {'Long P':>6} | {'BrkLnk':>6} | {'Excrpt':>6} | {'Score':>5}"
    print(header)
    print("-"*120)

    total_issues = []

    for r in results:
        if 'error' in r:
            print(f"{r['id']:>4} | ERROR: {r['error']}")
            continue

        score = 0
        max_score = 10

        wc_str = f"{r['wc']:>5}"
        wc_flag = "OK" if r['wc_ok'] else "FAIL"
        if r['wc_ok']: score += 1

        h2_str = f"{r['h2']:>2}"
        h2_flag = "OK" if r['h2_ok'] else "FAIL"
        if r['h2_ok']: score += 1

        il_str = f"{r['ilinks']:>3}"
        il_flag = "OK" if r['ilinks_ok'] else "FAIL"
        if r['ilinks_ok']: score += 1

        faq_str = "Y" if r['faq'] else "N"
        if r['faq']: score += 1

        html_str = str(len(r['html_issues'])) if r['html_issues'] else "OK"
        if not r['html_issues']: score += 1

        dup_str = str(len(r['dup_issues'])) if r['dup_issues'] else "OK"
        if not r['dup_issues']: score += 1

        lp_str = str(len(r['long_paras'])) if r['long_paras'] else "OK"
        if not r['long_paras']: score += 1

        bl_str = str(len(r['broken_links'])) if r['broken_links'] else "OK"
        if not r['broken_links']: score += 1

        # Content consistency — if no important keywords missing, OK
        if not r['missing_kw']: score += 1

        exc_str = "Y" if r['excerpt'] else "N"
        if r['excerpt']: score += 1

        print(f"{r['id']:>4} | {r['title']:<45} | {wc_str} {wc_flag:<4} | {h2_str} {h2_flag:<4} | {il_str} {il_flag:<4} | {faq_str:>3} | {html_str:>4} | {dup_str:>3} | {lp_str:>6} | {bl_str:>6} | {exc_str:>6} | {score}/{max_score}")

        # Collect issues for detail report
        post_issues = []
        if not r['wc_ok']: post_issues.append(f"Word count: {r['wc']} (need 2500+)")
        if not r['h2_ok']: post_issues.append(f"H2 tags: {r['h2']} (need 4+)")
        if not r['ilinks_ok']: post_issues.append(f"Internal links: {r['ilinks']} (need 3+)")
        if not r['faq']: post_issues.append("No FAQ Schema")
        if r['html_issues']: post_issues.extend([f"HTML: {i}" for i in r['html_issues']])
        if r['dup_issues']: post_issues.extend([f"Dup: {i}" for i in r['dup_issues']])
        if r['long_paras']: post_issues.append(f"Long paragraphs: {r['long_paras']} words each")
        if r['broken_links']: post_issues.extend([f"Broken link: {b}" for b in r['broken_links']])
        if r['missing_kw']: post_issues.append(f"Title keywords not in content: {r['missing_kw']}")
        if not r['excerpt']: post_issues.append("No excerpt set")

        if post_issues:
            total_issues.append((r['id'], r['title'], post_issues))

    # Detail report
    if total_issues:
        print("\n" + "="*120)
        print("DETAILED ISSUES")
        print("="*120)
        for pid, title, issues in total_issues:
            print(f"\n[{pid}] {title}")
            for issue in issues:
                print(f"  - {issue}")

    # Summary
    print("\n" + "="*120)
    print("SUMMARY")
    print("="*120)
    valid = [r for r in results if 'error' not in r]
    print(f"Total posts reviewed: {len(valid)}/{len(POST_IDS)}")
    print(f"Posts with word count < 2500: {sum(1 for r in valid if not r['wc_ok'])}")
    print(f"Posts with H2 < 4: {sum(1 for r in valid if not r['h2_ok'])}")
    print(f"Posts with internal links < 3: {sum(1 for r in valid if not r['ilinks_ok'])}")
    print(f"Posts without FAQ Schema: {sum(1 for r in valid if not r['faq'])}")
    print(f"Posts with HTML issues: {sum(1 for r in valid if r['html_issues'])}")
    print(f"Posts with duplicate content: {sum(1 for r in valid if r['dup_issues'])}")
    print(f"Posts with long paragraphs: {sum(1 for r in valid if r['long_paras'])}")
    print(f"Posts with broken links: {sum(1 for r in valid if r['broken_links'])}")
    print(f"Posts without excerpt: {sum(1 for r in valid if not r['excerpt'])}")


if __name__ == "__main__":
    main()
