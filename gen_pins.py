#!/usr/bin/env python3
"""Generate Pinterest vertical pin images (1000x1500) for all blog posts."""
import os, json, re, math
from urllib.parse import unquote, urlparse
from PIL import Image, ImageDraw, ImageFont
import requests

# ── Config ──
W, H = 1000, 1500
BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "pins")
FONT = "/System/Library/Fonts/HelveticaNeue.ttc"
SITE = "https://rhythmicaleskimo.com"
SITE_LABEL = "rhythmicaleskimo.com"

# ── Category color themes (top_color, bot_color) ──
THEMES = {
    "k-beauty":         ((255, 107, 157), (196, 69, 105)),
    "travel-food":      ((243, 156, 18),  (231, 76, 60)),
    "k-drama":          ((142, 68, 173),  (44, 62, 80)),
    "k-pop":            ((142, 68, 173),  (44, 62, 80)),
    "korean-language":  ((39, 174, 96),   (44, 62, 80)),
    "world-news":       ((192, 57, 43),   (44, 62, 80)),
    "default":          ((52, 73, 94),    (44, 62, 80)),
}

# ── Category detection keywords ──
CAT_KEYWORDS = {
    "k-beauty": ["k-beauty", "skincare", "beauty", "skin care", "olive young", "cosmetic"],
    "travel-food": ["food", "restaurant", "travel", "guide", "market", "street food",
                    "cafe", "bbq", "soup", "noodle", "bibimbap", "soju", "fried chicken",
                    "temple food", "anju", "buffet", "dumpling", "mandu", "tofu",
                    "jeju", "busan", "seoul", "myeongdong", "gwangjang", "jeonju",
                    "convenience store", "budget", "filming location", "pohang",
                    "hongcheon", "monkfish", "loach", "beef noodle", "cod soup",
                    "hotteok", "jjajang", "stone plate"],
    "k-drama": ["k-drama", "drama", "netflix", "boyfriend on demand", "jisoo", "tangerines"],
    "k-pop": ["k-pop", "bts", "concert", "arirang", "hybe", "world tour"],
    "korean-language": ["korean language", "learn korean", "korean phrases", "hangul",
                        "how to read korean", "how to order"],
    "world-news": ["war", "iran", "oil", "strike", "missile", "crisis", "market",
                   "trump", "pakistan", "flight", "news", "fifa", "paralympic",
                   "world cup", "anthropic", "openai", "pentagon"],
}

os.makedirs(OUT, exist_ok=True)


def font(size, index=0):
    return ImageFont.truetype(FONT, size, index=index)


def draw_gradient(draw, w, h, top_color, bot_color, y_start=0, y_end=None):
    if y_end is None:
        y_end = h
    span = y_end - y_start
    for y in range(y_start, y_end):
        t = (y - y_start) / max(span, 1)
        r = int(top_color[0] + (bot_color[0] - top_color[0]) * t)
        g = int(top_color[1] + (bot_color[1] - top_color[1]) * t)
        b = int(top_color[2] + (bot_color[2] - top_color[2]) * t)
        draw.line([(0, y), (w, y)], fill=(r, g, b))


def draw_text_shadow(draw, xy, text, fnt, fill, shadow=(30, 30, 30)):
    x, y = xy
    # Two-layer shadow for depth
    draw.text((x + 3, y + 3), text, font=fnt, fill=(0, 0, 0))
    draw.text((x + 1, y + 1), text, font=fnt, fill=shadow)
    draw.text(xy, text, font=fnt, fill=fill)


def wrap_text(text, fnt, max_w):
    words = text.split()
    lines, line = [], ""
    for w in words:
        test = f"{line} {w}".strip()
        bbox = fnt.getbbox(test)
        if bbox[2] > max_w and line:
            lines.append(line)
            line = w
        else:
            line = test
    if line:
        lines.append(line)
    return lines


