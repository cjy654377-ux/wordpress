#!/usr/bin/env python3
"""Generate featured image for comprehensive Iran war aftermath article."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 630
FONT = "/System/Library/Fonts/HelveticaNeue.ttc"
BASE = os.path.dirname(os.path.abspath(__file__))

def font(size, index=0):
    return ImageFont.truetype(FONT, size, index=index)

def draw_gradient(draw, w, h, top, bot):
    for y in range(h):
        r = int(top[0] + (bot[0]-top[0]) * y/h)
        g = int(top[1] + (bot[1]-top[1]) * y/h)
        b = int(top[2] + (bot[2]-top[2]) * y/h)
        draw.line([(0, y), (w, y)], fill=(r, g, b))

def shadow_text(draw, xy, text, fnt, fill):
    x, y = xy
    draw.text((x+2, y+2), text, font=fnt, fill=(0, 0, 0))
    draw.text(xy, text, font=fnt, fill=fill)

def wrap_text(text, fnt, max_w):
    words = text.split()
    lines, line = [], ""
    for w in words:
        test = f"{line} {w}".strip()
        if fnt.getbbox(test)[2] > max_w and line:
            lines.append(line)
            line = w
        else:
            line = test
    if line:
        lines.append(line)
    return lines

img = Image.new("RGB", (W, H))
d = ImageDraw.Draw(img)
draw_gradient(d, W, H, (15, 10, 35), (50, 20, 60))

# Grid of impact icons (colored blocks representing 12 effects)
colors = [
    (200,30,30), (220,140,0), (30,120,200), (200,60,60),
    (220,180,0), (40,160,80), (80,80,200), (180,60,120),
    (100,60,180), (200,100,30), (255,200,0), (60,180,180)
]
labels = ["WAR", "OIL", "CYBER", "FOOD", "FX", "DEFENSE",
          "FLIGHT", "SHIP", "GEO", "POLITICS", "NUCLEAR", "AI"]
for i, (c, lbl) in enumerate(zip(colors, labels)):
    row, col = i // 6, i % 6
    x1 = 640 + col * 90
    y1 = 200 + row * 90
    # Rounded rect with glow
    d.rounded_rectangle([(x1, y1), (x1+78, y1+78)], radius=8, fill=c)
    lf = font(13, 1)
    tw = lf.getbbox(lbl)[2]
    d.text((x1 + (78-tw)//2, y1+55), lbl, font=lf, fill=(255,255,255))

# Connecting lines between blocks
for i in range(5):
    x1 = 640 + i * 90 + 78
    y1 = 200 + 39
    d.line([(x1, y1), (x1+12, y1)], fill=(100, 100, 150), width=1)
d.line([(640+39, 278), (640+39, 290)], fill=(100, 100, 150), width=1)

# Alert banner
d.rectangle([(0, 0), (W, 50)], fill=(180, 20, 50))
shadow_text(d, (30, 9), "SPECIAL REPORT", font(26, 1), (255, 255, 255))
d.text((W-220, 12), "MARCH 2, 2026", font=font(22), fill=(255, 200, 200))

# Category
d.rounded_rectangle([(30, 70), (240, 105)], radius=5, fill=(120, 40, 140))
d.text((42, 74), "IN-DEPTH ANALYSIS", font=font(20, 1), fill=(255, 255, 255))

# Title
tf = font(44, 1)
title = "12 Ways the Iran War Is Reshaping the World Right Now"
lines = wrap_text(title, tf, 580)
y = 125
for line in lines:
    shadow_text(d, (35, y), line, tf, (255, 255, 255))
    y += 56

# Subtitle
sf = font(22)
sub = "From oil shocks to nuclear fears, cyber warfare to the largest refugee crisis in history"
slines = wrap_text(sub, sf, 580)
y += 10
for line in slines:
    d.text((35, y), line, font=sf, fill=(200, 180, 220))
    y += 30

# Bottom bar with key stats
d.rectangle([(0, H-70), (W, H)], fill=(10, 5, 25))
items = [("OIL +8%", (220,140,0)), ("3,400 FLIGHTS", (30,120,200)),
         ("$5,400 GOLD", (220,180,0)), ("70% HORMUZ DROP", (200,30,30))]
px = 40
for text, color in items:
    d.text((px, H-55), text, font=font(22, 1), fill=color)
    px += 290

img.save(os.path.join(BASE, "featured_iran_aftermath.png"), quality=95)
print("featured_iran_aftermath.png")
