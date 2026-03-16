#!/usr/bin/env python3
"""Generate featured image for Undercover Miss Hong article."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 630
img = Image.new("RGB", (W, H))
draw = ImageDraw.Draw(img)

# Bright red/gold gradient background - action comedy aesthetic
for y in range(H):
    r_ratio = y / H
    # Top: bright gold -> Bottom: deep red
    r = int(255 * (1 - r_ratio * 0.3))
    g = int(200 * (1 - r_ratio * 0.85))
    b = int(50 * (1 - r_ratio * 0.7))
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# Add diagonal action lines for dynamic feel
for i in range(0, W + H, 80):
    draw.line([(i, 0), (i - H, H)], fill=(255, 255, 255, 30), width=1)

# Add subtle overlay rectangles for depth
draw.rectangle([(40, 40), (W - 40, H - 40)], outline=(255, 215, 0), width=3)
draw.rectangle([(50, 50), (W - 50, H - 50)], outline=(255, 255, 255), width=1)

# Try to load a nice font, fall back to default
try:
    title_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Impact.ttf", 62)
    sub_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 32)
    tag_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 24)
    small_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 22)
except:
    title_font = ImageFont.load_default()
    sub_font = ImageFont.load_default()
    tag_font = ImageFont.load_default()
    small_font = ImageFont.load_default()

# Netflix badge
draw.rounded_rectangle([(80, 80), (230, 120)], radius=5, fill=(229, 9, 20))
draw.text((95, 85), "NETFLIX", fill="white", font=tag_font)

# K-Drama tag
draw.rounded_rectangle([(250, 80), (390, 120)], radius=5, fill=(255, 215, 0))
draw.text((265, 85), "K-DRAMA", fill=(30, 30, 30), font=tag_font)

# Main title
draw.text((80, 160), "UNDERCOVER", fill="white", font=title_font)
draw.text((80, 230), "MISS HONG", fill=(255, 215, 0), font=title_font)

# Korean title
draw.text((80, 310), "언더커버 미쓰홍", fill=(255, 255, 255), font=sub_font)

# Subtitle
draw.text((80, 370), "Park Shin-hye × Ko Kyung-pyo", fill=(255, 200, 200), font=sub_font)

# Rating badge
draw.rounded_rectangle([(80, 430), (320, 475)], radius=8, fill=(255, 215, 0))
draw.text((95, 437), "★ Peak 14.6% Ratings", fill=(30, 30, 30), font=tag_font)

# Year and review tag
draw.text((80, 500), "2026 Complete Review & Guide", fill=(220, 220, 220), font=sub_font)

# Site branding
draw.text((80, 560), "rhythmicaleskimo.com", fill=(180, 180, 180), font=small_font)

# Decorative star burst on right side
cx, cy = 950, 315
for angle in range(0, 360, 15):
    import math
    x1 = cx + 120 * math.cos(math.radians(angle))
    y1 = cy + 120 * math.sin(math.radians(angle))
    draw.line([(cx, cy), (int(x1), int(y1))], fill=(255, 215, 0, 80), width=2)

# Central circle with "TOP" badge
draw.ellipse([(890, 255), (1010, 375)], fill=(229, 9, 20), outline=(255, 215, 0), width=3)
draw.text((910, 280), "TOP", fill="white", font=title_font)

# "16 Episodes" badge
draw.rounded_rectangle([(870, 400), (1030, 440)], radius=5, fill="white")
draw.text((885, 405), "16 Episodes", fill=(30, 30, 30), font=tag_font)

out = "/Users/choijooyong/wordpress/featured_miss_hong.png"
img.save(out, "PNG", quality=95)
print(f"Saved: {out} ({os.path.getsize(out)} bytes)")
