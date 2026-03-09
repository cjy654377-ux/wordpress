#!/usr/bin/env python3
"""Insert Amazon affiliate links into K-Beauty WordPress posts.

Usage:
    python3 insert_affiliate_links.py              # dry-run (preview changes)
    python3 insert_affiliate_links.py --apply      # apply changes to WordPress

Auth: Set WP_APP_PASSWORD env var for Application Password auth, or update PASS below.
    export WP_APP_PASSWORD="xxxx xxxx xxxx xxxx xxxx xxxx"
"""
import requests, re, sys, time, os

SITE = "https://rhythmicaleskimo.com"
REST = f"{SITE}/wp-json/wp/v2"
USER = "cjy654377@gmail.com"
PASS = os.environ.get("WP_APP_PASSWORD", "Dkflekd1!!")
TAG = "rhythmicalesk-20"

# ── Product → ASIN mapping (verified Amazon ASINs) ──────────────────────────

PRODUCT_DB = {
    # (search_key, asin, display_name) — sorted by specificity (longest keys first applied)
    "Beauty of Joseon Relief Sun":  ("B0DB1NPDNX", "Beauty of Joseon Relief Sun"),
    "Beauty of Joseon":             ("B0DB1NPDNX", "Beauty of Joseon Relief Sun"),
    "Isntree Hyaluronic Acid":      ("B0C7B55GS3", "Isntree Hyaluronic Acid Sun Gel"),
    "ISNTREE":                      ("B0C7B55GS3", "Isntree Hyaluronic Acid Sun Gel"),
    "Isntree":                      ("B0C7B55GS3", "Isntree Hyaluronic Acid Sun Gel"),
    "Innisfree Daily UV":           ("B08WZS7LVN", "Innisfree Daily UV Defense Sunscreen"),
    "Innisfree":                    ("B08WZS7LVN", "Innisfree Daily UV Defense Sunscreen"),
    "PURITO Daily Go-To":           ("B09FF3V818", "PURITO Daily Go-To Sunscreen"),
    "PURITO":                       ("B09FF3V818", "PURITO Daily Go-To Sunscreen"),
    "Round Lab Birch":              ("B0DJGWH3TC", "Round Lab Birch Juice Sunscreen"),
    "Round Lab":                    ("B0DJGWH3TC", "Round Lab Birch Juice Sunscreen"),
    "ROUND LAB":                    ("B0DJGWH3TC", "Round Lab Birch Juice Sunscreen"),
    "COSRX Snail Mucin":            ("B00PBX3L7K", "COSRX Snail Mucin 96 Essence"),
    "COSRX Snail 96":               ("B00PBX3L7K", "COSRX Snail Mucin 96 Essence"),
    "Snail Mucin":                  ("B00PBX3L7K", "COSRX Snail Mucin 96 Essence"),
    "Snail 96":                     ("B00PBX3L7K", "COSRX Snail Mucin 96 Essence"),
    "COSRX BHA Blackhead":          ("B00OZEJ8R8", "COSRX BHA Blackhead Power Liquid"),
    "COSRX Aloe":                   ("B00PBX3L7K", "COSRX Snail Mucin 96 Essence"),
    "COSRX":                        ("B00PBX3L7K", "COSRX Snail Mucin 96 Essence"),
    "Torriden DIVE-IN":             ("B07WZ2YTDP", "Torriden DIVE-IN HA Serum"),
    "Torriden Dive-In":             ("B07WZ2YTDP", "Torriden DIVE-IN HA Serum"),
    "Torriden":                     ("B07WZ2YTDP", "Torriden DIVE-IN HA Serum"),
    "Anua Heartleaf":               ("B08CMS8P67", "Anua Heartleaf 77% Soothing Toner"),
    "Anua":                         ("B08CMS8P67", "Anua Heartleaf 77% Soothing Toner"),
    "SKIN1004 Madagascar":          ("B06Y15D1LH", "SKIN1004 Centella Ampoule"),
    "SKIN1004":                     ("B06Y15D1LH", "SKIN1004 Centella Ampoule"),
    "mixsoon Bean":                 ("B08ZXVVY8M", "mixsoon Bean Essence"),
    "mixsoon":                      ("B08ZXVVY8M", "mixsoon Bean Essence"),
    "Sulwhasoo First Care":         ("B00AHTK5WC", "Sulwhasoo First Care Activating Serum"),
    "Sulwhasoo":                    ("B00AHTK5WC", "Sulwhasoo First Care Activating Serum"),
    "Missha Time Revolution":       ("B09646RFWJ", "Missha Time Revolution Essence"),
    "MISSHA":                       ("B09646RFWJ", "Missha Time Revolution Essence"),
    "Missha":                       ("B09646RFWJ", "Missha Time Revolution Essence"),
    "Numbuzin No.3":                ("B0915K6WD3", "Numbuzin No.3 Skin Softening Serum"),
    "numbuzin":                     ("B0915K6WD3", "Numbuzin No.3 Skin Softening Serum"),
    "Numbuzin":                     ("B0915K6WD3", "Numbuzin No.3 Skin Softening Serum"),
    "Klairs Supple":                ("B07B65NJLV", "Klairs Supple Preparation Toner"),
    "Klairs":                       ("B07B65NJLV", "Klairs Supple Preparation Toner"),
    "Some By Mi AHA":               ("B07BYJF7L7", "Some By Mi 30 Days Miracle Toner"),
    "SOME BY MI":                   ("B07BYJF7L7", "Some By Mi 30 Days Miracle Toner"),
    "Some By Mi":                   ("B07BYJF7L7", "Some By Mi 30 Days Miracle Toner"),
    "30 Days Miracle":              ("B07BYJF7L7", "Some By Mi 30 Days Miracle Toner"),
    "Laneige Water Sleeping":       ("B09HN8JBFP", "Laneige Water Sleeping Mask"),
    "LANEIGE":                      ("B09HN8JBFP", "Laneige Water Sleeping Mask"),
    "Laneige":                      ("B09HN8JBFP", "Laneige Water Sleeping Mask"),
    "SoonJung":                     ("B091PN6NPT", "Etude SoonJung 2x Barrier Cream"),
    "Etude SoonJung":               ("B091PN6NPT", "Etude SoonJung 2x Barrier Cream"),
    "Etude":                        ("B091PN6NPT", "Etude SoonJung 2x Barrier Cream"),
    "Dr.G Red Blemish":             ("B0DCLVDH64", "Dr.G Red Blemish Soothing Cream"),
    "Dr.G Green Mild":              ("B0DCLVDH64", "Dr.G Red Blemish Soothing Cream"),
    "Dr.G":                         ("B0DCLVDH64", "Dr.G Red Blemish Soothing Cream"),
    "Banila Co Clean It Zero":      ("B0CW7LGBB6", "Banila Co Clean It Zero"),
    "Clean It Zero":                ("B0CW7LGBB6", "Banila Co Clean It Zero"),
    "Banila Co":                    ("B0CW7LGBB6", "Banila Co Clean It Zero"),
    "Medicube Age-R Booster":       ("B0CWK6YQ7V", "Medicube Age-R Booster Pro"),
    "Age-R Booster Pro":            ("B0CWK6YQ7V", "Medicube Age-R Booster Pro"),
    "Booster Pro":                  ("B0CWK6YQ7V", "Medicube Age-R Booster Pro"),
    "Age-R":                        ("B0CWK6YQ7V", "Medicube Age-R Booster Pro"),
    "Medicube PDRN":                ("B0DBF65JYY", "Medicube PDRN Peptide Serum"),
    "PDRN Peptide Serum":           ("B0DBF65JYY", "Medicube PDRN Peptide Serum"),
    "Zero Pore Pad":                ("B09V7Z4TJG", "Medicube Zero Pore Pad 2.0"),
    "Zero Pore":                    ("B09V7Z4TJG", "Medicube Zero Pore Pad 2.0"),
    "Medicube":                     ("B0CWK6YQ7V", "Medicube Age-R Booster Pro"),
    "Aromatica Rosemary":           ("B01NBJ9LTS", "Aromatica Rosemary Scalp Shampoo"),
    "Aromatica":                    ("B01NBJ9LTS", "Aromatica Rosemary Scalp Shampoo"),
    "Rosemary Scalp":               ("B01NBJ9LTS", "Aromatica Rosemary Scalp Shampoo"),
}

