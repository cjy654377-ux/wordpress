#!/usr/bin/env python3
"""Phase 3: Top up all posts that are still under 2500 words."""
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
    print(f'  ID:{pid} -> {wc} words')
    return wc

def get_wc(pid):
    r = s.get(f'{REST}/posts/{pid}?_fields=content', headers=h)
    text = re.sub(r'<[^>]+>', '', r.json()['content']['rendered'])
    return len(text.split())

# ============================================================
# ID:15 — needs ~50 more words (currently 2485)
# ============================================================
extra_15 = '''
<h2>Final Tips for Your Yasanhaechon Experience</h2>
<p>Before visiting Yasanhaechon, download Naver Map on your smartphone and search for the restaurant name in Korean characters. Google Maps is notoriously unreliable for Korean restaurant navigation, often showing outdated addresses or incorrect locations. Naver Map will provide accurate directions, real-time operating hours, and user-submitted photos of current menu items and prices. If you are visiting during winter peak season and the wait exceeds your patience, ask the staff about their takeout option for the cod soup, which many regular customers use to enjoy the same quality at home or at their accommodation. The restaurant packages the soup in heat-sealed containers that maintain temperature for approximately 30 minutes, making it viable for nearby hotels.</p>
'''
print("=== Top-up ID:15 ===")
wc = add_content(15, extra_15)
print(f"  Status: {'OK' if wc >= 2500 else 'NEED MORE'}")

# ============================================================
# ID:21 — needs ~250 more words (currently 2301)
# ============================================================
extra_21 = '''
<h2>Why Gukbo 1st Represents the Future of Korean Casual Dining</h2>
<p>Gukbo 1st's business model challenges conventional restaurant economics in ways that food industry analysts find fascinating. In an era when most Korean restaurants are reducing portions and raising prices to maintain margins, Gukbo 1st has doubled down on generosity as its core competitive strategy. The mathematical logic is counterintuitive but sound: by offering overwhelming value, the restaurant generates such intense word-of-mouth marketing that it spends essentially zero on advertising while maintaining a perpetual queue of customers.</p>

<p>This volume-based approach requires operational excellence that most restaurants cannot achieve. Gukbo 1st's kitchen is engineered for speed and consistency, with dedicated stations for broth maintenance, noodle preparation, and meat slicing that function like an assembly line. The broth, once the 24-hour cycle is complete, is maintained in heated holding tanks that can serve hundreds of bowls per service without quality degradation. The noodle station can produce a fresh bowl every 45 seconds during peak hours.</p>

<p>For travelers interested in experiencing Korea's best value dining, Gukbo 1st represents a growing category of restaurants that prove generous portions and premium ingredients are not mutually exclusive. Combine your visit with other exceptional value restaurants featured in our <a href="/top-10-must-try-korean-soups-for-winter-from-tv-show-kitchens-to-your-travel-list/">Korean winter soup guide</a> for a comprehensive tour of Korea's most satisfying affordable cuisine.</p>
'''
print("\n=== Top-up ID:21 ===")
wc = add_content(21, extra_21)
print(f"  Status: {'OK' if wc >= 2500 else 'NEED MORE'}")

# ============================================================
# ID:25 — needs ~300 more words (currently 2249)
# ============================================================
extra_25 = '''
<h2>Chueotang in Korean Popular Culture and Literature</h2>
<p>Chueotang occupies a unique space in Korean cultural memory that extends far beyond its nutritional value. The dish appears repeatedly in Korean literature, film, and television as a symbol of <strong>nostalgic comfort, rural authenticity, and generational connection</strong>. In many Korean novels and films set in the countryside, a scene of an elderly grandmother preparing chueotang serves as visual shorthand for warmth, tradition, and the kind of unhurried care that modern urban life has largely abandoned.</p>

<p>The Korean poet Baek Seok (백석) referenced loach in his celebrated works about rural Korean life, and the image of farmers harvesting loach from rice paddies after the autumn harvest has become one of the most enduring pastoral images in Korean cultural consciousness. When Koreans eat chueotang, they are not merely consuming a soup — they are participating in a cultural ritual that connects them to Korea's agricultural past and the values of patience, simplicity, and respect for natural ingredients that defined traditional Korean food culture.</p>

<p>This cultural significance adds a dimension to the Haengju Chueotang experience that transcends mere gastronomy. When Comedian Kim Mi-ryeo chose this restaurant as her go-to, she was endorsing not just a bowl of soup but a culinary philosophy — the belief that the most meaningful food experiences come from restaurants that refuse to modernize their methods at the cost of authenticity. In an era of fusion cuisine and Instagram-optimized presentation, Haengju Chueotang's stubborn dedication to traditional preparation is itself a statement about what Korean food should be.</p>

<p>For visitors looking to explore more of Korea's traditional food heritage, our <a href="/korean-temple-food-the-zen-buddhist-cuisine-you-never-knew-existed/">guide to Korean temple food</a> examines another ancient culinary tradition that emphasizes simplicity, seasonality, and mindful preparation — values that Haengju Chueotang embodies in every bowl.</p>
'''
print("\n=== Top-up ID:25 ===")
wc = add_content(25, extra_25)
print(f"  Status: {'OK' if wc >= 2500 else 'NEED MORE'}")

