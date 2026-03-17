#!/usr/bin/env python3
"""Generate 5 featured images for March 17 trending posts."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 630
BASE = os.path.dirname(os.path.abspath(__file__))

def find_font(size):
    for fname in ["HelveticaNeue-Bold", "HelveticaNeue", "Helvetica-Bold", "Helvetica", "Arial Bold", "Arial"]:
        for ext in [".ttc", ".ttf"]:
            for bdir in ["/System/Library/Fonts", "/Library/Fonts"]:
                path = os.path.join(bdir, fname + ext)
                if os.path.exists(path):
                    try:
                        return ImageFont.truetype(path, size)
                    except:
                        continue
    return ImageFont.load_default()

font_title = find_font(48)
font_sub = find_font(26)
font_badge = find_font(22)

def gradient_bg(colors):
    """Create gradient from color tuple (r1,g1,b1) -> (r2,g2,b2)"""
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    r1, g1, b1 = colors[0]
    r2, g2, b2 = colors[1]
    for y in range(H):
        t = y / H
        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)
        draw.line([(0, y), (W, y)], fill=(r, g, b))
    return img, draw

def add_decorative_circles(img, draw, color, positions):
    for cx, cy, rad, alpha in positions:
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        od.ellipse([cx-rad, cy-rad, cx+rad, cy+rad], fill=(*color, alpha))
        img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
        draw = ImageDraw.Draw(img)
    return img, draw

def draw_badge(draw, text, x, y, color):
    bb = draw.textbbox((0, 0), text, font=font_badge)
    bw = bb[2] - bb[0] + 30
    draw.rounded_rectangle([x, y, x + bw, y + 40], radius=15, fill=color)
    draw.text((x + 15, y + 8), text, fill="white", font=font_badge)

def draw_title_lines(draw, lines, x, y_start, line_height=58, colors=None):
    for i, line in enumerate(lines):
        c = colors[i] if colors and i < len(colors) else (45, 52, 54)
        draw.text((x, y_start + i * line_height), line, fill=c, font=font_title)

def draw_footer(draw, subtitle):
    draw.rectangle([0, H - 6, W, H], fill=(100, 100, 100))
    draw.text((70, H - 45), "rhythmicaleskimo.com", fill=(180, 180, 180), font=font_badge)
    if subtitle:
        draw.text((70, H - 80), subtitle, fill=(120, 120, 120), font=font_sub)

def save(img, name):
    out = os.path.join(BASE, name)
    img.save(out, "PNG", quality=95)
    print(f"  ✅ {name}")

# --- 1. BLACKPINK DEADLINE ---
img, draw = gradient_bg(((20, 20, 20), (50, 10, 30)))
img, draw = add_decorative_circles(img, draw, (255, 0, 100), [
    (150, 500, 100, 30), (1050, 130, 80, 25), (900, 500, 60, 20)
])
draw.rectangle([0, 0, W, 8], fill=(255, 0, 100))
draw_badge(draw, "K-POP COMEBACK", 70, 50, (255, 0, 100))
draw_title_lines(draw, [
    "BLACKPINK DEADLINE:",
    "The Comeback That",
    "Broke Every Record",
    "1.46M First-Day Sales"
], 70, 120, colors=[
    (255, 255, 255), (255, 255, 255), (255, 80, 150), (255, 80, 150)
])
draw_footer(draw, "Album Review | Track Analysis | Records")
draw.rectangle([0, H - 6, W, H], fill=(255, 0, 100))
save(img, "featured_blackpink_deadline.png")

# --- 2. SPICULE SKINCARE ---
img, draw = gradient_bg(((240, 248, 255), (220, 230, 245)))
img, draw = add_decorative_circles(img, draw, (100, 180, 255), [
    (200, 480, 110, 35), (1000, 150, 90, 25), (850, 500, 70, 30)
])
draw.rectangle([0, 0, W, 8], fill=(0, 150, 200))
draw_badge(draw, "K-BEAUTY TREND", 70, 50, (0, 150, 200))
draw_title_lines(draw, [
    "Spicule Skincare:",
    "K-Beauty's Microneedling",
    "Revolution in 2026",
    "The $20 Alternative"
], 70, 120, colors=[
    (30, 60, 90), (30, 60, 90), (0, 150, 200), (0, 150, 200)
])
draw_footer(draw, "What Are Spicules | Products | How to Use")
draw.rectangle([0, H - 6, W, H], fill=(0, 150, 200))
save(img, "featured_spicule_skincare.png")

# --- 3. STILL SHINING ---
img, draw = gradient_bg(((255, 245, 230), (255, 225, 200)))
img, draw = add_decorative_circles(img, draw, (255, 180, 100), [
    (180, 500, 100, 30), (1020, 120, 85, 25), (880, 480, 65, 20)
])
draw.rectangle([0, 0, W, 8], fill=(230, 126, 34))
draw_badge(draw, "K-DRAMA REVIEW", 70, 50, (230, 126, 34))
draw_title_lines(draw, [
    "Still Shining Review:",
    "Netflix's Most Visually",
    "Arresting K-Drama",
    "of 2026"
], 70, 120, colors=[
    (60, 40, 20), (60, 40, 20), (230, 126, 34), (230, 126, 34)
])
draw_footer(draw, "Park Jin Young | Kim Min Ju | IMDB 8.1")
draw.rectangle([0, H - 6, W, H], fill=(230, 126, 34))
save(img, "featured_still_shining.png")

# --- 4. CONVENIENCE STORE FOOD ---
img, draw = gradient_bg(((255, 250, 240), (255, 235, 210)))
img, draw = add_decorative_circles(img, draw, (255, 150, 50), [
    (160, 490, 110, 30), (1040, 140, 85, 25), (900, 510, 70, 20)
])
draw.rectangle([0, 0, W, 8], fill=(255, 100, 0))
draw_badge(draw, "KOREA TRAVEL & FOOD", 70, 50, (255, 100, 0))
draw_title_lines(draw, [
    "Korean Convenience",
    "Store Food Guide 2026:",
    "What Tourists Are",
    "Actually Buying"
], 70, 120, colors=[
    (60, 40, 10), (60, 40, 10), (255, 100, 0), (255, 100, 0)
])
draw_footer(draw, "CU | GS25 | 7-Eleven | Must-Try Items")
draw.rectangle([0, H - 6, W, H], fill=(255, 100, 0))
save(img, "featured_convenience_store_food.png")

# --- 5. ILLIT PRESS START ---
img, draw = gradient_bg(((250, 240, 255), (235, 220, 250)))
img, draw = add_decorative_circles(img, draw, (180, 100, 255), [
    (170, 500, 105, 30), (1030, 130, 80, 25), (870, 490, 65, 20)
])
draw.rectangle([0, 0, W, 8], fill=(150, 50, 255))
draw_badge(draw, "K-POP CONCERT", 70, 50, (150, 50, 255))
draw_title_lines(draw, [
    "ILLIT 'Press Start':",
    "First Concert Review",
    "& MAMIHLAPINATAPAI",
    "Comeback Preview"
], 70, 120, colors=[
    (50, 30, 80), (50, 30, 80), (150, 50, 255), (150, 50, 255)
])
draw_footer(draw, "Sold-Out Seoul Shows | New Album April 30")
draw.rectangle([0, H - 6, W, H], fill=(150, 50, 255))
save(img, "featured_illit_press_start.png")

print("\n✅ All 5 featured images generated!")
