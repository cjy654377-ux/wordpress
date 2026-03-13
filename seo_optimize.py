#!/usr/bin/env python3
"""SEO Technical Optimization — Check & Fix for rhythmicaleskimo.com"""
import requests, re, sys
from engine import SITE, REST, USER, PASS, login

def fetch_raw_html(url):
    """Fetch raw HTML without rendering"""
    r = requests.get(url, timeout=30, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    })
    return r.text

def check_robots_txt():
    print("=" * 60)
    print("1. ROBOTS.TXT CHECK")
    print("=" * 60)
    txt = fetch_raw_html(f"{SITE}/robots.txt")
    print(f"Current robots.txt:\n{txt}")

    issues = []
    if "/wp-admin/" not in txt:
        issues.append("Missing: Disallow /wp-admin/")
    if "sitemap" not in txt.lower():
        issues.append("Missing: Sitemap URL")
    if "/tag/" not in txt:
        issues.append("Missing: Disallow /tag/*/feed/ (tag feed spam)")
    if "/author/" not in txt:
        issues.append("Missing: Disallow /author/ (author archives)")
    if "/?s=" not in txt and "/search" not in txt:
        issues.append("Missing: Disallow /?s= (search results)")

    if issues:
        print(f"\nIssues found ({len(issues)}):")
        for i in issues:
            print(f"  - {i}")
    else:
        print("\nNo issues found.")

    return issues

def check_meta_tags():
    print("\n" + "=" * 60)
    print("2. OPEN GRAPH + TWITTER CARD META TAGS")
    print("=" * 60)

    # Check a specific post
    test_url = f"{SITE}/the-10-step-korean-skincare-routine-a-complete-beginners-guide-for-2026/"
    html = fetch_raw_html(test_url)

    # Extract head section
    head_match = re.search(r'<head[^>]*>(.*?)</head>', html, re.DOTALL)
    if not head_match:
        print("ERROR: Could not extract <head> section")
        return {}

    head = head_match.group(1)

    results = {}

    # OG tags
    og_tags = re.findall(r'<meta\s+property="(og:[^"]+)"\s+content="([^"]*)"', head)
    og_tags += re.findall(r'<meta\s+content="([^"]*)"\s+property="(og:[^"]+)"', head)

    print(f"\nURL checked: {test_url}")
    print(f"\nOpen Graph tags found: {len(og_tags)}")
    for prop, content in og_tags:
        if prop.startswith('og:'):
            print(f"  {prop} = {content[:80]}")
            results[prop] = content
        else:
            print(f"  {content} = {prop[:80]}")
            results[content] = prop

    # Twitter tags
    tw_tags = re.findall(r'<meta\s+name="(twitter:[^"]+)"\s+content="([^"]*)"', head)
    tw_tags += re.findall(r'<meta\s+content="([^"]*)"\s+name="(twitter:[^"]+)"', head)

    print(f"\nTwitter Card tags found: {len(tw_tags)}")
    for name, content in tw_tags:
        if name.startswith('twitter:'):
            print(f"  {name} = {content[:80]}")
            results[name] = content
        else:
            print(f"  {content} = {name[:80]}")
            results[content] = name

    # Canonical
    canonical = re.findall(r'<link\s+rel="canonical"\s+href="([^"]*)"', head)
    print(f"\nCanonical tag: {canonical[0] if canonical else 'NOT FOUND'}")

    # Check what's missing
    missing = []
    required_og = ['og:title', 'og:description', 'og:image', 'og:type', 'og:url']
    required_tw = ['twitter:card', 'twitter:title', 'twitter:description']

    for tag in required_og:
        if tag not in results:
            missing.append(tag)
    for tag in required_tw:
        if tag not in results:
            missing.append(tag)

    if missing:
        print(f"\nMissing tags: {', '.join(missing)}")
    else:
        print("\nAll required OG/Twitter tags present!")

    return {'results': results, 'missing': missing, 'head': head}