# ============================================================
# ID:19 — needs ~400 more words (currently 2133)
# ============================================================
extra_19 = '''
<h2>The Tofu Renaissance: Why Handmade Korean Tofu Is Having a Global Moment</h2>
<p>Seomyeon Sondubu-jip represents a broader trend in Korean food culture that international food media has begun calling the "tofu renaissance." After decades of being dismissed in Western food culture as a bland, joyless meat substitute, tofu is being rediscovered through the lens of Korean cuisine — where it has always been treated as a <strong>premium ingredient worthy of celebration rather than an apology for the absence of meat</strong>.</p>

<p>Korean tofu culture distinguishes between at least six different tofu textures, each with specific culinary applications: <em>sundubu</em> (unpressed, custard-like), <em>yeondubu</em> (soft), <em>modubu</em> (medium), <em>dubu</em> (firm), <em>ttubu</em> (extra firm, often called cotton tofu), and <em>yubu</em> (fried tofu skin). This textural vocabulary reflects centuries of refinement that most Western cuisines simply have not developed. Seomyeon Sondubu-jip's mastery of the sundubu end of this spectrum — the most technically demanding variety to produce — represents the pinnacle of a tradition that has been practiced in Korea for over 1,000 years.</p>

<p>International chefs have taken notice. Restaurants in New York, Los Angeles, London, and Sydney have opened specifically to showcase Korean-style handmade tofu, and several cite Busan's sundubu restaurants as their primary inspiration. The Netflix documentary series <em>Street Food: Asia</em> and <em>Chef's Table</em> have featured Korean tofu makers, introducing millions of viewers to the artistry behind what was previously considered one of the world's most mundane ingredients.</p>

<p>For travelers visiting Busan, experiencing Seomyeon Sondubu-jip is not just a meal — it is an education in what tofu can be when it is made with care, skill, and the kind of generational knowledge that cannot be replicated by industrial production. The flavor difference between their fresh, handmade sundubu and the shrink-wrapped blocks in your local supermarket is not subtle — it is a revelation that fundamentally changes how you think about this ancient food. Combined with a visit to the vibrant <a href="/busan-food-guide-8-dishes-you-can-only-find-in-koreas-coastal-city/">Busan food scene</a>, it creates an unforgettable culinary experience that justifies the trip to Korea on its own.</p>
'''
print("\n=== Top-up ID:19 ===")
wc = add_content(19, extra_19)
print(f"  Status: {'OK' if wc >= 2500 else 'NEED MORE'}")

# ============================================================
# ID:17 — needs ~500 more words (currently 2066)
# ============================================================
extra_17 = '''
<h2>The Korean-Chinese Fusion Food Movement That Birthed Jun's Menu</h2>
<p>To fully appreciate Jun's revolutionary approach, you need to understand the fascinating history of Korean-Chinese fusion cuisine (<em>junghwa-yori</em>, 중화요리). This is not a recent phenomenon — Korean-Chinese food has been a distinct culinary category in Korea for over 120 years, originating with Chinese immigrants who settled in Incheon's Chinatown in the late 1800s and adapted their recipes to Korean palates.</p>

<p>Over the decades, Korean-Chinese food evolved into something entirely distinct from both Chinese and Korean cuisine. The flavors became sweeter and less spicy than mainland Chinese cooking, portion sizes grew to match Korean expectations of generous servings, and entirely new dishes were invented. Jjajangmyeon itself is the best example: while its ancestor is Beijing's <em>zhajiangmian</em>, the Korean version uses a completely different sauce (sweeter, less funky), different noodle texture (chewier, thicker), and different vegetable accompaniments. A mainland Chinese person eating Korean jjajangmyeon would barely recognize it as a descendant of their dish.</p>

<p>Jun's innovation of adding king-sized galbi to jjajangmyeon represents the latest evolution in this ongoing fusion process. By integrating Korea's most prestigious meat cut into a Korean-Chinese classic, Jun is creating a third-generation fusion — Chinese origins, Korean adaptation, and now a premium Korean-Korean-Chinese hybrid that exists nowhere else in the world. Food critics have noted that this kind of bold cross-pollination is increasingly characteristic of Daegu's food scene, which benefits from being far enough from Seoul to develop independently while being connected enough to draw nationwide attention.</p>

<p>The restaurant's success has inspired imitators across Korea, but none have successfully replicated Jun's specific combination of hand-pulled noodles, custom-fermented sauce, and properly braised king ribs. This is because the dish's excellence depends not on the concept (which is simple enough to copy) but on the execution — particularly the 24-hour braising process for the ribs and the week-long secondary fermentation of the black bean paste. These time-intensive processes represent a commitment to quality that quick-copy competitors are rarely willing to make.</p>

<p>If Jun's Korean-Chinese fusion has piqued your interest in Korea's broader noodle culture, our guide to <a href="/the-ultimate-guide-to-korean-street-food-15-must-try-snacks-and-where-to-find-them/">Korean street food</a> covers several other unique noodle dishes you can find at markets and street stalls across the country, while our <a href="/budgets-meals-in-korea-10-tv-featured-restaurants-where-you-can-eat-for-under-10/">budget meals guide</a> features restaurants where innovative Korean fusion food comes at surprisingly accessible prices.</p>
'''
print("\n=== Top-up ID:17 ===")
wc = add_content(17, extra_17)
print(f"  Status: {'OK' if wc >= 2500 else 'NEED MORE'}")