# Target post slugs
TARGET_SLUGS = [
    "best-korean-sunscreens-2026-dermatologist-approved-spf-for-every-skin-type",
    "the-complete-korean-skincare-routine-for-oily-skin-7-steps-that-actually-work",
    "pdrn-skincare-explained-why-salmon-dna-is-koreas-hottest-beauty-ingredient-in-2026",
    "korean-scalp-care-the-k-beauty-secret-to-thicker-healthier-hair",
    "medicube-age-r-review-2026-is-koreas-viral-at-home-beauty-device-worth-it",
    "korean-peptide-serums-the-science-behind-koreas-anti-aging-revolution",
    "post-procedure-korean-skincare-what-korean-dermatologists-recommend-after-botox-lasers-peels",
    "top-7-k-beauty-trends-dominating-2026-pdrn-exosomes-and-the-science-behind-korean-skincares-revolution",
    "the-10-step-korean-skincare-routine-a-complete-beginners-guide-for-2026",
    "olive-young-shopping-guide-top-15-k-beauty-products-under-15-that-actually-work",
]

# ── Helpers ──────────────────────────────────────────────────────────────────

def make_link(asin):
    return (f'<a href="https://www.amazon.com/dp/{asin}?tag={TAG}" '
            f'target="_blank" rel="nofollow sponsored" '
            f'style="color:#d63031;font-weight:bold;">Check Price &rarr;</a>')