def detect_category(slug, title=""):
    text = f"{slug} {title}".lower()
    scores = {}
    for cat, keywords in CAT_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text)
        if score > 0:
            scores[cat] = score
    if scores:
        return max(scores, key=scores.get)
    return "default"


def get_category_label(cat):
    labels = {
        "k-beauty": "K-BEAUTY",
        "travel-food": "TRAVEL & FOOD",
        "k-drama": "K-DRAMA",
        "k-pop": "K-POP",
        "korean-language": "KOREAN LANGUAGE",
        "world-news": "WORLD NEWS",
        "default": "BLOG",
    }
    return labels.get(cat, "BLOG")


def slug_from_url(url):
    path = urlparse(url.strip()).path.strip("/")
    slug = unquote(path)
    return slug


def fetch_posts_from_api():
    """Fetch all posts from WP REST API with cookie auth."""
    session = requests.Session()

    # Get nonce via login
    login_url = f"{SITE}/wp-login.php"
    login_data = {
        "log": "cjy654377@gmail.com",
        "pwd": "Dkflekd1!!",
        "wp-submit": "Log In",
        "redirect_to": f"{SITE}/wp-admin/",
        "testcookie": "1",
    }
    session.post(login_url, data=login_data, allow_redirects=True)

    # Fetch posts (paginate)
    posts = {}
    page = 1
    while True:
        url = f"{SITE}/wp-json/wp/v2/posts?per_page=100&page={page}&_fields=id,title,slug,link,categories"
        resp = session.get(url)
        if resp.status_code != 200:
            break
        data = resp.json()
        if not data:
            break
        for p in data:
            posts[p["slug"]] = {
                "title": p["title"]["rendered"],
                "slug": p["slug"],
                "link": p["link"],
            }
        if len(data) < 100:
            break
        page += 1

    print(f"Fetched {len(posts)} posts from REST API")
    return posts


def title_from_slug(slug):
    """Fallback: convert slug to readable title."""
    title = slug.replace("-", " ")
    # Capitalize important words
    small = {"a", "an", "the", "in", "on", "at", "to", "for", "of", "and", "or", "but", "is", "with", "you", "your"}
    words = title.split()
    result = []
    for i, w in enumerate(words):
        if i == 0 or w.lower() not in small:
            result.append(w.capitalize())
        else:
            result.append(w.lower())
    return " ".join(result)


def draw_decorative_elements(draw, cat, top_col, bot_col):
    """Add subtle decorative elements based on category."""
    # Diagonal accent lines
    for i in range(3):
        y_off = 400 + i * 200
        alpha_col = tuple(min(255, c + 40) for c in top_col)
        draw.line([(0, y_off), (W, y_off - 100)], fill=alpha_col, width=1)

    # Corner accent
    accent = tuple(min(255, c + 60) for c in top_col)
    # Top-right decorative circle (partial)
    for r in range(80, 120, 2):
        draw.arc([(W - 60 - r, -60 - r), (W - 60 + r, -60 + r)], 0, 360, fill=accent, width=1)


