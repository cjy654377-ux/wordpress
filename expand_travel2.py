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

# ── ID:51 — How to Order Food in Korean ──
extra_51 = """
<h2>Regional Dining Etiquette: How Orders Differ Across Korea</h2>
<p>Korean dining culture is not monolithic. The way you order, interact with staff, and even pay the bill can vary dramatically depending on whether you are in Seoul, Busan, Jeju, or a small countryside village. Understanding these regional differences will elevate your dining experience from tourist-level to local-level.</p>

<h3>Seoul: Fast-Paced and Digital</h3>
<p>In Seoul, especially in trendy neighborhoods like Gangnam, Hongdae, and Itaewon, many restaurants have adopted kiosk ordering systems (키오스크). You will encounter touchscreen menus in Korean, though some now offer English interfaces. The key phrases here are slightly different — you might say <strong>"여기요" (yeogiyo)</strong> less often because the kiosk replaces human interaction. However, traditional restaurants in areas like Jongno and Euljiro still rely entirely on verbal ordering.</p>
<p>Seoul servers tend to be efficient but less chatty. Do not mistake brevity for rudeness — it is simply the fast-paced culture of a city where restaurants turn over tables quickly during lunch rush hours (typically 12:00–1:30 PM).</p>

<h3>Busan: Warm, Loud, and Generous</h3>
<p>Busan dining culture is noticeably warmer and louder than Seoul. Servers at seafood restaurants in Jagalchi Market or Haeundae might call you <strong>"아이가" (aiga)</strong> — a Gyeongsang dialect term of endearment. The portions tend to be more generous, and it is common for restaurant owners to bring out extra banchan without being asked.</p>
<p>In Busan, you will hear the dialect version of common phrases. Instead of the standard "주세요" (juseyo), locals often say <strong>"주이소" (juiso)</strong> or <strong>"다오" (dao)</strong>. While you do not need to use dialect yourself, recognizing these variations prevents confusion.</p>

<h3>Jeju Island: Relaxed and Unique</h3>
<p>Jeju restaurants operate on "island time." Meals are slower, portions reflect the island's fishing culture, and the specialty ingredients — black pork (흑돼지), abalone (전복), and horse meat (말고기) — require specific ordering vocabulary. When ordering Jeju black pork BBQ, specify the cut: <strong>"오겹살 주세요"</strong> (five-layer pork belly) is the island's signature, different from mainland's standard 삼겹살 (three-layer).</p>

<h3>Countryside Villages: Personal and Traditional</h3>
<p>In rural areas like Jeonju's Hanok Village, Andong, or small towns in Gangwon Province, the dining experience feels personal. Many restaurants are family-run with no written menu — the owner tells you what is available that day based on seasonal ingredients. The phrase <strong>"뭐가 맛있어요?"</strong> (What is delicious today?) works perfectly in these settings. The owner will often recommend their best dish and may even sit down to chat with you.</p>

<h2>Digital Ordering: Navigating Korean Restaurant Technology</h2>
<p>Korea's restaurant technology is among the most advanced in the world. Beyond kiosks, you will encounter several ordering systems that require specific knowledge to navigate successfully.</p>

<h3>Tablet Ordering Systems</h3>
<p>Many Korean BBQ restaurants and chain restaurants now use tablet ordering. The tablet sits at your table, and you browse a visual menu to select items. Key buttons to recognize:</p>
<ul>
<li><strong>주문하기 (jumun-hagi)</strong> — Place order</li>
<li><strong>추가주문 (chuga-jumun)</strong> — Additional order</li>
<li><strong>직원호출 (jigwon-hochul)</strong> — Call staff</li>
<li><strong>결제하기 (gyeolje-hagi)</strong> — Pay</li>
<li><strong>수량 (suryang)</strong> — Quantity (+ / - buttons)</li>
</ul>
<p>Most tablets display food photos, making visual ordering possible even without Korean reading ability. However, customization options (spice level, meat doneness, side dish selection) are almost always text-only in Korean.</p>

<h3>QR Code Ordering</h3>
<p>Post-pandemic, QR code ordering has become widespread in Korean cafes and restaurants. Scan the QR code at your table with your phone camera, and a mobile menu loads in your browser. These systems often support only Korean and occasionally English. The ordering flow mirrors tablet systems, but payment usually requires a Korean payment method (KakaoPay, NaverPay) or a physical card payment at the counter.</p>

<h3>Vending Machine Tickets (식권)</h3>
<p>Some traditional restaurants, especially budget eateries near universities and office areas, use a vending machine ticket system (식권 기계). You insert cash or card, press the button for your meal, receive a paper ticket, and hand it to the kitchen. These machines rarely have English, so knowing the Korean names of common dishes is essential. Look for photos on the machine buttons — they are your best visual guide.</p>

<h2>Advanced Ordering Scenarios: Beyond the Basics</h2>
<p>Once you have mastered basic ordering phrases, these advanced scenarios will help you navigate more complex dining situations that guidebooks rarely cover.</p>

<h3>Group Dining and Portion Ordering</h3>
<p>Korean restaurants often price dishes by portion size, and the minimum order for sharing dishes is typically 2 servings (2인분). This catches many solo travelers off guard. If dining alone, ask: <strong>"1인분도 되나요?"</strong> (Can I order one portion?). Some restaurants allow it; others firmly require minimum 2인분 for items like Korean BBQ, shabu-shabu, and stews.</p>
<p>When ordering for a group, use the counter <strong>"인분" (inbun)</strong>: "삼겹살 3인분 주세요" means three portions of pork belly. A common mistake is ordering individual dishes for everyone — many Korean meals are designed for sharing, and ordering separately can result in an awkwardly large amount of food.</p>

<h3>Customizing Your Order</h3>
<p>Korean restaurants are generally accommodating with modifications, though the culture around customization is different from Western countries. Useful customization phrases:</p>
<ul>
<li><strong>"덜 맵게 해주세요"</strong> (deol maepge haejuseyo) — Make it less spicy</li>
<li><strong>"고수 빼주세요"</strong> (gosu ppaejuseyo) — No cilantro</li>
<li><strong>"양파 빼주세요"</strong> (yangpa ppaejuseyo) — No onion</li>
<li><strong>"따로 주세요"</strong> (ttaro juseyo) — Serve it separately</li>
<li><strong>"많이 주세요"</strong> (mani juseyo) — Give me a lot (for banchan)</li>
</ul>

<h3>Handling Mistakes and Returns</h3>
<p>If the wrong dish arrives, say <strong>"이거 안 시켰는데요"</strong> (igeo an sikyeonneundeyo — I did not order this). Korean restaurants handle mistakes quickly and without drama. If a dish is too salty or has an issue, <strong>"좀 짠 것 같아요"</strong> (jom jjan geot gatayo — It seems a bit salty) is a polite way to flag it.</p>

<h2>Cultural Context: Why Food Ordering Matters in Korean Society</h2>
<p>In Korea, food is deeply connected to social hierarchy and relationship-building. How you order reveals your cultural awareness and can significantly impact your interactions with locals.</p>
<p>The concept of <strong>"눈치" (nunchi)</strong> — reading the room — applies directly to dining. In a business dinner (회식, hoesik), the most senior person orders first and often orders for the entire table. If you are the junior person, offering to order or choosing the most expensive item is a social faux pas. Wait for the senior to suggest or decide, then agree enthusiastically.</p>
<p>When dining with Korean friends, the phrase <strong>"아무거나" (amugeona — anything is fine)</strong> is both the most common and most frustrating response. If someone says this, they typically want you to choose but are being polite. Take the initiative and suggest a specific restaurant or dish — your decisiveness will be appreciated.</p>
<p>Tipping does not exist in Korean dining culture. The price on the menu is the final price (though VAT is included). Leaving money on the table after a meal can cause confusion — the server may chase you down thinking you forgot your change. Instead, express gratitude verbally: <strong>"잘 먹었습니다"</strong> (jal meogeosseumnida — I ate well) as you leave. This phrase is the Korean equivalent of a generous tip — it acknowledges the cook's effort and is deeply appreciated.</p>

<p>For more Korean dining experiences, explore our guides to <a href="/gwangjang-market-food-guide-seouls-oldest-market-and-its-legendary-eats/">Gwangjang Market's legendary food stalls</a>, discover <a href="/seouls-hidden-alley-restaurants-7-places-only-locals-know-about/">Seoul's hidden alley restaurants</a>, and learn <a href="/korean-bbq-etiquette-12-rules-every-first-timer-needs-to-know/">Korean BBQ etiquette rules</a>.</p>
"""