def already_has_affiliate(content):
    return f"tag={TAG}" in content or "amazon.com/dp/" in content.lower()


def login():
    """Authenticate via cookie auth or Application Password (Basic Auth)."""

    # Method 1: Try Application Password (Basic Auth) first
    s = requests.Session()
    s.auth = (USER, PASS)
    r = s.get(f"{REST}/users/me")
    if r.status_code == 200:
        print(f"  Authenticated as: {r.json().get('name')} (Application Password)")
        return s, {}

    # Method 2: Try cookie auth
    s = requests.Session()
    s.cookies.set("wordpress_test_cookie", "WP+Cookie+check")
    s.post(f"{SITE}/wp-login.php", data={
        "log": USER, "pwd": PASS, "wp-submit": "Log In",
        "redirect_to": "/wp-admin/", "testcookie": "1"
    }, allow_redirects=True)

    page = s.get(f"{SITE}/wp-admin/post-new.php").text
    m = re.search(r'"nonce":"([a-f0-9]+)"', page)
    if not m:
        r = s.post(f"{SITE}/wp-admin/admin-ajax.php", data={"action": "rest-nonce"})
        nonce = r.text.strip()
        if not nonce or nonce == "0":
            print("ERROR: Could not obtain REST API nonce"); sys.exit(1)
    else:
        nonce = m.group(1)
    return s, {"X-WP-Nonce": nonce}


# ── Content Insertion Engine ─────────────────────────────────────────────────

