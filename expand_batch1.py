#!/usr/bin/env python3
"""Expand thin posts batch 1: ID 51, 53, 55"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import login, REST

BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE, "template.html")) as f:
    template = f.read()

# ============================================================
# POST 51: How to Order Food in Korean
# ============================================================
article_51 = """
<h2>Why Learning Korean Food Phrases Changes Everything</h2>

<p>Walking into a Korean restaurant without knowing a single phrase is like showing up to a job interview in pajamas — you might survive, but it will not be pretty. Most restaurants outside Seoul's tourist zones operate entirely in Korean. Menus are handwritten on walls, ajummas (restaurant aunties) shout orders across the room, and pointing at pictures only gets you so far.</p>

<p>The good news: Korean restaurant interactions follow a predictable script. Learn 25 phrases, and you can eat anywhere in the country — from a Michelin-starred hanwoo beef house in Gangnam to a 3,000-won kimbap shop in a university neighborhood. These phrases are organized by the exact moment you will need them.</p>

<h2>Phase 1: Entering the Restaurant (입장)</h2>

<p>The moment you step through the door, a server will greet you with "어서오세요!" (eoseo-oseyo — welcome!). Here is what to say next:</p>

<div style="overflow-x:auto;margin:15px 0;">
<table class="rk-tbl" style="min-width:500px;">
<thead><tr><th>Korean</th><th>Romanization</th><th>English</th><th>When to Use</th></tr></thead>
<tbody>
<tr><td><strong>몇 명이에요?</strong></td><td>myeot myeong-ieyo?</td><td>How many people?</td><td>They will ask you this</td></tr>
<tr><td><strong>두 명이요</strong></td><td>du myeong-iyo</td><td>Two people</td><td>Replace 두(2) with: 한(1), 세(3), 네(4)</td></tr>
<tr><td><strong>자리 있어요?</strong></td><td>jari isseoyo?</td><td>Do you have a table?</td><td>Busy restaurants, no reservation</td></tr>
<tr><td><strong>예약했어요</strong></td><td>yeyak-haesseoyo</td><td>I have a reservation</td><td>Upscale restaurants</td></tr>
<tr><td><strong>혼밥이요</strong></td><td>honbab-iyo</td><td>Eating alone</td><td>Solo dining (very common in Korea)</td></tr>
</tbody>
</table>
</div>

<div class="rk-info">
<strong>Cultural tip:</strong> In Korea, solo dining (혼밥, honbab) is completely normal. Many restaurants even have solo seating counters. Do not feel awkward — Koreans respect solo diners.
</div>

<h2>Phase 2: Reading the Menu and Ordering (주문)</h2>

<p>Korean menus can look intimidating, but most follow a simple pattern: dish name + price. Here are the phrases that get your food on the table:</p>

<div style="overflow-x:auto;margin:15px 0;">
<table class="rk-tbl" style="min-width:500px;">
<thead><tr><th>Korean</th><th>Romanization</th><th>English</th><th>Context</th></tr></thead>
<tbody>
<tr><td><strong>메뉴판 주세요</strong></td><td>menyu-pan juseyo</td><td>Menu, please</td><td>If not given automatically</td></tr>
<tr><td><strong>추천 메뉴 뭐예요?</strong></td><td>chucheon menyu mwoyeyo?</td><td>What do you recommend?</td><td>Great for local specialties</td></tr>
<tr><td><strong>이거 주세요</strong></td><td>igeo juseyo</td><td>This one, please</td><td>Point at menu + say this</td></tr>
<tr><td><strong>이거 하나 더 주세요</strong></td><td>igeo hana deo juseyo</td><td>One more of this, please</td><td>Reorder banchan or drinks</td></tr>
<tr><td><strong>덜 맵게 해주세요</strong></td><td>deol maepge haejuseyo</td><td>Less spicy, please</td><td>Essential for spice-sensitive travelers</td></tr>
<tr><td><strong>안 맵게 해주세요</strong></td><td>an maepge haejuseyo</td><td>Not spicy, please</td><td>Zero spice tolerance</td></tr>
<tr><td><strong>여기요!</strong></td><td>yeogiyo!</td><td>Excuse me! (to call server)</td><td>Loudly — this is normal in Korea</td></tr>
<tr><td><strong>물 좀 주세요</strong></td><td>mul jom juseyo</td><td>Water, please</td><td>Water is usually self-serve, but ask if unsure</td></tr>
</tbody>
</table>
</div>

