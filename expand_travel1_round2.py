#!/usr/bin/env python3
"""Round 2: Expand 7 remaining posts to 2500+ words."""
import sys, re
sys.path.insert(0, '/Users/choijooyong/wordpress')
import engine as e

s, h = e.login()
REST = e.REST

def add_content(pid, extra):
    r = s.get(f'{REST}/posts/{pid}?_fields=content', headers=h)
    content = r.json()['content']['rendered']
    if '<h2>You Might Also Enjoy</h2>' in content:
        pt = content.find('<h2>You Might Also Enjoy</h2>')
        new = content[:pt] + extra + content[pt:]
    elif 'FAQPage' in content:
        pt = content.find('<script type="application/ld+json">')
        new = content[:pt] + extra + content[pt:]
    else:
        last = content.rfind('</div>')
        new = content[:last] + extra + content[last:]
    r2 = s.post(f'{REST}/posts/{pid}', headers=h, json={'content': new})
    text = re.sub(r'<[^>]+>', '', r2.json()['content']['rendered'])
    wc = len(text.split())
    print(f'  ID:{pid} → {wc} words')
    return wc

# ─── ID:42 Korean Food Show Guide (currently ~2236w, need ~300+ more) ───
extra_42b = '''
<h2>Korean Food Documentaries and Netflix Series</h2>
<p>Beyond variety shows, Korea's food documentary scene offers deeper cultural insight. Netflix's <strong>"Street Food: Asia"</strong> Season 1, Episode 1 focuses entirely on Seoul, following legendary Gwangjang Market vendor Cho Yonsoon, who has been making bindaetteok for 40+ years. The episode generated a 400% increase in foreign visitors to her stall. Netflix's <strong>"Somebody Feed Phil"</strong> Season 5 covers Seoul with host Phil Rosenthal exploring Noryangjin Fish Market, Korean BBQ, and pojangmacha culture — practical and entertaining for trip planning.</p>

<h3>Food Competition Shows</h3>
<p><strong>"Iron Chef Korea"</strong> (아이언셰프 코리아, 2022-present) on tvN pits master chefs against each other using Korean ingredients with a 60-minute time limit. Unlike the Japanese original, the Korean version emphasizes storytelling behind each dish's cultural roots. <strong>"Culinary Class Wars"</strong> (흑백요리사, 2024) became Netflix Korea's most-watched show, featuring anonymous chefs (including Michelin-starred restaurateurs cooking under aliases) competing in blind taste tests. The show's popularity made its featured dishes — particularly black bean jjajangmyeon and truffle tteokbokki — trend on social media for weeks.</p>

<h3>How to Use Food Shows for Trip Planning</h3>
<p>Create a food show itinerary with these practical steps: First, use <strong>Naver Map</strong> (Korea's Google Maps equivalent) and search the restaurant name in Korean — copy-paste from show subtitles. Second, check the <strong>"blog" tab</strong> on Naver search results for recent visitor reviews with photos, confirming the restaurant is still open and maintaining quality. Third, save locations to a <strong>Naver Map collection</strong> or Google Maps list. Many post-show restaurants change their hours due to increased demand, so always verify opening times within 24 hours of your visit. Fourth, remember that show-featured restaurants often close on <strong>Mondays</strong> — this is Korea's standard restaurant rest day.</p>
'''

# ─── ID:69 Korean Drinking Food Anju (currently ~2137w, need ~400+ more) ───
extra_69b = '''
<h2>Pojangmacha: The Iconic Korean Tent Bar Experience</h2>
<p>No discussion of anju culture is complete without <strong>pojangmacha (포장마차)</strong> — the orange tent bars that line Korean streets at night. These temporary structures, draped in vinyl tarps with plastic chairs and folding tables, are where Korea's drinking culture is at its most authentic. Pojangmacha specialize in simple, affordable anju: <strong>odeng tang</strong> (fish cake broth, 1,000 KRW per skewer — take as many as you want from the communal pot and pay at the end), <strong>tteokbokki</strong> (4,000 KRW), and <strong>gyeran mari</strong> (rolled egg omelet, 5,000 KRW).</p>

<h3>Where to Find the Best Pojangmacha</h3>
<p>The most atmospheric pojangmacha clusters are at <strong>Euljiro 3-ga</strong> (을지로3가) — the narrow alleys between printing shops transform into a drinking paradise after 7 PM. <strong>Namdaemun Market's east gate</strong> has pojangmacha serving kalguksu (knife-cut noodles, 7,000 KRW) alongside soju until midnight. In Busan, the <strong>BIFF Square</strong> pojangmacha strip serves Busan-style eomuk and ssiat hotteok with makgeolli. Warning: pojangmacha prices are not always displayed. Ask <strong>"eolmayeyo?"</strong> (얼마예요? — "How much?") before ordering to avoid surprises. Most pojangmacha are cash-only.</p>

<h3>Anju Etiquette: What Foreigners Get Wrong</h3>
<p>Several anju customs confuse first-time visitors. <strong>Never pour your own drink</strong> — always pour for others, and they'll pour for you. When receiving a pour from someone older, hold your glass with both hands as a sign of respect. <strong>Don't finish the anju before the drinks</strong> — anju should last the entire drinking session, so pace your eating. When ordering additional rounds, it's polite for different people to order each round rather than splitting the total bill. <strong>The youngest person at the table typically orders and handles payment</strong>, though the oldest person usually pays (or the person who suggested the outing). Finally, if someone is clearly drunk, ordering them a bowl of <strong>haejangguk</strong> (해장국 — hangover soup) is considered a kind gesture, not an insult.</p>
'''

