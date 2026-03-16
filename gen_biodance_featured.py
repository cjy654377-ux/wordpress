#!/usr/bin/env python3
"""Generate featured image for Biodance Bio-Collagen Mask review."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 630
img = Image.new("RGB", (W, H))
draw = ImageDraw.Draw(img)

# Soft pink/white gradient background
for y in range(H):
    r = int(255 - (y / H) * 20)
    g = int(245 - (y / H) * 40)
    b = int(250 - (y / H) * 30)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# Decorative elements - soft circles
for cx, cy, rad, alpha in [(150, 500, 120, 40), (1050, 130, 90, 30), (900, 520, 70, 25), (300, 100, 60, 35)]:
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.ellipse([cx-rad, cy-rad, cx+rad, cy+rad], fill=(255, 182, 193, alpha))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

# Accent bar at top
draw.rectangle([0, 0, W, 8], fill=(255, 150, 170))

# Load font
font_title = None
font_sub = None
for fname in ["HelveticaNeue-Bold", "HelveticaNeue", "Helvetica-Bold", "Helvetica", "Arial Bold", "Arial"]:
    for ext in [".ttc", ".ttf"]:
        for base in ["/System/Library/Fonts", "/Library/Fonts"]:
            path = os.path.join(base, fname + ext)
            if os.path.exists(path):
                try:
                    font_title = ImageFont.truetype(path, 52)
                    font_sub = ImageFont.truetype(path, 28)
                    break
                except:
                    continue
        if font_title:
            break
    if font_title:
        break

if not font_title:
    font_title = ImageFont.load_default()
    font_sub = font_title

# Category badge
badge_text = "K-BEAUTY REVIEW"
bb = draw.textbbox((0, 0), badge_text, font=font_sub)
bw = bb[2] - bb[0] + 30
draw.rounded_rectangle([60, 50, 60 + bw, 95], radius=15, fill=(255, 105, 135))
draw.text((75, 53), badge_text, fill="white", font=font_sub)

# Title text - wrap manually
title_lines = [
    "Biodance Bio-Collagen",
    "Mask Review:",
    "Why This $3 Sheet Mask",
    "Broke TikTok in 2026"
]

y_start = 130
for i, line in enumerate(title_lines):
    color = (45, 52, 54) if i < 2 else (214, 48, 49)
    draw.text((70, y_start + i * 65), line, fill=color, font=font_title)

# Subtitle
draw.text((70, y_start + 4 * 65 + 20), "Ingredients | Results | Where to Buy", fill=(100, 100, 100), font=font_sub)

# Bottom bar
draw.rectangle([0, H - 6, W, H], fill=(255, 105, 135))

# Site watermark
draw.text((70, H - 45), "rhythmicaleskimo.com", fill=(180, 180, 180), font=font_sub)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "featured_biodance.png")
img.save(out, "PNG", quality=95)
print(f"Saved: {out}")
