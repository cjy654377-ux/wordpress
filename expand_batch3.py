#!/usr/bin/env python3
"""Expand thin posts batch 3: ID 65, 67, 69"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import login, REST

BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE, "template.html")) as f:
    template = f.read()

# ============================================================
# POST 65: Korean Convenience Store Food Ranking
# ============================================================
article_65 = """
<h2>Why Korean Convenience Stores Are a Food Destination</h2>

<p>Korean convenience stores are nothing like their Western counterparts. While 7-Eleven in the United States sells stale hot dogs and overpriced sodas, Korean convenience stores — CU, GS25, 7-Eleven Korea, and Emart24 — are legitimate dining destinations. There are over 54,000 convenience stores in South Korea, roughly one for every 950 people, and they serve as cafeterias for office workers, late-night kitchens for students, and emergency restaurants for travelers.</p>

<p>Every store has a microwave, hot water dispenser, and eating area (often with USB charging). Many have outdoor seating where Koreans sit for hours eating ramen, drinking beer, and socializing. The food is fresh (most items are made daily and pulled from shelves after 24-48 hours), surprisingly high quality, and absurdly cheap — you can eat a full meal for under ₩5,000 ($3.70 USD).</p>

<h2>Top 20 Must-Try Items</h2>

<div style="overflow-x:auto;margin:15px 0;">
<table class="rk-tbl" style="min-width:600px;">
<thead><tr><th>#</th><th>Item</th><th>Korean</th><th>Price</th><th>Chain</th><th>Notes</th></tr></thead>
<tbody>
<tr><td>1</td><td>Triangle Kimbap</td><td>삼각김밥</td><td>₩1,000-1,500</td><td>All</td><td>Rice triangle, various fillings. Tuna mayo is the bestseller</td></tr>
<tr><td>2</td><td>Cup Ramyeon</td><td>컵라면</td><td>₩1,200-2,000</td><td>All</td><td>Add hot water, wait 3 min. Shin Ramyeon is spiciest</td></tr>
<tr><td>3</td><td>Cheese Buldak Noodles</td><td>치즈불닭</td><td>₩1,800</td><td>All</td><td>Viral fire noodles + cheese powder. Dangerously spicy</td></tr>
<tr><td>4</td><td>Egg Sandwich</td><td>에그샌드위치</td><td>₩2,500-3,000</td><td>All</td><td>Japanese-style fluffy egg sandwich. Fresh daily</td></tr>
<tr><td>5</td><td>Dosirak (Lunchbox)</td><td>도시락</td><td>₩3,500-5,000</td><td>All</td><td>Full meals: rice + 3-4 side dishes + meat. Microwave it</td></tr>
<tr><td>6</td><td>Corn Dog</td><td>핫도그</td><td>₩1,500-2,000</td><td>All</td><td>Korean corn dog with cheese/sausage, coated in batter</td></tr>
<tr><td>7</td><td>Banana Milk</td><td>바나나맛 우유</td><td>₩1,500</td><td>All</td><td>Binggrae's iconic drink since 1974. Cult classic</td></tr>
<tr><td>8</td><td>Yakult (Large)</td><td>야쿠르트</td><td>₩1,000</td><td>All</td><td>Probiotic drink, frozen version is a summer treat</td></tr>
<tr><td>9</td><td>Tteokbokki Cup</td><td>떡볶이컵</td><td>₩2,000-2,500</td><td>CU, GS25</td><td>Instant spicy rice cakes, add hot water</td></tr>
<tr><td>10</td><td>Samgak-jeon (Pancake)</td><td>삼각전</td><td>₩1,200</td><td>CU</td><td>Triangle-shaped savory pancake, unique to CU</td></tr>
<tr><td>11</td><td>Ice Cream: Melona</td><td>메로나</td><td>₩1,000</td><td>All</td><td>Honeydew melon ice cream bar. Korea's summer icon</td></tr>
<tr><td>12</td><td>Ice Cream: Pigbar</td><td>돼지바</td><td>₩1,200</td><td>All</td><td>Strawberry + vanilla ice cream, pig-shaped, nostalgic</td></tr>
<tr><td>13</td><td>GS25 Fresh Sushi</td><td>스시</td><td>₩3,000-4,500</td><td>GS25</td><td>Surprisingly good quality for the price</td></tr>
<tr><td>14</td><td>CU Baekjongwon Dosirak</td><td>백종원 도시락</td><td>₩4,500</td><td>CU</td><td>Celebrity chef collab lunchbox, premium quality</td></tr>
<tr><td>15</td><td>Paldo Bibimmyeon</td><td>팔도비빔면</td><td>₩1,300</td><td>All</td><td>Cold spicy-sweet noodles. Perfect summer snack</td></tr>
<tr><td>16</td><td>Soju (bottle)</td><td>소주</td><td>₩1,800</td><td>All</td><td>Cheapest alcohol purchase in Korea</td></tr>
<tr><td>17</td><td>Buldak Mayo Onigiri</td><td>불닭마요 주먹밥</td><td>₩1,500</td><td>All</td><td>Fire chicken mayo rice ball, perfect heat level</td></tr>
<tr><td>18</td><td>Honey Butter Chips</td><td>허니버터칩</td><td>₩1,800</td><td>All</td><td>Sweet-salty chips that caused a shortage in 2014</td></tr>
<tr><td>19</td><td>Cafe Latte (bottled)</td><td>카페라떼</td><td>₩1,800-2,500</td><td>All</td><td>Maeil, Seoul Milk brands. Solid quality</td></tr>
<tr><td>20</td><td>Emart24 Cheeseburger</td><td>치즈버거</td><td>₩2,500</td><td>Emart24</td><td>Best convenience store burger, microwaved</td></tr>
</tbody>
</table>
</div>

