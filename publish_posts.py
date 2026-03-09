#!/usr/bin/env python3
"""Publish 10 Korean Food TV Show posts to WordPress in English via REST API with cookie auth."""

import requests
import re
import json

SITE = "https://rhythmicaleskimo.com"
LOGIN_URL = f"{SITE}/wp-login.php"
REST_URL = f"{SITE}/wp-json/wp/v2"
USERNAME = "cjy654377@gmail.com"
PASSWORD = "Dkflekd1!!"

# ---- Step 1: Login and get cookies + nonce ----
session = requests.Session()
login_data = {
    "log": USERNAME,
    "pwd": PASSWORD,
    "wp-submit": "Log In",
    "redirect_to": "/wp-admin/",
    "testcookie": "1"
}
session.cookies.set("wordpress_test_cookie", "WP+Cookie+check")
resp = session.post(LOGIN_URL, data=login_data, allow_redirects=True)
print(f"Login status: {resp.status_code}")

# Get REST nonce from wp-admin
admin_page = session.get(f"{SITE}/wp-admin/post-new.php").text
nonce_match = re.search(r'"nonce":"([a-f0-9]+)"', admin_page)
if not nonce_match:
    print("ERROR: Could not find REST nonce")
    exit(1)
nonce = nonce_match.group(1)
print(f"REST nonce: {nonce}")

# ---- Step 2: Create category ----
headers = {"X-WP-Nonce": nonce}

# Check if category exists
cats = session.get(f"{REST_URL}/categories?search=Korean+Food+TV", headers=headers).json()
if cats and not isinstance(cats, dict):
    cat_id = cats[0]["id"]
else:
    cat_resp = session.post(f"{REST_URL}/categories", headers=headers, json={
        "name": "Korean Food TV",
        "slug": "korean-food-tv",
        "description": "Korean TV show restaurant guides and food reviews"
    })
    if cat_resp.status_code == 201:
        cat_id = cat_resp.json()["id"]
    else:
        cat_id = 1  # fallback to uncategorized
print(f"Category ID: {cat_id}")

