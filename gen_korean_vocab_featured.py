#!/usr/bin/env python3
"""Generate featured image for Korean Vocabulary from Boyfriend on Demand."""
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

# Teal-to-dark blue gradient (educational/language theme)
draw_gradient(d, W, H, (30, 150, 160), (15, 30, 80))

# Decorative diagonal accent
for i in range(60):
    d.line([(0, H//2 - 30 + i), (W, H//3 - 30 + i)], fill=(60, 200, 200))

# Top bar - category
d.rectangle([(0, 0), (W, 50)], fill=(20, 100, 120))
d.text((30, 10), "KOREAN LANGUAGE", font=font(24, 1), fill=(255, 255, 255))
d.text((W - 250, 12), "MARCH 12, 2026", font=font(20), fill=(180, 230, 240))

# Category badge
d.rounded_rectangle([(30, 70), (240, 105)], radius=5, fill=(30, 130, 150))
d.text((42, 74), "KOREAN LANGUAGE", font=font(22, 1), fill=(255, 255, 255))

# Main title
title_font = font(48, 1)
title = "30 Korean Words from Boyfriend on Demand"
lines = wrap_text(title, title_font, W - 80)
y = 125
for line in lines:
    draw_text_shadow(d, (40, y), line, title_font, (255, 255, 255))
    y += 60

# Subtitle
sub_font = font(26)
sub = "The Ultimate K-Drama Vocabulary Guide"
sub_lines = wrap_text(sub, sub_font, W - 80)
y += 15
for line in sub_lines:
    d.text((40, y), line, font=sub_font, fill=(140, 220, 230))
    y += 35

# Stats bar at bottom
d.rectangle([(0, H - 85), (W, H)], fill=(10, 20, 50))
stats = ["30 Words", "5 Categories", "\ud55c\uad6d\uc5b4", "Free Guide"]
sx = 40
stat_font = font(24, 1)
for s in stats:
    d.text((sx, H - 72), s, font=stat_font, fill=(100, 210, 230))
    sx += 280

# Site watermark
d.text((W - 280, H - 30), "rhythmicaleskimo.com", font=font(14), fill=(80, 140, 160))

img.save(os.path.join(BASE, "featured_korean_vocab_boyfriend.png"), quality=95)
print("featured_korean_vocab_boyfriend.png")