<h2>Chain Exclusives: What to Get Where</h2>

<div style="overflow-x:auto;margin:15px 0;">
<table class="rk-tbl" style="min-width:500px;">
<thead><tr><th>Chain</th><th>Stores</th><th>Exclusive Must-Try</th><th>Strength</th></tr></thead>
<tbody>
<tr><td><strong>CU</strong></td><td>17,000+</td><td>Baekjongwon collabs, GET coffee</td><td>Most stores, best lunchboxes</td></tr>
<tr><td><strong>GS25</strong></td><td>16,500+</td><td>Fresh sushi, Cafe25 coffee</td><td>Best prepared foods, fresh items</td></tr>
<tr><td><strong>7-Eleven</strong></td><td>13,000+</td><td>7-Select snacks, import drinks</td><td>International items, tourist areas</td></tr>
<tr><td><strong>Emart24</strong></td><td>6,000+</td><td>Cheeseburger, craft beer selection</td><td>Best alcohol selection, burgers</td></tr>
</tbody>
</table>
</div>

<h2>How to Use Korean Convenience Stores</h2>

<ol>
<li><strong>Hot water:</strong> Every store has a free hot water dispenser near the microwave. Use it for cup ramen and instant tteokbokki.</li>
<li><strong>Microwave:</strong> Free to use. Most dosirak (lunchboxes) and burgers need 2-3 minutes. Staff will help if you cannot read Korean buttons.</li>
<li><strong>Payment:</strong> All stores accept credit/debit cards and T-money (transportation card). Cash also works. Apple Pay and Samsung Pay accepted at most.</li>
<li><strong>Seating:</strong> Look for stools and counters along windows. Outdoor seating is common. Some stores have second-floor eating areas.</li>
<li><strong>1+1 deals:</strong> "1+1" (one plus one) means buy one get one free. "2+1" means buy two get one free. These deals rotate weekly and are genuinely excellent value.</li>
<li><strong>Seasonal items:</strong> Limited-edition seasonal items (cherry blossom drinks in spring, sweet potato snacks in autumn) are worth seeking out.</li>
</ol>

<div class="rk-hl">
<strong>Budget traveler tip:</strong> You can eat three meals a day from Korean convenience stores for under ₩15,000 ($11 USD) — triangle kimbap breakfast (₩1,500), dosirak lunch (₩4,500), cup ramen + banana milk dinner (₩3,200). Not the healthiest week of your life, but your wallet will thank you.
</div>

