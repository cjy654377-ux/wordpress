#!/usr/bin/env python3
"""Expand thin posts batch 2: ID 57, 59, 63"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import login, REST

BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE, "template.html")) as f:
    template = f.read()

# ============================================================
# POST 57: Korean Fried Chicken Guide
# ============================================================
article_57 = """
<h2>How Korean Fried Chicken Conquered the World</h2>

<p>Korean fried chicken (KFC — yes, Koreans use this acronym proudly) is not simply fried chicken with a Korean accent. It is a fundamentally different product. Where American fried chicken relies on a thick, seasoned flour coating for flavor, Korean fried chicken is double-fried to achieve a glass-like crunch that stays crispy for hours, then coated in sauces that range from sweet-and-spicy yangnyeom to soy-garlic to honey butter.</p>

<p>The phenomenon began in the 1960s when American military bases introduced fried chicken to Korea. Korean cooks took the concept and reinvented it: thinner batter, double-frying at different temperatures, and bold Korean sauces. By the 2000s, Korean fried chicken had become a cultural institution — there are over 87,000 chicken restaurants in South Korea, roughly one for every 600 people. That is more chicken restaurants per capita than any country on earth.</p>

<h2>The Three Styles You Need to Know</h2>

<div style="overflow-x:auto;margin:15px 0;">
<table class="rk-tbl" style="min-width:550px;">
<thead><tr><th>Style</th><th>Korean</th><th>Description</th><th>Spice Level</th><th>Best For</th></tr></thead>
<tbody>
<tr><td><strong>Yangnyeom</strong></td><td>양념치킨</td><td>Sweet-spicy red sauce coating (gochujang + garlic + honey)</td><td>Medium-Hot</td><td>First-timers, spice lovers</td></tr>
<tr><td><strong>Huraideu</strong></td><td>후라이드치킨</td><td>Plain double-fried, no sauce, ultra-crispy</td><td>None</td><td>Purists, beer pairing</td></tr>
<tr><td><strong>Ganjanng</strong></td><td>간장치킨</td><td>Soy-garlic glaze, savory-sweet</td><td>None</td><td>Those who dislike spice</td></tr>
<tr><td><strong>Honey Butter</strong></td><td>허니버터치킨</td><td>Sweet honey-butter glaze with almonds</td><td>None</td><td>Sweet tooth, kids</td></tr>
<tr><td><strong>Snow Onion</strong></td><td>스노윙치킨</td><td>Creamy sweet onion sauce on top</td><td>None</td><td>Mild flavor preference</td></tr>
<tr><td><strong>Bburinkle</strong></td><td>뿌링클</td><td>Cheese-flavored seasoning powder</td><td>None</td><td>Cheese lovers</td></tr>
</tbody>
</table>
</div>

<div class="rk-hl">
<strong>Pro tip:</strong> Cannot decide? Order "반반" (banban — half and half). Most chains let you get half yangnyeom and half huraideu in one order. Best of both worlds.
</div>

<h2>The Big Chains: Which One Should You Try?</h2>

<div style="overflow-x:auto;margin:15px 0;">
<table class="rk-tbl" style="min-width:600px;">
<thead><tr><th>Chain</th><th>Founded</th><th>Signature Item</th><th>Price (whole)</th><th>Best For</th></tr></thead>
<tbody>
<tr><td><strong>BBQ Chicken</strong></td><td>1995</td><td>Golden Olive Chicken</td><td>₩20,000-22,000</td><td>Premium quality, olive oil frying</td></tr>
<tr><td><strong>BHC</strong></td><td>2004</td><td>Bburinkle (cheese powder)</td><td>₩19,000-21,000</td><td>Unique flavors, younger crowd</td></tr>
<tr><td><strong>Kyochon</strong></td><td>1991</td><td>Honey Series, Soy Garlic</td><td>₩19,000-21,000</td><td>Consistent quality, international branches</td></tr>
<tr><td><strong>Pelicana</strong></td><td>1982</td><td>Original Fried (oldest chain)</td><td>₩18,000-20,000</td><td>Old-school taste, nostalgia</td></tr>
<tr><td><strong>Nene Chicken</strong></td><td>1999</td><td>Snow Onion Chicken</td><td>₩19,000-21,000</td><td>Creative sauces, variety</td></tr>
<tr><td><strong>Goobne</strong></td><td>2003</td><td>Oven-roasted (not fried)</td><td>₩20,000-22,000</td><td>Healthier option, less greasy</td></tr>
<tr><td><strong>Mom's Touch</strong></td><td>1997</td><td>Chicken burger combos</td><td>₩6,000-9,000</td><td>Budget-friendly, fast casual</td></tr>
</tbody>
</table>
</div>