<div class="rk-info">
<strong>Calling the server:</strong> In Korea, you shout "여기요!" (yeogiyo!) loudly across the restaurant. This is NOT rude — it is expected. Many restaurants also have a call button (호출벨) on the table. Press it and wait.
</div>

<h2>Phase 3: During the Meal — Banchan and Refills</h2>

<p>Banchan (반찬) — the small side dishes that arrive before your main course — are always free and always refillable. This is one of the most beautiful aspects of Korean dining culture. Here is how to navigate it:</p>

<div style="overflow-x:auto;margin:15px 0;">
<table class="rk-tbl" style="min-width:500px;">
<thead><tr><th>Korean</th><th>Romanization</th><th>English</th></tr></thead>
<tbody>
<tr><td><strong>반찬 더 주세요</strong></td><td>banchan deo juseyo</td><td>More side dishes, please</td></tr>
<tr><td><strong>김치 더 주세요</strong></td><td>kimchi deo juseyo</td><td>More kimchi, please</td></tr>
<tr><td><strong>밥 추가요</strong></td><td>bap chugayo</td><td>Extra rice, please (may cost ₩1,000)</td></tr>
<tr><td><strong>맛있어요!</strong></td><td>mashisseoyo!</td><td>It is delicious!</td></tr>
<tr><td><strong>배불러요</strong></td><td>baebulleoyo</td><td>I am full</td></tr>
</tbody>
</table>
</div>

<p>Banchan etiquette is simple: eat what you want, leave what you do not. Do not pile uneaten banchan on one plate — it signals to the restaurant that they gave you too much. If a banchan dish is empty and you want more, just ask. Refills are unlimited and free at virtually every Korean restaurant.</p>

<h2>Phase 4: Paying the Bill (계산)</h2>

<div style="overflow-x:auto;margin:15px 0;">
<table class="rk-tbl" style="min-width:500px;">
<thead><tr><th>Korean</th><th>Romanization</th><th>English</th><th>Notes</th></tr></thead>
<tbody>
<tr><td><strong>계산이요</strong></td><td>gyesan-iyo</td><td>Check, please</td><td>Or just walk to the counter</td></tr>
<tr><td><strong>카드 돼요?</strong></td><td>kadeu dwaeyo?</td><td>Can I pay by card?</td><td>99% of places accept cards</td></tr>
<tr><td><strong>현금만 돼요?</strong></td><td>hyeongeum-man dwaeyo?</td><td>Cash only?</td><td>Very rare, but some old markets</td></tr>
<tr><td><strong>영수증 주세요</strong></td><td>yeongsujeung juseyo</td><td>Receipt, please</td><td>For business travelers</td></tr>
<tr><td><strong>같이 계산이요</strong></td><td>gachi gyesan-iyo</td><td>Together (one bill)</td><td>Default in Korea</td></tr>
<tr><td><strong>따로 계산이요</strong></td><td>ttaro gyesan-iyo</td><td>Separate bills</td><td>Less common but possible</td></tr>
</tbody>
</table>
</div>

<div class="rk-hl">
<strong>No tipping in Korea!</strong> Tipping does not exist in Korean dining culture. The price on the menu is the final price. Leaving money on the table may confuse or even offend your server.
</div>

<h2>Common Menu Items You Will See Everywhere</h2>

<p>These are the dishes that appear on menus across the country. Knowing these words lets you order confidently even at places with Korean-only menus:</p>

