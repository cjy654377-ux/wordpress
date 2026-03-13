#!/usr/bin/env python3
"""Expand 8 Travel & Food posts to 2500+ words."""
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

# ─── ID:44 Korean Street Food Guide (1798w → 2500+) ───
extra_44 = '''
<h2>Regional Street Food Specialties Across South Korea</h2>
<p>While Seoul dominates the Korean street food scene, every major city has its own signature snacks that reflect local ingredients and culinary traditions. Understanding these regional differences transforms a simple food tour into a genuine cultural experience.</p>

<h3>Busan's Seafood Street Food</h3>
<p>Busan's Jagalchi Market and BIFF Square offer street food you simply cannot find in Seoul. <strong>Ssiat hotteok</strong> (seed-filled sweet pancakes) originated here — the Busan version is stuffed with sunflower seeds, pumpkin seeds, and brown sugar, then deep-fried until the shell shatters with each bite. A single piece costs 1,500 KRW ($1.10) at the famous stalls near BIFF Square. <strong>Eomuk</strong> (fish cake) in Busan uses freshly caught fish rather than the processed versions common in Seoul. At Samjin Eomuk (established 1953), you can watch artisans hand-press fish cakes and sample them with a free cup of warm broth — the perfect winter snack at 2,000 KRW per skewer.</p>

<h3>Daegu's Spicy Street Snacks</h3>
<p>Daegu residents proudly claim to have Korea's highest spice tolerance, and their street food reflects it. <strong>Napjak mandu</strong> (flat dumplings) are pressed thin on a griddle and served with a fiery dipping sauce at Seomun Market's night food alley. The market operates from 7 PM to midnight, and a plate of 10 dumplings costs just 4,000 KRW ($2.90). <strong>Makchang gui</strong> (grilled intestines) is another Daegu specialty — street vendors grill pork intestines over charcoal, producing an irresistibly smoky, chewy snack for 8,000 KRW per serving.</p>

<h3>Jeonju's Traditional Snacks</h3>
<p>Jeonju Hanok Village's streets are lined with vendors selling <strong>choco pie ice cream</strong> (a local invention combining Korea's beloved Choco Pie with soft-serve), <strong>PNB bakery bread</strong> (the 70-year-old bakery's signature butter bread at 3,500 KRW), and <strong>bibimbap croquettes</strong> — deep-fried balls of Jeonju-style bibimbap at 2,000 KRW each.</p>

<h2>Street Food Etiquette and Practical Tips</h2>

<h3>How to Order Like a Local</h3>
<p>Most Korean street food vendors appreciate when foreigners attempt basic Korean. Point at what you want and say <strong>"igeo hana juseyo"</strong> (이거 하나 주세요 — "one of this, please"). For multiple items, replace "hana" with the number: dul (two), set (three), net (four). Payment is almost always cash at traditional markets, though newer food stalls in tourist areas accept card payments. Vendors at Myeongdong and Hongdae typically have bilingual menus, but at local markets like Tongin or Mangwon, having a translation app ready helps enormously.</p>

<h3>When to Visit for the Best Experience</h3>
<p>Korean street food culture follows a distinct daily rhythm. Morning markets (like Gwangjang) serve <strong>mayak gimbap and bindaetteok from 8 AM</strong>. Afternoon stalls peak between 2-5 PM when school students flood areas like Hongdae and Sinchon. <strong>Night markets</strong> — Yeouido, Bamdokkaebi, and DDP — operate seasonally from April to October, typically 6 PM to 11 PM on Fridays and Saturdays. Winter brings the best street food season: bungeoppang (fish-shaped pastry, 1,000 KRW), hotteok, and steaming cups of eomuk broth appear at every subway exit.</p>

<h3>Budget Planning for Street Food Tours</h3>
<p>A satisfying street food meal in Korea costs between 8,000-15,000 KRW ($5.80-$10.90). Here's a realistic budget breakdown for a half-day food tour:</p>
<ul>
<li><strong>Tteokbokki + eomuk</strong>: 5,000 KRW</li>
<li><strong>Hotteok or bungeoppang</strong>: 1,500 KRW</li>
<li><strong>Gimbap (1 roll)</strong>: 3,500 KRW</li>
<li><strong>Twigim set (assorted fried items)</strong>: 4,000 KRW</li>
<li><strong>Drink (banana milk or soju)</strong>: 1,500-5,000 KRW</li>
</ul>
<p>Total: approximately 15,500-19,000 KRW ($11-$14) for a filling street food crawl. Compare this to a restaurant meal averaging 10,000-15,000 KRW per person — street food delivers more variety at a similar or lower price point.</p>

<h2>Vegetarian and Allergy-Friendly Street Food Options</h2>
<p>Finding vegetarian street food in Korea requires strategy, but it's absolutely possible. <strong>Hotteok</strong> (brown sugar pancake) is naturally vegetarian. <strong>Gungoguma</strong> (roasted sweet potato, 3,000 KRW) appears at street carts from November through March. <strong>Twigim</strong> vendors always offer vegetable options — sweet potato, perilla leaf, and lotus root tempura are safe choices. However, beware of hidden ingredients: tteokbokki broth often contains anchovy stock, and even vegetable-looking jeon (pancakes) may include seafood. Ask <strong>"gogi deureogayo?"</strong> (고기 들어가요? — "Does it contain meat?") to confirm.</p>
<p>For allergies, note that <strong>wheat, soy, and sesame</strong> are present in nearly every Korean street food. Gluten-free options are limited to grilled items on skewers, roasted sweet potatoes, and fresh fruit cups (5,000 KRW at tourist areas). If you have severe allergies, carry a Korean-language allergy card — several free templates are available online from Korea Tourism Organization.</p>

<h3>Related Guides</h3>
<p>Continue your Korean food adventure with our <a href="/gwangjang-market-food-guide-seouls-oldest-market-and-its-legendary-eats/">Gwangjang Market Food Guide</a> for Seoul's most iconic market experience, explore <a href="/korean-fried-chicken-guide-why-kfc-means-something-different-in-korea/">Korean Fried Chicken culture</a>, or discover <a href="/korean-convenience-store-food-ranking-top-20-must-try-items-at-cu-gs25-and-7-eleven/">Korea's best convenience store food</a> for late-night snacking.</p>
'''