# ─── ID:63 Soju Guide for Beginners (currently ~2097w, need ~450+ more) ───
extra_63b = '''
<h2>Soju and Korean Food: The Perfect Pairing Guide</h2>
<p>Soju's neutral, clean flavor profile makes it Korea's universal food companion, but certain combinations are elevated to cultural institution status. Understanding these pairings enhances both the food and the drink.</p>

<h3>The "Golden Ratio" Soju Cocktails</h3>
<p>Koreans have invented several soju-based mixed drinks that have become standard bar orders:</p>
<ul>
<li><strong>Somaek (소맥)</strong>: Soju + beer. The most popular mixed drink in Korea. Standard ratio: 3:7 (soju to beer). Pour soju into a shot glass, drop the full glass into a beer glass, and drink. The technique — called "poktanju" (폭탄주, bomb drink) — is a bonding ritual at company dinners. A gentler version: pour 1 shot of soju into a glass of beer and stir.</li>
<li><strong>Yogurt Soju (요구르트소주)</strong>: Soju + Yakult (Korean yogurt drink). Mix 1:1 ratio. Sweet, creamy, and dangerously drinkable. Often served frozen in summer at clubs and bars (3,000-5,000 KRW).</li>
<li><strong>Watermelon Soju (수박소주)</strong>: A summer party staple. Hollow out a small watermelon, fill with soju, add Sprite, and scoop with a ladle. The Instagram-friendly presentation makes it popular at rooftop bars (25,000-35,000 KRW for the full watermelon at bars in Itaewon and Hongdae).</li>
<li><strong>Cojinganmek (코진감맥)</strong>: Coca-Cola + soju + Bacchus (Korean energy drink) + beer. This chaotic mix is a staple at Korean university drinking sessions. Not recommended for the faint of heart or liver.</li>
</ul>

<h3>Hangover Prevention and Cures</h3>
<p>Korea takes hangovers so seriously that it has spawned a <strong>$250 million hangover cure industry</strong>. The most effective strategies:</p>
<ul>
<li><strong>Before drinking</strong>: Take a "Condition" (컨디션) or "Dawn 808" (여명808) drink — these herbal supplements cost 3,000-4,000 KRW at any convenience store and contain oriental raisin tree extract, scientifically shown to accelerate alcohol metabolism.</li>
<li><strong>During drinking</strong>: Eat fatty anju (samgyeopsal, cheese) — fat slows alcohol absorption. Alternate soju with water.</li>
<li><strong>After drinking</strong>: Eat haejangguk (해장국, hangover soup) — the next morning's ritual. Varieties include sundaeguk (blood sausage soup, 8,000 KRW), kongnamulguk (bean sprout soup, 7,000 KRW), and the nuclear option, bugeoguk (dried pollack soup, 8,000 KRW). Chains like "Bon Juk" (본죽) and "Hadongkwan" (하동관) serve hangover soups 24 hours.</li>
</ul>
'''