<div style="overflow-x:auto;margin:15px 0;">
<table class="rk-tbl" style="min-width:500px;">
<thead><tr><th>Korean</th><th>English</th><th>Price Range</th><th>Description</th></tr></thead>
<tbody>
<tr><td>김치찌개</td><td>Kimchi Jjigae</td><td>₩7,000–9,000</td><td>Kimchi stew with pork, tofu</td></tr>
<tr><td>된장찌개</td><td>Doenjang Jjigae</td><td>₩7,000–9,000</td><td>Soybean paste stew</td></tr>
<tr><td>비빔밥</td><td>Bibimbap</td><td>₩8,000–12,000</td><td>Mixed rice with vegetables, egg</td></tr>
<tr><td>삼겹살</td><td>Samgyeopsal</td><td>₩15,000–20,000</td><td>Grilled pork belly (per serving)</td></tr>
<tr><td>냉면</td><td>Naengmyeon</td><td>₩9,000–13,000</td><td>Cold buckwheat noodles</td></tr>
<tr><td>떡볶이</td><td>Tteokbokki</td><td>₩3,000–5,000</td><td>Spicy rice cakes</td></tr>
<tr><td>김밥</td><td>Gimbap</td><td>₩2,500–4,000</td><td>Korean rice rolls</td></tr>
<tr><td>제육볶음</td><td>Jeyuk Bokkeum</td><td>₩8,000–10,000</td><td>Spicy stir-fried pork</td></tr>
</tbody>
</table>
</div>

<h2>Dietary Restrictions and Allergies</h2>

<p>Communicating dietary needs in Korean is challenging but not impossible. These phrases cover the most common situations:</p>

<div style="overflow-x:auto;margin:15px 0;">
<table class="rk-tbl" style="min-width:500px;">
<thead><tr><th>Korean</th><th>Romanization</th><th>English</th></tr></thead>
<tbody>
<tr><td>고기 빼주세요</td><td>gogi ppaejuseyo</td><td>No meat, please</td></tr>
<tr><td>채식이에요</td><td>chaesig-ieyo</td><td>I am vegetarian</td></tr>
<tr><td>알레르기 있어요</td><td>allereugi isseoyo</td><td>I have allergies</td></tr>
<tr><td>땅콩 알레르기</td><td>ttangkong allereugi</td><td>Peanut allergy</td></tr>
<tr><td>해산물 못 먹어요</td><td>haesanmul mot meogeoyo</td><td>I cannot eat seafood</td></tr>
</tbody>
</table>
</div>

<p>Be aware that many Korean dishes contain hidden ingredients — fish sauce, shrimp paste, and anchovy stock are in almost everything, including dishes that look vegetarian. If you have severe allergies, consider carrying a translated allergy card.</p>

<h2>Pro Tips for Korean Restaurant Dining</h2>

<ul>
<li><strong>Shoes off:</strong> If you see shoes at the entrance or the floor is raised, remove your shoes before entering the dining area.</li>
<li><strong>Chopsticks + spoon:</strong> Korea uses metal chopsticks and a long-handled spoon. The spoon is for rice and soup — never lift your rice bowl.</li>
<li><strong>Wait for elders:</strong> If dining with Koreans, wait for the oldest person to start eating before you begin.</li>
<li><strong>Lunch rush:</strong> Between 12:00 and 1:00 PM, popular restaurants have 30-minute waits. Eat at 11:30 or after 1:30 to avoid crowds.</li>
<li><strong>Business hours:</strong> Most restaurants open 11:00 AM to 9:00 PM. Many close between 2:30 PM and 5:00 PM (break time, 브레이크 타임).</li>
</ul>