def check_schema(head=None):
    print("\n" + "=" * 60)
    print("3. ARTICLE SCHEMA (JSON-LD)")
    print("=" * 60)

    if head is None:
        html = fetch_raw_html(f"{SITE}/the-10-step-korean-skincare-routine-a-complete-beginners-guide-for-2026/")
        head_match = re.search(r'<head[^>]*>(.*?)</head>', html, re.DOTALL)
        head = head_match.group(1) if head_match else ""

    # Find JSON-LD scripts
    schemas = re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', head, re.DOTALL)

    print(f"\nJSON-LD schemas found: {len(schemas)}")

    has_article = False
    has_faq = False
    has_breadcrumb = False
    has_webpage = False

    for i, schema in enumerate(schemas):
        try:
            import json
            data = json.loads(schema)

            # Check @graph if present
            items = data.get('@graph', [data]) if isinstance(data, dict) else [data]

            for item in items:
                t = item.get('@type', '')
                if isinstance(t, list):
                    types = t
                else:
                    types = [t]

                for typ in types:
                    if typ == 'Article' or typ == 'NewsArticle' or typ == 'BlogPosting':
                        has_article = True
                        print(f"\n  Article Schema: YES")
                        print(f"    headline: {item.get('headline', 'N/A')[:60]}")
                        print(f"    datePublished: {item.get('datePublished', 'N/A')}")
                        print(f"    dateModified: {item.get('dateModified', 'N/A')}")
                        print(f"    wordCount: {item.get('wordCount', 'N/A')}")
                        author = item.get('author', {})
                        if isinstance(author, list):
                            author = author[0] if author else {}
                        print(f"    author: {author.get('name', 'N/A') if isinstance(author, dict) else 'N/A'}")
                    elif typ == 'FAQPage':
                        has_faq = True
                        entities = item.get('mainEntity', [])
                        print(f"\n  FAQPage Schema: YES ({len(entities)} questions)")
                    elif typ == 'BreadcrumbList':
                        has_breadcrumb = True
                        print(f"\n  BreadcrumbList Schema: YES")
                    elif typ == 'WebPage':
                        has_webpage = True
                        print(f"\n  WebPage Schema: YES")
        except json.JSONDecodeError:
            print(f"  Schema {i+1}: Invalid JSON")

    if not has_article:
        print("\n  WARNING: No Article schema found!")
    if not has_breadcrumb:
        print("\n  WARNING: No BreadcrumbList schema found!")

    return {'article': has_article, 'faq': has_faq, 'breadcrumb': has_breadcrumb}

