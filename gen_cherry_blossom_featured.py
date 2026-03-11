#!/usr/bin/env python3
"""Generate featured image for Korea Cherry Blossom Season 2026 guide."""
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

def draw_text_shadow(draw, xy, text, fnt, fill, shadow=(200,180,180)):
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

# Soft pink-to-white gradient (cherry blossom theme)
draw_gradient(d, W, H, (255, 210, 220), (255, 245, 248))

# Decorative diagonal accent
for i in range(60):
    d.line([(0, H//2 - 30 + i), (W, H//3 - 30 + i)], fill=(255, 180, 200))

# Top bar - category
d.rectangle([(0, 0), (W, 50)], fill=(200, 100, 120))
d.text((30, 10), "KOREA TRAVEL", font=font(24, 1), fill=(255, 255, 255))
d.text((W - 250, 12), "MARCH 12, 2026", font=font(20), fill=(255, 230, 235))

# Category badge
d.rounded_rectangle([(30, 70), (210, 105)], radius=5, fill=(190, 80, 110))
d.text((42, 74), "KOREA TRAVEL", font=font(22, 1), fill=(255, 255, 255))

# Main title (darker text for light background)
title_font = font(48, 1)
title = "Korea Cherry Blossom Season 2026"
lines = wrap_text(title, title_font, W - 80)
y = 125
for line in lines:
    draw_text_shadow(d, (40, y), line, title_font, (80, 30, 50), shadow=(220, 190, 200))
    y += 60

# Subtitle
sub_font = font(26)
sub = "Complete Guide: Dates, Festivals & Best Spots"
sub_lines = wrap_text(sub, sub_font, W - 80)
y += 15
for line in sub_lines:
    d.text((40, y), line, font=sub_font, fill=(140, 60, 80))
    y += 35

# Stats bar at bottom
d.rectangle([(0, H - 85), (W, H)], fill=(120, 50, 70))
stats = ["Mar 25 Jeju", "Apr 3 Seoul", "6 Festivals", "15+ Spots"]
sx = 40
stat_font = font(24, 1)
for s in stats:
    d.text((sx, H - 72), s, font=stat_font, fill=(255, 200, 215))
    sx += 280

# Site watermark
d.text((W - 280, H - 30), "rhythmicaleskimo.com", font=font(14), fill=(200, 150, 170))

img.save(os.path.join(BASE, "featured_cherry_blossom_2026.png"), quality=95)
print("featured_cherry_blossom_2026.png")
