#!/usr/bin/env python3
"""Generate and publish Google Web Stories for rhythmicaleskimo.com
Content must be a FULL AMP HTML document (not just amp-story-page fragments).
The Web Stories plugin's renderer uses post_content as-is via get_markup().
"""
import requests, re, json, sys

SITE = "https://rhythmicaleskimo.com"
REST = f"{SITE}/wp-json"
USER = "cjy654377@gmail.com"
PASS = "Dkflekd1!!"
PUBLISHER = "Rhythmical Eskimo"

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

def rgb(r,g,b):
    return {"r": r, "g": g, "b": b}

def make_amp_page_html(page_id, bg_hex, texts, advance="7s"):
    """Create AMP HTML for one story page"""
    text_html = "".join(texts)
    return (
        f'<amp-story-page id="{page_id}" auto-advance-after="{advance}">'
        f'<amp-story-grid-layer template="fill">'
        f'<div style="background-color:{bg_hex};width:100%;height:100%"></div>'
        f'</amp-story-grid-layer>'
        f'<amp-story-grid-layer template="vertical" style="padding:24px;align-content:center;justify-content:center">'
        f'{text_html}'
        f'</amp-story-grid-layer>'
        f'</amp-story-page>'
    )

def make_cta_page_html(page_id, bg_hex, texts, cta_url, cta_text="Read Full Article"):
    """Create final CTA page with outlink"""
    text_html = "".join(texts)
    return (
        f'<amp-story-page id="{page_id}" auto-advance-after="7s">'
        f'<amp-story-grid-layer template="fill">'
        f'<div style="background-color:{bg_hex};width:100%;height:100%"></div>'
        f'</amp-story-grid-layer>'
        f'<amp-story-grid-layer template="vertical" style="padding:24px;align-content:center;justify-content:center">'
        f'{text_html}'
        f'</amp-story-grid-layer>'
        f'<amp-story-cta-layer>'
        f'<a href="{cta_url}" style="font-size:18px;font-weight:700;padding:12px 24px;background:#fff;color:#000;border-radius:24px;text-decoration:none">{cta_text}</a>'
        f'</amp-story-cta-layer>'
        f'</amp-story-page>'
    )

def wrap_full_amp_doc(title, pages_html):
    """Wrap story pages in a complete AMP HTML document"""
    return (
        '<!DOCTYPE html>'
        '<html amp="" lang="en-US">'
        '<head>'
        '<meta charSet="utf-8"/>'
        '<meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1"/>'
        '<script async="" src="https://cdn.ampproject.org/v0.js"></script>'
        '<script async="" src="https://cdn.ampproject.org/v0/amp-story-1.0.js" custom-element="amp-story"></script>'
        '<style amp-boilerplate="">body{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}@-webkit-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@-moz-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}</style>'
        '<noscript><style amp-boilerplate="">body{-webkit-animation:none;-moz-animation:none;animation:none}</style></noscript>'
        '<!-- WEB_STORIES_HEAD_START -->'
        '<link rel="canonical" href=""/>'
        f'<title>{title}</title>'
        '<!-- WEB_STORIES_HEAD_END -->'
        '</head>'
        '<body>'
        f'<amp-story standalone="" publisher="{PUBLISHER}" title="{title}" publisher-logo-src="" poster-portrait-src="">'
        f'{pages_html}'
        '</amp-story>'
        '</body>'
        '</html>'
    )

def make_story_data_page(page_id, bg_rgb, elements):
    """Create story_data page object for the editor"""
    els = [{
        "id": f"bg-{page_id}",
        "type": "shape",
        "x": 0, "y": 0, "width": 412, "height": 732,
        "isBackground": True,
        "backgroundColor": {"color": bg_rgb}
    }]
    for i, el in enumerate(elements):
        els.append({
            "id": f"el-{page_id}-{i}",
            "type": "text",
            "x": el.get("x", 30), "y": el.get("y", 200),
            "width": el.get("width", 352), "height": el.get("height", 80),
            "content": el["content"],
            "fontSize": el.get("fontSize", 20),
            "textAlign": el.get("textAlign", "center"),
            "padding": {"horizontal": 0, "vertical": 0, "locked": True}
        })
    return {
        "id": page_id,
        "elements": els,
        "backgroundColor": {"color": bg_rgb},
        "autoAdvanceAfter": "7s"
    }