def check_core_web_vitals():
    print("\n" + "=" * 60)
    print("4. CORE WEB VITALS BASIC CHECK")
    print("=" * 60)

    # Check homepage
    html = fetch_raw_html(SITE)

    print(f"\n  Homepage HTML size: {len(html):,} bytes ({len(html)/1024:.1f} KB)")

    # Check a post
    post_url = f"{SITE}/the-10-step-korean-skincare-routine-a-complete-beginners-guide-for-2026/"
    post_html = fetch_raw_html(post_url)

    print(f"  Post HTML size: {len(post_html):,} bytes ({len(post_html)/1024:.1f} KB)")

    # Image lazy loading
    all_imgs = re.findall(r'<img[^>]*>', post_html)
    lazy_imgs = [img for img in all_imgs if 'loading="lazy"' in img or "loading='lazy'" in img]
    eager_imgs = [img for img in all_imgs if 'loading="lazy"' not in img and "loading='lazy'" not in img]

    print(f"\n  Images total: {len(all_imgs)}")
    print(f"  Images with lazy loading: {len(lazy_imgs)}")
    print(f"  Images without lazy loading: {len(eager_imgs)}")

    if eager_imgs:
        print("  First 3 non-lazy images:")
        for img in eager_imgs[:3]:
            src = re.search(r'src="([^"]*)"', img)
            print(f"    - {src.group(1)[:80] if src else 'no src'}")

    # Render-blocking resources
    head_match = re.search(r'<head[^>]*>(.*?)</head>', post_html, re.DOTALL)
    head = head_match.group(1) if head_match else ""

    # Stylesheets in head (all are render-blocking by default)
    stylesheets = re.findall(r'<link[^>]*rel=["\']stylesheet["\'][^>]*href="([^"]*)"[^>]*/?\s*>', head)
    stylesheets += re.findall(r'<link[^>]*href="([^"]*)"[^>]*rel=["\']stylesheet["\'][^>]*/?\s*>', head)

    print(f"\n  Render-blocking stylesheets: {len(stylesheets)}")
    for ss in stylesheets[:10]:
        print(f"    - {ss.split('?')[0][-60:]}")

    # Scripts without async/defer
    all_scripts = re.findall(r'<script([^>]*)>', head)
    blocking_scripts = []
    for attrs in all_scripts:
        if 'async' not in attrs and 'defer' not in attrs and 'type="application/ld+json"' not in attrs and 'type="importmap"' not in attrs and 'type="module"' not in attrs:
            src = re.search(r'src="([^"]*)"', attrs)
            if src:
                blocking_scripts.append(src.group(1))

    print(f"\n  Render-blocking scripts (no async/defer): {len(blocking_scripts)}")
    for s in blocking_scripts[:5]:
        print(f"    - {s.split('?')[0][-60:]}")

    # Inline styles size
    inline_styles = re.findall(r'<style[^>]*>(.*?)</style>', head, re.DOTALL)
    total_inline = sum(len(s) for s in inline_styles)
    print(f"\n  Inline CSS in head: {total_inline:,} bytes ({len(inline_styles)} blocks)")

    return {
        'html_size': len(post_html),
        'total_imgs': len(all_imgs),
        'lazy_imgs': len(lazy_imgs),
        'stylesheets': len(stylesheets),
        'blocking_scripts': len(blocking_scripts),
        'inline_css_bytes': total_inline
    }

