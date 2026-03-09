#!/usr/bin/env python3
"""Create Disclaimer page and update Privacy Policy with AdSense info."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import login, REST

DISCLAIMER_HTML = """
<h2>General Information</h2>
<p>The information provided on Rhythmical Eskimo (https://rhythmicaleskimo.com) is for general informational and educational purposes only. While we strive to keep the content accurate and up to date, we make no representations or warranties of any kind, express or implied, about the completeness, accuracy, reliability, suitability, or availability of the information, products, services, or related graphics contained on this website.</p>

<h2>Not Professional Advice</h2>
<p>The content on this site does not constitute professional advice — whether financial, legal, medical, or otherwise. Any reliance you place on such information is strictly at your own risk. Always consult a qualified professional before making decisions based on information found on this website.</p>

<h2>Affiliate Links &amp; Sponsored Content</h2>
<p>Some posts on this site may contain affiliate links, meaning we may earn a small commission if you click through and make a purchase — at no additional cost to you. Sponsored content, when present, will be clearly disclosed. Our editorial opinions remain our own and are not influenced by affiliate partnerships.</p>

<h2>Opinions &amp; Views</h2>
<p>All opinions expressed on this website are solely those of the author(s) and do not represent the views of any organization, employer, or other entity. Product reviews and recommendations are based on personal experience and research.</p>

<h2>External Links</h2>
<p>This site may contain links to external websites that are not maintained by us. We have no control over the content, privacy policies, or practices of third-party sites and assume no responsibility for them. Visiting external links is at your own discretion.</p>

<h2>Accuracy of Information</h2>
<p>We make every effort to ensure the accuracy of information published on this site. However, prices, availability, product specifications, and other details may change without notice. We encourage readers to verify critical information independently before relying on it.</p>

<h2>Limitation of Liability</h2>
<p>In no event shall Rhythmical Eskimo or its authors be liable for any loss or damage — including, without limitation, indirect or consequential loss or damage — arising from the use of this website or reliance on any information provided herein.</p>

<h2>Changes to This Disclaimer</h2>
<p>We reserve the right to update or modify this disclaimer at any time without prior notice. Your continued use of the website after changes are posted constitutes acceptance of the updated disclaimer.</p>

<p><em>Last updated: March 10, 2026</em></p>
"""

ADSENSE_ADDON = """
<h2>Google AdSense &amp; Advertising Cookies</h2>
<p>This website uses Google AdSense, a service provided by Google LLC, to display advertisements. Google AdSense uses cookies — including the DoubleClick cookie — to serve ads based on your prior visits to this site and other websites on the Internet.</p>

<h3>How Cookies Are Used for Advertising</h3>
<ul>
<li>Google uses cookies to serve ads based on your visits to this website and other sites on the Internet.</li>
<li>Google's use of advertising cookies enables it and its partners to serve ads based on your browsing history.</li>
<li>Third-party advertising networks that serve ads on this site may also use cookies, web beacons, and similar technologies to collect information about your interactions with their ads.</li>
</ul>

<h3>Third-Party Ad Networks</h3>
<p>Third-party vendors, including Google, use cookies to serve ads based on your prior visits to this website or other websites. These third-party ad servers or ad networks use technology to display advertisements and links that appear on this site directly to your browser. They may automatically receive your IP address when this occurs. Other technologies such as cookies, JavaScript, or web beacons may also be used by third-party ad networks to measure the effectiveness of their advertisements and to personalize the advertising content you see.</p>

<h3>Opting Out of Personalized Advertising</h3>
<p>You may opt out of personalized advertising by visiting <a href="https://www.google.com/settings/ads" target="_blank" rel="noopener noreferrer">Google Ads Settings</a>. Alternatively, you can opt out of third-party cookies for personalized advertising by visiting <a href="https://www.aboutads.info/choices/" target="_blank" rel="noopener noreferrer">www.aboutads.info/choices</a> or <a href="https://www.networkadvertising.org/choices/" target="_blank" rel="noopener noreferrer">the NAI opt-out page</a>.</p>

<p>Please note that opting out of personalized ads does not prevent ads from being shown to you; it simply means the ads will not be tailored to your interests.</p>

<p><em>AdSense disclosure last updated: March 10, 2026</em></p>
"""

def main():
    s, h = login()

    # 1) Get existing pages
    pages = []
    page_num = 1
    while True:
        r = s.get(f"{REST}/pages?per_page=100&page={page_num}&status=publish,draft,private", headers=h)
        if r.status_code != 200:
            break
        batch = r.json()
        if not batch:
            break
        pages.extend(batch)
        page_num += 1

    print(f"Found {len(pages)} existing pages")

    # Check for existing Disclaimer and Privacy Policy
    disclaimer_page = None
    privacy_page = None
    for p in pages:
        slug = p.get("slug", "")
        title = p.get("title", {}).get("rendered", "")
        if slug == "disclaimer" or "disclaimer" in title.lower():
            disclaimer_page = p
        if slug == "privacy-policy" or "privacy" in title.lower():
            privacy_page = p

    # 2) Create or update Disclaimer
    if disclaimer_page:
        print(f"Disclaimer page already exists (ID: {disclaimer_page['id']}), updating...")
        r = s.post(f"{REST}/pages/{disclaimer_page['id']}", headers=h, json={
            "title": "Disclaimer",
            "content": DISCLAIMER_HTML,
            "status": "publish"
        })
    else:
        print("Creating Disclaimer page...")
        r = s.post(f"{REST}/pages", headers=h, json={
            "title": "Disclaimer",
            "slug": "disclaimer",
            "content": DISCLAIMER_HTML,
            "status": "publish"
        })

    if r.status_code in (200, 201):
        print(f"  OK — Disclaimer: {r.json()['link']}")
    else:
        print(f"  FAIL — {r.status_code}: {r.text[:200]}")

    # 3) Update Privacy Policy with AdSense info
    if privacy_page:
        print(f"Privacy Policy found (ID: {privacy_page['id']}), appending AdSense section...")
        existing_content = privacy_page.get("content", {}).get("rendered", "")
        # Check if AdSense section already exists
        if "Google AdSense" in existing_content:
            print("  AdSense section already present, skipping.")
        else:
            new_content = existing_content + ADSENSE_ADDON
            r = s.post(f"{REST}/pages/{privacy_page['id']}", headers=h, json={
                "content": new_content,
                "status": "publish"
            })
            if r.status_code == 200:
                print(f"  OK — Privacy Policy updated: {r.json()['link']}")
            else:
                print(f"  FAIL — {r.status_code}: {r.text[:200]}")
    else:
        print("Privacy Policy page not found! Creating one with AdSense section...")
        r = s.post(f"{REST}/pages", headers=h, json={
            "title": "Privacy Policy",
            "slug": "privacy-policy",
            "content": ADSENSE_ADDON,
            "status": "publish"
        })
        if r.status_code == 201:
            print(f"  OK — Privacy Policy created: {r.json()['link']}")
        else:
            print(f"  FAIL — {r.status_code}: {r.text[:200]}")

    print("\nDone.")

if __name__ == "__main__":
    main()