<p>For more dining etiquette, read our <a href="https://rhythmicaleskimo.com/korean-bbq-etiquette-12-rules-every-first-timer-needs-to-know/">Korean BBQ Etiquette Guide</a>. If you want to explore Korea's best street food, check out our <a href="https://rhythmicaleskimo.com/the-ultimate-guide-to-korean-street-food-15-must-try-snacks-and-where-to-find-them/">Ultimate Korean Street Food Guide</a>. And for market dining adventures, do not miss our <a href="https://rhythmicaleskimo.com/gwangjang-market-food-guide-seouls-oldest-market-and-its-legendary-street-food/">Gwangjang Market Food Guide</a>.</p>

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "How do I call a waiter in a Korean restaurant?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Shout '여기요!' (yeogiyo!) loudly. This is completely normal in Korean dining culture. Many restaurants also have a call button on the table."
      }
    },
    {
      "@type": "Question",
      "name": "Do I need to tip in Korean restaurants?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "No. Tipping does not exist in Korean dining culture. The menu price is the final price. Leaving money on the table may confuse your server."
      }
    },
    {
      "@type": "Question",
      "name": "Are banchan (side dishes) really free and unlimited?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes. Banchan are complimentary at virtually every Korean restaurant and you can request refills at no charge. Extra rice may cost ₩1,000."
      }
    },
    {
      "@type": "Question",
      "name": "Can I eat alone in Korean restaurants?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Absolutely. Solo dining (혼밥, honbab) is extremely common in Korea. Many restaurants have counter seating specifically for solo diners."
      }
    }
  ]
}
</script>
"""

# ============================================================
# POST 53: Gwangjang Market Food Guide
# ============================================================
article_53 = """
<h2>Why Gwangjang Market Is Seoul's Greatest Food Destination</h2>

<p>Gwangjang Market (광장시장) is not just a market — it is a living museum of Korean food culture. Established in 1905, it is Korea's oldest continuously operating traditional market, and its food alley has been featured on Netflix's Street Food Asia, Anthony Bourdain's Parts Unknown, and countless Korean food shows. Every day, hundreds of vendors prepare the same recipes their grandmothers taught them, in the same stalls, using the same techniques that have not changed in decades.</p>

<p>The market sprawls across several city blocks near Jongno 5-ga station, but the famous food alley is concentrated in a single indoor corridor that you can walk end-to-end in 10 minutes. In that short walk, you will pass over 200 food stalls selling everything from sizzling bindaetteok (mung bean pancakes) to raw beef tartare to hand-pulled knife-cut noodles.</p>

<h2>How to Get There</h2>

<div class="rk-info">
<strong>Subway:</strong> Line 1 — Jongno 5-ga Station (종로5가역), Exit 8 or 9. Walk 2 minutes straight ahead.<br>
<strong>Hours:</strong> 9:00 AM – 11:00 PM daily (some stalls close earlier). Best time: 10:30 AM – 2:00 PM for lunch rush atmosphere, or after 7:00 PM for dinner crowds.<br>
<strong>Closed:</strong> Sundays (most food stalls). Always go Monday–Saturday.
</div>

<h2>The 8 Must-Eat Dishes (and Where to Find Them)</h2>

<div style="overflow-x:auto;margin:15px 0;">
<table class="rk-tbl" style="min-width:600px;">
<thead><tr><th>#</th><th>Dish</th><th>Korean</th><th>Price</th><th>Best Stall</th><th>What to Know</th></tr></thead>
<tbody>
<tr><td>1</td><td>Bindaetteok</td><td>빈대떡</td><td>₩5,000</td><td>Stall near East Gate (look for the longest line)</td><td>Crispy mung bean pancake fried in oil, served with soy-vinegar dipping sauce</td></tr>
<tr><td>2</td><td>Mayak Gimbap</td><td>마약김밥</td><td>₩3,000–4,000</td><td>Cho Yonsoon Mayak Gimbap (조연순 마약김밥)</td><td>"Drug kimbap" — tiny, addictive sesame oil rice rolls with mustard sauce</td></tr>
<tr><td>3</td><td>Yukhoe</td><td>육회</td><td>₩15,000–20,000</td><td>2nd floor stalls (look for raw beef displays)</td><td>Korean beef tartare with Asian pear and raw egg yolk</td></tr>
<tr><td>4</td><td>Kalguksu</td><td>칼국수</td><td>₩7,000–8,000</td><td>Any stall with hand-pulling noodles visible</td><td>Knife-cut noodle soup in anchovy broth</td></tr>
<tr><td>5</td><td>Tteokbokki</td><td>떡볶이</td><td>₩4,000</td><td>Main food alley entrance stalls</td><td>Spicy rice cakes — Gwangjang style is chewier than average</td></tr>
<tr><td>6</td><td>Sundae</td><td>순대</td><td>₩5,000</td><td>Usually sold alongside tteokbokki</td><td>Korean blood sausage stuffed with glass noodles</td></tr>
<tr><td>7</td><td>Jeon (assorted)</td><td>전</td><td>₩5,000–8,000</td><td>Corner stalls with large griddles</td><td>Pan-fried pancakes: kimchi, seafood, or vegetable varieties</td></tr>
<tr><td>8</td><td>Nokdu-jeon</td><td>녹두전</td><td>₩5,000</td><td>Same stalls as bindaetteok</td><td>Mung bean pancake with kimchi and pork filling</td></tr>
</tbody>
</table>
</div>