<h2>Chimaek Culture: Chicken + Beer = Korean Lifestyle</h2>

<p>"Chimaek" (치맥) is the combination of "chicken" (치킨) and "maekju" (맥주, beer). It is not just a food pairing — it is a cultural ritual. On any given evening, millions of Koreans gather at chicken restaurants, parks, or Han River picnic spots with boxes of fried chicken and cases of beer. The chimaek scene hit global fame when it appeared in the K-drama "My Love from the Star" (2013), where the lead character's love of chicken and beer sparked a craze across Asia.</p>

<p>The best beers to pair with Korean fried chicken:</p>

<ul>
<li><strong>Cass Fresh:</strong> Korea's best-selling beer, light and crisp — the default chimaek choice</li>
<li><strong>Kloud:</strong> Slightly more premium, malty flavor</li>
<li><strong>Terra:</strong> Refreshing, marketed as "clean lager"</li>
<li><strong>Craft options:</strong> Seoul's craft beer scene is booming — try Magpie Brewing or Amazing Brewing Company</li>
</ul>

<div class="rk-info">
<strong>Delivery culture:</strong> In Korea, you can order fried chicken delivered to almost anywhere — your hotel, a park bench, a riverbank. Use Baedal Minjok (배달의민족) or Coupang Eats apps. Minimum order is usually ₩15,000.
</div>

<h2>The Side Dishes That Complete the Experience</h2>

<ul>
<li><strong>Pickled radish (치킨무):</strong> The cube-shaped, sweet-sour radish that comes free with every chicken order. Its acidity cuts through the oil and refreshes your palate.</li>
<li><strong>Coleslaw:</strong> Most chains include a small container of creamy coleslaw.</li>
<li><strong>French fries:</strong> Increasingly popular as a combo add-on (₩2,000-3,000).</li>
<li><strong>Tteokbokki:</strong> Some restaurants offer a chicken + tteokbokki combo — the sweet-spicy rice cakes complement the savory chicken perfectly.</li>
</ul>

<h2>Late-Night Chicken Culture</h2>

<p>Korean chicken restaurants typically operate until 2:00-4:00 AM, and delivery is available until at least midnight. Late-night chicken is practically a national pastime — after work drinks, study sessions, or K-drama binge-watching sessions are all enhanced by a midnight chicken delivery. Many Koreans consider 9:00 PM the "prime chicken hour."</p>

<h2>How to Order Like a Local</h2>

<div style="overflow-x:auto;margin:15px 0;">
<table class="rk-tbl" style="min-width:500px;">
<thead><tr><th>Korean</th><th>Romanization</th><th>English</th></tr></thead>
<tbody>
<tr><td>양념 한 마리 주세요</td><td>yangnyeom han mari juseyo</td><td>One whole yangnyeom chicken, please</td></tr>
<tr><td>반반 주세요</td><td>banban juseyo</td><td>Half-and-half, please</td></tr>
<tr><td>순살로 주세요</td><td>sunsal-lo juseyo</td><td>Boneless, please</td></tr>
<tr><td>뼈 있는 걸로요</td><td>ppyeo inneun geollo-yo</td><td>Bone-in, please</td></tr>
<tr><td>맥주 한 병 주세요</td><td>maekju han byeong juseyo</td><td>One bottle of beer, please</td></tr>
</tbody>
</table>
</div>