# ── ID:59 — Korean Temple Food ──
extra_59 = """
<h2>The Five Forbidden Ingredients: Understanding Osinchae (오신채)</h2>
<p>At the heart of Korean temple food lies a strict prohibition that sets it apart from all other vegetarian cuisines worldwide. The <strong>osinchae (오신채)</strong>, or five pungent vegetables, are completely banned from temple kitchens: garlic (마늘), green onion (파), chives (부추), wild leek (달래), and asafoetida (흥거). This prohibition originates from Buddhist texts that teach these ingredients stimulate desire and anger, disturbing the monk's meditation practice.</p>
<p>What makes this restriction fascinating from a culinary perspective is how temple cooks have developed an entire flavor system without these foundational ingredients. Korean cuisine outside temples relies heavily on garlic and green onion — they appear in virtually every dish. Temple cooks replace these flavors with perilla seeds (들깨), sesame oil (참기름), wild mushrooms, fermented soybean paste (된장), and dried kelp (다시마). The result is a subtler, more nuanced flavor profile that many professional chefs now study as a masterclass in umami building.</p>

<h3>How Temple Cooks Build Flavor Without Garlic</h3>
<p>The absence of garlic — perhaps the most challenging restriction — forces temple cooks to layer flavors through technique rather than ingredients. They use three primary methods:</p>
<ul>
<li><strong>Extended fermentation</strong> — Temple doenjang (fermented soybean paste) is aged for 3-5 years, compared to 6 months for commercial versions. This extended aging develops deep, complex flavors that compensate for garlic's absence.</li>
<li><strong>Mushroom concentration</strong> — Dried shiitake, wood ear, pine, and oyster mushrooms are used in combination to create layers of umami. A single temple soup might contain four different mushroom varieties.</li>
<li><strong>Cold extraction</strong> — Rather than boiling, many temple stocks are made by cold-soaking dried kelp and mushrooms overnight. This produces a cleaner, more delicate flavor than hot extraction.</li>
</ul>

<h2>A Day of Eating at a Korean Temple: The Complete Meal Schedule</h2>
<p>Buddhist temples follow a rigorous eating schedule that has remained unchanged for over a thousand years. Understanding this schedule is essential for anyone planning a temple stay experience.</p>

<h3>Joban Gongyang (조반공양) — Morning Meal at 6:00 AM</h3>
<p>The morning meal is the lightest of the day. It typically consists of rice porridge (죽), pickled vegetables, and a simple clear soup. The porridge varies by season — pumpkin porridge in autumn, pine nut porridge in winter, vegetable porridge in spring. This meal follows the 3:30 AM wake-up bell and morning chanting, so the body needs gentle nourishment rather than heavy food.</p>

<h3>Jungban Gongyang (중반공양) — Midday Meal at 11:30 AM</h3>
<p>The main meal of the day features the full <strong>balwoo gongyang (발우공양)</strong> formal eating ritual when practiced traditionally. This is the most substantial meal: steamed rice, two or three vegetable side dishes, soup, and seasonal specialties. Common midday dishes include lotus root braised in soy sauce, seasoned fernbrake (고사리), stir-fried mountain vegetables, and tofu prepared in various styles.</p>

<h3>Yakseok (약석) — Evening Snack at 5:00 PM</h3>
<p>Traditionally, Buddhist monks do not eat a full dinner — the evening "meal" is technically medicine food (약석 literally means "medicine stone"). It is deliberately small: perhaps a bowl of grain tea, some dried persimmons, rice crackers, or leftover rice mixed into a simple porridge. The principle is that eating too much at night interferes with meditation and sleep.</p>

<h2>Temple Food Ingredients: A Seasonal Foraging Guide</h2>
<p>Korean temple food is inseparable from its natural environment. Temples are almost always located in mountains, and monks have foraged their surrounding forests for centuries. This creates a direct farm-to-temple connection that modern restaurants can only imitate.</p>

<h3>Spring (봄): March–May</h3>
<p>Spring is the most exciting season for temple food. After months of relying on preserved and fermented foods, fresh wild greens emerge: <strong>냉이 (naengi, shepherd's purse)</strong>, <strong>달래 (dallae, wild chives — used only in cooking temples that follow modified rules)</strong>, <strong>씀바귀 (sseumba-gwi, ixeris)</strong>, and <strong>취나물 (chwinamul, aster)</strong>. These greens are blanched, seasoned with sesame oil and perilla, and served as banchan. Spring temple food has a fresh, slightly bitter quality that Koreans believe cleanses the body after winter.</p>

<h3>Summer (여름): June–August</h3>
<p>Summer temple food focuses on cooling the body. Chilled cucumber soup (오이냉국), perilla seed noodles (들깨국수), and lotus leaf-wrapped rice (연잎밥) are staples. Temples also prepare <strong>maesil-cheong (매실청)</strong> — green plum syrup — during June when the plums ripen. This syrup is aged for at least a year and used as a natural sweetener and digestive aid throughout the year.</p>

<h3>Autumn (가을): September–November</h3>
<p>Autumn is preservation season at Korean temples. Monks prepare <strong>kimjang (김장)</strong> — the massive annual kimchi-making event — though temple kimchi differs from household versions by omitting garlic, green onion, and fish sauce. Temple kimchi relies on dried chili flakes, ginger, fermented soybean liquid, and salt alone. The result is a cleaner, more purely vegetable flavor. Autumn also brings chestnuts, ginkgo nuts, persimmons, and mushrooms that are dried and stored for winter.</p>

<h3>Winter (겨울): December–February</h3>
<p>Winter temple food relies on preserved ingredients: dried mushrooms, fermented pastes, root vegetables (radish, burdock, lotus root), and kimchi at various stages of fermentation. Hot soups and stews become central — doenjang jjigae, mushroom hot pot, and root vegetable stews. Temples also serve <strong>sujeonggwa (수정과)</strong>, a cinnamon-ginger punch, as a warming after-meal drink.</p>

<h2>How Temple Food Influenced Modern Korean Cuisine</h2>
<p>The influence of temple food extends far beyond monastery walls. Several iconic Korean dishes and food practices originated in or were refined by temple kitchens.</p>
<p><strong>Fermentation techniques</strong> — Korea's globally famous fermented foods (kimchi, doenjang, gochujang, ganjang) were refined over centuries in temple kitchens where monks had the time, patience, and discipline for long fermentation processes. Commercial production later adopted these temple-developed methods.</p>
<p><strong>Seasonal eating philosophy</strong> — The temple principle of eating only what grows naturally in the current season directly influenced Korea's food culture. Even today, Korean grocery stores dramatically shift their offerings by season, and many restaurants change their menus quarterly — a practice rooted in temple food tradition.</p>
<p><strong>The Michelin star connection</strong> — Several Michelin-starred restaurants in Seoul, including the three-starred <strong>Balwoo Gongyang</strong> at the Templestay Information Center in Jongno, serve refined temple food. The restaurant holds the distinction of being one of the only temple food establishments in the world with Michelin recognition, proving that Buddhist cuisine can compete at the highest levels of fine dining.</p>

<p>For more Korean culinary traditions, explore our <a href="/gwangjang-market-food-guide-seouls-oldest-market-and-its-legendary-eats/">Gwangjang Market food guide</a>, discover the differences between <a href="/jeonju-bibimbap-vs-seoul-bibimbap-whats-the-difference-and-where-to-eat/">Jeonju and Seoul bibimbap</a>, and read about <a href="/seouls-hidden-alley-restaurants-7-places-only-locals-know-about/">Seoul's hidden alley restaurants that only locals know</a>.</p>
"""