<h2>Late-Night Convenience Store Culture</h2>

<p>Korean convenience stores are open 24/7, and after midnight they transform into social hubs. College students study there, couples share late-night snacks, and groups of friends sit outside with soju and dried squid from the shelves. The convenience store is Korea's unofficial third place — not home, not work, but somewhere in between.</p>

<p>For more budget eating options, check our <a href="https://rhythmicaleskimo.com/budgets-meals-in-korea-10-tv-featured-restaurants-where-you-can-eat-for-under-7/">Budget Meals Under $7 Guide</a>. Explore Korea's best street food in our <a href="https://rhythmicaleskimo.com/the-ultimate-guide-to-korean-street-food-15-must-try-snacks-and-where-to-find-them/">Ultimate Street Food Guide</a>. And pair your convenience store soju with proper anju from our <a href="https://rhythmicaleskimo.com/soju-guide-for-beginners-how-to-drink-koreas-national-spirit-like-a-local/">Soju Beginner's Guide</a>.</p>

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Are Korean convenience stores open 24 hours?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes. CU, GS25, 7-Eleven Korea, and Emart24 are open 24/7. They have microwaves, hot water dispensers, and seating areas available at all hours."
      }
    },
    {
      "@type": "Question",
      "name": "What is the cheapest meal at a Korean convenience store?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "A triangle kimbap (₩1,000-1,500) is the cheapest filling option. A cup ramyeon with hot water costs ₩1,200-2,000. A full dosirak lunchbox with rice and side dishes is ₩3,500-5,000."
      }
    },
    {
      "@type": "Question",
      "name": "Can I use a credit card at Korean convenience stores?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes. All major convenience stores accept credit/debit cards, T-money (transportation card), and mobile payments (Apple Pay, Samsung Pay). Cash is also accepted."
      }
    }
  ]
}
</script>
"""

# ============================================================
# POST 67: Jeju Island Food Guide
# ============================================================
article_67 = """
<h2>Why Jeju Food Is Unlike Anything Else in Korea</h2>

<p>Jeju Island (제주도) is Korea's volcanic tropical paradise — a UNESCO World Heritage site floating 80 kilometers off the southern coast. But beyond the lava tubes, tangerine orchards, and dramatic coastline, Jeju has a food culture that is genuinely unique in Korea. The island's volcanic soil, surrounding ocean waters, and centuries of isolation from the mainland created a cuisine that mainland Koreans travel specifically to experience.</p>

<p>Jeju's food story is shaped by three factors: the haenyeo (해녀, female free-divers who harvest seafood without equipment), the island's famous black pigs raised on volcanic grasslands, and subtropical ingredients like hallabong tangerines and cactus fruit that simply do not grow on the mainland. Many Jeju dishes cannot be replicated anywhere else because the ingredients are literally unavailable outside the island.</p>

<h2>The 7 Essential Jeju Dishes</h2>

<h3>1. Heuk-dwaeji (흑돼지) — Jeju Black Pork</h3>

<p>Jeju black pork is the island's signature dish and the reason many Koreans make the trip. These small, native black pigs have been raised on Jeju for centuries, fed on volcanic grassland and a diet that includes tangerine peels. The result is meat that is darker, more marbled, and more intensely flavored than mainland pork.</p>

<p><strong>Where to eat:</strong> Dombe Gogi Street (돔베고기 거리) near Jeju City, or the famous Black Pork Street (흑돼지 거리) in Seogwipo. Expect to pay ₩15,000-22,000 per serving (200g) for genuine Jeju black pork grilled at your table.</p>

<h3>2. Jeonbok-juk (전복죽) — Abalone Porridge</h3>

<p>Fresh abalone harvested by haenyeo divers is simmered with rice into a creamy, ocean-green porridge. The color comes from the abalone's innards, which dissolve during cooking and create a naturally rich, umami-heavy broth. This is the quintessential Jeju breakfast — comforting, nutritious, and a taste you will not find on the mainland.</p>

<p><strong>Where to eat:</strong> O'sulloc Tea Museum area restaurants or Myeongjin Jeonbok (명진전복) chain. Price: ₩12,000-18,000 per bowl.</p>