<p>For the perfect anju (drinking food) pairing guide, see our <a href="https://rhythmicaleskimo.com/korean-drinking-food-anju-the-best-bar-snacks-to-order-with-soju-and-beer/">Korean Drinking Food (Anju) Guide</a>. Learn about Korea's national spirit in our <a href="https://rhythmicaleskimo.com/soju-guide-for-beginners-how-to-drink-koreas-national-spirit-like-a-local/">Soju Guide for Beginners</a>. And discover more Korean street food in our <a href="https://rhythmicaleskimo.com/the-ultimate-guide-to-korean-street-food-15-must-try-snacks-and-where-to-find-them/">Ultimate Street Food Guide</a>.</p>

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What makes Korean fried chicken different from American fried chicken?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Korean fried chicken is double-fried at different temperatures, creating an ultra-thin, glass-like crispy coating that stays crunchy for hours. It uses less batter and is typically coated in sauces like yangnyeom (sweet-spicy), soy-garlic, or honey butter."
      }
    },
    {
      "@type": "Question",
      "name": "What does chimaek mean?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Chimaek (치맥) combines 치킨 (chicken) and 맥주 (maekju, beer). It refers to the Korean cultural ritual of eating fried chicken with beer, often at parks, riverside spots, or chicken restaurants."
      }
    },
    {
      "@type": "Question",
      "name": "How much does Korean fried chicken cost?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "A whole chicken at major chains costs ₩18,000-22,000 ($13-16 USD). Budget options like Mom's Touch offer chicken combos from ₩6,000. Delivery usually requires a ₩15,000 minimum order."
      }
    }
  ]
}
</script>
"""

# ============================================================
# POST 59: Korean Temple Food
# ============================================================
article_59 = """
<h2>What Is Korean Temple Food?</h2>

<p>Korean temple food (사찰음식, sachal eumsik) is the plant-based cuisine developed over 1,700 years by Buddhist monks living in Korea's mountain temples. It is not simply "Korean vegetarian food" — it is a complete culinary philosophy built around mindfulness, seasonal ingredients, and the belief that food is medicine.</p>

<p>What makes temple food unique is not just what is included, but what is deliberately excluded. The "five pungent roots" (오신채, osinchae) — garlic, onion, green onion, chives, and leek — are banned because Buddhist monks believe these ingredients stimulate desire and anger, disturbing meditation. Without these aromatics that form the foundation of virtually all other Korean cooking, temple food chefs must create depth of flavor through fermentation, slow cooking, natural mushroom umami, and seasonal vegetable combinations.</p>

<h2>The Philosophy Behind Every Dish</h2>

<p>Temple food follows three core principles:</p>

<ul>
<li><strong>Seasonal eating (제철음식):</strong> Monks eat only what grows naturally in each season. Spring brings wild greens (봄나물), summer offers fresh vegetables, autumn brings root vegetables and mushrooms, winter relies on preserved and fermented foods.</li>
<li><strong>Zero waste (발우공양):</strong> In formal temple meals, monks eat from four nested bowls (발우) and wash them with water they then drink — nothing is wasted. Every grain of rice is consumed.</li>
<li><strong>Simplicity:</strong> Flavors are subtle, not bold. The goal is to taste the ingredient itself, not mask it with sauce or seasoning. After eating temple food, many people report that regular Korean food tastes overwhelmingly salty.</li>
</ul>

<h2>Signature Temple Food Dishes</h2>

<div style="overflow-x:auto;margin:15px 0;">
<table class="rk-tbl" style="min-width:550px;">
<thead><tr><th>Dish</th><th>Korean</th><th>Description</th><th>Season</th></tr></thead>
<tbody>
<tr><td><strong>Yeonip-bap</strong></td><td>연잎밥</td><td>Rice steamed in a lotus leaf with chestnuts, jujubes, ginkgo nuts</td><td>Summer-Autumn</td></tr>
<tr><td><strong>Beoseot-jeon</strong></td><td>버섯전</td><td>Pan-fried mushroom pancakes (shiitake, king oyster, wood ear)</td><td>Autumn</td></tr>
<tr><td><strong>Doraji-namul</strong></td><td>도라지나물</td><td>Seasoned bellflower root — slightly bitter, good for respiratory health</td><td>Spring-Autumn</td></tr>
<tr><td><strong>Dubu-gui</strong></td><td>두부구이</td><td>Grilled temple-made tofu with soy dipping sauce</td><td>Year-round</td></tr>
<tr><td><strong>Sanchae-bibimbap</strong></td><td>산채비빔밥</td><td>Mountain vegetable bibimbap — 15+ wild greens over rice</td><td>Spring</td></tr>
<tr><td><strong>Hobak-juk</strong></td><td>호박죽</td><td>Sweet pumpkin porridge — creamy, naturally sweet</td><td>Autumn-Winter</td></tr>
<tr><td><strong>Temple kimchi</strong></td><td>사찰김치</td><td>Kimchi without garlic, fish sauce, or shrimp paste — uses mushroom broth</td><td>Year-round</td></tr>
<tr><td><strong>Songpyeon</strong></td><td>송편</td><td>Pine-scented rice cakes filled with sesame or chestnut</td><td>Chuseok (Autumn)</td></tr>
</tbody>
</table>
</div>