# ── ID:55 — Jeonju vs Seoul Bibimbap ──
extra_55 = """
<h2>The Ingredients That Make Jeonju Bibimbap Unique</h2>
<p>Jeonju bibimbap is not simply bibimbap served in Jeonju — it is a fundamentally different dish with specific ingredients that are codified by local tradition. Understanding these ingredients reveals why food scholars consider Jeonju bibimbap a separate culinary category from the bibimbap served elsewhere in Korea.</p>

<h3>Yukhoe (육회): Raw Beef Tartare</h3>
<p>The most distinctive ingredient in authentic Jeonju bibimbap is <strong>yukhoe (육회)</strong> — Korean-style raw beef tartare. While Seoul bibimbap typically uses cooked beef (bulgogi-style or stir-fried), Jeonju tradition demands fresh raw beef seasoned with sesame oil, garlic, and pine nuts. The beef must be from that day's butchering — Jeonju restaurants source from nearby Gimje and Imsil cattle farms, where Hanwoo (한우) beef is raised specifically for raw consumption.</p>
<p>The yukhoe sits at the center of the bowl as a bright red crown, topped with a raw egg yolk and scattered pine nuts. When you mix the bibimbap, the residual heat from the rice gently warms the beef without cooking it fully — creating a silky, half-raw texture that is entirely different from the fully-cooked protein in Seoul versions.</p>

<h3>Kongnamul (콩나물): Jeonju's Famous Bean Sprouts</h3>
<p>Jeonju is the undisputed bean sprout capital of Korea. The city's location over limestone aquifers produces mineral-rich water that grows exceptionally plump, crunchy bean sprouts. These are not the thin, watery sprouts found in supermarkets — Jeonju kongnamul are thick-stemmed, almost juicy, with a satisfying snap when bitten. Every authentic Jeonju bibimbap restaurant serves a separate bowl of kongnamul-guk (bean sprout soup) alongside the bibimbap, made from the same premium sprouts.</p>

<h3>The 30-Topping Standard</h3>
<p>Traditional Jeonju bibimbap contains approximately 30 individual toppings (나물), compared to Seoul bibimbap's typical 8-12. These include: seasoned fernbrake (고사리), spinach (시금치), bellflower root (도라지), crown daisy (쑥갓), radish (무), zucchini (호박), shiitake mushroom (표고버섯), dried seaweed (김), cucumber (오이), carrot (당근), mung bean jelly (청포묵), egg (계란), ginkgo nut (은행), walnut (호두), pine nut (잣), chestnut (밤), jujube (대추), and more. Each topping is individually seasoned and prepared — a single bowl represents hours of kitchen work.</p>

<h2>Seoul Bibimbap: The Evolution of a Street Food Classic</h2>
<p>Seoul bibimbap has its own proud tradition, even if it is less codified than Jeonju's version. Its evolution reflects Seoul's character as a fast-moving metropolis that adapts tradition to modern lifestyles.</p>

<h3>Gwangjang Market: The Living Museum of Seoul Bibimbap</h3>
<p>The closest thing to "authentic" Seoul bibimbap is found at <a href="/gwangjang-market-food-guide-seouls-oldest-market-and-its-legendary-eats/">Gwangjang Market</a>, where elderly vendors have served bibimbap from narrow stalls for decades. Market bibimbap is served in stainless steel bowls with a practical selection of toppings — typically 8-10 items arranged in colorful sections. The gochujang is mixed in before serving (unlike Jeonju, where you mix it yourself), and the rice is regular white rice rather than Jeonju's stock-cooked version.</p>
<p>What makes market bibimbap special is its accessibility and speed. For 7,000-8,000 won ($5-6), you get a filling, balanced meal in under five minutes. This democratic pricing is part of Seoul bibimbap's identity — it is fundamentally a people's food, not a luxury item.</p>

<h3>Dolsot Bibimbap: Seoul's Hot Stone Innovation</h3>
<p>The <strong>dolsot (돌솥)</strong> — hot stone pot — version of bibimbap is widely associated with Seoul, though its exact origin is debated. The scorching stone bowl creates <strong>nurungji (누룽지)</strong>, the crispy rice crust at the bottom, which adds a smoky, toasted dimension that regular bowl bibimbap lacks. The sizzling sound and visual drama of a dolsot bibimbap arriving at your table has made it the most photographed version of the dish.</p>
<p>Dolsot bibimbap requires a specific eating technique: immediately push the rice away from the edges of the bowl to prevent excessive burning, add your gochujang and sesame oil, then mix vigorously. Let the mixed bibimbap sit for 30-60 seconds against the hot stone to develop more nurungji, then eat from the edges inward. At the end of the meal, pour hot water or barley tea into the empty dolsot — the liquid loosens the remaining nurungji into a pleasant tea-like drink called <strong>sungnyung (숭늉)</strong>.</p>

<h2>Making Authentic Bibimbap at Home: A Complete Guide</h2>
<p>Creating restaurant-quality bibimbap at home is entirely achievable, but it requires understanding the three elements that determine quality: the rice, the namul preparation, and the sauce.</p>

<h3>The Rice Foundation</h3>
<p>For Jeonju-style bibimbap, cook your rice in beef bone broth instead of water. Add a tablespoon of soybean sprout cooking water for extra umami. The rice should be slightly firmer than regular eating rice — use a 1:0.9 rice-to-liquid ratio instead of the standard 1:1. This prevents the bibimbap from becoming mushy when mixed with the vegetable juices and sauce.</p>

<h3>Namul Preparation Principles</h3>
<p>Each vegetable topping must be prepared individually — this is non-negotiable. Never mix raw vegetables together before seasoning. The basic namul seasoning formula: blanch the vegetable, squeeze out excess water, then season with sesame oil (1 tsp), salt (pinch), and minced garlic (for home cooking — temples omit this). Some namul get soy sauce instead of salt, and heartier vegetables like fernbrake and bellflower root need stir-frying after blanching.</p>
<p>The color arrangement matters. Traditional presentation follows the Korean five-color principle (오방색): white (bean sprouts, radish), green (spinach, cucumber, zucchini), red (carrot, gochujang), yellow (egg yolk, squash), black (seaweed, shiitake, fernbrake). Arrange toppings in color-separated sections on top of the rice — never randomly scattered.</p>

<h3>The Gochujang Sauce</h3>
<p>Restaurant bibimbap gochujang sauce is not straight gochujang from the jar. The standard bibimbap sauce recipe: 3 tablespoons gochujang, 1 tablespoon sesame oil, 1 tablespoon sugar (or plum syrup), 1 teaspoon rice vinegar, 1 teaspoon minced garlic. Mix well and let sit for at least 30 minutes before serving. Some restaurants add a small amount of doenjang for depth, and Jeonju restaurants often include pine nut oil for richness.</p>

<p>For related food adventures, check out our <a href="/busan-food-guide-8-dishes-you-can-only-find-in-koreas-coastal-city/">Busan food guide</a>, explore <a href="/the-ultimate-guide-to-korean-street-food-15-must-try-snacks-and-where-to-find-them/">Korea's best street food</a>, and learn about <a href="/korean-fried-chicken-guide-why-kfc-means-something-different-in-korea/">why Korean fried chicken is a national obsession</a>.</p>
"""

