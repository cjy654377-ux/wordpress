import requests, re, json, os

SITE = "https://rhythmicaleskimo.com"
REST = f"{SITE}/wp-json/wp/v2"

# --- Login ---
s = requests.Session()
s.cookies.set("wordpress_test_cookie", "WP+Cookie+check")
login = s.post(f"{SITE}/wp-login.php", data={
    "log": "cjy654377@gmail.com",
    "pwd": "Dkflekd1!!",
    "wp-submit": "Log In",
    "redirect_to": "/wp-admin/",
    "testcookie": "1"
}, allow_redirects=True)
print(f"Login status: {login.status_code}")

page = s.get(f"{SITE}/wp-admin/post-new.php").text
m = re.search(r'"nonce":"([a-f0-9]+)"', page)
if not m:
    m = re.search(r'_wpnonce=([a-f0-9]+)', page)
if not m:
    print("ERROR: Could not find nonce")
    exit(1)
nonce = m.group(1)
h = {"X-WP-Nonce": nonce}
print(f"Nonce: {nonce}")

# --- Find Korea Travel & Food category ---
cats = s.get(f"{REST}/categories", params={"per_page": 100}, headers=h).json()
travel_food_id = None
for c in cats:
    if "travel" in c["name"].lower() and "food" in c["name"].lower():
        travel_food_id = c["id"]
        print(f"Category: {c['name']} (ID: {c['id']})")
        break
if not travel_food_id:
    print("WARNING: Korea Travel & Food category not found, using ID 4")
    travel_food_id = 4

# --- Create tags ---
tag_names = ["spring cabbage bibimbap", "bomdong", "Korean food trend", "viral recipe 2026",
             "Korean street food", "bibimbap recipe", "Seoul food guide", "Korean cooking",
             "TikTok food trend", "convenience store Korea"]
tag_ids = []
for tn in tag_names:
    try:
        r = s.post(f"{REST}/tags", headers=h, json={"name": tn})
        if r.status_code == 201:
            tag_ids.append(r.json()["id"])
        elif "term_exists" in r.text:
            tid = r.json().get("data", {}).get("term_id", None)
            if tid:
                tag_ids.append(tid)
    except:
        pass
print(f"Tags: {tag_ids}")

# --- Upload featured image ---
img_path = "/Users/choijooyong/wordpress/featured_spring_bibimbap.png"
with open(img_path, "rb") as f:
    img_data = f.read()
media_r = s.post(f"{REST}/media", headers={
    **h,
    "Content-Disposition": "attachment; filename=spring-cabbage-bibimbap-viral-recipe-2026.png",
    "Content-Type": "image/png"
}, data=img_data)
if media_r.status_code == 201:
    media_id = media_r.json()["id"]
    media_url = media_r.json()["source_url"]
    print(f"Image uploaded: {media_id} -> {media_url}")
    # Update alt text
    s.post(f"{REST}/media/{media_id}", headers=h, json={
        "alt_text": "Spring cabbage bibimbap (bomdong bibimbap) - Korea's viral TikTok recipe for 2026 with fresh green leaves, gochujang sauce, and fried egg over rice"
    })
else:
    print(f"Image upload failed: {media_r.status_code} {media_r.text[:200]}")
    media_id = 0