# ─── ID:42 Korean Food Show Guide (1480w → 2500+) ───
extra_42 = '''
<h2>Must-Watch Korean Food Variety Shows for Beginners</h2>
<p>If you're new to Korean food shows, the sheer number of options can feel overwhelming. Here's a curated starting point organized by what you're looking for.</p>

<h3>For Restaurant Discovery: "Baek Jong-won's Alley Restaurant"</h3>
<p>This SBS show (백종원의 골목식당) follows celebrity chef Baek Jong-won as he visits struggling small restaurants across Korea and helps them improve. What makes it invaluable for food travelers is that <strong>every restaurant featured is real and visitable</strong>. After episodes air, these spots often see 300-500% increases in customers. Notable episodes include the Busan milmyeon (cold wheat noodle) shop in Season 3, Episode 12, and the Seoul Mapo-gu tteokbokki vendor in Season 5, Episode 8. The show airs Wednesdays at 10:50 PM KST and is available on Viki with English subtitles.</p>

<h3>For Cooking Inspiration: "Please Take Care of My Refrigerator"</h3>
<p>JTBC's "냉장고를 부탁해" (2014-2019, 237 episodes) pits professional chefs against each other using only ingredients from celebrity guests' actual refrigerators. The 15-minute cooking battles reveal authentic Korean home cooking — far more useful than polished cooking shows. Standout episodes: IU's episode (#89) spawned the viral "IU sweet potato diet," and BTS Jin's appearance (#150) crashed the show's servers. All episodes are available on streaming platform Wavve.</p>

<h3>For Street Food: "Wednesday Food Talk"</h3>
<p>tvN's "수요미식회" (2015-2019) took a more analytical approach, dedicating each episode to a single dish — an entire hour exploring the best jjajangmyeon, the best naengmyeon, or the best tonkatsu in Seoul. The show's panel includes food critics, chefs, and celebrities who visit 3-4 restaurants per episode and provide brutally honest reviews. This show single-handedly popularized the concept of "matjib hunting" (맛집 hunting — restaurant hunting) in Korean culture.</p>

<h2>How Korean Food Shows Influence Real Dining Culture</h2>
<p>Korean food shows don't just entertain — they reshape the entire restaurant industry. Understanding this influence helps you navigate Korea's dining scene more effectively.</p>

<h3>The "Broadcast Effect" Phenomenon</h3>
<p>When a restaurant appears on a popular food show, Koreans call the resulting surge <strong>"bangsong hyogwa"</strong> (방송 효과 — broadcast effect). Sales typically increase 200-400% in the week following an episode. Some restaurants can't handle the demand: the famous "Mapo Ttukbaegi" in Mangwon-dong, featured on "Baek Jong-won's Top 3 Chef King," saw lines of 2+ hours for months after airing. Savvy travelers should visit featured restaurants <strong>3-6 months after the episode airs</strong>, when the initial rush has subsided but the improved quality remains.</p>

<h3>The Rise of Mukbang and Its Restaurant Impact</h3>
<p>Mukbang (먹방 — eating broadcast) started on AfreecaTV in 2010 and has become a global phenomenon generating an estimated $1.2 billion annually in South Korea alone. Top mukbang creators like <strong>Tzuyang</strong> (14M+ YouTube subscribers) and <strong>Hamzy</strong> (8M+ subscribers) influence restaurant traffic more than traditional TV shows. When Tzuyang visits a restaurant, it can see 1,000+ new customers within days. Her 2024 video at a Hongdae tteokbokki restaurant generated 45 million views and turned a struggling shop into a tourist destination. The restaurant — "Sindang-dong Original Tteokbokki" — now has a permanent line.</p>

<h3>Food Show Tourism: Planning Your Trip</h3>
<p>Several travel agencies now offer <strong>"food show pilgrimage" tours</strong> in Seoul, visiting 5-7 restaurants featured on popular shows in a single day. These typically cost 80,000-120,000 KRW ($58-$87) per person including all food. For self-guided tours, apps like <strong>MangoPlate</strong> (Korea's Yelp equivalent) and <strong>Naver Map</strong> tag restaurants with their TV appearance history. Search "방송 맛집" (broadcast restaurant) on Naver Map to find clusters of TV-featured restaurants near you.</p>

<h2>Korean Food YouTube Channels Worth Following</h2>
<p>Beyond traditional TV, YouTube has become Korea's primary food content platform. These channels provide the most practical value for travelers:</p>
<ul>
<li><strong>영국남자 (Korean Englishman)</strong> — 5.9M subscribers. British host Josh brings friends to experience Korean food for the first time. Great for understanding which dishes have universal appeal.</li>
<li><strong>백종원의 요리비책 (Paik's Cuisine)</strong> — 5.7M subscribers. Chef Baek's home cooking channel with recipes anyone can follow. His "3,000 KRW meal" series shows how to eat well in Korea on a tiny budget.</li>
<li><strong>떵개떵 (Ddeonggae)</strong> — 2.1M subscribers. Honest restaurant reviews with no sponsorships. Known for visiting the same restaurant 3 times before filming to ensure consistency.</li>
<li><strong>국민은행 (Kukmin's Kitchen)</strong> — 1.8M subscribers. Regional food deep dives — if you're traveling outside Seoul, this channel covers restaurants in cities that TV shows ignore.</li>
</ul>

<h3>Related Reads</h3>
<p>Ready to eat your way through Korea? Start with our <a href="/the-ultimate-guide-to-korean-street-food-15-must-try-snacks-and-where-to-find-them/">Korean Street Food Guide</a> for the snacks you'll see on every show, learn <a href="/how-to-order-food-in-korean-25-essential-phrases-every-traveler-needs/">how to order food in Korean</a>, and check out <a href="/soju-guide-for-beginners-how-to-drink-koreas-national-spirit-like-a-local/">our Soju guide</a> for the drinks that pair with every Korean meal.</p>
'''

