#!/usr/bin/env python3
"""Generate 5 featured images for March 3 articles."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 630
FONT = "/System/Library/Fonts/HelveticaNeue.ttc"
BASE = os.path.dirname(os.path.abspath(__file__))

def font(size, index=0):
    return ImageFont.truetype(FONT, size, index=index)

def gradient(draw, w, h, top, bot):
    for y in range(h):
        r = int(top[0] + (bot[0]-top[0]) * y/h)
        g = int(top[1] + (bot[1]-top[1]) * y/h)
        b = int(top[2] + (bot[2]-top[2]) * y/h)
        draw.line([(0, y), (w, y)], fill=(r, g, b))

def shadow(draw, xy, text, fnt, fill):
    x, y = xy
    draw.text((x+2, y+2), text, font=fnt, fill=(0,0,0))
    draw.text(xy, text, font=fnt, fill=fill)

def wrap(text, fnt, max_w):
    words = text.split()
    lines, line = [], ""
    for w in words:
        test = f"{line} {w}".strip()
        if fnt.getbbox(test)[2] > max_w and line:
            lines.append(line); line = w
        else:
            line = test
    if line: lines.append(line)
    return lines

def badge(draw, xy, text, bg):
    x, y = xy
    f = font(18, 1)
    tw = f.getbbox(text)[2] + 24
    draw.rounded_rectangle([(x, y), (x+tw, y+32)], radius=5, fill=bg)
    draw.text((x+12, y+4), text, font=f, fill=(255,255,255))

def stat_bar(draw, items, y_pos):
    draw.rectangle([(0, y_pos), (W, H)], fill=(10,5,25))
    px = 40
    spacing = (W - 80) // len(items)
    for text, color in items:
        draw.text((px, y_pos+15), text, font=font(22, 1), fill=color)
        px += spacing

# ── 1. BTS Arirang ──
img = Image.new("RGB", (W, H))
d = ImageDraw.Draw(img)
gradient(d, W, H, (26,10,46), (74,31,122))

# Decorative music note blocks
for i, (x, y, c) in enumerate([
    (700,120,(178,102,255)), (820,160,(138,43,226)), (940,100,(200,150,255)),
    (760,280,(148,103,189)), (880,240,(186,85,211)), (1000,300,(153,50,204)),
    (700,380,(128,0,128)), (850,350,(180,120,220)), (980,420,(160,32,240))]):
    d.rounded_rectangle([(x,y),(x+70,y+70)], radius=10, fill=c)
    nf = font(28)
    d.text((x+22, y+18), "♪" if i%2==0 else "♫", font=nf, fill=(255,255,255,180))

# Top banner
d.rectangle([(0,0),(W,50)], fill=(138,43,226))
shadow(d, (30,9), "K-POP COMEBACK", font(26,1), (255,255,255))
d.text((W-220,12), "MARCH 2026", font=font(22), fill=(220,200,255))

badge(d, (30,70), "EXCLUSIVE GUIDE", (178,102,255))

tf = font(46, 1)
for i, line in enumerate(wrap("BTS Arirang: The Comeback That Will Break Every Record", tf, 620)):
    shadow(d, (35, 120+i*58), line, tf, (255,255,255))

sf = font(22)
for i, line in enumerate(wrap("Album, World Tour, Netflix Live Concert — Everything You Need to Know", sf, 580)):
    d.text((35, 310+i*30), line, font=sf, fill=(220,200,255))

stat_bar(d, [("14 TRACKS",(178,102,255)), ("82 DATES",(255,215,0)),
             ("34 CITIES",(0,206,209)), ("190+ COUNTRIES",(255,105,180))], H-70)
img.save(os.path.join(BASE, "featured_bts_arirang.png"), quality=95)
print("featured_bts_arirang.png")

# ── 2. Boyfriend on Demand ──
img = Image.new("RGB", (W, H))
d = ImageDraw.Draw(img)
gradient(d, W, H, (180,50,100), (255,120,90))

# Heart decorations
for x, y, s in [(720,100,60),(850,180,50),(980,120,45),(760,300,55),(900,350,40),(1050,280,50)]:
    d.rounded_rectangle([(x,y),(x+s,y+s)], radius=s//4, fill=(255,255,255,40))
    hf = font(s//2)
    d.text((x+s//4, y+s//6), "♥", font=hf, fill=(255,200,220))

d.rectangle([(0,0),(W,50)], fill=(220,20,60))
shadow(d, (30,9), "K-DRAMA PREVIEW", font(26,1), (255,255,255))
d.text((W-200,12), "NETFLIX", font=font(24,1), fill=(255,200,200))

badge(d, (30,70), "PREMIERES MAR 6", (229,57,53))

tf = font(44, 1)
for i, line in enumerate(wrap("Boyfriend on Demand: Jisoo's Netflix Drama Everyone Is Talking About", tf, 620)):
    shadow(d, (35, 120+i*56), line, tf, (255,255,255))

sf = font(22)
for i, line in enumerate(wrap("Blackpink's Jisoo x Seo In-guk in the most anticipated K-Drama of Spring 2026", sf, 580)):
    d.text((35, 340+i*30), line, font=sf, fill=(255,230,230))

stat_bar(d, [("JISOO",(255,105,180)), ("SEO IN-GUK",(255,215,0)),
             ("8 VIRTUAL BFs",(0,206,209)), ("NETFLIX MAR 6",(255,100,100))], H-70)
img.save(os.path.join(BASE, "featured_boyfriend_demand.png"), quality=95)
print("featured_boyfriend_demand.png")

# ── 3. K-Beauty 2026 ──
img = Image.new("RGB", (W, H))
d = ImageDraw.Draw(img)
gradient(d, W, H, (0,150,100), (240,248,245))

# Ingredient bubbles
ingredients = [("PDRN",700,130,(0,184,148)), ("EXOSOMES",850,170,(46,213,115)),
               ("PEPTIDES",980,110,(85,239,196)), ("STEM CELLS",720,290,(0,210,170)),
               ("RETINOL",880,330,(29,209,161)), ("NIACINAMIDE",1020,270,(0,184,148)),
               ("CICA",760,430,(46,213,115))]
for lbl, x, y, c in ingredients:
    d.ellipse([(x,y),(x+90,y+90)], fill=c)
    lf = font(12, 1)
    tw = lf.getbbox(lbl)[2]
    d.text((x+(90-tw)//2, y+35), lbl, font=lf, fill=(255,255,255))

d.rectangle([(0,0),(W,50)], fill=(0,150,100))
shadow(d, (30,9), "K-BEAUTY TRENDS", font(26,1), (255,255,255))
d.text((W-120,12), "2026", font=font(26,1), fill=(200,255,230))

badge(d, (30,70), "TOP 7 TRENDS", (0,184,148))

tf = font(44, 1)
title_color = (30,50,40) if True else (255,255,255)
for i, line in enumerate(wrap("The Science Behind K-Beauty's 2026 Skincare Revolution", tf, 620)):
    shadow(d, (35, 120+i*56), line, tf, (30,50,40))

sf = font(22)
for i, line in enumerate(wrap("PDRN, Exosomes, Medicube AGE-R — The trends rewriting global beauty standards", sf, 580)):
    d.text((35, 320+i*30), line, font=sf, fill=(20,80,60))

stat_bar(d, [("PDRN +340%",(0,230,150)), ("$12B MARKET",(255,215,0)),
             ("MEDICUBE #1",(0,206,209)), ("EXOSOMES 2.0",(200,255,200))], H-70)
img.save(os.path.join(BASE, "featured_kbeauty_2026.png"), quality=95)
print("featured_kbeauty_2026.png")

# ── 4. Iran War + Korea ──
img = Image.new("RGB", (W, H))
d = ImageDraw.Draw(img)
gradient(d, W, H, (139,0,0), (26,26,62))

# Impact grid blocks
impacts = [("OIL",(200,30,30)), ("WON",(220,140,0)), ("KOSPI",(30,120,200)),
           ("GAS",(200,60,60)), ("TRAVEL",(180,60,120)), ("TRADE",(60,180,180))]
for i, (lbl, c) in enumerate(impacts):
    col, row = i%3, i//3
    x1 = 740 + col*140
    y1 = 180 + row*140
    d.rounded_rectangle([(x1,y1),(x1+120,y1+120)], radius=10, fill=c)
    lf = font(18, 1)
    tw = lf.getbbox(lbl)[2]
    d.text((x1+(120-tw)//2, y1+80), lbl, font=lf, fill=(255,255,255))

d.rectangle([(0,0),(W,50)], fill=(180,20,50))
shadow(d, (30,9), "SPECIAL REPORT", font(26,1), (255,255,255))
d.text((W-220,12), "MARCH 3, 2026", font=font(22), fill=(255,200,200))

badge(d, (30,70), "SOUTH KOREA", (180,20,50))

tf = font(42, 1)
for i, line in enumerate(wrap("How the Iran War Is Hitting South Korea's Economy Right Now", tf, 660)):
    shadow(d, (35, 120+i*54), line, tf, (255,255,255))

sf = font(22)
for i, line in enumerate(wrap("Oil dependency, currency shock, and rising prices — a Korean perspective", sf, 620)):
    d.text((35, 340+i*30), line, font=sf, fill=(255,180,180))

stat_bar(d, [("OIL +8%",(220,140,0)), ("70% M.EAST",(30,120,200)),
             ("$79 BRENT",(220,180,0)), ("HORMUZ DOWN",(200,30,30))], H-70)
img.save(os.path.join(BASE, "featured_iran_korea.png"), quality=95)
print("featured_iran_korea.png")

# ── 5. Korean Phrases BTS ──
img = Image.new("RGB", (W, H))
d = ImageDraw.Draw(img)
gradient(d, W, H, (9,132,227), (108,92,231))

# Korean character blocks
chars = [("방탄",700,120,(99,110,255)), ("소년단",840,160,(120,111,230)),
         ("화이팅",960,110,(130,100,240)), ("사랑해",720,280,(100,120,255)),
         ("대박",870,320,(110,90,230)), ("응원",1000,260,(125,105,245)),
         ("아미",760,420,(95,115,250))]
for txt, x, y, c in chars:
    d.rounded_rectangle([(x,y),(x+100,y+80)], radius=12, fill=c)
    try:
        kf = ImageFont.truetype("/System/Library/Fonts/AppleSDGothicNeo.ttc", 24, index=0)
    except:
        kf = font(20)
    tw = kf.getbbox(txt)[2]
    d.text((x+(100-tw)//2, y+25), txt, font=kf, fill=(255,255,255))

d.rectangle([(0,0),(W,50)], fill=(9,132,227))
shadow(d, (30,9), "LANGUAGE GUIDE", font(26,1), (255,255,255))
d.text((W-240,12), "BTS WORLD TOUR", font=font(22), fill=(200,220,255))

badge(d, (30,70), "25 PHRASES", (108,92,231))

tf = font(44, 1)
for i, line in enumerate(wrap("Essential Korean Phrases Every BTS Fan Needs for the World Tour", tf, 620)):
    shadow(d, (35, 120+i*56), line, tf, (255,255,255))

sf = font(22)
for i, line in enumerate(wrap("Fan chants, concert survival expressions, and ARMY vocabulary guide", sf, 580)):
    d.text((35, 320+i*30), line, font=sf, fill=(200,210,255))

stat_bar(d, [("25 PHRASES",(100,180,255)), ("FAN CHANTS",(255,215,0)),
             ("PRONUNCIATION",(0,206,209)), ("ARMY GUIDE",(255,105,180))], H-70)
img.save(os.path.join(BASE, "featured_korean_bts.png"), quality=95)
print("featured_korean_bts.png")
