#!/usr/bin/env python3
"""Add FAQ Schema JSON-LD to 16 posts that lack it."""
import requests, re, sys, json, html

SITE = "https://rhythmicaleskimo.com"
REST = f"{SITE}/wp-json/wp/v2"
USER = "cjy654377@gmail.com"
PASS = "Dkflekd1!!"

def login():
    s = requests.Session()
    s.cookies.set("wordpress_test_cookie", "WP+Cookie+check")
    s.post(f"{SITE}/wp-login.php", data={
        "log": USER, "pwd": PASS, "wp-submit": "Log In",
        "redirect_to": "/wp-admin/", "testcookie": "1"
    }, allow_redirects=True)
    page = s.get(f"{SITE}/wp-admin/post-new.php").text
    m = re.search(r'"nonce":"([a-f0-9]+)"', page)
    if not m:
        print("ERROR: nonce not found"); sys.exit(1)
    return s, {"X-WP-Nonce": m.group(1)}

# FAQ data per post ID
FAQ_DATA = {
    11: {
        "title": "Bangi Gullim Mandu Ttegul",
        "faqs": [
            {"q": "Do I need a reservation at Bangi Gullim Mandu Ttegul in Seoul?",
             "a": "Reservations are not accepted — it operates on a first-come, first-served basis. Weekday lunch (11:30 AM–1 PM) sees the longest lines, so arriving 15–20 minutes before opening is recommended. Weekend afternoons tend to be slightly less crowded."},
            {"q": "What makes the hand-rolled dumplings at Bangi Gullim Mandu Ttegul different from regular Korean mandu?",
             "a": "Each dumpling is hand-rolled to order using a thick, chewy dough wrapper rather than the thin machine-pressed skins used at most restaurants. The filling is a generous mix of pork, tofu, kimchi, and glass noodles, making each piece roughly 2–3 times larger than standard Korean mandu."},
            {"q": "Is Bangi Gullim Mandu Ttegul accessible by public transit?",
             "a": "Yes, it is a 5-minute walk from Bangi Station (Seoul Metro Line 5, Exit 4). The restaurant is located in a residential alley in Songpa-gu, so using Naver Map or KakaoMap with the Korean name (반기 굴림만두 떡을) is the easiest way to navigate there."},
        ]
    },
    13: {
        "title": "World Bap",
        "faqs": [
            {"q": "How much does the all-you-can-eat buffet at World Bap in Gwangju actually cost?",
             "a": "The lunch buffet is priced at approximately 8,000 KRW (around $6 USD), making it one of the most affordable unlimited Korean buffets in the country. Dinner pricing is slightly higher at around 9,000–10,000 KRW. Prices may vary seasonally."},
            {"q": "What types of dishes are available at World Bap's buffet?",
             "a": "The buffet features 40+ rotating Korean dishes including japchae, various kimchi varieties, stir-fried pork, doenjang-jjigae, seasonal namul (vegetable side dishes), rice, and fresh fruit. The menu changes daily based on ingredient availability and season."},
            {"q": "Is World Bap suitable for vegetarians or people with dietary restrictions?",
             "a": "While there is no dedicated vegetarian menu, the buffet typically includes 10–15 vegetable-based banchan (side dishes), rice, and tofu soup. However, many Korean dishes use anchovy or shrimp-based broths, so strict vegetarians should ask staff about specific items."},
        ]
    },
    15: {
        "title": "Yasanhaechon",
        "faqs": [
            {"q": "Why is Yasanhaechon in Yangpyeong famous among Korean celebrities?",
             "a": "Trot singer Seol Woon-do publicly named Yasanhaechon as his favorite fresh cod soup (saengtae-tang) restaurant, which led to a surge in popularity. The restaurant has since been featured on multiple Korean TV food shows, drawing visitors from Seoul who make the 1-hour drive specifically for this dish."},
            {"q": "What is saengtae-tang and how is it different from regular Korean fish soup?",
             "a": "Saengtae-tang (생태탕) is a spicy soup made with fresh (not dried) pollock or cod, Korean radish, tofu, and egg. Unlike dried pollock soup (bugeoguk), the fresh fish gives a cleaner, more delicate flavor with tender, flaky flesh. Yasanhaechon uses fish sourced daily from local markets."},
            {"q": "How do I get to Yasanhaechon from Seoul without a car?",
             "a": "Take the Gyeongui-Jungang Line from Seoul Station or Yongsan Station to Yangpyeong Station (approximately 1 hour). From there, a taxi ride costs about 5,000–8,000 KRW. Alternatively, intercity buses run from Seoul's Dong Seoul Terminal to Yangpyeong every 20–30 minutes."},
        ]
    },
    17: {
        "title": "Jun (준)",
        "faqs": [
            {"q": "What is the signature dish at Jun restaurant in Daegu?",
             "a": "The signature dish is the King Rib Seafood Stone Plate Jjajang (왕갈비 해물 돌판 짜장), which combines massive pork ribs with seafood and jjajang sauce served sizzling on a stone plate. This unique fusion dish is not found at typical Chinese-Korean restaurants and costs around 15,000–18,000 KRW per serving."},
            {"q": "Is Jun restaurant in Daegu worth the trip from Seoul?",
             "a": "Many food enthusiasts take the KTX from Seoul to Daegu (1 hour 40 minutes) specifically to visit Jun. The restaurant offers a completely unique take on Korean-Chinese cuisine that you cannot find elsewhere, with generous portions that typically satisfy even heavy eaters. Combining it with other Daegu attractions makes it a worthwhile day trip."},
            {"q": "Does Jun restaurant in Daegu accept credit cards and have English menus?",
             "a": "The restaurant accepts all major Korean credit cards and cash. There is no official English menu, but the staff can assist with basic ordering. Taking a screenshot of the Korean menu items mentioned in food blogs and showing it to staff is the easiest approach for non-Korean speakers."},
        ]
    },
    19: {
        "title": "Seomyeon Sondubu-jip",
        "faqs": [
            {"q": "What makes Seomyeon Sondubu-jip's handmade tofu different from regular Korean sundubu?",
             "a": "The tofu at Seomyeon Sondubu-jip is made fresh daily on-site using traditional stone-grinding methods passed down through generations. Unlike factory-produced sundubu, this handmade version has a noticeably creamier texture and a subtle nutty soybean flavor that sets it apart from chain restaurant tofu dishes."},
            {"q": "What is included in the set meal at Seomyeon Sondubu-jip in Chuncheon?",
             "a": "The set meal typically includes the signature handmade sundubu-jjigae, steamed rice, 6–8 banchan (side dishes), and homemade dubu-buchimgae (tofu pancake). The generous portion and quality of side dishes make it excellent value, usually priced around 9,000–12,000 KRW per person."},
            {"q": "How do I get to Seomyeon Sondubu-jip from Seoul?",
             "a": "Take the ITX-Cheongchun train from Yongsan or Cheongnyangni Station to Chuncheon Station (about 1 hour 20 minutes). The restaurant is accessible by local bus or a short taxi ride from the station. Chuncheon is also a popular day-trip destination with Nami Island and Dakgalbi Street nearby."},
        ]
    },
    21: {
        "title": "Gukbo 1st",
        "faqs": [
            {"q": "Is the beef noodle soup at Gukbo 1st really unlimited refills for $10?",
             "a": "Yes, Gukbo 1st offers unlimited refills of their Korean beef noodle soup (guksu) as part of their set meal, which also includes bossam (boiled pork wraps). The set is priced at approximately 12,000–13,000 KRW (around $10 USD). Most customers go through 2–3 bowls of the rich, beefy broth."},
            {"q": "What cuts of beef does Gukbo 1st use in their soup?",
             "a": "The restaurant uses a combination of beef brisket and leg bones simmered for over 12 hours to create their signature milky-white broth (seolleongtang style). The sliced beef served in each bowl is tender brisket, and the bone marrow enriches the soup's depth of flavor significantly."},
            {"q": "Where exactly is Gukbo 1st located in Bucheon and how do I get there?",
             "a": "Gukbo 1st is located near Bucheon Station on Seoul Metro Line 1, making it easily accessible from central Seoul in about 30–40 minutes. The restaurant is within a 5-minute walk from Exit 1 of Bucheon Station. Search '국보1st' on Naver Map for exact navigation."},
        ]
    },
    23: {
        "title": "Imja",
        "faqs": [
            {"q": "What is the free liver service at Imja restaurant in Gangnam?",
             "a": "Imja provides complimentary monkfish liver (agwi-gan) as a side dish when you order their monkfish soup. This is highly unusual — monkfish liver is considered a delicacy in Korea and is typically charged as a premium add-on at most restaurants. The liver is lightly steamed and served with a ponzu-like dipping sauce."},
            {"q": "What are the three styles of monkfish soup available at Imja?",
             "a": "Imja offers three distinct preparations: the classic spicy agwi-jjim (braised monkfish with bean sprouts), a clear broth agwi-tang for those who prefer milder flavors, and a rich doenjang (fermented soybean paste) based monkfish stew. Each style highlights different aspects of the fresh monkfish's flavor and texture."},
            {"q": "How much does a meal at Imja in Gangnam typically cost?",
             "a": "Main dishes range from 15,000 to 25,000 KRW per person depending on the preparation style and portion size. Given Gangnam's premium location and the quality of fresh monkfish used, this is considered very reasonable. The free liver service adds significant value compared to competitors in the area."},
        ]
    },
    25: {
        "title": "Haengju Chueotang",
        "faqs": [
            {"q": "What is chueotang and why is Haengju Chueotang considered the best?",
             "a": "Chueotang (추어탕) is a traditional Korean loach soup where the freshwater fish is ground into the broth, creating a thick, savory, and highly nutritious soup. Haengju Chueotang has been serving this dish for decades near Haengju Fortress, earning celebrity endorsements including comedian Kim Mi-ryeo, who visits regularly."},
            {"q": "Is loach soup (chueotang) safe to eat for first-time visitors?",
             "a": "Absolutely. The loach is thoroughly ground and slow-cooked into the broth, so there are no bones or recognizable fish parts. The soup tastes similar to a rich, earthy doenjang-jjigae and is packed with protein, calcium, and iron. It has been a staple Korean health food for centuries and is especially popular in autumn and winter."},
            {"q": "Can I visit Haengju Fortress and eat at Haengju Chueotang in the same trip?",
             "a": "Yes, this is the ideal plan. Haengju Fortress (행주산성) is a scenic historic site with easy walking trails and panoramic views of the Han River. The restaurant cluster at the fortress entrance specializes in chueotang. The entire trip from Seoul takes about 1 hour by subway (Line 3 to Gupabal, then bus) and makes a perfect half-day excursion."},
        ]
    },
    27: {
        "title": "Pohang Halmae-jip",
        "faqs": [
            {"q": "How long has Pohang Halmae-jip been operating in Yeongcheon Market?",
             "a": "Pohang Halmae-jip has been serving ox head soup for approximately 70 years, now run by the 3rd generation of the founding family. This extraordinary longevity in Korea's competitive restaurant scene speaks to the consistent quality of their signature dish and their deep roots in the Yeongcheon market community."},
            {"q": "What makes ox head soup (someori-gukbap) at Pohang Halmae-jip special?",
             "a": "The soup uses ox head meat slow-simmered for over 15 hours, resulting in an incredibly rich, collagen-heavy broth with meltingly tender meat. Unlike chain restaurants that use powdered stock bases, Pohang Halmae-jip prepares everything from scratch daily. Each bowl is served with rice, sliced scallions, and their house-made salted shrimp sauce."},
            {"q": "Is Yeongcheon Market worth visiting beyond Pohang Halmae-jip?",
             "a": "Yeongcheon Market is one of Korea's traditional five-day markets (opens on dates ending in 3 and 8) with dozens of food stalls, fresh produce vendors, and local artisan goods. Even on non-market days, the permanent shops and restaurants are active. Combining the market visit with Pohang Halmae-jip makes for an authentic Korean countryside food experience."},
        ]
    },
    29: {
        "title": "Han Hye-jin's Hongcheon Food Trip",
        "faqs": [
            {"q": "Which restaurants did model Han Hye-jin visit on her Hongcheon food trip?",
             "a": "Han Hye-jin's Hongcheon food trip featured three standout spots: a buckwheat noodle restaurant known for handmade memil-guksu, a tofu village serving freshly made dubu with mountain spring water, and a traditional market stall famous for pine nut hotteok (sweet filled pancakes). Each location showcases Gangwon Province's local specialties."},
            {"q": "What is pine nut hotteok and where can I find it in Hongcheon?",
             "a": "Pine nut hotteok is a regional variation of the classic Korean sweet pancake, filled with locally harvested pine nuts, brown sugar, and cinnamon instead of the standard peanut filling. Hongcheon is one of Korea's largest pine nut producing regions, and several market vendors and small shops in the town center offer this specialty, typically priced at 2,000–3,000 KRW each."},
            {"q": "How do I plan a day trip to Hongcheon from Seoul for food tourism?",
             "a": "Take an intercity bus from Seoul's Express Bus Terminal or Dong Seoul Terminal to Hongcheon (approximately 1.5–2 hours, departures every 30 minutes). The food spots are clustered within the town center and surrounding countryside, so renting a car or using local taxis between stops is recommended. A full food tour covering all three featured restaurants takes about 4–5 hours."},
        ]
    },
    40: {
        "title": "Top 10 Must-Try Korean Soups for Winter",
        "faqs": [
            {"q": "What is the most popular Korean soup to eat during winter?",
             "a": "Kimchi-jjigae (kimchi stew) and seolleongtang (ox bone soup) are the two most universally loved Korean winter soups. However, regional specialties like Busan's dwaeji-gukbap (pork soup with rice) and Jeonju's kongnamul-gukbap (bean sprout soup) are equally iconic. Most Korean restaurants serve these soups year-round, but the flavors are especially comforting during the cold months from November through February."},
            {"q": "Are Korean soups suitable for people who cannot eat spicy food?",
             "a": "Several popular Korean soups are completely non-spicy, including seolleongtang (milky ox bone broth), galbitang (short rib soup), samgyetang (ginseng chicken soup), and tteokguk (rice cake soup). When ordering spicy soups, you can request 'deol maepge' (덜 맵게, less spicy) at most restaurants, and some places offer mild versions by default."},
            {"q": "Where can tourists find the best Korean soup restaurants featured on TV shows?",
             "a": "Many TV-featured soup restaurants are located in traditional market areas and residential neighborhoods rather than tourist districts. Using Naver Map and searching the Korean restaurant name is the most reliable method. Popular food TV show locations are also compiled on the Korean app 'Siksin' (식신), which functions like a curated Korean Yelp with TV appearance tags."},
        ]
    },
    46: {
        "title": "Budget Meals in Korea",
        "faqs": [
            {"q": "Is it really possible to eat a full meal in Korea for under $10?",
             "a": "Yes, Korea has an extensive culture of affordable dining. Gukbap (soup with rice) restaurants, kimbap shops, and university district eateries routinely serve filling meals for 5,000–8,000 KRW ($4–6 USD). Traditional market food courts and convenience store meal deals offer even cheaper options starting at 3,000 KRW. The restaurants featured in this guide were all verified as under 10,000 KRW per meal."},
            {"q": "What are the cheapest areas in Korea to find budget restaurants?",
             "a": "University districts (Sinchon, Hongdae, Konkuk) offer the most budget-friendly options due to student demand. Traditional markets like Gwangjang Market, Namdaemun Market, and local five-day markets (오일장) have incredibly affordable stalls. Outside Seoul, smaller cities like Gwangju, Daejeon, and Chuncheon generally have lower restaurant prices than the capital."},
            {"q": "Do budget Korean restaurants accept credit cards or only cash?",
             "a": "Most Korean restaurants, including budget ones, accept credit cards (especially Samsung Pay and local cards). However, very small traditional market stalls and some old-generation restaurants may be cash-only. Carrying 20,000–30,000 KRW in cash as backup is advisable when exploring markets and small neighborhood eateries."},
        ]
    },
    48: {
        "title": "Korean BBQ Etiquette",
        "faqs": [
            {"q": "Who is supposed to grill the meat at a Korean BBQ restaurant?",
             "a": "Traditionally, the youngest person at the table or the host grills the meat as a sign of respect to elders and guests. At many tourist-friendly restaurants, staff will grill for you. If dining with Koreans, offering to handle the grilling is considered polite, but do not insist if someone senior takes over — they may prefer to control the cooking themselves."},
            {"q": "Is it rude to ask for extra side dishes (banchan) at Korean BBQ?",
             "a": "Not at all — requesting banchan refills is completely normal and expected in Korean dining culture. Most banchan including kimchi, pickled radish, lettuce wraps, and ssamjang sauce are free and unlimited. Simply catch a staff member's attention and say 'banchan deo juseyo' (반찬 더 주세요). The only exception is premium sides like egg steamer or cheese, which may cost extra."},
            {"q": "How much should I tip at a Korean BBQ restaurant?",
             "a": "Tipping is not practiced in Korea and can actually make staff uncomfortable. The service charge is included in the menu price. This applies to all restaurants, cafes, and bars throughout the country. If you want to show appreciation, a simple 'jal meogeotsseumnida' (잘 먹었습니다, meaning 'I ate well') when leaving is the culturally appropriate way to express thanks."},
        ]
    },
    80: {
        "title": "Learn Korean Through K-Dramas",
        "faqs": [
            {"q": "Can I actually become conversational in Korean just by watching K-Dramas?",
             "a": "K-Dramas are an excellent supplementary tool but should not be your only study method. They help with listening comprehension, natural pronunciation, and cultural context that textbooks cannot teach. However, K-Drama dialogue often uses informal speech levels and dramatic expressions that may not be appropriate in real-life situations. Combining drama watching with structured grammar study and speaking practice yields the best results."},
            {"q": "What are the best K-Dramas for learning Korean as a beginner?",
             "a": "Slice-of-life dramas with everyday conversations are ideal for beginners. 'Reply 1988' features family dialogue, 'Hometown Cha-Cha-Cha' uses simple small-town language, and 'Weightlifting Fairy Kim Bok-joo' has natural campus conversations. Avoid historical dramas (sageuk) initially, as they use archaic Korean that is not used in modern conversation."},
            {"q": "Should I watch K-Dramas with Korean subtitles or English subtitles when studying?",
             "a": "Use a three-step approach: first watch with English subtitles to understand the story, then rewatch key scenes with Korean subtitles to connect sounds to text, and finally watch without any subtitles to test comprehension. Most streaming platforms like Netflix and Viki offer dual subtitle options. Even 15 minutes of focused subtitle-free watching daily can significantly improve your listening skills over time."},
        ]
    },
    180: {
        "title": "Myeongdong Street Food Map",
        "faqs": [
            {"q": "What are the must-try street foods in Myeongdong for first-time visitors?",
             "a": "The top 5 must-tries are: egg bread (gyeran-ppang, 2,000 KRW), tornado potato on a stick (hoeori-gamja, 4,000 KRW), Korean corn dogs with various coatings (3,000–5,000 KRW), tteokbokki (spicy rice cakes, 4,000 KRW), and fresh strawberry mochi (3,000 KRW). Most stalls are concentrated along the main Myeongdong shopping street between exits 6 and 7 of Myeongdong Station."},
            {"q": "What time should I visit Myeongdong for the best street food experience?",
             "a": "Street food stalls typically open between 11 AM and noon, with peak activity from 3 PM to 9 PM. Weekday afternoons (2–5 PM) offer the best experience with shorter lines and freshly prepared food. Weekend evenings can be extremely crowded, with wait times of 10–15 minutes at popular stalls. Most vendors close by 10 PM."},
            {"q": "How much money should I budget for a Myeongdong street food tour?",
             "a": "A satisfying street food tour sampling 5–7 different items costs approximately 20,000–30,000 KRW ($15–22 USD). Individual items range from 2,000 KRW for simple snacks to 6,000 KRW for premium items like lobster tails or wagyu skewers. Most stalls are cash-preferred, though an increasing number now accept card payments via tap-to-pay terminals."},
        ]
    },
    184: {
        "title": "HYBE Insight Museum & Big 4 Entertainment Tours",
        "faqs": [
            {"q": "Do I need to book HYBE Insight tickets in advance or can I walk in?",
             "a": "Advance booking is mandatory — HYBE Insight does not accept walk-in visitors. Tickets sell out quickly, especially during weekends and school holidays. Book through the official HYBE Insight website or Weverse app at least 2–3 weeks ahead. Tickets are released in batches, and international fans should note that a Korean phone number is not required for booking through the global Weverse platform."},
            {"q": "Can I visit all Big 4 entertainment company buildings in one day?",
             "a": "Yes, a well-planned itinerary can cover HYBE (Yongsan), SM Entertainment (Seongsu), JYP Entertainment (Cheongdam), and YG Entertainment (Hapjeong) in one day. They are all accessible via Seoul's subway system. Allow 2 hours for HYBE Insight's full experience, and 30–45 minutes at each of the other locations for photo opportunities and nearby fan merchandise shops."},
            {"q": "Are there official merchandise shops at the Big 4 entertainment company buildings?",
             "a": "HYBE Insight has the most extensive official merchandise shop with exclusive items only available on-site. SM Entertainment operates a separate KWANGYA store in Seongsu-dong with artist-specific goods. JYP and YG do not have dedicated public retail shops at their headquarters, but nearby Cheongdam and Hapjeong areas have licensed merchandise stores and fan cafes within walking distance."},
        ]
    },
}

