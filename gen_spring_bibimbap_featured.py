from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 630
img = Image.new("RGB", (W, H), "#2d5016")
draw = ImageDraw.Draw(img)

# Warm spring gradient background
for y in range(H):
    r = int(45 + (y / H) * 60)
    g = int(100 + (1 - y / H) * 80)
    b = int(22 + (y / H) * 30)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# Decorative circles (food plate aesthetic)
draw.ellipse([400, 120, 800, 520], fill="#3a6b1e", outline="#5a9b2e", width=3)
draw.ellipse([420, 140, 780, 500], fill="#4a7b28", outline="#6aab3e", width=2)
draw.ellipse([450, 170, 750, 470], fill="#5a8b32", outline="#7abb4e", width=2)

# Inner bowl detail
draw.ellipse([470, 190, 730, 450], fill="#f5e6c8", outline="#d4c4a0", width=2)

# Rice base
draw.ellipse([490, 250, 710, 410], fill="#fff8e7", outline="#e8d8b0", width=1)

# Green cabbage strips
for i in range(5):
    x = 510 + i * 35
    draw.ellipse([x, 270, x + 30, 350], fill="#7bc043", outline="#5a9b2e", width=1)

# Red gochujang sauce center
draw.ellipse([570, 310, 630, 370], fill="#c0392b", outline="#a93226", width=1)

# Egg on top
draw.ellipse([555, 280, 645, 355], fill="#ffffff", outline="#f0e0c0", width=1)
draw.ellipse([580, 300, 620, 335], fill="#f39c12", outline="#e67e22", width=1)

# Small garnish dots (sesame seeds)
for pos in [(520, 360), (540, 380), (660, 360), (640, 380), (580, 390)]:
    draw.ellipse([pos[0], pos[1], pos[0]+5, pos[1]+5], fill="#d4a017")

# Text
font_paths = [
    "/System/Library/Fonts/Helvetica.ttc",
    "/System/Library/Fonts/HelveticaNeue.ttc",
    "/Library/Fonts/Arial.ttf",
]
font_path = None
for fp in font_paths:
    if os.path.exists(fp):
        font_path = fp
        break

try:
    title_font = ImageFont.truetype(font_path, 42) if font_path else ImageFont.load_default()
    sub_font = ImageFont.truetype(font_path, 24) if font_path else ImageFont.load_default()
    tag_font = ImageFont.truetype(font_path, 18) if font_path else ImageFont.load_default()
except:
    title_font = ImageFont.load_default()
    sub_font = ImageFont.load_default()
    tag_font = ImageFont.load_default()

# Top tag
draw.rounded_rectangle([430, 40, 770, 75], radius=15, fill="#c0392b")
draw.text((460, 44), "VIRAL TIKTOK RECIPE 2026", fill="white", font=tag_font)

# Bottom text area
draw.rectangle([0, 480, W, H], fill=(0, 0, 0, 180))
overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
overlay_draw = ImageDraw.Draw(overlay)
overlay_draw.rectangle([0, 480, W, H], fill=(0, 0, 0, 160))
img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
draw = ImageDraw.Draw(img)

# Title text
title1 = "Spring Cabbage Bibimbap"
title2 = "Korea's #1 Viral Recipe"
draw.text((W // 2, 510), title1, fill="white", font=title_font, anchor="mt")
draw.text((W // 2, 565), title2, fill="#7bc043", font=sub_font, anchor="mt")

# Site branding
draw.text((W // 2, 600), "rhythmicaleskimo.com", fill="#aaaaaa", font=tag_font, anchor="mt")

# Decorative leaf elements on sides
for y_pos in [100, 200, 300, 400]:
    # Left leaves
    draw.ellipse([30, y_pos, 80, y_pos + 40], fill="#5a9b2e", outline="#3a6b1e")
    draw.ellipse([60, y_pos + 10, 120, y_pos + 35], fill="#4a8b28", outline="#3a6b1e")
    # Right leaves
    draw.ellipse([1120, y_pos, 1170, y_pos + 40], fill="#5a9b2e", outline="#3a6b1e")
    draw.ellipse([1080, y_pos + 10, 1140, y_pos + 35], fill="#4a8b28", outline="#3a6b1e")

out = "/Users/choijooyong/wordpress/featured_spring_bibimbap.png"
img.save(out, "PNG")
print(f"Saved: {out}")
