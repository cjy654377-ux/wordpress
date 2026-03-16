#!/usr/bin/env python3
"""Generate featured image for Korean Glass Hair article."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 630
img = Image.new("RGB", (W, H))
draw = ImageDraw.Draw(img)

# Gradient: silver/pearl tones (left to right)
for x in range(W):
    r = int(180 + (230 - 180) * x / W)
    g = int(185 + (225 - 185) * x / W)
    b = int(200 + (240 - 200) * x / W)
    draw.line([(x, 0), (x, H)], fill=(r, g, b))

# Add subtle shimmer streaks
for i in range(8):
    y_start = 50 + i * 72
    for x in range(W):
        alpha = max(0, min(255, int(40 * (1 - abs(x - W//2) / (W//2)))))
        current = img.getpixel((x, y_start))
        new_r = min(255, current[0] + alpha // 3)
        new_g = min(255, current[1] + alpha // 3)
        new_b = min(255, current[2] + alpha // 2)
        img.putpixel((x, y_start), (new_r, new_g, new_b))
        if y_start + 1 < H:
            current2 = img.getpixel((x, y_start + 1))
            img.putpixel((x, y_start + 1), (min(255, current2[0] + alpha // 4), min(255, current2[1] + alpha // 4), min(255, current2[2] + alpha // 3)))

# Decorative circles (pearl effect)
for cx, cy, radius in [(150, 120, 60), (1050, 500, 45), (950, 100, 35), (200, 480, 40)]:
    for angle_step in range(360):
        import math
        ax = cx + int(radius * math.cos(math.radians(angle_step)))
        ay = cy + int(radius * math.sin(math.radians(angle_step)))
        if 0 <= ax < W and 0 <= ay < H:
            draw.point((ax, ay), fill=(220, 225, 235))

# Load font
font_paths = [
    "/System/Library/Fonts/HelveticaNeue.ttc",
    "/System/Library/Fonts/Helvetica.ttc",
    "/Library/Fonts/Arial.ttf",
]
font_large = font_small = None
for fp in font_paths:
    if os.path.exists(fp):
        try:
            font_large = ImageFont.truetype(fp, 52)
            font_small = ImageFont.truetype(fp, 28)
            break
        except:
            continue
if not font_large:
    font_large = ImageFont.load_default()
    font_small = ImageFont.load_default()

# Title text with shadow
title_lines = ["Korean Glass Hair", "Trend 2026"]
subtitle = "The 7-Step Routine for Mirror-Shine Hair"

y_pos = 180
for line in title_lines:
    bbox = draw.textbbox((0, 0), line, font=font_large)
    tw = bbox[2] - bbox[0]
    x = (W - tw) // 2
    # Shadow
    draw.text((x + 2, y_pos + 2), line, fill=(120, 125, 140), font=font_large)
    # Main text
    draw.text((x, y_pos), line, fill=(45, 52, 54), font=font_large)
    y_pos += 65

# Subtitle
bbox = draw.textbbox((0, 0), subtitle, font=font_small)
tw = bbox[2] - bbox[0]
x = (W - tw) // 2
draw.text((x, y_pos + 30), subtitle, fill=(80, 85, 100), font=font_small)

# Bottom bar
draw.rectangle([(0, H - 50), (W, H)], fill=(45, 52, 54))
site_text = "rhythmicaleskimo.com"
bbox = draw.textbbox((0, 0), site_text, font=font_small)
tw = bbox[2] - bbox[0]
draw.text(((W - tw) // 2, H - 44), site_text, fill=(220, 225, 235), font=font_small)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "featured_glass_hair.png")
img.save(out, "PNG", quality=95)
print(f"Saved: {out}")
