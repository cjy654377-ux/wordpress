#!/usr/bin/env python3
"""Generate featured image for Boyfriend on Demand K-drama guide."""
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

# Pink-to-purple gradient (romantic K-drama theme)
draw_gradient(d, W, H, (220, 80, 140), (80, 30, 120))

# Decorative diagonal accent
for i in range(60):
    d.line([(0, H//2 - 30 + i), (W, H//3 - 30 + i)], fill=(255, 120, 180))

# Top bar - category
d.rectangle([(0, 0), (W, 50)], fill=(160, 40, 100))
d.text((30, 10), "K-DRAMA GUIDE", font=font(24, 1), fill=(255, 255, 255))
d.text((W - 250, 12), "MARCH 12, 2026", font=font(20), fill=(255, 210, 230))

# Category badge
d.rounded_rectangle([(30, 70), (210, 105)], radius=5, fill=(200, 50, 120))
d.text((42, 74), "K-DRAMA GUIDE", font=font(22, 1), fill=(255, 255, 255))

# Main title
title_font = font(48, 1)
title = "Boyfriend on Demand: Complete Guide"
lines = wrap_text(title, title_font, W - 80)
y = 125
for line in lines:
    draw_text_shadow(d, (40, y), line, title_font, (255, 255, 255))
    y += 60

# Subtitle
sub_font = font(26)
sub = "Jisoo's Netflix Hit — Cast, Cameos & Review"
sub_lines = wrap_text(sub, sub_font, W - 80)
y += 15
for line in sub_lines:
    d.text((40, y), line, font=sub_font, fill=(255, 200, 220))
    y += 35

# Stats bar at bottom
d.rectangle([(0, H - 85), (W, H)], fill=(50, 15, 60))
stats = ["10 Episodes", "69 Countries", "#1 Netflix", "9 Cameos"]
sx = 40
stat_font = font(24, 1)
for s in stats:
    d.text((sx, H - 72), s, font=stat_font, fill=(255, 150, 200))
    sx += 280

# Site watermark
d.text((W - 280, H - 30), "rhythmicaleskimo.com", font=font(14), fill=(180, 120, 160))

img.save(os.path.join(BASE, "featured_boyfriend_on_demand.png"), quality=95)
print("featured_boyfriend_on_demand.png")