# ── ID:11 — Bangi Gullim Mandu ──
extra_11 = """
<h2>The History of Korean Mandu: From Silk Road to Seoul</h2>
<p>Korean mandu (만두) trace their origins to the Mongolian Empire's influence during the Goryeo Dynasty (918-1392). When Mongol rulers introduced their buuz (steamed dumplings) to the Korean peninsula, local cooks adapted the concept using Korean ingredients and techniques. The word "mandu" itself derives from the Chinese "mantou" (馒头), though Korean mandu evolved into something distinctly different from both Chinese and Mongolian versions.</p>
<p>What makes Korean mandu unique in the global dumpling family is the filling composition. While Chinese jiaozi emphasize pork and Japanese gyoza focus on garlic-heavy ground meat, Korean mandu traditionally combine <strong>tofu, kimchi, glass noodles (dangmyeon), and vegetables</strong> with smaller amounts of meat. This reflects Korea's historical Buddhist influence and the practical reality that meat was expensive for common people. The result is a lighter, more textured dumpling that does not sit as heavily in the stomach.</p>

<h3>Regional Mandu Varieties Across Korea</h3>
<p>Every region of Korea has its own mandu tradition, and understanding these variations puts Bangi Gullim Mandu's hand-rolled style into proper context:</p>
<ul>
<li><strong>Pyongyang-style (평양만두)</strong> — Large, generously stuffed dumplings with a thin wrapper. These are the ancestors of the jumbo mandu style that Bangi Gullim continues.</li>
<li><strong>Kaesong-style (개성만두)</strong> — Elaborately shaped dumplings resembling tiny pouches, with a filling that includes pine nuts and walnuts for richness.</li>
<li><strong>Kimchi mandu (김치만두)</strong> — Found everywhere in Korea, these use well-fermented kimchi as the primary filling ingredient, creating a tangy, spicy dumpling that pairs perfectly with makgeolli.</li>
<li><strong>Mandu-guk (만두국)</strong> — Dumpling soup, the traditional New Year's dish. Thin-skinned dumplings float in a clear beef broth, often with egg ribbons and seaweed garnish.</li>
<li><strong>Jjin mandu (찐만두)</strong> — Steamed dumplings, the style most similar to Chinese dim sum but with Korean filling.</li>
</ul>

<h2>Hand-Rolling vs Machine: Why Method Matters</h2>
<p>The "gullim" (굴림) in Bangi Gullim Mandu refers to rolling by hand — a technique that fundamentally changes the dumpling's character compared to machine-made versions. Understanding this difference explains why food lovers specifically seek out hand-rolled mandu.</p>
<p><strong>Wrapper thickness variation</strong> — Machine-rolled wrappers are perfectly uniform, typically 1mm thick throughout. Hand-rolled wrappers have natural variation: slightly thicker at the pleated edges (1.5-2mm) and thinner at the center where the filling sits (0.5-0.8mm). This variation creates textural contrast — crispy-chewy edges with a delicate center that lets the filling flavors come through.</p>
<p><strong>Filling distribution</strong> — Hand-wrapped mandu contain roughly 40% more filling per dumpling than machine-made versions. The artisan can feel the wrapper's stretch limit and adjust filling accordingly, while machines operate on fixed measurements that must account for wrapper breakage.</p>
<p><strong>Cooking behavior</strong> — When hand-rolled mandu are boiled in hot pot broth (as served at Bangi Gullim), the uneven wrapper thickness creates different textures simultaneously. The thin center becomes almost translucent and silky, while the thicker edges maintain a pleasant chew. Machine-made dumplings cook uniformly — functional but less interesting.</p>

<h2>Korean Hot Pot Culture: The Ttegul Tradition</h2>
<p>The "ttegul" (떡을) in the restaurant's name refers to the hot pot service style — mandu served in a boiling, bubbling broth tableside. This is not simply soup with dumplings; it is a specific dining format with its own etiquette and eating rhythm.</p>
<p>Korean hot pot (전골, jeongol) differs from Chinese hotpot and Japanese shabu-shabu in several important ways. First, the broth is heavily seasoned before serving — it is a complete flavor on its own, not a neutral cooking medium. Second, the ingredients are pre-arranged in the pot by the kitchen, not selected by diners from a raw bar. Third, the pot is meant to be eaten communally but in a specific order: start with the broth and lighter items, move to the dumplings, and finish by adding noodles or rice to the remaining broth.</p>

<h3>How to Eat Mandu Hot Pot Like a Local</h3>
<p>When your mandu hot pot arrives at Bangi Gullim, follow this sequence for the optimal experience:</p>
<ol>
<li><strong>Wait 2-3 minutes</strong> — Let the bubbling settle slightly. Impatient eating leads to burned tongues, and the mandu need time to finish cooking in the broth.</li>
<li><strong>Start with broth</strong> — Use the communal ladle to pour broth into your individual bowl. Taste the stock first to appreciate its depth before the mandu flavors meld in.</li>
<li><strong>Eat mandu with dipping sauce</strong> — Use chopsticks (not a spoon) to lift each dumpling. The restaurant provides a soy-vinegar dipping sauce (초간장) — dip lightly, as the broth has already seasoned the mandu.</li>
<li><strong>Pace yourself</strong> — Korean hot pot is designed for slow eating. The pot stays on a burner, keeping everything hot. Rushing defeats the purpose.</li>
<li><strong>Add rice at the end</strong> — When the mandu are finished, add steamed rice to the remaining broth. This final step creates a porridge-like finish called <strong>juk (죽)</strong> that captures every remaining flavor in the pot.</li>
</ol>

<h2>Songpa-gu Food Scene: Beyond the Tourist Path</h2>
<p>Bangi Gullim Mandu's location in Songpa-gu places it in one of Seoul's most interesting food neighborhoods — an area that most tourists overlook in favor of Myeongdong, Itaewon, or Hongdae. Songpa-gu, anchored by Lotte World and the Olympic Park, has developed a sophisticated local food scene driven by residents rather than tourists.</p>
<p>The neighborhood around Bangi Station and Jamsil Station contains a concentration of restaurants that have operated for 20-40 years, serving the same families across generations. Unlike trendy Seoul neighborhoods where restaurants open and close rapidly, Songpa-gu rewards loyalty — many establishments offer better portions and off-menu items to regular customers.</p>
<p>Notable food stops near Bangi Gullim Mandu include the morning fish market at Garak Market (가락시장) — Korea's largest wholesale seafood and produce market, just one subway stop away. Visit before 7 AM for the auction atmosphere, then have fresh-catch sashimi at one of the market's upstairs restaurants where fishmongers prepare what they could not sell at wholesale prices. The quality rivals Busan at a fraction of the cost.</p>

<p>Explore more Seoul food destinations: <a href="/gwangjang-market-food-guide-seouls-oldest-market-and-its-legendary-eats/">Gwangjang Market food guide</a>, <a href="/seouls-hidden-alley-restaurants-7-places-only-locals-know-about/">Seoul's hidden alley restaurants</a>, and <a href="/the-ultimate-guide-to-korean-street-food-15-must-try-snacks-and-where-to-find-them/">the ultimate Korean street food guide</a>.</p>
"""