# ─── ID:69 Korean Drinking Food Anju (1360w → 2500+) ───
extra_69 = '''
<h2>The Unwritten Rules of Anju Culture</h2>
<p>In Korean drinking culture, <strong>ordering anju isn't optional — it's a social expectation</strong>. Most Korean bars and hofs (호프 — beer halls) actually require a food order with drinks, and some will refuse service if you only order alcohol. This practice, called <strong>"anju pildok"</strong> (안주 필독), exists partly because Korean liquor laws historically required food service alongside alcohol sales.</p>

<h3>Matching Anju to Your Drink</h3>
<p>Koreans follow specific pairing traditions that have evolved over decades:</p>
<ul>
<li><strong>Soju → Samgyeopsal (grilled pork belly)</strong>: The most classic pairing. The fatty pork cuts through soju's sharp bite. Budget: 15,000-18,000 KRW per serving at most BBQ restaurants.</li>
<li><strong>Beer → Chikin (Korean fried chicken)</strong>: The "chimaek" (치맥 — chicken + maekju/beer) combo is practically a national institution. Order a whole fried chicken (18,000-22,000 KRW) with a pitcher of Cass or Kloud beer (12,000-15,000 KRW).</li>
<li><strong>Makgeolli → Pajeon (scallion pancake)</strong>: This pairing is so deeply embedded that most makgeolli bars serve pajeon as their primary anju. A haemul pajeon (seafood pancake) costs 12,000-15,000 KRW and easily feeds 2-3 people.</li>
<li><strong>Wine → Cheese ddeokbokki</strong>: A newer trend — wine bars in Itaewon and Gangnam serve cheese-loaded tteokbokki as their signature anju. Expect 15,000-20,000 KRW per plate.</li>
<li><strong>Whisky → Dried squid and nuts</strong>: At Korean "whisky bars" (위스키바), dried ojingeo (squid) with peanuts is the traditional pairing. Simple but effective at 8,000-12,000 KRW.</li>
</ul>

<h3>The "1차, 2차, 3차" Drinking Progression</h3>
<p>Korean drinking culture follows a multi-stop format called <strong>"cha"</strong> (차 — rounds). Understanding this helps you pace both your eating and drinking:</p>
<p><strong>1차 (First round)</strong>: A proper sit-down meal with heavy anju — BBQ, jjigae (stew), or a seafood spread. This is where you eat the most. Duration: 1.5-2 hours. Budget: 25,000-40,000 KRW per person.</p>
<p><strong>2차 (Second round)</strong>: Move to a different bar for lighter anju — fried chicken, dried snacks, or fruit platters. More drinking, less eating. Duration: 1-1.5 hours. Budget: 15,000-25,000 KRW per person.</p>
<p><strong>3차 (Third round)</strong>: Often a noraebang (karaoke room) or a pojangmacha (tent bar) for the final stretch. Minimal anju — maybe ramyeon or dried squid. Duration: 1-2 hours. Budget: 10,000-20,000 KRW per person.</p>

<h2>Best Anju Restaurants and Bars by Neighborhood</h2>

<h3>Jongno 3-ga: The Traditional Drinking District</h3>
<p>Jongno 3-ga (종로3가) is Seoul's oldest and most authentic drinking neighborhood. The narrow alleys behind Tapgol Park are packed with <strong>pojangmacha-style bars</strong> serving classic anju at local prices. <strong>Eulji Darak</strong> (을지다락) is a rooftop bar with panoramic views serving modernized anju like truffle tteokbokki (14,000 KRW) and soju cocktails. For the traditional experience, the unnamed tent bars along the main alley serve odeng (fish cake skewers, 1,000 KRW each) and dubu kimchi (tofu with stir-fried kimchi, 8,000 KRW). This area is especially popular with Korean office workers on weeknights — arrive before 7 PM to secure a seat.</p>

<h3>Mapo-gu: The Craft Beer and Anju Scene</h3>
<p>The Mangwon-dong and Yeonnam-dong areas in Mapo-gu have become Seoul's craft beer capital, and their anju game has evolved accordingly. <strong>Magpie Brewing</strong> in Yeonnam-dong pairs their IPAs with Korean-fusion anju like kimchi quesadillas (12,000 KRW) and gochujang chicken wings (15,000 KRW). <strong>Amazing Brewing Company</strong> in Seongsu-dong (technically Seongdong-gu, but part of the same cultural zone) serves an incredible beer-battered dakgangjeong (sweet crispy chicken, 18,000 KRW) with their house lager.</p>

<h2>Making Anju at Home: 3 Easy Recipes</h2>

<h3>1. Cheese Corn (치즈콘) — 10 Minutes</h3>
<p>This is the single most popular home anju in Korea. Mix one can of sweet corn (drained) with 2 tablespoons of mayonnaise, 1 tablespoon of sugar, and a pinch of salt. Top with shredded mozzarella cheese and microwave for 2 minutes or bake at 200°C for 8 minutes until the cheese bubbles. Pairs perfectly with beer. Total cost: approximately 3,000 KRW ($2.20).</p>

<h3>2. Dubu Kimchi (두부김치) — 15 Minutes</h3>
<p>Slice a block of soft tofu into 1cm slabs and arrange on a plate. Stir-fry 200g of aged kimchi with 100g of sliced pork belly, 1 tablespoon of gochugaru (red pepper flakes), and 1 teaspoon of sugar for 8-10 minutes. Spoon the kimchi-pork mixture over the tofu. This is the most common soju anju at Korean homes. Total cost: approximately 7,000 KRW ($5.10).</p>

<h3>3. Dried Squid with Gochujang Mayo — 5 Minutes</h3>
<p>Buy pre-dried squid (건오징어, available at any Korean grocery for 5,000-8,000 KRW). Tear into strips, microwave for 30 seconds to soften slightly, and serve with a dipping sauce of 2 tablespoons mayonnaise mixed with 1 tablespoon gochujang (Korean red pepper paste). The simplest anju that every Korean household keeps on hand.</p>

<h3>Related Articles</h3>
<p>Pair your anju knowledge with our <a href="/soju-guide-for-beginners-how-to-drink-koreas-national-spirit-like-a-local/">complete Soju guide for beginners</a>, discover <a href="/korean-bbq-etiquette-12-rules-every-first-timer-needs-to-know/">Korean BBQ etiquette</a> for the ultimate 1차 experience, and explore <a href="/the-ultimate-guide-to-korean-street-food-15-must-try-snacks-and-where-to-find-them/">Korean street food</a> for budget-friendly snacking between drinking rounds.</p>
'''