<h3>3. Galchi-jorim (갈치조림) — Braised Hairtail Fish</h3>

<p>Jeju's waters produce Korea's finest galchi (hairtail/cutlass fish) — silver, serpentine fish that are braised in a spicy red sauce with radish and potatoes. The flesh is delicate and flaky, and the sauce is intensely flavorful. Galchi is available on the mainland, but Jeju galchi is noticeably fresher and larger.</p>

<p><strong>Where to eat:</strong> Jungmun area seafood restaurants or Dongmun Market stalls. Price: ₩15,000-25,000.</p>

<h3>4. Haemul-ttukbaegi (해물뚝배기) — Seafood Hot Pot</h3>

<p>A bubbling stone pot filled with whatever the haenyeo caught that morning — abalone, sea urchin, octopus, conch, and various shellfish in a clear, briny broth. Every restaurant's version is slightly different depending on the day's catch.</p>

<p><strong>Where to eat:</strong> Coastal restaurants near Hallim or Seongsan, especially near haenyeo diving spots. Price: ₩15,000-30,000.</p>

<h3>5. Hallabong (한라봉) — Jeju Tangerines</h3>

<p>Hallabong are Jeju's famous seedless tangerines with a distinctive bump on top (named after Hallasan mountain). They are intensely sweet, easy to peel, and available from December through March. Hallabong juice, hallabong chocolate, hallabong makgeolli, and hallabong everything can be found across the island.</p>

<p><strong>Where to buy:</strong> Any roadside stand or Dongmun Market. Price: ₩5,000-10,000 per bag (about 8-10 fruits). Buy directly from farms for the freshest.</p>

<h3>6. Jeju Makgeolli (제주 막걸리)</h3>

<p>Jeju's makgeolli (traditional rice wine) is made with the island's volcanic spring water and often infused with local ingredients — hallabong, cactus fruit (baeknyeoncho), or even carrot. It pairs perfectly with Jeju seafood pancakes (haemul-pajeon) and is served at virtually every restaurant.</p>

<p><strong>Must try:</strong> Jeju Wit Ale (제주 위트 에일) from Jeju Beer — Korea's best craft brewery, founded on the island.</p>

<h3>7. Heuk-tang (흑돼지 국수) — Black Pork Noodle Soup</h3>

<p>A simple, deeply satisfying bowl of handmade noodles in a pork bone broth made from — you guessed it — Jeju black pig bones. The broth is milky white and rich, the noodles are chewy, and slices of black pork sit on top. This is Jeju's comfort food.</p>

<p><strong>Where to eat:</strong> Gogi Guksu (고기국수) restaurants throughout the island. Price: ₩8,000-10,000.</p>

<h2>Price Guide: What to Budget</h2>

<div style="overflow-x:auto;margin:15px 0;">
<table class="rk-tbl" style="min-width:500px;">
<thead><tr><th>Meal Type</th><th>Price Range</th><th>Example</th></tr></thead>
<tbody>
<tr><td>Budget meal</td><td>₩8,000-10,000</td><td>Gogi guksu, kimbap, market food</td></tr>
<tr><td>Mid-range meal</td><td>₩12,000-18,000</td><td>Abalone porridge, galchi-jorim</td></tr>
<tr><td>Premium meal</td><td>₩20,000-35,000</td><td>Black pork BBQ, seafood hot pot</td></tr>
<tr><td>Special experience</td><td>₩40,000+</td><td>Haenyeo-caught sashimi platter</td></tr>
</tbody>
</table>
</div>

<h2>Dongmun Market: Jeju's Food Hub</h2>

<p>Dongmun Traditional Market (동문재래시장) in Jeju City is the island's largest and oldest market, operating since 1945. Unlike Seoul's tourist-heavy markets, Dongmun is where locals actually shop. The covered market has over 300 vendors selling fresh seafood, hallabong, dried fish, Jeju specialty snacks, and prepared foods.</p>