# ============================================================
# ID:40 — needs ~650 more words (currently 1884)
# ============================================================
extra_40 = '''
<h2>Korean Soup Tourism: Planning a Soup-Focused Food Trip</h2>
<p>For dedicated food travelers, a Korean trip organized entirely around soup experiences offers an extraordinary way to explore the country's regional diversity while enjoying some of its most comforting cuisine. Here is a suggested 5-day itinerary that covers the major soup traditions across different regions.</p>

<p><strong>Day 1: Seoul — The Classics</strong><br>
Begin with breakfast at one of Seoul's legendary seolleongtang restaurants in the Mapo or Jongno districts. These establishments have been operating for decades, some for over 50 years, and their bone broths have achieved a depth of flavor that only time can produce. For lunch, explore the gomtang (beef soup) restaurants near Gwanghwamun, and end with a warming bowl of budae-jjigae (army stew) in Uijeongbu, the dish's birthplace just north of Seoul.</p>

<p><strong>Day 2: Jeonju — The Culinary Capital</strong><br>
Take the KTX to Jeonju (1 hour 40 minutes from Seoul), Korea's acknowledged food capital. Start with Jeonju's famous kongnamul-gukbap (soybean sprout rice soup), a local specialty served in dozens of dedicated restaurants in the traditional hanok village area. The Jeonju version includes a raw egg and gochugaru that cook in the hot broth, creating a hearty, slightly spicy masterpiece. For dinner, try Jeonju's legendary bibimbap — while not a soup, it would be criminal to visit Jeonju without tasting its most famous contribution to Korean cuisine.</p>

<p><strong>Day 3: The Countryside — Chueotang Country</strong><br>
Travel to Namwon or the Chungcheong countryside for an authentic chueotang (loach soup) experience at a rural restaurant. The countryside versions are often richer and more intensely flavored than their Seoul counterparts because they source loach locally from nearby rice paddies. Pair with a visit to a traditional market where you can sample regional specialties not available in the cities.</p>

<p><strong>Day 4: Busan — Coastal Flavors</strong><br>
KTX to Busan for the peninsula's best seafood soups. Begin with daegutang (cod soup) at Jagalchi Fish Market, followed by Busan's iconic dwaeji gukbap (pork rice soup) at one of the famous restaurants near Seomyeon. End the day at a milmyeon (wheat noodle soup) restaurant — this cold soup is a Busan original that provides a refreshing contrast to the heartier options.</p>

<p><strong>Day 5: Return to Seoul — Modern Innovations</strong><br>
Back in Seoul, explore the modern soup scene in Gangnam and Itaewon, where contemporary chefs are reinterpreting traditional soups with premium ingredients and refined techniques. Several New Korean restaurants offer tasting menus that feature deconstructed or modernized versions of classic soups, providing a fitting conclusion to your soup odyssey that bridges tradition and innovation.</p>

<h2>The Global Spread of Korean Soup Culture</h2>
<p>Korean soups are experiencing unprecedented international popularity, driven by the global Korean Wave (hallyu), the worldwide interest in fermented foods, and the growing recognition of Korean cuisine as one of the world's great culinary traditions. Understanding this global context adds appreciation for how special it is to experience these soups in their homeland.</p>

<p>In the United States, sundubu-jjigae restaurants have expanded beyond traditional Korean neighborhoods in Los Angeles and New York to appear in mainstream dining districts across the country. The chain BCD Tofu House has brought Korean soft tofu stew to over 15 locations across North America, while independent Korean restaurants in cities from Houston to Portland report that their soup and stew dishes are increasingly popular with non-Korean diners who discover them through social media and K-drama exposure.</p>

<p>Japan, despite having its own sophisticated soup tradition (ramen, miso, etc.), has embraced Korean soups with particular enthusiasm. Sundubu-jjigae restaurants have proliferated across Tokyo and Osaka, and Korean-style kimchi-jjigae has been adapted into Japanese convenience store ready-meals sold in the millions annually. The Korean soup trend in Japan is partly driven by the country's aging population seeking warming, nutritious, easy-to-eat meals — exactly the role these soups have played in Korean culture for centuries.</p>

<p>Europe is the newest frontier for Korean soup culture, with London, Paris, and Berlin seeing rapid growth in Korean restaurants that feature soups prominently on their menus. The European interest tends to focus on the health and fermentation aspects of Korean soups — particularly the probiotic benefits of doenjang and kimchi-based varieties — aligning with the continent's growing interest in gut health and functional foods.</p>

<p>Despite this global spread, experiencing Korean soups in Korea remains irreplaceably superior. The freshness of ingredients, the depth of generations-old restaurant recipes, and the cultural context of eating soup as part of a complete Korean dining experience — with banchan, rice, and the social rituals of Korean table culture — cannot be replicated abroad. For dedicated food travelers, this is the strongest argument for making Korea a priority destination.</p>
'''
print("\n=== Top-up ID:40 ===")
wc = add_content(40, extra_40)
print(f"  Status: {'OK' if wc >= 2500 else 'NEED MORE'}")