# ─── ID:53 Gwangjang Market (currently ~2056w, need ~500+ more) ───
extra_53b = '''
<h2>Gwangjang Market for Non-Food Shopping</h2>
<p>While food dominates visitors' attention, Gwangjang Market's upper floors house Korea's largest <strong>hanbok (traditional clothing)</strong> and <strong>vintage fabric</strong> market. The second floor has 200+ hanbok shops offering both traditional and modern designs. A custom-made hanbok costs 150,000-500,000 KRW ($109-$363) — significantly cheaper than boutique shops in Insadong or Bukchon that charge 300,000-1,000,000 KRW. Ready-made modernized hanboks (perfect for photos at Gyeongbokgung) cost 50,000-100,000 KRW. Fabric vendors sell silk, cotton, and linen by the meter — Korean quilters and designers source materials here because prices are 40-60% below retail.</p>

<h3>Photography Tips for the Market</h3>
<p>Gwangjang Market is intensely photogenic, but there are unwritten rules. <strong>Always ask before photographing vendors</strong> — most are happy to pose, but some, especially yukhoe stall owners, prefer not to be filmed while handling raw meat. The best light for photography enters the market's central corridor between <strong>10-11 AM</strong> when overhead skylights create dramatic beams. For the famous "alley shot" showing rows of food stalls with steam rising, position yourself at the <strong>intersection near stall #47</strong> (central bindaetteok area) and shoot toward the east gate. Evening visits (after 5 PM) offer moody orange lighting from the vendors' heat lamps — ideal for food photography.</p>

<h3>Combining Gwangjang with Nearby Attractions</h3>
<p>Gwangjang Market sits in a culturally rich neighborhood perfect for a full-day itinerary:</p>
<ul>
<li><strong>Morning (8-10 AM)</strong>: Gwangjang Market breakfast — mayak gimbap and bindaetteok</li>
<li><strong>Mid-morning (10-11:30 AM)</strong>: Walk to <strong>Changgyeonggung Palace</strong> (10-minute walk, 1,000 KRW entry) — far less crowded than Gyeongbokgung</li>
<li><strong>Lunch (12-1 PM)</strong>: Return to the market for yukhoe and sundae</li>
<li><strong>Afternoon (1:30-3 PM)</strong>: <strong>Cheonggyecheon Stream</strong> (5-minute walk) — the restored urban stream has walking paths and public art</li>
<li><strong>Late afternoon (3:30-5 PM)</strong>: <strong>Dongdaemun Design Plaza (DDP)</strong> (8-minute walk) — Zaha Hadid's iconic building with free exhibitions</li>
<li><strong>Evening</strong>: Return to the market for a final round of tteokbokki with makgeolli before the stalls close</li>
</ul>
'''

# ─── ID:67 Jeju Island Food Guide (currently ~2050w, need ~500+ more) ───
extra_67b = '''
<h2>Where to Eat in Jeju: A Neighborhood Guide</h2>

<h3>Jeju City: Urban Dining</h3>
<p>Jeju City's food scene centers around three areas. <strong>Yeon-dong (연동)</strong> is the modern commercial district with upscale restaurants and cafes — try <strong>"Noodle Garden" (면가)</strong> for their renowned gogi guksu (9,000 KRW, consistently rated Jeju's best). <strong>Tapgol Road (탑골로)</strong> near City Hall has a strip of seafood restaurants where locals eat — prices are 20-30% lower than tourist areas. <strong>Arario Museum area</strong> in the old downtown has trendy cafes repurposing vintage buildings, with hallabong juice and matcha desserts for 5,000-8,000 KRW.</p>

<h3>Seogwipo: The Foodie Destination</h3>
<p>Seogwipo's <strong>Lee Jung-seop Street (이중섭거리)</strong> — named after Korea's famous painter — is a charming pedestrian strip with cafes and restaurants. <strong>"Olle Chicken" (올레치킨)</strong> serves Jeju-style fried chicken marinated in hallabong juice (22,000 KRW for a whole chicken). The <strong>Cheonjiyeon Waterfall area</strong> has traditional restaurants serving galchi jorim (braided hairtail fish stew, 15,000-20,000 KRW) — Jeju's other signature fish dish besides okdom.</p>

<h2>Jeju Cafe Culture: Beyond Food</h2>
<p>Jeju has approximately <strong>4,500 cafes</strong> — an astonishing number for an island of 680,000 residents. Many are architecturally stunning, designed as Instagram destinations:</p>
<ul>
<li><strong>Monsant de Aewol (몽상드애월)</strong>: Built by GD (G-Dragon of BIGBANG). Ocean-cliff cafe with floor-to-ceiling windows. Americano 7,000 KRW. Expect 20-30 minute waits on weekends.</li>
<li><strong>Anthracite Jeju (앤트러사이트)</strong>: Converted from an old warehouse, roasts its own beans. Their hallabong cold brew (7,500 KRW) is Jeju in a cup.</li>
<li><strong>Spring Day (봄날)</strong>: Hidden in a tangerine orchard in Hallim. You pick your own tangerines (5,000 KRW for a bag) and the cafe squeezes them into fresh juice while you wait.</li>
<li><strong>Cafe Delmoondo (카페 델문도)</strong>: Minimalist concrete building on the south coast with panoramic ocean views. Their green tea tiramisu (8,000 KRW) is legendary on Korean social media.</li>
</ul>
<p>Jeju's cafe culture is so developed that "cafe hopping" (카페 투어) has become a primary tourist activity — many visitors plan entire itineraries around cafe visits, with food as the connecting thread between stops.</p>

<h3>Seasonal Food Calendar for Jeju</h3>
<p>Planning your Jeju food trip around seasonal ingredients maximizes your culinary experience:</p>
<ul>
<li><strong>January-March</strong>: Hallabong peak season, bok (blowfish) soup, fresh abalone</li>
<li><strong>April-June</strong>: Sea urchin season (best uni of the year), canola flower honey, spring mackerel</li>
<li><strong>July-September</strong>: Hairtail fish peak, summer tangerines, raw horse meat (Jeju specialty, controversial but traditional)</li>
<li><strong>October-December</strong>: Mandarin orange harvest, black pork peak season (pigs are fattened for winter), galchi (cutlassfish) season</li>
</ul>
'''