<p><strong>Must-try at Dongmun:</strong></p>
<ul>
<li>Fresh tangerine juice (₩3,000) — squeezed in front of you</li>
<li>Grilled black pork skewers (₩5,000)</li>
<li>Hallabong tart (₩2,000) — buttery pastry with tangerine curd</li>
<li>Raw seafood platter from the fish section (price varies)</li>
</ul>

<h2>Best Food + Sightseeing Combos</h2>

<ul>
<li><strong>Morning:</strong> Abalone porridge breakfast at O'sulloc area → O'sulloc Tea Museum (free) → Innisfree Jeju House</li>
<li><strong>Afternoon:</strong> Black pork lunch at Seogwipo → Jeongbang Waterfall (₩2,000) → Jungmun Beach</li>
<li><strong>Evening:</strong> Dongmun Market street food → Jeju City waterfront walk → craft beer at Jeju Beer Brewery</li>
</ul>

<p>For more regional food adventures, explore our <a href="https://rhythmicaleskimo.com/busan-food-guide-8-dishes-you-can-only-find-in-koreas-coastal-city/">Busan Food Guide</a>. Master restaurant etiquette with our <a href="https://rhythmicaleskimo.com/korean-bbq-etiquette-12-rules-every-first-timer-needs-to-know/">Korean BBQ Etiquette Guide</a>. And learn how to order with our <a href="https://rhythmicaleskimo.com/how-to-order-food-in-korean-25-essential-phrases-every-traveler-needs/">25 Essential Korean Food Phrases</a>.</p>

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is the most famous food on Jeju Island?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Jeju black pork (흑돼지) is the island's most famous dish. These native black pigs are raised on volcanic grassland and have a distinctly richer flavor than mainland pork. Expect to pay ₩15,000-22,000 per serving at BBQ restaurants."
      }
    },
    {
      "@type": "Question",
      "name": "What are hallabong tangerines?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Hallabong are Jeju's signature seedless tangerines with a bump on top (named after Hallasan mountain). They are intensely sweet and available December through March. Buy them at any roadside stand or market for ₩5,000-10,000 per bag."
      }
    },
    {
      "@type": "Question",
      "name": "Is Jeju food expensive?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Budget meals start at ₩8,000 (noodle soup, market food). Mid-range dishes like abalone porridge cost ₩12,000-18,000. Premium black pork BBQ runs ₩20,000-35,000. Jeju is slightly more expensive than the mainland for seafood and specialty items."
      }
    }
  ]
}
</script>
"""

# ============================================================
# POST 69: Korean Drinking Food (Anju)
# ============================================================
article_69 = """
<h2>What Is Anju and Why Koreans Never Drink Without It</h2>

<p>In Korea, drinking without eating is considered bizarre, borderline irresponsible, and frankly un-Korean. The word "anju" (안주) refers specifically to food eaten while drinking alcohol — not before, not after, but during. Every bar, every chicken restaurant, every pojangmacha (포장마차, tent bar) serves anju, and choosing the right one is considered an art form.</p>

<p>The cultural rule is simple: if there is alcohol, there must be food. This is not a suggestion — it is a deeply ingrained social norm. Korean bars do not serve "just drinks." Order a bottle of soju or a round of beer, and the server will ask what anju you want. In many places, you cannot order alcohol without also ordering food.</p>

<h2>The Anju Tier List: From Essential to Legendary</h2>