def generate_pin(slug, title, cat=None):
    """Generate a single Pinterest pin image."""
    if cat is None:
        cat = detect_category(slug, title)

    top_col, bot_col = THEMES.get(cat, THEMES["default"])
    cat_label = get_category_label(cat)

    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)

    # Background gradient
    draw_gradient(d, W, H, top_col, bot_col)

    # Subtle decorative elements
    draw_decorative_elements(d, cat, top_col, bot_col)

    # Dark overlay in center for text readability (blend with gradient)
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for y in range(200, 1200):
        t = 1.0 - abs(y - 700) / 500
        t = max(0, min(1, t))
        alpha = int(100 * t)
        od.line([(0, y), (W, y)], fill=(0, 0, 0, alpha))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    d = ImageDraw.Draw(img)

    # ── Top: Category badge ──
    badge_font = font(28, 1)
    badge_text = cat_label
    badge_bbox = badge_font.getbbox(badge_text)
    badge_w = badge_bbox[2] - badge_bbox[0] + 40
    badge_h = 50
    badge_x = (W - badge_w) // 2
    badge_y = 100

    # Badge background (rounded rectangle)
    d.rounded_rectangle(
        [(badge_x, badge_y), (badge_x + badge_w, badge_y + badge_h)],
        radius=25,
        fill=(255, 255, 255),
    )
    # Badge text
    text_x = badge_x + (badge_w - (badge_bbox[2] - badge_bbox[0])) // 2
    text_y = badge_y + (badge_h - (badge_bbox[3] - badge_bbox[1])) // 2 - 2
    d.text((text_x, text_y), badge_text, font=badge_font, fill=top_col)

    # ── Decorative line under badge ──
    line_y = badge_y + badge_h + 30
    line_w = 60
    d.line([(W // 2 - line_w, line_y), (W // 2 + line_w, line_y)],
           fill=(255, 255, 255), width=3)

    # ── Center: Title text ──
    # Adaptive font size based on title length
    if len(title) < 40:
        title_size = 62
    elif len(title) < 70:
        title_size = 54
    elif len(title) < 100:
        title_size = 46
    else:
        title_size = 40

    title_font = font(title_size, 1)
    max_text_w = W - 120
    lines = wrap_text(title, title_font, max_text_w)

    # Limit to 8 lines max
    if len(lines) > 8:
        lines = lines[:8]
        lines[-1] = lines[-1][:len(lines[-1]) - 3] + "..."

    line_height = int(title_size * 1.35)
    total_text_h = len(lines) * line_height
    start_y = (H // 2) - (total_text_h // 2) + 30

    for i, line in enumerate(lines):
        y = start_y + i * line_height
        draw_text_shadow(d, (60, y), line, title_font, (255, 255, 255))

    # ── Decorative line above footer ──
    footer_line_y = H - 220
    d.line([(100, footer_line_y), (W - 100, footer_line_y)],
           fill=(200, 200, 200), width=1)

    # ── Bottom: Site branding ──
    # Site icon (circle with R)
    circle_cx, circle_cy = W // 2, H - 160
    circle_r = 30
    d.ellipse(
        [(circle_cx - circle_r, circle_cy - circle_r),
         (circle_cx + circle_r, circle_cy + circle_r)],
        fill=(255, 255, 255),
    )
    r_font = font(32, 1)
    r_bbox = r_font.getbbox("R")
    r_w = r_bbox[2] - r_bbox[0]
    r_h = r_bbox[3] - r_bbox[1]
    d.text((circle_cx - r_w // 2, circle_cy - r_h // 2 - 3), "R",
           font=r_font, fill=top_col)

    # Site name
    site_font = font(26, 0)
    site_bbox = site_font.getbbox(SITE_LABEL)
    site_w = site_bbox[2] - site_bbox[0]
    d.text(((W - site_w) // 2, H - 110), SITE_LABEL,
           font=site_font, fill=(255, 255, 255))

    # Save
    out_path = os.path.join(OUT, f"pin_{slug[:100]}.png")
    img.save(out_path, "PNG", quality=95)
    return out_path


def main():
    # Read URLs
    url_file = os.path.join(BASE, "all_urls.txt")
    with open(url_file) as f:
        urls = [u.strip() for u in f if u.strip()]

    print(f"Found {len(urls)} URLs in all_urls.txt")

    # Fetch titles from REST API
    api_posts = fetch_posts_from_api()

    # Generate pins
    count = 0
    for url in urls:
        slug = slug_from_url(url)
        if not slug:
            continue

        # Use API title if available, else fallback
        if slug in api_posts:
            import html
            title = html.unescape(api_posts[slug]["title"])
        else:
            title = title_from_slug(slug)
            print(f"  [fallback title] {slug}")

        cat = detect_category(slug, title)
        out = generate_pin(slug, title, cat)
        count += 1
        print(f"  [{count:02d}] {get_category_label(cat):18s} → {os.path.basename(out)}")

    print(f"\nDone! Generated {count} pin images in {OUT}/")


if __name__ == "__main__":
    main()