<h2>The Perfect Gwangjang Market Eating Strategy</h2>

<p>The biggest mistake first-timers make is sitting down at the first stall and ordering a full meal. You will be too full to try everything. Here is the veteran strategy:</p>

<ol>
<li><strong>Start with mayak gimbap</strong> (small, light, opens your appetite)</li>
<li><strong>Walk the entire food alley once</strong> without stopping — scout what looks good</li>
<li><strong>Bindaetteok and makgeolli</strong> — the classic pairing, split one pancake with a friend</li>
<li><strong>Kalguksu or sundae</strong> for your main course (pick one, not both)</li>
<li><strong>Yukhoe</strong> if you eat raw beef — this is the premium experience</li>
<li><strong>Hotteok for dessert</strong> (sweet pancake filled with brown sugar and nuts, ₩2,000)</li>
</ol>

<div class="rk-hl">
<strong>Budget tip:</strong> A full Gwangjang Market food tour costs ₩15,000–25,000 per person (about $11–18 USD), including drinks. That gets you 4–5 different dishes — an extraordinary value for the quality.
</div>

<h2>Seating, Ordering, and Market Etiquette</h2>

<p>Gwangjang Market is not a polished food court. It is chaotic, loud, and wonderful. Here is how to navigate it:</p>

<ul>
<li><strong>Seating:</strong> Most stalls have plastic stools at a counter. Just sit down — no need to wait to be seated. If all seats are taken, hover nearby and someone will leave soon.</li>
<li><strong>Ordering:</strong> Point and say "이거 주세요" (igeo juseyo — this one, please). Most vendors understand basic English but appreciate any Korean effort.</li>
<li><strong>Payment:</strong> Cash is preferred at most stalls, but many now accept cards. Bring at least ₩30,000 in cash to be safe.</li>
<li><strong>Sharing:</strong> It is perfectly acceptable (and encouraged) to share dishes. Order one portion and split it.</li>
<li><strong>Peak hours:</strong> The market is shoulder-to-shoulder between 12:00–1:30 PM on weekdays and all day on Saturdays. Visit early morning (10:00 AM) for a calmer experience.</li>
</ul>

<h2>Beyond Food: What Else to See</h2>

<p>Gwangjang Market is not only about food. The upper floors are a textile paradise:</p>

<ul>
<li><strong>2nd floor:</strong> Hanbok (traditional Korean clothing) shops — great for rental or purchase. Custom hanbok starts around ₩200,000.</li>
<li><strong>Vintage clothing:</strong> The market has one of Seoul's best vintage clothing sections, with second-hand goods from ₩5,000.</li>
<li><strong>Fabric shops:</strong> Hundreds of fabric vendors sell silk, cotton, and traditional Korean textiles by the meter.</li>
</ul>

<h2>Nearby Attractions</h2>

<p>Gwangjang Market is in central Seoul, making it easy to combine with other sightseeing:</p>

