#!/usr/bin/env python3
"""Round 2: Push all 8 posts above 2500 words."""
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

# ── ID:51 — needs ~150 more words ──
extra_51 = """
<h2>Emergency Phrases: When Things Go Wrong at a Korean Restaurant</h2>
<p>Even with perfect preparation, unexpected situations arise. These emergency phrases will help you handle problems confidently without resorting to English.</p>
<p>If you have a food allergy and feel symptoms: <strong>"알레르기가 있어요. 도와주세요"</strong> (I have an allergy. Please help me). If food has gone bad or tastes wrong: <strong>"이거 상한 것 같아요"</strong> (I think this has gone bad). If you accidentally order something you cannot eat: <strong>"죄송한데 이거 바꿀 수 있을까요?"</strong> (I'm sorry, can I change this?). If you need to find a restroom urgently: <strong>"화장실 어디예요?"</strong> (Where is the restroom?). Restaurant restrooms in Korea are frequently located outside the restaurant in the building hallway — do not panic if there is no bathroom sign inside the restaurant.</p>
<p>For food poisoning concerns (rare but possible), Korean pharmacies (약국, yakguk) are found on virtually every block and pharmacists can recommend over-the-counter remedies. The phrase <strong>"배가 아파요"</strong> (My stomach hurts) or <strong>"체했어요"</strong> (I have indigestion) will get you the right medication immediately. Pharmacies display a green cross symbol and most are open until 8-9 PM on weekdays.</p>
"""

# ── ID:59 — needs ~300 more words ──
extra_59 = """
<h2>Temple Stay Booking Guide: Practical Information for Visitors</h2>
<p>Experiencing temple food firsthand through a temple stay program is one of Korea's most transformative travel experiences. Here is everything you need to know about booking and preparing for your visit.</p>

<h3>How to Book a Temple Stay</h3>
<p>The official booking platform is <strong>templestay.com</strong>, operated by the Jogye Order of Korean Buddhism. The site offers programs at over 130 temples nationwide, ranging from one-night introductory stays (50,000-80,000 won) to week-long intensive meditation retreats (200,000-500,000 won). Most programs include all meals, accommodation, temple activities, and a monastic uniform.</p>
<p>Popular temples for food-focused stays include <strong>Jinkwansa (진관사)</strong> in Seoul, famous for its cooking classes where you prepare temple food alongside monks. <strong>Haeinsa (해인사)</strong> in Hapcheon offers the most authentic traditional experience — this UNESCO-listed temple houses the Tripitaka Koreana and maintains strict traditional eating practices. <strong>Woljeongsa (월정사)</strong> in Pyeongchang provides a mountain forest setting where foraging for wild vegetables is part of the program.</p>

<h3>What to Expect During Meals</h3>
<p>Temple meals follow strict protocols. You eat in silence. You take only what you will finish — wasting food is considered a serious transgression. After eating, you clean your bowls using pickled radish and warm water, then drink the cleaning water. This practice, called <strong>"balwoo gongyang" (발우공양)</strong>, teaches mindfulness and respect for food. First-time visitors often find this practice challenging but profoundly meaningful — many describe it as the most memorable part of their temple stay.</p>
<p>Expect to wake at 3:30-4:00 AM for morning chanting, eat breakfast by 6:30 AM, and have your last food by 6:00 PM. The schedule is non-negotiable. Bring warm layers (temples in mountains can be cold even in summer), minimal personal items, and an open mind. Mobile phones should be turned off or left in your room during communal activities.</p>
"""