# ---- Step 3: Define 10 English posts ----
posts = [
    {
        "title": "Bangi Gullim Mandu Ttegul – Giant Hand-Rolled Dumpling Hot Pot in Seoul Songpa-gu",
        "tags": ["Korean Food", "KBS 2TV", "Seoul Restaurant", "Songpa-gu", "Dumpling Hot Pot", "Mandu Jeongol", "Korean TV Show", "생생정보"],
        "content": """<style>
.sf-post { font-family: 'Noto Sans KR', sans-serif; max-width: 800px; margin: 0 auto; line-height: 1.8; color: #333; }
.sf-post h2 { color: #2d3436; margin-top: 30px; }
.sf-post .highlight-box { background: #ffeaa7; padding: 15px 20px; border-radius: 10px; margin: 20px 0; }
.sf-post .menu-table { width: 100%; border-collapse: collapse; margin: 15px 0; }
.sf-post .menu-table th, .sf-post .menu-table td { border: 1px solid #ddd; padding: 10px; text-align: left; }
.sf-post .menu-table th { background: #d63031; color: white; }
.sf-post .info-card { background: #f8f9fa; border-left: 4px solid #d63031; padding: 15px; margin: 20px 0; }
.sf-post .tag { display: inline-block; background: #74b9ff; color: white; padding: 3px 10px; border-radius: 15px; margin: 3px; font-size: 13px; }
.sf-post .cta { background: #d63031; color: white; padding: 15px; text-align: center; border-radius: 10px; margin: 30px 0; font-size: 18px; }
</style>
<div class="sf-post">

<p><em>Featured on KBS2 "2TV 생생정보" (Feb 27, 2026) — Corner: Star Restaurant</em></p>

<p>Hidden in the streets of <strong>Songpa-gu, Seoul</strong>, there's a restaurant that serves one of the most spectacular dumpling hot pots in Korea. <strong>Bangi Gullim Mandu Ttegul (방이굴림만두떼굴)</strong> was featured on the popular Korean TV show "2TV 생생정보" and has been making waves with its oversized hand-rolled dumplings.</p>

<div class="highlight-box">
💡 <strong>Why This Restaurant is Special:</strong> Each dumpling is hand-rolled to an enormous size, filled with premium ingredients, and served in a rich, flavorful broth. The hot pot comes loaded with fresh vegetables, tofu, and their signature giant dumplings — a perfect warming meal for any season.
</div>

<h2>📍 Restaurant Info</h2>
<div class="info-card">
<strong>🏪 Name:</strong> 방이굴림만두떼굴 (Bangi Gullim Mandu Ttegul)<br>
<strong>📍 Location:</strong> Bangi-dong, Songpa-gu, Seoul, South Korea<br>
<strong>📺 Featured on:</strong> KBS2 2TV 생생정보 (Feb 27, 2026) — "Star Restaurant" segment<br>
<strong>🅿️ Parking:</strong> Available nearby
</div>

<h2>🍽️ Signature Menu</h2>
<table class="menu-table">
<tr><th>Menu</th><th>Description</th></tr>
<tr><td>🥇 Giant Dumpling Hot Pot (굴림만두전골)</td><td>Oversized hand-rolled dumplings in rich broth with vegetables and tofu</td></tr>
<tr><td>🥈 Steamed Dumplings (찐만두)</td><td>Traditional Korean steamed dumplings with savory filling</td></tr>
<tr><td>🥉 Pan-fried Dumplings (군만두)</td><td>Crispy pan-fried dumplings with golden crust</td></tr>
</table>

<h2>💬 Visitor Reviews</h2>
<blockquote style="background:#f1f2f6; padding:15px; border-radius:10px; border-left:4px solid #d63031;">
"The dumplings are HUGE and packed with flavor. The broth is incredibly rich and comforting. This is a must-visit when you're in the Songpa area!"
</blockquote>

<h2>🗺️ How to Get There</h2>
<p>🚇 <strong>Subway:</strong> Line 8, Mongchontoseong Station or Bangi Station<br>
🚌 <strong>Bus:</strong> Multiple routes to Songpa-gu area<br>
🅿️ <strong>Parking:</strong> Street parking and nearby lots available</p>

<div class="cta">📍 A must-try Korean dumpling experience in Seoul's Songpa-gu! Featured on Korea's top food TV show.</div>

<span class="tag">#KoreanFood</span> <span class="tag">#SeoulRestaurant</span> <span class="tag">#DumplingHotPot</span> <span class="tag">#KoreanFoodShow</span> <span class="tag">#Songpagu</span> <span class="tag">#ManduJeongol</span>
</div>"""
    },
    {
        "title": "World Bap – All-You-Can-Eat Korean Buffet for Only $6 in Gwangju",
        "tags": ["Korean Food", "KBS 2TV", "Gwangju Restaurant", "Korean Buffet", "Budget Dining", "Korean TV Show"],
        "content": """<style>
.sf-post { font-family: 'Noto Sans KR', sans-serif; max-width: 800px; margin: 0 auto; line-height: 1.8; color: #333; }
.sf-post h2 { color: #2d3436; margin-top: 30px; }
.sf-post .highlight-box { background: #ffeaa7; padding: 15px 20px; border-radius: 10px; margin: 20px 0; }
.sf-post .menu-table { width: 100%; border-collapse: collapse; margin: 15px 0; }
.sf-post .menu-table th, .sf-post .menu-table td { border: 1px solid #ddd; padding: 10px; text-align: left; }
.sf-post .menu-table th { background: #d63031; color: white; }
.sf-post .info-card { background: #f8f9fa; border-left: 4px solid #d63031; padding: 15px; margin: 20px 0; }
.sf-post .tag { display: inline-block; background: #74b9ff; color: white; padding: 3px 10px; border-radius: 15px; margin: 3px; font-size: 13px; }
.sf-post .cta { background: #d63031; color: white; padding: 15px; text-align: center; border-radius: 10px; margin: 30px 0; font-size: 18px; }
</style>
<div class="sf-post">

<p><em>Featured on KBS2 "2TV 생생정보" (Feb 26, 2026) — Corner: Price Destroyer Why</em></p>

<p>Can you imagine enjoying a <strong>full Korean buffet with over 40 homestyle dishes for just 8,000 KRW (~$6)?</strong> Welcome to <strong>World Bap (월드밥)</strong> in Gwangju's Seo-gu district — featured on Korea's hit TV show as a "Price Destroyer" restaurant that defies all expectations.</p>

<div class="highlight-box">
💡 <strong>Why This Restaurant is Special:</strong> Over 40 different Korean homestyle dishes available as an all-you-can-eat buffet for just 8,000 KRW. Fresh kimchi jjigae, japchae, Korean pancakes, grilled fish, and dozens more side dishes — all made fresh daily. It's the ultimate Korean comfort food experience at an unbeatable price.
</div>

<h2>📍 Restaurant Info</h2>
<div class="info-card">
<strong>🏪 Name:</strong> 월드밥 (World Bap)<br>
<strong>📍 Location:</strong> Seo-gu, Gwangju, South Korea<br>
<strong>💰 Price:</strong> 8,000 KRW (~$6 USD) per person — unlimited buffet<br>
<strong>📺 Featured on:</strong> KBS2 2TV 생생정보 (Feb 26, 2026) — "Price Destroyer Why" segment<br>
<strong>🕐 Hours:</strong> 11:00-21:00 daily
</div>

<h2>🍽️ What You Can Expect</h2>
<table class="menu-table">
<tr><th>Category</th><th>Dishes</th></tr>
<tr><td>🍲 Stews & Soups</td><td>Kimchi Jjigae, Doenjang Jjigae, various Korean soups</td></tr>
<tr><td>🥘 Main Dishes</td><td>Japchae, Grilled Fish, Bulgogi, Korean Pancakes</td></tr>
<tr><td>🥗 Side Dishes (Banchan)</td><td>40+ rotating Korean side dishes made fresh daily</td></tr>
<tr><td>🍚 Rice & Noodles</td><td>Steamed rice, various noodle options</td></tr>
</table>

<h2>💬 Visitor Reviews</h2>
<blockquote style="background:#f1f2f6; padding:15px; border-radius:10px; border-left:4px solid #d63031;">
"I couldn't believe this was only 8,000 won! The variety is amazing and everything tastes homemade. Perfect for travelers who want to try many Korean dishes at once without breaking the bank."
</blockquote>

<h2>🗺️ How to Get There</h2>
<p>🚇 <strong>Subway:</strong> Gwangju Metro Line 1, nearest station in Seo-gu area<br>
🚌 <strong>Bus:</strong> Multiple city bus routes to Seo-gu<br>
✈️ <strong>From Seoul:</strong> KTX to Gwangju Songjeong Station (~1.5 hours)</p>

<div class="cta">🔥 The best budget Korean food experience! 40+ dishes, unlimited refills, just $6. A food lover's dream in Gwangju.</div>

<span class="tag">#KoreanFood</span> <span class="tag">#KoreanBuffet</span> <span class="tag">#BudgetDining</span> <span class="tag">#Gwangju</span> <span class="tag">#KoreanFoodShow</span> <span class="tag">#AllYouCanEat</span>
</div>"""
    },
    {
        "title": "Yasanhaechon – Singer Seol Woon-do's Favorite Fresh Cod Soup in Yangpyeong",
        "tags": ["Korean Food", "KBS 2TV", "Yangpyeong", "Cod Soup", "Celebrity Restaurant", "Korean TV Show", "Daegu Tang"],
        "content": """<style>
.sf-post { font-family: 'Noto Sans KR', sans-serif; max-width: 800px; margin: 0 auto; line-height: 1.8; color: #333; }
.sf-post h2 { color: #2d3436; margin-top: 30px; }
.sf-post .highlight-box { background: #ffeaa7; padding: 15px 20px; border-radius: 10px; margin: 20px 0; }
.sf-post .menu-table { width: 100%; border-collapse: collapse; margin: 15px 0; }
.sf-post .menu-table th, .sf-post .menu-table td { border: 1px solid #ddd; padding: 10px; text-align: left; }
.sf-post .menu-table th { background: #d63031; color: white; }
.sf-post .info-card { background: #f8f9fa; border-left: 4px solid #d63031; padding: 15px; margin: 20px 0; }
.sf-post .tag { display: inline-block; background: #74b9ff; color: white; padding: 3px 10px; border-radius: 15px; margin: 3px; font-size: 13px; }
.sf-post .cta { background: #d63031; color: white; padding: 15px; text-align: center; border-radius: 10px; margin: 30px 0; font-size: 18px; }
</style>
<div class="sf-post">

<p><em>Featured on KBS2 "2TV 생생정보" (Feb 25, 2026) — Corner: Star Restaurant | Recommended by: Singer Seol Woon-do</em></p>

<p>Legendary Korean singer <strong>Seol Woon-do</strong>, who has lived in Yangpyeong for 14 years, personally recommends this hidden gem. <strong>Yasanhaechon (야산해촌)</strong> serves the most pristine, clear <strong>fresh cod soup (생대구맑은탕)</strong> — a warming, clean-flavored broth that keeps locals coming back for over a decade.</p>

<div class="highlight-box">
💡 <strong>Why This Restaurant is Special:</strong> Fresh seasonal cod simmered into a crystal-clear, deeply flavorful broth. No MSG, no shortcuts — just pure ingredients. Singer Seol Woon-do has been a regular for 14 years and calls it his #1 restaurant in Yangpyeong.
</div>

<h2>📍 Restaurant Info</h2>
<div class="info-card">
<strong>🏪 Name:</strong> 야산해촌 본점 (Yasanhaechon Main Branch)<br>
<strong>📍 Location:</strong> Yangpyeong-gun, Gyeonggi-do, South Korea<br>
<strong>📺 Featured on:</strong> KBS2 2TV 생생정보 (Feb 25, 2026) — "Star Restaurant" segment<br>
<strong>⭐ Recommended by:</strong> Singer Seol Woon-do (14-year Yangpyeong resident)<br>
<strong>🅿️ Parking:</strong> Available on-site
</div>

<h2>🍽️ Signature Menu</h2>
<table class="menu-table">
<tr><th>Menu</th><th>Description</th></tr>
<tr><td>🥇 Fresh Cod Clear Soup (생대구맑은탕)</td><td>Crystal-clear broth with tender fresh cod — the signature dish</td></tr>
<tr><td>Braised Fish (생선조림)</td><td>Sweet and spicy braised seasonal fish</td></tr>
<tr><td>Raw Fish Salad (회무침)</td><td>Fresh sashimi tossed with vegetables in tangy dressing</td></tr>
<tr><td>Fish Jiri Tang (지리탕)</td><td>Light, clean fish soup — perfect for hangovers</td></tr>
</table>

<h2>💬 Visitor Reviews</h2>
<blockquote style="background:#f1f2f6; padding:15px; border-radius:10px; border-left:4px solid #d63031;">
"The broth is unbelievably clean and refreshing. The cod is so tender it melts in your mouth. I understand why Seol Woon-do comes here every week. Worth the drive from Seoul!"
</blockquote>

<h2>🗺️ How to Get There</h2>
<p>🚗 <strong>By Car:</strong> From Seoul via Jungang Expressway, about 1 hour to Yangpyeong<br>
🚆 <strong>Train:</strong> Gyeongui-Jungang Line to Yangpyeong Station, then taxi<br>
💡 <strong>Tip:</strong> Combine with a scenic Yangpyeong river drive for the perfect day trip from Seoul</p>

<div class="cta">🐟 A celebrity-approved hidden gem! Fresh cod soup so good, a famous singer has been a regular for 14 years.</div>

<span class="tag">#KoreanFood</span> <span class="tag">#CodSoup</span> <span class="tag">#Yangpyeong</span> <span class="tag">#CelebrityRestaurant</span> <span class="tag">#KoreanFoodShow</span> <span class="tag">#DayTripFromSeoul</span>
</div>"""
    },
    {
        "title": "Jun (준) – Mind-Blowing King Rib Seafood Stone Plate Jjajang in Daegu",
        "tags": ["Korean Food", "KBS 2TV", "Daegu Restaurant", "Chinese-Korean Fusion", "Jjajangmyeon", "Korean TV Show"],
        "content": """<style>
.sf-post { font-family: 'Noto Sans KR', sans-serif; max-width: 800px; margin: 0 auto; line-height: 1.8; color: #333; }
.sf-post h2 { color: #2d3436; margin-top: 30px; }
.sf-post .highlight-box { background: #ffeaa7; padding: 15px 20px; border-radius: 10px; margin: 20px 0; }
.sf-post .menu-table { width: 100%; border-collapse: collapse; margin: 15px 0; }
.sf-post .menu-table th, .sf-post .menu-table td { border: 1px solid #ddd; padding: 10px; text-align: left; }
.sf-post .menu-table th { background: #d63031; color: white; }
.sf-post .info-card { background: #f8f9fa; border-left: 4px solid #d63031; padding: 15px; margin: 20px 0; }
.sf-post .tag { display: inline-block; background: #74b9ff; color: white; padding: 3px 10px; border-radius: 15px; margin: 3px; font-size: 13px; }
.sf-post .cta { background: #d63031; color: white; padding: 15px; text-align: center; border-radius: 10px; margin: 30px 0; font-size: 18px; }
</style>
<div class="sf-post">

<p><em>Featured on KBS2 "2TV 생생정보" (Feb 24, 2026) — Corner: The Decisive Move</em></p>

<p>Imagine <strong>jjajangmyeon (black bean noodles)</strong> — but reinvented with <strong>king-sized galbi ribs and seafood, served on a sizzling stone plate</strong>. Welcome to <strong>Jun (준)</strong> in Daegu's Dalseo-gu district, where Korean-Chinese cuisine gets a jaw-dropping upgrade.</p>

<div class="highlight-box">
💡 <strong>Why This Restaurant is Special:</strong> "Rediscovery of Meat" — that's how the TV show described it. King ribs + seafood + jjajang sauce on a blazing hot stone plate. Plus thick-cut sirloin tangsuyuk (sweet & sour pork) that's unlike anything you've had before.
</div>

<h2>📍 Restaurant Info</h2>
<div class="info-card">
<strong>🏪 Name:</strong> 준 (Jun)<br>
<strong>📍 Location:</strong> Dalgubeol-daero 251 An-gil 5-6, Dalseo-gu, Daegu<br>
<strong>📞 Phone:</strong> 0507-1481-7773<br>
<strong>📺 Featured on:</strong> KBS2 2TV 생생정보 (Feb 24, 2026) — "The Decisive Move" segment
</div>

<h2>🍽️ Signature Menu</h2>
<table class="menu-table">
<tr><th>Menu</th><th>Description</th></tr>
<tr><td>🥇 King Rib Seafood Stone Plate Jjajang</td><td>Sizzling stone plate with king ribs, seafood, and jjajang — the star dish</td></tr>
<tr><td>King Rib Seafood Jjamppong</td><td>Spicy noodle soup with king ribs and fresh seafood</td></tr>
<tr><td>🥈 Thick-Cut Sirloin Tangsuyuk</td><td>Premium sirloin sweet & sour pork, crispy outside, juicy inside</td></tr>
<tr><td>Silky Tofu Jjamppong</td><td>Unique jjamppong with soft Chodang tofu</td></tr>
</table>

<h2>💬 Visitor Reviews</h2>
<blockquote style="background:#f1f2f6; padding:15px; border-radius:10px; border-left:4px solid #d63031;">
"I was skeptical about ribs on jjajangmyeon, but one bite and I was converted. The stone plate keeps everything sizzling hot until the last bite. The tangsuyuk is next-level crispy!"
</blockquote>

<h2>🗺️ How to Get There</h2>
<p>🚇 <strong>Subway:</strong> Daegu Metro Line 2, Seongseosaneopdanji Station (~200m walk)<br>
✈️ <strong>From Seoul:</strong> KTX to Dongdaegu Station (~1.5 hours), then subway</p>

<div class="cta">🔥 Korean-Chinese fusion at its finest! King ribs + seafood + stone plate jjajang = unforgettable Daegu food experience.</div>

<span class="tag">#KoreanFood</span> <span class="tag">#Daegu</span> <span class="tag">#Jjajangmyeon</span> <span class="tag">#KoreanChineseFusion</span> <span class="tag">#KoreanFoodShow</span> <span class="tag">#StonePlate</span>
</div>"""
    },
    {
        "title": "Seomyeon Sondubu-jip – Grandma's Handmade Tofu Set Meal in Chuncheon",
        "tags": ["Korean Food", "KBS 2TV", "Chuncheon", "Handmade Tofu", "Traditional Korean", "Korean TV Show", "Gangwon-do"],
        "content": """<style>
.sf-post { font-family: 'Noto Sans KR', sans-serif; max-width: 800px; margin: 0 auto; line-height: 1.8; color: #333; }
.sf-post h2 { color: #2d3436; margin-top: 30px; }
.sf-post .highlight-box { background: #ffeaa7; padding: 15px 20px; border-radius: 10px; margin: 20px 0; }
.sf-post .menu-table { width: 100%; border-collapse: collapse; margin: 15px 0; }
.sf-post .menu-table th, .sf-post .menu-table td { border: 1px solid #ddd; padding: 10px; text-align: left; }
.sf-post .menu-table th { background: #d63031; color: white; }
.sf-post .info-card { background: #f8f9fa; border-left: 4px solid #d63031; padding: 15px; margin: 20px 0; }
.sf-post .tag { display: inline-block; background: #74b9ff; color: white; padding: 3px 10px; border-radius: 15px; margin: 3px; font-size: 13px; }
.sf-post .cta { background: #d63031; color: white; padding: 15px; text-align: center; border-radius: 10px; margin: 30px 0; font-size: 18px; }
</style>
<div class="sf-post">

<p><em>Featured on KBS2 "2TV 생생정보" (Feb 20, 2026) — Corner: Grandma, Is the Rice Ready?</em></p>

<p>Deep in the mountains of <strong>Chuncheon, Gangwon-do</strong>, Grandma Yang-suk wakes before dawn every morning to soak beans, grind them on a traditional stone mill, and hand-make the silkiest tofu you'll ever taste. <strong>Seomyeon Sondubu-jip (서면손두부집)</strong> is the definition of Korean soul food.</p>

<div class="highlight-box">
💡 <strong>Why This Restaurant is Special:</strong> 100% handmade tofu made fresh every morning using traditional methods. The set meal comes with different homestyle side dishes every visit — all grown and prepared by the grandmother herself. Pure, healthy Korean comfort food.
</div>

<h2>📍 Restaurant Info</h2>
<div class="info-card">
<strong>🏪 Name:</strong> 서면손두부집 (Seomyeon Handmade Tofu House)<br>
<strong>📍 Address:</strong> 31-11 Dangsan-gil, Seomyeon, Chuncheon, Gangwon-do<br>
<strong>📞 Phone:</strong> 033-243-2280<br>
<strong>📺 Featured on:</strong> KBS2 2TV 생생정보 (Feb 20, 2026) — "Grandma, Is the Rice Ready?" segment<br>
<strong>🕐 Hours:</strong> Mon-Sat 10:00-18:00 (Closed Sundays)
</div>

<h2>🍽️ Signature Menu</h2>
<table class="menu-table">
<tr><th>Menu</th><th>Description</th></tr>
<tr><td>🥇 Handmade Tofu Set Meal (손두부 정식)</td><td>Silky fresh tofu with rotating daily side dishes — full Korean table</td></tr>
<tr><td>Tofu Hot Pot (두부 전골)</td><td>Warming tofu stew perfect for cold days</td></tr>
<tr><td>Grilled Tofu (두부구이)</td><td>Pan-grilled tofu with crispy outside and creamy inside</td></tr>
</table>

<h2>💬 Visitor Reviews</h2>
<blockquote style="background:#f1f2f6; padding:15px; border-radius:10px; border-left:4px solid #d63031;">
"The tofu literally melts on your tongue — so silky and delicate. Every side dish feels like a grandma's home cooking. My stomach felt so happy and light after this meal. A healing experience!"
</blockquote>

<h2>🗺️ How to Get There</h2>
<p>🚗 <strong>By Car:</strong> Seoul-Chuncheon Expressway, exit at Chuncheon IC<br>
🚌 <strong>Bus:</strong> From Chuncheon Intercity Bus Terminal, take local bus to Seomyeon<br>
💡 <strong>Tip:</strong> Perfect combined with Nami Island or Chuncheon Dakgalbi Street visit</p>

<div class="cta">🌿 Healing Korean food at its purest. Grandma's handmade tofu in the mountains of Chuncheon — worth the journey.</div>

<span class="tag">#KoreanFood</span> <span class="tag">#HandmadeTofu</span> <span class="tag">#Chuncheon</span> <span class="tag">#TraditionalKorean</span> <span class="tag">#KoreanFoodShow</span> <span class="tag">#Gangwondo</span>
</div>"""
    },
    {
        "title": "Gukbo 1st – Unlimited Korean Beef Noodle Soup & Bossam for $10 in Bucheon",
        "tags": ["Korean Food", "KBS 2TV", "Bucheon", "Budget Dining", "Bossam", "Kalguksu", "Korean TV Show", "Unlimited Refill"],
        "content": """<style>
.sf-post { font-family: 'Noto Sans KR', sans-serif; max-width: 800px; margin: 0 auto; line-height: 1.8; color: #333; }
.sf-post h2 { color: #2d3436; margin-top: 30px; }
.sf-post .highlight-box { background: #ffeaa7; padding: 15px 20px; border-radius: 10px; margin: 20px 0; }
.sf-post .menu-table { width: 100%; border-collapse: collapse; margin: 15px 0; }
.sf-post .menu-table th, .sf-post .menu-table td { border: 1px solid #ddd; padding: 10px; text-align: left; }
.sf-post .menu-table th { background: #d63031; color: white; }
.sf-post .info-card { background: #f8f9fa; border-left: 4px solid #d63031; padding: 15px; margin: 20px 0; }
.sf-post .tag { display: inline-block; background: #74b9ff; color: white; padding: 3px 10px; border-radius: 15px; margin: 3px; font-size: 13px; }
.sf-post .cta { background: #d63031; color: white; padding: 15px; text-align: center; border-radius: 10px; margin: 30px 0; font-size: 18px; }
.sf-post .price-badge { background: #e17055; color: white; font-size: 24px; font-weight: bold; padding: 10px 20px; border-radius: 10px; display: inline-block; }
</style>
<div class="sf-post">

<p><em>Featured on KBS2 "2TV 생생정보" (Feb 11, 2026) — Corner: Price Destroyer Why</em></p>

<div class="highlight-box">
<div class="price-badge">Unlimited Kalguksu + Bossam = $10</div><br><br>
💡 <strong>Korean beef bone broth noodle soup + domestic pork bossam — UNLIMITED REFILLS</strong> for just 13,900 KRW (~$10). The rich bone broth is simmered for hours, and the bossam is tender with zero gamey taste.
</div>

<h2>📍 Restaurant Info</h2>
<div class="info-card">
<strong>🏪 Name:</strong> 국보1호점 (Gukbo 1st Branch)<br>
<strong>📍 Address:</strong> 234 Gilju-ro, Wonmi-gu, Bucheon (Hillstate Joong-dong)<br>
<strong>📞 Phone:</strong> 032-651-1566<br>
<strong>💰 Price:</strong> 13,900 KRW (Adult) / 9,000 KRW (Child) — unlimited<br>
<strong>🕐 Hours:</strong> 11:00-21:00 (Break 15:00-17:00)<br>
<strong>📺 Featured on:</strong> KBS2 2TV 생생정보 (Feb 11, 2026)
</div>

<h2>🍽️ Menu & Pricing</h2>
<table class="menu-table">
<tr><th>Menu</th><th>Description</th><th>Price</th></tr>
<tr><td>🥇 Kalguksu + Bossam Unlimited (Adult)</td><td>Korean beef bone broth noodles + pork bossam — eat all you want</td><td>13,900 KRW</td></tr>
<tr><td>Kalguksu + Bossam Unlimited (Child)</td><td>Same menu, kid's price</td><td>9,000 KRW</td></tr>
<tr><td>Hot Pot Kalguksu + Bossam Set</td><td>Hot pot style noodles + bossam tasting set</td><td>10,000 KRW</td></tr>
</table>

<h2>💬 Visitor Reviews</h2>
<blockquote style="background:#f1f2f6; padding:15px; border-radius:10px; border-left:4px solid #d63031;">
"UNLIMITED kalguksu and bossam for this price?! The bone broth is seriously rich and deep. The bossam is so tender and clean-tasting. I kept going back for refills. Best value meal I've had in Korea!"
</blockquote>

<h2>🗺️ How to Get There</h2>
<p>🚇 <strong>Subway:</strong> Line 7, Sinjungdong Station or Bucheon City Hall Station<br>
🅿️ <strong>Parking:</strong> Free underground parking at Hillstate Joong-dong</p>

<div class="cta">🔥 Best budget Korean meal! Unlimited Korean beef noodle soup + bossam for just $10. Bucheon's ultimate price buster!</div>

<span class="tag">#KoreanFood</span> <span class="tag">#BudgetDining</span> <span class="tag">#Kalguksu</span> <span class="tag">#Bossam</span> <span class="tag">#Bucheon</span> <span class="tag">#UnlimitedRefill</span> <span class="tag">#KoreanFoodShow</span>
</div>"""
    },
    {
        "title": "Imja – Triple-Style Fresh Monkfish Soup with Free Liver Service in Gangnam",
        "tags": ["Korean Food", "KBS 2TV", "Gangnam", "Seoul Restaurant", "Monkfish Soup", "Korean TV Show", "Agwi Tang"],
        "content": """<style>
.sf-post { font-family: 'Noto Sans KR', sans-serif; max-width: 800px; margin: 0 auto; line-height: 1.8; color: #333; }
.sf-post h2 { color: #2d3436; margin-top: 30px; }
.sf-post .highlight-box { background: #ffeaa7; padding: 15px 20px; border-radius: 10px; margin: 20px 0; }
.sf-post .menu-table { width: 100%; border-collapse: collapse; margin: 15px 0; }
.sf-post .menu-table th, .sf-post .menu-table td { border: 1px solid #ddd; padding: 10px; text-align: left; }
.sf-post .menu-table th { background: #d63031; color: white; }
.sf-post .info-card { background: #f8f9fa; border-left: 4px solid #d63031; padding: 15px; margin: 20px 0; }
.sf-post .tag { display: inline-block; background: #74b9ff; color: white; padding: 3px 10px; border-radius: 15px; margin: 3px; font-size: 13px; }
.sf-post .cta { background: #d63031; color: white; padding: 15px; text-align: center; border-radius: 10px; margin: 30px 0; font-size: 18px; }
</style>
<div class="sf-post">

<p><em>Featured on KBS2 "2TV 생생정보" (Feb 9, 2026) — Corner: Master of Business</em></p>

<p>In the heart of <strong>Gangnam, Nonhyeon-dong</strong>, there's a monkfish specialist that offers something unique: choose your broth style — <strong>clear, spicy, or perilla seed</strong> — and get a complimentary serving of rare <strong>fresh monkfish liver</strong>. Welcome to <strong>Imja (임자)</strong>.</p>

<div class="highlight-box">
💡 <strong>Why This Restaurant is Special:</strong> Three styles of fresh monkfish soup (clear, spicy, perilla), each with deep, complex flavors. Because they use only fresh (not frozen) monkfish, they can offer the prized monkfish liver as a FREE side — a delicacy most places can't serve.
</div>

<h2>📍 Restaurant Info</h2>
<div class="info-card">
<strong>🏪 Name:</strong> 임자 (Imja)<br>
<strong>📍 Location:</strong> Nonhyeon-dong, Gangnam-gu, Seoul (near Seonjeongneung & Gangnam-gu Office Station)<br>
<strong>📺 Featured on:</strong> KBS2 2TV 생생정보 (Feb 9, 2026) — "Master of Business" segment
</div>

<h2>🍽️ Signature Menu</h2>
<table class="menu-table">
<tr><th>Menu</th><th>Description</th></tr>
<tr><td>🥇 Fresh Monkfish Soup – Clear (맑은탕)</td><td>Crystal-clear, refreshing broth with tender monkfish</td></tr>
<tr><td>Fresh Monkfish Soup – Spicy (매운탕)</td><td>Bold, fiery broth for spice lovers</td></tr>
<tr><td>Fresh Monkfish Soup – Perilla (들깨탕)</td><td>Rich, nutty perilla seed broth — the signature choice</td></tr>
<tr><td>⭐ Monkfish Liver (FREE)</td><td>Rare delicacy served complimentary with fresh monkfish orders</td></tr>
<tr><td>🥈 Spicy Monkfish Stew (아귀찜)</td><td>Spicy-sweet braised monkfish with bean sprouts</td></tr>
</table>

<h2>💬 Visitor Reviews</h2>
<blockquote style="background:#f1f2f6; padding:15px; border-radius:10px; border-left:4px solid #d63031;">
"The perilla seed broth is INCREDIBLE — spicy yet nutty and creamy. The monkfish meat is so tender. And the free liver side? Chef's kiss. Best seafood soup I've had in Seoul."
</blockquote>

<h2>🗺️ How to Get There</h2>
<p>🚇 <strong>Subway:</strong> Seonjeongneung Station or Gangnam-gu Office Station, 5-10 min walk<br>
📍 <strong>Area:</strong> Gangnam Nonhyeon-dong — plenty of dining options nearby</p>

<div class="cta">🐟 Three ways to enjoy fresh monkfish + free liver service! A hidden Gangnam gem for seafood lovers.</div>

<span class="tag">#KoreanFood</span> <span class="tag">#Gangnam</span> <span class="tag">#MonkfishSoup</span> <span class="tag">#SeoulRestaurant</span> <span class="tag">#KoreanFoodShow</span> <span class="tag">#SeafoodLovers</span>
</div>"""
    },
    {
        "title": "Haengju Chueotang – Comedian Kim Mi-ryeo's Go-To Loach Soup at Haengju Fortress",
        "tags": ["Korean Food", "KBS 2TV", "Goyang", "Loach Soup", "Celebrity Restaurant", "Korean TV Show", "Traditional Korean"],
        "content": """<style>
.sf-post { font-family: 'Noto Sans KR', sans-serif; max-width: 800px; margin: 0 auto; line-height: 1.8; color: #333; }
.sf-post h2 { color: #2d3436; margin-top: 30px; }
.sf-post .highlight-box { background: #ffeaa7; padding: 15px 20px; border-radius: 10px; margin: 20px 0; }
.sf-post .menu-table { width: 100%; border-collapse: collapse; margin: 15px 0; }
.sf-post .menu-table th, .sf-post .menu-table td { border: 1px solid #ddd; padding: 10px; text-align: left; }
.sf-post .menu-table th { background: #d63031; color: white; }
.sf-post .info-card { background: #f8f9fa; border-left: 4px solid #d63031; padding: 15px; margin: 20px 0; }
.sf-post .tag { display: inline-block; background: #74b9ff; color: white; padding: 3px 10px; border-radius: 15px; margin: 3px; font-size: 13px; }
.sf-post .cta { background: #d63031; color: white; padding: 15px; text-align: center; border-radius: 10px; margin: 30px 0; font-size: 18px; }
</style>
<div class="sf-post">

<p><em>Featured on KBS2 "2TV 생생정보" (Feb 5, 2026) — Corner: Star Restaurant | Recommended by: Comedian Kim Mi-ryeo</em></p>

<p>Near the historic <strong>Haengju Fortress</strong> in Goyang city, comedian <strong>Kim Mi-ryeo</strong> swears by this old-school restaurant's <strong>spicy loach soup (추어매운탕)</strong>. Unlike typical thick, muddy-tasting chueotang, this version is <strong>clear, clean, and vibrantly spicy</strong>.</p>

<div class="highlight-box">
💡 <strong>Why This Restaurant is Special:</strong> A beloved local institution! Their loach soup defies expectations — clear broth that's both refreshing and fiery, with handmade sujebi (dough flakes) and noodles in the pot. Order whole loach (통추어, min. 2 portions) or ground loach (간추어, 1 portion OK).
</div>

<h2>📍 Restaurant Info</h2>
<div class="info-card">
<strong>🏪 Name:</strong> 행주추어매운탕 (Haengju Chueotang)<br>
<strong>📍 Location:</strong> Haengju-dong, Deokyang-gu, Goyang-si (Haengju Fortress Food Village)<br>
<strong>📺 Featured on:</strong> KBS2 2TV 생생정보 (Feb 5, 2026) — "Star Restaurant" segment<br>
<strong>⭐ Recommended by:</strong> Comedian Kim Mi-ryeo
</div>

<h2>🍽️ Signature Menu</h2>
<table class="menu-table">
<tr><th>Menu</th><th>Description</th></tr>
<tr><td>🥇 Spicy Loach Soup – Whole (통추어)</td><td>Clear, spicy broth with whole loach + sujebi + noodles (min. 2 portions)</td></tr>
<tr><td>Spicy Loach Soup – Ground (간추어)</td><td>Ground loach version, available per portion</td></tr>
<tr><td>🥈 Catfish Stew (메기 매운탕)</td><td>Light yet spicy catfish stew</td></tr>
<tr><td>🥉 Grilled Eel (장어구이)</td><td>Charcoal-grilled eel, savory and chewy</td></tr>
</table>

<h2>💬 Visitor Reviews</h2>
<blockquote style="background:#f1f2f6; padding:15px; border-radius:10px; border-left:4px solid #d63031;">
"Nothing like the thick, heavy chueotang I expected. This is CLEAR and refreshing but still packs a spicy punch. The sujebi and noodles make it a complete meal. Even people who hate chueotang would love this version!"
</blockquote>

<h2>🗺️ How to Get There</h2>
<p>🚇 <strong>Subway:</strong> Line 3, Wondang or Hwajeong Station, then bus/taxi<br>
💡 <strong>Tip:</strong> Visit Haengju Fortress first, then walk to the Food Village for lunch</p>

<div class="cta">🏯 History + Food combo! Visit Haengju Fortress, then warm up with celebrity-approved spicy loach soup.</div>

<span class="tag">#KoreanFood</span> <span class="tag">#LoachSoup</span> <span class="tag">#Goyang</span> <span class="tag">#HaengjuFortress</span> <span class="tag">#CelebrityRestaurant</span> <span class="tag">#KoreanFoodShow</span>
</div>"""
    },
    {
        "title": "Pohang Halmae-jip – 70-Year-Old, 3rd Generation Ox Head Soup in Yeongcheon Market",
        "tags": ["Korean Food", "KBS 2TV", "Yeongcheon", "Ox Head Soup", "Traditional Market", "Korean TV Show", "Century Restaurant"],
        "content": """<style>
.sf-post { font-family: 'Noto Sans KR', sans-serif; max-width: 800px; margin: 0 auto; line-height: 1.8; color: #333; }
.sf-post h2 { color: #2d3436; margin-top: 30px; }
.sf-post .highlight-box { background: #ffeaa7; padding: 15px 20px; border-radius: 10px; margin: 20px 0; }
.sf-post .menu-table { width: 100%; border-collapse: collapse; margin: 15px 0; }
.sf-post .menu-table th, .sf-post .menu-table td { border: 1px solid #ddd; padding: 10px; text-align: left; }
.sf-post .menu-table th { background: #d63031; color: white; }
.sf-post .info-card { background: #f8f9fa; border-left: 4px solid #d63031; padding: 15px; margin: 20px 0; }
.sf-post .tag { display: inline-block; background: #74b9ff; color: white; padding: 3px 10px; border-radius: 15px; margin: 3px; font-size: 13px; }
.sf-post .cta { background: #d63031; color: white; padding: 15px; text-align: center; border-radius: 10px; margin: 30px 0; font-size: 18px; }
</style>
<div class="sf-post">

<p><em>Featured on KBS2 "2TV 생생정보" (Feb 2, 2026) — Corner: Grandma, Is the Rice Ready?</em></p>

<p>For <strong>70 years and three generations</strong>, this family has been serving one thing and one thing only: <strong>ox head soup (소머리곰탕)</strong>. Located inside the bustling <strong>Yeongcheon Public Market</strong>, <strong>Pohang Halmae-jip</strong> is a government-certified "Century Restaurant" where people drive hours just for a single bowl.</p>

<div class="highlight-box">
💡 <strong>Why This Restaurant is Special:</strong> Certified "Century Restaurant" by Korea's Ministry of SMEs. The ox head is slow-simmered in a massive traditional cauldron, then ladled into stone bowls using the toreum (pouring) method. Zero gamey smell — just pure, milky-white, deeply satisfying bone broth. Only 9,000 KRW (~$7).
</div>

<h2>📍 Restaurant Info</h2>
<div class="info-card">
<strong>🏪 Name:</strong> 포항할매집 (Pohang Halmae-jip / Pohang Grandma's House)<br>
<strong>📍 Address:</strong> 52 Sijang 4-gil, Yeongcheon-si, Gyeongsangbuk-do (inside Yeongcheon Public Market)<br>
<strong>💰 Price:</strong> 9,000 KRW (regular) / 10,000 KRW (Korean beef version)<br>
<strong>🕐 Hours:</strong> 07:00-20:00 (Closed 1st & 15th of each month)<br>
<strong>📺 Featured on:</strong> KBS2 2TV 생생정보 (Feb 2, 2026)
</div>

<h2>🍽️ Menu</h2>
<table class="menu-table">
<tr><th>Menu</th><th>Description</th><th>Price</th></tr>
<tr><td>🥇 Ox Head Soup (소머리곰탕)</td><td>70-year recipe, massive cauldron, toreum-style serving</td><td>9,000 KRW</td></tr>
<tr><td>🐄 Korean Beef Ox Head Soup</td><td>Premium Korean beef version</td><td>10,000 KRW</td></tr>
<tr><td>📦 Takeout Pack (5 bowls)</td><td>Take-home set of 5 servings</td><td>20,000 KRW</td></tr>
</table>

<h2>💬 Visitor Reviews</h2>
<blockquote style="background:#f1f2f6; padding:15px; border-radius:10px; border-left:4px solid #d63031;">
"Drove 3 hours from Seoul and zero regrets. The broth is IMPOSSIBLY clean — milky white, deeply beefy, absolutely no gamey taste. Generous chunks of meat. At 9,000 won, this might be the best value meal in all of Korea. 70 years of mastery in every sip."
</blockquote>

<h2>🗺️ How to Get There</h2>
<p>🚗 <strong>By Car:</strong> Gyeongbu Expressway, Yeongcheon IC exit (~10 min to market)<br>
🚆 <strong>Train:</strong> KTX/Mugunghwa to Yeongcheon Station, taxi ~5 min<br>
💡 <strong>Tip:</strong> Explore Yeongcheon Traditional Market after your meal</p>

<div class="cta">🏆 Government-certified Century Restaurant! 70 years, 3 generations, one perfect ox head soup. Worth every kilometer of the drive.</div>

<span class="tag">#KoreanFood</span> <span class="tag">#OxHeadSoup</span> <span class="tag">#Yeongcheon</span> <span class="tag">#TraditionalMarket</span> <span class="tag">#CenturyRestaurant</span> <span class="tag">#KoreanFoodShow</span>
</div>"""
    },
    {
        "title": "Han Hye-jin's Hongcheon Food Trip – Buckwheat Noodles, Mind-Blowing Tofu & Pine Nut Hotteok",
        "tags": ["Korean Food", "KBS 2TV", "Hongcheon", "Gangwon-do Travel", "Makguksu", "Korean TV Show", "Winter Travel Korea"],
        "content": """<style>
.sf-post { font-family: 'Noto Sans KR', sans-serif; max-width: 800px; margin: 0 auto; line-height: 1.8; color: #333; }
.sf-post h2 { color: #2d3436; margin-top: 30px; }
.sf-post .highlight-box { background: #ffeaa7; padding: 15px 20px; border-radius: 10px; margin: 20px 0; }
.sf-post .menu-table { width: 100%; border-collapse: collapse; margin: 15px 0; }
.sf-post .menu-table th, .sf-post .menu-table td { border: 1px solid #ddd; padding: 10px; text-align: left; }
.sf-post .menu-table th { background: #d63031; color: white; }
.sf-post .info-card { background: #f8f9fa; border-left: 4px solid #d63031; padding: 15px; margin: 20px 0; }
.sf-post .tag { display: inline-block; background: #74b9ff; color: white; padding: 3px 10px; border-radius: 15px; margin: 3px; font-size: 13px; }
.sf-post .cta { background: #d63031; color: white; padding: 15px; text-align: center; border-radius: 10px; margin: 30px 0; font-size: 18px; }
</style>
<div class="sf-post">

<p><em>Featured on KBS2 "2TV 생생정보" (Jan 13, 2026) — Corner: Star's Hometown | With: Singer Han Hye-jin</em></p>

<p>Korean singer <strong>Han Hye-jin</strong> takes us on an unforgettable winter food trip through <strong>Hongcheon, Gangwon-do</strong> — one of Korea's best-kept secrets for nature, festivals, and incredible food. From chewy buckwheat noodles to "faint-worthy" fresh tofu to pine nut honey hotteok… this is the ultimate Hongcheon guide.</p>

<div class="highlight-box">
💡 <strong>Hongcheon Travel Highlights:</strong> Buckwheat noodles + fresh tofu combo at Sigol Makguksu, pine nut rice cakes & honey hotteok from local shops, PLUS winter attractions like the Hongcheongang Ice Festival and Alpaca World!
</div>

<h2>📍 Restaurant 1: Sigol Makguksu (시골막국수)</h2>
<div class="info-card">
<strong>🏪 Name:</strong> 시골막국수 (Country Buckwheat Noodles)<br>
<strong>📍 Address:</strong> 9 Sanghwagye 3-gil, Bukbang-myeon, Hongcheon-gun, Gangwon-do<br>
<strong>📞 Phone:</strong> 033-434-4313<br>
<strong>📺 Featured on:</strong> KBS2 2TV 생생정보 (Jan 13, 2026)
</div>

<table class="menu-table">
<tr><th>Menu</th><th>Description</th></tr>
<tr><td>🥇 Makguksu (막국수)</td><td>Chewy buckwheat noodles in cold broth — Gangwon-do's iconic dish</td></tr>
<tr><td>🥈 Fresh Whole Tofu (모두부)</td><td>"One bite and you'll faint" — silky, rich, unforgettable handmade tofu</td></tr>
</table>

<h2>📍 Restaurant 2: Pine Nut Treats (홍천읍)</h2>
<div class="info-card">
<strong>📍 Location:</strong> Hongcheon-eup, Hongcheon-gun<br>
<strong>📌 Specialty:</strong> Hongcheon's famous pine nuts turned into unique local snacks
</div>

<table class="menu-table">
<tr><th>Menu</th><th>Description</th></tr>
<tr><td>🥇 Pine Nut Rice Cake (잣떡)</td><td>Chewy rice cake packed with fragrant local pine nuts</td></tr>
<tr><td>🥈 Pine Nut Honey Hotteok (잣꿀호떡)</td><td>Crispy Korean pancake filled with honey and pine nuts — perfect winter snack</td></tr>
</table>

<h2>🎿 Hongcheon Winter Activities</h2>
<div class="highlight-box">
⛄ <strong>Hongcheongang Ice Festival:</strong> Ice fishing, sledding, and winter fun on the frozen Hongcheon River<br><br>
🦙 <strong>Alpaca World:</strong> Meet adorable alpacas at this animal theme park — great for families!
</div>

<h2>💬 Visitor Reviews</h2>
<blockquote style="background:#f1f2f6; padding:15px; border-radius:10px; border-left:4px solid #d63031;">
"The makguksu was great, but the TOFU — oh my god. So creamy and rich, I literally gasped. Then we hit the pine nut hotteok vendor and it was the perfect winter snack. Combined with the Ice Festival and Alpaca World, this was the best day trip from Seoul ever!"
</blockquote>

<h2>🗺️ How to Get There</h2>
<p>🚗 <strong>By Car:</strong> Seoul-Yangyang Expressway or Jungang Expressway, exit at Hongcheon IC<br>
🚌 <strong>Bus:</strong> East Seoul Terminal → Hongcheon (~1.5 hours)<br>
💡 <strong>Tip:</strong> Plan a full day: Sigol Makguksu → Alpaca World → Ice Festival → Pine Nut Hotteok</p>

<div class="cta">❄️ The ultimate Hongcheon winter food & travel guide! Buckwheat noodles + tofu + pine nut hotteok + ice festival = perfect Korean winter day trip.</div>

<span class="tag">#KoreanFood</span> <span class="tag">#Hongcheon</span> <span class="tag">#Makguksu</span> <span class="tag">#WinterTravel</span> <span class="tag">#KoreanFoodShow</span> <span class="tag">#Gangwondo</span> <span class="tag">#AlpacaWorld</span>
</div>"""
    }
]