<div style="overflow-x:auto;margin:15px 0;">
<table class="rk-tbl" style="min-width:600px;">
<thead><tr><th>Tier</th><th>Dish</th><th>Korean</th><th>Price</th><th>Best With</th><th>Description</th></tr></thead>
<tbody>
<tr><td>S</td><td>Samgyeopsal</td><td>삼겹살</td><td>₩15,000-18,000</td><td>Soju</td><td>Grilled pork belly — the ultimate soju partner</td></tr>
<tr><td>S</td><td>Chikin (Fried Chicken)</td><td>치킨</td><td>₩19,000-22,000</td><td>Beer</td><td>The chimaek (chicken + beer) combo that conquered the world</td></tr>
<tr><td>A</td><td>Pajeon</td><td>파전</td><td>₩12,000-15,000</td><td>Makgeolli</td><td>Green onion pancake — the classic rainy-day drinking combo</td></tr>
<tr><td>A</td><td>Jokbal</td><td>족발</td><td>₩30,000-40,000</td><td>Soju</td><td>Braised pig feet, served sliced. Feeds 3-4 people</td></tr>
<tr><td>A</td><td>Dak-bal</td><td>닭발</td><td>₩15,000-18,000</td><td>Soju</td><td>Spicy chicken feet — chewy, fiery, addictive</td></tr>
<tr><td>B</td><td>Ojingeo-gui</td><td>오징어구이</td><td>₩15,000-20,000</td><td>Soju</td><td>Grilled whole squid with gochujang sauce</td></tr>
<tr><td>B</td><td>Dubu-kimchi</td><td>두부김치</td><td>₩12,000-15,000</td><td>Soju</td><td>Stir-fried kimchi with pork served on silken tofu</td></tr>
<tr><td>B</td><td>Nakji-bokkeum</td><td>낙지볶음</td><td>₩15,000-18,000</td><td>Soju</td><td>Spicy stir-fried octopus — intense, sweet-spicy</td></tr>
<tr><td>C</td><td>Dried squid</td><td>마른 오징어</td><td>₩5,000-8,000</td><td>Beer/Soju</td><td>Tear-and-chew strips with mayo. Convenience store classic</td></tr>
<tr><td>C</td><td>Corn cheese</td><td>콘치즈</td><td>₩8,000-10,000</td><td>Beer</td><td>Sweet corn baked with cheese and mayo in a hot skillet</td></tr>
<tr><td>C</td><td>Eomuk-tang</td><td>어묵탕</td><td>₩10,000-12,000</td><td>Soju</td><td>Fish cake soup — warm, comforting, low effort</td></tr>
<tr><td>C</td><td>Golbaengi-muchim</td><td>골뱅이무침</td><td>₩15,000-18,000</td><td>Soju</td><td>Spicy sea snails with noodles — classic Korean bar food</td></tr>
</tbody>
</table>
</div>

<h2>The Perfect Pairings</h2>

<p>Korean drinking culture has specific, well-established food-alcohol pairings. While no one will stop you from mixing them up, these combinations have been refined over generations:</p>

<div style="overflow-x:auto;margin:15px 0;">
<table class="rk-tbl" style="min-width:500px;">
<thead><tr><th>Alcohol</th><th>Best Anju</th><th>Why It Works</th></tr></thead>
<tbody>
<tr><td><strong>Soju</strong></td><td>Samgyeopsal, Jokbal, Dubu-kimchi</td><td>Soju's clean burn cuts through fatty, rich flavors</td></tr>
<tr><td><strong>Beer</strong></td><td>Fried Chicken, Corn Cheese, Dried Squid</td><td>Beer's carbonation refreshes after salty, crispy foods</td></tr>
<tr><td><strong>Makgeolli</strong></td><td>Pajeon, Bindaetteok, Jeon (pancakes)</td><td>Creamy rice wine + crispy pancakes = rainy-day perfection</td></tr>
<tr><td><strong>Somaek (소맥)</strong></td><td>Anything spicy — Dak-bal, Nakji</td><td>The soju-beer mix needs strong flavors to match</td></tr>
</tbody>
</table>
</div>

<h2>Where to Find the Best Anju</h2>

<h3>Pojangmacha (포장마차) — Tent Bars</h3>

<p>Pojangmacha are the orange-tented street bars that line Korean streets after dark. They are the most atmospheric place to eat anju — sitting on plastic stools under a tarp, eating fish cake soup and drinking soju while the city moves around you. Classic pojangmacha anju includes eomuk-tang, tteokbokki, and fried dumplings.</p>

<p><strong>Best areas:</strong> Euljiro (을지로) in Seoul for retro vibes, Gwangjang Market late night, Busan's BIFF Square.</p>

<h3>Hof (호프) — Beer Bars</h3>

<p>A "hof" is a Korean beer bar, descended from German beer halls. Hofs serve pitcher beer and anju like fried chicken, corn cheese, and dried squid. They are the standard after-work drinking spot for Korean office workers.</p>

<h3>Samgyeopsal Restaurants</h3>

