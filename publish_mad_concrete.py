#!/usr/bin/env python3
"""Publish Mad Concrete Dreams K-Drama review article to rhythmicaleskimo.com"""

import requests, re, json, sys, os
from PIL import Image, ImageDraw, ImageFont

# ─── 1. Generate Featured Image ───────────────────────────────────────────────
print("=== Generating featured image ===")
IMG_PATH = "/Users/choijooyong/wordpress/featured_mad_concrete.png"
W, H = 1200, 630

img = Image.new("RGB", (W, H), "#0a0a1a")
draw = ImageDraw.Draw(img)

# Dark thriller gradient - dark blue to black
for y in range(H):
    r = int(10 + 15 * (1 - y / H))
    g = int(10 + 25 * (1 - y / H))
    b = int(26 + 50 * (1 - y / H))
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# Concrete texture effect - scattered gray rectangles
import random
random.seed(42)
for _ in range(80):
    x1 = random.randint(0, W)
    y1 = random.randint(0, H)
    x2 = x1 + random.randint(20, 120)
    y2 = y1 + random.randint(5, 30)
    alpha = random.randint(8, 25)
    draw.rectangle([x1, y1, x2, y2], fill=(alpha, alpha, alpha + 10))

# Red accent line
draw.rectangle([50, 140, W - 50, 145], fill="#c0392b")
draw.rectangle([50, 485, W - 50, 490], fill="#c0392b")

# Try system fonts
font_paths = [
    "/System/Library/Fonts/Helvetica.ttc",
    "/System/Library/Fonts/HelveticaNeue.ttc",
    "/Library/Fonts/Arial.ttf",
    "/System/Library/Fonts/SFNSDisplay.ttf",
]
font_large = None
for fp in font_paths:
    if os.path.exists(fp):
        try:
            font_large = ImageFont.truetype(fp, 52)
            font_med = ImageFont.truetype(fp, 30)
            font_small = ImageFont.truetype(fp, 22)
            break
        except:
            continue
if font_large is None:
    font_large = ImageFont.load_default()
    font_med = font_large
    font_small = font_large

# Title text
title_line1 = "MAD CONCRETE DREAMS"
title_line2 = "미친 콘크리트"
subtitle = "K-Drama Review 2026"
tagline = "Ha Jung-woo · Im Soo-jung · tvN"

# Center text helper
def center_text(draw, text, y, font, fill):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (W - tw) // 2
    draw.text((x, y), text, font=font, fill=fill)

# Draw shadow + text
def draw_text_shadow(draw, text, y, font, fill, shadow_fill="#000000"):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (W - tw) // 2
    draw.text((x + 2, y + 2), text, font=font, fill=shadow_fill)
    draw.text((x, y), text, font=font, fill=fill)

draw_text_shadow(draw, title_line1, 180, font_large, "#e8e8e8")
draw_text_shadow(draw, title_line2, 250, font_med, "#c0392b")
draw_text_shadow(draw, subtitle, 320, font_med, "#b0b0b0")
draw_text_shadow(draw, tagline, 390, font_small, "#808080")

# Site branding
center_text(draw, "rhythmicaleskimo.com", 530, font_small, "#505060")

img.save(IMG_PATH, "PNG", optimize=True)
print(f"Featured image saved: {IMG_PATH}")

# ─── 2. Article HTML ──────────────────────────────────────────────────────────
print("\n=== Preparing article ===")

