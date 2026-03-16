from PIL import Image, ImageDraw, ImageFont
import os

width, height = 1200, 630
img = Image.new('RGB', (width, height))
draw = ImageDraw.Draw(img)

# Romantic soft pink/lavender gradient
for y in range(height):
    r = int(255 - (y / height) * 50)   # 255 -> 205
    g = int(182 - (y / height) * 60)   # 182 -> 122
    b = int(193 + (y / height) * 62)   # 193 -> 255
    draw.line([(0, y), (width, y)], fill=(r, g, b))

# Decorative hearts
for cx, cy, sz in [(150, 120, 30), (1050, 100, 25), (200, 500, 20), (1000, 520, 22), (600, 80, 18)]:
    draw.ellipse([cx-sz, cy-sz, cx+sz//2, cy+sz], fill=(255, 200, 210, 180))
    draw.ellipse([cx-sz//2, cy-sz, cx+sz, cy+sz], fill=(255, 200, 210, 180))
    draw.polygon([(cx-sz, cy), (cx+sz, cy), (cx, cy+sz+10)], fill=(255, 200, 210, 180))

# Title text
try:
    font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 52)
    font_med = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 36)
    font_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 28)
except:
    font_large = ImageFont.load_default()
    font_med = ImageFont.load_default()
    font_small = ImageFont.load_default()

# Shadow + text
lines = ["Can This Love", "Be Translated?"]
y_start = 180
for i, line in enumerate(lines):
    bbox = draw.textbbox((0, 0), line, font=font_large)
    tw = bbox[2] - bbox[0]
    x = (width - tw) // 2
    y = y_start + i * 70
    draw.text((x+3, y+3), line, fill=(100, 60, 80), font=font_large)
    draw.text((x, y), line, fill=(255, 255, 255), font=font_large)

# Subtitle
sub = "K-Drama Review | Cast & Plot [2026]"
bbox = draw.textbbox((0, 0), sub, font=font_med)
tw = bbox[2] - bbox[0]
x = (width - tw) // 2
draw.text((x+2, y_start + 172), sub, fill=(100, 60, 80), font=font_med)
draw.text((x, y_start + 170), sub, fill=(255, 255, 255), font=font_med)

# Bottom tag
tag = "Kim Seon-ho | Go Youn-jung | Netflix"
bbox = draw.textbbox((0, 0), tag, font=font_small)
tw = bbox[2] - bbox[0]
x = (width - tw) // 2
draw.text((x, 530), tag, fill=(220, 180, 200), font=font_small)

# Decorative line
draw.line([(300, 440), (900, 440)], fill=(255, 220, 230), width=2)

out = "/Users/choijooyong/wordpress/featured_love_translated.png"
img.save(out, "PNG")
print(f"Saved: {out}")