# ── ID:13 — World Bap Korean Buffet ──
extra_13 = """
<h2>Korean Buffet Culture: A Complete Guide for First-Timers</h2>
<p>Korean all-you-can-eat buffets (뷔페) operate differently from Western buffets in ways that catch many visitors off guard. Understanding these differences before your visit will help you maximize your experience at places like World Bap and similar Korean buffet restaurants.</p>

<h3>The Time Limit System</h3>
<p>Most Korean buffets enforce a strict time limit — typically 60-90 minutes. At World Bap, the lunch time limit is 70 minutes, which may feel rushed if you are accustomed to leisurely buffet dining. The time starts when you sit down, not when you get your first plate. Strategy: do a full reconnaissance walk past all stations before picking up a plate, so you know exactly what you want and waste no time on items you will not enjoy.</p>

<h3>The Pricing Structure</h3>
<p>Korean buffets use tiered pricing that varies by meal period. Lunch is always cheaper than dinner (sometimes by 30-50%), and weekday prices undercut weekends. At World Bap's price point of approximately 8,000 won ($6), you are at the extreme budget end of the Korean buffet spectrum. For context, the pricing tiers in Korea are:</p>
<ul>
<li><strong>Budget (6,000-12,000 won)</strong> — Home-style Korean food, limited seafood. World Bap sits here.</li>
<li><strong>Mid-range (15,000-25,000 won)</strong> — Better ingredients, sushi stations, grilled meats.</li>
<li><strong>Premium (30,000-50,000 won)</strong> — Hotel buffets, premium seafood, chef stations.</li>
<li><strong>Luxury (60,000-100,000+ won)</strong> — 5-star hotel, lobster, wagyu, champagne.</li>
</ul>

<h3>Banchan Buffet vs Full Buffet</h3>
<p>An important distinction in Korean dining is between a full buffet (뷔페) and a banchan buffet (반찬뷔페). World Bap falls into the banchan buffet category — the focus is on the dozens of side dishes (반찬) that define Korean home cooking. While a Western buffet emphasizes main dishes with sides as afterthoughts, a Korean banchan buffet flips this: the sides ARE the main attraction, with rice and soup as the supporting cast.</p>
<p>This format reflects how Koreans actually eat at home. A traditional Korean home meal (한식, hansik) centers on rice surrounded by 5-12 small side dishes, each offering different flavors, textures, and nutritional profiles. The banchan buffet simply scales this concept up, offering 30-50 side dish options so you can compose your ideal Korean meal.</p>

<h2>What to Eat at a Korean Banchan Buffet: Strategic Guide</h2>
<p>With dozens of options and limited time, strategy matters. Here is how Korean regulars approach a banchan buffet to get the best experience.</p>

<h3>Round 1: The Foundation (0-15 minutes)</h3>
<p>Start with a small bowl of rice and select 6-8 banchan for your first round. Focus on the dishes you cannot easily find elsewhere:</p>
<ul>
<li><strong>Jeon (전)</strong> — Korean savory pancakes. Look for hobak-jeon (zucchini), dongtae-jeon (pollock), and nokdu-jeon (mung bean). These are labor-intensive to make at home and taste best fresh from the buffet griddle.</li>
<li><strong>Namul (나물)</strong> — Seasoned vegetables. Try at least three different types to compare: spinach, fernbrake, bean sprouts, bellflower root.</li>
<li><strong>Jorim (조림)</strong> — Braised dishes. Gamja-jorim (potatoes), dubu-jorim (tofu), and myeolchi-jorim (anchovies) are essentials.</li>
</ul>

<h3>Round 2: Deep Exploration (15-35 minutes)</h3>
<p>Now that your initial hunger is satisfied, explore more adventurous options:</p>
<ul>
<li><strong>Jjigae and tang (찌개/탕)</strong> — Stews and soups. Most banchan buffets offer 3-5 soup options. Doenjang-jjigae, kimchi-jjigae, and some form of meat soup are standard.</li>
<li><strong>Grilled items</strong> — If available, grilled fish (especially galchi/cutlassfish or godeungeo/mackerel) is always worth trying. These are expensive to buy individually at restaurants.</li>
<li><strong>Kimchi varieties</strong> — A good banchan buffet offers 4-8 types of kimchi: napa cabbage (standard), radish (kkakdugi), cucumber (oi-sobagi), young radish (chonggak), perilla leaf (kkaennip), and water kimchi (mul-kimchi).</li>
</ul>

<h3>Round 3: Finishing Touches (35-50 minutes)</h3>
<p>End with items that cleanse the palate and complete the nutritional balance:</p>
<ul>
<li><strong>Fruit</strong> — Korean buffets always offer seasonal fruit. In Korea, fruit is dessert — not an afterthought but a deliberate palate cleanser.</li>
<li><strong>Sikhye (식혜)</strong> — Sweet rice punch. This traditional digestive drink is served at most Korean buffets as the finishing beverage.</li>
<li><strong>Sungnyung (숭늉)</strong> — Roasted rice tea. Pour hot water over scorched rice for a nutty, warming end to the meal.</li>
</ul>

<h2>Gwangju: Korea's Most Underrated Food Capital</h2>
<p>World Bap's location in Gwangju (광주) places it in what many Korean food experts consider the country's true culinary capital — not Seoul, not Jeonju, but Gwangju. This claim may surprise visitors who have never heard of the city, but the evidence is compelling.</p>
<p>Gwangju sits in the heart of <strong>Jeolla Province (전라도)</strong>, historically Korea's agricultural breadbasket. The surrounding Honam Plain produces some of Korea's finest rice, and the nearby coast provides abundant seafood. This combination of premium ingredients, combined with a regional food culture that prioritizes generosity and flavor complexity, created a dining tradition that Koreans themselves regard as the country's best.</p>
<p>The Jeolla Province food philosophy can be summarized in one concept: <strong>"한 상 가득" (han sang gadeuk)</strong> — a table completely full. When you order a single main dish at a Gwangju restaurant, the table fills with 15-25 banchan. This is not premium service; it is the baseline expectation. Restaurants that skimp on banchan in Gwangju lose customers immediately.</p>
<p>This cultural context explains World Bap's business model. At approximately $6 for unlimited banchan and rice, the restaurant is not offering a special deal — it is operating within Gwangju's food culture where abundance is the norm. A similar operation in Seoul would likely charge double and serve half the variety.</p>

<h2>Practical Tips for Budget Eating Across South Korea</h2>
<p>World Bap represents one strategy for eating well in Korea on a budget. Here are additional approaches that savvy travelers use to eat exceptional Korean food without breaking the bank:</p>
<ul>
<li><strong>University district restaurants (대학로 맛집)</strong> — Areas around Korea's major universities (Hongdae, Sinchon, Konkuk, Sungshin) have restaurants competing for student budgets. Expect filling Korean meals for 6,000-8,000 won.</li>
<li><strong>Market food courts (시장 먹거리)</strong> — Traditional markets like <a href="/gwangjang-market-food-guide-seouls-oldest-market-and-its-legendary-eats/">Gwangjang Market</a> in Seoul offer complete meals for 5,000-10,000 won with zero compromise on quality.</li>
<li><strong>Gimbap-cheongguk (김밥천국)</strong> — Korea's ubiquitous budget restaurant chain serves dozens of Korean dishes for 4,000-7,000 won each. The quality varies by location, but the best branches rival independent restaurants.</li>
<li><strong>Convenience store meals (편의점)</strong> — Korean convenience stores (CU, GS25, 7-Eleven) sell surprisingly good rice bowls, ramen, and kimbap for 2,000-5,000 won. The triangle kimbap (삼각김밥) at 1,000-1,500 won is Korea's ultimate budget snack.</li>
</ul>

<p>Discover more Korean food experiences: <a href="/busan-food-guide-8-dishes-you-can-only-find-in-koreas-coastal-city/">Busan's coastal food guide</a>, <a href="/korean-fried-chicken-guide-why-kfc-means-something-different-in-korea/">Korean fried chicken culture</a>, and <a href="/soju-guide-for-beginners-how-to-drink-koreas-national-spirit-like-a-local/">the ultimate soju guide</a>.</p>
"""