<h2>Where to Experience Temple Food</h2>

<h3>Temple Stay Programs (체험)</h3>

<p>The most authentic way to experience temple food is through a temple stay program, where you live, eat, and meditate alongside monks for 1-3 days.</p>

<div style="overflow-x:auto;margin:15px 0;">
<table class="rk-tbl" style="min-width:550px;">
<thead><tr><th>Temple</th><th>Location</th><th>Price</th><th>Duration</th><th>Highlights</th></tr></thead>
<tbody>
<tr><td><strong>Jogye-sa</strong></td><td>Central Seoul</td><td>₩50,000</td><td>Day program</td><td>Most accessible, cooking class included</td></tr>
<tr><td><strong>Bongeun-sa</strong></td><td>Gangnam, Seoul</td><td>₩50,000</td><td>Day program</td><td>English-friendly, near COEX</td></tr>
<tr><td><strong>Haein-sa</strong></td><td>Hapcheon, Gyeongsang</td><td>₩70,000</td><td>1 night 2 days</td><td>UNESCO site, Tripitaka Koreana</td></tr>
<tr><td><strong>Beomeo-sa</strong></td><td>Busan</td><td>₩60,000</td><td>1 night 2 days</td><td>Mountain setting, sunrise meditation</td></tr>
<tr><td><strong>Guin-sa</strong></td><td>Danyang, Chungbuk</td><td>Free</td><td>2 nights 3 days</td><td>Largest temple, 10,000+ monks during ceremonies</td></tr>
</tbody>
</table>
</div>

<div class="rk-info">
<strong>Book at:</strong> <a href="https://www.templestay.com" rel="nofollow">templestay.com</a> — the official Jogye Order website. English bookings available. Most programs include all meals, accommodation, and meditation instruction.
</div>

<h3>Temple Food Restaurants in Seoul</h3>

<ul>
<li><strong>Balwoo Gongyang (발우공양):</strong> Michelin-starred temple food restaurant in Jogye-sa temple complex. Lunch course ₩35,000-55,000. Reservation recommended.</li>
<li><strong>Sanchon (산촌):</strong> In Insadong, serving temple food since 1988. Full course ₩30,000. Traditional performance included at dinner.</li>
<li><strong>Oseh Gye Hyang (오세계향):</strong> Near Anguk station, casual temple food at affordable prices (₩10,000-15,000).</li>
</ul>

<h2>Health Benefits of Temple Food</h2>

<p>Korean temple food has attracted attention from nutritionists worldwide for several reasons:</p>

<ul>
<li><strong>Anti-inflammatory:</strong> Heavy use of mushrooms, wild greens, and fermented foods reduces chronic inflammation</li>
<li><strong>Gut health:</strong> Temple kimchi and fermented pastes (without garlic) provide probiotics in a gentler form</li>
<li><strong>Low calorie, high nutrition:</strong> A typical temple meal is 400-600 calories with dense micronutrient content</li>
<li><strong>Mindful eating:</strong> The practice of eating in silence and chewing each bite 30+ times improves digestion</li>
</ul>

<h2>Temple Food vs Regular Korean Food</h2>

<div style="overflow-x:auto;margin:15px 0;">
<table class="rk-tbl" style="min-width:500px;">
<thead><tr><th>Aspect</th><th>Temple Food</th><th>Regular Korean Food</th></tr></thead>
<tbody>
<tr><td>Garlic/Onion</td><td>Never used</td><td>In almost every dish</td></tr>
<tr><td>Meat/Fish</td><td>Never used</td><td>Central to many dishes</td></tr>
<tr><td>Fish sauce/Shrimp paste</td><td>Never used</td><td>In kimchi and many stews</td></tr>
<tr><td>Flavor source</td><td>Mushrooms, soy, fermentation</td><td>Garlic, sesame oil, gochujang</td></tr>
<tr><td>Cooking speed</td><td>Slow, deliberate</td><td>Fast, high-heat</td></tr>
<tr><td>MSG</td><td>Never</td><td>Sometimes</td></tr>
</tbody>
</table>
</div>