# ============================================================
# ID:46 — needs ~700 more words (currently 1817)
# ============================================================
extra_46 = '''
<h2>The Economics Behind Korea's Affordable Food: How Restaurants Keep Prices Low</h2>
<p>Understanding why Korean food is so affordable requires examining the economic and cultural factors that enable restaurants to maintain remarkably low prices while still delivering quality that would command much higher prices in other countries.</p>

<p><strong>Government Agricultural Subsidies</strong><br>
The Korean government heavily subsidizes rice production, maintaining domestic rice prices below international market rates. Since rice is the foundation of virtually every Korean meal, this subsidy effectively reduces the base cost of every restaurant dish in the country. The government also maintains strategic reserves of key ingredients like garlic, onions, and red peppers, releasing reserves to stabilize prices during supply shortages. These interventions keep food costs predictable for restaurant operators, allowing them to maintain fixed menu prices for longer periods than would be possible in an unsubsidized market.</p>

<p><strong>High Volume, Thin Margin Business Model</strong><br>
Korean restaurant culture fundamentally differs from Western dining in its approach to profitability. While a typical American restaurant targets 10 to 15 percent profit margins on each dish, many Korean restaurants operate on margins of 3 to 5 percent, compensating through extremely high customer volume and rapid table turnover. A busy Seoul restaurant serving 300 to 500 customers daily at 5 percent margin can generate the same absolute profit as a restaurant serving 100 customers at 15 percent margin — but the result is dramatically lower prices for consumers.</p>

<p><strong>Family Labor and Low Overhead</strong><br>
Many of Korea's most affordable and beloved restaurants are family-run operations where the owners serve as cooks, servers, and dishwashers, eliminating labor costs that constitute 30 to 40 percent of a typical restaurant's expenses. These <em>bubu-sikdang</em> (husband-wife restaurants) are a cultural institution in Korea, often operating from the ground floor of the family's own building, further reducing overhead. The food quality at these establishments frequently exceeds that of larger, more expensive restaurants because the owners have direct, personal investment in every dish that leaves their kitchen.</p>

<p><strong>Competitive Density</strong><br>
Seoul has approximately one restaurant for every 50 residents — one of the highest restaurant-to-population ratios in the world. This extreme competitive density creates constant downward pressure on prices and upward pressure on quality, because consumers can literally walk 30 seconds in any direction to find an alternative if they are dissatisfied. This market dynamic, while brutal for restaurant operators (Korea has one of the highest restaurant failure rates in the developed world), is extraordinarily beneficial for diners.</p>

<h2>Saving Money on Korean Street Food</h2>
<p>Street food represents the absolute best value in Korean dining, with satisfying snacks available for as little as 1,000 to 3,000 KRW. Here are strategies for maximizing your street food budget.</p>

<p><strong>Traditional Markets Over Tourist Areas</strong><br>
The same tteokbokki that costs 5,000 KRW in Myeongdong is typically 3,000 to 3,500 KRW at traditional markets like Gwangjang, Namdaemun, or Tongin. Market vendors have lower overhead and serve primarily local customers who would not tolerate tourist-inflated pricing. For the best <a href="/gwangjang-market-food-guide-seouls-oldest-market-and-its-legendary-eats/">Gwangjang Market food experiences</a>, visit during weekday mornings when vendors are less rushed and sometimes more generous with portions.</p>

<p><strong>Pojangmacha (포장마차) — Tent Bars</strong><br>
These orange-tented street stalls, iconic in K-dramas, serve simple drinking snacks at honest prices. A plate of odeng (fish cake skewers) with free broth, a plate of fried mandu (dumplings), and a bottle of soju typically costs 12,000 to 15,000 KRW for two people — an authentic and memorable Korean experience for under $10 total. The best pojangmacha clusters are found in Jongno 3-ga, Euljiro, and near university areas.</p>

<p><strong>Convenience Store Strategy</strong><br>
Korean convenience stores (GS25, CU, 7-Eleven, emart24) have evolved far beyond their international counterparts. They offer fresh triangle kimbap (1,200 KRW), cup noodles with premium toppings (1,500 to 2,500 KRW), and ready-to-heat meals (3,000 to 5,000 KRW) that are genuinely good. Many stores have seating areas with microwaves and hot water dispensers. For budget travelers, a convenience store breakfast and a restaurant lunch and dinner keeps daily food costs well under 20,000 KRW while maintaining variety and satisfaction.</p>

<p>For a comprehensive food experience that includes both street food and sit-down dining, our <a href="/myeongdong-street-food-map-the-12-best-stalls-with-exact-locations-2026/">Myeongdong street food map</a> and <a href="/the-ultimate-guide-to-korean-street-food-15-must-try-snacks-and-where-to-find-them/">complete Korean street food guide</a> provide detailed recommendations for every budget level.</p>
'''
print("\n=== Top-up ID:46 ===")
wc = add_content(46, extra_46)
print(f"  Status: {'OK' if wc >= 2500 else 'NEED MORE'}")