# --- Article HTML ---
article_html = """
<p>Every spring, Korea's food scene delivers a new obsession. In 2026, that obsession has a name: <strong>bomdong bibimbap</strong> (봄동 비빔밥) &mdash; a brilliantly simple bowl of warm rice topped with crisp spring cabbage, a fiery gochujang-based sauce, and a runny fried egg. This dish has taken over TikTok, YouTube Shorts, and Korean social media with over <strong>5 million views</strong> on a single viral clip, sending spring cabbage prices soaring 78% and spawning convenience store versions nationwide.</p>

<p>But bomdong bibimbap is more than a fleeting internet trend. It is a celebration of Korean seasonal eating at its finest &mdash; affordable, nutritious, and ready in under 15 minutes. Whether you are planning a trip to Seoul, stocking up at a Korean grocery store abroad, or just curious about what everyone on your feed is eating, this guide covers everything you need to know.</p>

<h2>What Is Bomdong? The Spring Cabbage That Started It All</h2>

<p><strong>Bomdong</strong> (봄동) literally translates to "spring cabbage." It is a variety of napa cabbage harvested between late fall and early spring, primarily cultivated in the southern coastal regions of <strong>South Jeolla Province</strong>, which supplies over 90% of Korea's production. Unlike regular napa cabbage, bomdong grows with loose, flat, open leaves rather than forming a tight head.</p>

<p>What makes bomdong special is the cold. Winter temperatures concentrate the plant's natural sugars, resulting in a remarkably sweet flavor profile that sets it apart from cabbage harvested at other times of the year. The texture is equally distinctive: outer leaves deliver a satisfying, almost snappy crunch, while the inner leaves are soft enough to absorb any sauce you put near them.</p>

<h3>Bomdong vs. Regular Napa Cabbage: Key Differences</h3>

<div style="overflow-x:auto;">
<table style="width:100%;border-collapse:collapse;margin:1em 0;">
<thead><tr style="background:#f0f7e6;">
<th style="border:1px solid #ddd;padding:10px;text-align:left;">Feature</th>
<th style="border:1px solid #ddd;padding:10px;text-align:left;">Bomdong (Spring Cabbage)</th>
<th style="border:1px solid #ddd;padding:10px;text-align:left;">Regular Napa Cabbage</th>
</tr></thead>
<tbody>
<tr><td style="border:1px solid #ddd;padding:10px;">Season</td><td style="border:1px solid #ddd;padding:10px;">November &ndash; March</td><td style="border:1px solid #ddd;padding:10px;">Year-round</td></tr>
<tr><td style="border:1px solid #ddd;padding:10px;">Shape</td><td style="border:1px solid #ddd;padding:10px;">Flat, open leaves</td><td style="border:1px solid #ddd;padding:10px;">Tight cylindrical head</td></tr>
<tr><td style="border:1px solid #ddd;padding:10px;">Flavor</td><td style="border:1px solid #ddd;padding:10px;">Noticeably sweeter, less bitter</td><td style="border:1px solid #ddd;padding:10px;">Mild, slightly peppery</td></tr>
<tr><td style="border:1px solid #ddd;padding:10px;">Texture</td><td style="border:1px solid #ddd;padding:10px;">Crunchy outer, tender inner</td><td style="border:1px solid #ddd;padding:10px;">Uniformly crisp</td></tr>
<tr><td style="border:1px solid #ddd;padding:10px;">Beta-carotene (per 100g)</td><td style="border:1px solid #ddd;padding:10px;">1,015 mg (6x more)</td><td style="border:1px solid #ddd;padding:10px;">~170 mg</td></tr>
<tr><td style="border:1px solid #ddd;padding:10px;">Calories (per 100g)</td><td style="border:1px solid #ddd;padding:10px;">23 kcal</td><td style="border:1px solid #ddd;padding:10px;">16 kcal</td></tr>
<tr><td style="border:1px solid #ddd;padding:10px;">Best use</td><td style="border:1px solid #ddd;padding:10px;">Geotjeori, bibimbap, salads</td><td style="border:1px solid #ddd;padding:10px;">Kimchi, soups, stir-fry</td></tr>
</tbody></table>
</div>

<p>If you cannot find bomdong at your local Asian grocery, the inner leaves of napa cabbage or butterhead lettuce make acceptable substitutes &mdash; though neither will replicate that signature sweetness.</p>

<h2>How Kang Ho-dong Made Bibimbap Go Viral (Again)</h2>

<p>The 2026 bomdong bibimbap craze traces back to an unexpected source: an <strong>18-year-old TV clip</strong>. In a 2008 episode of KBS's beloved variety show <em>1 Night 2 Days</em> (1박 2일), comedian and entertainer <strong>Kang Ho-dong</strong> was filmed enthusiastically devouring a massive bowl of spring cabbage bibimbap during a rural filming trip. His exaggerated enjoyment &mdash; the vigorous mixing, the satisfied expressions, the sheer volume of food &mdash; became an iconic moment in Korean television history.</p>

<p>Fast forward to early 2026. Short-form content creators rediscovered the clip and began reposting it as a YouTube Short titled "Re-viewing Kang Ho-dong's legendary spring cabbage mukbang." The video <strong>surpassed 5 million views</strong> by late February, triggering an avalanche of copycat "bibimbap challenge" videos where creators attempted to replicate Kang Ho-dong's enthusiastic eating style with seasonal spring vegetables.</p>

<p>Social media mentions of "spring cabbage bibimbap" surged <strong>888% between December 2025 and January 2026</strong>, according to trend tracking data. The hashtag quickly overtook the previous viral food sensation &mdash; Dubai chewy cookies (두쫀쿠) &mdash; as Korea's most-searched food trend.</p>

<h3>Kang Ho-dong's Response</h3>

<p>On March 2, 2026, Coupang Play released a special segment on Kang Ho-dong's show <em>Kang Ho-dong's Bookstore</em> where the entertainer recreated his legendary 2008 bibimbap moment. The recreation video went viral in its own right, with fans commenting "감다살" (short for "감동의 다시 살아남" &mdash; "the emotion lives again"), further fueling the trend.</p>

<h2>The Complete Bomdong Bibimbap Recipe (15 Minutes)</h2>

<p>The beauty of bomdong bibimbap lies in its simplicity. You need no special equipment, no advanced cooking skills, and no more than 15 minutes from start to finish. Here is the full recipe, adapted from traditional Korean home cooking with tips gathered from Korea's most popular recipe platforms.</p>

<h3>Ingredients (Serves 2)</h3>

<p><strong>For the bowl:</strong></p>
<ul>
<li>1 head bomdong (spring cabbage), about 300g &mdash; or substitute with inner napa cabbage leaves</li>
<li>2 cups cooked warm white rice (short-grain Korean rice preferred)</li>
<li>2 eggs</li>
<li>1 tbsp sesame oil for frying</li>
<li>Toasted sesame seeds for garnish</li>
<li>Roasted seaweed flakes (gim-garu) for garnish (optional)</li>
</ul>

<p><strong>For the sauce (Simple Version):</strong></p>
<ul>
<li>2 tbsp gochugaru (Korean chili flakes)</li>
<li>1 tbsp soy sauce</li>
<li>1 tbsp sesame oil</li>
<li>&frac12; tbsp sugar</li>
<li>&frac12; tbsp rice vinegar</li>
<li>&frac12; tsp minced garlic</li>
<li>&frac12; tsp fish sauce (optional, adds umami depth)</li>
<li>Toasted sesame seeds</li>
</ul>

<p><strong>For the sauce (Full Geotjeori Version):</strong></p>
<ul>
<li>4 tbsp gochugaru</li>
<li>3 tbsp soy sauce</li>
<li>3 tbsp fish sauce (anchovy or sandlance)</li>
<li>2 tbsp sesame oil</li>
<li>2 tbsp rice vinegar</li>
<li>1 tbsp minced garlic</li>
<li>&frac12;&ndash;1 tbsp sugar</li>
<li>Toasted sesame seeds</li>
</ul>

<h3>Step-by-Step Instructions</h3>

<p><strong>Step 1: Prepare the spring cabbage (3 minutes)</strong></p>
<p>Cut off the base of the spring cabbage and separate the leaves one by one. Wash thoroughly between the stems where soil tends to hide. If thick stems are too tough, split them in half lengthwise. Shake or spin dry. Tear or cut leaves into rough 2&ndash;3 inch pieces.</p>

<p><strong>Step 2: Mix the sauce (2 minutes)</strong></p>
<p>Combine all sauce ingredients in a bowl and whisk until the sugar dissolves. Taste and adjust &mdash; the sauce should be spicy, slightly sweet, and tangy. The sugar is important: it suppresses the raw heat of gochugaru while enhancing the cabbage's natural sweetness.</p>

<p><strong>Step 3: Dress the cabbage (2 minutes)</strong></p>
<p>Add the torn cabbage to the sauce bowl. Toss with your hands (wear gloves if using the full geotjeori version) or tongs until every leaf is evenly coated. Let it sit for 2&ndash;3 minutes to slightly wilt &mdash; this is when the magic happens as the cabbage absorbs the dressing.</p>

<p><strong>Step 4: Fry the eggs (3 minutes)</strong></p>
<p>Heat sesame oil in a non-stick pan over medium heat. Crack in eggs and fry sunny-side-up until the whites are set but the yolk remains runny. A runny yolk is non-negotiable &mdash; it becomes part of the sauce when you mix.</p>

<p><strong>Step 5: Assemble and mix (2 minutes)</strong></p>
<p>Scoop warm rice into a large bowl. Pile the dressed spring cabbage on top. Place the fried egg on the crown. Drizzle a final swirl of sesame oil and sprinkle toasted sesame seeds and seaweed flakes. Now mix everything together vigorously &mdash; as Kang Ho-dong demonstrated, the key is to really commit to the mixing. Every grain of rice should be coated.</p>

<h3>Pro Tips</h3>
<ul>
<li><strong>Use warm rice</strong> &mdash; Cold rice will not absorb the sauce properly and the temperature contrast with the egg will be wrong.</li>
<li><strong>Do not overdress</strong> &mdash; Start with 1&ndash;2 tablespoons of sauce per serving. You can always add more, but you cannot take it away.</li>
<li><strong>Add extras</strong> &mdash; Canned tuna, sliced spam, or stir-fried ground pork all make excellent protein additions.</li>
<li><strong>Substitute greens</strong> &mdash; No bomdong? Use a mix of romaine hearts and inner napa cabbage leaves for similar crunch-to-tender ratio.</li>
</ul>

<p>For more iconic Korean rice dishes with regional twists, check out our guide on <a href="/jeonju-bibimbap-vs-seoul-bibimbap-whats-the-difference-and-where-to-ea/">Jeonju Bibimbap vs. Seoul Bibimbap</a> to understand how bibimbap styles vary across Korea.</p>

<h2>Convenience Store Versions: Bomdong Bibimbap on the Go</h2>

<p>Korean convenience stores are legendary for transforming viral food trends into grab-and-go products within weeks. The bomdong bibimbap craze was no exception. Here is how the major chains responded:</p>

<h3>GS25: Jeongseong Gadeuk Bomdong Bibimbap (정성가득 봄동비빔밥)</h3>

<p>GS25 was the first mover, launching its bomdong bibimbap lunchbox as a <strong>March-only seasonal item</strong> at <strong>4,900 won</strong> (~$3.35). The product uses domestic spring cabbage pickled vegetables made in collaboration with <strong>Jonggga</strong> (종가), Korea's leading kimchi brand. Each box includes spring cabbage geotjeori, assorted vegetables, a fried egg, meat topping, and a sesame oil packet.</p>

<p>Before the full launch, GS25 offered a pre-order set through its "Our Neighborhood GS" (우리동네GS) app on March 3. The initial run of <strong>1,000 units sold out instantly</strong>, forcing an expansion to 2,500 units &mdash; which also sold out within hours.</p>

<h3>Emart24: Fresh Spring Cabbage Promotion</h3>

<p>Rather than a ready-made lunchbox, Emart24 took a different approach with a <strong>presale discount promotion on fresh spring cabbage</strong>, targeting customers who prefer to make the dish at home. The chain positioned itself as the affordable ingredient supplier for the DIY crowd.</p>

<h3>CU: Ready-Made Bibimbap Line</h3>

<p>CU announced plans for its own bomdong bibimbap product, competing directly with GS25 for the seasonal convenience store market. Details on pricing and availability were still emerging at time of writing.</p>

<div style="overflow-x:auto;">
<table style="width:100%;border-collapse:collapse;margin:1em 0;">
<thead><tr style="background:#f0f7e6;">
<th style="border:1px solid #ddd;padding:10px;text-align:left;">Chain</th>
<th style="border:1px solid #ddd;padding:10px;text-align:left;">Product</th>
<th style="border:1px solid #ddd;padding:10px;text-align:left;">Price</th>
<th style="border:1px solid #ddd;padding:10px;text-align:left;">Availability</th>
<th style="border:1px solid #ddd;padding:10px;text-align:left;">Highlight</th>
</tr></thead>
<tbody>
<tr><td style="border:1px solid #ddd;padding:10px;">GS25</td><td style="border:1px solid #ddd;padding:10px;">정성가득 봄동비빔밥</td><td style="border:1px solid #ddd;padding:10px;">4,900 won</td><td style="border:1px solid #ddd;padding:10px;">March only</td><td style="border:1px solid #ddd;padding:10px;">Jonggga kimchi collab</td></tr>
<tr><td style="border:1px solid #ddd;padding:10px;">Emart24</td><td style="border:1px solid #ddd;padding:10px;">Fresh bomdong (DIY)</td><td style="border:1px solid #ddd;padding:10px;">~3,000 won</td><td style="border:1px solid #ddd;padding:10px;">While stocks last</td><td style="border:1px solid #ddd;padding:10px;">Presale discount</td></tr>
<tr><td style="border:1px solid #ddd;padding:10px;">CU</td><td style="border:1px solid #ddd;padding:10px;">Bomdong bibimbap (TBA)</td><td style="border:1px solid #ddd;padding:10px;">TBA</td><td style="border:1px solid #ddd;padding:10px;">Spring 2026</td><td style="border:1px solid #ddd;padding:10px;">Competing launch</td></tr>
</tbody></table>
</div>

<p>If you are visiting Korea and want to explore more convenience store treasures, our <a href="/korean-convenience-store-food-ranking-top-20-must-try-items-at-cu-gs25/">Korean Convenience Store Food Ranking: Top 20 Must-Try Items</a> is the definitive guide to navigating GS25, CU, and Emart24 like a local.</p>

<h2>Where to Eat Bomdong Bibimbap in Seoul</h2>

<p>While bomdong bibimbap is fundamentally a home-cooked dish, several Seoul restaurants have added it to their menus as a seasonal special. Here are the best spots to try it during spring 2026:</p>

<h3>1. Sangdo Neulbori &mdash; Bongcheon Station (상도늘보리 봉천역점)</h3>
<ul>
<li><strong>Address:</strong> 379 Bongcheon-ro, Gwanak-gu, Seoul (서울 관악구 봉천로 379)</li>
<li><strong>Hours:</strong> Daily 11:30&ndash;22:00 (weekday break 15:30&ndash;16:30, last order 21:00)</li>
<li><strong>Getting there:</strong> 3-minute walk from Bongcheon Station Exit 5</li>
<li><strong>What to expect:</strong> A self-service concept where spring cabbage and sides are provided at a counter. You mix your own bibimbap with rice, gochujang, and sesame oil to your preferred ratio. Popular with university students for generous portions at reasonable prices.</li>
</ul>

<h3>2. Seochon Nugak &mdash; Seongbuk-dong (서촌누각)</h3>
<ul>
<li><strong>Address:</strong> Seongbuk-dong, Seongbuk-gu, Seoul</li>
<li><strong>What to expect:</strong> A refined take on seasonal vegetable bibimbap. The set meals here emphasize the pure flavor and texture of seasonal ingredients over heavy seasoning. Their spring menu features bomdong alongside shepherd's purse and wild chives. Reservation recommended during peak lunch hours.</li>
</ul>

<h3>3. Somun Bapsang &mdash; City Hall (소문밥상)</h3>
<ul>
<li><strong>Address:</strong> B1 Floor B104-6, 124 Seosokmun-ro, Jung-gu, Seoul (서울 중구 서소문로 124 B1층 B104-6)</li>
<li><strong>Getting there:</strong> Near City Hall Station</li>
<li><strong>What to expect:</strong> A limited Friday lunch-only spot using spring cabbage, arugula, and wild garlic sourced fresh from Gyeongdong Market. The sesame oil is freshly pressed and whole sesame seeds are used &mdash; small details that elevate the dish. Arrive early as servings are limited.</li>
</ul>

<h3>4. Gwangjang Market (광장시장)</h3>
<p>While not specifically a bomdong bibimbap destination, Gwangjang Market's bibimbap vendors have historically incorporated seasonal greens into their offerings during spring. Multiple stalls in the market's food alley offer variations. For a complete market food experience, read our <a href="/gwangjang-market-food-guide-seouls-oldest-market-and-its-legendary-eat/">Gwangjang Market Food Guide</a>.</p>

<p>When ordering at any of these spots, knowing a few Korean food phrases goes a long way. Our guide on <a href="/how-to-order-food-in-korean-25-essential-phrases-every-traveler-needs/">How to Order Food in Korean: 25 Essential Phrases</a> will help you navigate menus and communicate with restaurant staff confidently.</p>

<h2>Nutrition, Health Benefits, and Risks</h2>

<p>Bomdong bibimbap is often praised as a healthier alternative to other viral food trends. At <strong>23 calories per 100g</strong>, spring cabbage is a nutritional powerhouse compared to, say, the 600+ calories per Dubai chewy cookie it replaced as Korea's top food trend. But the full picture is more nuanced.</p>

<h3>Nutritional Benefits of Spring Cabbage</h3>

<div style="overflow-x:auto;">
<table style="width:100%;border-collapse:collapse;margin:1em 0;">
<thead><tr style="background:#f0f7e6;">
<th style="border:1px solid #ddd;padding:10px;text-align:left;">Nutrient (per 100g)</th>
<th style="border:1px solid #ddd;padding:10px;text-align:left;">Bomdong</th>
<th style="border:1px solid #ddd;padding:10px;text-align:left;">Significance</th>
</tr></thead>
<tbody>
<tr><td style="border:1px solid #ddd;padding:10px;">Calories</td><td style="border:1px solid #ddd;padding:10px;">23 kcal</td><td style="border:1px solid #ddd;padding:10px;">Very low-calorie</td></tr>
<tr><td style="border:1px solid #ddd;padding:10px;">Beta-carotene</td><td style="border:1px solid #ddd;padding:10px;">1,015 mg</td><td style="border:1px solid #ddd;padding:10px;">6x more than regular cabbage</td></tr>
<tr><td style="border:1px solid #ddd;padding:10px;">Vitamin C</td><td style="border:1px solid #ddd;padding:10px;">2x regular cabbage</td><td style="border:1px solid #ddd;padding:10px;">Immune support, skin health</td></tr>
<tr><td style="border:1px solid #ddd;padding:10px;">Calcium</td><td style="border:1px solid #ddd;padding:10px;">2x that of eggs</td><td style="border:1px solid #ddd;padding:10px;">Bone health</td></tr>
<tr><td style="border:1px solid #ddd;padding:10px;">Fiber</td><td style="border:1px solid #ddd;padding:10px;">High</td><td style="border:1px solid #ddd;padding:10px;">Digestive health, blood sugar control</td></tr>
<tr><td style="border:1px solid #ddd;padding:10px;">Oxalate</td><td style="border:1px solid #ddd;padding:10px;">Low</td><td style="border:1px solid #ddd;padding:10px;">Kidney-friendly</td></tr>
</tbody></table>
</div>

<p>Additional benefits include antioxidant and anti-inflammatory compounds, support for blood sugar regulation due to high fiber and low glycemic index, and the fact that bomdong retains much of its nutritional value even when cooked.</p>

<h3>Health Risks and Warnings</h3>

<p>Health experts have flagged several concerns that viral recipe videos tend to skip:</p>

<p><strong>1. Sodium overload from the sauce.</strong> Gochujang contains approximately <strong>2,340&ndash;2,474 mg of sodium per 100g</strong>. Combined with soy sauce and fish sauce, a single bowl of bomdong bibimbap can easily exceed half the recommended daily sodium intake. People with hypertension should use reduced-sodium soy sauce and limit gochujang to 1 tablespoon.</p>

<p><strong>2. "Cold-natured food" in Korean medicine.</strong> In traditional Korean medicine (한의학), spring cabbage is classified as a <strong>cold-natured food</strong> (찬 성질). Excessive consumption may cause abdominal pain or diarrhea in some individuals, particularly those with sensitive digestive systems. Combining it with warm-natured ingredients like chili peppers, ginger, and green onions (all present in the sauce) can help neutralize this effect.</p>

<p><strong>3. Hidden sugar in the sauce.</strong> Many viral recipes call for generous amounts of sugar and plum syrup. While this balances the heat, people with diabetes should be mindful of the total sugar content per serving.</p>

<p>As Dr. Lee Je-kyun of Daegu Jaseng Korean Medicine Hospital advises: <em>"Rather than blindly following social media recipes, consumers should consider their individual constitution and eating habits for balanced intake."</em></p>

<h2>The Market Impact: How a Meme Moved an Entire Industry</h2>

<p>The bomdong bibimbap trend is a case study in how social media can reshape agricultural economics in real time.</p>

<h3>Price Surge Timeline</h3>
<ul>
<li><strong>January 3, 2026:</strong> Wholesale price for 15kg top-grade spring cabbage at Garak Market &mdash; 22,618 won</li>
<li><strong>February 24, 2026:</strong> Price surged <strong>78.2%</strong> year-on-year to 53,996 won</li>
<li><strong>February 28, 2026:</strong> Price reached 36,281 won ($24.80), a <strong>60% increase</strong> from January</li>
<li><strong>Emart sales:</strong> Bomdong sales jumped <strong>78.3%</strong> year-on-year in February</li>
<li><strong>Kim's Club:</strong> Approximately <strong>25% growth</strong> in spring cabbage sales</li>
</ul>

<p>South Jeolla Province, which produces over 90% of Korea's spring cabbage, suddenly found itself at the center of a supply crunch. Farmers who had planted normal seasonal quantities were caught off guard by demand that far exceeded historical norms.</p>

<p>This pattern mirrors previous SNS-driven food crazes in Korea &mdash; from the sugar-laden Dubai chewy cookies to the rosemary lemonade trend of 2025 &mdash; but the bomdong situation is unique because it involves a fresh, perishable agricultural product with a limited growing season. Unlike manufactured snacks that can scale production, spring cabbage has a biological ceiling.</p>

<h2>Bomdong Bibimbap for Travelers: Practical Tips</h2>

<p>If you are visiting Korea during spring (February through April), here is how to make the most of bomdong season:</p>

<p><strong>At restaurants:</strong> Look for "봄동 비빔밥" on menus or chalkboard specials. Many Korean restaurants rotate their menus seasonally, so ask staff "봄동 비빔밥 있어요?" (Bomdong bibimbap isseoyo? &mdash; "Do you have spring cabbage bibimbap?").</p>

<p><strong>At convenience stores:</strong> Head to any GS25 during March 2026 for the limited-edition lunchbox at 4,900 won. Heat it in the store's microwave (except the cabbage packet &mdash; add that cold after heating the rice).</p>

<p><strong>At traditional markets:</strong> Visit <a href="/gwangjang-market-food-guide-seouls-oldest-market-and-its-legendary-eat/">Gwangjang Market</a> or Gyeongdong Market (경동시장) for fresh bomdong to take back to your Airbnb kitchen. Bundles typically cost 2,000&ndash;4,000 won depending on size and the current market price.</p>

<p><strong>DIY in your accommodation:</strong> Korean guesthouses and Airbnbs almost always have a rice cooker. Buy bomdong, gochugaru, soy sauce, sesame oil, and eggs from any convenience store or supermarket. Total cost: under 8,000 won for two servings.</p>

<p>For more Korean street food and market discoveries, browse our <a href="/the-ultimate-guide-to-korean-street-food-15-must-try-snacks-and-where-/">Ultimate Guide to Korean Street Food: 15 Must-Try Snacks</a>.</p>

<h2>Frequently Asked Questions</h2>

<h3>What is bomdong bibimbap?</h3>
<p>Bomdong bibimbap is a Korean rice dish made with bomdong (봄동), a type of spring cabbage that is sweeter and more tender than regular napa cabbage. The cabbage is dressed in a spicy-sweet sauce made from gochugaru (Korean chili flakes), soy sauce, sesame oil, and garlic, then served over warm rice with a fried egg. It is a seasonal dish best enjoyed between January and March when spring cabbage is at peak sweetness.</p>

<h3>Why did bomdong bibimbap go viral in 2026?</h3>
<p>A 2008 clip from KBS's variety show <em>1 Night 2 Days</em> featuring comedian Kang Ho-dong enthusiastically eating spring cabbage bibimbap was rediscovered and reposted as a YouTube Short in early 2026. The video surpassed 5 million views, inspiring a wave of "bibimbap challenge" content across TikTok and Korean social media. Social media mentions increased 888% between December 2025 and January 2026.</p>

<h3>Where can I buy bomdong outside Korea?</h3>
<p>Bomdong is available at well-stocked Korean and Asian grocery stores during late winter and early spring, particularly H Mart, Zion Market, and 99 Ranch Market in the US. If you cannot find bomdong specifically, the inner leaves of napa cabbage or butterhead lettuce are the closest substitutes, though they lack bomdong's distinctive sweetness.</p>

<h3>Is bomdong bibimbap healthy?</h3>
<p>Spring cabbage itself is very healthy &mdash; only 23 calories per 100g with high levels of beta-carotene, vitamin C, calcium, and fiber. However, the sauce can be high in sodium (from soy sauce and gochujang) and sugar. For a healthier version, use reduced-sodium soy sauce, limit gochujang to 1 tablespoon, and reduce or skip the added sugar. The assembled dish with rice and egg provides a balanced meal of carbohydrates, protein, fiber, and micronutrients.</p>

<h3>Can I make bomdong bibimbap without gochugaru?</h3>
<p>Yes. For a non-spicy version, dress the cabbage with a mixture of soy sauce, sesame oil, rice vinegar, minced garlic, and a pinch of sugar. The result is milder but still delicious, and it allows the natural sweetness of the spring cabbage to shine through. This version is popular for children and those who cannot tolerate spicy food.</p>

<h3>How long does the bomdong bibimbap season last?</h3>
<p>Bomdong is typically available from November through March, with peak flavor and sweetness in January through March when winter cold has concentrated the sugars. By April, the season is essentially over as warmer temperatures change the cabbage's flavor profile. The 2026 convenience store versions are limited to March only.</p>

<hr>

<h2>You Might Also Enjoy</h2>
<ul>
<li><a href="/jeonju-bibimbap-vs-seoul-bibimbap-whats-the-difference-and-where-to-ea/">Jeonju Bibimbap vs. Seoul Bibimbap: What's the Difference and Where to Eat</a></li>
<li><a href="/korean-convenience-store-food-ranking-top-20-must-try-items-at-cu-gs25/">Korean Convenience Store Food Ranking: Top 20 Must-Try Items at CU, GS25</a></li>
<li><a href="/the-ultimate-guide-to-korean-street-food-15-must-try-snacks-and-where-/">The Ultimate Guide to Korean Street Food: 15 Must-Try Snacks</a></li>
</ul>

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is bomdong bibimbap?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Bomdong bibimbap is a Korean rice dish made with bomdong (봄동), a type of spring cabbage that is sweeter and more tender than regular napa cabbage. The cabbage is dressed in a spicy-sweet sauce made from gochugaru, soy sauce, sesame oil, and garlic, then served over warm rice with a fried egg. It is a seasonal dish best enjoyed between January and March."
      }
    },
    {
      "@type": "Question",
      "name": "Why did bomdong bibimbap go viral in 2026?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "A 2008 clip from KBS's 1 Night 2 Days featuring Kang Ho-dong eating spring cabbage bibimbap was rediscovered as a YouTube Short in early 2026. The video surpassed 5 million views, inspiring bibimbap challenge content across TikTok and Korean social media. Mentions increased 888% between December 2025 and January 2026."
      }
    },
    {
      "@type": "Question",
      "name": "Where can I buy bomdong outside Korea?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Bomdong is available at Korean and Asian grocery stores like H Mart, Zion Market, and 99 Ranch Market during late winter and early spring. If unavailable, the inner leaves of napa cabbage or butterhead lettuce are the closest substitutes."
      }
    },
    {
      "@type": "Question",
      "name": "Is bomdong bibimbap healthy?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Spring cabbage itself is very healthy at only 23 calories per 100g with high beta-carotene, vitamin C, calcium, and fiber. However, the sauce can be high in sodium and sugar. For a healthier version, use reduced-sodium soy sauce and limit gochujang to 1 tablespoon."
      }
    },
    {
      "@type": "Question",
      "name": "Can I make bomdong bibimbap without gochugaru?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes. For a non-spicy version, dress the cabbage with soy sauce, sesame oil, rice vinegar, minced garlic, and a pinch of sugar. This milder version allows the natural sweetness of spring cabbage to shine and is popular for children."
      }
    },
    {
      "@type": "Question",
      "name": "How long does the bomdong bibimbap season last?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Bomdong is available from November through March, with peak sweetness in January through March. By April the season ends. The 2026 convenience store versions are limited to March only."
      }
    }
  ]
}
</script>
"""

# --- Publish ---
post_data = {
    "title": "Spring Cabbage Bibimbap: Korea's Viral Recipe [2026]",
    "content": article_html.strip(),
    "status": "publish",
    "categories": [travel_food_id],
    "tags": tag_ids,
    "excerpt": "Korea's hottest food trend of 2026: bomdong bibimbap. Learn the 15-minute recipe, find Seoul restaurants, compare convenience store versions, and discover why an 18-year-old Kang Ho-dong clip broke the internet.",
    "featured_media": media_id,
    "meta": {
        "_yoast_wpseo_metadesc": "Spring cabbage bibimbap (bomdong bibimbap) is Korea's #1 viral food trend in 2026. Full recipe, Seoul restaurants, convenience store versions, and health tips."
    }
}

r = s.post(f"{REST}/posts", headers=h, json=post_data)
if r.status_code == 201:
    post = r.json()
    print(f"\nPUBLISHED!")
    print(f"ID: {post['id']}")
    print(f"URL: {post['link']}")
    print(f"Title: {post['title']['rendered']}")
else:
    print(f"Publish failed: {r.status_code}")
    print(r.text[:500])