# ============================================================
# STORY DEFINITIONS
# ============================================================

STORIES = [
    {
        "title": "10-Step Korean Skincare Routine Explained",
        "slug": "10-step-korean-skincare-routine-web-story",
        "cta_url": f"{SITE}/the-10-step-korean-skincare-routine-a-complete-beginners-guide-for-2026/",
        "cta_text": "Read the Full Skincare Guide",
        "pages": [
            {
                "bg": ("#e8d5c4", rgb(232,213,196)),
                "texts": [
                    '<h1 style="color:#2c1810;font-size:32px;font-weight:800;text-align:center;margin:0">The 10-Step Korean Skincare Routine</h1>',
                    '<p style="color:#5a3d2e;font-size:18px;text-align:center;margin-top:16px">Why Korean women have the best skin in the world</p>',
                ],
                "elements": [
                    {"content": '<span style="color:#2c1810;font-size:32px;font-weight:800">The 10-Step Korean Skincare Routine</span>', "y": 250, "height": 120, "fontSize": 32},
                    {"content": '<span style="color:#5a3d2e;font-size:18px">Why Korean women have the best skin in the world</span>', "y": 390, "height": 60, "fontSize": 18},
                ]
            },
            {
                "bg": ("#f5e6d3", rgb(245,230,211)),
                "texts": [
                    '<h2 style="color:#2c1810;font-size:26px;font-weight:700;text-align:center;margin:0">Step 1-2: Double Cleanse</h2>',
                    '<p style="color:#5a3d2e;font-size:17px;text-align:center;margin-top:12px">Oil cleanser removes makeup &amp; SPF. Water-based cleanser removes sweat &amp; dirt.</p>',
                    '<p style="color:#8b6914;font-size:15px;text-align:center;margin-top:12px;font-style:italic">This is the foundation of K-beauty</p>',
                ],
                "elements": [
                    {"content": '<span style="color:#2c1810;font-size:26px;font-weight:700">Step 1-2: Double Cleanse</span>', "y": 200, "height": 80, "fontSize": 26},
                    {"content": '<span style="color:#5a3d2e;font-size:17px">Oil cleanser + Water-based cleanser</span>', "y": 300, "height": 100, "fontSize": 17},
                ]
            },
            {
                "bg": ("#dce8d5", rgb(220,232,213)),
                "texts": [
                    '<h2 style="color:#1a3d10;font-size:26px;font-weight:700;text-align:center;margin:0">Step 3-4: Exfoliate &amp; Tone</h2>',
                    '<p style="color:#2e5a1e;font-size:17px;text-align:center;margin-top:12px">Chemical exfoliants (AHA/BHA) 2-3x per week. Hydrating toner applied with hands, not cotton pads.</p>',
                ],
                "elements": [
                    {"content": '<span style="color:#1a3d10;font-size:26px;font-weight:700">Step 3-4: Exfoliate &amp; Tone</span>', "y": 200, "height": 80, "fontSize": 26},
                    {"content": '<span style="color:#2e5a1e;font-size:17px">AHA/BHA + Hydrating toner</span>', "y": 300, "height": 120, "fontSize": 17},
                ]
            },
            {
                "bg": ("#d5dce8", rgb(213,220,232)),
                "texts": [
                    '<h2 style="color:#10243d;font-size:26px;font-weight:700;text-align:center;margin:0">Step 5-7: Essence, Serum &amp; Mask</h2>',
                    '<p style="color:#1e3a5a;font-size:17px;text-align:center;margin-top:12px">Essence hydrates at cellular level. Serum targets specific concerns. Sheet masks deliver concentrated ingredients.</p>',
                ],
                "elements": [
                    {"content": '<span style="color:#10243d;font-size:26px;font-weight:700">Step 5-7: Essence, Serum &amp; Mask</span>', "y": 200, "height": 100, "fontSize": 26},
                    {"content": '<span style="color:#1e3a5a;font-size:17px">Hydrate + Target + Concentrate</span>', "y": 320, "height": 120, "fontSize": 17},
                ]
            },
            {
                "bg": ("#e8d5e4", rgb(232,213,228)),
                "texts": [
                    '<h2 style="color:#3d102e;font-size:26px;font-weight:700;text-align:center;margin:0">Step 8-10: Eye Cream, Moisturizer &amp; SPF</h2>',
                    '<p style="color:#5a2e4e;font-size:17px;text-align:center;margin-top:12px">SPF 50+ every single day - rain or shine.</p>',
                    '<p style="color:#8b1466;font-size:16px;text-align:center;margin-top:16px;font-weight:600">Korean dermatologists say: No SPF = No skincare</p>',
                ],
                "elements": [
                    {"content": '<span style="color:#3d102e;font-size:26px;font-weight:700">Step 8-10: Moisturize &amp; Protect</span>', "y": 180, "height": 100, "fontSize": 26},
                    {"content": '<span style="color:#5a2e4e;font-size:17px">No SPF = No skincare</span>', "y": 300, "height": 120, "fontSize": 17},
                ]
            },
        ]
    },
    {
        "title": "BTS Spring Day: The Deepest K-Pop Song Ever Written",
        "slug": "bts-spring-day-meaning-web-story",
        "cta_url": f"{SITE}/bts-spring-day-%eb%b4%84%eb%82%a0-lyrics-meaning-the-deepest-k-pop-song-ever-written/",
        "cta_text": "Read Full Lyrics Analysis",
        "pages": [
            {
                "bg": ("#1a1a2e", rgb(26,26,46)),
                "texts": [
                    '<h1 style="color:#e0d0ff;font-size:30px;font-weight:800;text-align:center;margin:0">BTS Spring Day Lyrics Meaning</h1>',
                    '<p style="color:#b0a0d0;font-size:18px;text-align:center;margin-top:16px">The deepest K-Pop song ever written</p>',
                ],
                "elements": [
                    {"content": '<span style="color:#e0d0ff;font-size:30px;font-weight:800">BTS Spring Day Lyrics Meaning</span>', "y": 250, "height": 120, "fontSize": 30},
                    {"content": '<span style="color:#b0a0d0;font-size:18px">The deepest K-Pop song ever written</span>', "y": 390, "height": 60, "fontSize": 18},
                ]
            },
            {
                "bg": ("#16213e", rgb(22,33,62)),
                "texts": [
                    '<h2 style="color:#a0c4ff;font-size:24px;font-weight:700;text-align:center;margin:0">The Sewol Ferry Connection</h2>',
                    '<p style="color:#c0d8ff;font-size:17px;text-align:center;margin-top:12px">Released Feb 13, 2017. Widely believed to reference the 2014 Sewol ferry disaster that killed 304 people, mostly high school students.</p>',
                ],
                "elements": [
                    {"content": '<span style="color:#a0c4ff;font-size:24px;font-weight:700">The Sewol Ferry Connection</span>', "y": 200, "height": 80, "fontSize": 24},
                    {"content": '<span style="color:#c0d8ff;font-size:17px">Sewol ferry disaster - 304 victims</span>', "y": 300, "height": 120, "fontSize": 17},
                ]
            },
            {
                "bg": ("#1a1a3e", rgb(26,26,62)),
                "texts": [
                    '<h2 style="color:#ffd0e0;font-size:28px;font-weight:700;text-align:center;margin:0">I miss you</h2>',
                    '<p style="color:#e0b0c0;font-size:17px;text-align:center;margin-top:12px">In Korean, bogoshipda carries deep emotional weight - longing for someone who cannot return.</p>',
                ],
                "elements": [
                    {"content": '<span style="color:#ffd0e0;font-size:28px;font-weight:700">I miss you (bogoshipda)</span>', "y": 220, "height": 80, "fontSize": 28},
                    {"content": '<span style="color:#e0b0c0;font-size:17px">Longing for someone who cannot return</span>', "y": 320, "height": 120, "fontSize": 17},
                ]
            },
            {
                "bg": ("#2e1a3e", rgb(46,26,62)),
                "texts": [
                    '<h2 style="color:#e0c0ff;font-size:24px;font-weight:700;text-align:center;margin:0">The Ones Who Walk Away from Omelas</h2>',
                    '<p style="color:#c0a0e0;font-size:17px;text-align:center;margin-top:12px">The MV references Le Guin\'s story about a perfect city built on one child\'s suffering. Can we accept happiness built on others\' pain?</p>',
                ],
                "elements": [
                    {"content": '<span style="color:#e0c0ff;font-size:24px;font-weight:700">Omelas Reference</span>', "y": 200, "height": 80, "fontSize": 24},
                    {"content": '<span style="color:#c0a0e0;font-size:17px">Happiness built on suffering</span>', "y": 300, "height": 120, "fontSize": 17},
                ]
            },
            {
                "bg": ("#1e2d4a", rgb(30,45,74)),
                "texts": [
                    '<h2 style="color:#ffe0a0;font-size:24px;font-weight:700;text-align:center;margin:0">8+ Years on the Charts</h2>',
                    '<p style="color:#e0d0b0;font-size:17px;text-align:center;margin-top:12px">The longest charting song in K-Pop history. Returns to #1 every April 16th, the Sewol anniversary.</p>',
                ],
                "elements": [
                    {"content": '<span style="color:#ffe0a0;font-size:24px;font-weight:700">8+ Years on Charts</span>', "y": 180, "height": 80, "fontSize": 24},
                    {"content": '<span style="color:#e0d0b0;font-size:17px">Longest charting K-Pop song ever</span>', "y": 280, "height": 120, "fontSize": 17},
                ]
            },
        ]
    },
    {
        "title": "Best Korean Sunscreens 2026: Dermatologist Picks",
        "slug": "best-korean-sunscreens-2026-web-story",
        "cta_url": f"{SITE}/best-korean-sunscreens-2026-dermatologist-approved-spf-for-every-skin-type/",
        "cta_text": "See All 7 Sunscreen Picks",
        "pages": [
            {
                "bg": ("#fff5e6", rgb(255,245,230)),
                "texts": [
                    '<h1 style="color:#cc6600;font-size:30px;font-weight:800;text-align:center;margin:0">Best Korean Sunscreens 2026</h1>',
                    '<p style="color:#995200;font-size:18px;text-align:center;margin-top:16px">Dermatologist-approved SPF for every skin type</p>',
                ],
                "elements": [
                    {"content": '<span style="color:#cc6600;font-size:30px;font-weight:800">Best Korean Sunscreens 2026</span>', "y": 250, "height": 120, "fontSize": 30},
                    {"content": '<span style="color:#995200;font-size:18px">Dermatologist-approved SPF</span>', "y": 390, "height": 60, "fontSize": 18},
                ]
            },
            {
                "bg": ("#f0f8ff", rgb(240,248,255)),
                "texts": [
                    '<h2 style="color:#1a4d80;font-size:24px;font-weight:700;text-align:center;margin:0">Why Korean Sunscreens Are #1</h2>',
                    '<p style="color:#2a6dad;font-size:17px;text-align:center;margin-top:12px">Lightweight, no white cast, under $15. They use newer UV filters not yet approved in the US.</p>',
                ],
                "elements": [
                    {"content": '<span style="color:#1a4d80;font-size:24px;font-weight:700">Why Korean Sunscreens Are #1</span>', "y": 200, "height": 80, "fontSize": 24},
                    {"content": '<span style="color:#2a6dad;font-size:17px">Better filters, better texture</span>', "y": 300, "height": 120, "fontSize": 17},
                ]
            },
            {
                "bg": ("#fff0f0", rgb(255,240,240)),
                "texts": [
                    '<h2 style="color:#cc3333;font-size:24px;font-weight:700;text-align:center;margin:0">Beauty of Joseon Relief Sun</h2>',
                    '<p style="color:#993333;font-size:17px;text-align:center;margin-top:12px">SPF 50+ PA++++. Rice bran &amp; probiotics. Sold every 3 seconds worldwide. Under $12.</p>',
                    '<p style="color:#666;font-size:15px;text-align:center;margin-top:8px">Best for: Normal to dry skin</p>',
                ],
                "elements": [
                    {"content": '<span style="color:#cc3333;font-size:24px;font-weight:700">Beauty of Joseon Relief Sun</span>', "y": 200, "height": 80, "fontSize": 24},
                    {"content": '<span style="color:#993333;font-size:17px">SPF 50+ PA++++, Under $12</span>', "y": 300, "height": 100, "fontSize": 17},
                ]
            },
            {
                "bg": ("#f0fff0", rgb(240,255,240)),
                "texts": [
                    '<h2 style="color:#2d7d2d;font-size:24px;font-weight:700;text-align:center;margin:0">ROUND LAB Birch Juice Sun</h2>',
                    '<p style="color:#3d8d3d;font-size:17px;text-align:center;margin-top:12px">Matte finish, controls oil 8+ hours. #1 sunscreen in Korea for oily skin.</p>',
                ],
                "elements": [
                    {"content": '<span style="color:#2d7d2d;font-size:24px;font-weight:700">ROUND LAB Birch Juice</span>', "y": 200, "height": 80, "fontSize": 24},
                    {"content": '<span style="color:#3d8d3d;font-size:17px">Matte finish, 8hr oil control</span>', "y": 300, "height": 100, "fontSize": 17},
                ]
            },
        ]
    },
    {
        "title": "Seoul Hidden Alley Restaurants Only Locals Know",
        "slug": "seoul-hidden-restaurants-web-story",
        "cta_url": f"{SITE}/seouls-hidden-alley-restaurants-7-places-only-locals-know-about/",
        "cta_text": "See All 7 Restaurants + Maps",
        "pages": [
            {
                "bg": ("#2d1810", rgb(45,24,16)),
                "texts": [
                    '<h1 style="color:#ffd700;font-size:30px;font-weight:800;text-align:center;margin:0">Seoul\'s Hidden Alley Restaurants</h1>',
                    '<p style="color:#e0c080;font-size:18px;text-align:center;margin-top:16px">7 places only locals know about</p>',
                ],
                "elements": [
                    {"content": '<span style="color:#ffd700;font-size:30px;font-weight:800">Seoul Hidden Restaurants</span>', "y": 250, "height": 120, "fontSize": 30},
                    {"content": '<span style="color:#e0c080;font-size:18px">7 places only locals know</span>', "y": 390, "height": 60, "fontSize": 18},
                ]
            },
            {
                "bg": ("#3d2010", rgb(61,32,16)),
                "texts": [
                    '<h2 style="color:#ffa500;font-size:24px;font-weight:700;text-align:center;margin:0">Skip the Tourist Spots</h2>',
                    '<p style="color:#e0b060;font-size:17px;text-align:center;margin-top:12px">Myeongdong charges 2-3x for mediocre food. Real Seoul food is in narrow golmok alleys where office workers eat.</p>',
                ],
                "elements": [
                    {"content": '<span style="color:#ffa500;font-size:24px;font-weight:700">Skip Tourist Spots</span>', "y": 200, "height": 80, "fontSize": 24},
                    {"content": '<span style="color:#e0b060;font-size:17px">Real food is in the alleys</span>', "y": 300, "height": 120, "fontSize": 17},
                ]
            },
            {
                "bg": ("#4a2810", rgb(74,40,16)),
                "texts": [
                    '<h2 style="color:#ff8c00;font-size:24px;font-weight:700;text-align:center;margin:0">Jongno Pojangmacha Alley</h2>',
                    '<p style="color:#e0a050;font-size:17px;text-align:center;margin-top:12px">Open-air tent bars since the 1960s. Pajeon, sundae, soju. $3.50 for a full meal. Best after 10 PM.</p>',
                ],
                "elements": [
                    {"content": '<span style="color:#ff8c00;font-size:24px;font-weight:700">Jongno Pojangmacha</span>', "y": 200, "height": 80, "fontSize": 24},
                    {"content": '<span style="color:#e0a050;font-size:17px">Tent bars since 1960s, $3.50</span>', "y": 300, "height": 100, "fontSize": 17},
                ]
            },
            {
                "bg": ("#3a2818", rgb(58,40,24)),
                "texts": [
                    '<h2 style="color:#ffb347;font-size:24px;font-weight:700;text-align:center;margin:0">Euljiro Nogari Alley</h2>',
                    '<p style="color:#e0b870;font-size:17px;text-align:center;margin-top:12px">Dried pollack + cheap beer in retro-industrial Euljiro. Where young Koreans go for hip-retro vibes. 3,000 KRW per plate.</p>',
                ],
                "elements": [
                    {"content": '<span style="color:#ffb347;font-size:24px;font-weight:700">Euljiro Nogari Alley</span>', "y": 200, "height": 80, "fontSize": 24},
                    {"content": '<span style="color:#e0b870;font-size:17px">Hip-retro vibes, 3,000 KRW</span>', "y": 300, "height": 100, "fontSize": 17},
                ]
            },
        ]
    },
    {
        "title": "Learn to Read Korean Hangul in 30 Minutes",
        "slug": "learn-hangul-30-minutes-web-story",
        "cta_url": f"{SITE}/how-to-read-korean-hangul-in-30-minutes-the-fastest-method-that-actually-works/",
        "cta_text": "Start Learning Hangul Now",
        "pages": [
            {
                "bg": ("#0d1b2a", rgb(13,27,42)),
                "texts": [
                    '<h1 style="color:#00d4ff;font-size:30px;font-weight:800;text-align:center;margin:0">Read Korean in 30 Minutes</h1>',
                    '<p style="color:#80c0e0;font-size:18px;text-align:center;margin-top:16px">Hangul is the easiest alphabet in the world</p>',
                ],
                "elements": [
                    {"content": '<span style="color:#00d4ff;font-size:30px;font-weight:800">Read Korean in 30 Minutes</span>', "y": 250, "height": 100, "fontSize": 30},
                    {"content": '<span style="color:#80c0e0;font-size:18px">The easiest alphabet in the world</span>', "y": 370, "height": 60, "fontSize": 18},
                ]
            },
            {
                "bg": ("#1b2a3d", rgb(27,42,61)),
                "texts": [
                    '<h2 style="color:#4de0ff;font-size:24px;font-weight:700;text-align:center;margin:0">Invented by a King in 1443</h2>',
                    '<p style="color:#a0d0e8;font-size:17px;text-align:center;margin-top:12px">King Sejong created Hangul so common people could read. Only 24 letters total - you can learn them in one sitting.</p>',
                ],
                "elements": [
                    {"content": '<span style="color:#4de0ff;font-size:24px;font-weight:700">Created by King Sejong, 1443</span>', "y": 200, "height": 80, "fontSize": 24},
                    {"content": '<span style="color:#a0d0e8;font-size:17px">Only 24 letters total</span>', "y": 300, "height": 120, "fontSize": 17},
                ]
            },
            {
                "bg": ("#0d2b1b", rgb(13,43,27)),
                "texts": [
                    '<h2 style="color:#00ff88;font-size:24px;font-weight:700;text-align:center;margin:0">The Shape = The Sound</h2>',
                    '<p style="color:#80e0b0;font-size:17px;text-align:center;margin-top:12px">The letters literally show you how to pronounce them. The mouth shapes become the letter shapes.</p>',
                ],
                "elements": [
                    {"content": '<span style="color:#00ff88;font-size:24px;font-weight:700">Shape = Sound</span>', "y": 200, "height": 80, "fontSize": 24},
                    {"content": '<span style="color:#80e0b0;font-size:17px">Mouth shapes become letters</span>', "y": 300, "height": 120, "fontSize": 17},
                ]
            },
            {
                "bg": ("#2a1b0d", rgb(42,27,13)),
                "texts": [
                    '<h2 style="color:#ffaa00;font-size:24px;font-weight:700;text-align:center;margin:0">Stack Like LEGO Blocks</h2>',
                    '<p style="color:#e0c080;font-size:17px;text-align:center;margin-top:12px">Korean syllables stack into blocks. Know 24 letters and you can read any Korean word - even K-Pop lyrics!</p>',
                ],
                "elements": [
                    {"content": '<span style="color:#ffaa00;font-size:24px;font-weight:700">Stack Like LEGO</span>', "y": 200, "height": 80, "fontSize": 24},
                    {"content": '<span style="color:#e0c080;font-size:17px">24 letters = read anything</span>', "y": 300, "height": 120, "fontSize": 17},
                ]
            },
        ]
    },
]