# ============================================================
# ID:48 — needs ~650 more words (currently 1880)
# ============================================================
extra_48 = '''
<h2>Korean BBQ for Special Dietary Needs</h2>
<p>Navigating Korean BBQ with dietary restrictions requires advance knowledge and preparation. While Korean BBQ is inherently meat-focused, understanding the options and limitations helps visitors with specific dietary needs participate in this essential Korean cultural experience.</p>

<p><strong>Halal Considerations</strong><br>
Korea does not have a widespread halal certification system, and most Korean BBQ restaurants are not halal-certified. However, Itaewon (Seoul's international district) has several halal-certified Korean BBQ restaurants that serve halal beef and chicken. These restaurants have proliferated in response to growing Muslim tourism from Malaysia, Indonesia, and the Middle East. Outside Itaewon, Muslim travelers can focus on seafood options at some BBQ restaurants that also offer grilled shrimp, squid, and shellfish on the same style of table grill.</p>

<p><strong>Vegetarian and Vegan Options</strong><br>
Traditional Korean BBQ restaurants are challenging for vegetarians, as even the banchan may contain fish sauce, shrimp paste, or anchovy stock. However, the growing vegetarian movement in Korea has spawned several "vegetable BBQ" restaurants in Seoul and Busan that grill mushrooms (particularly king oyster mushrooms, which develop a remarkably meat-like texture), tofu, and seasonal vegetables using the same tableside grill setup. These restaurants maintain the communal, interactive spirit of Korean BBQ while being completely plant-based.</p>

<p><strong>Gluten-Free Dining</strong><br>
The BBQ meat itself is generally gluten-free when unmarinated, but marinated options (especially galbi and bulgogi) frequently contain soy sauce, which contains wheat. Request unmarinated cuts (samgyeopsal, moksal, chadolbaegi) and avoid the ssamjang dipping sauce, which also typically contains soy sauce. The safest approach is to inform the server of your gluten restriction using the Korean phrase "mil allergy-ga isseoyo" (밀 알레르기가 있어요, "I have a wheat allergy") and request salt and sesame oil as alternative seasonings.</p>

<h2>The Different Types of Korean BBQ Restaurants Explained</h2>
<p>Not all Korean BBQ restaurants are created equal, and understanding the different categories helps you choose the right experience for your budget, group size, and culinary goals.</p>

<p><strong>Premium Hanwoo Restaurants (한우 전문점)</strong><br>
These upscale establishments specialize in Korean native cattle (hanwoo), which is graded on a scale from 1 (lowest) to 1++ (highest). A 1++ hanwoo experience, with beautifully marbled beef that rivals the best Japanese wagyu, can cost 60,000 to 120,000 KRW per person. The service is typically more attentive, with staff grilling the meat for you to ensure optimal results. Recommended for special occasions or serious beef enthusiasts who want to understand why hanwoo commands such a premium.</p>

<p><strong>Samgyeopsal Specialists (삼겹살 전문점)</strong><br>
The most common and affordable type of Korean BBQ restaurant. Pork belly is the star, offered in multiple variations: plain, garlic-infused, wine-aged, herb-marinated, and frozen (which is then shaved thin). Prices range from 10,000 to 16,000 KRW per serving, and the unlimited banchan makes it an exceptional value. Many offer all-you-can-eat promotions during off-peak hours for around 15,000 to 18,000 KRW.</p>

<p><strong>Unlimited BBQ Chains (무한리필 고깃집)</strong><br>
These all-you-can-eat BBQ restaurants charge a fixed price (typically 15,000 to 25,000 KRW per person) for unlimited meat over a set time period (usually 90 to 120 minutes). The meat quality is generally a step below specialist restaurants, but the value proposition is undeniable for hungry travelers. Popular chains include Gogi-nara, Palgakdo, and Seorae. The meat selection usually includes multiple pork and beef cuts, and the banchan is also unlimited.</p>

<p><strong>Charcoal BBQ Restaurants (숯불구이)</strong><br>
These restaurants use natural hardwood charcoal instead of gas or electric grills, adding a smoky depth to the meat that gas grills cannot replicate. The charcoal creates more intense heat with better searing capabilities, producing a superior caramelized crust on the meat. Charcoal BBQ restaurants are somewhat harder to find in central Seoul but are common in neighborhoods like Mapo-gu and in smaller cities where traditional cooking methods are more prevalent.</p>

<p>Whether you choose a premium hanwoo experience or a budget samgyeopsal joint, the social ritual remains the same — and mastering the etiquette covered in this guide ensures you will enjoy the experience to its fullest. For your next Korean food adventure, explore our <a href="/seouls-hidden-alley-restaurants-7-places-only-locals-know-about/">guide to Seoul's hidden alley restaurants</a> for intimate dining experiences that take you far off the tourist trail.</p>
'''
print("\n=== Top-up ID:48 ===")
wc = add_content(48, extra_48)
print(f"  Status: {'OK' if wc >= 2500 else 'NEED MORE'}")