# ── ID:29 — Hongcheon Food Trip ──
extra_29 = """
<h2>Buckwheat in Korean Cuisine: Why Gangwon Province Is the Capital</h2>
<p>Buckwheat (메밀, memil) holds a special place in Korean cuisine, and Gangwon Province — where Hongcheon is located — is its undisputed heartland. The mountainous terrain, cold winters, and short growing season of Gangwon make it unsuitable for rice paddies but perfect for buckwheat, which thrives in poor soil and matures in just 70-80 days.</p>
<p>The connection between Gangwon Province and buckwheat is immortalized in Korean literature through Lee Hyo-seok's famous short story <strong>"When Buckwheat Flowers Bloom" (메밀꽃 필 무렵)</strong>, set in Pyeongchang. Every September, the buckwheat fields of Gangwon Province bloom into seas of white flowers — a spectacle that now draws tourists from across Korea for the annual Buckwheat Festival in Bongpyeong.</p>

<h3>Makguksu (막국수): Gangwon's Signature Buckwheat Noodle</h3>
<p>The makguksu served at Hongcheon's Sigol Makguksu and similar Gangwon restaurants differs fundamentally from Seoul versions. Here is what makes the regional original special:</p>
<ul>
<li><strong>Buckwheat ratio</strong> — Authentic Gangwon makguksu uses 70-100% buckwheat flour, compared to Seoul restaurants that often cut it to 30-50% with wheat flour for easier noodle-making. Higher buckwheat content means a grainier, more fragile noodle with deeper nutty flavor.</li>
<li><strong>Broth preparation</strong> — The cold broth (육수) is made from dongchimi (동치미, radish water kimchi) mixed with beef bone stock. The broth should be ice-cold, slightly tangy from the dongchimi fermentation, and refreshing enough to drink on its own.</li>
<li><strong>Serving style</strong> — The noodles arrive on a cutting board or in a metal bowl with a scissors-cut option. Use the provided scissors to cut the long noodles into manageable lengths — this is standard practice, not rude. Add vinegar (식초) and mustard (겨자) to taste. The vinegar brightens the buckwheat flavor, while the mustard adds a nasal heat that complements the cold broth.</li>
</ul>

<h3>Memil-jeonbyeong (메밀전병): Buckwheat Crepes</h3>
<p>Beyond noodles, Gangwon Province is famous for <strong>memil-jeonbyeong</strong> — thin buckwheat crepes filled with kimchi, vegetables, or sweet red bean paste. These are Hongcheon's answer to French crêpes, predating them by centuries. The buckwheat batter is spread thin on a hot griddle, filled with stir-fried kimchi and vegetables, then rolled into a cylinder. The exterior is crispy-chewy while the interior is savory and satisfying. At Hongcheon's traditional markets, these sell for 3,000-5,000 won each — an essential snack between restaurant meals.</p>

<h2>Pine Nuts: Hongcheon's Other Culinary Treasure</h2>
<p>While buckwheat noodles bring food tourists to Hongcheon, the region's pine nuts (잣, jat) are equally prized by Korean food connoisseurs. Korea's pine nuts — specifically from the Korean pine (잣나무, Pinus koraiensis) — are considered the world's finest, and Hongcheon's mountain forests produce a significant portion of the national harvest.</p>

<h3>Why Korean Pine Nuts Are Different</h3>
<p>Korean pine nuts are larger, more elongated, and richer in oil than Mediterranean pine nuts (from Pinus pinea) commonly used in Italian cuisine. The flavor profile is more complex: buttery with a slight resinous quality that adds depth to any dish. Korean pine nuts contain approximately 68% fat (mostly healthy unsaturated), 14% protein, and are rich in pinolenic acid — a fatty acid unique to pine nuts that studies suggest may help suppress appetite.</p>
<p>The harvesting process is extraordinary. Pine nut cones grow at the very top of 20-30 meter tall trees. Harvesters must climb these trees using only basic safety equipment, often at altitudes above 500 meters in Gangwon's mountains. The cones are harvested in October, dried, then cracked individually by hand to extract the nuts. A single harvester might collect 20-30 kg of cones per day, yielding only 1-2 kg of edible pine nuts. This labor-intensive process explains why Korean pine nuts retail for 80,000-120,000 won ($60-90) per kilogram.</p>

<h3>Pine Nut Dishes to Try in Hongcheon</h3>
<ul>
<li><strong>Jat-juk (잣죽)</strong> — Pine nut porridge. Ground pine nuts are simmered with rice into a creamy, ivory-colored porridge. Traditionally served to the sick and elderly as nourishment, it is now a sought-after delicacy served at Hongcheon's specialty restaurants.</li>
<li><strong>Jat-gangjeong (잣강정)</strong> — Pine nut candy. Whole pine nuts are coated in a thin shell of grain syrup and rice puffs, creating a crunchy, sweet snack. These make excellent souvenirs and last for weeks at room temperature.</li>
<li><strong>Jat-makgeolli (잣막걸리)</strong> — Pine nut rice wine. Hongcheon breweries infuse traditional makgeolli with pine nut powder, creating a rich, creamy variation that is uniquely local.</li>
</ul>

<h2>Hongcheon Through the Seasons: A Year-Round Food Calendar</h2>
<p>While Hongcheon is famous as a winter ski destination (Vivaldi Park is just 15 minutes from the town center), the town's food scene changes dramatically with each season, offering compelling reasons to visit year-round.</p>

<h3>Spring (March–May)</h3>
<p>The mountains surrounding Hongcheon come alive with wild greens. Local restaurants feature <strong>sanchae-bibimbap (산채비밥)</strong> — bibimbap topped with freshly foraged mountain vegetables including chamnamul, chwinamul, and dallae. The Hongcheon River begins its trout season, and restaurants along the riverbank serve <strong>songeo-hoe (송어회)</strong> — raw trout sashimi that is a Gangwon Province specialty.</p>

<h3>Summer (June–August)</h3>
<p>Summer in Hongcheon means <strong>samgyetang (삼계탕)</strong> — ginseng chicken soup eaten on the three hottest days of the year (복날, boknal). Hongcheon's version uses locally-raised free-range chickens stuffed with Gangwon ginseng, jujubes, and sticky rice. The town's riverside restaurants also serve chilled makguksu as relief from the heat, and local watermelon from the Hongcheon plains is prized across Korea.</p>

<h3>Autumn (September–November)</h3>
<p>Autumn is buckwheat season. The fields bloom white in late September, and fresh buckwheat noodles made from the new harvest have a quality that stored buckwheat cannot match. This is the best time for makguksu. Pine nut harvesting also peaks in October, and fresh pine nuts appear in markets before being shipped nationwide. Autumn mushroom foraging produces <strong>songi (송이, matsutake)</strong> mushrooms — among the most expensive ingredients in Korean cuisine at 200,000-500,000 won per kg.</p>

<h3>Winter (December–February)</h3>
<p>Hongcheon's cold winters (temperatures regularly reach -15°C to -20°C) make it the ideal setting for hearty, warming foods. <strong>Dakgalbi (닭갈비)</strong> — spicy stir-fried chicken — is a winter favorite, served on a sizzling hotplate. The nearby Chuncheon (30 minutes by car) is the official birthplace of dakgalbi, but Hongcheon versions are equally good with fewer crowds. Ice fishing (빙어낚시) on Hongcheon's frozen rivers is a unique winter activity, and the tiny freshwater fish (빙어, bing-eo) caught through the ice are deep-fried immediately into a sweet, crunchy snack.</p>

<p>For more regional Korean food adventures, see our guides to <a href="/busan-food-guide-8-dishes-you-can-only-find-in-koreas-coastal-city/">Busan's coastal cuisine</a>, <a href="/jeonju-bibimbap-vs-seoul-bibimbap-whats-the-difference-and-where-to-eat/">Jeonju's legendary bibimbap</a>, and <a href="/seouls-hidden-alley-restaurants-7-places-only-locals-know-about/">Seoul's hidden alley restaurants</a>.</p>
"""