# ── ID:55 — needs ~400 more words ──
extra_55 = """
<h2>Beyond Bibimbap: Jeonju's Complete Food Scene</h2>
<p>While bibimbap rightfully claims the spotlight, limiting a Jeonju food trip to just bibimbap would be a culinary sin. The city — designated a <strong>UNESCO Creative City of Gastronomy</strong> in 2012 — offers a food culture so rich that serious food travelers spend 2-3 days eating their way through its specialties.</p>

<h3>Jeonju Hanok Village: The Food Tourist's Playground</h3>
<p>The Hanok Village (한옥마을), a preserved neighborhood of 700+ traditional Korean houses, has become Korea's most concentrated food tourism zone. Walking its narrow streets, you will encounter:</p>
<ul>
<li><strong>Choco-pie (초코파이)</strong> — Jeonju's artisan version of the famous Korean snack, hand-dipped in premium chocolate with flavors like matcha, strawberry, and traditional injeolmi (rice cake). Shops sell 3-5 per box for 5,000-8,000 won.</li>
<li><strong>PNB bakery (풍년제과)</strong> — Jeonju's legendary bakery since 1951, famous for its butter cake and red bean bread. The original store near Jungang Market has lines out the door on weekends.</li>
<li><strong>Makgeolli bars (막걸리집)</strong> — Jeonju-style makgeolli is served with an astonishing spread of free anju (drinking snacks) — order one kettle of rice wine and receive 8-15 side dishes. The Samcheon-dong makgeolli alley near Hanok Village is the best area for this experience.</li>
<li><strong>Kongnamul-gukbap (콩나물국밥)</strong> — Bean sprout rice soup is Jeonju's second-most-famous dish after bibimbap. Made with those same premium Jeonju bean sprouts, the soup is a traditional hangover cure and early-morning breakfast. The best restaurants, like Hyundai-ok (현대옥), serve it 24 hours with a side of perfectly fermented kkakdugi radish kimchi.</li>
</ul>

<h3>Getting to Jeonju and Transportation</h3>
<p>From Seoul, the KTX high-speed train reaches Jeonju Station in approximately 1 hour 40 minutes (departing from Yongsan Station). Tickets cost around 34,000 won one-way. From the station, Bus 119 or a taxi (10,000 won) takes you to Hanok Village. Alternatively, express buses from Seoul's Central City Terminal run every 20-30 minutes, taking about 2.5 hours and costing 17,000-25,000 won.</p>
<p>Within Jeonju, most food destinations in and around Hanok Village are walkable. For restaurants outside the village, taxis are cheap (base fare 4,800 won) and readily available. The city also has a public bicycle rental system called Jeonju Bike that costs just 1,000 won per hour — a pleasant way to explore the flat city streets between meals.</p>
"""

# ── ID:11 — needs ~400 more words ──
extra_11 = """
<h2>Korean Dumpling Ordering Guide: What to Know Before You Go</h2>
<p>Ordering at a traditional mandu restaurant like Bangi Gullim can be confusing for first-time visitors. Korean dumpling restaurants typically offer multiple preparation methods for the same filling, and understanding the options ensures you get exactly the experience you want.</p>

<h3>Cooking Method Options</h3>
<ul>
<li><strong>Mul-mandu (물만두)</strong> — Boiled dumplings served in broth. The gentlest cooking method, producing soft, delicate dumplings that absorb broth flavor. This is the style served in Bangi Gullim's hot pot.</li>
<li><strong>Jjin-mandu (찐만두)</strong> — Steamed dumplings. Slightly firmer than boiled, with a more concentrated filling flavor since no broth dilutes the taste. Often served in bamboo steamers.</li>
<li><strong>Gun-mandu (군만두)</strong> — Pan-fried dumplings (similar to Japanese gyoza). One side is crispy-golden while the other remains soft. Best for people who enjoy textural contrast.</li>
<li><strong>Twigim-mandu (튀김만두)</strong> — Deep-fried dumplings. Crunchy exterior, hot juicy filling. Popular as anju (drinking snack) with beer or soju.</li>
</ul>

<h3>Pairing Your Mandu: Drinks and Side Dishes</h3>
<p>Korean mandu pairs exceptionally well with specific beverages and accompaniments. At traditional restaurants, the classic combination is mandu with <strong>dongchimi (동치미)</strong> — cold radish water kimchi. The icy, tangy dongchimi broth cuts through the richness of the dumpling filling and acts as a palate cleanser between bites.</p>
<p>For alcoholic pairing, <strong>makgeolli (막걸리)</strong> is the traditional choice. The slightly sweet, creamy rice wine complements the savory dumpling filling without overpowering it. Ask for <strong>saeng-makgeolli (생막걸리)</strong> — unpasteurized draft version — if available. The carbonation from active fermentation adds a pleasant fizz that cuts through the dumpling's richness.</p>
<p>Another excellent pairing is <strong>soju (소주)</strong> with gun-mandu or twigim-mandu. The crispy fried dumpling and clean soju combination is a cornerstone of Korean drinking culture. For the full Korean drinking experience, order a plate of mandu alongside some additional anju: <a href="/soju-guide-for-beginners-how-to-drink-koreas-national-spirit-like-a-local/">our soju guide</a> explains the complete etiquette and pairing tradition.</p>
<p>Bangi Gullim's location near Jamsil means you can combine your mandu meal with nearby attractions. Lotte World amusement park is a 10-minute walk, Seokchon Lake (석촌호수) — famous for its cherry blossoms in April — is just across the street, and the 555-meter Lotte World Tower observation deck offers panoramic views of Seoul. Plan your mandu meal as either a pre-adventure fuel stop or a satisfying post-exploration dinner.</p>
"""

