from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 630
img = Image.new("RGB", (W, H))
draw = ImageDraw.Draw(img)

# White to mint gradient
for y in range(H):
    r = int(255 - (255 - 230) * y / H)
    g = int(255 - (255 - 250) * y / H)
    b = int(255 - (255 - 245) * y / H)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# Decorative circles (medical/beauty aesthetic)
for cx, cy, radius, color in [
    (950, 120, 180, (200, 235, 225, 60)),
    (150, 500, 120, (220, 240, 235, 50)),
    (1050, 480, 90, (210, 230, 225, 55)),
]:
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=color)
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

# Accent line
draw.rectangle([80, 200, 86, 420], fill=(120, 190, 170))

# Try system fonts
def get_font(size, bold=False):
    paths = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/SFNSDisplay.ttf",
        "/Library/Fonts/Arial Bold.ttf" if bold else "/Library/Fonts/Arial.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size, index=1 if bold and p.endswith(".ttc") else 0)
            except:
                try:
                    return ImageFont.truetype(p, size)
                except:
                    continue
    return ImageFont.load_default()

# Title
title_font = get_font(52, bold=True)
sub_font = get_font(30)
tag_font = get_font(22)
brand_font = get_font(18)

# Tag
draw.rounded_rectangle([100, 140, 290, 178], radius=12, fill=(120, 190, 170))
draw.text((118, 144), "K-BEAUTY 2026", fill="white", font=tag_font)

# Title lines
lines = ["Dr. Melaxin Multi Balm", "Review: TikTok's", "'Botox in a Stick'"]
y_pos = 210
for line in lines:
    draw.text((110, y_pos), line, fill=(30, 40, 50), font=title_font)
    y_pos += 62

# Subtitle
draw.text((110, y_pos + 20), "Ingredients | Results | Expert Verdict", fill=(100, 120, 130), font=sub_font)

# Brand watermark
draw.text((110, 560), "rhythmicaleskimo.com", fill=(160, 180, 175), font=brand_font)

# Decorative product stick shape on right side
draw.rounded_rectangle([850, 180, 920, 500], radius=20, fill=(180, 160, 200))
draw.rounded_rectangle([855, 185, 915, 340], radius=16, fill=(200, 180, 220))
draw.rounded_rectangle([860, 350, 910, 490], radius=10, fill=(240, 235, 245))
# Cap
draw.rounded_rectangle([845, 160, 925, 195], radius=10, fill=(160, 140, 180))

# Small text on stick
stick_font = get_font(12)
draw.text((862, 370), "Dr.Melaxin", fill=(160, 140, 180), font=stick_font)
draw.text((862, 385), "Multi Balm", fill=(160, 140, 180), font=stick_font)

out = "/Users/choijooyong/wordpress/featured_dr_melaxin.png"
img.save(out, "PNG", quality=95)
print(f"Saved: {out} ({os.path.getsize(out)} bytes)")
