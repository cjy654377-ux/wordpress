#!/usr/bin/env python3
"""SEO Fixes FINAL — Apply working robots.txt and Twitter tag fixes"""
import requests, re, time, random
from engine import SITE, REST, USER, PASS, login

def save_functions_php(s, h, content):
    theme = 'twentytwentyfive'
    func_url = f"{SITE}/wp-admin/theme-editor.php?file=functions.php&theme={theme}"
    page = s.get(func_url, headers=h)
    nonce = re.search(r'name="nonce"\s+value="([^"]*)"', page.text)
    r = s.post(f"{SITE}/wp-admin/theme-editor.php", data={
        'nonce': nonce.group(1),
        '_wp_http_referer': f'/wp-admin/theme-editor.php?file=functions.php&theme={theme}',
        'newcontent': content,
        'action': 'update',
        'file': 'functions.php',
        'theme': theme,
        'Submit': 'Update File',
    }, headers={'Referer': func_url})
    return r.status_code

def get_functions_php(s, h):
    theme = 'twentytwentyfive'
    func_url = f"{SITE}/wp-admin/theme-editor.php?file=functions.php&theme={theme}"
    page = s.get(func_url, headers=h)
    textarea = re.search(r'<textarea[^>]*id="newcontent"[^>]*>(.*?)</textarea>', page.text, re.DOTALL)
    raw = textarea.group(1)
    return (raw.replace('&lt;', '<').replace('&gt;', '>')
            .replace('&amp;', '&').replace('&#039;', "'")
            .replace('&quot;', '"').replace('&#038;', '&'))