# ── ID:13 — needs ~500 more words ──
extra_13 = """
<h2>Korean Home Cooking 101: Dishes You Will Find at Banchan Buffets</h2>
<p>The beauty of a banchan buffet like World Bap is that it serves as a living textbook of Korean home cooking. Each dish on the buffet line represents a technique and tradition passed down through generations. Here are the foundational dishes you should understand and try:</p>

<h3>Kimchi Varieties: Beyond Napa Cabbage</h3>
<p>While baechu-kimchi (napa cabbage kimchi) is the most famous, Korean cuisine includes over 200 documented types of kimchi. A well-stocked banchan buffet will feature at least 5-8 varieties:</p>
<ul>
<li><strong>Kkakdugi (깍두기)</strong> — Cubed radish kimchi with a satisfying crunch. The slight sweetness of Korean radish balances the spice.</li>
<li><strong>Chonggak-kimchi (총각김치)</strong> — Whole young radish kimchi with the green tops still attached. Crunchy and refreshing.</li>
<li><strong>Oi-sobagi (오이소박이)</strong> — Stuffed cucumber kimchi, filled with chive and garlic seasoning. Best in summer when cucumbers are in peak season.</li>
<li><strong>Mul-kimchi (물김치)</strong> — Water kimchi, a mild, refreshing variety served in its brine. The liquid is as important as the vegetables — drink it as a cold, probiotic-rich soup.</li>
<li><strong>Gat-kimchi (갓김치)</strong> — Mustard green kimchi with an assertive, peppery bite. A Jeolla Province specialty that World Bap, being in Gwangju, showcases particularly well.</li>
</ul>

<h3>Essential Banchan Categories Every Visitor Should Know</h3>
<p><strong>Bokkeum (볶음) — Stir-fried dishes:</strong> Ojingeo-bokkeum (spicy stir-fried squid), jeyuk-bokkeum (spicy pork), and myeolchi-bokkeum (stir-fried anchovies with nuts) are staples. These dishes tend to be more heavily seasoned and work as flavor anchors for your rice.</p>
<p><strong>Muchim (무침) — Seasoned cold dishes:</strong> Raw or blanched vegetables dressed in sesame oil, garlic, and salt or soy sauce. Sigeumchi-namul (spinach), kongnamul-muchim (bean sprouts), and doraji-muchim (bellflower root) are the most common. These lighter dishes provide contrast to the heavier braised and stir-fried options.</p>
<p><strong>Jjim (찜) — Steamed/braised dishes:</strong> Gyeran-jjim (steamed egg custard) is the most beloved — a fluffy, custardy egg dish that every Korean associates with home cooking. Galbi-jjim (braised short ribs) appears at premium buffets but is less common at budget-tier restaurants like World Bap.</p>
<p><strong>Gui (구이) — Grilled items:</strong> Grilled fish is the star of this category. Godeungeo-gui (grilled mackerel) and galchi-gui (grilled cutlassfish) are the most prized. At a buffet, these go fast — time your visit to the grill station when a fresh batch comes out.</p>

<h2>Making the Most of Your Gwangju Food Trip</h2>
<p>If World Bap is your first stop in Gwangju, here is how to build a full food-focused day around it:</p>
<ul>
<li><strong>Breakfast (7-9 AM)</strong> — Yukjeon Market (육전 시장) for Korean-style breakfast: gukbap (rice soup) or sundae-guk (blood sausage soup) at a market stall. Budget: 7,000-9,000 won.</li>
<li><strong>Lunch (11:30 AM-1 PM)</strong> — World Bap banchan buffet. Go early to avoid the noon rush. Budget: 8,000 won.</li>
<li><strong>Afternoon snack (3 PM)</strong> — Gwangju's 1913 Songjeong Station Market, a revitalized heritage market with artisan coffee shops and modern takes on traditional snacks.</li>
<li><strong>Dinner (6-8 PM)</strong> — Gwangju is famous for <strong>ori-tang (오리탕)</strong>, spicy duck stew, and <strong>tteokgalbi (떡갈비)</strong>, grilled minced short rib patties. The Chungjang-ro area has excellent options for both.</li>
<li><strong>Late night (10 PM+)</strong> — Gwangju's Geumnam-ro area for <strong>chimaek (치맥)</strong> — <a href="/korean-fried-chicken-guide-why-kfc-means-something-different-in-korea/">Korean fried chicken</a> and beer. Gwangju's fried chicken scene is surprisingly competitive.</li>
</ul>
"""