# ============================================================
# ID:180 — needs ~850 more words (currently 1700)
# ============================================================
extra_180 = '''
<h2>Myeongdong Beyond Street Food: Complete Neighborhood Guide</h2>
<p>While street food is Myeongdong's most famous attraction, the neighborhood offers a dense concentration of experiences that reward exploration beyond the food stalls. Understanding the full scope of what Myeongdong offers helps you plan a complete half-day or full-day visit.</p>

<p><strong>K-Beauty Shopping</strong><br>
Myeongdong is the undisputed epicenter of K-beauty retail, with flagship stores for every major Korean skincare and cosmetics brand within a few hundred meters of each other. Innisfree, The Face Shop, Etude House, Olive Young, Tony Moly, and Laneige all have major presence here, often with Myeongdong-exclusive products and samples. The competition between stores is fierce, resulting in generous free sample policies — experienced Myeongdong shoppers report accumulating enough samples during a single shopping trip to last weeks. Many stores employ multilingual staff (English, Chinese, Japanese) to assist international visitors.</p>

<p><strong>Myeongdong Cathedral (명동성당)</strong><br>
Rising above the commercial chaos, this stunning Gothic cathedral (completed in 1898) is one of Seoul's most important historical landmarks and a functioning Catholic church. Its red-brick exterior and peaceful gardens provide a dramatic contrast to the surrounding shopping frenzy. The cathedral played a significant role in Korea's democracy movement in the 1980s, serving as a sanctuary for protesters. Admission is free, and the interior is worth visiting for its stained glass windows and the serene atmosphere.</p>

<p><strong>Namsan Tower Access</strong><br>
From the southern edge of Myeongdong, you can walk to the Namsan Cable Car station in about 15 minutes, providing access to N Seoul Tower (Namsan Tower) and its famous love lock fences, observation deck, and rotating restaurant. The walk itself takes you through a quiet, tree-lined path that feels worlds away from the commercial district below. Many visitors combine a Myeongdong street food lunch with an afternoon Namsan Tower visit, timing the ascent to arrive for sunset views over Seoul.</p>

<h2>Seasonal Street Food Specials in Myeongdong</h2>
<p>Myeongdong's street food scene shifts significantly with the seasons, and timing your visit to coincide with seasonal specialties can reveal dishes unavailable during other parts of the year.</p>

<p><strong>Winter (December to February)</strong><br>
Winter is peak season for Myeongdong street food, both in terms of vendor numbers and the quality of offerings. This is when you will find the widest selection of warming foods: hotteok (sweet pancakes) at their most popular, bungeoppang (fish-shaped pastry filled with sweet red bean paste), steaming cups of fish cake broth, and roasted chestnuts. The cold weather also brings out vendors selling hoppang (steamed buns with sweet or savory fillings) and the best quality eomuk (fish cake), which tastes markedly better in cold weather when the hot broth provides maximum contrast.</p>

<p><strong>Spring (March to May)</strong><br>
Spring brings lighter offerings as vendors pivot from heavy winter comfort food. Flower-themed desserts appear, including rose-flavored ice cream, cherry blossom mochi, and strawberry-based treats that take advantage of Korea's peak strawberry season. The moderate temperatures make this an ideal time for a leisurely street food tour, as you can eat comfortably without sweating from summer heat or shivering from winter cold.</p>

<p><strong>Summer (June to August)</strong><br>
The hottest months shift the vendor landscape toward cold and frozen items. Bingsu (Korean shaved ice) vendors appear, along with frozen fruit skewers, iced drinks, and Korea's unique corn-based ice cream bars. The humid heat makes heavy fried items less appealing, so vendors adapt by offering lighter versions of their standard fare. Be aware that some winter-specialty vendors shut down entirely during the hottest weeks of July and August.</p>

<p><strong>Autumn (September to November)</strong><br>
Korea's most beautiful season brings its own street food specialties. Sweet potato vendors return with oven-roasted goguma (Korean sweet potato), which has a drier, chestnut-like texture compared to Western varieties and is absolutely addictive. Freshly made dalgona (honeycomb candy, made famous by Squid Game) vendors are most active in autumn, along with sellers of hotteok transitioning back to winter mode. The comfortable temperatures and beautiful fall foliage make autumn arguably the best overall season for a Myeongdong street food experience.</p>

<h2>Safety and Health Tips for Myeongdong Street Food</h2>
<p><strong>Food Safety Standards</strong><br>
Korean street food vendors are subject to regular health inspections by district health authorities, and Myeongdong — as one of Seoul's premier tourist destinations — receives more frequent inspections than average. Food safety standards are generally high by international standards. However, the usual street food precautions apply: eat items that are freshly cooked rather than those that have been sitting out, and be cautious with raw or minimally cooked seafood items during summer months.</p>

<p><strong>Staying Hydrated</strong><br>
Extended street food tours involve significant walking, standing in lines, and eating sodium-rich foods. Bring a water bottle (refill stations are available at subway stations and some public buildings) or purchase water from any of the dozens of convenience stores in the district. Avoid replacing water with the sweet beverages sold by many vendors — these can actually increase dehydration.</p>

<p><strong>Pickpocket Awareness</strong><br>
While Korea is one of the world's safest countries, Myeongdong's extreme crowds during peak hours create conditions that pickpockets can exploit. Keep your phone and wallet in front pockets or a cross-body bag, particularly during the shoulder-to-shoulder evening hours. That said, the actual risk is very low — Seoul consistently ranks among the safest major cities in the world for tourists.</p>

<p>Complete your Seoul food journey by exploring the incredible diversity of <a href="/the-ultimate-guide-to-korean-street-food-15-must-try-snacks-and-where-to-find-them/">Korean street food beyond Myeongdong</a>, including regional specialties from Busan, Jeonju, and Jeju that offer entirely different snacking experiences.</p>
'''
print("\n=== Top-up ID:180 ===")
wc = add_content(180, extra_180)
print(f"  Status: {'OK' if wc >= 2500 else 'NEED MORE'}")

