#!/usr/bin/env python3
"""Generate featured image for BTS ARIRANG album analysis article."""
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

# Deep purple-to-black gradient (BTS Arirang era colors)
draw_gradient(d, W, H, (60, 20, 80), (10, 5, 20))

# Decorative diagonal accent
for i in range(60):
    alpha = int(200 * (1 - i/60))
    d.line([(0, H//2 - 30 + i), (W, H//3 - 30 + i)], fill=(140, 80, 200))

# Top bar - category
d.rectangle([(0, 0), (W, 50)], fill=(100, 40, 140))
d.text((30, 10), "K-POP DEEP DIVE", font=font(24, 1), fill=(255, 255, 255))
d.text((W - 250, 12), "MARCH 10, 2026", font=font(20), fill=(220, 200, 255))

# Category badge
d.rounded_rectangle([(30, 70), (180, 105)], radius=5, fill=(140, 60, 200))
d.text((42, 74), "BTS ARIRANG", font=font(22, 1), fill=(255, 255, 255))

# Main title
title_font = font(48, 1)
title = "BTS ARIRANG: The Cultural Meaning Behind Every Song"
lines = wrap_text(title, title_font, W - 80)
y = 125
for line in lines:
    draw_text_shadow(d, (40, y), line, title_font, (255, 255, 255))
    y += 60

# Subtitle
sub_font = font(26)
sub = "Han, Heung, and 600 Years of Korean Soul in 14 Tracks"
sub_lines = wrap_text(sub, sub_font, W - 80)
y += 15
for line in sub_lines:
    d.text((40, y), line, font=sub_font, fill=(200, 180, 255))
    y += 35

# Korean text accent
korean_font = font(36)
d.text((40, y + 10), "아리랑, 아리랑, 아라리요", font=korean_font, fill=(180, 140, 220))

# Stats bar at bottom
d.rectangle([(0, H - 85), (W, H)], fill=(20, 8, 30))
stats = [("4.06M", "Pre-orders"), ("14", "Tracks"), ("82", "Tour Dates"), ("600yr", "Cultural Legacy")]
sx = 40
for num, label in stats:
    d.text((sx, H - 78), num, font=font(30, 1), fill=(180, 120, 255))
    bw = font(30, 1).getbbox(num)[2]
    d.text((sx + bw + 8, H - 70), label, font=font(18), fill=(180, 180, 200))
    sx += 280

# Site watermark
d.text((W - 280, H - 30), "rhythmicaleskimo.com", font=font(14), fill=(120, 100, 140))

img.save(os.path.join(BASE, "featured_bts_arirang_album.png"), quality=95)
print("✅ featured_bts_arirang_album.png")