# ── ID:29 — needs ~500 more words ──
extra_29 = """
<h2>Gangwon Province Road Trip: A Food-Focused Driving Guide</h2>
<p>Hongcheon's central location in Gangwon Province makes it an ideal starting point or stopover on a larger food road trip through Korea's most scenic region. Here is a practical driving itinerary that connects Hongcheon's culinary highlights with nearby food destinations.</p>

<h3>Route 1: Hongcheon → Chuncheon → Nami Island (Half Day)</h3>
<p>Drive 30 minutes west from Hongcheon to <strong>Chuncheon (춘천)</strong>, the provincial capital and birthplace of <strong>dakgalbi (닭갈비)</strong> — spicy stir-fried chicken with rice cakes, cabbage, and sweet potato. Chuncheon's Dakgalbi Street (닭갈비골목) near Myeongdong has over 20 competing restaurants, all serving the same dish with slight variations. The classic experience: order dakgalbi (12,000-15,000 won per person), add cheese topping (3,000 won), and finish with bokkeumbap (fried rice) made in the remaining sauce on the hotplate.</p>
<p>From Chuncheon, drive 20 minutes south to <strong>Nami Island (남이섬)</strong> for a post-meal walk through the famous tree-lined paths. The island's <a href="/how-to-order-food-in-korean-25-essential-phrases-every-traveler-needs/">restaurants serve decent Korean food</a>, but Chuncheon's options are far superior — eat before crossing.</p>

<h3>Route 2: Hongcheon → Pyeongchang → Gangneung (Full Day)</h3>
<p>Drive 1.5 hours east through stunning mountain passes to <strong>Pyeongchang (평창)</strong>, the 2018 Winter Olympics host city. Stop at the Bongpyeong buckwheat village for the freshest memil-jeonbyeong and makguksu you will find anywhere. Continue 40 minutes east to <strong>Gangneung (강릉)</strong> on the coast for a completely different food experience: fresh sashimi at Jumunjin Port, tofu village cuisine at Chodang (초당두부마을), and Korea's best specialty coffee scene — Gangneung hosts an annual Coffee Festival and has more independent coffee roasters per capita than any Korean city outside Seoul.</p>

<h3>Driving Tips for Gangwon Province</h3>
<ul>
<li><strong>Toll costs</strong> — The Seoul-Hongcheon expressway toll is approximately 5,000 won each way. Budget 15,000-20,000 won total for a Gangwon day trip in tolls.</li>
<li><strong>Gas stations</strong> — Fill up in Hongcheon town before heading into mountain areas. Gas stations become sparse on rural mountain roads.</li>
<li><strong>Winter driving (December-March)</strong> — Snow chains are mandatory on Gangwon mountain passes. Rental cars usually include chains in winter; verify before departing.</li>
<li><strong>Rest stops (휴게소)</strong> — Korean highway rest stops serve surprisingly good food. The Hongcheon rest stop on the Seoul-Yangyang expressway is known for its buckwheat noodles and pine nut snacks — a preview of what awaits in Hongcheon proper.</li>
</ul>

<h2>Where to Stay in Hongcheon: Accommodation Guide</h2>
<p>Hongcheon offers accommodation for every budget, from luxury ski resorts to traditional countryside guesthouses:</p>
<ul>
<li><strong>Vivaldi Park (비발디파크)</strong> — The area's largest resort, with ski slopes in winter and water park in summer. Rooms from 150,000 won/night. Multiple on-site restaurants, though town restaurants offer better value.</li>
<li><strong>Pension (펜션) stays</strong> — Korea's version of vacation rentals. Hongcheon has dozens of pensions in scenic mountain and riverside locations, typically 80,000-150,000 won/night with full kitchen facilities. Ideal if you want to buy ingredients at Hongcheon's traditional market and cook your own Korean meals.</li>
<li><strong>Minbak (민박)</strong> — Traditional homestay accommodation in local homes. The most authentic and affordable option at 30,000-50,000 won/night. Hosts sometimes provide homemade breakfast. Limited English but maximum cultural immersion.</li>
</ul>
"""