def fix_robots_txt(s, h):
    """Update robots.txt via Yoast SEO settings if possible, otherwise provide manual instructions"""
    print("\n" + "=" * 60)
    print("FIX: ROBOTS.TXT OPTIMIZATION")
    print("=" * 60)

    # Yoast manages robots.txt dynamically — we need to add rules via a custom plugin or filter
    # The best approach for WordPress is to use Yoast's robots.txt settings or WPCode

    # Check if we can access Yoast settings
    # Try the WP admin page for Yoast robots.txt editor
    page = s.get(f"{SITE}/wp-admin/admin.php?page=wpseo_tools&tool=file-editor", headers=h)

    if 'robots.txt' in page.text.lower() or 'file-editor' in page.text.lower():
        print("  Yoast file editor accessible.")

        # Extract the current robots.txt content and nonce from the form
        nonce_match = re.search(r'name="_wpnonce"\s+value="([^"]*)"', page.text)

        if nonce_match:
            nonce = nonce_match.group(1)

            new_robots = """# START YOAST BLOCK
# ---------------------------
User-agent: *
Disallow: /wp-admin/
Allow: /wp-admin/admin-ajax.php
Disallow: /tag/*/feed/
Disallow: /?s=
Disallow: /search/
Disallow: /author/
Disallow: /wp-json/
Allow: /wp-json/wp/v2/

Sitemap: https://rhythmicaleskimo.com/sitemap_index.xml
# ---------------------------
# END YOAST BLOCK"""

            # Submit the form
            data = {
                '_wpnonce': nonce,
                'robotsnew': new_robots,
                'submitrobots': 'Save changes to robots.txt'
            }
            r = s.post(f"{SITE}/wp-admin/admin.php?page=wpseo_tools&tool=file-editor",
                       data=data, headers={'Referer': f"{SITE}/wp-admin/admin.php?page=wpseo_tools&tool=file-editor"})

            if r.status_code == 200:
                # Verify
                verify = fetch_raw_html(f"{SITE}/robots.txt")
                if '/wp-admin/' in verify:
                    print("  robots.txt updated successfully!")
                    print(f"\nNew robots.txt:\n{verify}")
                    return True
                else:
                    print("  Update may not have taken effect. Trying alternative...")
            else:
                print(f"  Form submission returned {r.status_code}")

    # Alternative: Use WPCode to add a filter
    print("\n  Trying WPCode approach to modify robots.txt via wp_robots filter...")

    # Check WPCode snippets
    snippets = s.get(f"{REST}/posts?per_page=100&post_type=wpcode", headers=h)

    # The most reliable approach: create a PHP snippet via WPCode
    # Let's check if WPCode is available
    wpcode_page = s.get(f"{SITE}/wp-admin/admin.php?page=wpcode-snippet-manager", headers=h)

    if wpcode_page.status_code == 200 and 'wpcode' in wpcode_page.text.lower():
        print("  WPCode is available. Creating robots.txt filter snippet...")

        # Get the add-new page nonce
        add_page = s.get(f"{SITE}/wp-admin/admin.php?page=wpcode-snippet-manager&snippet_id=0", headers=h)

        snippet_nonce = re.search(r'name="wpcode_security"\s+value="([^"]*)"', add_page.text)
        if not snippet_nonce:
            snippet_nonce = re.search(r'"wpcode_security":"([^"]*)"', add_page.text)

        if snippet_nonce:
            php_code = """// Optimize robots.txt for SEO
add_filter('robots_txt', function($output, $public) {
    $custom = "User-agent: *\\n";
    $custom .= "Disallow: /wp-admin/\\n";
    $custom .= "Allow: /wp-admin/admin-ajax.php\\n";
    $custom .= "Disallow: /tag/*/feed/\\n";
    $custom .= "Disallow: /?s=\\n";
    $custom .= "Disallow: /search/\\n";
    $custom .= "Disallow: /author/\\n";
    $custom .= "\\n";
    $custom .= "Sitemap: https://rhythmicaleskimo.com/sitemap_index.xml\\n";
    return $custom;
}, 10, 2);"""

            print(f"  PHP snippet prepared. Manual steps needed:")
            print(f"  1. Go to WP Admin > WPCode > Add Snippet")
            print(f"  2. Choose 'Add Your Custom Code (New Snippet)'")
            print(f"  3. Code Type: PHP Snippet")
            print(f"  4. Paste the robots.txt filter code")
            print(f"  5. Activate and save")

    print("\n  Alternative: Manually edit via Yoast > Tools > File Editor")
    return False