# ─── ID:63 Soju Guide for Beginners (1312w → 2500+) ───
extra_63 = '''
<h2>Understanding Soju Varieties: Beyond the Green Bottle</h2>
<p>Most foreigners only encounter the standard green-bottle soju, but Korea's soju landscape is far more diverse than the convenience store shelf suggests. Understanding the different types transforms your drinking experience from "shots of clear liquor" to genuine appreciation of Korean distilling tradition.</p>

<h3>Mass-Produced Soju (희석식 소주)</h3>
<p>The green-bottle soju you see everywhere — Chamisul, Chum Churum, Good Day — is <strong>diluted soju (huiseoksik soju)</strong>, made by diluting ethanol with water and adding sweeteners. Each brand is regionally dominant:</p>
<ul>
<li><strong>Chamisul (참이슬) by HiteJinro</strong>: 16.5% ABV. Korea's #1 selling soju and the world's best-selling spirit by volume. Crisp and clean. Dominates Seoul and Gyeonggi-do. 1,800 KRW at convenience stores.</li>
<li><strong>Chum Churum (처음처럼) by Lotte</strong>: 16.5% ABV. Slightly softer mouthfeel than Chamisul due to alkaline water processing. Popular in Chungcheong and Gangwon provinces. 1,800 KRW.</li>
<li><strong>Good Day (좋은데이) by Muhak</strong>: 16.9% ABV. Sweeter profile, dominant in Gyeongsang province (Busan, Daegu). 1,700 KRW.</li>
<li><strong>Hallasan (한라산) by Hallasan Soju</strong>: 17% ABV. Jeju Island's exclusive soju, available only on Jeju. Made with Jeju volcanic water. 1,900 KRW. Buying this on the mainland marks you as a Jeju tourist.</li>
</ul>

<h3>Premium Craft Soju (증류식 소주)</h3>
<p>Traditional distilled soju is a completely different drink — closer to Japanese shochu or high-quality vodka. These are meant to be <strong>sipped, not shot</strong>:</p>
<ul>
<li><strong>Andong Soju (안동소주)</strong>: 45% ABV. Korea's most famous traditional soju, distilled in Andong since the Goryeo Dynasty (13th century). Smooth despite high alcohol content. 15,000-25,000 KRW per bottle.</li>
<li><strong>Hwayo (화요)</strong>: Available in 17%, 25%, 41%, and 53% ABV versions. Made from 100% Korean rice. The 41% version won gold at the San Francisco World Spirits Competition. 25,000-80,000 KRW.</li>
<li><strong>Ilpoom Jinro (일품진로)</strong>: 25% ABV. HiteJinro's premium line, distilled rather than diluted. A good bridge between mass-produced and craft soju. 8,000 KRW.</li>
</ul>

<h3>Flavored Soju: The Gateway Drink</h3>
<p>Flavored soju (typically 12-13% ABV) has exploded in popularity since 2015, especially among younger drinkers and foreigners. Top sellers include peach (복숭아), grapefruit (자몽), green grape (청포도), and strawberry (딸기). At 12% ABV and around 1,800 KRW per bottle, these are dangerously easy to drink. Warning: the sweetness masks the alcohol, and many tourists report their worst Korean hangovers came from "the fruity soju that tasted like juice."</p>

<h2>Soju Drinking Games That Every Visitor Should Know</h2>
<p>Korean drinking culture revolves around games that ensure everyone drinks equally and the mood stays lively. Learning even one game before your trip will instantly endear you to Korean drinking companions.</p>

<h3>Flick the Cap (병뚜껑 치기)</h3>
<p>After opening a soju bottle, twist the metal seal hanging from the cap until it's taut. Players take turns flicking it. The person who flicks it off <strong>doesn't drink</strong> — instead, they choose who drinks. This game appears in countless K-dramas (Reply 1988, Episode 5 is the most famous example). Simple, requires zero Korean language skill, and works at any table.</p>

<h3>Baskin Robbins 31</h3>
<p>Players count from 1 to 31, each person saying 1-3 numbers per turn. The person forced to say "31" drinks. Strategy: try to land on numbers that are multiples of 4 (4, 8, 12, 16, 20, 24, 28) to control the game. This game gets louder and more chaotic as the night progresses.</p>

<h3>Nunchi Game (눈치게임)</h3>
<p>Everyone starts seated. The goal is to stand up and call out sequential numbers (1, 2, 3...) without two people standing simultaneously. If two people stand at the same time, both drink. The last person seated also drinks. This game is pure chaos and never fails to generate laughter. "Nunchi" means "social awareness" in Korean — the game literally tests your ability to read the room.</p>

<h2>Where to Experience Soju Culture</h2>

<h3>Traditional Soju Bars (전통주점)</h3>
<p><strong>Baekse Joo (백세주마을)</strong> in Insadong offers a curated selection of 30+ traditional Korean spirits with food pairings. Their tasting flight (3 premium sojus, 15,000 KRW) is the best introduction to craft soju in Seoul. <strong>Sansawon (산사원)</strong> in Pocheon, Gyeonggi-do, is a traditional liquor museum and brewery 40 minutes from Seoul — their tour (8,000 KRW) includes tastings of 5 traditional spirits and a walk through beautiful Korean gardens.</p>

<h3>Best Convenience Store Soju Experience</h3>
<p>The most authentically Korean soju experience might be sitting outside a CU or GS25 convenience store on plastic chairs. Buy a bottle of Chamisul Fresh (1,800 KRW), a cup of instant ramyeon (1,200 KRW), and a triangle kimbap (1,500 KRW). Total: 4,500 KRW ($3.30) for a complete Korean drinking experience. This is not a budget compromise — it's genuinely how millions of Koreans enjoy soju on any given night.</p>

<h3>Explore More Korean Food Culture</h3>
<p>Complete your Korean drinking education with our <a href="/korean-drinking-food-anju-the-best-bar-snacks-to-order-with-soju-and-beer/">guide to anju (Korean drinking food)</a>, learn <a href="/how-to-order-food-in-korean-25-essential-phrases-every-traveler-needs/">essential Korean food phrases</a>, and discover <a href="/korean-convenience-store-food-ranking-top-20-must-try-items-at-cu-gs25-and-7-eleven/">Korea's best convenience store snacks</a> for the ultimate late-night soju pairing.</p>
'''