<p>Any Korean BBQ restaurant doubles as a drinking destination after 7 PM. Order samgyeopsal, bottles of soju, and settle in for 2-3 hours of grilling, drinking, and conversation.</p>

<h3>Chimaek Restaurants</h3>

<p>Dedicated chicken-and-beer restaurants (치맥집) are everywhere. Order a whole chicken and a few beers — the fried chicken IS the anju. See our <a href="https://rhythmicaleskimo.com/korean-fried-chicken-guide-why-kfc-means-something-different-in-korea/">Korean Fried Chicken Guide</a> for chain recommendations.</p>

<h2>Anju Etiquette and Tips</h2>

<ul>
<li><strong>Order anju first, drinks second.</strong> In many Korean bars, you must order food before they will bring alcohol.</li>
<li><strong>Share everything.</strong> Anju is always communal — order 2-3 dishes for the table and share.</li>
<li><strong>Expect large portions.</strong> Korean anju portions are designed for sharing among 2-4 people. One dish per person is usually too much.</li>
<li><strong>Late-night hours.</strong> Most anju restaurants operate until 2-4 AM. Pojangmacha are open until the early morning.</li>
<li><strong>Budget:</strong> A typical Korean drinking session (2-3 hours, 2 people) with soju, beer, and anju costs ₩30,000-50,000 ($22-37 USD) total.</li>
</ul>

<h2>The Pojangmacha Experience: How to Do It</h2>

<ol>
<li>Look for orange-lit tents along the street after dark (usually 8 PM onwards)</li>
<li>Duck inside and sit on a plastic stool</li>
<li>The ajumma (아주머니) will hand you a menu or just tell you what is available</li>
<li>Order eomuk-tang (fish cake soup, usually comes free or ₩5,000) and your drink</li>
<li>Add more dishes as you go — tteokbokki, fried dumplings, grilled items</li>
<li>Pay cash (many pojangmacha are cash-only)</li>
</ol>

<p>Master Korea's drinking spirit with our <a href="https://rhythmicaleskimo.com/soju-guide-for-beginners-how-to-drink-koreas-national-spirit-like-a-local/">Soju Guide for Beginners</a>. Learn BBQ etiquette in our <a href="https://rhythmicaleskimo.com/korean-bbq-etiquette-12-rules-every-first-timer-needs-to-know/">Korean BBQ Etiquette Guide</a>. And discover more street food in our <a href="https://rhythmicaleskimo.com/the-ultimate-guide-to-korean-street-food-15-must-try-snacks-and-where-to-find-them/">Ultimate Street Food Guide</a>.</p>

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is anju in Korean culture?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Anju (안주) refers to food specifically eaten while drinking alcohol. In Korea, drinking without eating is considered socially unacceptable. Every bar and restaurant that serves alcohol also serves anju, and many require you to order food with your drinks."
      }
    },
    {
      "@type": "Question",
      "name": "What is a pojangmacha?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "A pojangmacha (포장마차) is a Korean tent bar — an orange-tented street stall that serves alcohol and anju. They typically open after dark and operate until early morning. They serve classic anju like fish cake soup, tteokbokki, and grilled items."
      }
    },
    {
      "@type": "Question",
      "name": "How much does a Korean drinking session cost?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "A typical 2-3 hour drinking session for two people with soju, beer, and anju costs ₩30,000-50,000 ($22-37 USD). Pojangmacha is the cheapest option, while samgyeopsal restaurants and chimaek places cost more."
      }
    }
  ]
}
</script>
"""

# ============================================================
# Execute updates
# ============================================================
s, h = login()
print("Logged in.")

updates = [
    (65, article_65, "Convenience Store"),
    (67, article_67, "Jeju Food"),
    (69, article_69, "Anju Guide"),
]

for pid, body, label in updates:
    html = template.replace("{CONTENT}", body)
    r = s.post(f"{REST}/posts/{pid}", headers=h, json={"content": html})
    if r.status_code == 200:
        print(f"  Updated: {label} (ID={pid})")
    else:
        print(f"  FAIL {label}: {r.status_code} {r.text[:200]}")

print("Batch 3 done!")
