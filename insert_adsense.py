#!/usr/bin/env python3
"""Insert Google AdSense code into WordPress via Yoast SEO header scripts or theme customizer."""
import requests, re, sys

SITE = "https://rhythmicaleskimo.com"
USER = "cjy654377@gmail.com"
PASS = "Dkflekd1!!"

ADSENSE_CODE = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9965298818399386" crossorigin="anonymous"></script>'

# Login
s = requests.Session()
s.cookies.set("wordpress_test_cookie", "WP+Cookie+check")
resp = s.post(f"{SITE}/wp-login.php", data={
    "log": USER, "pwd": PASS, "wp-submit": "Log In",
    "redirect_to": "/wp-admin/", "testcookie": "1"
}, allow_redirects=True)

# Try Yoast SEO Webmaster Tools - it has a "Other verification" or custom head section
# Check Yoast settings page for head scripts
yoast_page = s.get(f"{SITE}/wp-admin/admin.php?page=wpseo_settings").text

# Try the WordPress options approach - update blogdescription or use wp_options
# Most reliable: Use the WordPress customizer to add custom HTML

# Check for LiteSpeed Cache - it has "Tuning" with extra header
ls_tuning = s.get(f"{SITE}/wp-admin/admin.php?page=litespeed-page_optm").text

# Get the nonce for LiteSpeed settings
nonce_match = re.search(r'name="_wpnonce"\s+value="([^"]+)"', ls_tuning)
if nonce_match:
    print(f"Found LiteSpeed nonce")

# Alternative approach: Check theme's header.php or use wp_options
# Let's try using the customizer API
customize_page = s.get(f"{SITE}/wp-admin/customize.php").text

# Best approach: Find the Additional HTML/CSS section in customizer
# Or use wp-admin/options.php to set a custom option

# Let's try the most reliable method - check if there's a "Header and Footer Scripts" in theme settings
theme_page = s.get(f"{SITE}/wp-admin/themes.php").text

# Try inserting via Jetpack if available
jetpack_check = s.get(f"{SITE}/wp-admin/admin.php?page=jetpack").text
has_jetpack = "jetpack" in jetpack_check.lower()
print(f"Jetpack available: {has_jetpack}")

# Since we have Yoast, let's use its REST API to update site verification/head tags
# Yoast stores custom head scripts in wpseo_social option or wpseo option

# Get current options via admin-ajax
admin_nonce_match = re.search(r'"_ajax_nonce":"([^"]+)"', ls_tuning) or re.search(r'name="_wpnonce"\s+value="([^"]+)"', s.get(f"{SITE}/wp-admin/options-general.php").text)

# Simplest method: use options.php to add custom code
# Check for Insert Headers and Footers option
options_page = s.get(f"{SITE}/wp-admin/options-general.php").text
if "insert_headers" in options_page.lower() or "header_scripts" in options_page.lower():
    print("Found header scripts option")
else:
    print("No header scripts plugin found")

# Final approach: Use theme.json or functions.php via File Editor
# Let's check what theme is active
theme_editor = s.get(f"{SITE}/wp-admin/theme-editor.php").text
active_theme_match = re.search(r'<h2>Editing Themes:.*?<strong>(.*?)</strong>', theme_editor)
if active_theme_match:
    print(f"Active theme: {active_theme_match.group(1)}")

# Check if header.php exists
header_match = re.search(r'theme-editor\.php\?file=header\.php', theme_editor)
if header_match:
    print("header.php found - can insert AdSense code there")
    
    # Get header.php content
    header_page = s.get(f"{SITE}/wp-admin/theme-editor.php?file=header.php").text
    # Extract the file content from the textarea
    content_match = re.search(r'<textarea[^>]*id="newcontent"[^>]*>(.*?)</textarea>', header_page, re.DOTALL)
    if content_match:
        content = content_match.group(1)
        import html
        content = html.unescape(content)
        
        if 'adsbygoogle' in content:
            print("AdSense code already present!")
        elif '</head>' in content:
            new_content = content.replace('</head>', f'{ADSENSE_CODE}\n</head>')
            
            # Get the nonce and file path for saving
            file_nonce = re.search(r'name="_wpnonce"\s+value="([^"]+)"', header_page)
            theme_name = re.search(r'name="theme"\s+value="([^"]+)"', header_page)
            
            if file_nonce and theme_name:
                save_data = {
                    "_wpnonce": file_nonce.group(1),
                    "newcontent": new_content,
                    "action": "update",
                    "file": "header.php",
                    "theme": theme_name.group(1),
                    "submit": "Update File"
                }
                save_resp = s.post(f"{SITE}/wp-admin/theme-editor.php", data=save_data)
                if save_resp.status_code == 200 and "File edited successfully" in save_resp.text:
                    print("✅ AdSense code inserted into header.php successfully!")
                else:
                    print(f"Save response: {save_resp.status_code}")
                    if "File edited successfully" in save_resp.text:
                        print("✅ AdSense code inserted!")
                    else:
                        print("❌ Could not save - may need manual insertion")
            else:
                print("Could not find save nonce")
        else:
            print("</head> tag not found in header.php")
    else:
        print("Could not extract header.php content")
else:
    print("header.php not found - block theme likely")
    print("\n📋 Manual insertion needed:")
    print(f"Go to: {SITE}/wp-admin/admin.php?page=wpseo_settings")
    print(f"Or add this code via Appearance > Customize > Additional HTML/head")
    print(f"\nAdSense code:\n{ADSENSE_CODE}")