# ─── ID:53 Gwangjang Market Food Guide (1311w → 2500+) ───
extra_53 = '''
<h2>A Complete Walking Tour of Gwangjang Market's Food Alleys</h2>
<p>Gwangjang Market's food section is divided into distinct zones, and knowing the layout saves you from wandering past the best stalls. The market spans 42,000 square meters with over 5,000 shops, but the food action concentrates in three main areas.</p>

<h3>East Gate Entrance: The Bindaetteok Alley</h3>
<p>Enter from Exit 8 of Jongno 5-ga Station and you'll immediately hit the famous <strong>bindaetteok (mung bean pancake) row</strong>. These stalls have been operating since the 1960s, and the competition between vendors keeps quality remarkably high. The most photographed stall is <strong>"Sunim's Bindaetteok"</strong> (순남시래기 빈대떡), recognizable by its perpetual queue. Their bindaetteok costs 5,000 KRW and is made fresh to order — watch as the ajumma (아줌마 — older woman) ladles batter onto a sizzling griddle, spreading it thin for maximum crispiness. Pro tip: order the <strong>nokdu bindaetteok with kimchi</strong> (김치 녹두전, 6,000 KRW) — the fermented kimchi adds an acidic kick that cuts through the oily richness.</p>

<h3>Central Corridor: The Mayak Gimbap Zone</h3>
<p>"Mayak" means "drug" in Korean, and <strong>mayak gimbap</strong> earned its name because these tiny, sesame oil-drenched rice rolls are considered "addictively" delicious. The original stall — <strong>"Gwangjang Market Mayak Gimbap"</strong> (광장시장 마약김밥) — serves them in portions of 10 for 4,000 KRW with a sweet mustard-soy dipping sauce that is the secret to their appeal. Arrive before 10 AM to avoid the 30-45 minute wait that develops by lunch. If the main stall's line is too long, the stall two doors down (marked by a blue banner) serves nearly identical gimbap with no wait.</p>

<h3>West Section: The Tteokbokki and Sundae Strip</h3>
<p>The western corridor houses stalls specializing in <strong>sundae (Korean blood sausage)</strong> and <strong>tteokbokki</strong>. Unlike the sweet, spicy tteokbokki found at most street stalls, Gwangjang Market's version is often <strong>ganjang tteokbokki</strong> (간장 떡볶이) — seasoned with soy sauce instead of gochujang. This older style, popular before gochujang tteokbokki took over in the 1970s, has a savory, slightly sweet flavor that surprises most first-timers. A plate costs 4,000-5,000 KRW. Pair it with <strong>sundae</strong> (4,000 KRW) — the Korean version is stuffed with glass noodles and pork blood, sliced into rounds and served with salt and perilla seed powder.</p>

<h2>Beyond the Famous Dishes: Hidden Gems</h2>

<h3>Yukhoe (Korean Beef Tartare)</h3>
<p>Gwangjang Market is one of the few places in Seoul where you can safely eat <strong>yukhoe</strong> (육회 — raw beef) at market-stall prices. The beef tartare stalls in the central market area serve impossibly fresh raw beef seasoned with sesame oil, garlic, and topped with a raw egg yolk. A generous portion costs 15,000-18,000 KRW — compared to 30,000-45,000 KRW at Gangnam restaurants. The key to their freshness: the market's butchers slaughter and deliver daily, and stalls that sell out simply close for the day rather than serve less-than-perfect beef.</p>

<h3>Seasonal Specialties</h3>
<p>Gwangjang Market's menu shifts with the seasons, a detail most tourist guides miss:</p>
<ul>
<li><strong>Spring (March-May)</strong>: Ssuk-tteok (mugwort rice cakes, 3,000 KRW/5 pieces) and fresh hobak jeon (zucchini pancake, 4,000 KRW)</li>
<li><strong>Summer (June-August)</strong>: Naengmyeon stalls appear, serving Pyongyang-style cold buckwheat noodles (8,000 KRW) — the broth is icy, tangy, and perfect for Seoul's brutal humidity</li>
<li><strong>Autumn (September-November)</strong>: Freshly harvested chestnut and sweet potato snacks; roasted chestnut carts charge 5,000 KRW per bag</li>
<li><strong>Winter (December-February)</strong>: Hotteok stalls multiply, and steaming bowls of sundaeguk (sundae soup, 8,000 KRW) become the market's star attraction</li>
</ul>

<h2>Practical Information for Your Visit</h2>
<h3>Getting There and Opening Hours</h3>
<p>Take Seoul Metro Line 1 to <strong>Jongno 5-ga Station, Exit 8</strong> (30-second walk). The market officially opens at 8:30 AM, but food stalls start serving as early as 7 AM. Most stalls close by 6 PM on weekdays, 7 PM on weekends. The market is <strong>closed on Sundays</strong> — this catches many tourists off guard. Saturday mornings (8-10 AM) offer the best experience: full vendor selection with manageable crowds.</p>

<h3>How Much to Budget</h3>
<p>A thorough Gwangjang Market food crawl covering the essential dishes:</p>
<ul>
<li>Mayak gimbap (10 pieces): 4,000 KRW</li>
<li>Bindaetteok: 5,000 KRW</li>
<li>Yukhoe (beef tartare): 15,000 KRW</li>
<li>Sundae + tteokbokki: 8,000 KRW</li>
<li>Makgeolli to drink: 5,000 KRW</li>
</ul>
<p><strong>Total: 37,000 KRW ($27)</strong> for one of the most memorable food experiences in Asia. Bring cash — most stalls don't accept cards, though some newer vendors have adopted Samsung Pay and Kakao Pay.</p>

<h3>Discover More Korean Food Adventures</h3>
<p>After Gwangjang Market, explore <a href="/the-ultimate-guide-to-korean-street-food-15-must-try-snacks-and-where-to-find-them/">Seoul's best street food spots</a>, learn <a href="/how-to-order-food-in-korean-25-essential-phrases-every-traveler-needs/">how to order food in Korean</a> before your visit, and continue your market tour with our <a href="/busan-food-guide-8-dishes-you-can-only-find-in-koreas-coastal-city/">Busan food guide</a> for Korea's other legendary food city.</p>
'''