# ============================================================
# ID:80 — needs ~700 more words (currently 1860)
# ============================================================
extra_80 = '''
<h2>Building Your Korean Vocabulary Through K-Drama Genres</h2>
<p>Different K-drama genres expose you to specific vocabulary domains that textbooks rarely cover comprehensively. Strategic genre selection can rapidly build vocabulary in areas most relevant to your needs.</p>

<p><strong>Food and Restaurant Vocabulary — Food/Cooking Dramas</strong><br>
Dramas like <em>Wok of Love</em>, <em>Let's Eat</em>, and <em>Jewel in the Palace</em> are vocabulary goldmines for food-related Korean. You will learn ingredient names, cooking techniques, flavor descriptions, and restaurant interaction phrases in natural context. These are immediately practical if you plan to visit Korea: learning how to describe flavors (맛있어요 mashisseoyo "delicious," 매워요 maewoyo "spicy," 달아요 darayo "sweet") and order confidently transforms your dining experience.</p>

<p><strong>Travel and Direction Vocabulary — Road Trip/Travel Dramas</strong><br>
Shows like <em>Hometown Cha-Cha-Cha</em> (set in a seaside village) and <em>Crash Landing on You</em> (featuring both South and North Korean settings) introduce transportation, direction, and location vocabulary naturally. You will learn place-related words (역 yeok "station," 길 gil "road/street," 앞 ap "front," 뒤 dwi "behind") that are essential for navigating Korea.</p>

<p><strong>Emotional and Relationship Vocabulary — Romance Dramas</strong><br>
The romance genre teaches the vocabulary of human relationships in extraordinary depth. Korean has nuanced terms for different types of relationships (선배 seonbae "senior colleague," 동생 dongsaeng "younger sibling/friend," 오빠 oppa "older brother from female perspective") that are critical for understanding Korean social dynamics. These relationship terms carry emotional weight and social implications that only drama context can fully convey.</p>

<p><strong>Professional and Academic Vocabulary — Workplace Dramas</strong><br>
Shows set in offices, hospitals, or law firms introduce formal Korean that is essential for business travelers or anyone planning to work in Korea. You will learn meeting etiquette phrases, email language, hierarchical address forms, and industry-specific terminology. <em>Misaeng</em> (Incomplete Life) is particularly recommended for workplace Korean, as it depicts realistic office interactions with minimal dramatization.</p>

<h2>Free and Paid Resources for K-Drama Korean Learning</h2>
<p>Several dedicated platforms and tools have emerged specifically to support learning Korean through K-dramas. Here are the most effective options currently available.</p>

<p><strong>Viki (Free with Ads / Premium)</strong><br>
Rakuten Viki is uniquely valuable because it offers community-contributed subtitles in both Korean and English, often with timing precision that allows you to read along with the dialogue. The "Learn Mode" feature (premium subscription) highlights vocabulary and grammar points within the subtitles, creating an integrated learning experience. The free tier provides access to most content with ads.</p>

<p><strong>Netflix Korean Content (Subscription)</strong><br>
Netflix has the largest library of Korean dramas with professional subtitle quality. The ability to switch between Korean and English subtitles is essential for the multi-pass study method described earlier. Netflix also allows you to adjust playback speed, which is useful for slowing down rapid dialogue to catch individual words and sounds.</p>

<p><strong>TTMIK (Talk To Me In Korean) — K-Drama Courses</strong><br>
This popular Korean learning platform offers specific courses built around K-drama dialogue. Their "Korean Through K-Drama" series breaks down real drama scenes, explaining grammar, vocabulary, and cultural context. Free content is available on their website and YouTube channel, with premium courses offering more structured progression.</p>

<p><strong>Anki Flashcard Decks</strong><br>
The spaced repetition flashcard app Anki has community-created decks specifically designed for K-drama vocabulary. The most popular decks include audio clips from actual dramas, associating each word with a memorable scene. This leverages the emotional memory advantage discussed earlier and is remarkably effective for long-term retention.</p>

<p><strong>HelloTalk and Tandem (Language Exchange Apps)</strong><br>
After building passive comprehension through K-dramas, you need active practice with real speakers. HelloTalk and Tandem connect you with Korean native speakers interested in language exchange. Many Korean users on these platforms are enthusiastic K-drama fans themselves, creating natural conversation topics and shared cultural reference points that make exchanges enjoyable and productive.</p>

<h2>Measuring Your Progress: From K-Drama Beginner to Conversational</h2>
<p>A realistic timeline for progressing from zero Korean to conversational fluency using K-dramas as your primary study tool (supplemented with structured grammar study) looks approximately like this.</p>

<p><strong>Months 1 to 3: Recognition Phase</strong><br>
You begin recognizing common words and phrases without subtitles. You can identify basic emotions, greetings, and common exclamations. You start to hear where one word ends and another begins in spoken Korean. At this stage, you should have mastered reading <a href="/how-to-read-korean-hangul-in-30-minutes-the-fastest-method-that-actually-works/">Hangul</a> and begun using Korean subtitles.</p>

<p><strong>Months 4 to 8: Comprehension Phase</strong><br>
You understand the general gist of conversations without subtitles. You can follow simple plot points in Korean and recognize most common grammar patterns. You begin catching jokes, wordplay, and cultural references that do not translate well into English subtitles. This is when K-drama learning becomes genuinely fun because you start experiencing content that English subtitle viewers miss.</p>

<p><strong>Months 9 to 18: Production Phase</strong><br>
You can construct basic sentences and participate in simple Korean conversations. Your pronunciation, shaped by hundreds of hours of drama listening, is noticeably more natural than learners who studied only from textbooks. You can watch some K-dramas (especially rom-coms and slice-of-life) without English subtitles and follow the majority of the dialogue.</p>

<p><strong>Months 18 and Beyond: Fluency Development</strong><br>
With continued drama exposure and active conversation practice, you develop the ability to express complex thoughts, understand rapid speech, and navigate different speech levels appropriately. At this stage, K-dramas shift from being a learning tool to being pure entertainment that you happen to consume in Korean — the ultimate goal of any language learning journey.</p>
'''
print("\n=== Top-up ID:80 ===")
wc = add_content(80, extra_80)
print(f"  Status: {'OK' if wc >= 2500 else 'NEED MORE'}")

print("\n=== Phase 3 complete ===")
