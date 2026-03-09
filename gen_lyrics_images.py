#!/usr/bin/env python3
"""BTS 가사 분석 시리즈 대표이미지 재생성 — 한글 폰트 적용"""
from PIL import Image, ImageDraw, ImageFont
import os

BASE = os.path.dirname(os.path.abspath(__file__))
W, H = 1200, 630

# 한글 지원 폰트
FONT_BOLD = "C:/Windows/Fonts/malgunbd.ttf"
FONT_REG = "C:/Windows/Fonts/malgun.ttf"

SONGS = [
    {
        "file": "featured_spring_day.png",
        "title": "Spring Day",
        "korean": "봄날",
        "artist_kr": "방탄소년단",
        "quote_kr": "보고 싶다",
        "quote_en": "I miss you",
        "bg": [(25, 20, 60), (60, 40, 120)],  # deep purple
        "accent": (180, 160, 220),
    },
    {
        "file": "featured_black_swan.png",
        "title": "Black Swan",
        "korean": "블랙스완",
        "artist_kr": "방탄소년단",
        "quote_kr": "심장이 더 이상 뛰지 않는다면",
        "quote_en": "If my heart no longer beats",
        "bg": [(15, 20, 35), (40, 50, 80)],  # dark blue
        "accent": (140, 150, 190),
    },
    {
        "file": "featured_fake_love.png",
        "title": "Fake Love",
        "korean": "페이크 러브",
        "artist_kr": "방탄소년단",
        "quote_kr": "나를 지워줄래 나를 지워줄래",
        "quote_en": "I tried to erase myself",
        "bg": [(50, 15, 20), (100, 30, 40)],  # dark red
        "accent": (230, 130, 130),
    },
    {
        "file": "featured_bst.png",
        "title": "Blood Sweat & Tears",
        "korean": "피 땀 눈물",
        "artist_kr": "방탄소년단",
        "quote_kr": "내 피 땀 눈물, 내 마지막 춤을",
        "quote_en": "Take my blood, sweat, and tears",
        "bg": [(45, 15, 10), (90, 30, 20)],  # dark crimson
        "accent": (210, 180, 80),
    },
]


def make_gradient(w, h, c1, c2):
    img = Image.new("RGB", (w, h))
    for y in range(h):
        r = int(c1[0] + (c2[0] - c1[0]) * y / h)
        g = int(c1[1] + (c2[1] - c1[1]) * y / h)
        b = int(c1[2] + (c2[2] - c1[2]) * y / h)
        for x in range(w):
            img.putpixel((x, y), (r, g, b))
    return img


def draw_particles(draw, w, h, color, count=40):
    import random
    random.seed(42)
    for _ in range(count):
        x = random.randint(0, w)
        y = random.randint(0, h)
        r = random.randint(2, 8)
        alpha_color = (*color[:3], random.randint(30, 80))
        draw.ellipse([x - r, y - r, x + r, y + r], fill=color[:3])


def create_image(song):
    img = make_gradient(W, H, song["bg"][0], song["bg"][1])
    draw = ImageDraw.Draw(img)
    accent = song["accent"]

    # particles
    draw_particles(draw, W, H, accent)

    # fonts
    f_artist = ImageFont.truetype(FONT_BOLD, 28)
    f_title = ImageFont.truetype(FONT_BOLD, 64)
    f_korean = ImageFont.truetype(FONT_BOLD, 36)
    f_sub = ImageFont.truetype(FONT_REG, 28)
    f_quote = ImageFont.truetype(FONT_REG, 22)

    y = 80

    # BTS (방탄소년단)
    artist_text = f"BTS ({song['artist_kr']})"
    bbox = draw.textbbox((0, 0), artist_text, font=f_artist)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) / 2, y), artist_text, fill=accent, font=f_artist)
    y += 60

    # Song title (English)
    bbox = draw.textbbox((0, 0), song["title"], font=f_title)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) / 2, y), song["title"], fill="white", font=f_title)
    y += 90

    # Korean title
    bbox = draw.textbbox((0, 0), song["korean"], font=f_korean)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) / 2, y), song["korean"], fill=accent, font=f_korean)
    y += 60

    # Subtitle
    sub = "Lyrics Meaning & Korean Translation"
    bbox = draw.textbbox((0, 0), sub, font=f_sub)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) / 2, y), sub, fill="white", font=f_sub)
    y += 50

    # Divider
    draw.line([(W / 2 - 120, y), (W / 2 + 120, y)], fill=accent, width=2)
    y += 30

    # Quote
    quote = f'"{song["quote_kr"]}" — {song["quote_en"]}'
    bbox = draw.textbbox((0, 0), quote, font=f_quote)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) / 2, y), quote, fill=accent, font=f_quote)
    y += 50

    # Site name
    site = "Rhythmical Eskimo"
    bbox = draw.textbbox((0, 0), site, font=f_quote)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) / 2, H - 50), site, fill=(180, 180, 180), font=f_quote)

    path = os.path.join(BASE, song["file"])
    img.save(path, "PNG")
    print(f"  OK: {song['file']}")


if __name__ == "__main__":
    for song in SONGS:
        create_image(song)
    print("Done!")