<p>For more Korean food exploration, check our guide to <a href="https://rhythmicaleskimo.com/top-10-must-try-korean-soups-for-winter-from-tv-show-kitchens-to-your-travel-itinerary/">Korean Winter Soups</a>. Find hidden gems in our <a href="https://rhythmicaleskimo.com/seouls-hidden-alley-restaurants-7-places-only-locals-know-about/">Seoul's Hidden Alley Restaurants</a> guide. And learn essential dining phrases in our <a href="https://rhythmicaleskimo.com/how-to-order-food-in-korean-25-essential-phrases-every-traveler-needs/">Korean Restaurant Ordering Guide</a>.</p>

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Is Korean temple food vegan?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Korean temple food is plant-based and excludes all meat, fish, eggs, and dairy. However, it also excludes garlic, onion, green onion, chives, and leek — the five pungent roots banned in Buddhist cooking."
      }
    },
    {
      "@type": "Question",
      "name": "Where can I try temple food in Seoul?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "The best options are Balwoo Gongyang (Michelin-starred, in Jogye-sa temple), Sanchon in Insadong (since 1988), and Oseh Gye Hyang near Anguk station for a budget-friendly option."
      }
    },
    {
      "@type": "Question",
      "name": "How much does a temple stay cost in Korea?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Day programs cost ₩50,000 ($37 USD). Overnight stays range from free (Guin-sa) to ₩70,000 ($52 USD). Book at templestay.com for English-language reservations."
      }
    }
  ]
}
</script>
"""

# ============================================================
# POST 63: Soju Guide for Beginners
# ============================================================
article_63 = """
<h2>What Is Soju and Why Does Korea Drink So Much of It?</h2>

<p>Soju (소주) is Korea's national spirit — a clear, slightly sweet distilled alcohol that outsells every other liquor on earth. Jinro soju alone sells over 86 million cases per year, more than Smirnoff vodka, Bacardi rum, and Jack Daniel's whiskey combined. South Korea's per-capita alcohol consumption is among the highest in Asia, and soju is the reason.</p>

<p>At 16-20% ABV (alcohol by volume), soju sits in a unique middle ground — stronger than beer (4-5%) and wine (12-15%) but gentler than vodka (40%). This "just right" strength means it goes down dangerously smooth, especially the modern fruit-flavored versions that taste like juice. Many tourists discover soju's power the hard way the morning after their first Korean BBQ dinner.</p>

<h2>A Brief History: From Mongol Distillation to Modern Phenomenon</h2>

<p>Soju's origin traces back to the 13th century Mongol invasion of Korea. The Mongols brought arak distillation techniques from Persia, and Korean distillers adapted them using local rice. The city of Andong in southeastern Korea became the center of traditional soju production, and Andong Soju (안동소주, 45% ABV) is still made using the original 700-year-old method.</p>

<p>Modern soju took a dramatic turn in 1965 when the Korean government banned the use of rice for alcohol production (to preserve food supply during the post-war era). Distillers switched to cheaper starches — sweet potato, tapioca, and wheat — diluted with water and sweetened. This created the light, affordable soju that dominates today. The ban was lifted in 1999, but most commercial brands still use the cheaper formula because consumers are accustomed to the taste.</p>

<h2>Types of Soju</h2>