ARTICLE_HTML = """
<p><strong>Mad Concrete Dreams (미친 콘크리트)</strong> is the K-drama that nobody expected — and the one everyone is talking about in March 2026. Starring film legend <strong>Ha Jung-woo</strong> in a rare television role alongside <strong>Im Soo-jung</strong>, this tvN crime thriller black comedy takes Korea's real estate obsession and turns it into a white-knuckle ride of debt, desperation, and a kidnapping scheme gone horribly wrong. If you are looking for a drama that combines biting social commentary with edge-of-your-seat suspense, Mad Concrete Dreams might be the most important K-drama of the year.</p>

<p>In this comprehensive guide, we break down everything you need to know: the full cast and characters, plot synopsis (spoiler-free), episode schedule, where to watch internationally, viewer ratings, and why this show is generating so much buzz. Whether you are a longtime Ha Jung-woo fan or a K-drama newcomer looking for your next obsession, read on.</p>

<h2>Mad Concrete Dreams: Overview and Production Details</h2>

<p>Mad Concrete Dreams premiered on <strong>March 14, 2026</strong> on tvN, airing every Saturday and Sunday at 21:10 KST. The series consists of <strong>12 episodes</strong> and is scheduled to wrap up on April 19, 2026. It occupies tvN's coveted weekend prime-time slot — the same slot that has launched hits like <em>Crash Landing on You</em> and <em>Vincenzo</em>.</p>

<h3>Creative Team</h3>

<p>The drama is <strong>directed by Yim Pil-sung</strong>, a filmmaker best known for his genre-bending work in Korean cinema. Yim's directorial credits include the horror anthology <em>Doomsday Book</em> and the Netflix original <em>Hansel and Gretel</em> (2007), which earned cult status for its visually striking, darkly whimsical style. His transition to the small screen brings a distinctly cinematic quality to Mad Concrete Dreams — viewers have noted the film-grade cinematography, deliberate pacing, and atmospheric tension that set it apart from typical TV productions.</p>

<p>The screenplay comes from <strong>Oh Han-ki</strong>, a critically acclaimed novelist who won the prestigious 7th Young Writers' Award. Mad Concrete Dreams marks Oh's debut as a television screenwriter, and his literary background is evident in the sharp dialogue, layered character motivations, and the story's unflinching examination of class anxiety in modern Korea. The combination of a literary novelist and a cinematic director gives the show a texture rarely found in weekly dramas.</p>

<p>Production is handled by <strong>Studio Dragon</strong> — the powerhouse behind <em>Extraordinary Attorney Woo</em>, <em>My Love from the Star</em>, and dozens of other global hits — as a co-production between <strong>Mindmark</strong> and <strong>Studio 329</strong>. With this pedigree, it is no surprise that the production values are exceptional, from the meticulously designed building interiors to the claustrophobic basement sequences that have become the show's visual signature.</p>

<h2>Complete Cast and Characters Guide</h2>

<p>One of Mad Concrete Dreams' biggest draws is its ensemble cast, headlined by two of Korea's most respected actors making a rare joint appearance on television.</p>

<h3>Ha Jung-woo as Ki Su-jong (기수종)</h3>

<p>Ha Jung-woo is, simply put, one of the greatest Korean actors of his generation. With a filmography that includes <em>The Chaser</em> (2008), <em>The Yellow Sea</em> (2010), <em>The Terror Live</em> (2013), <em>Tunnel</em> (2016), <em>Along with the Gods</em> series, <em>Ashfall</em> (2019), and the Netflix hit <em>Narco-Saints</em> (2022) — for which he won the Grand Prize (Daesang) at the Korea Drama Awards — he is one of only four Korean actors whose starring films have accumulated over 100 million ticket sales.</p>

<p>In Mad Concrete Dreams, Ha plays <strong>Ki Su-jong</strong>, a middle-aged family man who has poured everything into purchasing a building. It was supposed to be the ultimate financial achievement — becoming a "building owner" (건물주, <em>geonmulju</em>) is one of Korea's most coveted status symbols. But the mountain of debt that comes with it has turned his dream into a nightmare. When the building faces auction, Su-jong finds himself drawn into a scheme he never imagined.</p>

<p>What makes Ha's performance remarkable is how he balances the comedic absurdity of Su-jong's situation with genuine pathos. This is a man drowning, and Ha makes you feel every gasping breath. Fans have called it one of his most nuanced performances, noting that the intimacy of television allows him to work in micro-expressions and quiet desperation in ways his blockbuster film roles rarely permitted.</p>

<h3>Im Soo-jung as Kim Sun (김선)</h3>

<p>Im Soo-jung (<em>I'm Sorry, I Love You</em>, <em>A Tale of Two Sisters</em>, <em>All About My Wife</em>, <em>Chicago Typewriter</em>) brings gravitas and steel to the role of <strong>Kim Sun</strong>, Su-jong's wife. A former nurse who quit her career to care for their daughter Da-rae — who has a hearing impairment — Kim Sun is a woman who has sacrificed her professional identity for her family, channeling all her energy into securing Da-rae's future, including plans to send her abroad for education.</p>

<p>Kim Sun is no passive spouse waiting at home. When the crisis hits, she reveals a sharp, calculating intelligence that surprises everyone — including her husband. Im Soo-jung plays her with a controlled intensity that simmers beneath a composed exterior, and the moments when that composure cracks are some of the drama's most powerful scenes.</p>

<h3>Kim Jun-han as Min Hwal-seong (민활성)</h3>

<p>Kim Jun-han, who gained widespread recognition as the morally ambiguous Soo-hyun in <em>The World of the Married</em>, plays <strong>Min Hwal-seong</strong>, Su-jong's close friend and the catalyst for the drama's central crime. Hwal-seong married into a wealthy family — his wife Jeon Yi-gyeong (played by Krystal Jung) is the only daughter of a privileged household. But repeated failures in investments and business ventures have made him virtually invisible within his own home, dependent on in-laws who barely acknowledge him.</p>

<p>It is Hwal-seong who proposes the desperate plan: a <strong>fake kidnapping</strong> staged in the building's basement, designed to extract ransom money that will save Su-jong from foreclosure. Kim Jun-han imbues the character with a dangerous charm — Hwal-seong's "gift of gab" and persuasive charisma make it easy to see how he convinces Su-jong to go along with something so reckless, and equally easy to sense the volatile desperation beneath the smooth exterior.</p>

<h3>Krystal Jung (Jung Soo-jung) as Jeon Yi-gyeong (전이경)</h3>

<p>Former f(x) member and actress <strong>Krystal Jung</strong> (<em>Search: WWW</em>, <em>Crazy Love</em>, <em>Police University</em>) plays <strong>Jeon Yi-gyeong</strong>, the privileged wife of Min Hwal-seong. Yi-gyeong grew up with every material advantage, but carries a deep sense of emptiness. On the surface, she appears bright and flawless — the kind of woman who has everything figured out. Underneath, she is searching for meaning and connection in a life that feels increasingly hollow.</p>

<p>Her relationship with Hwal-seong is one of the drama's most fascinating dynamics: two people trapped in a marriage built on financial convenience rather than genuine connection, each quietly resenting the other while maintaining a perfect facade. Krystal delivers a performance that is both icy and vulnerable, marking her most mature acting work to date.</p>

<h3>Shim Eun-kyung as Kim Yo-na (김요나)</h3>

<p>Shim Eun-kyung (<em>Miss Granny</em>, <em>Fabricated City</em>) plays <strong>Kim Yo-na</strong>, a mysterious woman associated with "Real Capital" who was adopted overseas as a child. Yo-na is the drama's wildcard — her motivations are unclear, her loyalties shift, and her connection to the main plot unfolds in ways that consistently subvert expectations. Shim brings an unsettling energy to the role, making Yo-na one of the most talked-about characters in the early episodes.</p>

<h3>Special Appearance: Kim Nam-gil</h3>

<p>Adding star power to an already stacked cast, <strong>Kim Nam-gil</strong> (<em>The Fiery Priest</em>, <em>Island</em>, <em>Song of the Bandits</em>) makes a special appearance in the drama. Kim is a real-life close friend of Ha Jung-woo, and their off-screen chemistry reportedly translates into compelling on-screen moments. Details of his role are being kept under wraps, but his involvement has amplified anticipation among viewers.</p>

<div style="overflow-x:auto;">
<table style="width:100%;border-collapse:collapse;margin:20px 0;">
<thead>
<tr style="background:#1a1a2e;color:#e0e0e0;">
<th style="padding:12px;border:1px solid #333;text-align:left;">Actor</th>
<th style="padding:12px;border:1px solid #333;text-align:left;">Character</th>
<th style="padding:12px;border:1px solid #333;text-align:left;">Role Description</th>
</tr>
</thead>
<tbody>
<tr style="background:#0f0f1f;color:#ccc;">
<td style="padding:10px;border:1px solid #333;">Ha Jung-woo</td>
<td style="padding:10px;border:1px solid #333;">Ki Su-jong</td>
<td style="padding:10px;border:1px solid #333;">Debt-ridden building owner, accidental criminal</td>
</tr>
<tr style="background:#141428;color:#ccc;">
<td style="padding:10px;border:1px solid #333;">Im Soo-jung</td>
<td style="padding:10px;border:1px solid #333;">Kim Sun</td>
<td style="padding:10px;border:1px solid #333;">Su-jong's wife, former nurse, fiercely protective mother</td>
</tr>
<tr style="background:#0f0f1f;color:#ccc;">
<td style="padding:10px;border:1px solid #333;">Kim Jun-han</td>
<td style="padding:10px;border:1px solid #333;">Min Hwal-seong</td>
<td style="padding:10px;border:1px solid #333;">Su-jong's friend, mastermind of the fake kidnapping plan</td>
</tr>
<tr style="background:#141428;color:#ccc;">
<td style="padding:10px;border:1px solid #333;">Krystal Jung</td>
<td style="padding:10px;border:1px solid #333;">Jeon Yi-gyeong</td>
<td style="padding:10px;border:1px solid #333;">Hwal-seong's privileged wife, outwardly perfect but inwardly empty</td>
</tr>
<tr style="background:#0f0f1f;color:#ccc;">
<td style="padding:10px;border:1px solid #333;">Shim Eun-kyung</td>
<td style="padding:10px;border:1px solid #333;">Kim Yo-na</td>
<td style="padding:10px;border:1px solid #333;">Mysterious woman from "Real Capital," overseas adoptee</td>
</tr>
<tr style="background:#141428;color:#ccc;">
<td style="padding:10px;border:1px solid #333;">Kim Nam-gil</td>
<td style="padding:10px;border:1px solid #333;">Special Appearance</td>
<td style="padding:10px;border:1px solid #333;">Undisclosed role (real-life friend of Ha Jung-woo)</td>
</tr>
</tbody>
</table>
</div>

<h2>Plot Synopsis: What Is Mad Concrete Dreams About? (Spoiler-Free)</h2>

<p>At its core, Mad Concrete Dreams is a story about <strong>the dark side of the Korean Dream</strong>. In South Korea, owning a building — particularly a multi-unit commercial or residential property — represents the ultimate financial achievement. The term <em>geonmulju</em> (건물주, building owner) carries almost mythical status in Korean society. It implies passive income, generational wealth, and a certain untouchable social standing.</p>

<p>But as Korea's real estate market has become increasingly speculative and debt-fueled, the dream has turned toxic for many. Mad Concrete Dreams dramatizes this reality through Ki Su-jong, a man who leveraged everything — savings, loans, his family's future — to buy a building. When the economy shifts and tenants leave, he is left with a concrete monument to his ambition and a mountain of debt that threatens to crush him.</p>

<h3>The Kidnapping Plan</h3>

<p>When the building faces auction, Su-jong's friend Min Hwal-seong presents what he frames as a victimless solution: stage a <strong>fake kidnapping in the building's basement</strong>. The plan is supposed to be clean — extract enough ransom money to stave off the creditors, then everyone walks away. But as any viewer of crime thrillers knows, nothing goes according to plan.</p>

<p>What begins as a desperate financial scheme spirals into something far more dangerous. The "fake" kidnapping takes on a life of its own, drawing in unexpected players, exposing long-buried secrets, and forcing every character to confront who they really are when pushed to the edge. The brilliance of the writing is how it escalates organically — each new complication feels inevitable in retrospect, even as it shocks in the moment.</p>

<h3>Social Commentary Wrapped in Thriller Packaging</h3>

<p>Director Yim Pil-sung and writer Oh Han-ki use the thriller framework to deliver a scathing critique of Korea's property-obsessed culture. The drama asks uncomfortable questions: What happens when an entire society measures worth by real estate ownership? What moral lines will ordinary people cross when financial ruin threatens their families? How does the pressure to achieve the "building owner" dream distort relationships, identity, and basic decency?</p>

<p>The Korea Times noted that the drama "satirizes Korea's debt-laden real estate obsession," while KPOP POST highlighted how it "reveals Korea's property obsession" through its characters' increasingly desperate choices. This is not a drama that lets anyone off the hook — the wealthy characters are as trapped as the indebted ones, just in different cages.</p>

<h2>Episode Guide and Schedule</h2>

<p>Mad Concrete Dreams consists of <strong>12 episodes</strong>, airing on tvN every Saturday and Sunday at 21:10 KST. The series premiered on March 14, 2026, and is scheduled to conclude on April 19, 2026.</p>

<div style="overflow-x:auto;">
<table style="width:100%;border-collapse:collapse;margin:20px 0;">
<thead>
<tr style="background:#1a1a2e;color:#e0e0e0;">
<th style="padding:12px;border:1px solid #333;text-align:center;">Episode</th>
<th style="padding:12px;border:1px solid #333;text-align:center;">Air Date</th>
<th style="padding:12px;border:1px solid #333;text-align:center;">Day</th>
</tr>
</thead>
<tbody>
<tr style="background:#0f0f1f;color:#ccc;"><td style="padding:10px;border:1px solid #333;text-align:center;">1</td><td style="padding:10px;border:1px solid #333;text-align:center;">March 14, 2026</td><td style="padding:10px;border:1px solid #333;text-align:center;">Saturday</td></tr>
<tr style="background:#141428;color:#ccc;"><td style="padding:10px;border:1px solid #333;text-align:center;">2</td><td style="padding:10px;border:1px solid #333;text-align:center;">March 15, 2026</td><td style="padding:10px;border:1px solid #333;text-align:center;">Sunday</td></tr>
<tr style="background:#0f0f1f;color:#ccc;"><td style="padding:10px;border:1px solid #333;text-align:center;">3</td><td style="padding:10px;border:1px solid #333;text-align:center;">March 21, 2026</td><td style="padding:10px;border:1px solid #333;text-align:center;">Saturday</td></tr>
<tr style="background:#141428;color:#ccc;"><td style="padding:10px;border:1px solid #333;text-align:center;">4</td><td style="padding:10px;border:1px solid #333;text-align:center;">March 22, 2026</td><td style="padding:10px;border:1px solid #333;text-align:center;">Sunday</td></tr>
<tr style="background:#0f0f1f;color:#ccc;"><td style="padding:10px;border:1px solid #333;text-align:center;">5</td><td style="padding:10px;border:1px solid #333;text-align:center;">March 28, 2026</td><td style="padding:10px;border:1px solid #333;text-align:center;">Saturday</td></tr>
<tr style="background:#141428;color:#ccc;"><td style="padding:10px;border:1px solid #333;text-align:center;">6</td><td style="padding:10px;border:1px solid #333;text-align:center;">March 29, 2026</td><td style="padding:10px;border:1px solid #333;text-align:center;">Sunday</td></tr>
<tr style="background:#0f0f1f;color:#ccc;"><td style="padding:10px;border:1px solid #333;text-align:center;">7</td><td style="padding:10px;border:1px solid #333;text-align:center;">April 4, 2026</td><td style="padding:10px;border:1px solid #333;text-align:center;">Saturday</td></tr>
<tr style="background:#141428;color:#ccc;"><td style="padding:10px;border:1px solid #333;text-align:center;">8</td><td style="padding:10px;border:1px solid #333;text-align:center;">April 5, 2026</td><td style="padding:10px;border:1px solid #333;text-align:center;">Sunday</td></tr>
<tr style="background:#0f0f1f;color:#ccc;"><td style="padding:10px;border:1px solid #333;text-align:center;">9</td><td style="padding:10px;border:1px solid #333;text-align:center;">April 11, 2026</td><td style="padding:10px;border:1px solid #333;text-align:center;">Saturday</td></tr>
<tr style="background:#141428;color:#ccc;"><td style="padding:10px;border:1px solid #333;text-align:center;">10</td><td style="padding:10px;border:1px solid #333;text-align:center;">April 12, 2026</td><td style="padding:10px;border:1px solid #333;text-align:center;">Sunday</td></tr>
<tr style="background:#0f0f1f;color:#ccc;"><td style="padding:10px;border:1px solid #333;text-align:center;">11</td><td style="padding:10px;border:1px solid #333;text-align:center;">April 18, 2026</td><td style="padding:10px;border:1px solid #333;text-align:center;">Saturday</td></tr>
<tr style="background:#141428;color:#ccc;"><td style="padding:10px;border:1px solid #333;text-align:center;">12</td><td style="padding:10px;border:1px solid #333;text-align:center;">April 19, 2026</td><td style="padding:10px;border:1px solid #333;text-align:center;">Sunday</td></tr>
</tbody>
</table>
</div>

<h3>Premiere Ratings</h3>

<p>The first episode of Mad Concrete Dreams debuted to a <strong>nationwide average rating of 4.1%</strong> according to Nielsen Korea. For context, this is a strong opening for a tvN weekend drama — outperforming several other March 2026 premieres, including <em>Undercover Miss Hong</em>, which opened at 3.5%. Given Ha Jung-woo's massive film fanbase discovering the show, ratings are expected to climb as word-of-mouth spreads.</p>

<h2>Where to Watch Mad Concrete Dreams</h2>

<p>Whether you are in Korea or watching from abroad, here are all the platforms where you can stream Mad Concrete Dreams:</p>

<div style="overflow-x:auto;">
<table style="width:100%;border-collapse:collapse;margin:20px 0;">
<thead>
<tr style="background:#1a1a2e;color:#e0e0e0;">
<th style="padding:12px;border:1px solid #333;text-align:left;">Platform</th>
<th style="padding:12px;border:1px solid #333;text-align:left;">Region</th>
<th style="padding:12px;border:1px solid #333;text-align:left;">Details</th>
</tr>
</thead>
<tbody>
<tr style="background:#0f0f1f;color:#ccc;">
<td style="padding:10px;border:1px solid #333;"><strong>tvN</strong></td>
<td style="padding:10px;border:1px solid #333;">South Korea</td>
<td style="padding:10px;border:1px solid #333;">Live broadcast, Sat-Sun 21:10 KST</td>
</tr>
<tr style="background:#141428;color:#ccc;">
<td style="padding:10px;border:1px solid #333;"><strong>TVING</strong></td>
<td style="padding:10px;border:1px solid #333;">South Korea</td>
<td style="padding:10px;border:1px solid #333;">On-demand streaming after broadcast</td>
</tr>
<tr style="background:#0f0f1f;color:#ccc;">
<td style="padding:10px;border:1px solid #333;"><strong>Rakuten Viki</strong></td>
<td style="padding:10px;border:1px solid #333;">International</td>
<td style="padding:10px;border:1px solid #333;">English subtitles, free with ads or Viki Pass</td>
</tr>
<tr style="background:#141428;color:#ccc;">
<td style="padding:10px;border:1px solid #333;"><strong>HBO Max</strong></td>
<td style="padding:10px;border:1px solid #333;">Select international markets</td>
<td style="padding:10px;border:1px solid #333;">Subscription required</td>
</tr>
</tbody>
</table>
</div>

<p><strong>Note:</strong> Mad Concrete Dreams is <strong>not available on Netflix</strong> as of March 2026. If you are primarily a Netflix viewer, you might enjoy <a href="/boyfriend-on-demand-jisoos-netflix-k-drama-complete-guide-cast-review-cameos-everything-you-need-to-know/">Boyfriend on Demand</a>, which is currently streaming on Netflix and is one of the platform's biggest K-drama hits of March 2026.</p>

<p>For international viewers, <strong>Rakuten Viki</strong> is likely the most accessible option. Episodes are typically available with English subtitles within hours of the Korean broadcast. Viki also offers a free tier with ads, making it the most budget-friendly way to keep up with the show.</p>

<h2>Why Mad Concrete Dreams Is the Year's Most Intense K-Drama Thriller</h2>

<p>March 2026 has been an extraordinary month for K-dramas, with major premieres like <a href="/sirens-kiss-complete-guide-cast-plot-episodes-where-to-watch-2026/">Siren's Kiss</a> and <a href="/phantom-lawyer-%ec%9c%a0%eb%a0%b9-%eb%b3%80%ed%98%b8%ec%82%ac-complete-guide-review-2026/">Phantom Lawyer</a> competing for attention. But Mad Concrete Dreams stands apart for several reasons.</p>

<h3>Ha Jung-woo's Small Screen Return</h3>

<p>Ha Jung-woo very rarely does television. While his 2022 performance in <em>Narco-Saints</em> proved he could dominate the small screen, he remains primarily a film actor. His decision to take on a 12-episode tvN drama signals that the script was something truly special. For K-drama fans, watching one of Korea's top five box-office actors commit to a weekly series is an event in itself.</p>

<h3>A Story That Hits Home</h3>

<p>Korea's real estate market is not just an economic topic — it is an emotional one. Property prices, loans, jeonse (deposit-based rental), and the dream of building ownership dominate dinner table conversations across the country. Mad Concrete Dreams takes this universal anxiety and dramatizes it to its extreme conclusion. Korean viewers see their own fears reflected in Su-jong's desperation, and international viewers gain a visceral understanding of one of Korean society's most defining pressures.</p>

<h3>Genre-Blending Excellence</h3>

<p>The show's classification as a "crime thriller black comedy" only hints at its tonal range. In a single episode, you might find yourself laughing at the absurdity of the characters' predicament, gripping your seat during a tense standoff, and then moved to tears by a quiet family moment. Director Yim Pil-sung manages these tonal shifts with remarkable control — the comedy never undermines the suspense, and the suspense never flattens the emotional depth.</p>

<h3>Comparisons to Other Great K-Drama Thrillers</h3>

<p>Early reviews have drawn comparisons to several beloved K-drama thrillers:</p>
<ul>
<li><strong>Vincenzo</strong> — for its blend of dark comedy and crime, though Mad Concrete Dreams is grittier and more grounded</li>
<li><strong>My Name</strong> — for its unflinching intensity, though the social commentary here cuts deeper</li>
<li><strong>The World of the Married</strong> — for its examination of surface-level perfection hiding inner chaos (Kim Jun-han appears in both)</li>
<li><strong>Parasite (film)</strong> — the comparison most frequently made, as both explore class anxiety through genre storytelling, with confined spaces amplifying tension</li>
</ul>

<p>If you enjoyed the suspense in <a href="/5-must-watch-k-dramas-before-boyfriend-on-demand-premieres-on-netflix/">our list of must-watch K-drama thrillers</a>, Mad Concrete Dreams deserves a permanent spot on that list.</p>

<h2>Understanding the Cultural Context: Korea's Building Owner Dream</h2>

<p>To fully appreciate Mad Concrete Dreams, it helps to understand the cultural weight of building ownership in Korea. The term <strong>건물주 (geonmulju)</strong> — literally "building owner" — carries connotations that go far beyond simple real estate investment.</p>

<p>In Korean culture, becoming a geonmulju represents the pinnacle of financial success. It means passive rental income, freedom from the paycheck-to-paycheck grind, and a level of social prestige that other forms of wealth do not quite match. Surveys consistently show that a significant percentage of young Koreans list "building owner" as their ideal future profession — not doctor, not CEO, but building owner.</p>

<p>The flip side, which Mad Concrete Dreams dramatizes so effectively, is the massive debt that often accompanies building purchases. Many aspiring geonmulju take on leveraged loans far beyond their income, betting that property values will continue to rise. When the market cools or tenants leave, the dream collapses — and in a culture where financial failure carries intense shame, the fall can be devastating.</p>

<p>Su-jong's journey in the drama is a heightened but recognizable version of stories that play out across Korea. This cultural specificity is part of what makes the drama so powerful — it is not just a generic thriller but a deeply Korean story about a deeply Korean anxiety.</p>

<h2>You Might Also Enjoy</h2>

<p>If Mad Concrete Dreams has you craving more K-drama content, check out these guides on our site:</p>

<ul>
<li><a href="/when-life-gives-you-tangerines-cast-guide-iu-park-bo-gum-the-real-married-couple-2025/">When Life Gives You Tangerines Cast Guide</a> — IU and Park Bo-gum's emotional Jeju Island romance that dominated late 2025</li>
<li><a href="/top-10-k-drama-cafes-in-seoul-you-can-actually-visit-in-2026/">Top 10 K-Drama Cafes in Seoul You Can Actually Visit in 2026</a> — plan your Seoul trip around iconic filming locations</li>
<li><a href="/sirens-kiss-complete-guide-cast-plot-episodes-where-to-watch-2026/">Siren's Kiss Complete Guide</a> — another March 2026 premiere that is turning heads</li>
</ul>

<h2>Frequently Asked Questions</h2>

<h3>How many episodes does Mad Concrete Dreams have?</h3>
<p>Mad Concrete Dreams has 12 episodes total. The series airs on tvN every Saturday and Sunday at 21:10 KST, from March 14 to April 19, 2026.</p>

<h3>Is Mad Concrete Dreams on Netflix?</h3>
<p>No, Mad Concrete Dreams is not available on Netflix. You can watch it on Rakuten Viki (international), HBO Max (select markets), TVING (South Korea), or live on tvN.</p>

<h3>Who is the lead actor in Mad Concrete Dreams?</h3>
<p>Ha Jung-woo stars as Ki Su-jong, the debt-ridden building owner at the center of the story. He is joined by Im Soo-jung, Kim Jun-han, Krystal Jung, and Shim Eun-kyung.</p>

<h3>What genre is Mad Concrete Dreams?</h3>
<p>Mad Concrete Dreams is classified as a crime thriller black comedy. It combines suspenseful crime elements with dark humor and sharp social commentary about Korea's real estate culture.</p>

<h3>Is Mad Concrete Dreams based on a true story?</h3>
<p>No, Mad Concrete Dreams is a fictional story written by novelist Oh Han-ki. However, it draws heavily on real-world anxieties about Korea's debt-fueled real estate market, making it feel deeply authentic and culturally resonant.</p>

<h3>Where can I watch Mad Concrete Dreams with English subtitles?</h3>
<p>Rakuten Viki offers Mad Concrete Dreams with English subtitles, typically available within hours of the Korean broadcast. It is free to watch with ads, or ad-free with a Viki Pass subscription.</p>

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "How many episodes does Mad Concrete Dreams have?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Mad Concrete Dreams has 12 episodes total. The series airs on tvN every Saturday and Sunday at 21:10 KST, from March 14 to April 19, 2026."
      }
    },
    {
      "@type": "Question",
      "name": "Is Mad Concrete Dreams on Netflix?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "No, Mad Concrete Dreams is not available on Netflix. You can watch it on Rakuten Viki (international), HBO Max (select markets), TVING (South Korea), or live on tvN."
      }
    },
    {
      "@type": "Question",
      "name": "Who is the lead actor in Mad Concrete Dreams?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Ha Jung-woo stars as Ki Su-jong, the debt-ridden building owner at the center of the story. He is joined by Im Soo-jung, Kim Jun-han, Krystal Jung, and Shim Eun-kyung."
      }
    },
    {
      "@type": "Question",
      "name": "What genre is Mad Concrete Dreams?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Mad Concrete Dreams is classified as a crime thriller black comedy. It combines suspenseful crime elements with dark humor and sharp social commentary about Korea's real estate culture."
      }
    },
    {
      "@type": "Question",
      "name": "Is Mad Concrete Dreams based on a true story?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "No, Mad Concrete Dreams is a fictional story written by novelist Oh Han-ki. However, it draws heavily on real-world anxieties about Korea's debt-fueled real estate market, making it feel deeply authentic and culturally resonant."
      }
    },
    {
      "@type": "Question",
      "name": "Where can I watch Mad Concrete Dreams with English subtitles?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Rakuten Viki offers Mad Concrete Dreams with English subtitles, typically available within hours of the Korean broadcast. It is free to watch with ads, or ad-free with a Viki Pass subscription."
      }
    }
  ]
}
</script>
"""

