#!/usr/bin/env python3
"""Generate featured images for calculator posts — bold text on gradient background."""
from PIL import Image, ImageDraw, ImageFont
import os, sys

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "calc_imgs")
os.makedirs(OUT_DIR, exist_ok=True)

CALCS = [
    {"file": "tax_calculator.png", "title": "TAX\nCALCULATOR", "colors": ((22,33,62), (15,52,96))},
    {"file": "mortgage_calculator.png", "title": "MORTGAGE\nCALCULATOR", "colors": ((233,69,96), (15,52,96))},
    {"file": "loan_calculator.png", "title": "LOAN\nCALCULATOR", "colors": ((15,52,96), (44,62,80))},
    {"file": "salary_calculator.png", "title": "SALARY\nCALCULATOR", "colors": ((39,174,96), (22,33,62))},
    {"file": "investment_calculator.png", "title": "INVESTMENT\nCALCULATOR", "colors": ((142,68,173), (22,33,62))},
]

W, H = 1200, 630

def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

def make_gradient(draw, c1, c2):
    for y in range(H):
        color = lerp(c1, c2, y / H)
        draw.line([(0, y), (W, y)], fill=color)

def get_font(size):
    paths = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/SFNSDisplay.ttf",
        "/Library/Fonts/Arial Bold.ttf",
        "/System/Library/Fonts/HelveticaNeue.ttc",
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except:
                continue
    return ImageFont.load_default()

for calc in CALCS:
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    make_gradient(draw, calc["colors"][0], calc["colors"][1])

    # Decorative lines
    for i in range(5):
        y = 50 + i * 130
        draw.line([(0, y), (W, y)], fill=(255,255,255,15), width=1)

    font_big = get_font(90)
    lines = calc["title"].split("\n")
    total_h = sum(draw.textbbox((0,0), l, font=font_big)[3] - draw.textbbox((0,0), l, font=font_big)[1] for l in lines)
    gap = 15
    total_h += gap * (len(lines) - 1)
    y_start = (H - total_h) // 2

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font_big)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        x = (W - tw) // 2
        # Shadow
        draw.text((x+3, y_start+3), line, font=font_big, fill=(0,0,0,80))
        draw.text((x, y_start), line, font=font_big, fill=(255,255,255))
        y_start += th + gap

    # Subtitle
    font_sm = get_font(24)
    sub = "Free Online Calculator Tool"
    bbox = draw.textbbox((0, 0), sub, font=font_sm)
    sw = bbox[2] - bbox[0]
    draw.text(((W - sw) // 2, y_start + 20), sub, font=font_sm, fill=(255,255,255,200))

    # Brand
    font_brand = get_font(16)
    draw.text((W - 280, H - 40), "rhythmicaleskimo.com", font=font_brand, fill=(255,255,255,150))

    path = os.path.join(OUT_DIR, calc["file"])
    img.save(path, "PNG")
    print(f"  ✅ {calc['file']}")

print(f"\nDone: {len(CALCS)} images in {OUT_DIR}")