# ── ID:27 — Pohang Halmae-jip ──
extra_27 = """
<h2>Somoori-gukbap: Understanding Korea's Ox Head Soup Tradition</h2>
<p>Ox head soup (소머리국밥, somoori-gukbap) is one of Korea's most ancient and culturally significant dishes, yet it remains virtually unknown outside the country. Unlike galbitang (short rib soup) or seolleongtang (ox bone soup), which have gained international recognition, somoori-gukbap occupies a unique niche: it is the blue-collar worker's breakfast, the hangover cure, and the regional pride dish all in one.</p>
<p>The name breaks down simply: 소 (so, cow) + 머리 (meori, head) + 국밥 (gukbap, rice soup). The dish uses every part of the ox head — cheek meat, tongue, brain, eye, ear cartilage — simmered for 12-20 hours until the collagen-rich tissues dissolve into a thick, milky-white broth. The extended cooking time is not optional; it is what transforms tough, gelatinous head meat into melt-in-your-mouth tenderness.</p>

<h3>The 12-Hour Cooking Process</h3>
<p>At restaurants like Pohang Halmae-jip, the cooking process begins the night before serving:</p>
<ol>
<li><strong>Evening preparation (6-8 PM)</strong> — The ox head is thoroughly cleaned, soaked in cold water for 2-3 hours to remove blood, then placed in a massive pot (가마솥, gamasot) with water.</li>
<li><strong>First boil (8-10 PM)</strong> — The head is brought to a rolling boil, then the water is discarded. This first boil removes impurities and excess fat. Fresh water is added.</li>
<li><strong>Overnight simmer (10 PM – 6 AM)</strong> — The pot simmers on low heat through the night. During this phase, the collagen from skin, cartilage, and bone dissolves into the broth, turning it from clear to opaque white. A staff member monitors the pot throughout the night, maintaining the temperature and skimming occasionally.</li>
<li><strong>Morning separation (6-7 AM)</strong> — The head is removed from the broth. The meat is separated by hand into different textures: lean cheek meat, gelatinous skin, crunchy ear cartilage, tender tongue. Each type is sliced separately and arranged on serving plates.</li>
<li><strong>Serving (7 AM onwards)</strong> — Each bowl is assembled to order: steamed rice in the bottom, sliced head meat on top, boiling broth ladled over everything. The broth reheats the meat and partially cooks into the rice, creating a cohesive dish.</li>
</ol>

<h3>How to Eat Somoori-gukbap Properly</h3>
<p>The serving style at Pohang Halmae-jip and similar traditional restaurants follows a specific format:</p>
<p>Your bowl arrives with the meat arranged on top of rice in a boiling broth. On the table, you will find: <strong>coarse sea salt (굵은소금)</strong>, chopped green onion (대파), minced garlic (다진마늘), and red chili flakes (고춧가루). The soup itself is deliberately unseasoned — the customer seasons it to personal preference.</p>
<p>Start by adding a pinch of salt and stirring. Taste. Add more salt, green onion, or garlic as desired. Some locals add a raw egg to the boiling broth, which cooks instantly into delicate egg ribbons. Others add a spoonful of <strong>saeu-jeot (새우젓, salted fermented shrimp)</strong> for deeper umami. There is no wrong way to season your bowl, but the salt-first approach lets you gauge the broth's natural depth before modifying it.</p>

<h2>Pohang: Korea's Seafood and Steel City</h2>
<p>Pohang (포항) is a city of contrasts that most international tourists bypass on their way to better-known destinations like Busan or Gyeongju. This oversight is their loss. Pohang offers a unique combination of industrial grit, natural beauty, and extraordinary food that rewards adventurous eaters.</p>

<h3>Geographic Advantage</h3>
<p>Pohang sits on the southeastern coast of the Korean peninsula where the Hyeongsangang River meets the East Sea (Sea of Japan). This location gives the city access to both freshwater and saltwater ecosystems, reflected in its diverse food scene. The Jukdo Market (죽도시장) — Pohang's central fish market — is one of Korea's largest, spanning 1,500 shops across a maze of covered alleys. The market is famous for <strong>gwamegi (과메기)</strong>, a semi-dried Pacific saury that is Pohang's signature winter delicacy.</p>

<h3>Gwamegi: Pohang's Most Distinctive Food</h3>
<p>Gwamegi deserves special attention because it is one of Korea's most unusual foods — a semi-dried fish that is neither fully raw nor fully dried, aged in the cold sea wind for 7-10 days during winter. The process originally used herring (청어) but now primarily uses Pacific saury (꽁치) due to herring scarcity.</p>
<p>The fish is hung on outdoor racks along the coast from December to February, where the alternating freeze-thaw cycle of cold nights and slightly warmer days creates a unique texture: firm but not hard, with concentrated umami flavor and a pleasant chewiness. Gwamegi is eaten wrapped in dried seaweed (김) with raw garlic, green chili, and a dab of gochujang. It pairs exceptionally well with soju, making it one of Korea's most popular anju (drinking snacks).</p>

<h3>Mul-hoe: Pohang's Cold Raw Fish Soup</h3>
<p>Another Pohang specialty is <strong>mul-hoe (물회)</strong> — a cold raw fish soup that originated as a fisherman's breakfast. Fresh raw fish (usually flatfish, squid, or sea cucumber) is served in an icy, sweet-spicy broth made from gochujang, vinegar, and cold water. Vegetables — cucumber, radish, perilla leaves — float alongside the fish. The dish is refreshing, light, and deeply satisfying in summer. At Jukdo Market, a generous bowl of mul-hoe costs 12,000-18,000 won ($9-14) — a fraction of Seoul restaurant prices for comparable quality.</p>

<h2>Day Trip Planning: Combining Pohang, Gyeongju, and the Coast</h2>
<p>Pohang's location makes it an excellent base for exploring Korea's southeast coast. Here is a realistic one-day food-focused itinerary:</p>
<ul>
<li><strong>7:00 AM</strong> — Somoori-gukbap breakfast at Pohang Halmae-jip. Arrive early for the freshest broth.</li>
<li><strong>9:00 AM</strong> — Drive 30 minutes to Homigot (호미곶), Korea's easternmost point. The sunrise monument and lighthouse are photogenic even if you miss the sunrise.</li>
<li><strong>10:30 AM</strong> — Head to Jukdo Market for gwamegi tasting and market snacks.</li>
<li><strong>12:00 PM</strong> — Lunch at one of the market's mul-hoe restaurants.</li>
<li><strong>1:30 PM</strong> — Drive 40 minutes south to Gyeongju (경주), the ancient Silla Dynasty capital. Visit Bulguksa Temple and Seokguram Grotto (UNESCO World Heritage Sites).</li>
<li><strong>4:30 PM</strong> — Gyeongju hwangnam-ppang (황남빵) — the city's famous red bean pastry, sold from shops around Daereungwon Tomb Complex.</li>
<li><strong>6:00 PM</strong> — Dinner at Gyeongju's Ssambap Street (쌈밥거리), where restaurants serve Korean BBQ with unlimited vegetable wraps.</li>
</ul>

<p>For more Korean food adventures, explore <a href="/busan-food-guide-8-dishes-you-can-only-find-in-koreas-coastal-city/">Busan's coastal cuisine just 1.5 hours south</a>, discover <a href="/korean-bbq-etiquette-12-rules-every-first-timer-needs-to-know/">Korean BBQ etiquette</a>, and learn about <a href="/soju-guide-for-beginners-how-to-drink-koreas-national-spirit-like-a-local/">Korea's national spirit, soju</a>.</p>
"""