<div style="overflow-x:auto;margin:15px 0;">
<table class="rk-tbl" style="min-width:550px;">
<thead><tr><th>Type</th><th>ABV</th><th>Price</th><th>Taste</th><th>Best For</th></tr></thead>
<tbody>
<tr><td><strong>Classic (참이슬, Chamisul)</strong></td><td>16.5%</td><td>₩1,800-2,500</td><td>Clean, slightly sweet, neutral</td><td>Default choice, Korean BBQ pairing</td></tr>
<tr><td><strong>Fruit-flavored (자몽, 청포도)</strong></td><td>12-13%</td><td>₩1,800-2,500</td><td>Sweet, fruity, easy drinking</td><td>Beginners, those who dislike alcohol taste</td></tr>
<tr><td><strong>Premium (원소주, 화요)</strong></td><td>25-41%</td><td>₩12,000-30,000</td><td>Smooth, complex, rice-forward</td><td>Sipping neat, special occasions</td></tr>
<tr><td><strong>Traditional Andong</strong></td><td>45%</td><td>₩15,000-25,000</td><td>Rich, herbal, intense</td><td>Serious drinkers, cultural experience</td></tr>
<tr><td><strong>Zero Sugar</strong></td><td>16%</td><td>₩1,800-2,500</td><td>Drier, less sweet</td><td>Calorie-conscious drinkers</td></tr>
</tbody>
</table>
</div>

<h2>Regional Soju Brands: Every City Has Its Own</h2>

<p>Each Korean region has a dominant local soju brand, and locals are fiercely loyal to their hometown spirit. Ordering the "wrong" soju in certain cities can earn you puzzled looks:</p>

<div style="overflow-x:auto;margin:15px 0;">
<table class="rk-tbl" style="min-width:500px;">
<thead><tr><th>Region</th><th>Brand</th><th>ABV</th><th>Character</th></tr></thead>
<tbody>
<tr><td>Seoul / National</td><td><strong>Chamisul (참이슬)</strong></td><td>16.5%</td><td>Market leader, clean taste</td></tr>
<tr><td>Busan / Gyeongsang</td><td><strong>C1 (시원)</strong></td><td>16.5%</td><td>Slightly sweeter than Chamisul</td></tr>
<tr><td>Daejeon / Chungcheong</td><td><strong>Charm (잎새주)</strong></td><td>16.5%</td><td>Smooth, subtle sweetness</td></tr>
<tr><td>Gwangju / Jeolla</td><td><strong>Isul Tok Tok (이슬톡톡)</strong></td><td>13%</td><td>Slightly carbonated</td></tr>
<tr><td>Jeju Island</td><td><strong>Hallasan (한라산)</strong></td><td>17.5%</td><td>Made with Jeju volcanic water</td></tr>
<tr><td>Andong</td><td><strong>Andong Soju (안동소주)</strong></td><td>45%</td><td>Traditional distillation, premium</td></tr>
</tbody>
</table>
</div>

<h2>Korean Drinking Etiquette: The Unwritten Rules</h2>

<p>Korean drinking culture is built on respect, hierarchy, and social bonding. Break these rules and you will get forgiven (you are a foreigner, after all), but follow them and you will earn instant respect:</p>

<ol>
<li><strong>Never pour your own drink.</strong> In Korea, you pour for others, and they pour for you. An empty glass is an invitation for someone else to fill it.</li>
<li><strong>Pour and receive with two hands.</strong> Hold the bottle with both hands when pouring for someone older or senior. When receiving, hold your glass with both hands.</li>
<li><strong>Turn away when drinking with elders.</strong> If drinking with someone older, turn your body slightly to the side and cover your glass with one hand. This shows respect.</li>
<li><strong>The eldest drinks first.</strong> Wait for the oldest or most senior person to take the first sip before you drink.</li>
<li><strong>Do not refuse the first drink.</strong> The first drink offered to you is a gesture of friendship. Accepting it is almost mandatory in Korean culture.</li>
<li><strong>Pace yourself with food.</strong> Koreans never drink without eating. Always order anju (drinking food) — see our <a href="https://rhythmicaleskimo.com/korean-drinking-food-anju-the-best-bar-snacks-to-order-with-soju-and-beer/">anju guide</a> for recommendations.</li>
</ol>

<h2>Popular Soju Drinking Games</h2>

<ul>
<li><strong>Flick the Cap (병뚜껑 치기):</strong> Twist the loose strip on the soju cap into a tight coil. Players take turns flicking it. The person who flicks it off makes everyone else drink.</li>
<li><strong>Love Shot (러브샷):</strong> Two people link arms and drink simultaneously. Often done between couples or as a friendly gesture.</li>
<li><strong>Titanic (타이타닉):</strong> Float a shot glass in a beer glass. Players take turns pouring soju into the floating glass. The person who sinks it drinks the entire beer + soju mix (this creates "somaek").</li>
<li><strong>Baskin Robbins 31:</strong> Players count numbers 1-31, saying 1-3 numbers per turn. The person who says "31" drinks.</li>
</ul>