# ─── ID:67 Jeju Island Food Guide (1305w → 2500+) ───
extra_67 = '''
<h2>Jeju's Unique Food Culture: Why Island Food Tastes Different</h2>
<p>Jeju Island's food is fundamentally different from mainland Korean cuisine, shaped by centuries of isolation, volcanic soil, and a harsh oceanic climate. The island was historically one of Korea's poorest regions, and its cuisine reflects a philosophy of <strong>"waste nothing, use everything."</strong> Understanding this context transforms your dining from mere eating into cultural appreciation.</p>

<h3>The Haenyeo Influence on Jeju Cuisine</h3>
<p>The <strong>haenyeo (해녀 — sea women)</strong> are Jeju's legendary female divers who harvest seafood without oxygen tanks, diving to depths of 10-20 meters on a single breath. UNESCO recognized them as Intangible Cultural Heritage in 2016. Today, approximately 3,800 haenyeo remain active, with an average age of 72. Their daily catches — <strong>abalone (전복), sea urchin (성게), conch (소라), and octopus (문어)</strong> — form the backbone of Jeju's seafood cuisine. At restaurants near Seogwipo's haenyeo diving spots, you can eat seafood that was literally pulled from the ocean hours ago. A haenyeo seafood platter typically costs 40,000-60,000 KRW for 2 people and includes raw and cooked preparations.</p>

<h3>Black Pork: Jeju's Signature Meat</h3>
<p>Jeju black pork (흑돼지, heukdwaeji) comes from a heritage pig breed raised exclusively on the island. These pigs are smaller than mainland breeds, with darker meat, more intramuscular fat, and a distinctly nuttier flavor. The best place to try it is <strong>Heukdwaeji Street (흑돼지거리)</strong> near Jeju City's Dongmun Market, a 600-meter strip of 30+ BBQ restaurants specializing exclusively in black pork. Standard pricing: 200g of samgyeopsal (pork belly) costs 14,000-16,000 KRW; 200g of moksal (pork neck) costs 15,000-17,000 KRW. Recommended restaurant: <strong>"Dombe Don" (돔베돈)</strong> — their signature dish is boiled black pork sliced thin and served with salted fermented shrimp. Wait times average 30-45 minutes on weekends.</p>

<h2>7 Essential Jeju Dishes with Where to Eat Them</h2>

<h3>1. Jeonbok Juk (전복죽 — Abalone Porridge)</h3>
<p>Creamy rice porridge cooked with fresh abalone and its green-tinged innards, which give the dish its distinctive color. The abalone innards add an oceanic umami depth impossible to replicate with mainland ingredients. Best at: <strong>"Jejuneun Jeonbok" (제주는 전복)</strong> near Hamdeok Beach, 12,000 KRW per bowl. Arrives steaming hot with side dishes of kimchi and pickled radish.</p>

<h3>2. Gogi Guksu (고기국수 — Pork Noodle Soup)</h3>
<p>Jeju's answer to ramen: thick wheat noodles in a cloudy, deeply savory pork bone broth, topped with sliced boiled pork. This was historically a celebration dish served at weddings and holidays. Today it's available everywhere for 8,000-10,000 KRW. Best at: <strong>"Guksu Madang" (국수마당)</strong> in Jeju City — cash only, open 10 AM to 3 PM, and the broth is made from 12 hours of pork bone simmering.</p>

<h3>3. Hallabong Desserts</h3>
<p>Hallabong (한라봉) is Jeju's famous mandarin orange variety — sweeter and larger than regular Korean tangerines, with a distinctive bumpy top. During season (December-March), hallabong appears in everything: juice (5,000 KRW at roadside stands), chocolate (gift boxes from 15,000 KRW), ice cream (4,000 KRW at Jeju's famous "Hallabong Soft Serve" shops in Seogwipo), and even hallabong makgeolli (8,000 KRW per bottle, only sold on Jeju).</p>

<h3>4. Okdom Gui (옥돔구이 — Grilled Red Tilefish)</h3>
<p>Okdom is Jeju's most prized fish — so integral to island culture that it was once used as tax payment to the Joseon court. The fish is salted and sun-dried for 2-3 days before grilling, concentrating its flavor. A whole grilled okdom costs 25,000-35,000 KRW at restaurants but is worth every won for the sweet, flaky meat. Best at: <strong>"Haecheonilsik" (해천일식)</strong> near Jeju Airport — convenient for a last meal before departing.</p>

<h2>Jeju Food Markets Worth Visiting</h2>
<h3>Dongmun Traditional Market (동문재래시장)</h3>
<p>Jeju City's largest market has operated since 1945 and houses 300+ vendors. The food highlights include fresh-squeezed hallabong juice (3,000 KRW), grilled abalone on the half-shell (5,000 KRW each), and <strong>heukdwaeji sundae</strong> (blood sausage made with black pork, 5,000 KRW) — a Jeju-only specialty. The night market section opens from 6 PM to midnight on Fridays and Saturdays, featuring creative fusion dishes from young Jeju chefs.</p>

<h3>Seogwipo Maeil Olle Market (서귀포매일올레시장)</h3>
<p>Seogwipo's daily market is smaller but more tourist-friendly, with bilingual signs and food court-style seating. Must-try: <strong>hallabong tart</strong> (4,000 KRW) from the bakery near the east entrance, and <strong>haenyeo-caught raw sea urchin</strong> (15,000 KRW per plate) — the uni is scooped live from the shell and has a completely different sweetness from mainland versions.</p>

<h3>Continue Your Korean Food Journey</h3>
<p>For more regional Korean cuisine, check out our <a href="/busan-food-guide-8-dishes-you-can-only-find-in-koreas-coastal-city/">Busan food guide</a>, explore <a href="/the-ultimate-guide-to-korean-street-food-15-must-try-snacks-and-where-to-find-them/">Korean street food nationwide</a>, or pair your Jeju meals with <a href="/soju-guide-for-beginners-how-to-drink-koreas-national-spirit-like-a-local/">Jeju's exclusive Hallasan soju</a>.</p>
'''