<ul>
<li><strong>Changdeokgung Palace</strong> (10-minute walk) — UNESCO World Heritage site with the beautiful Secret Garden</li>
<li><strong>Cheonggyecheon Stream</strong> (5-minute walk) — peaceful walking path along a restored urban stream</li>
<li><strong>Dongdaemun Design Plaza</strong> (8-minute walk) — Zaha Hadid's iconic architecture and night market</li>
<li><strong>Insadong</strong> (15-minute walk) — traditional craft shops and tea houses</li>
</ul>

<p>For more Seoul food adventures, explore our guide to <a href="https://rhythmicaleskimo.com/seouls-hidden-alley-restaurants-7-places-only-locals-know-about/">Seoul's Hidden Alley Restaurants</a>. Want to know what else to eat? Check our <a href="https://rhythmicaleskimo.com/the-ultimate-guide-to-korean-street-food-15-must-try-snacks-and-where-to-find-them/">Ultimate Korean Street Food Guide</a>. And learn how to order like a local with our <a href="https://rhythmicaleskimo.com/how-to-order-food-in-korean-25-essential-phrases-every-traveler-needs/">Korean Restaurant Phrases Guide</a>.</p>

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Is Gwangjang Market open on Sundays?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Most food stalls are closed on Sundays. Visit Monday through Saturday for the full experience. The textile and clothing shops may still be open."
      }
    },
    {
      "@type": "Question",
      "name": "How much money should I bring to Gwangjang Market?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Bring at least ₩30,000 in cash (about $22 USD). A full food tour of 4-5 dishes costs ₩15,000-25,000. Some stalls accept cards, but cash is safer."
      }
    },
    {
      "@type": "Question",
      "name": "What is the most famous food at Gwangjang Market?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Bindaetteok (mung bean pancakes) and mayak gimbap (addictive mini rice rolls) are the two most iconic dishes. The raw beef tartare (yukhoe) is the premium choice."
      }
    }
  ]
}
</script>
"""

# ============================================================
# POST 55: Jeonju Bibimbap vs Seoul Bibimbap
# ============================================================
article_55 = """
<h2>The Great Bibimbap Debate: Jeonju vs Seoul</h2>

<p>Bibimbap is Korea's most internationally recognized dish — a bowl of rice topped with seasoned vegetables, meat, a fried or raw egg, and gochujang (red pepper paste), mixed together into a colorful, flavorful mess. But not all bibimbap is created equal. The two dominant styles — Jeonju and Seoul — are as different as New York pizza and Chicago deep dish. Same concept, completely different experiences.</p>

<p>Jeonju, a city of 650,000 people about 2 hours south of Seoul by KTX, is the undisputed capital of bibimbap. UNESCO recognized Jeonju as a Creative City of Gastronomy in 2012, largely because of this single dish. Seoul's version is what most tourists encounter first, and while it is good, locals will tell you it is not the real thing.</p>

<h2>Side-by-Side Comparison</h2>

<div style="overflow-x:auto;margin:15px 0;">
<table class="rk-tbl" style="min-width:550px;">
<thead><tr><th>Element</th><th>Jeonju Bibimbap</th><th>Seoul Bibimbap</th></tr></thead>
<tbody>
<tr><td><strong>Rice</strong></td><td>Cooked in beef bone broth (사골육수)</td><td>Plain steamed white rice</td></tr>
<tr><td><strong>Egg</strong></td><td>Raw egg yolk (날계란)</td><td>Fried egg (계란후라이)</td></tr>
<tr><td><strong>Toppings</strong></td><td>30+ individually seasoned namul vegetables</td><td>10-15 basic vegetables</td></tr>
<tr><td><strong>Meat</strong></td><td>Yukhoe (raw beef tartare) with sesame oil</td><td>Cooked bulgogi or ground beef</td></tr>
<tr><td><strong>Bean sprouts</strong></td><td>Jeonju kongnamul (larger, crunchier soybean sprouts)</td><td>Regular mung bean sprouts</td></tr>
<tr><td><strong>Gochujang</strong></td><td>House-made, often milder and slightly sweet</td><td>Standard commercial gochujang</td></tr>
<tr><td><strong>Banchan</strong></td><td>12-20 side dishes (included)</td><td>3-5 side dishes</td></tr>
<tr><td><strong>Price</strong></td><td>₩12,000-15,000</td><td>₩8,000-12,000</td></tr>
<tr><td><strong>Serving style</strong></td><td>Brass bowl (놋그릇) — traditional</td><td>Stone pot (돌솥) or regular bowl</td></tr>
</tbody>
</table>
</div>

