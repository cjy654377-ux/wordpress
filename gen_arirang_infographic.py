#!/usr/bin/env python3
"""Generate high-quality Han→Heung infographic for BTS ARIRANG article.
Timeline: Military enlistment → Separation → Discharge → Album → Concert → Tour
Visual: Vertical timeline with gradient from dark (han) to bright (heung)
"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 2400
BASE = os.path.dirname(os.path.abspath(__file__))
FONT = "/System/Library/Fonts/HelveticaNeue.ttc"

def font(size, index=0):
    return ImageFont.truetype(FONT, size, index=index)

def draw_gradient(draw, x1, y1, x2, y2, top_color, bot_color):
    for y in range(y1, y2):
        t = (y - y1) / (y2 - y1)
        r = int(top_color[0] + (bot_color[0] - top_color[0]) * t)
        g = int(top_color[1] + (bot_color[1] - top_color[1]) * t)
        b = int(top_color[2] + (bot_color[2] - top_color[2]) * t)
        draw.line([(x1, y), (x2, y)], fill=(r, g, b))

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

def rounded_rect(draw, xy, radius, fill):
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle(xy, radius=radius, fill=fill)

img = Image.new("RGB", (W, H))
d = ImageDraw.Draw(img)

# === BACKGROUND: Gradient from deep navy (han) to warm gold (heung) ===
draw_gradient(d, 0, 0, W, H, (12, 8, 30), (25, 15, 45))

# === HEADER ===
# Top accent bar
d.rectangle([(0, 0), (W, 6)], fill=(140, 80, 200))

# Title section
d.text((60, 40), "BTS ARIRANG", font=font(22, 1), fill=(140, 100, 200))
d.text((60, 75), "The Journey from", font=font(44, 1), fill=(255, 255, 255))

# Han in blue
han_text = "한 (Han)"
d.text((60, 130), han_text, font=font(52, 1), fill=(100, 150, 255))
han_w = font(52, 1).getbbox(han_text)[2]

d.text((60 + han_w + 20, 145), "to", font=font(36), fill=(180, 180, 200))

# Heung in gold
d.text((60 + han_w + 70, 130), "흥 (Heung)", font=font(52, 1), fill=(255, 200, 80))

d.text((60, 200), "2.5 Years of Separation → The Greatest Comeback in K-Pop History", font=font(22), fill=(160, 160, 180))

# Divider line
d.line([(60, 250), (W - 60, 250)], fill=(60, 40, 80), width=2)

# === TIMELINE ===
timeline_x = 160  # center line x position
start_y = 300
dot_radius = 14
line_color = (60, 40, 100)

# Timeline events
events = [
    {
        "date": "DEC 2022",
        "title": "Jin Enlists First",
        "desc": "The oldest member begins mandatory service. BTS promises: \"We'll be back.\"",
        "phase": "han",
        "color": (70, 100, 180),
        "dot_color": (80, 120, 200),
    },
    {
        "date": "APR — DEC 2023",
        "title": "All 7 Members Enter Service",
        "desc": "J-Hope (Apr), SUGA (Sep), RM, V (Dec 11), Jimin, Jungkook (Dec 12). The stage goes silent.",
        "phase": "han",
        "color": (60, 80, 160),
        "dot_color": (70, 100, 180),
    },
    {
        "date": "2023 — 2025",
        "title": "2.5 Years of Silence",
        "desc": "No group music. No concerts. ARMY waits. RM considers disbandment \"thousands of times.\"",
        "phase": "han_deep",
        "color": (50, 50, 130),
        "dot_color": (60, 60, 150),
    },
    {
        "date": "JUN 2024 — JUN 2025",
        "title": "Members Return One by One",
        "desc": "Jin (Jun '24) → J-Hope (Oct '24) → RM, V, Jimin, Jungkook, SUGA (Jun '25). The circle reforms.",
        "phase": "transition",
        "color": (100, 80, 160),
        "dot_color": (130, 100, 200),
    },
    {
        "date": "JAN 16, 2026",
        "title": "ARIRANG Album Announced",
        "desc": "Named after Korea's 600-year-old folk song. 4.06M pre-orders in 7 days — all-time record.",
        "phase": "heung_start",
        "color": (150, 100, 180),
        "dot_color": (180, 120, 220),
    },
    {
        "date": "MAR 20, 2026",
        "title": "Album Release + SWIM MV",
        "desc": "14 tracks. RM wrote on 13. Diplo, Tame Impala, JPEGMAFIA, Flume. \"The whole package.\"",
        "phase": "heung",
        "color": (200, 150, 80),
        "dot_color": (230, 180, 60),
    },
    {
        "date": "MAR 21, 2026",
        "title": "Gwanghwamun Live Concert",
        "desc": "Netflix global stream. In front of Gyeongbokgung Palace. Cultural homecoming, not just a show.",
        "phase": "heung",
        "color": (220, 170, 50),
        "dot_color": (255, 200, 60),
    },
    {
        "date": "APR 2026 — 2027",
        "title": "82-Show World Tour Begins",
        "desc": "34 cities, 23 countries. The biggest BTS tour ever. Han becomes heung — every night, in every city.",
        "phase": "heung_peak",
        "color": (240, 190, 40),
        "dot_color": (255, 210, 50),
    },
]

card_gap = 250
y = start_y

for i, ev in enumerate(events):
    # Timeline vertical line segment
    if i < len(events) - 1:
        # Gradient line between dots
        next_y = y + card_gap
        for ly in range(y + dot_radius, next_y - dot_radius):
            t = (ly - y) / card_gap
            c = ev["dot_color"]
            nc = events[i+1]["dot_color"]
            lr = int(c[0] + (nc[0] - c[0]) * t)
            lg = int(c[1] + (nc[1] - c[1]) * t)
            lb = int(c[2] + (nc[2] - c[2]) * t)
            d.line([(timeline_x, ly), (timeline_x, ly)], fill=(lr, lg, lb), width=4)

    # Dot on timeline
    d.ellipse(
        [(timeline_x - dot_radius, y - dot_radius),
         (timeline_x + dot_radius, y + dot_radius)],
        fill=ev["dot_color"], outline=(255, 255, 255), width=3
    )

    # Glow effect around dot
    for g in range(3):
        glow_r = dot_radius + 4 + g * 3
        glow_alpha = 80 - g * 25
        gc = ev["dot_color"]
        d.ellipse(
            [(timeline_x - glow_r, y - glow_r),
             (timeline_x + glow_r, y + glow_r)],
            outline=(*gc, glow_alpha), width=1
        )

    # Card (right side of timeline)
    card_x = timeline_x + 50
    card_y = y - 45
    card_w = W - card_x - 60
    card_h = 180

    # Card background with subtle gradient
    bg = ev["color"]
    card_bg = (bg[0]//4, bg[1]//4, bg[2]//4)
    rounded_rect(d, (card_x, card_y, card_x + card_w, card_y + card_h), 12, card_bg)

    # Left accent bar on card
    d.rounded_rectangle(
        (card_x, card_y, card_x + 5, card_y + card_h),
        radius=3, fill=ev["dot_color"]
    )

    # Date label
    d.text((card_x + 22, card_y + 14), ev["date"], font=font(16, 1), fill=ev["dot_color"])

    # Title
    d.text((card_x + 22, card_y + 40), ev["title"], font=font(28, 1), fill=(255, 255, 255))

    # Description (wrapped)
    desc_lines = wrap_text(ev["desc"], font(18), card_w - 50)
    dy = card_y + 78
    for line in desc_lines:
        d.text((card_x + 22, dy), line, font=font(18), fill=(190, 190, 210))
        dy += 26

    # Phase label on left side of timeline
    phase_labels = {
        "han": ("한 HAN", (80, 120, 200)),
        "han_deep": ("한 HAN", (60, 60, 150)),
        "transition": ("전환", (130, 100, 200)),
        "heung_start": ("흥 HEUNG", (180, 120, 220)),
        "heung": ("흥 HEUNG", (230, 180, 60)),
        "heung_peak": ("흥 HEUNG", (255, 210, 50)),
    }
    label, lcolor = phase_labels[ev["phase"]]
    lw = font(14, 1).getbbox(label)[2]
    d.text((timeline_x - 30 - lw, y - 8), label, font=font(14, 1), fill=lcolor)

    y += card_gap

# === BOTTOM SECTION: Album arc visualization ===
bottom_y = y + 30
d.line([(60, bottom_y), (W - 60, bottom_y)], fill=(60, 40, 80), width=2)

# Album emotional arc mini visualization
arc_y = bottom_y + 40
d.text((60, arc_y), "THE ALBUM ARC: 14 TRACKS, ONE JOURNEY", font=font(22, 1), fill=(180, 160, 220))

arc_y += 50
track_w = (W - 140) / 14

# Colors from han (blue) to heung (gold)
arc_colors = [
    (100, 140, 220),  # 1 Body to Body
    (90, 130, 210),   # 2 Hooligan
    (80, 110, 190),   # 3 Aliens
    (70, 90, 170),    # 4 FYA
    (80, 80, 160),    # 5 2.0
    (90, 70, 150),    # 6 No. 29
    (140, 100, 200),  # 7 SWIM ★ (center/pivot)
    (160, 120, 180),  # 8 Merry Go Round
    (150, 110, 160),  # 9 NORMAL
    (170, 130, 140),  # 10 Like Animals
    (200, 160, 100),  # 11 they don't know
    (210, 170, 80),   # 12 One More Night
    (220, 180, 60),   # 13 Please
    (250, 210, 50),   # 14 Into the Sun
]

# Bar heights representing emotional intensity
bar_heights = [120, 110, 100, 130, 95, 80, 150, 115, 85, 105, 125, 100, 90, 160]

track_names = ["Body\nto Body", "Hooligan", "Aliens", "FYA", "2.0", "No. 29",
               "SWIM\n★", "Merry Go\nRound", "NORMAL", "Like\nAnimals",
               "they don't\nknow", "One More\nNight", "Please", "Into the\nSun"]

bar_base = arc_y + 200

for i in range(14):
    x = 70 + i * track_w
    bh = bar_heights[i]
    color = arc_colors[i]

    # Bar
    d.rounded_rectangle(
        (int(x + 4), bar_base - bh, int(x + track_w - 4), bar_base),
        radius=6, fill=color
    )

    # Track number
    num_text = str(i + 1)
    nw = font(14, 1).getbbox(num_text)[2]
    d.text((int(x + track_w/2 - nw/2), bar_base - bh + 8), num_text, font=font(14, 1), fill=(255, 255, 255))

    # Track name below bar
    name_lines = track_names[i].split("\n")
    ny = bar_base + 8
    for nl in name_lines:
        nlw = font(11).getbbox(nl)[2]
        d.text((int(x + track_w/2 - nlw/2), ny), nl, font=font(11), fill=(160, 160, 180))
        ny += 15

# Arc labels
d.text((70, bar_base + 55), "← 한 (Han) — Separation, Struggle", font=font(16, 1), fill=(100, 140, 220))
rtext = "Reunion, Celebration — 흥 (Heung) →"
rtw = font(16, 1).getbbox(rtext)[2]
d.text((W - 70 - rtw, bar_base + 55), rtext, font=font(16, 1), fill=(250, 210, 50))

# Center pivot label
pivot_x = 70 + 6.5 * track_w
d.text((int(pivot_x - 20), bar_base - 170), "PIVOT", font=font(12, 1), fill=(160, 120, 220))

# === FOOTER ===
footer_y = bar_base + 100
d.line([(60, footer_y), (W - 60, footer_y)], fill=(60, 40, 80), width=1)

# Key stats row
stats = [
    ("600+", "Years of\nArirang"),
    ("2.5", "Years of\nSeparation"),
    ("4.06M", "Pre-orders\nin 7 Days"),
    ("14", "Tracks of\nHealing"),
    ("82", "Shows to\nCelebrate"),
]

stat_w = (W - 120) / len(stats)
for i, (num, label) in enumerate(stats):
    sx = 60 + i * stat_w
    nw = font(36, 1).getbbox(num)[2]
    # Determine color based on position (han to heung)
    t = i / (len(stats) - 1)
    sc = (
        int(100 + 155 * t),
        int(140 + 70 * t),
        int(220 - 170 * t),
    )
    d.text((int(sx + stat_w/2 - nw/2), footer_y + 20), num, font=font(36, 1), fill=sc)

    for j, ll in enumerate(label.split("\n")):
        llw = font(14).getbbox(ll)[2]
        d.text((int(sx + stat_w/2 - llw/2), footer_y + 65 + j * 18), ll, font=font(14), fill=(160, 160, 180))

# Site branding
brand_y = footer_y + 120
d.text((W//2 - 100, brand_y), "rhythmicaleskimo.com", font=font(16, 1), fill=(120, 100, 160))

# Trim height to actual content
final_h = brand_y + 50
img_cropped = img.crop((0, 0, W, final_h))
img_cropped.save(os.path.join(BASE, "infographic_arirang_timeline.png"), quality=95)
print(f"✅ infographic_arirang_timeline.png ({W}x{final_h})")