def insert_links(content):
    """Insert affiliate links into post content.

    Strategies (in order):
    1. Add "Shop" column to product tables
    2. Insert link after <h3>/<h4> product headings
    3. Insert link after <strong> product mentions
    4. Insert link after first paragraph mention
    """
    if already_has_affiliate(content):
        return content, 0

    inserted_asins = set()
    count = 0
    sorted_keys = sorted(PRODUCT_DB.keys(), key=len, reverse=True)

    # ── Strategy 1: Add Shop column to tables ────────────────────────────
    # Find tables with product names and add a "Shop" column
    table_pattern = re.compile(r'(<table[^>]*class="rk-tbl"[^>]*>)(.*?)(</table>)', re.DOTALL)
    for tm in table_pattern.finditer(content):
        table_html = tm.group(2)
        new_table = table_html
        modified = False

        # Add "Shop" header to <th> row
        th_row_match = re.search(r'(<tr>\s*(?:<th[^>]*>.*?</th>\s*)+)(</tr>)', new_table, re.DOTALL)
        if th_row_match:
            new_table = new_table[:th_row_match.end(1)] + '<th>Shop</th>' + new_table[th_row_match.end(1):]

        # Process each data row
        rows = list(re.finditer(r'<tr>\s*(<td.*?</td>\s*)+</tr>', new_table, re.DOTALL))
        # Re-parse after header modification
        new_table_rows = re.split(r'(?=<tr>)', new_table)
        rebuilt = []
        for row in new_table_rows:
            if not row.strip():
                rebuilt.append(row)
                continue
            if '<th' in row:
                rebuilt.append(row)
                continue

            # Check if this row mentions any product
            link_added = False
            for key in sorted_keys:
                if key.lower() in row.lower():
                    asin, name = PRODUCT_DB[key]
                    if asin not in inserted_asins:
                        # Add Shop cell before </tr>
                        shop_cell = f'<td style="text-align:center">{make_link(asin)}</td>'
                        row = row.rstrip()
                        if row.endswith('</tr>'):
                            row = row[:-5] + shop_cell + '</tr>'
                        inserted_asins.add(asin)
                        count += 1
                        link_added = True
                        modified = True
                        break
            if not link_added and '<td' in row:
                # Add empty cell to maintain table structure
                row = row.rstrip()
                if row.endswith('</tr>'):
                    row = row[:-5] + '<td></td></tr>'
            rebuilt.append(row)

        if modified:
            new_table = ''.join(rebuilt)
            content = content[:tm.start(2)] + new_table + content[tm.end(2):]

    # ── Strategy 2: Insert after product headings (h2/h3/h4) ────────────
    for key in sorted_keys:
        asin, name = PRODUCT_DB[key]
        if asin in inserted_asins:
            continue

        h_pattern = re.compile(
            r'(<h[2-4][^>]*>[^<]*?' + re.escape(key) + r'[^<]*?</h[2-4]>)',
            re.IGNORECASE
        )
        m = h_pattern.search(content)
        if m:
            link_block = f'\n<p style="margin:5px 0 15px;">{make_link(asin)}</p>'
            content = content[:m.end()] + link_block + content[m.end():]
            inserted_asins.add(asin)
            count += 1

    # ── Strategy 3: Insert after <strong> product mention ────────────────
    for key in sorted_keys:
        asin, name = PRODUCT_DB[key]
        if asin in inserted_asins:
            continue

        strong_pattern = re.compile(
            r'(<strong>[^<]*?' + re.escape(key) + r'[^<]*?</strong>)',
            re.IGNORECASE
        )
        m = strong_pattern.search(content)
        if m:
            content = content[:m.end()] + ' ' + make_link(asin) + content[m.end():]
            inserted_asins.add(asin)
            count += 1

    # ── Strategy 4: Insert inline after first paragraph mention ──────────
    for key in sorted_keys:
        asin, name = PRODUCT_DB[key]
        if asin in inserted_asins:
            continue

        # Only match if the key appears in a paragraph or list context
        # Avoid matching inside HTML tags or attributes
        p = re.compile(r'(?<=>)([^<]*?)(' + re.escape(key) + r')([^<]*?)(?=<)', re.IGNORECASE)
        m = p.search(content)
        if m:
            # Insert after the matched text segment
            insert_pos = m.start(2) + len(m.group(2))
            content = content[:insert_pos] + ' (' + make_link(asin) + ')' + content[insert_pos:]
            inserted_asins.add(asin)
            count += 1

    return content, count


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    apply_mode = "--apply" in sys.argv
    mode = "APPLY" if apply_mode else "DRY-RUN"
    print(f"=== Amazon Affiliate Link Inserter [{mode}] ===\n")

    # Read posts via public API (no auth needed)
    print("[1] Fetching K-Beauty posts (public API)...")
    posts = []
    for slug in TARGET_SLUGS:
        r = requests.get(f"{REST}/posts", params={"slug": slug, "per_page": 1})
        if r.status_code == 200 and r.json():
            post = r.json()[0]
            posts.append(post)
            print(f"  OK: {post['title']['rendered'][:60]}... (ID:{post['id']})")
        else:
            print(f"  NOT FOUND: {slug}")
        time.sleep(0.3)
    print(f"  Total: {len(posts)} posts found.\n")

    if not posts:
        print("No posts found."); return

    # Process each post
    print("[2] Processing posts...\n")
    results = []
    for post in posts:
        title = post["title"]["rendered"]
        content = post["content"]["rendered"]
        post_id = post["id"]

        if already_has_affiliate(content):
            print(f"  SKIP (already has links): {title[:55]}...")
            results.append((post_id, title, None, 0))
            continue

        new_content, count = insert_links(content)
        results.append((post_id, title, new_content, count))
        print(f"  PROCESSED: {title[:55]}... → {count} links inserted")

    # Summary
    total_links = sum(r[3] for r in results)
    to_update = [(pid, title, c, n) for pid, title, c, n in results if c and n > 0]
    print(f"\n  Total links to insert: {total_links} across {len(to_update)} posts")

    if not to_update:
        print("\n  Nothing to update."); return

    if not apply_mode:
        print("\n  [DRY-RUN] No changes applied.")
        print("  Run with --apply to update WordPress posts.")

        # Save preview to file for inspection
        preview_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "affiliate_preview.html")
        with open(preview_path, "w") as f:
            f.write("<html><head><meta charset='utf-8'><title>Affiliate Preview</title></head><body>\n")
            for pid, title, new_content, count in to_update:
                f.write(f"<h1>{title} ({count} links)</h1>\n<hr>\n{new_content}\n<hr><br>\n")
            f.write("</body></html>")
        print(f"  Preview saved to: {preview_path}")
        return

    # Apply changes
    print("\n[3] Applying changes to WordPress...")
    s = requests.Session()
    s.cookies.set("wordpress_test_cookie", "WP+Cookie+check")
    s.post(f"{SITE}/wp-login.php", data={
        "log": USER, "pwd": PASS, "wp-submit": "Log In",
        "redirect_to": "/wp-admin/", "testcookie": "1"
    }, allow_redirects=True)
    page = s.get(f"{SITE}/wp-admin/post-new.php").text
    m_nonce = re.search(r'"nonce":"([a-f0-9]+)"', page)
    if not m_nonce:
        print("ERROR: nonce not found"); return
    h = {"X-WP-Nonce": m_nonce.group(1)}
    updated = 0
    for pid, title, new_content, count in to_update:
        r = s.post(f"{REST}/posts/{pid}", headers=h, json={"content": new_content})
        if r.status_code == 200:
            print(f"  UPDATED: {title[:55]}... ({count} links)")
            updated += 1
        else:
            print(f"  FAILED ({r.status_code}): {title[:55]}...")
        time.sleep(0.5)

    print(f"\n=== Done: {updated}/{len(to_update)} posts updated ===")


if __name__ == "__main__":
    main()