# ─── ID:57 Korean Fried Chicken Guide (currently ~2001w, need ~550+ more) ───
extra_57b = '''
<h2>Regional Fried Chicken Specialties</h2>
<p>While Seoul has the highest concentration of chicken restaurants, several regional styles deserve a detour.</p>

<h3>Daegu's "Chicken Alley" (닭골목)</h3>
<p>Daegu's Dongin-dong Chicken Alley has been serving fried chicken since the 1970s, making it one of Korea's oldest chicken destinations. The style here is distinctly different: <strong>whole chickens are spatchcocked (flattened) and deep-fried in a single piece</strong>, producing a dramatically crispy skin. <strong>"Chimac Alley Original" (치맥골목 원조)</strong> has been operating for 45 years — their whole flat-fried chicken costs 16,000 KRW and comes with a basket of raw cabbage leaves and pickled daikon. This is the original Korean fried chicken style, predating the yangnyeom craze by decades.</p>

<h3>Chuncheon's Dakgalbi Connection</h3>
<p>Chuncheon (Gangwon Province) is famous for dakgalbi — spicy stir-fried chicken — but its fried chicken scene is equally impressive. <strong>"Myeongdong Dakgalbi Street"</strong> in Chuncheon (not Seoul's Myeongdong) has shops that serve both dakgalbi and fried chicken, letting you experience both styles. A combo meal — half dakgalbi, half fried chicken — runs 30,000 KRW for 2 people and is the ultimate Korean chicken experience.</p>

<h2>Making Korean Fried Chicken at Home</h2>
<h3>The Essential Recipe</h3>
<p>While restaurant-quality Korean fried chicken requires industrial fryers, a home version that's 80% as good is achievable:</p>
<p><strong>Batter</strong>: Mix 1 cup all-purpose flour, 1/2 cup potato starch (the secret ingredient — creates extra crunch), 1 teaspoon baking powder, 1 teaspoon salt, and 1 cup ice-cold water. The batter should be thin — thinner than American fried chicken batter. Korean fried chicken's light, crispy coating comes from this minimal batter approach.</p>
<p><strong>Double-fry method</strong>: Heat oil to 160°C. Fry chicken pieces (drumsticks or wings work best) for 10 minutes. Remove and rest on a wire rack for 8 minutes. Raise oil temperature to 180°C and fry again for 3-4 minutes until deep golden brown.</p>
<p><strong>Yangnyeom sauce</strong>: Combine 3 tablespoons gochujang, 2 tablespoons ketchup, 3 tablespoons corn syrup (or honey), 1 tablespoon soy sauce, 1 tablespoon minced garlic, and 1 tablespoon rice vinegar. Heat in a pan until bubbling, then toss with freshly fried chicken. Serve immediately with pickled radish cubes.</p>

<h3>Where to Buy Ingredients Outside Korea</h3>
<p>Korean fried chicken's key ingredients — potato starch, gochujang, and corn syrup — are available at any H Mart, Lotte Plaza, or Asian grocery store. Online, Amazon carries all essentials. The one ingredient worth splurging on is <strong>Korean corn syrup (물엿, mulyeot)</strong> — it has a different viscosity and sweetness than Western corn syrup, producing a more authentic yangnyeom coating. A 700g bottle costs approximately $5 and lasts for multiple batches.</p>
'''

