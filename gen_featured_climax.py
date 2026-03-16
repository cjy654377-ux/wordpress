#!/usr/bin/env python3
"""Generate featured image for Climax K-Drama article."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 630
img = Image.new("RGB", (W, H))
draw = ImageDraw.Draw(img)

# Dark dramatic gradient: deep purple to black
for y in range(H):
    r = int(45 * (1 - y / H))
    g = int(10 * (1 - y / H))
    b = int(70 * (1 - y / H) + 20 * (y / H))
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# Add subtle red accent line
for x in range(100, 1100):
    for y in range(295, 298):
        draw.point((x, y), fill=(180, 30, 50))
    for y in range(430, 433):
        draw.point((x, y), fill=(180, 30, 50))

# Load font
font_paths = [
    "/System/Library/Fonts/HelveticaNeue.ttc",
    "/System/Library/Fonts/Helvetica.ttc",
    "/Library/Fonts/Arial.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
]
font_path = None
for fp in font_paths:
    if os.path.exists(fp):
        font_path = fp
        break

title_font = ImageFont.truetype(font_path, 52) if font_path else ImageFont.load_default()
sub_font = ImageFont.truetype(font_path, 28) if font_path else ImageFont.load_default()
tag_font = ImageFont.truetype(font_path, 20) if font_path else ImageFont.load_default()

# Tag line
draw.text((W // 2, 250), "K-DRAMA REVIEW 2026", font=tag_font, fill=(180, 30, 50), anchor="mm")

# Title
draw.text((W // 2, 340), "CLIMAX", font=title_font, fill=(255, 255, 255), anchor="mm")

# Korean title
korean_fonts = [
    "/System/Library/Fonts/AppleSDGothicNeo.ttc",
    "/Library/Fonts/NanumGothic.ttf",
]
kr_font_path = None
for fp in korean_fonts:
    if os.path.exists(fp):
        kr_font_path = fp
        break

kr_font = ImageFont.truetype(kr_font_path, 26) if kr_font_path else sub_font
draw.text((W // 2, 390), "\ud074\ub77c\uc774\ub9c9\uc2a4", font=kr_font, fill=(200, 200, 210), anchor="mm")

# Subtitle
draw.text((W // 2, 460), "Cast, Plot & Why Everyone Is Watching", font=sub_font, fill=(200, 200, 210), anchor="mm")

# Bottom credits
draw.text((W // 2, 540), "Ju Ji-hoon \u00b7 Ha Ji-won \u00b7 Nana \u00b7 Oh Jung-se \u00b7 Cha Joo-young", font=tag_font, fill=(140, 140, 160), anchor="mm")

# Site branding
draw.text((W // 2, 580), "rhythmicaleskimo.com", font=tag_font, fill=(100, 100, 120), anchor="mm")

out = "/Users/choijooyong/wordpress/featured_climax.png"
img.save(out, quality=95)
print(f"Saved: {out}")