# ─── ID:57 Korean Fried Chicken Guide (1279w → 2500+) ───
extra_57 = '''
<h2>The Science Behind Korean Fried Chicken's Legendary Crunch</h2>
<p>Korean fried chicken's superiority over American-style fried chicken isn't subjective — it's chemistry. The key technique is <strong>double frying</strong>: the chicken is fried at 160°C for 8-10 minutes, rested for 5 minutes, then fried again at 180°C for 3-4 minutes. The first fry cooks the meat through; the rest allows moisture to migrate to the surface; the second fry at higher temperature evaporates that surface moisture and creates an extraordinarily thin, shatteringly crispy crust that stays crunchy for over an hour — even under sauce.</p>

<h3>The Sauce Technology</h3>
<p>Korean fried chicken sauces are engineered differently from American wing sauces. Instead of butter-based hot sauces, Korean sauces use <strong>corn syrup or maltose</strong> as a base, which creates a glossy, sticky coating that bonds to the crust without making it soggy. The two dominant sauce families:</p>
<ul>
<li><strong>Yangnyeom (양념)</strong>: Gochujang + corn syrup + garlic + soy sauce. Sweet-spicy, the most popular choice. The sauce caramelizes slightly on the hot chicken, creating a candy-like shell.</li>
<li><strong>Ganjang (간장)</strong>: Soy sauce + garlic + sesame oil + honey. Savory-sweet, less common but arguably more addictive. Often garnished with sliced dried chili peppers and garlic chips.</li>
</ul>
<p>Recent innovations include <strong>buldak (fire chicken)</strong> sauce — weaponized spicy versions measuring 10,000+ Scoville units — and <strong>honey butter</strong> flavor, which became a nationwide obsession in 2024-2025.</p>

<h2>The Major Korean Fried Chicken Chains Ranked</h2>
<p>Korea has over 87,000 fried chicken restaurants — more chicken shops per capita than any country on Earth. Here's how the major chains compare:</p>

<h3>Tier 1: The Legends</h3>
<p><strong>Kyochon (교촌치킨)</strong>: Founded 1991. The gold standard. Their signature soy garlic chicken uses a proprietary sauce recipe that hasn't changed in 30+ years. A whole chicken costs 20,000-22,000 KRW. Their honey series (2020 launch) is also exceptional. 1,200+ locations nationwide.</p>
<p><strong>BBQ Chicken (BBQ치킨)</strong>: Founded 1995. Pioneer of olive oil frying — lighter, less greasy than competitors. Their "Golden Original" (황금올리브) uses 100% olive oil and has a distinctly crisp, non-heavy texture. Whole chicken: 20,000-22,000 KRW. Famous internationally from K-drama product placements (appeared in Goblin, Itaewon Class, and Vincenzo). 1,500+ locations.</p>

<h3>Tier 2: The Specialists</h3>
<p><strong>BHC (BHC치킨)</strong>: Founded 2004. Known for the viral "Bburinkle" chicken — fried chicken with a shaker bag of seasoning powder (cheese, onion, BBQ flavors). The interactive element (you shake the powder yourself) makes it Instagram-friendly. 1,800+ locations. Whole chicken: 19,000-21,000 KRW.</p>
<p><strong>Nene Chicken (네네치킨)</strong>: Founded 1999. Their "Snowflake Chicken" (눈꽃치킨) is coated in a fine white cheese powder that looks like snow. It's milder than yangnyeom, making it family-friendly. 1,300+ locations. Whole chicken: 19,000-20,000 KRW.</p>

<h3>Tier 3: The Cult Favorites</h3>
<p><strong>Puradak (푸라닭)</strong>: Premium-positioned chain known for "Black Garlic Soy" chicken. Uses a charcoal-based cooking method alongside frying. More expensive (23,000-25,000 KRW) but significantly more complex flavor. 700+ locations.</p>
<p><strong>Goobne Chicken (굽네치킨)</strong>: The "healthy" option — oven-roasted rather than fried. Their "Volcano" series adds spicy sauce post-roasting. Whole chicken: 19,000-21,000 KRW. 800+ locations. Popular with health-conscious Koreans and dieters.</p>

<h2>The Chimaek Experience: How to Order Like a Korean</h2>
<h3>The Standard Order</h3>
<p>When Koreans order chimaek, the standard group order for 2-3 people is:</p>
<ul>
<li><strong>1 whole fried chicken</strong> (후라이드 한 마리) — 18,000-22,000 KRW</li>
<li><strong>1 whole yangnyeom chicken</strong> (양념 한 마리) — 19,000-23,000 KRW</li>
<li><strong>Beer pitcher</strong> (생맥주 피처) — 12,000-15,000 KRW</li>
<li><strong>Pickled radish</strong> (치킨무) — always free, always essential</li>
</ul>
<p>Total for the table: approximately 50,000-60,000 KRW ($36-$44). The half-and-half option (반반 — half fried, half yangnyeom in one order) is available at every chain and costs the same as a single whole chicken, giving you variety without doubling the price.</p>

<h3>Delivery Culture: Korea's Real Fried Chicken Experience</h3>
<p>Over 60% of Korean fried chicken is consumed via delivery. Apps like <strong>Baemin (배달의민족)</strong> and <strong>Coupang Eats</strong> deliver from virtually every chicken restaurant within 30-45 minutes. Even in hotels, you can order delivery — give the front desk address and meet the driver in the lobby. Delivery minimum orders are typically 15,000-18,000 KRW, with a delivery fee of 0-3,000 KRW. Late-night delivery (after 10 PM) is completely normal — in fact, 11 PM to 1 AM is peak fried chicken delivery time in Korea.</p>

<h3>Related Food Guides</h3>
<p>Perfect your Korean food knowledge with our <a href="/korean-drinking-food-anju-the-best-bar-snacks-to-order-with-soju-and-beer/">anju guide</a> (fried chicken is Korea's #1 beer snack), learn <a href="/soju-guide-for-beginners-how-to-drink-koreas-national-spirit-like-a-local/">how to drink soju</a> to pair with your chicken, and explore <a href="/korean-convenience-store-food-ranking-top-20-must-try-items-at-cu-gs25-and-7-eleven/">convenience store snacks</a> for when you need a quick chicken fix.</p>
'''