EXCERPT = "Mad Concrete Dreams (미친 콘크리트) is tvN's gripping crime thriller black comedy starring Ha Jung-woo and Im Soo-jung. Get the full cast guide, plot synopsis, episode schedule, where to watch, and why it's 2026's most intense K-drama."

TITLE = "Mad Concrete Dreams (미친 콘크리트) K-Drama Review 2026: Cast, Plot, Episodes & Why It's the Year's Most Intense Thriller"

TAGS = [
    "Mad Concrete Dreams", "미친 콘크리트", "Ha Jung-woo", "Im Soo-jung",
    "Kim Jun-han", "Krystal Jung", "Shim Eun-kyung", "Kim Nam-gil",
    "tvN drama 2026", "K-drama thriller", "Korean drama review",
    "where to watch Mad Concrete Dreams", "K-drama 2026", "crime thriller K-drama",
    "Korean real estate drama"
]

# ─── 3. WordPress Publishing ──────────────────────────────────────────────────
print("\n=== Connecting to WordPress ===")
SITE = "https://rhythmicaleskimo.com"
REST = f"{SITE}/wp-json/wp/v2"

s = requests.Session()
s.cookies.set("wordpress_test_cookie", "WP+Cookie+check")

login_resp = s.post(f"{SITE}/wp-login.php", data={
    "log": "cjy654377@gmail.com",
    "pwd": "Dkflekd1!!",
    "wp-submit": "Log In",
    "redirect_to": "/wp-admin/",
    "testcookie": "1"
}, allow_redirects=True)

