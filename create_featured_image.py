from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 630

# Build background as RGBA
img = Image.new("RGBA", (W, H), (10, 0, 20, 255))
draw = ImageDraw.Draw(img)

# Gradient background
for y in range(H):
    r = int(10 + 40 * (y / H))
    g = int(0 + 10 * (y / H))
    b = int(20 + 80 * (y / H))
    draw.line([(0, y), (W, y)], fill=(r, g, b, 255))

# Bokeh circles
overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
odraw = ImageDraw.Draw(overlay)
circles = [
    (150, 200, 120, (147, 51, 234, 30)),
    (900, 150, 180, (88, 28, 135, 25)),
    (600, 400, 200, (124, 58, 237, 20)),
    (350, 500, 100, (168, 85, 247, 35)),
    (1050, 450, 140, (107, 33, 168, 28)),
    (200, 80, 90, (192, 132, 252, 22)),
    (750, 100, 110, (139, 92, 246, 18)),
]
for cx, cy, radius, color in circles:
    for i in range(radius, 0, -2):
        alpha = int(color[3] * (i / radius))
        odraw.ellipse([cx - i, cy - i, cx + i, cy + i], fill=(color[0], color[1], color[2], alpha))

img = Image.alpha_composite(img, overlay)

# Subtle horizontal light streak
streak = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sdraw = ImageDraw.Draw(streak)
for y in range(280, 350):
    alpha = int(15 * (1 - abs(y - 315) / 35))
    sdraw.line([(0, y), (W, y)], fill=(147, 51, 234, alpha))
img = Image.alpha_composite(img, streak)

# Bottom dark gradient for text readability
bottom = Image.new("RGBA", (W, H), (0, 0, 0, 0))
bdraw = ImageDraw.Draw(bottom)
for y in range(H - 280, H):
    alpha = int(220 * ((y - (H - 280)) / 280))
    bdraw.line([(0, y), (W, y)], fill=(0, 0, 0, alpha))
img = Image.alpha_composite(img, bottom)

# Convert to RGB for final drawing
img = img.convert("RGB")
draw = ImageDraw.Draw(img)

# Font
font_paths = [
    "/System/Library/Fonts/Helvetica.ttc",
    "/System/Library/Fonts/HelveticaNeue.ttc",
    "/Library/Fonts/Arial Bold.ttf",
]
title_font = sub_font = tag_font = None
for fp in font_paths:
    if os.path.exists(fp):
        try:
            title_font = ImageFont.truetype(fp, 52)
            sub_font = ImageFont.truetype(fp, 26)
            tag_font = ImageFont.truetype(fp, 20)
            break
        except Exception:
            continue
if not title_font:
    title_font = ImageFont.load_default()
    sub_font = title_font
    tag_font = title_font

# Netflix red accent bar at top
draw.rectangle([0, 0, W, 4], fill=(229, 9, 20))

# Badges
draw.rounded_rectangle([40, 25, 155, 58], radius=4, fill=(229, 9, 20))
draw.text((52, 28), "NETFLIX", fill="white", font=tag_font)

draw.rounded_rectangle([170, 25, 345, 58], radius=4, fill=(147, 51, 234))
draw.text((182, 28), "DOCUMENTARY", fill="white", font=tag_font)

draw.rounded_rectangle([360, 25, 535, 58], radius=4, fill=(40, 15, 60))
draw.text((372, 28), "MARCH 27, 2026", fill=(192, 132, 252), font=tag_font)

# Seven purple dots representing 7 members
y_dots = 350
for i in range(7):
    cx = 60 + i * 28
    draw.ellipse([cx - 5, y_dots - 5, cx + 5, y_dots + 5], fill=(147, 51, 234))

# Main title
y_title = 370
lines = ["BTS: THE RETURN", "Netflix Documentary Guide"]
for i, line in enumerate(lines):
    y = y_title + i * 60
    draw.text((62, y + 2), line, fill=(0, 0, 0), font=title_font)
    draw.text((60, y), line, fill="white", font=title_font)

# Decorative line
draw.line([(60, y_title + 130), (650, y_title + 130)], fill=(147, 51, 234), width=2)

# Subtitle
draw.text(
    (60, y_title + 142),
    "Behind the Scenes of the Biggest Comeback in K-Pop History",
    fill=(192, 132, 252),
    font=sub_font,
)

out = "/Users/choijooyong/wordpress/featured_bts_return.png"
img.save(out, quality=95)
print(f"Saved: {out}")