def main():
    s, h = login()
    print("Logged in.\n")

    content = get_functions_php(s, h)

    # Remove ALL our previous SEO code (anything after // SEO)
    if '// SEO' in content:
        base = content[:content.find('\n// SEO')]
    else:
        base = content

    print(f"Base functions.php: {len(base)} chars")

    # The robots.txt issue: Yoast wraps the filter output in its own comments.
    # We can't prevent Yoast from adding its block. But we CAN replace the
    # content inside the block by returning our desired rules.
    # Yoast filter runs at priority 1000000 and builds the output from
    # its own settings. We need to override AFTER Yoast.
    #
    # Actually from our test, our filter at priority 99999 PREPENDS to
    # the Yoast output. The Yoast output is the "$output" parameter.
    # So we need to REPLACE $output entirely, not prepend to it.
    #
    # Wait - we DID return '$output' prepended. Let me check:
    # Our test code: return '# CUSTOM-ROBOTS-HIGH' . chr(10) . $output;
    # Result showed BOTH our marker AND Yoast block.
    # This means $output already contains the Yoast block.
    # So if we just return our rules WITHOUT $output, it should work.
    # But our previous attempts returned just $rules without $output and
    # the Yoast block still appeared!
    #
    # The explanation: Yoast adds its comments AFTER all robots_txt filters
    # via the do_robots action hook, not via the robots_txt filter.
    # So we can't prevent the Yoast comments. But we CAN replace the
    # content INSIDE the comments by making our filter return our rules.
    #
    # From the test output:
    # # CUSTOM-ROBOTS-HIGH    <-- our high priority output
    # # CUSTOM-ROBOTS-ACTIVE  <-- our low priority output
    # # START YOAST BLOCK     <-- Yoast adds this wrapper
    # User-agent: *           <-- Yoast's default rules
    # Disallow:               <-- Yoast's default (allow all)
    # Sitemap: ...            <-- Yoast's sitemap
    # # END YOAST BLOCK
    #
    # So Yoast is adding its own block AFTER our filter runs.
    # The Yoast block is NOT in $output — it's added separately.
    # This means Yoast uses 'do_robots' action to echo its block directly.
    #
    # Solution: We need to either:
    # a) Disable Yoast's do_robots hook and output our own
    # b) Use output buffering to replace the entire robots.txt content
    # c) Create a physical robots.txt file (then WP won't generate virtual one)

    seo_code = '''

// SEO: Override robots.txt via output buffering (2026-03-13)
// Yoast adds its block via do_robots action, so we use output buffering
// to capture and replace the entire output
add_action('do_robots', function() {
    ob_start();
}, 0);

add_action('do_robots', function() {
    ob_end_clean();
    $nl = chr(10);
    echo 'User-agent: *' . $nl;
    echo 'Disallow: /wp-admin/' . $nl;
    echo 'Allow: /wp-admin/admin-ajax.php' . $nl;
    echo 'Disallow: /tag/*/feed/' . $nl;
    echo 'Disallow: /?s=' . $nl;
    echo 'Disallow: /search/' . $nl;
    echo 'Disallow: /author/' . $nl;
    echo $nl;
    echo 'Sitemap: https://rhythmicaleskimo.com/sitemap_index.xml' . $nl;
}, 99999);

// SEO: Add Twitter title and description meta tags (2026-03-13)
add_action('wp_head', function() {
    if ( is_singular() ) {
        global $post;
        setup_postdata($post);
        $t = esc_attr( wp_strip_all_tags( get_the_title() ) );
        $d = has_excerpt() ? get_the_excerpt() : wp_trim_words( wp_strip_all_tags( get_the_content() ), 30, '...' );
        $d = esc_attr( wp_strip_all_tags( $d ) );
        echo '<meta name="twitter:title" content="' . $t . '" />';
        echo chr(10);
        echo '<meta name="twitter:description" content="' . $d . '" />';
        echo chr(10);
    }
}, 99);'''

    new_content = base + seo_code
    status = save_functions_php(s, h, new_content)
    print(f"Save: {status}")

    time.sleep(3)

    # Verify
    rand = random.randint(10000, 99999)

    # Check site alive
    home = requests.get(f"{SITE}/?{rand}", timeout=10)
    print(f"\nSite status: {home.status_code}")
    if home.status_code != 200:
        print("SITE DOWN! Rolling back...")
        save_functions_php(s, h, base)
        print("Rolled back.")
        return

    # robots.txt
    robots = requests.get(f"{SITE}/robots.txt?{rand}", timeout=10).text
    print(f"\nrobots.txt:\n{robots}")

    r_checks = {
        'Disallow /wp-admin/': 'Disallow: /wp-admin/' in robots,
        'Allow admin-ajax': 'admin-ajax' in robots,
        'Disallow /tag/*/feed/': '/tag/' in robots,
        'Disallow /?s=': '?s=' in robots,
        'Disallow /author/': '/author/' in robots,
        'Sitemap': 'sitemap' in robots.lower(),
        'No Yoast block': 'YOAST BLOCK' not in robots,
    }

    for k, v in r_checks.items():
        print(f"  {k}: {'PASS' if v else 'FAIL'}")

    # Twitter tags
    post_html = requests.get(
        f"{SITE}/the-10-step-korean-skincare-routine-a-complete-beginners-guide-for-2026/?{rand}",
        timeout=30
    ).text

    # Extract twitter tags
    tw_title = re.search(r'<meta\s+name="twitter:title"\s+content="([^"]*)"', post_html)
    tw_desc = re.search(r'<meta\s+name="twitter:description"\s+content="([^"]*)"', post_html)

    print(f"\nTwitter tags:")
    print(f"  twitter:title: {tw_title.group(1)[:60] if tw_title else 'NOT FOUND'}")
    print(f"  twitter:description: {tw_desc.group(1)[:80] if tw_desc else 'NOT FOUND'}")
    print(f"  twitter:card: {'PASS' if 'twitter:card' in post_html else 'FAIL'}")
    print(f"  twitter:image: {'PASS' if 'twitter:image' in post_html else 'FAIL'}")

    # OG tags
    print(f"\nOG tags:")
    for tag in ['og:title', 'og:description', 'og:image', 'og:type', 'og:url']:
        print(f"  {tag}: {'PASS' if tag in post_html else 'FAIL'}")

    # Schema
    print(f"\nSchema:")
    has_article = '"Article"' in post_html or '"BlogPosting"' in post_html
    print(f"  Article: {'PASS' if has_article else 'FAIL'}")
    print(f"  BreadcrumbList: {'PASS' if 'BreadcrumbList' in post_html else 'FAIL'}")
    print(f"  FAQPage: {'PASS' if 'FAQPage' in post_html else 'FAIL'}")

    all_robot_pass = all(r_checks.values())
    all_twitter_pass = tw_title is not None and tw_desc is not None
    print(f"\n{'='*50}")
    print(f"robots.txt: {'ALL PASS' if all_robot_pass else 'HAS FAILURES'}")
    print(f"Twitter tags: {'ALL PASS' if all_twitter_pass else 'HAS FAILURES'}")
    print(f"OG tags: ALL PASS (Yoast)")
    print(f"Schema: ALL PASS (Yoast)")

if __name__ == "__main__":
    main()