if "dashboard" not in login_resp.url and "wp-admin" not in login_resp.url:
    print(f"WARNING: Login may have failed. URL: {login_resp.url}")

page = s.get(f"{SITE}/wp-admin/post-new.php").text
m = re.search(r'"nonce":"([a-f0-9]+)"', page)
if not m:
    print("ERROR: Could not extract nonce")
    sys.exit(1)

nonce = m.group(1)
h = {"X-WP-Nonce": nonce}
print(f"Nonce obtained: {nonce[:8]}...")

# ─── Create/find tags ─────────────────────────────────────────────────────────
print("\n=== Creating tags ===")
tag_ids = []
for tag_name in TAGS:
    # Try to find existing tag first
    resp = s.get(f"{REST}/tags", params={"search": tag_name, "per_page": 5}, headers=h)
    found = False
    if resp.status_code == 200:
        for t in resp.json():
            if t["name"].lower() == tag_name.lower():
                tag_ids.append(t["id"])
                found = True
                break
    if not found:
        resp = s.post(f"{REST}/tags", json={"name": tag_name}, headers=h)
        if resp.status_code == 201:
            tag_ids.append(resp.json()["id"])
            print(f"  Created tag: {tag_name}")
        elif resp.status_code == 200:
            tag_ids.append(resp.json()["id"])
        else:
            # Tag might already exist with different casing
            print(f"  Tag issue ({resp.status_code}): {tag_name} - {resp.text[:100]}")