def build_faq_jsonld(faqs):
    entities = []
    for faq in faqs:
        entities.append({
            "@type": "Question",
            "name": faq["q"],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": faq["a"]
            }
        })
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": entities
    }
    return '\n<script type="application/ld+json">\n' + json.dumps(schema, indent=2, ensure_ascii=False) + '\n</script>'

def main():
    s, h = login()
    success = 0
    fail = 0

    for pid, data in FAQ_DATA.items():
        # Get current content
        r = s.get(f"{REST}/posts/{pid}", headers=h)
        if r.status_code != 200:
            print(f"  FAIL fetch ID:{pid} - {r.status_code}")
            fail += 1
            continue

        post = r.json()
        content = post["content"]["rendered"]

        # Skip if already has FAQ schema
        if "FAQPage" in content:
            print(f"  SKIP ID:{pid} - already has FAQ schema")
            continue

        # Append FAQ JSON-LD to content
        faq_html = build_faq_jsonld(data["faqs"])
        new_content = content + faq_html

        # Update post
        r = s.post(f"{REST}/posts/{pid}", headers=h, json={"content": new_content})
        if r.status_code == 200:
            print(f"  OK   ID:{pid} - {data['title']}")
            success += 1
        else:
            print(f"  FAIL ID:{pid} - {r.status_code}: {r.text[:100]}")
            fail += 1

    print(f"\nDone: {success} updated, {fail} failed")

if __name__ == "__main__":
    main()
