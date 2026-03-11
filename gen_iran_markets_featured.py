#!/usr/bin/env python3
"""Generate featured image for Iran War global markets article."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 630
BASE = os.path.dirname(os.path.abspath(__file__))
FONT = "/System/Library/Fonts/HelveticaNeue.ttc"

def font(size, index=0):
    return ImageFont.truetype(FONT, size, index=index)

def draw_gradient(draw, w, h, top_color, bot_color):
    for y in range(h):
        r = int(top_color[0] + (bot_color[0]-top_color[0]) * y/h)
        g = int(top_color[1] + (bot_color[1]-top_color[1]) * y/h)
        b = int(top_color[2] + (bot_color[2]-top_color[2]) * y/h)
        draw.line([(0, y), (w, y)], fill=(r, g, b))

def draw_text_shadow(draw, xy, text, fnt, fill, shadow=(0,0,0)):
    x, y = xy
    draw.text((x+2, y+2), text, font=fnt, fill=shadow)
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

# ── Main Image ──
img = Image.new("RGB", (W, H))
d = ImageDraw.Draw(img)

# Dark red-to-black gradient (financial crisis theme)
draw_gradient(d, W, H, (80, 15, 10), (10, 5, 5))

# Decorative diagonal accent lines (orange/gold streaks)
for i in range(80):
    alpha_factor = 1 - i/80
    r = int(200 * alpha_factor)
    g = int(100 * alpha_factor)
    d.line([(0, H//2 - 40 + i), (W, H//3 - 40 + i)], fill=(r, g, 0))

# Second accent (red glow)
for i in range(40):
    alpha_factor = 1 - i/40
    r = int(160 * alpha_factor)
    d.line([(0, H//3 + 80 + i), (W, H//4 + 80 + i)], fill=(r, 20, 10))

# Top bar - category
d.rectangle([(0, 0), (W, 50)], fill=(120, 20, 15))
d.text((30, 10), "WORLD FINANCIAL ISSUES", font=font(24, 1), fill=(255, 220, 180))
d.text((W - 250, 12), "MARCH 11, 2026", font=font(20), fill=(255, 200, 160))

# Category badge
d.rounded_rectangle([(30, 70), (260, 105)], radius=5, fill=(180, 50, 20))
d.text((42, 74), "GEOPOLITICS & MARKETS", font=font(20, 1), fill=(255, 255, 255))

# Main title
title_font = font(46, 1)
title = "How the 2026 Iran War Is Reshaping Global Markets"
lines = wrap_text(title, title_font, W - 80)
y = 125
for line in lines:
    draw_text_shadow(d, (40, y), line, title_font, (255, 255, 255))
    y += 58

# Subtitle
sub_font = font(26)
sub = "Oil, Gold, Stocks, and What Comes Next"
y += 15
d.text((40, y), sub, font=sub_font, fill=(255, 190, 100))

# Downward chart lines (visual decoration)
import random
random.seed(42)
chart_y_base = y + 60
for cx in range(0, W, 3):
    noise = random.randint(-8, 8)
    trend = int(30 * (cx / W))  # downward trend
    cy = chart_y_base + trend + noise
    color_r = min(255, 180 + int(75 * cx / W))
    d.point((cx, cy), fill=(color_r, 80, 40))
    d.point((cx, cy+1), fill=(color_r, 80, 40))

# Stats bar at bottom
d.rectangle([(0, H - 90), (W, H)], fill=(15, 5, 5))
d.line([(0, H - 90), (W, H - 90)], fill=(200, 80, 30), width=2)

stats = [
    ("Brent $126", (255, 160, 60)),
    ("Gold $5,400", (255, 215, 0)),
    ("S&P -4.2%", (255, 80, 80)),
    ("BTC -47%", (255, 60, 60)),
]
sx = 40
for text, color in stats:
    d.text((sx, H - 78), text, font=font(28, 1), fill=color)
    sx += 280

# Site watermark
d.text((W - 280, H - 28), "rhythmicaleskimo.com", font=font(14), fill=(140, 100, 80))

out = os.path.join(BASE, "featured_iran_war_markets.png")
img.save(out, quality=95)
print(f"Done: {out}")