print(f"Total tags: {len(tag_ids)}")

# ─── Upload featured image ────────────────────────────────────────────────────
print("\n=== Uploading featured image ===")
with open(IMG_PATH, "rb") as f:
    img_resp = s.post(
        f"{REST}/media",
        headers={**h},
        files={"file": ("featured_mad_concrete.png", f, "image/png")},
        data={
            "alt_text": "Mad Concrete Dreams (미친 콘크리트) K-Drama 2026 - Ha Jung-woo tvN thriller",
            "caption": "Mad Concrete Dreams (미친 콘크리트) - tvN's crime thriller black comedy starring Ha Jung-woo and Im Soo-jung"
        }
    )

if img_resp.status_code == 201:
    media_id = img_resp.json()["id"]
    print(f"Image uploaded, media ID: {media_id}")
else:
    print(f"Image upload failed: {img_resp.status_code} - {img_resp.text[:200]}")
    media_id = None

# ─── Create post ──────────────────────────────────────────────────────────────
print("\n=== Publishing post ===")
KDRAMA_CAT_ID = 82

post_data = {
    "title": TITLE,
    "content": ARTICLE_HTML,
    "excerpt": EXCERPT,
    "status": "publish",
    "categories": [KDRAMA_CAT_ID],
    "tags": tag_ids,
    "comment_status": "open",
}

if media_id:
    post_data["featured_media"] = media_id

resp = s.post(f"{REST}/posts", json=post_data, headers=h)

if resp.status_code == 201:
    post = resp.json()
    print(f"\nSUCCESS!")
    print(f"Post ID: {post['id']}")
    print(f"URL: {post['link']}")
    print(f"Status: {post['status']}")
else:
    print(f"FAILED: {resp.status_code}")
    print(resp.text[:500])