<h2>Food Pairings: What to Eat with Soju</h2>

<div style="overflow-x:auto;margin:15px 0;">
<table class="rk-tbl" style="min-width:500px;">
<thead><tr><th>Food</th><th>Why It Works</th><th>Where to Find It</th></tr></thead>
<tbody>
<tr><td><strong>Samgyeopsal (삼겹살)</strong></td><td>Fatty pork belly cuts through soju's sharpness</td><td>Every Korean BBQ restaurant</td></tr>
<tr><td><strong>Pajeon (파전)</strong></td><td>Savory green onion pancake, perfect rainy-day pairing</td><td>Traditional restaurants, pojangmacha</td></tr>
<tr><td><strong>Dried squid (마른 오징어)</strong></td><td>Chewy, salty, zero prep — classic convenience store anju</td><td>Every convenience store (₩3,000-5,000)</td></tr>
<tr><td><strong>Jokbal (족발)</strong></td><td>Braised pig feet — rich, gelatinous, pairs beautifully</td><td>Jokbal specialty restaurants</td></tr>
<tr><td><strong>Dakbal (닭발)</strong></td><td>Spicy chicken feet — extreme anju for adventurous drinkers</td><td>Dakbal restaurants, late-night bars</td></tr>
</tbody>
</table>
</div>

<h2>Hangover Cures: The Morning After</h2>

<p>Korea takes hangovers seriously. An entire industry exists around "haejangguk" (해장국, hangover soup). The morning after soju night, Koreans reach for:</p>

<ul>
<li><strong>Haejangguk (해장국):</strong> Beef blood soup with vegetables — the classic 6 AM remedy, sold at 24-hour restaurants</li>
<li><strong>Kongnamul-guk (콩나물국):</strong> Soybean sprout soup — lighter option, packed with amino acids</li>
<li><strong>Dawn 808 (여명808):</strong> Hangover drink sold at every convenience store (₩3,000) — drink before sleeping</li>
<li><strong>Condition (컨디션):</strong> Another popular hangover prevention drink — take before or during drinking</li>
</ul>

<p>Pair your soju with the right food — read our <a href="https://rhythmicaleskimo.com/korean-drinking-food-anju-the-best-bar-snacks-to-order-with-soju-and-beer/">complete anju guide</a>. Learn proper BBQ manners in our <a href="https://rhythmicaleskimo.com/korean-bbq-etiquette-12-rules-every-first-timer-needs-to-know/">Korean BBQ Etiquette Guide</a>. And master restaurant ordering with our <a href="https://rhythmicaleskimo.com/how-to-order-food-in-korean-25-essential-phrases-every-traveler-needs/">25 Essential Korean Food Phrases</a>.</p>

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "How strong is soju?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Standard soju is 16-17% ABV, about three times stronger than beer. Fruit-flavored versions are 12-13% ABV. Traditional Andong soju is 45% ABV, similar to whiskey."
      }
    },
    {
      "@type": "Question",
      "name": "Why is soju so cheap in Korea?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "A bottle of soju costs ₩1,800-2,500 ($1.30-1.80 USD) because it is made from inexpensive starches (sweet potato, tapioca) rather than rice, and production is highly industrialized. The government also keeps alcohol taxes relatively low."
      }
    },
    {
      "@type": "Question",
      "name": "What is the best soju for beginners?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Fruit-flavored soju (grapefruit/자몽 or green grape/청포도 are most popular) at 12-13% ABV is the easiest entry point. Chamisul Fresh (16.5%) is the standard if you want the classic experience."
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
    (57, article_57, "Korean Fried Chicken"),
    (59, article_59, "Temple Food"),
    (63, article_63, "Soju Guide"),
]

for pid, body, label in updates:
    html = template.replace("{CONTENT}", body)
    r = s.post(f"{REST}/posts/{pid}", headers=h, json={"content": html})
    if r.status_code == 200:
        print(f"  Updated: {label} (ID={pid})")
    else:
        print(f"  FAIL {label}: {r.status_code} {r.text[:200]}")

print("Batch 2 done!")
