#!/usr/bin/env python3
"""Generate featured images for March 3 batch 2 articles."""
from PIL import Image, ImageDraw, ImageFont
import os

BASE = os.path.dirname(os.path.abspath(__file__))
W, H = 1200, 630

def font(size):
    return ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", size)

def gradient(draw, c1, c2):
    for y in range(H):
        r = int(c1[0] + (c2[0]-c1[0]) * y/H)
        g = int(c1[1] + (c2[1]-c1[1]) * y/H)
        b = int(c1[2] + (c2[2]-c1[2]) * y/H)
        draw.line([(0,y),(W,y)], fill=(r,g,b))

def make_5dramas():
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    gradient(draw, (180, 50, 80), (40, 20, 60))
    # Film reel decorations
    for i in range(6):
        x = 100 + i * 200
        draw.rounded_rectangle([x, 50, x+160, 90], radius=8, fill=(255,255,255,80), outline=(255,200,200))
        draw.rounded_rectangle([x, 520, x+160, 560], radius=8, fill=(255,255,255,80), outline=(255,200,200))
    # Badge
    draw.rounded_rectangle([40, 120, 300, 170], radius=20, fill=(255, 80, 120))
    draw.text((60, 127), "K-DRAMA WATCHLIST", fill="white", font=font(24))
    # Title
    draw.text((40, 200), "5 Must-Watch K-Dramas", fill="white", font=font(52))
    draw.text((40, 270), "Before Boyfriend on Demand", fill=(255, 200, 210), font=font(44))
    # Subtitle
    draw.text((40, 350), "Snowdrop | Are You Human Too? | Reply 1988", fill=(255,180,190), font=font(24))
    draw.text((40, 385), "My Love from the Star | W: Two Worlds", fill=(255,180,190), font=font(24))
    # Bottom bar
    draw.rectangle([0, 580, W, H], fill=(20, 10, 30))
    draw.text((40, 590), "RHYTHMICAL ESKIMO", fill=(255,100,140), font=font(22))
    draw.text((750, 590), "Netflix  |  March 6, 2026  |  Jisoo", fill=(200,180,190), font=font(20))
    img.save(os.path.join(BASE, "featured_5dramas_bod.png"))
    print("  Created: featured_5dramas_bod.png")

def make_bts_tour():
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    gradient(draw, (100, 30, 180), (20, 10, 60))
    # Globe/city dots
    import random
    random.seed(42)
    for _ in range(40):
        x, y = random.randint(50, 1150), random.randint(50, 570)
        s = random.randint(3, 8)
        draw.ellipse([x, y, x+s, y+s], fill=(200, 150, 255, 150))
    # Connection lines between cities
    cities = [(200,150),(400,200),(600,100),(800,250),(1000,180),(300,400),(700,350),(900,450)]
    for i in range(len(cities)-1):
        draw.line([cities[i], cities[i+1]], fill=(180, 120, 255), width=1)
    # Badge
    draw.rounded_rectangle([40, 100, 220, 150], radius=20, fill=(180, 80, 255))
    draw.text((60, 107), "WORLD TOUR", fill="white", font=font(24))
    # Title
    draw.text((40, 180), "BTS Arirang World Tour", fill="white", font=font(52))
    draw.text((40, 250), "2026 Complete Guide", fill=(220, 180, 255), font=font(48))
    # Stats
    draw.text((40, 340), "Every Date  |  Every City  |  Ticket Guide", fill=(200, 170, 240), font=font(26))
    # Big numbers
    draw.rounded_rectangle([40, 400, 280, 500], radius=15, fill=(120, 50, 200))
    draw.text((70, 410), "82", fill="white", font=font(52))
    draw.text((70, 465), "DATES", fill=(200,170,255), font=font(18))
    draw.rounded_rectangle([310, 400, 550, 500], radius=15, fill=(120, 50, 200))
    draw.text((340, 410), "34", fill="white", font=font(52))
    draw.text((340, 465), "CITIES", fill=(200,170,255), font=font(18))
    draw.rounded_rectangle([580, 400, 820, 500], radius=15, fill=(120, 50, 200))
    draw.text((610, 410), "7", fill="white", font=font(52))
    draw.text((680, 430), "months", fill=(200,170,255), font=font(22))
    # Bottom bar
    draw.rectangle([0, 580, W, H], fill=(10, 5, 30))
    draw.text((40, 590), "RHYTHMICAL ESKIMO", fill=(180,100,255), font=font(22))
    draw.text((800, 590), "April – October 2026  |  ARMY", fill=(180,150,220), font=font(20))
    img.save(os.path.join(BASE, "featured_bts_tour_guide.png"))
    print("  Created: featured_bts_tour_guide.png")

make_5dramas()
make_bts_tour()
print("Done!")