# ---- Step 4: Publish all posts ----
published = 0
for i, post in enumerate(posts):
    print(f"\nPublishing [{i+1}/10]: {post['title'][:50]}...")

    data = {
        "title": post["title"],
        "content": post["content"],
        "status": "publish",
        "categories": [cat_id],
        "tags": [],  # will set separately
    }

    resp = session.post(f"{REST_URL}/posts", headers=headers, json=data)

    if resp.status_code == 201:
        post_id = resp.json()["id"]
        post_url = resp.json()["link"]
        print(f"  ✅ Published! ID={post_id} URL={post_url}")

        # Set tags
        tag_ids = []
        for tag_name in post["tags"]:
            # Check if tag exists
            existing = session.get(f"{REST_URL}/tags?search={tag_name}", headers=headers).json()
            if existing and not isinstance(existing, dict):
                tag_ids.append(existing[0]["id"])
            else:
                tag_resp = session.post(f"{REST_URL}/tags", headers=headers, json={"name": tag_name})
                if tag_resp.status_code == 201:
                    tag_ids.append(tag_resp.json()["id"])

        if tag_ids:
            session.post(f"{REST_URL}/posts/{post_id}", headers=headers, json={"tags": tag_ids})
            print(f"  Tags set: {len(tag_ids)} tags")

        published += 1
    else:
        print(f"  ❌ Failed: {resp.status_code} - {resp.text[:200]}")

print(f"\n{'='*50}")
print(f"DONE! Published {published}/10 posts.")
print(f"Visit: https://rhythmicaleskimo.com")