# ── ID:23 — Imja Monkfish Soup ──
extra_23 = """
<h2>Agwi-jjim: Korea's Monkfish Mastery Explained</h2>
<p>Monkfish (아귀, agwi) occupies a peculiar position in Korean culinary history. For centuries, Korean fishermen considered it too ugly to eat and threw it back into the sea. Its bulbous head, gaping mouth full of needle-sharp teeth, and mottled brown skin made it one of the ocean's least attractive creatures. The fish that transformed Korean coastal cuisine was literally trash fish — until the port city of Masan discovered its potential in the 1960s.</p>
<p>The breakthrough came when Masan fishermen's wives, looking for ways to use every available protein during lean economic times, began braising monkfish with soybean sprouts in a spicy sauce. The result — <strong>agwi-jjim (아귀찜)</strong> — revealed monkfish's hidden virtue: its flesh, when properly cooked, has a lobster-like sweetness and a firm, almost meaty texture unlike any other fish. The cartilaginous skeleton means no small bones to worry about, and the liver (아귀 간, agwi-gan) is considered a delicacy comparable to foie gras in richness.</p>

<h3>Monkfish Anatomy: Why Each Part Tastes Different</h3>
<p>At restaurants like Imja, a quality monkfish dish showcases multiple textures from different body parts:</p>
<ul>
<li><strong>Tail meat (살)</strong> — The firmest, most lobster-like section. Dense, white, and slightly sweet. This is the premium cut that most resembles the monkfish tail sold in Western fish markets.</li>
<li><strong>Cheek meat (볼살)</strong> — Softer and more gelatinous than tail meat, with a higher collagen content that gives it a silky mouthfeel when braised.</li>
<li><strong>Liver (간)</strong> — Creamy, buttery, and intensely flavored. Korean monkfish liver is typically steamed and sliced, served with a ponzu-like dipping sauce. It rivals ankimo (Japanese monkfish liver) in quality but costs a fraction of the price.</li>
<li><strong>Skin (껍질)</strong> — The thick, gelatinous skin becomes incredibly tender when braised, developing a texture similar to braised oxtail. It is rich in collagen and is prized for both its texture and its beauty-enhancing reputation.</li>
<li><strong>Stomach and tripe (위, 내장)</strong> — For adventurous eaters. The stomach has a chewy, crunchy texture when quickly blanched, and is often served as a separate anju (drinking snack).</li>
</ul>

<h3>Fresh vs Dried Monkfish: Two Completely Different Dishes</h3>
<p>Korean monkfish cuisine splits into two distinct categories based on whether the fish is used fresh or dried, and understanding this distinction is crucial for ordering correctly.</p>
<p><strong>Fresh monkfish (생아귀)</strong> is used for agwi-jjim (braised) and agwi-tang (soup). The flesh is plump, moist, and relatively mild in flavor. Fresh monkfish dishes emphasize the sauce and accompanying ingredients (soybean sprouts, watercress, Korean radish) as much as the fish itself. Imja's monkfish soup falls into this category.</p>
<p><strong>Dried monkfish (코다리/건아귀)</strong> is a entirely different experience. The whole fish is hung in the cold winter wind to partially dry, concentrating its flavors and firming its texture dramatically. Dried monkfish is reconstituted and braised, resulting in a chewier, more intensely flavored dish that is popular as anju with soju. The drying process concentrates amino acids, creating an umami depth that fresh monkfish cannot match.</p>

<h2>The Soybean Sprout Connection: Why Kongnamul Matters</h2>
<p>No discussion of Korean monkfish cuisine is complete without addressing its inseparable partner: <strong>kongnamul (콩나물, soybean sprouts)</strong>. The combination of monkfish and bean sprouts is so fundamental that ordering one without the other would puzzle any Korean chef.</p>
<p>The pairing works on multiple levels. Scientifically, soybean sprouts contain <strong>asparagine</strong>, an amino acid that aids in alcohol metabolism — which is why kongnamul-guk (bean sprout soup) is Korea's most trusted hangover remedy. Since monkfish dishes are frequently consumed with soju, the sprouts serve a practical detoxification function alongside their culinary role.</p>
<p>Texturally, the crisp crunch of fresh bean sprouts contrasts perfectly with the soft, gelatinous monkfish flesh. The sprouts also absorb the spicy braising sauce, becoming flavor carriers that extend the dish's impact. In a well-made agwi-jjim, the sprouts on the bottom of the plate absorb the most sauce and are often the most flavorful bites.</p>

<h2>Gangnam's Surprising Seafood Scene</h2>
<p>Imja's location in Gangnam might seem counterintuitive — why would a serious seafood restaurant operate in Seoul's glitziest, most expensive neighborhood rather than near the coast? The answer reveals an important aspect of Korean food culture.</p>
<p>Gangnam (강남) is home to some of Seoul's most discerning eaters — business executives, entertainment industry figures, and affluent families who demand exceptional quality and are willing to pay for it. This customer base supports restaurants that can afford to source premium ingredients via Korea's sophisticated cold-chain logistics system.</p>
<p>Korean seafood distribution is remarkably efficient. Fish caught in Busan or Pohang at 4 AM can be on a Gangnam restaurant table by noon, transported in temperature-controlled vehicles via the KTX high-speed rail corridor or the Gyeongbu Expressway. This infrastructure means that a Gangnam seafood restaurant can serve fish that is nearly as fresh as a coastal restaurant — sometimes fresher, because Gangnam restaurants can cherry-pick the best catches rather than relying on whatever the local boats bring in.</p>

<h3>Hidden Seafood Gems Near Imja</h3>
<p>Imja sits in a Gangnam area that has quietly developed into a seafood dining cluster. Within walking distance, you will find:</p>
<ul>
<li><strong>Raw fish restaurants (횟집, hoetjip)</strong> — Several specialize in particular fish species rather than offering generic assortments. Look for ones that display their fish alive in tanks and slice to order.</li>
<li><strong>Ganjang-gejang specialists (간장게장)</strong> — Soy-marinated raw crab, often called "rice thief" (밥도둑) because the sweet, savory crab meat makes you eat bowl after bowl of rice involuntarily.</li>
<li><strong>Haemul-tang restaurants (해물탕)</strong> — Spicy seafood hot pot loaded with crab, shrimp, clams, octopus, and fish. These communal pots are designed for groups of 3-4 and typically cost 40,000-60,000 won for a large pot.</li>
</ul>

<h2>Korean Seafood Soup Culture: A Taxonomy</h2>
<p>Korean cuisine features an extraordinarily diverse range of seafood soups, each with distinct characteristics. Understanding this taxonomy helps you navigate Korean menus and appreciate where Imja's monkfish soup fits in the broader tradition:</p>

<table style="width:100%; border-collapse:collapse; max-width:100%;">
<tr style="background:#f0f0f0;"><th style="padding:10px; border:1px solid #ddd; text-align:left;">Soup Type</th><th style="padding:10px; border:1px solid #ddd; text-align:left;">Broth Character</th><th style="padding:10px; border:1px solid #ddd; text-align:left;">Key Ingredient</th><th style="padding:10px; border:1px solid #ddd; text-align:left;">Price Range</th></tr>
<tr><td style="padding:10px; border:1px solid #ddd;">아귀탕 (Agwi-tang)</td><td style="padding:10px; border:1px solid #ddd;">Spicy, rich, red</td><td style="padding:10px; border:1px solid #ddd;">Monkfish + sprouts</td><td style="padding:10px; border:1px solid #ddd;">15,000-25,000₩</td></tr>
<tr><td style="padding:10px; border:1px solid #ddd;">대구탕 (Daegu-tang)</td><td style="padding:10px; border:1px solid #ddd;">Clear, light, clean</td><td style="padding:10px; border:1px solid #ddd;">Cod + radish + tofu</td><td style="padding:10px; border:1px solid #ddd;">12,000-18,000₩</td></tr>
<tr><td style="padding:10px; border:1px solid #ddd;">매운탕 (Maeun-tang)</td><td style="padding:10px; border:1px solid #ddd;">Spicy, medium body</td><td style="padding:10px; border:1px solid #ddd;">Mixed fish + vegetables</td><td style="padding:10px; border:1px solid #ddd;">10,000-20,000₩</td></tr>
<tr><td style="padding:10px; border:1px solid #ddd;">꽃게탕 (Kkotge-tang)</td><td style="padding:10px; border:1px solid #ddd;">Sweet, spicy, complex</td><td style="padding:10px; border:1px solid #ddd;">Blue crab</td><td style="padding:10px; border:1px solid #ddd;">20,000-35,000₩</td></tr>
<tr><td style="padding:10px; border:1px solid #ddd;">해물탕 (Haemul-tang)</td><td style="padding:10px; border:1px solid #ddd;">Spicy, rich, busy</td><td style="padding:10px; border:1px solid #ddd;">Mixed seafood</td><td style="padding:10px; border:1px solid #ddd;">35,000-60,000₩</td></tr>
<tr><td style="padding:10px; border:1px solid #ddd;">조개탕 (Jogae-tang)</td><td style="padding:10px; border:1px solid #ddd;">Light, briny, clear</td><td style="padding:10px; border:1px solid #ddd;">Clams</td><td style="padding:10px; border:1px solid #ddd;">10,000-15,000₩</td></tr>
</table>

<p>For more Korean food exploration, read our <a href="/busan-food-guide-8-dishes-you-can-only-find-in-koreas-coastal-city/">Busan seafood guide</a>, discover <a href="/gwangjang-market-food-guide-seouls-oldest-market-and-its-legendary-eats/">Gwangjang Market's legendary eats</a>, and explore <a href="/how-to-order-food-in-korean-25-essential-phrases-every-traveler-needs/">essential Korean food ordering phrases</a>.</p>
"""

# ── Execute all expansions ──
print("=== Expanding 8 Travel & Food posts ===\n")

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

print("\n=== RESULTS ===")
under = []
for pid, title, wc in results:
    status = "OK" if wc >= 2500 else "NEEDS MORE"
    print(f"  ID:{pid} | {wc}w | {status} | {title}")
    if wc < 2500:
        under.append((pid, title, wc))

if under:
    print(f"\n{len(under)} posts still under 2500 words — need additional content")
else:
    print("\nAll 8 posts at 2500+ words!")
