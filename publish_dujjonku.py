#!/usr/bin/env python3
"""Publish Dujjonku Dubai Chocolate Cookie article to rhythmicaleskimo.com"""

import requests
import re
import json
import sys
import os
from PIL import Image, ImageDraw, ImageFont

# ─── 1. Generate Featured Image ───────────────────────────────────────────────

def generate_featured_image():
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), "#1a0a00")
    draw = ImageDraw.Draw(img)

    # Warm chocolate/gold gradient background
    for y in range(H):
        r_ratio = y / H
        r = int(26 + (60 - 26) * r_ratio)
        g = int(10 + (25 - 10) * r_ratio)
        b = int(0 + (10 - 0) * r_ratio)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # Gold decorative circles (cookie/chocolate aesthetic)
    import random
    random.seed(42)
    for _ in range(30):
        x = random.randint(0, W)
        y = random.randint(0, H)
        radius = random.randint(5, 40)
        opacity_r = random.randint(120, 200)
        opacity_g = random.randint(80, 160)
        opacity_b = random.randint(20, 60)
        draw.ellipse(
            [x - radius, y - radius, x + radius, y + radius],
            fill=(opacity_r, opacity_g, opacity_b),
            outline=None,
        )

    # Add pistachio green accent circles
    for _ in range(15):
        x = random.randint(0, W)
        y = random.randint(0, H)
        radius = random.randint(3, 20)
        draw.ellipse(
            [x - radius, y - radius, x + radius, y + radius],
            fill=(random.randint(80, 140), random.randint(140, 180), random.randint(60, 100)),
            outline=None,
        )

    # Semi-transparent overlay for text readability
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rectangle([50, 100, W - 50, H - 80], fill=(20, 8, 0, 180))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    # Gold border
    draw.rectangle([55, 105, W - 55, H - 85], outline=(212, 175, 55), width=2)

    # Text
    try:
        font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 48)
        font_medium = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 32)
        font_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
    except Exception:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Title line 1
    title1 = "DUJJONKU"
    bbox1 = draw.textbbox((0, 0), title1, font=font_large)
    x1 = (W - (bbox1[2] - bbox1[0])) // 2
    draw.text((x1, 150), title1, fill=(212, 175, 55), font=font_large)

    # Title line 2
    title2 = "Korea's Viral Dubai"
    bbox2 = draw.textbbox((0, 0), title2, font=font_medium)
    x2 = (W - (bbox2[2] - bbox2[0])) // 2
    draw.text((x2, 220), title2, fill=(255, 255, 255), font=font_medium)

    # Title line 3
    title3 = "Chocolate Cookie"
    bbox3 = draw.textbbox((0, 0), title3, font=font_medium)
    x3 = (W - (bbox3[2] - bbox3[0])) // 2
    draw.text((x3, 265), title3, fill=(255, 255, 255), font=font_medium)

    # Divider line
    draw.line([(W // 2 - 120, 325), (W // 2 + 120, 325)], fill=(212, 175, 55), width=2)

    # Subtitle
    subtitle = "Where to Buy in Seoul 2026"
    bbox_s = draw.textbbox((0, 0), subtitle, font=font_small)
    xs = (W - (bbox_s[2] - bbox_s[0])) // 2
    draw.text((xs, 345), subtitle, fill=(200, 200, 200), font=font_small)

    # Cookie emoji text
    tag = "Pistachio  |  Kataifi  |  Marshmallow  |  Chewy"
    bbox_t = draw.textbbox((0, 0), tag, font=font_small)
    xt = (W - (bbox_t[2] - bbox_t[0])) // 2
    draw.text((xt, 395), tag, fill=(170, 210, 130), font=font_small)

    # TikTok viral badge
    badge = "Taking Over TikTok"
    bbox_b = draw.textbbox((0, 0), badge, font=font_small)
    xb = (W - (bbox_b[2] - bbox_b[0])) // 2
    draw.text((xb, 445), badge, fill=(255, 100, 100), font=font_small)

    # Site branding
    brand = "rhythmicaleskimo.com"
    bbox_br = draw.textbbox((0, 0), brand, font=font_small)
    xbr = (W - (bbox_br[2] - bbox_br[0])) // 2
    draw.text((xbr, 500), brand, fill=(150, 150, 150), font=font_small)

    path = "/Users/choijooyong/wordpress/featured_dujjonku.png"
    img.save(path, "PNG", quality=95)
    print(f"Featured image saved: {path}")
    return path


# ─── 2. Article HTML ──────────────────────────────────────────────────────────

ARTICLE_HTML = """
<p><strong>Walk through any trendy Seoul neighborhood in early 2026 and you will see the same thing: long lines of people waiting before sunrise for a single cookie.</strong> Not just any cookie — a <em>dujjonku</em> (두쫑쿠), the Korean-born Dubai chocolate cookie that has taken over TikTok, crashed pistachio markets, and turned ordinary bakeries into overnight sensations.</p>

<p>Part cookie, part confection, part cultural phenomenon — dujjonku is a dense, stretchy, pull-apart dessert stuffed with pistachio cream and shredded kataifi pastry, wrapped in melted marshmallow and dusted with cocoa powder. If you are planning a trip to Korea or simply want to understand why an entire nation lost its mind over a cookie, this is the only guide you need.</p>

<h2>What Exactly Is a Dujjonku? The Dubai Chocolate Cookie Explained</h2>

<p>The name "dujjonku" (두쫑쿠) is a playful Korean abbreviation of "Dubai jjondeukhada cookie" — roughly meaning "Dubai chewy cookie." Unlike a traditional crumbly American cookie, dujjonku delivers a dense, almost mochi-like chewiness that Koreans describe as <em>jjondeukhada</em> (쫀득하다), a texture word that has no direct English equivalent but means something between "stretchy" and "satisfyingly chewy."</p>

<h3>Key Ingredients That Make It Special</h3>

<p><strong>Pistachio cream</strong> forms the rich, nutty heart of every dujjonku. This is not just any pistachio paste — Korean bakeries use premium blends that deliver an intense, almost savory depth. The pistachio cream creates the signature green filling that makes every pulled-apart cookie photo so Instagram-worthy.</p>

<p><strong>Kataifi (kadaif) pastry</strong> provides the crunch factor. These angel-hair-thin shredded phyllo threads add a delicate crispy texture that contrasts beautifully with the chewy base. When you bite in, you get that satisfying crackle before hitting the soft, stretchy center.</p>

<p><strong>Melted marshmallow</strong> is what transforms this from a regular stuffed cookie into something almost otherworldly. The marshmallow binding creates that legendary stretch — the dramatic pull-apart moment that has generated millions of TikTok views. Some bakeries use house-made marshmallow for an even silkier texture.</p>

<p><strong>Cocoa powder dusting</strong> finishes the cookie with a bittersweet contrast, balancing the sweetness of the marshmallow and the richness of the pistachio. Premium versions use high-quality Dutch-process cocoa for a deeper chocolate flavor.</p>

<h3>How It Differs from the Original Dubai Chocolate</h3>

<p>The original Dubai chocolate bar — the Fix Dessert Chocolatier creation that went viral globally in 2024 — is a thin chocolate shell filled with pistachio cream and kataifi. Korean creators took that flavor combination and reimagined it inside a thick, American-style cookie shell, adding marshmallow for the signature Korean <em>jjondeukhada</em> texture. The result is something entirely new: bigger, chewier, more dramatic, and perfectly engineered for social media content.</p>

<h2>How Dujjonku Went from Zero to National Obsession</h2>

<h3>The Dubai Chocolate Wave Hits Korea (2024)</h3>

<p>When the Dubai chocolate bar trend exploded on global social media in 2024, Korean consumers could not easily import the original Fix Dessert Chocolatier bars. Instead of waiting, creative Korean cafe owners decided to improvise. They took the key flavor profile — pistachio and kataifi — and infused it into the thick, chewy cookies that were already popular in Korea's dessert scene.</p>

<p>The first versions appeared in small independent bakeries in Seoul's Seongsu and Hapjeong neighborhoods during late 2024. Word spread slowly through Korean food blogs and Instagram food accounts, building a dedicated following among dessert enthusiasts.</p>

<h3>The K-Pop Spark: Jang Wonyoung Changes Everything</h3>

<p>The dujjonku craze might have remained a niche Seoul dessert trend if not for K-pop. In September 2025, IVE's Jang Wonyoung — one of the most influential celebrities in South Korea — posted photos of herself enjoying a dujjonku on social media. The effect was immediate and explosive.</p>

<p>Within days, the bakeries she visited reported lines stretching around the block. Other celebrities followed suit: actress Kim Se-jeong and actor Ko Yoon-jung both posted their own dujjonku reviews, adding fuel to an already blazing fire. By December 2025, buying a dujjonku in Seoul was harder than getting concert tickets.</p>

<h3>The "Open Run" Phenomenon</h3>

<p>Korea's famous "open run" culture — where people sprint to stores the moment they open — found a new target in dujjonku. People began lining up at famous cookie shops hours before opening time, sometimes arriving at 5 or 6 AM just to secure one or two cookies. Some bakeries had to halt in-store sales entirely and switch to online-only ordering to manage the crowds.</p>

<p>A live online map was even created to track which cafes and bakeries still had stock in real time, turning the hunt for dujjonku into a citywide treasure hunt. The scarcity only fueled more demand — the harder it was to get, the more people wanted it.</p>

<h3>TikTok and the Global Explosion</h3>

<p>On TikTok, dujjonku content has accumulated hundreds of millions of views. The dramatic pull-apart videos — showing the cookie stretching with its marshmallow filling in slow motion — became one of the most replicated food content formats on the platform. Korean food TikTokers, ASMR creators, and international food bloggers all jumped on the trend.</p>

<p>According to South Korea's largest food delivery app Baedal Minjok, pickup orders for dujjonku during the first week of January 2026 jumped more than 300 percent from a month earlier. The cookie did not just trend — it dominated.</p>

<h3>The Pistachio Price Crisis</h3>

<p>The dujjonku craze had unintended economic consequences that made headlines. A 1-kilogram bag of pistachios in South Korea surged from approximately 20,000 KRW to around 80,000 KRW — a 400% increase — between December 2025 and mid-January 2026. Domestic retailers reported price hikes of around 20%, driven by the combined pressure of surging domestic demand, rising global pistachio prices, and a weaker Korean won.</p>

<p>International pistachio prices climbed to about $12 per pound, up from around $8 a year earlier. The dujjonku was literally reshaping commodity markets.</p>

<h2>Where to Buy Dujjonku in Seoul: The Complete 2026 Guide</h2>

<p>Whether you are a tourist visiting Seoul or an expat looking to finally try the viral cookie, here is your comprehensive guide to the best dujjonku spots in the city.</p>

<h3>Top Specialty Bakeries</h3>

<div style="overflow-x:auto;">
<table style="width:100%;border-collapse:collapse;margin:1em 0;">
<thead>
<tr style="background:#2a1a0a;color:#d4af37;">
<th style="padding:12px;text-align:left;border-bottom:2px solid #d4af37;">Bakery</th>
<th style="padding:12px;text-align:left;border-bottom:2px solid #d4af37;">Location</th>
<th style="padding:12px;text-align:left;border-bottom:2px solid #d4af37;">Price Range</th>
<th style="padding:12px;text-align:left;border-bottom:2px solid #d4af37;">Why Visit</th>
</tr>
</thead>
<tbody>
<tr style="border-bottom:1px solid #333;">
<td style="padding:10px;"><strong>Mont Cookie</strong></td>
<td style="padding:10px;">Multiple locations; pop-ups at Shinsegae Gangnam</td>
<td style="padding:10px;">6,500–8,000 KRW</td>
<td style="padding:10px;">Credited as the original creator of dujjonku. The OG.</td>
</tr>
<tr style="border-bottom:1px solid #333;">
<td style="padding:10px;"><strong>All The Ugly Cookie</strong></td>
<td style="padding:10px;">Hapjeong: 45 Tojeong-ro, Mapo-gu / Seongsu branch</td>
<td style="padding:10px;">5,500–7,500 KRW</td>
<td style="padding:10px;">Famous rustic look, incredibly rich filling. Massive lines.</td>
</tr>
<tr style="border-bottom:1px solid #333;">
<td style="padding:10px;"><strong>Saddler Haus</strong></td>
<td style="padding:10px;">Sinsa-dong & Seongsu-dong</td>
<td style="padding:10px;">7,000–10,000 KRW</td>
<td style="padding:10px;">Premium packaging, innovative flavor variations. Gift-worthy.</td>
</tr>
<tr style="border-bottom:1px solid #333;">
<td style="padding:10px;"><strong>Kelly Green</strong></td>
<td style="padding:10px;">Mangwon-dong, Mapo-gu</td>
<td style="padding:10px;">5,500–7,000 KRW</td>
<td style="padding:10px;">Cozy neighborhood bakery with loyal following.</td>
</tr>
</tbody>
</table>
</div>

<h3>Department Store and Hotel Versions</h3>

<p>Major department stores have jumped on the trend with their own premium versions. Shinsegae Gangnam and Lotte Department Store both feature rotating pop-up dujjonku counters from popular bakeries. Several luxury hotels, including the JW Marriott Seoul and Grand Hyatt, have added dujjonku to their patisserie menus — expect to pay a premium (10,000–15,000 KRW) but skip the street-level lines.</p>

<h3>Convenience Store Options (Budget-Friendly)</h3>

<p>If you cannot face a 2-hour wait, Korean convenience stores offer surprisingly decent alternatives:</p>

<ul>
<li><strong>CU</strong>: Their "Kataifi Chocolate Chewy Rice Cake" launched in October 2025 and has sold over 1.8 million units. Also offers a Dubai Chocolate Brownie and Kataifi Chewy Macaron. Check the PocketCU app for preorders.</li>
<li><strong>GS25</strong>: Dubai-related dessert sales jumped 144.9% month-over-month in January 2026. Multiple Dubai-inspired items available.</li>
<li><strong>7-Eleven</strong>: Offers its own Dubai chewy cookie variations at the most budget-friendly prices (2,500–3,500 KRW).</li>
</ul>

<p>For more on what Korean convenience stores offer, check out our <a href="/korean-convenience-store-food-ranking-top-20-must-try-items-at-cu-gs25-and-7-eleven/">Korean Convenience Store Food Ranking: Top 20 Must-Buy Items</a>.</p>

<h3>Franchise and Chain Cafe Versions</h3>

<p>Even Starbucks Korea released a Dubai-inspired seasonal item. Twosome Place, Ediya, and other major Korean cafe chains have all launched their own dujjonku-style cookies, though purists insist the independent bakery versions are superior. These chain versions typically cost 4,500–6,500 KRW and are widely available without waiting.</p>

<h3>Tips for Actually Getting One</h3>

<ul>
<li><strong>Go on weekday mornings</strong> — arrive right at opening time (usually 10 or 11 AM) for the best chances.</li>
<li><strong>Use the real-time stock map</strong> — search "dujjonku map" (두쫑쿠 지도) on Naver for live inventory tracking.</li>
<li><strong>Try preorder apps</strong> — CU's PocketCU and Baedal Minjok both support preordering at select locations.</li>
<li><strong>Check department store pop-ups</strong> — these rotate weekly and often have shorter lines than standalone bakeries.</li>
<li><strong>Avoid weekends entirely</strong> — wait times can exceed 2 hours at popular spots on Saturday and Sunday.</li>
</ul>

<h2>Flavor Guide: Beyond the Original Pistachio</h2>

<p>While the classic pistachio-kataifi-marshmallow combination remains the most popular, Korean bakeries have developed an impressive range of variations. Here is our ranking of the best flavors to try.</p>

<h3>Tier 1: Must-Try</h3>

<p><strong>Original Pistachio (오리지널 피스타치오)</strong> — The classic that started it all. Rich pistachio cream, crunchy kataifi, stretchy marshmallow, cocoa dust. If you only try one, make it this.</p>

<p><strong>Matcha (말차)</strong> — Matcha cream replaces pistachio for a bittersweet, earthy twist. The green color is even more dramatic in pull-apart photos, and the slight bitterness pairs beautifully with the sweet marshmallow.</p>

<p><strong>Injeolmi (인절미)</strong> — A uniquely Korean variation using roasted soybean powder (<em>konggaru</em>) and rice cake filling. The flavor evokes the traditional Korean rice cake of the same name, bridging Dubai chocolate with Korean heritage desserts.</p>

<h3>Tier 2: Worth Seeking Out</h3>

<p><strong>Biscoff (비스코프)</strong> — Cookie butter cream filling with kataifi. Sweeter and more caramel-forward than the original, this version appeals to those who find pistachio too nutty.</p>

<p><strong>Strawberry (딸기)</strong> — Seasonal fresh strawberry versions appear in spring with freeze-dried strawberry pieces mixed into the cream. Lighter and more fruity than the original.</p>

<p><strong>Yellow Cheese (옐로치즈)</strong> — A savory-sweet combination that sounds strange but works surprisingly well. Cream cheese filling with a hint of salt cuts through the sweetness.</p>

<h3>Tier 3: Adventurous</h3>

<p><strong>Black Sesame (흑임자)</strong> — Deep, nutty, and distinctly Korean. An acquired taste but beloved by local food critics.</p>

<p><strong>Almond (아몬드)</strong> — A nuttier, slightly more affordable alternative to pistachio. Available at bakeries near Seoul National University Station.</p>

<h2>The Cultural Impact: More Than Just a Cookie</h2>

<h3>How Korea Transforms Global Trends</h3>

<p>The dujjonku story perfectly illustrates how South Korea does not simply adopt global food trends — it transforms them. The country has a long history of taking international concepts and creating something entirely new and often superior. Korean fried chicken took American fried chicken and added double-frying techniques and creative sauces. Korean street food evolved from simple market snacks into an art form. Dujjonku follows the same pattern: taking a Dubai chocolate bar and reimagining it as something uniquely Korean.</p>

<p>For more on Korea's incredible food innovation, explore our <a href="/the-ultimate-guide-to-korean-street-food-15-must-try-snacks-and-where-to-find-them/">Ultimate Guide to Korean Street Food: 15 Must-Try Snacks</a>.</p>

<h3>The Economics of Viral Food</h3>

<p>Dujjonku reshaped how small businesses operate in Korea. Tiny neighborhood bakeries that previously served a handful of customers suddenly faced thousands of daily visitors. Some adapted by switching to online-only sales, while others imposed strict purchase limits — typically 2 cookies per person.</p>

<p>The pistachio price crisis forced bakeries to absorb costs or raise prices. Some switched to alternative nuts (almonds, hazelnuts) to offer more affordable versions. The weaker Korean won compounded the problem, as most pistachios are imported from the United States and Iran.</p>

<h3>Korea's Viral Food Cycle</h3>

<p>Korea has a well-documented pattern of viral food trends that burn incredibly bright and then fade. Honey butter chips (2014), <em>tanghulu</em> candied fruit (2023-2024), and <em>croffles</em> (2021) all followed similar trajectories. Dujjonku is the latest in this cycle — peaking in late 2025 through early 2026 before gradually becoming a mainstream dessert option rather than a phenomenon.</p>

<p>By March 2026, the lines have shortened significantly, and the cookie has become widely available at convenience stores and chain cafes. This actually makes it the perfect time to try dujjonku — you get the quality without the 2-hour wait.</p>

<h3>Going Global: Dujjonku Reaches Dubai</h3>

<p>In a delicious irony, the Korean-made Dubai chewy cookie has traveled back to the Middle Eastern city that inspired its name. Korean bakeries have opened pop-ups in Dubai, and the Korean version has been featured in Dubai food media. The full circle moment — from Dubai chocolate bar to Korean cookie to Dubai pop-up — perfectly captures how food trends move in our connected world.</p>

<h2>Online Ordering and International Shipping</h2>

<p>For those who cannot visit Seoul, here are your options for getting dujjonku delivered.</p>

<h3>Domestic Delivery (Within Korea)</h3>

<p><strong>Baedal Minjok (배달의민족)</strong> and <strong>Coupang Eats</strong> both offer dujjonku delivery from select bakeries in Seoul. Delivery times and availability vary — popular bakeries often sell out by noon even for delivery orders. Coupang's marketplace also carries packaged versions from various brands.</p>

<p><strong>PocketCU</strong> (CU's preorder app) allows you to reserve convenience store dujjonku items for pickup, which is the most reliable budget option.</p>

<h3>International Options</h3>

<p>As of March 2026, direct international shipping of fresh dujjonku remains limited due to the cookie's short shelf life (typically 2-3 days for optimal texture). However, some Korean food export services on platforms like <strong>Creatrip</strong> and <strong>KoreanMall</strong> offer packaged, longer-shelf-life versions that can be shipped internationally.</p>

<p>DIY kits — including Korean pistachio cream, kataifi pastry, and recipe cards — are also available through Amazon and specialty Korean food import shops. These let you recreate the experience at home, though results will vary based on your baking skills.</p>

<h2>How to Eat Dujjonku Like a Local</h2>

<p>There is actually an art to eating dujjonku properly. Here are tips from Seoul food insiders.</p>

<p><strong>The pull-apart</strong>: Before taking your first bite, gently pull the cookie apart from the center. This is not just for photos — it lets you see (and smell) the filling, and creates the perfect ratio of cookie edge to gooey center in each piece.</p>

<p><strong>Temperature matters</strong>: Dujjonku is best eaten slightly warm. If you bought it earlier and it has cooled, 10 seconds in the microwave restores the stretch. Do not overheat or the marshmallow becomes too liquid.</p>

<p><strong>Pair with coffee</strong>: Koreans typically pair dujjonku with an iced Americano — the bitterness of black coffee perfectly balances the cookie's sweetness. A latte works too, but avoid sweet drinks that compound the sugar overload.</p>

<p><strong>Do not wait</strong>: Dujjonku is best consumed within a few hours of purchase. By the next day, the kataifi loses its crunch and the marshmallow firms up. If you must save it, store at room temperature (not refrigerated) in an airtight container.</p>

<h2>Dujjonku Near Popular Tourist Areas</h2>

<p>If you are visiting Seoul as a tourist, here is where to find dujjonku near major tourist districts.</p>

<p><strong>Myeongdong</strong>: Several bakeries and department store basement food halls offer dujjonku within walking distance. While you are in the area, check out our <a href="/myeongdong-street-food-map-the-12-best-stalls-with-exact-locations-2026/">Myeongdong Street Food Map: 12 Best Stalls</a> for more food finds.</p>

<p><strong>Hongdae/Hapjeong</strong>: All The Ugly Cookie's Hapjeong location (45 Tojeong-ro, Mapo-gu) is a short walk from Hongdae's main shopping area. Combine your cookie hunt with the neighborhood's famous cafe culture.</p>

<p><strong>Gangnam/Sinsa</strong>: Saddler Haus in Sinsa-dong and Shinsegae Department Store in Gangnam are both excellent options. Garosu-gil's trendy cafes also feature various dujjonku interpretations.</p>

<p><strong>Seongsu</strong>: Often called Seoul's Brooklyn, Seongsu-dong is ground zero for the artisan cookie scene. Multiple bakeries within walking distance of each other make it easy to compare versions. All The Ugly Cookie's Seongsu branch is here too.</p>

<p><strong>Gwangjang Market area</strong>: After exploring the legendary food stalls (see our <a href="/gwangjang-market-food-guide-seouls-oldest-market-and-its-legendary-eats/">Gwangjang Market Food Guide</a>), several nearby bakeries in the Jongno area offer dujjonku.</p>

<h2>Is the Dujjonku Trend Over? What to Expect in 2026</h2>

<p>By March 2026, the most intense phase of the dujjonku craze has passed. The sunrise queues are mostly gone, and the cookie is now widely available at convenience stores and chain cafes. But this does not mean the trend is dead — far from it.</p>

<p>Dujjonku has transitioned from "impossible to find" to "established Korean dessert." Similar to how <em>tanghulu</em> went from viral sensation to permanent street food fixture, dujjonku has earned a lasting place in Korea's dessert landscape. Premium bakeries continue to innovate with seasonal flavors, and the quality of widely available versions keeps improving.</p>

<p>For food tourists, this is actually the ideal moment. You get to experience a genuinely innovative Korean dessert without the frustration of multi-hour waits. The pistachio supply has stabilized, prices have come down from their January peak, and bakeries have perfected their recipes after months of practice.</p>

<p>If you are visiting Seoul for the cherry blossoms or spring travel season, adding dujjonku to your food itinerary is a no-brainer. It is a perfect example of how Korea takes global trends and makes them distinctly its own — which, really, is the story of Korean culture itself.</p>

<p>Looking for more Seoul food adventures? Do not miss our guide to <a href="/seouls-hidden-alley-restaurants-7-places-only-locals-know-about/">Seoul's Hidden Alley Restaurants: 7 Places Only Locals Know</a>.</p>

<h2>Frequently Asked Questions</h2>

<h3>What does dujjonku mean?</h3>
<p>Dujjonku (두쫑쿠) is a Korean abbreviation of "Dubai jjondeukhada cookie" (두바이 쫀득 쿠키), meaning "Dubai chewy cookie." The word <em>jjondeukhada</em> (쫀득하다) describes a stretchy, chewy texture unique to Korean food vocabulary.</p>

<h3>How much does a dujjonku cost?</h3>
<p>Prices range from 2,500 KRW ($2 USD) for convenience store versions to 5,500–10,000 KRW ($4–8 USD) at specialty bakeries. Hotel and department store versions can cost up to 15,000 KRW ($12 USD). The most popular bakery versions typically cost around 6,500–7,500 KRW ($5–6 USD).</p>

<h3>Where is the best place to buy dujjonku in Seoul?</h3>
<p>Mont Cookie is credited as the original creator and remains a top choice. All The Ugly Cookie in Hapjeong/Seongsu is famous for its rich filling and rustic style. For convenience, CU and GS25 convenience stores offer surprisingly good budget versions. Department store pop-ups at Shinsegae and Lotte offer premium versions with shorter wait times.</p>

<h3>Can I order dujjonku online for international delivery?</h3>
<p>Fresh dujjonku has a short shelf life (2-3 days optimal), making international shipping difficult. However, packaged versions with extended shelf life are available through Korean food export platforms like Creatrip and KoreanMall. DIY ingredient kits can also be ordered through Amazon.</p>

<h3>Is dujjonku the same as Dubai chocolate?</h3>
<p>No. The original Dubai chocolate is a thin chocolate bar filled with pistachio cream and kataifi pastry, created by Fix Dessert Chocolatier in Dubai. Dujjonku is a Korean reimagination that puts those same flavors inside a thick, chewy cookie with added marshmallow — creating an entirely different texture and eating experience.</p>

<h3>What flavors of dujjonku are available?</h3>
<p>The original pistachio is most popular, but Korean bakeries offer many variations including matcha, injeolmi (roasted soybean), Biscoff, strawberry, yellow cheese, black sesame, and almond. Seasonal limited editions appear regularly at specialty bakeries.</p>

<h3>Do I need to wait in line for dujjonku?</h3>
<p>As of March 2026, the extreme lines have mostly subsided. Weekday mornings at popular bakeries may require 15-30 minute waits, but convenience store and chain cafe versions are widely available without any wait. Weekend afternoons at famous spots like Mont Cookie or All The Ugly Cookie may still see 30-60 minute lines.</p>

<h3>Is dujjonku halal?</h3>
<p>Most standard dujjonku recipes use gelatin-based marshmallow, which may not be halal. Some bakeries offer halal-certified versions — check with the specific bakery before purchasing. Convenience store versions typically list ingredients on the packaging for verification.</p>

<!-- You Might Also Enjoy -->
<div style="background:#f9f5f0;padding:24px;border-radius:12px;margin:32px 0;">
<h3 style="margin-top:0;color:#2a1a0a;">You Might Also Enjoy</h3>
<ul style="list-style:none;padding:0;">
<li style="margin-bottom:12px;">🍜 <a href="/the-ultimate-guide-to-korean-street-food-15-must-try-snacks-and-where-to-find-them/" style="color:#8B4513;font-weight:600;">The Ultimate Guide to Korean Street Food: 15 Must-Try Snacks</a></li>
<li style="margin-bottom:12px;">🏪 <a href="/korean-convenience-store-food-ranking-top-20-must-try-items-at-cu-gs25-and-7-eleven/" style="color:#8B4513;font-weight:600;">Korean Convenience Store Food Ranking: Top 20 Must-Buy Items</a></li>
<li style="margin-bottom:12px;">🍻 <a href="/korean-drinking-food-anju-the-best-bar-snacks-to-order-with-soju-and-beer/" style="color:#8B4513;font-weight:600;">Korean Anju Guide: Best Bar Snacks with Soju & Beer</a></li>
</ul>
</div>

<!-- FAQ Schema JSON-LD -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What does dujjonku mean?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Dujjonku (두쫑쿠) is a Korean abbreviation of 'Dubai jjondeukhada cookie' (두바이 쫀득 쿠키), meaning 'Dubai chewy cookie.' The word jjondeukhada (쫀득하다) describes a stretchy, chewy texture unique to Korean food vocabulary."
      }
    },
    {
      "@type": "Question",
      "name": "How much does a dujjonku cost?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Prices range from 2,500 KRW ($2 USD) for convenience store versions to 5,500–10,000 KRW ($4–8 USD) at specialty bakeries. Hotel and department store versions can cost up to 15,000 KRW ($12 USD)."
      }
    },
    {
      "@type": "Question",
      "name": "Where is the best place to buy dujjonku in Seoul?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Mont Cookie is credited as the original creator. All The Ugly Cookie in Hapjeong/Seongsu is famous for its rich filling. CU and GS25 convenience stores offer good budget versions. Department store pop-ups at Shinsegae and Lotte offer premium versions with shorter waits."
      }
    },
    {
      "@type": "Question",
      "name": "Can I order dujjonku online for international delivery?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Fresh dujjonku has a short shelf life (2-3 days), making international shipping difficult. Packaged versions are available through Korean food export platforms like Creatrip and KoreanMall. DIY ingredient kits can be ordered through Amazon."
      }
    },
    {
      "@type": "Question",
      "name": "Is dujjonku the same as Dubai chocolate?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "No. The original Dubai chocolate is a thin chocolate bar by Fix Dessert Chocolatier. Dujjonku is a Korean reimagination that puts those flavors inside a thick, chewy cookie with marshmallow, creating an entirely different texture."
      }
    },
    {
      "@type": "Question",
      "name": "What flavors of dujjonku are available?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "The original pistachio is most popular, but variations include matcha, injeolmi (roasted soybean), Biscoff, strawberry, yellow cheese, black sesame, and almond. Seasonal limited editions appear regularly."
      }
    },
    {
      "@type": "Question",
      "name": "Do I need to wait in line for dujjonku?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "As of March 2026, extreme lines have mostly subsided. Weekday mornings may require 15-30 minute waits at popular bakeries, but convenience store versions are available without any wait."
      }
    },
    {
      "@type": "Question",
      "name": "Is dujjonku halal?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Most standard recipes use gelatin-based marshmallow which may not be halal. Some bakeries offer halal-certified versions. Check with the specific bakery before purchasing."
      }
    }
  ]
}
</script>
"""

EXCERPT = "Dujjonku (두쫑쿠) is Korea's viral Dubai chocolate cookie — a chewy, stretchy masterpiece filled with pistachio cream, kataifi, and marshmallow. Here's where to buy it in Seoul, the best flavors to try, and how a K-pop post turned a cookie into a national obsession."

TAGS = [
    "dujjonku", "dubai chocolate cookie", "korean dessert", "seoul food",
    "korean food trend", "dubai chewy cookie", "where to buy dujjonku",
    "seoul bakery", "korean street food", "tiktok food trend",
    "pistachio cookie", "korea travel", "korean cafe", "viral food"
]

# ─── 3. WordPress Publishing ──────────────────────────────────────────────────

def publish():
    SITE = "https://rhythmicaleskimo.com"
    REST = f"{SITE}/wp-json/wp/v2"

    # Login
    s = requests.Session()
    s.cookies.set("wordpress_test_cookie", "WP+Cookie+check")
    login_resp = s.post(f"{SITE}/wp-login.php", data={
        "log": "cjy654377@gmail.com",
        "pwd": "Dkflekd1!!",
        "wp-submit": "Log In",
        "redirect_to": "/wp-admin/",
        "testcookie": "1"
    }, allow_redirects=True)
    print(f"Login status: {login_resp.status_code}")

    # Get nonce
    page = s.get(f"{SITE}/wp-admin/post-new.php").text
    m = re.search(r'"nonce":"([a-f0-9]+)"', page)
    if not m:
        print("ERROR: Could not find nonce")
        sys.exit(1)
    nonce = m.group(1)
    h = {"X-WP-Nonce": nonce}
    print(f"Nonce obtained: {nonce[:8]}...")

    # Create or get tags
    tag_ids = []
    for tag_name in TAGS:
        # Check if tag exists
        resp = s.get(f"{REST}/tags", params={"search": tag_name}, headers=h)
        existing = [t for t in resp.json() if t["name"].lower() == tag_name.lower()]
        if existing:
            tag_ids.append(existing[0]["id"])
        else:
            resp = s.post(f"{REST}/tags", json={"name": tag_name}, headers=h)
            if resp.status_code == 201:
                tag_ids.append(resp.json()["id"])
            else:
                print(f"  Warning: Could not create tag '{tag_name}': {resp.status_code}")
    print(f"Tags ready: {len(tag_ids)} tags")

    # Upload featured image
    img_path = "/Users/choijooyong/wordpress/featured_dujjonku.png"
    with open(img_path, "rb") as f:
        img_resp = s.post(
            f"{REST}/media",
            headers={**h, "Content-Disposition": "attachment; filename=featured_dujjonku.png"},
            files={"file": ("featured_dujjonku.png", f, "image/png")},
            data={
                "alt_text": "Dujjonku Dubai Chocolate Cookie Korea - Where to Buy in Seoul 2026",
                "caption": "Dujjonku: Korea's viral Dubai chocolate cookie taking over TikTok"
            }
        )
    if img_resp.status_code == 201:
        media_id = img_resp.json()["id"]
        print(f"Featured image uploaded: ID {media_id}")
    else:
        print(f"Image upload failed: {img_resp.status_code} {img_resp.text[:200]}")
        media_id = None

    # Publish post
    post_data = {
        "title": "Dujjonku: Korea's Viral Dubai Chocolate Cookie Taking Over TikTok [Where to Buy in 2026]",
        "content": ARTICLE_HTML,
        "excerpt": EXCERPT,
        "status": "publish",
        "categories": [87],  # Korea Travel & Food
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
        print(f"Publish failed: {resp.status_code}")
        print(resp.text[:500])


if __name__ == "__main__":
    print("=" * 60)
    print("Generating featured image...")
    generate_featured_image()
    print("=" * 60)
    print("Publishing article...")
    publish()
    print("=" * 60)