def build_story(story_def):
    """Build full AMP HTML content and story_data from definition"""
    pages_html = []
    pages_data = []

    for i, p in enumerate(story_def["pages"]):
        pid = f"page-{i+1}"
        bg_hex, bg_rgb = p["bg"]

        # Last page gets CTA
        is_last = (i == len(story_def["pages"]) - 1)
        if is_last and story_def.get("cta_url"):
            pages_html.append(make_cta_page_html(
                pid, bg_hex, p["texts"],
                story_def["cta_url"],
                story_def.get("cta_text", "Read More")
            ))
        else:
            pages_html.append(make_amp_page_html(pid, bg_hex, p["texts"]))

        pages_data.append(make_story_data_page(pid, bg_rgb, p["elements"]))

    content = wrap_full_amp_doc(story_def["title"], "".join(pages_html))
    story_data = {"version": 48, "pages": pages_data}
    return content, story_data


def publish_story(s, h, story_def):
    """Publish a single web story"""
    content, story_data = build_story(story_def)

    r = s.post(f"{REST}/web-stories/v1/web-story", headers=h, json={
        "title": story_def["title"],
        "status": "publish",
        "content": content,
        "story_data": story_data,
        "slug": story_def["slug"],
    })

    if r.status_code == 201:
        result = r.json()
        sid = result["id"]
        link = result["link"]
        print(f"  OK: {story_def['title']}")
        print(f"      ID:{sid} | {link}")
        return sid, link
    else:
        print(f"  FAIL ({r.status_code}): {r.text[:200]}")
        return None, None


if __name__ == "__main__":
    s, h = login()
    print("Publishing Web Stories...\n")

    results = []
    for sd in STORIES:
        sid, link = publish_story(s, h, sd)
        if sid:
            results.append({"id": sid, "title": sd["title"], "link": link})

    print(f"\nDone: {len(results)}/{len(STORIES)} published")
    for r in results:
        print(f"  [{r['id']}] {r['link']}")

    # Verify first story renders correctly
    if results:
        import requests as req
        fr = req.get(results[0]["link"])
        has_story = "<amp-story" in fr.text
        print(f"\nFront-end verification: {'OK' if has_story else 'FAILED'} (amp-story {'found' if has_story else 'missing'})")