# ── ID:27 — needs ~600 more words ──
extra_27 = """
<h2>The Art of Korean Gukbap: Rice Soup Culture Explained</h2>
<p>Gukbap (국밥) — literally "soup rice" — is one of Korea's most democratic food traditions. Unlike elaborate dishes that require expensive ingredients and skilled preparation, gukbap originated as workers' fuel: cheap, filling, and available from early morning. Understanding gukbap culture provides essential context for appreciating Pohang Halmae-jip's somoori-gukbap.</p>

<h3>Regional Gukbap Varieties Across Korea</h3>
<p>Every major Korean city has its own gukbap specialty, each reflecting local ingredients and economic history:</p>
<ul>
<li><strong>Busan — Dwaeji-gukbap (돼지국밥)</strong> — Pork bone soup with rice. <a href="/busan-food-guide-8-dishes-you-can-only-find-in-koreas-coastal-city/">Busan's most iconic breakfast food</a>, descended from Korean War-era refugees who used every available pork part. The milky broth is intensely porky and deeply satisfying.</li>
<li><strong>Seoul — Seolleongtang (설렁탕)</strong> — Ox bone soup. The capital's version uses leg bones rather than head meat, producing a lighter broth. Traditionally served with thin wheat noodles (소면) in addition to rice.</li>
<li><strong>Jeonju — Kongnamul-gukbap (콩나물국밥)</strong> — Bean sprout soup with rice. Jeonju's famous plump sprouts in a spicy or clear broth, often topped with a raw egg that cooks in the hot soup.</li>
<li><strong>Daegu — Ttaro-gukbap (따로국밥)</strong> — "Separate" rice soup where the rice comes in its own bowl instead of submerged in broth. This allows diners to control how much rice they mix into the soup.</li>
<li><strong>Pohang — Somoori-gukbap (소머리국밥)</strong> — Ox head soup. The head meat's higher collagen content produces the richest, thickest broth of all gukbap varieties. Pohang Halmae-jip exemplifies this tradition.</li>
</ul>

<h3>Gukbap Etiquette and Customs</h3>
<p>Gukbap restaurants operate on an unwritten social contract. The soup arrives unseasoned — you customize it with the table condiments (salt, green onion, chili flakes, salted shrimp). This is not laziness; it is respect for individual taste preferences. A good gukbap restaurant is judged by three criteria: broth depth, meat quality, and condiment freshness. If the green onions look wilted or the salt shaker is crusted, leave.</p>
<p>Eating speed matters in gukbap culture. These restaurants cater to working people on time constraints. While you should not rush, lingering for an hour over a single bowl is considered inconsiderate during peak hours. The typical gukbap meal takes 15-25 minutes — arrive, eat, pay, leave. This efficiency is part of the culture, not a lack of hospitality.</p>

<h2>Pohang Travel Essentials: Getting There and Getting Around</h2>
<p>Pohang is accessible by multiple transportation methods from Seoul and other major Korean cities:</p>

<h3>By KTX High-Speed Train</h3>
<p>The KTX from Seoul Station to Pohang Station takes approximately 2 hours 20 minutes, with tickets costing around 44,000 won. Trains run roughly every 1-2 hours throughout the day. Pohang Station is located in the city center, making it convenient for reaching restaurants and attractions by bus or taxi.</p>

<h3>By Express Bus</h3>
<p>Express buses from Seoul's East Seoul Terminal (동서울터미널) reach Pohang in approximately 4 hours, costing 25,000-35,000 won depending on the bus class. This is the budget option, and overnight buses are available for maximum time efficiency.</p>

<h3>Local Transportation in Pohang</h3>
<p>Within Pohang, the city bus network covers major attractions and food destinations. However, for a food-focused visit to multiple restaurants and markets, taxis are the practical choice. Pohang taxis are affordable (base fare 4,800 won, most trips within the city under 8,000 won) and readily available. For coastal destinations like Homigot or the seafood villages north of the city, a rental car provides the most flexibility.</p>

<h3>Best Time to Visit Pohang</h3>
<p>Each season offers a different Pohang food experience:</p>
<ul>
<li><strong>Spring (April-May)</strong> — Cherry blossoms along the Hyeongsangang River, fresh squid season, pleasant temperatures for market walking.</li>
<li><strong>Summer (July-August)</strong> — Beach season at Yeongildae Beach, fresh mul-hoe (cold raw fish soup) is at its peak, but humidity is intense.</li>
<li><strong>Autumn (September-November)</strong> — The best overall season. Comfortable weather, excellent seafood, and the surrounding countryside turns golden.</li>
<li><strong>Winter (December-February)</strong> — Gwamegi season. The semi-dried fish is only available in winter, making this the must-visit season for adventurous food travelers.</li>
</ul>
"""