<h2>Why Jeonju Bibimbap Is Different (The History)</h2>

<p>Jeonju's bibimbap tradition dates back to the Joseon Dynasty (1392-1897), when the city served as the ancestral home of the Yi royal family. The dish was originally prepared for royal ceremonies and special occasions, which is why it uses premium ingredients like raw beef tartare and broth-cooked rice — luxuries that commoners could not afford.</p>

<p>The Jeonju version uses kongnamul (soybean sprouts) grown in the region's naturally mineral-rich water, which produces sprouts that are significantly larger and crunchier than those found elsewhere in Korea. Each vegetable topping is prepared separately with its own seasoning — a process that can take hours. The raw egg yolk is placed on top as a symbol of prosperity and richness.</p>

<p>Seoul's version emerged as a more practical, everyday adaptation. The fried egg is easier to prepare, the toppings are simpler, and the stone pot (dolsot) version creates a crispy rice crust at the bottom that adds textural contrast. Seoul-style dolsot bibimbap has its own loyal following, and many people actually prefer the sizzling, crispy version.</p>

<h2>How to Mix Bibimbap Properly</h2>

<p>Whether Jeonju or Seoul, proper mixing technique matters:</p>

<ol>
<li><strong>Add gochujang:</strong> Start with less than you think — you can always add more. One tablespoon is a good starting point.</li>
<li><strong>Add sesame oil:</strong> A generous drizzle (most restaurants provide a bottle on the table).</li>
<li><strong>Mix vigorously:</strong> Use your spoon to fold everything from the bottom up. Mix for at least 30 seconds until every grain of rice is coated.</li>
<li><strong>Scrape the sides:</strong> For dolsot (stone pot) bibimbap, press the mixed rice against the hot sides to create extra crispy bits.</li>
<li><strong>Eat immediately:</strong> Bibimbap is best eaten right after mixing, while the colors and textures are still distinct.</li>
</ol>

<div class="rk-info">
<strong>Local secret:</strong> In Jeonju, locals add a spoonful of kongnamul gukbap broth (soybean sprout soup) to their bibimbap before mixing. It loosens the rice and adds umami depth. Ask for "국물 좀 주세요" (gungmul jom juseyo — some broth, please).
</div>

<h2>Where to Eat: Best Bibimbap Restaurants</h2>

<h3>Jeonju (전주)</h3>

<div style="overflow-x:auto;margin:15px 0;">
<table class="rk-tbl" style="min-width:550px;">
<thead><tr><th>Restaurant</th><th>Price</th><th>Known For</th><th>Location</th></tr></thead>
<tbody>
<tr><td><strong>Hanguk-jip (한국집)</strong></td><td>₩13,000</td><td>Most famous, 70+ year history</td><td>Near Jeonju Hanok Village entrance</td></tr>
<tr><td><strong>Gajok Hoegwan (가족회관)</strong></td><td>₩12,000</td><td>Generous portions, local favorite</td><td>Central Jeonju, near city hall</td></tr>
<tr><td><strong>Vegibap (베지밥)</strong></td><td>₩11,000</td><td>Vegetarian bibimbap specialist</td><td>Inside Hanok Village</td></tr>
</tbody>
</table>
</div>

<h3>Seoul (서울)</h3>

