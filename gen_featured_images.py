#!/usr/bin/env python3
"""Generate featured images for Iran war + Oil crisis articles using PIL."""
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

# ── Image 1: Iran Strikes ──
img = Image.new("RGB", (W, H))
d = ImageDraw.Draw(img)
draw_gradient(d, W, H, (30, 0, 0), (120, 15, 15))

# Diagonal accent stripe
for i in range(80):
    alpha = int(255 * (1 - i/80))
    d.line([(0, H//2 - 40 + i), (W, H//3 - 40 + i)], fill=(200, 30, 30, alpha))

# Breaking news banner
d.rectangle([(0, 0), (W, 55)], fill=(200, 20, 20))
draw_text_shadow(d, (30, 10), "BREAKING NEWS", font(28, 1), (255, 255, 255))
d.text((W-220, 14), "MARCH 2, 2026", font=font(22), fill=(255, 200, 200))

# Category badge
d.rounded_rectangle([(30, 80), (220, 115)], radius=5, fill=(255, 60, 60))
d.text((45, 84), "WORLD NEWS", font=font(22, 1), fill=(255, 255, 255))

# Title
title_font = font(52, 1)
title = "US-Israel Strikes Kill Iran's Supreme Leader Khamenei"
lines = wrap_text(title, title_font, W - 80)
y = 140
for line in lines:
    draw_text_shadow(d, (40, y), line, title_font, (255, 255, 255))
    y += 65

# Subtitle
sub_font = font(28)
sub = "1,000+ targets hit across 130 cities — Iran retaliates with missiles on Gulf states"
sub_lines = wrap_text(sub, sub_font, W - 80)
y += 15
for line in sub_lines:
    d.text((40, y), line, font=sub_font, fill=(255, 180, 180))
    y += 38

# Stats bar at bottom
d.rectangle([(0, H-90), (W, H)], fill=(20, 0, 0))
stats = [("555+", "Killed in Iran"), ("4", "US Troops KIA"), ("2,000+", "Strikes"), ("6", "Countries Hit")]
sx = 40
for num, label in stats:
    d.text((sx, H-82), num, font=font(32, 1), fill=(255, 80, 80))
    bw = font(32, 1).getbbox(num)[2]
    d.text((sx + bw + 8, H-74), label, font=font(20), fill=(200, 200, 200))
    sx += 280

img.save(os.path.join(BASE, "featured_iran_strikes.png"), quality=95)
print("✅ featured_iran_strikes.png")

# ── Image 2: Oil Crisis ──
img2 = Image.new("RGB", (W, H))
d2 = ImageDraw.Draw(img2)
draw_gradient(d2, W, H, (10, 10, 40), (40, 60, 100))

# Oil price chart visual (rising bars)
bar_x = 50
bar_colors = [(60,120,60), (70,130,60), (80,140,50), (100,150,40),
              (120,140,30), (150,120,20), (180,80,20), (200,50,20), (220,30,30), (240,20,20)]
bar_heights = [120, 135, 140, 160, 180, 220, 280, 320, 380, 420]
for i, (c, bh) in enumerate(zip(bar_colors, bar_heights)):
    bh_scaled = int(bh * 0.6)
    x1 = bar_x + i * 60
    d2.rectangle([(x1, H - 90 - bh_scaled), (x1 + 45, H - 90)], fill=c)

# Overlay gradient for readability
for y in range(H):
    alpha = int(180 * (1 - y/H))
    d2.line([(0, y), (W, y)], fill=(10, 10, 40, alpha))

# Breaking banner
d2.rectangle([(0, 0), (W, 55)], fill=(200, 140, 0))
draw_text_shadow(d2, (30, 10), "MARKET ALERT", font(28, 1), (255, 255, 255))
d2.text((W-220, 14), "MARCH 2, 2026", font=font(22), fill=(60, 40, 0))

# Category
d2.rounded_rectangle([(30, 80), (250, 115)], radius=5, fill=(200, 140, 0))
d2.text((45, 84), "GLOBAL ECONOMY", font=font(22, 1), fill=(255, 255, 255))

# Title
t2 = "Oil Prices Surge 8% as Iran War Threatens Global Energy Supply"
lines2 = wrap_text(t2, title_font, W - 80)
y2 = 140
for line in lines2:
    draw_text_shadow(d2, (40, y2), line, title_font, (255, 255, 255))
    y2 += 65

# Subtitle
sub2 = "Strait of Hormuz under threat — stocks plunge, gas prices rising worldwide"
sub2_lines = wrap_text(sub2, sub_font, W - 80)
y2 += 15
for line in sub2_lines:
    d2.text((40, y2), line, font=sub_font, fill=(255, 220, 150))
    y2 += 38

# Price indicators at bottom
d2.rectangle([(0, H-90), (W, H)], fill=(10, 10, 30))
prices = [("WTI $72.41", "+8.0%"), ("BRENT $79.05", "+8.5%"), ("GAS $2.98", "Rising"), ("S&P 500", "Plunging")]
px = 40
for name, chg in prices:
    d2.text((px, H-82), name, font=font(24, 1), fill=(255, 200, 80))
    nw = font(24, 1).getbbox(name)[2]
    color = (255, 80, 80) if "+" in chg or chg in ("Rising", "Plunging") else (100, 255, 100)
    d2.text((px + nw + 10, H-76), chg, font=font(20), fill=color)
    px += 290

img2.save(os.path.join(BASE, "featured_oil_crisis.png"), quality=95)
print("✅ featured_oil_crisis.png")