# ─── ID:65 Korean Convenience Store Food (currently ~2059w, need ~500+ more) ───
extra_65b = '''
<h2>Convenience Store Desserts and Drinks Worth Trying</h2>

<h3>Ice Cream Rankings</h3>
<p>Korean convenience store ice cream is an experience category of its own. The top sellers:</p>
<ul>
<li><strong>Melona (메로나)</strong>: 1,200 KRW. Honeydew melon-flavored ice bar. Korea's most iconic ice cream, exported to 30+ countries. Creamy, not too sweet, and incredibly refreshing in Seoul's summer heat.</li>
<li><strong>Samanco (사만코)</strong>: 1,500 KRW. Fish-shaped ice cream sandwich filled with red bean paste and vanilla ice cream. The wafer shell is crispy and never soggy — an engineering marvel.</li>
<li><strong>Gyeongju Bread Ice Cream (경주빵 아이스크림)</strong>: 1,800 KRW. Based on Gyeongju's famous red bean bread, this ice cream bar has a cookie shell filled with red bean-flavored ice cream. Limited edition that returns each summer.</li>
<li><strong>Babambar (바밤바)</strong>: 1,200 KRW. Chestnut-flavored ice cream bar coated in a chocolate shell with real chestnut pieces. An autumn/winter favorite that's available year-round due to demand.</li>
<li><strong>Jaws Bar (죠스바)</strong>: 800 KRW. Shark-shaped grape popsicle that every Korean child grew up eating. Pure nostalgia at the cheapest price point.</li>
</ul>

<h3>Unique Drinks You Can't Find Elsewhere</h3>
<p>Korean convenience store beverages go far beyond the familiar:</p>
<ul>
<li><strong>Banana Milk (바나나맛 우유)</strong>: 1,500 KRW. Binggrae's iconic squat bottle is Korea's most beloved drink. The banana flavor is artificial and perfect. Available in strawberry, melon, and coffee variants. Over 800 million bottles sold annually.</li>
<li><strong>Milkis (밀키스)</strong>: 1,200 KRW. Carbonated milk drink that sounds terrible but tastes incredible — like Calpico with bubbles. Korean university students drink this as a hangover cure.</li>
<li><strong>Sungnyung Tea (숭늉차)</strong>: 1,800 KRW. Roasted rice tea in a bottle. Nutty, warm (sold heated in winter), and caffeine-free. Perfect after a heavy Korean meal.</li>
<li><strong>Makgeolli (convenience store version)</strong>: 2,500-4,000 KRW. Seoul Jangsoo Makgeolli and Kooksoondang are the best brands available at every store. 6% ABV, fizzy, slightly sweet. The cheapest legitimate alcohol experience in Korea.</li>
</ul>

<h3>Convenience Stores as Late-Night Lifelines</h3>
<p>Korean convenience stores operate 24/7/365 with no exceptions — Christmas, Lunar New Year, typhoon warnings. For travelers, they serve as de facto service centers after hours:</p>
<ul>
<li><strong>Phone charging</strong>: Most stores sell portable charger rentals (1,000 KRW/hour) or Lightning/USB-C cables (5,000-8,000 KRW)</li>
<li><strong>Printing/copying</strong>: Multifunction printers available at most CU and GS25 locations (50-100 KRW per page)</li>
<li><strong>Umbrella purchase</strong>: Sudden rain? Every store stocks compact umbrellas (5,000-8,000 KRW)</li>
<li><strong>Medicine</strong>: Basic over-the-counter medications — headache pills (Tylenol equivalent, 2,000 KRW), stomach medicine, bandages</li>
<li><strong>SIM cards</strong>: Some stores near airports and tourist areas sell prepaid SIM cards for foreigners (10,000-30,000 KRW for 3-30 days of data)</li>
</ul>
<p>Korean convenience stores are arguably the most useful single establishment for any traveler — mastering them transforms your entire Korea trip experience.</p>
'''

# ─── Execute Round 2 ───
print("=== Round 2: Expanding 7 posts ===")

posts2 = [
    (42, extra_42b, "Korean Food Show Guide"),
    (69, extra_69b, "Korean Drinking Food Anju"),
    (63, extra_63b, "Soju Guide for Beginners"),
    (53, extra_53b, "Gwangjang Market Food Guide"),
    (67, extra_67b, "Jeju Island Food Guide"),
    (57, extra_57b, "Korean Fried Chicken Guide"),
    (65, extra_65b, "Korean Convenience Store Food"),
]

results = {}
for pid, extra, title in posts2:
    print(f"\n--- {title} (ID:{pid}) ---")
    wc = add_content(pid, extra)
    results[pid] = wc

print("\n=== ROUND 2 RESULTS ===")
for pid, wc in results.items():
    status = "OK" if wc >= 2500 else "NEEDS MORE"
    print(f"  ID:{pid} → {wc} words [{status}]")