def fix_og_twitter_tags(s, h, missing_tags):
    """Check and fix OG/Twitter tags"""
    print("\n" + "=" * 60)
    print("FIX: OPEN GRAPH + TWITTER CARD TAGS")
    print("=" * 60)

    if not missing_tags:
        print("  All OG/Twitter tags are present. No fix needed.")
        return True

    print(f"  Missing tags: {', '.join(missing_tags)}")

    # Check Yoast Social settings
    # Yoast should auto-generate these. Let's check Yoast Social settings
    social_page = s.get(f"{SITE}/wp-admin/admin.php?page=wpseo_social", headers=h)

    if social_page.status_code == 200:
        # Check if OpenGraph is enabled
        og_enabled = 'opengraph' in social_page.text.lower()
        twitter_enabled = 'twitter' in social_page.text.lower()

        print(f"  Yoast Social settings page accessible: YES")

        # Check for the checkbox states
        og_checkbox = re.search(r'id="opengraph"[^>]*checked', social_page.text)
        tw_checkbox = re.search(r'id="twitter"[^>]*checked', social_page.text)

        if not og_checkbox:
            og_checkbox = re.search(r'name="opengraph"[^>]*checked', social_page.text)
        if not tw_checkbox:
            tw_checkbox = re.search(r'name="twitter"[^>]*checked', social_page.text)

        print(f"  OpenGraph enabled in Yoast: {'YES' if og_checkbox else 'UNCLEAR (check manually)'}")
        print(f"  Twitter Card enabled in Yoast: {'YES' if tw_checkbox else 'UNCLEAR (check manually)'}")

    # The issue might be that Yoast generates them but they're in the body or after head
    # Let's do a full-page check
    test_url = f"{SITE}/the-10-step-korean-skincare-routine-a-complete-beginners-guide-for-2026/"
    full_html = fetch_raw_html(test_url)

    # Search entire HTML for OG tags (not just head)
    og_anywhere = re.findall(r'<meta\s+property="(og:[^"]+)"', full_html)
    tw_anywhere = re.findall(r'<meta\s+name="(twitter:[^"]+)"', full_html)

    print(f"\n  OG tags in full HTML: {og_anywhere}")
    print(f"  Twitter tags in full HTML: {tw_anywhere}")

    if og_anywhere and tw_anywhere:
        print("  Tags ARE present in the HTML! The head extraction regex may have been too narrow.")
        return True

    # If truly missing, Yoast settings need to be enabled
    if not og_anywhere:
        print("\n  OG tags genuinely missing. Yoast Social > Facebook > Enable Open Graph needs to be ON.")
        print("  Fix: Navigate to WP Admin > Yoast SEO > Social > Facebook > 'Add Open Graph meta data' = ON")

    if not tw_anywhere:
        print("\n  Twitter tags genuinely missing. Yoast Social > Twitter needs to be enabled.")
        print("  Fix: Navigate to WP Admin > Yoast SEO > Social > Twitter > 'Add Twitter card meta data' = ON")

    # Try to enable via Yoast REST API
    try:
        # Yoast settings endpoint
        yoast_settings = s.get(f"{SITE}/wp-json/yoast/v1/configuration", headers=h)
        if yoast_settings.status_code == 200:
            print(f"\n  Yoast API accessible. Checking configuration...")
            import json
            config = yoast_settings.json()
            print(f"  Yoast config keys: {list(config.keys())[:10]}")
    except Exception as e:
        print(f"  Yoast API check failed: {e}")

    return False


def main():
    print("SEO Technical Optimization Check")
    print(f"Site: {SITE}")
    print("=" * 60)

    # 1. Check robots.txt
    robots_issues = check_robots_txt()

    # 2. Check OG + Twitter tags
    meta_info = check_meta_tags()

    # 3. Check Schema
    check_schema(meta_info.get('head'))

    # 4. Check Core Web Vitals
    cwv = check_core_web_vitals()

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY & FIXES NEEDED")
    print("=" * 60)

    fixes_needed = []

    if robots_issues:
        fixes_needed.append(f"robots.txt: {len(robots_issues)} issues")

    missing = meta_info.get('missing', [])
    if missing:
        fixes_needed.append(f"Meta tags: {len(missing)} missing ({', '.join(missing)})")

    if cwv.get('total_imgs', 0) > 0 and cwv.get('lazy_imgs', 0) < cwv.get('total_imgs', 0):
        non_lazy = cwv['total_imgs'] - cwv['lazy_imgs']
        fixes_needed.append(f"Lazy loading: {non_lazy}/{cwv['total_imgs']} images not lazy-loaded")

    if cwv.get('blocking_scripts', 0) > 0:
        fixes_needed.append(f"Render-blocking scripts: {cwv['blocking_scripts']}")

    if cwv.get('html_size', 0) > 200000:
        fixes_needed.append(f"Large HTML: {cwv['html_size']/1024:.0f} KB (consider optimization)")

    if cwv.get('inline_css_bytes', 0) > 50000:
        fixes_needed.append(f"Large inline CSS: {cwv['inline_css_bytes']/1024:.0f} KB")

    if fixes_needed:
        print(f"\n{len(fixes_needed)} areas need attention:")
        for i, fix in enumerate(fixes_needed, 1):
            print(f"  {i}. {fix}")
    else:
        print("\nAll checks passed!")

    # Apply fixes
    if robots_issues or missing:
        print("\n\nAPPLYING FIXES...")
        s, h = login()

        if robots_issues:
            fix_robots_txt(s, h)

        if missing:
            fix_og_twitter_tags(s, h, missing)

    print("\n\nDone.")

if __name__ == "__main__":
    main()