<div style="overflow-x:auto;margin:15px 0;">
<table class="rk-tbl" style="min-width:550px;">
<thead><tr><th>Restaurant</th><th>Price</th><th>Known For</th><th>Location</th></tr></thead>
<tbody>
<tr><td><strong>Gogung (고궁)</strong></td><td>₩14,000</td><td>Jeonju-style in Seoul, chain</td><td>Multiple locations (Myeongdong, Insadong)</td></tr>
<tr><td><strong>Jeonju Jungang Hoegwan</strong></td><td>₩12,000</td><td>Authentic Jeonju taste</td><td>Near Gwanghwamun</td></tr>
<tr><td><strong>Dolsot Bibimbap street stalls</strong></td><td>₩8,000-9,000</td><td>Quick, affordable, hot stone pot</td><td>Throughout Seoul</td></tr>
</tbody>
</table>
</div>

<h2>Planning a Jeonju Food Trip</h2>

<p>If you are serious about bibimbap, a day trip to Jeonju is absolutely worth it. Here is a suggested itinerary:</p>

<ul>
<li><strong>Getting there:</strong> KTX from Seoul Station to Jeonju Station — 1 hour 40 minutes, ₩33,000 one way</li>
<li><strong>10:00 AM:</strong> Arrive, take bus or taxi to Jeonju Hanok Village (전주한옥마을)</li>
<li><strong>11:00 AM:</strong> Bibimbap lunch at Hanguk-jip (arrive before noon to avoid the line)</li>
<li><strong>12:30 PM:</strong> Walk through Hanok Village — 800+ traditional Korean houses, free to explore</li>
<li><strong>2:00 PM:</strong> Visit PNB Bakery (PNB풍년제과) for their famous choco pie — a Jeonju institution since 1951</li>
<li><strong>3:00 PM:</strong> Jeonju National Museum or Gyeonggijeon Shrine</li>
<li><strong>5:00 PM:</strong> Return to Seoul</li>
</ul>

<p>For more Korean food adventures, read our <a href="https://rhythmicaleskimo.com/korean-bbq-etiquette-12-rules-every-first-timer-needs-to-know/">Korean BBQ Etiquette Guide</a>, explore <a href="https://rhythmicaleskimo.com/gwangjang-market-food-guide-seouls-oldest-market-and-its-legendary-street-food/">Gwangjang Market's legendary street food</a>, or discover <a href="https://rhythmicaleskimo.com/busan-food-guide-8-dishes-you-can-only-find-in-koreas-coastal-city/">Busan's unique coastal cuisine</a>.</p>

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is the main difference between Jeonju and Seoul bibimbap?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Jeonju bibimbap uses rice cooked in beef bone broth, raw egg yolk, raw beef tartare, and 30+ individually seasoned vegetables in a brass bowl. Seoul bibimbap uses plain rice, a fried egg, cooked meat, and fewer toppings, often served in a hot stone pot."
      }
    },
    {
      "@type": "Question",
      "name": "Is it worth traveling to Jeonju just for bibimbap?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes. Jeonju is a UNESCO Creative City of Gastronomy and the Hanok Village alone makes the trip worthwhile. The KTX takes only 1 hour 40 minutes from Seoul, making it an easy day trip."
      }
    },
    {
      "@type": "Question",
      "name": "How much does bibimbap cost in Korea?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Seoul bibimbap costs ₩8,000-12,000 ($6-9 USD). Jeonju bibimbap costs ₩12,000-15,000 ($9-11 USD) and comes with significantly more banchan side dishes."
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
    (51, article_51, "Order Food in Korean"),
    (53, article_53, "Gwangjang Market"),
    (55, article_55, "Bibimbap Comparison"),
]

for pid, body, label in updates:
    html = template.replace("{CONTENT}", body)
    r = s.post(f"{REST}/posts/{pid}", headers=h, json={"content": html})
    if r.status_code == 200:
        print(f"  Updated: {label} (ID={pid})")
    else:
        print(f"  FAIL {label}: {r.status_code} {r.text[:200]}")

print("Batch 1 done!")