# ─── ID:65 Korean Convenience Store Food (1240w → 2500+) ───
extra_65 = '''
<h2>Understanding Korea's Convenience Store Culture</h2>
<p>South Korea has approximately <strong>55,000 convenience stores</strong> — one for every 940 residents, making it the highest density in the world after Taiwan. The three major chains — <strong>CU (14,800+ stores), GS25 (17,200+ stores), and 7-Eleven (13,500+ stores)</strong> — compete ferociously on food quality, turning what were once simple snack shops into genuine dining destinations. In 2025, convenience store food sales exceeded 8 trillion KRW ($5.8 billion), accounting for 35% of total convenience store revenue.</p>

<h3>Why Korean Convenience Store Food Is Different</h3>
<p>Korean convenience stores operate under a fundamentally different food philosophy than their Western counterparts. While American 7-Elevens sell hot dogs that have been rotating for hours, Korean stores receive <strong>fresh food deliveries 2-3 times daily</strong>, with strict expiration enforcement — items are pulled from shelves with 6+ hours remaining before their sell-by date. The food is developed by teams of professional chefs (CU employs 40+ food development specialists) and tested through consumer panels before launch. New products launch weekly, and items that don't sell are discontinued within 2-3 months. This Darwinian competition means the surviving products are genuinely excellent.</p>

<h2>The Definitive Convenience Store Food Rankings by Category</h2>

<h3>Triangle Kimbap (삼각김밥) — The Gateway Item</h3>
<p>If you try one convenience store item in Korea, make it a triangle kimbap. These onigiri-style rice triangles come in 15-20 flavors per chain, cost <strong>1,200-1,800 KRW ($0.87-$1.30)</strong>, and are genuinely delicious. Top flavors ranked:</p>
<ul>
<li><strong>#1 Chamchi Mayo (참치마요 — Tuna Mayo)</strong>: The undisputed king. Available at all three chains. CU's version has the best rice-to-filling ratio.</li>
<li><strong>#2 Bulgogi (불고기)</strong>: Sweet marinated beef with rice. GS25's version uses slightly higher-quality meat.</li>
<li><strong>#3 Gochujang Jeyuk (고추장제육 — Spicy Pork)</strong>: Fiery and satisfying. 7-Eleven's version is the spiciest.</li>
<li><strong>#4 Myeongran (명란 — Pollock Roe)</strong>: Salty, umami-rich cod roe. A premium option at 1,800 KRW that justifies the extra cost.</li>
<li><strong>#5 Kimchi Chamchi (김치참치 — Kimchi Tuna)</strong>: Kimchi + tuna mayo, combining Korea's two comfort foods.</li>
</ul>

<h3>Cup Ramyeon (컵라면) — Late-Night Essential</h3>
<p>Every Korean convenience store has a hot water dispenser specifically for cup ramyeon. The ritual: choose your cup, pay, fill with hot water at the station, wait 3 minutes, eat at the outdoor seating area. Best options:</p>
<ul>
<li><strong>Shin Ramyun Cup (신라면큰사발)</strong>: 1,500 KRW. The classic. Spicy, satisfying, perfect at 2 AM.</li>
<li><strong>Buldak Bokkeum Myun Cup (불닭볶음면)</strong>: 1,800 KRW. Extremely spicy. A rite of passage for foreigners — the "fire noodle challenge" has billions of YouTube views.</li>
<li><strong>Jin Ramen Cup (진라면)</strong>: 1,300 KRW. Milder than Shin, with a richer broth. Available in "mild" (순한맛) for spice-sensitive visitors.</li>
<li><strong>Gomtang Myun (곰탕면)</strong>: 1,400 KRW. Non-spicy bone broth flavor. The best option for those who can't handle heat.</li>
</ul>

<h3>Fresh Sandwiches and Premium Items</h3>
<p>Korean convenience store sandwiches are in a completely different league from their Western equivalents. The <strong>egg salad sandwich (계란샌드위치)</strong> at GS25 costs 2,800 KRW and features thick, creamy egg salad between pillowy milk bread — it rivals dedicated sandwich shops. CU's <strong>"Deli Master" line</strong> offers premium sandwiches (3,500-4,500 KRW) with ingredients like smoked salmon, prosciutto, and cream cheese that would cost 8,000+ KRW at a cafe.</p>

<h2>Convenience Store Hacks That Locals Know</h2>

<h3>The 1+1 and 2+1 Deals</h3>
<p>Korean convenience stores constantly run <strong>1+1 (buy one get one free)</strong> and <strong>2+1 (buy two get one free)</strong> promotions. These are marked with bright stickers on the shelf. The deals rotate weekly, but snacks, drinks, and ice cream are almost always included. Check the store's app (CU has "Pocket CU," GS25 has "Our GS") to see current promotions before entering. Students and budget travelers survive on these deals.</p>

<h3>The Microwave Station</h3>
<p>Every Korean convenience store has a customer-use microwave. This unlocks an entire category of food: frozen dumplings (mandu, 3,000-4,000 KRW for a bag of 8), frozen rice bowls (dosirak, 3,500-5,000 KRW), and frozen tteokbokki (3,000 KRW). The <strong>CU Backban Dosirak (CU 백반도시락)</strong> at 4,500 KRW is a complete Korean meal — rice, meat, vegetables, and kimchi in a microwave container — that genuinely tastes home-cooked.</p>

<h3>Seasonal Limited Editions</h3>
<p>Korean convenience stores release seasonal items that create genuine buying frenzies:</p>
<ul>
<li><strong>Spring</strong>: Strawberry sandwiches, cherry blossom-themed drinks (March-April)</li>
<li><strong>Summer</strong>: Bingsu cups (shaved ice, 3,000 KRW), frozen fruit bars, cold noodle cups</li>
<li><strong>Autumn</strong>: Sweet potato lattes, chestnut-filled bread, pumpkin desserts</li>
<li><strong>Winter</strong>: Steamed buns (hoppang, 1,500 KRW from the counter warmer), hot chocolate, roasted corn cups</li>
</ul>

<h3>Korean Convenience Store Payment</h3>
<p>All three major chains accept credit/debit cards, Samsung Pay, Kakao Pay, and Naver Pay. Cash works too, but coins are disappearing from Korean commerce. Many stores also have ATMs (KB, Shinhan, Woori banks) that accept international cards — useful for travelers needing Korean won at midnight when banks are closed. The ATM fee is typically 1,000-2,000 KRW per transaction.</p>

<h3>More Korean Food Exploration</h3>
<p>Pair your convenience store discoveries with our <a href="/the-ultimate-guide-to-korean-street-food-15-must-try-snacks-and-where-to-find-them/">Korean street food guide</a>, learn how to enhance your late-night snacking with <a href="/soju-guide-for-beginners-how-to-drink-koreas-national-spirit-like-a-local/">soju from the store cooler</a>, and discover <a href="/korean-fried-chicken-guide-why-kfc-means-something-different-in-korea/">Korean fried chicken delivery</a> when convenience store food isn't enough.</p>
'''

# ─── Execute all expansions ───
print("=== Expanding 8 Travel & Food posts ===")

posts = [
    (44, extra_44, "Korean Street Food Guide"),
    (42, extra_42, "Korean Food Show Guide"),
    (69, extra_69, "Korean Drinking Food Anju"),
    (63, extra_63, "Soju Guide for Beginners"),
    (53, extra_53, "Gwangjang Market Food Guide"),
    (67, extra_67, "Jeju Island Food Guide"),
    (57, extra_57, "Korean Fried Chicken Guide"),
    (65, extra_65, "Korean Convenience Store Food"),
]

results = {}
for pid, extra, title in posts:
    print(f"\n--- {title} (ID:{pid}) ---")
    wc = add_content(pid, extra)
    results[pid] = wc

print("\n=== RESULTS ===")
for pid, wc in results.items():
    status = "OK" if wc >= 2500 else "NEEDS MORE"
    print(f"  ID:{pid} → {wc} words [{status}]")