# ── ID:23 — needs ~600 more words ──
extra_23 = """
<h2>How to Eat Monkfish Soup Like a Korean: Step-by-Step Guide</h2>
<p>Monkfish soup (아귀탕) at a restaurant like Imja is a communal dining experience with a specific eating rhythm. Following this sequence ensures you experience every flavor and texture the dish offers.</p>

<h3>Step 1: Observe Before Eating</h3>
<p>When the pot arrives at your table, still bubbling vigorously, take a moment to observe the arrangement. A well-made monkfish soup has distinct zones: the fish pieces sit in the center, bean sprouts line the bottom and edges, and vegetables (radish, tofu, crown daisy) are scattered throughout. The broth should be a deep red-orange color with visible chili flakes and a thin layer of oil on the surface that indicates proper seasoning.</p>

<h3>Step 2: Start with the Broth</h3>
<p>Ladle the broth into your personal bowl first. The initial sip tells you everything about the restaurant's quality. Good monkfish broth should be spicy but not overwhelmingly so, with a underlying sweetness from the fish and sprouts. If the broth tastes like pure gochugaru (red pepper flakes) without depth, the restaurant has cut corners on simmering time.</p>

<h3>Step 3: Eat the Fish with Accompaniments</h3>
<p>Use chopsticks to pick up fish pieces and eat them with a dip in the soy-vinegar sauce provided. Alternate between monkfish, bean sprouts, and rice to create balanced bites. The liver pieces (darker, creamier portions) should be eaten separately to appreciate their distinctive richness.</p>

<h3>Step 4: The Rice Finish</h3>
<p>When the fish is finished and the broth has reduced and concentrated, add a bowl of rice directly into the remaining soup. Stir it thoroughly, scraping the bottom of the pot where the most concentrated flavors have settled. Let the rice absorb the broth for 2-3 minutes. This final rice porridge is often the best part of the entire meal — the cumulative flavor of all ingredients concentrated into each spoonful.</p>

<h2>Monkfish in Korean Medicine: Health Benefits and Traditional Uses</h2>
<p>Korean food culture does not separate nutrition from medicine — the concept of <strong>"약식동원" (yaksik-dongwon)</strong> holds that food and medicine share the same origin. Monkfish has specific health associations in Korean traditional medicine that explain its enduring popularity beyond mere taste.</p>
<p><strong>Collagen content</strong> — Monkfish skin and cartilage are extremely rich in collagen, the protein responsible for skin elasticity. Korean women have long consumed monkfish soup as a beauty food, believing that the dietary collagen improves skin texture and delays wrinkles. While modern science debates the efficacy of dietary collagen (stomach acid breaks it down before absorption), the association remains powerful in Korean food culture.</p>
<p><strong>Low calorie, high protein</strong> — Monkfish flesh contains approximately 76 calories per 100g with 14.5g of protein, making it one of the leanest fish proteins available. For comparison, salmon has 208 calories per 100g. This nutritional profile makes agwi-jjim popular among Korean dieters who want satisfying meals without excessive calories.</p>
<p><strong>Hangover recovery</strong> — The combination of spicy broth, bean sprouts (containing hangover-fighting asparagine), and protein-rich fish makes monkfish soup a popular morning-after meal in Korea. Many monkfish restaurants in Gangnam open as early as 7 AM specifically to serve the business district's hangover crowd.</p>
<p><strong>Liver as superfood</strong> — Monkfish liver (아귀간) contains high concentrations of vitamins A and D, omega-3 fatty acids, and DHA. In Japanese cuisine, the equivalent ankimo is considered a winter delicacy comparable to foie gras. Korean preparations — typically steamed and sliced with a ponzu-like dipping sauce — preserve more of these nutrients than the seared preparations common in Western fine dining.</p>

<h2>Planning Your Gangnam Food Tour Around Imja</h2>
<p>If you are visiting Imja for monkfish soup, build a full Gangnam food day around it. Despite Gangnam's reputation for luxury shopping and K-pop entertainment agencies, the neighborhood has an exceptional local food scene that many tourists miss entirely.</p>
<ul>
<li><strong>Morning (8-10 AM)</strong> — Start with a traditional Korean breakfast at one of Gangnam's gukbap restaurants. Seolleongtang (ox bone soup) or haejang-guk (hangover soup) establishments near Gangnam Station open early and serve hearty breakfasts for 8,000-12,000 won.</li>
<li><strong>Lunch (12-2 PM)</strong> — Imja for monkfish soup. Arrive before noon to avoid the business lunch rush that peaks between 12:30 and 1:30 PM.</li>
<li><strong>Afternoon café (3-5 PM)</strong> — Gangnam's Garosugil (가로수길) neighborhood, a 10-minute taxi ride from Imja, is Seoul's premier café district. The tree-lined street features dozens of specialty coffee shops, dessert cafes, and boutiques. Try bingsu (빙수, shaved ice dessert) at any established café — the Gangnam versions are among Seoul's most elaborate.</li>
<li><strong>Dinner (7-9 PM)</strong> — Return to Gangnam's restaurant scene for Korean BBQ. The area around Yeoksam Station has excellent <a href="/korean-bbq-etiquette-12-rules-every-first-timer-needs-to-know/">Korean BBQ restaurants</a> where premium Hanwoo beef is available at prices 20-30% lower than equivalent restaurants in Itaewon or Myeongdong.</li>
</ul>
"""

# ── Execute round 2 ──
print("=== Round 2: Pushing all posts to 2500+ ===\n")

posts = [
    (51, extra_51, "How to Order Food in Korean"),
    (59, extra_59, "Korean Temple Food"),
    (55, extra_55, "Jeonju vs Seoul Bibimbap"),
    (11, extra_11, "Bangi Gullim Mandu"),
    (13, extra_13, "World Bap Korean Buffet"),
    (29, extra_29, "Hongcheon Food Trip"),
    (27, extra_27, "Pohang Halmae-jip"),
    (23, extra_23, "Imja Monkfish Soup"),
]

results = []
for pid, extra, title in posts:
    print(f"Expanding: {title} (ID:{pid})...")
    wc = add_content(pid, extra)
    results.append((pid, title, wc))

print("\n=== FINAL RESULTS ===")
under = []
for pid, title, wc in results:
    status = "OK" if wc >= 2500 else "NEEDS MORE"
    print(f"  ID:{pid} | {wc}w | {status} | {title}")
    if wc < 2500:
        under.append((pid, title, wc))

if under:
    print(f"\n{len(under)} posts still under 2500 words")
else:
    print("\nAll 8 posts at 2500+ words!")
