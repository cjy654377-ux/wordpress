import requests
import re
import json
import os

SITE = "https://rhythmicaleskimo.com"
REST = f"{SITE}/wp-json/wp/v2"

# === Login ===
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
    m = re.search(r'_wpnonce":"([a-f0-9]+)"', page)
if not m:
    print("ERROR: Could not find nonce")
    exit(1)
nonce = m.group(1)
h = {"X-WP-Nonce": nonce}
print(f"Nonce: {nonce}")

# === Find K-Drama category ===
cats = s.get(f"{REST}/categories", params={"per_page": 100}, headers=h).json()
kdrama_id = None
for c in cats:
    if "drama" in c["name"].lower():
        kdrama_id = c["id"]
        print(f"K-Drama category: {c['name']} (ID: {kdrama_id})")
        break
if not kdrama_id:
    print("K-Drama category not found, using default")
    kdrama_id = 1

# === Upload featured image ===
img_path = "/Users/choijooyong/wordpress/featured_love_translated.png"
with open(img_path, "rb") as f:
    img_data = f.read()

media_resp = s.post(f"{REST}/media", headers={
    **h,
    "Content-Disposition": "attachment; filename=featured-love-translated.png",
    "Content-Type": "image/png"
}, data=img_data)
print(f"Media upload: {media_resp.status_code}")
media_id = media_resp.json().get("id")
print(f"Media ID: {media_id}")

# === Article HTML ===
article_html = """
<p>When Netflix announced a romantic comedy starring <strong>Kim Seon-ho</strong> and <strong>Go Youn-jung</strong>, written by the legendary Hong sisters, K-drama fans around the world collectively held their breath. <em>Can This Love Be Translated?</em> (이 사랑 통역 되나요?) premiered on January 16, 2026, and within days it had climbed to the top of Netflix charts across Asia.</p>

<p>But does it live up to the hype? This complete guide covers every detail you need: the full cast breakdown, episode-by-episode plot analysis, filming locations spanning four countries, streaming information, and our honest review of what works and what stumbles along the way.</p>

<h2>Quick Overview: Everything You Need to Know</h2>

<div style="overflow-x:auto;">
<table>
<thead><tr><th>Detail</th><th>Information</th></tr></thead>
<tbody>
<tr><td><strong>Korean Title</strong></td><td>이 사랑 통역 되나요?</td></tr>
<tr><td><strong>Genre</strong></td><td>Romantic Comedy, Drama, Supernatural</td></tr>
<tr><td><strong>Episodes</strong></td><td>12 (approx. 66 min each)</td></tr>
<tr><td><strong>Release Date</strong></td><td>January 16, 2026</td></tr>
<tr><td><strong>Network</strong></td><td>Netflix (worldwide simultaneous release)</td></tr>
<tr><td><strong>Director</strong></td><td>Yoo Young-eun</td></tr>
<tr><td><strong>Writers</strong></td><td>Hong Jung-eun &amp; Hong Mi-ran (Hong Sisters)</td></tr>
<tr><td><strong>IMDb Rating</strong></td><td>7.9/10</td></tr>
<tr><td><strong>MyDramaList Score</strong></td><td>8.4/10 (32,000+ ratings)</td></tr>
<tr><td><strong>Filming Locations</strong></td><td>South Korea, Japan, Canada, Italy</td></tr>
</tbody>
</table>
</div>

<p>The drama ranked first globally on Netflix in multiple countries including South Korea, Indonesia, Malaysia, the Philippines, Singapore, Taiwan, Thailand, and Vietnam. For three consecutive weeks, it held the number one spot in the integrated TV-OTT drama category in Korea.</p>

<h2>Complete Cast Guide: Who Plays Whom</h2>

<h3>Kim Seon-ho as Joo Ho-jin</h3>

<p><strong>Kim Seon-ho</strong> plays Joo Ho-jin, a genius polyglot interpreter who speaks eight languages fluently. Ho-jin is brilliant with words but emotionally guarded. He lives by logic, keeping romance at arm's length, preferring the predictable structure of language over the chaos of human emotion.</p>

<p>Kim Seon-ho is best known for his breakout role as Hong Du-sik in <em>Hometown Cha-Cha-Cha</em> (2021), which earned him the Gallup Korea Television Actor of the Year title. He also starred as Han Ji-pyeong in <em>Start-Up</em> (2020) and made his film debut in the action thriller <em>The Childe</em> (2023), winning multiple Best New Actor awards.</p>

<p>In <em>Can This Love Be Translated?</em>, Kim delivers a performance that feels like a natural evolution of his rom-com charm. His portrayal of a man who can decode every language except the language of love is both endearing and layered with vulnerability. The role demands a subtlety that Kim handles masterfully, particularly in scenes where Ho-jin's emotional walls begin to crack.</p>

<h3>Go Youn-jung as Cha Mu-hee</h3>

<p><strong>Go Youn-jung</strong> plays Cha Mu-hee, an actress whose career skyrocketed after her breakout role as Do Ra-mi in a hit zombie film. Mu-hee is vibrant, unpredictable, and carrying deep emotional scars beneath her confident exterior.</p>

<p>Go Youn-jung rose to prominence through <em>Alchemy of Souls Part 2</em> (2022-2023), where she played the dual role of Jin Bu-yeon and Nak-su. She has since appeared in <em>Sweet Home</em> (2020), <em>Moving</em> (2023), and <em>Resident Playbook</em> (2025). Her performance in <em>Can This Love Be Translated?</em> showcases her impressive range, shifting between comedy, vulnerability, and the eerie intensity of her alter ego.</p>

<p>The chemistry between Kim and Go is undeniable. Their push-and-pull dynamic fuels the emotional core of the series, and fans have praised their natural on-screen connection as one of the best pairings in recent K-drama history.</p>

<h3>Sota Fukushi as Hiro Kurosawa</h3>

<p>Japanese actor <strong>Sota Fukushi</strong> plays Hiro Kurosawa, Mu-hee's co-star on the reality dating show <em>Romantic Trip</em>. Hiro was once a beloved Japanese actor whose star has faded, and he joins the show hoping to revive his career. He speaks no Korean, which creates a central tension: every interaction between Hiro and Mu-hee must pass through Ho-jin's interpretation.</p>

<p>This dynamic creates a fascinating love triangle where the interpreter literally controls the emotional flow between two people who cannot communicate directly. The question of whether translation can ever truly capture feeling becomes the show's central metaphor.</p>

<h3>Supporting Cast</h3>

<div style="overflow-x:auto;">
<table>
<thead><tr><th>Actor</th><th>Character</th><th>Role</th></tr></thead>
<tbody>
<tr><td><strong>Choi Woo-sung</strong></td><td>Kim Yong-woo</td><td>Mu-hee's loyal manager who gave up a sports career after injury. Her closest confidant and protector.</td></tr>
<tr><td><strong>Lee Yi-dam</strong></td><td>Shin Ji-seon</td><td>The sharp, ambitious producer who runs the <em>Romantic Trip</em> reality show.</td></tr>
<tr><td><strong>Kim Won-hae</strong></td><td>Kim Yeong-hwan</td><td>A novelist whose words provide philosophical depth to the storyline.</td></tr>
<tr><td><strong>Hyunri</strong></td><td>Nanami</td><td>Hiro's Japanese manager who navigates the cross-cultural tensions behind the scenes.</td></tr>
<tr><td><strong>Baek Joo-hee</strong></td><td>Writer Cho</td><td>The reality show's writer who orchestrates romantic scenarios.</td></tr>
<tr><td><strong>Im Chul-soo</strong></td><td>Kim Jeong-su</td><td>A PD on the reality show production team.</td></tr>
</tbody>
</table>
</div>

<h2>Plot Breakdown: What Is the Drama Actually About?</h2>

<h3>The Premise</h3>

<p>Joo Ho-jin first meets Cha Mu-hee in Japan, back when she is still a struggling unknown actress. Years later, Mu-hee has become a global superstar after her zombie film role, and they are reunited when Ho-jin is hired as her interpreter for an international press tour.</p>

<p>The two cross paths again on <em>Romantic Trip</em>, a reality show that pairs two actors who share no common language, one Korean and one Japanese, and sends them to romantic destinations around the world. The twist? Every word between them must be translated in real time by Ho-jin. As interpreter, he is supposed to be invisible, a neutral conduit. But when feelings start bleeding through the translations, neutrality becomes impossible.</p>

<h3>The Supernatural Twist: Do Ra-mi</h3>

<p>Here is where the Hong sisters inject their signature genre-blending magic. Mu-hee's deepest insecurities manifest as <strong>Do Ra-mi</strong>, the zombie character she played in her breakout film. Do Ra-mi appears as a psychological projection, a vengeful inner voice that surfaces whenever Mu-hee feels emotionally exposed.</p>

<p>Do Ra-mi whispers every catastrophic possibility, every reason love will fail, every justification for pushing people away before they can abandon her first. As the series progresses, this alter ego grows stronger, eventually taking over Mu-hee's consciousness in moments of extreme vulnerability.</p>

<p>The supernatural element is ambitious. It transforms what could have been a straightforward rom-com into something more psychologically complex. Whether it fully succeeds is debatable, but it gives Go Youn-jung extraordinary material to work with, and she delivers.</p>

<h3>The Ending (Spoiler Warning)</h3>

<p>The final episode delivers a major revelation: Do Ra-mi was never truly an alter ego born from career anxiety. She was a manifestation of Mu-hee's <strong>mother</strong>, who spent years telling her daughter she would never be happy or truly loved. The inner saboteur traces back to childhood trauma, not Hollywood pressure.</p>

<p>Once Mu-hee confronts this truth, Do Ra-mi disappears completely. The series ends with Ho-jin and Mu-hee together, sharing a kiss under the stars at an observatory. Mu-hee also makes peace with Hiro, apologizing for the confusion her Do Ra-mi persona caused in their interactions on the show.</p>

<h2>Filming Locations: A Four-Country Love Story</h2>

<p>One of the most visually stunning aspects of <em>Can This Love Be Translated?</em> is its globe-trotting production. The series filmed across four countries, creating a travelogue quality that enriches every episode.</p>

<h3>Japan</h3>

<p>The early episodes were filmed in <strong>Kamakura</strong> and <strong>Enoshima</strong>, capturing the nostalgic seaside charm of Japan's coastal towns. Key locations include Gokurakuji Station, Goryo Shrine, Kamakura Seaside Park, and the Grand Torii of Enoshima Shrine. Filming took place from June 24 to July 10, with additional scenes at Tenzan Lab and Katase Fishing Port.</p>

<p>These Japanese sequences feel deliberately reminiscent of classic anime romance settings, and the cinematography emphasizes golden-hour lighting and ocean views that will make viewers want to book flights immediately.</p>

<h3>South Korea</h3>

<p>The Korean segments span multiple regions. Seoul locations include Gamgodang-gil, the Peninsula Lounge at the Lotte Hotel, Raum Art Center, and the trendy Seongsu-dong area. Outside Seoul, filming took place at Sanmeoru Farm in Paju, Hwiwoo Cafe in Goyang, Pinodia Expo Tower in Sokcho, and the Buyeo National Museum.</p>

<p>If you are planning a trip to Korea, our <a href="/seouls-hidden-alley-restaurants-7-places-only-locals-know-about/">guide to Seoul's hidden alley restaurants</a> covers some neighborhoods featured in the drama.</p>

<h3>Canada (Alberta)</h3>

<p>The production team, operating under the name Sailor Films Inc. with a crew of 150, filmed in Alberta from September 23 to October 11, 2024. The Canadian landscapes provide a striking visual contrast to the Asian settings, with wide-open spaces and rugged mountain scenery serving as the backdrop for some of the drama's most emotionally pivotal scenes.</p>

<h3>Italy (Tuscany)</h3>

<p>The final leg of filming took place in Tuscany from November 23 to December 9. Locations include <strong>Siena</strong>, <strong>Montalcino</strong>, and <strong>Florence</strong>. The Italian sequences serve as the romantic climax of the series, with Renaissance architecture and rolling vineyard hills creating a fairy-tale atmosphere that perfectly complements the love story's resolution.</p>

<h2>Where to Watch and Subscription Options</h2>

<div style="overflow-x:auto;">
<table>
<thead><tr><th>Plan</th><th>Monthly Price (US)</th><th>Quality</th><th>Simultaneous Streams</th></tr></thead>
<tbody>
<tr><td>Standard with Ads</td><td>$7.99</td><td>1080p</td><td>2</td></tr>
<tr><td>Standard</td><td>$17.99</td><td>1080p</td><td>2</td></tr>
<tr><td>Premium</td><td>$24.99</td><td>4K + HDR</td><td>4</td></tr>
</tbody>
</table>
</div>

<p><em>Can This Love Be Translated?</em> is a <strong>Netflix exclusive</strong>, available worldwide since January 16, 2026. All 12 episodes were released simultaneously. The series is available with subtitles in over 30 languages and dubbed in several languages including English, Japanese, and Spanish.</p>

<p>For the best viewing experience, we recommend the Premium plan for 4K quality, as the drama's international cinematography truly shines in high resolution.</p>

<h2>Honest Review: What Works and What Doesn't</h2>

<h3>Strengths</h3>

<p><strong>The leads' chemistry is electric.</strong> Kim Seon-ho and Go Youn-jung are magnetic together. Their bickering-to-longing arc is paced beautifully across 12 episodes, with enough tension to keep viewers hooked without feeling artificially drawn out.</p>

<p><strong>The language-as-metaphor concept is brilliant.</strong> The idea that an interpreter controls the emotional flow between two people who cannot communicate directly is fresh and compelling. Every mistranslation, every added nuance, every omitted word carries weight. It is a clever way to explore how much of love is about what we say versus what we mean.</p>

<p><strong>The production value is outstanding.</strong> Filming across Japan, Korea, Canada, and Italy gives the series a cinematic quality rare in K-dramas. Each location feels intentional, not just as a backdrop but as an emotional landscape that mirrors the characters' internal journeys.</p>

<p><strong>The Hong sisters' dialogue sparkles.</strong> The writing team behind <em>My Girl</em>, <em>Hotel del Luna</em>, and <em>The Master's Sun</em> delivers witty, quotable dialogue that balances humor with emotional depth.</p>

<h3>Weaknesses</h3>

<p><strong>The Do Ra-mi subplot is uneven.</strong> While ambitious, the supernatural/psychological element feels clumsy at times. The transition from a metaphorical inner voice to a full alter ego that takes over Mu-hee's consciousness is jarring. Several critics noted that the horror elements do not always mesh smoothly with the rom-com tone.</p>

<p><strong>The ending explanation feels rushed.</strong> Revealing that Do Ra-mi represents Mu-hee's mother rather than career anxiety is a significant twist, but it arrives late and resolves too quickly. A theme this heavy deserves more breathing room than a single episode can provide.</p>

<p><strong>Hiro's arc deserves more depth.</strong> Sota Fukushi is charming as Hiro, but his character sometimes feels like a plot device rather than a fully realized person. The resolution of his feelings for Mu-hee, while handled with grace, could have been explored more thoroughly.</p>

<h3>Overall Verdict</h3>

<p>Despite its stumbles with the supernatural subplot, <em>Can This Love Be Translated?</em> is one of the strongest K-drama rom-coms of early 2026. The central metaphor is fresh, the leads are captivating, and the production quality sets a new standard. If you enjoyed <a href="/boyfriend-on-demand-jisoos-netflix-k-drama-complete-guide-cast-review-/">Boyfriend on Demand</a> or <a href="/when-life-gives-you-tangerines-cast-guide-iu-park-bo-gum-the-real-marr/">When Life Gives You Tangerines</a>, this belongs on your watchlist.</p>

<p><strong>Our Rating: 8.2/10</strong></p>

<h2>How It Compares to Other 2026 K-Dramas</h2>

<p>2026 has been a remarkable year for K-dramas already, and <em>Can This Love Be Translated?</em> holds its own against strong competition.</p>

<div style="overflow-x:auto;">
<table>
<thead><tr><th>Drama</th><th>Genre</th><th>IMDb</th><th>MDL</th><th>Highlight</th></tr></thead>
<tbody>
<tr><td><strong>Can This Love Be Translated?</strong></td><td>Rom-Com</td><td>7.9</td><td>8.4</td><td>Language-as-love metaphor, globe-trotting visuals</td></tr>
<tr><td><strong>Boyfriend on Demand</strong></td><td>Rom-Com</td><td>7.8</td><td>8.2</td><td>Jisoo's acting debut, subscription romance concept</td></tr>
<tr><td><strong>When Life Gives You Tangerines</strong></td><td>Period Romance</td><td>8.3</td><td>8.7</td><td>IU + Park Bo-gum, Jeju Island setting</td></tr>
<tr><td><strong>Siren's Kiss</strong></td><td>Fantasy Romance</td><td>7.6</td><td>8.0</td><td>Mermaid mythology meets modern Seoul</td></tr>
<tr><td><strong>Climax</strong></td><td>Thriller</td><td>8.1</td><td>8.5</td><td>Most talked-about show this spring</td></tr>
</tbody>
</table>
</div>

<p>Compared to the emotional gravity of <em>When Life Gives You Tangerines</em> or the genre thrills of <a href="/climax-%ED%81%B4%EB%9D%BC%EC%9D%B4%EB%A7%89%EC%8A%A4-k-drama-review-2026-cast-plot-why-its-the-most-talked-about-show-this-spring/">Climax</a>, this drama carves out its own niche: a smart, visually gorgeous rom-com that takes genuine risks with its storytelling. It doesn't always nail the landing, but it swings for the fences in ways that most rom-coms don't dare to try.</p>

<h2>5 Reasons to Watch Can This Love Be Translated</h2>

<ol>
<li><strong>Fresh Concept</strong> &mdash; The interpreter-as-love-conduit idea has never been done quite like this. It adds layers of tension and meaning to every conversation.</li>
<li><strong>Stunning Visuals</strong> &mdash; Four countries, world-class cinematography, and each location feels like a character in the story.</li>
<li><strong>Top-Tier Cast</strong> &mdash; Kim Seon-ho at his most charming, Go Youn-jung at her most versatile, and a scene-stealing turn by Sota Fukushi.</li>
<li><strong>Hong Sisters Writing</strong> &mdash; The duo behind some of the most beloved K-dramas delivers sharp, emotionally resonant dialogue with their trademark genre twists.</li>
<li><strong>Binge-Friendly</strong> &mdash; All 12 episodes drop at once on Netflix, and at roughly 66 minutes each, it's a satisfying weekend binge.</li>
</ol>

<p>For more romantic K-drama recommendations, check our guide to <a href="/5-must-watch-k-dramas-before-boyfriend-on-demand-premieres-on-netflix/">5 must-watch K-dramas</a> that pair well with this series.</p>

<h2>Korean Vocabulary From the Drama</h2>

<p>If you are <a href="/learn-korean-through-k-dramas-30-essential-phrases-youll-actually-use/">learning Korean through K-dramas</a>, <em>Can This Love Be Translated?</em> is packed with useful vocabulary related to language, translation, and emotions.</p>

<div style="overflow-x:auto;">
<table>
<thead><tr><th>Korean</th><th>Romanization</th><th>Meaning</th><th>Context in Drama</th></tr></thead>
<tbody>
<tr><td>통역사</td><td>tong-yeok-sa</td><td>Interpreter</td><td>Ho-jin's profession</td></tr>
<tr><td>번역</td><td>beon-yeok</td><td>Translation</td><td>Central theme of the show</td></tr>
<tr><td>사랑해</td><td>saranghae</td><td>I love you</td><td>The words Ho-jin struggles to say</td></tr>
<tr><td>오해</td><td>o-hae</td><td>Misunderstanding</td><td>Frequent between Mu-hee and Hiro</td></tr>
<tr><td>진심</td><td>jin-sim</td><td>Sincerity / True feelings</td><td>What Ho-jin eventually reveals</td></tr>
<tr><td>고백</td><td>go-baek</td><td>Confession (of love)</td><td>The climactic moment viewers wait for</td></tr>
<tr><td>촬영지</td><td>chwal-yeong-ji</td><td>Filming location</td><td>The global destinations in the show</td></tr>
<tr><td>대본</td><td>dae-bon</td><td>Script</td><td>Referenced in the reality show segments</td></tr>
</tbody>
</table>
</div>

<h2>Frequently Asked Questions</h2>

<h3>How many episodes does Can This Love Be Translated have?</h3>
<p>The drama has <strong>12 episodes</strong>, each running approximately 66 minutes. All episodes were released simultaneously on Netflix on January 16, 2026.</p>

<h3>Is Can This Love Be Translated based on a webtoon or novel?</h3>
<p>No. <em>Can This Love Be Translated?</em> is an <strong>original screenplay</strong> written by the Hong sisters (Hong Jung-eun and Hong Mi-ran). It is not based on any existing webtoon, novel, or source material.</p>

<h3>Where can I watch Can This Love Be Translated?</h3>
<p>The drama is a <strong>Netflix exclusive</strong> available worldwide. You need an active Netflix subscription (plans start at $7.99/month with ads in the US). It is available with subtitles in over 30 languages.</p>

<h3>Who are the Hong sisters?</h3>
<p>Hong Jung-eun and Hong Mi-ran are a sibling screenwriting duo known for genre-blending K-dramas including <em>My Girl</em> (2005), <em>You're Beautiful</em> (2009), <em>The Master's Sun</em> (2013), <em>Hotel del Luna</em> (2019), and now <em>Can This Love Be Translated?</em> (2026). They are famous for mixing romance with supernatural or fantasy elements.</p>

<h3>Does the drama have a happy ending?</h3>
<p>Yes. Without giving away too many details, <strong>Ho-jin and Mu-hee end up together</strong>. The final episode resolves the main romantic conflict and provides emotional closure for all major characters, including Hiro.</p>

<h3>Is there a season 2 planned?</h3>
<p>As of March 2026, Netflix has not announced a second season. The series tells a complete story across 12 episodes and was marketed as a limited series. However, given its massive viewership numbers, a follow-up project with the same creative team is not impossible.</p>

<h2>You Might Also Enjoy</h2>

<ul>
<li><a href="/sirens-kiss-complete-guide-cast-plot-episodes-where-to-watch-2026/">Siren's Kiss: Complete Guide &mdash; Cast, Plot, Episodes &amp; Where to Watch (2026)</a></li>
<li><a href="/boyfriend-on-demand-jisoos-netflix-k-drama-complete-guide-cast-review-/">Boyfriend on Demand: Jisoo's Netflix K-Drama Complete Guide</a></li>
<li><a href="/climax-%ED%81%B4%EB%9D%BC%EC%9D%B4%EB%A7%89%EC%8A%A4-k-drama-review-2026-cast-plot-why-its-the-most-talked-about-show-this-spring/">Climax K-Drama Review 2026: Why It's the Most Talked-About Show This Spring</a></li>
</ul>

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "How many episodes does Can This Love Be Translated have?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "The drama has 12 episodes, each running approximately 66 minutes. All episodes were released simultaneously on Netflix on January 16, 2026."
      }
    },
    {
      "@type": "Question",
      "name": "Is Can This Love Be Translated based on a webtoon or novel?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "No. Can This Love Be Translated? is an original screenplay written by the Hong sisters (Hong Jung-eun and Hong Mi-ran). It is not based on any existing webtoon, novel, or source material."
      }
    },
    {
      "@type": "Question",
      "name": "Where can I watch Can This Love Be Translated?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "The drama is a Netflix exclusive available worldwide. You need an active Netflix subscription (plans start at $7.99/month with ads in the US). It is available with subtitles in over 30 languages."
      }
    },
    {
      "@type": "Question",
      "name": "Who are the Hong sisters?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Hong Jung-eun and Hong Mi-ran are a sibling screenwriting duo known for genre-blending K-dramas including My Girl (2005), You're Beautiful (2009), The Master's Sun (2013), Hotel del Luna (2019), and Can This Love Be Translated? (2026)."
      }
    },
    {
      "@type": "Question",
      "name": "Does the drama have a happy ending?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes. Ho-jin and Mu-hee end up together. The final episode resolves the main romantic conflict and provides emotional closure for all major characters."
      }
    },
    {
      "@type": "Question",
      "name": "Is there a season 2 planned?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "As of March 2026, Netflix has not announced a second season. The series tells a complete story across 12 episodes and was marketed as a limited series."
      }
    }
  ]
}
</script>
"""

# === Publish ===
post_data = {
    "title": "Can This Love Be Translated? K-Drama Review [2026]",
    "content": article_html.strip(),
    "status": "publish",
    "categories": [kdrama_id],
    "tags": [],
    "excerpt": "Complete guide to Netflix's Can This Love Be Translated? starring Kim Seon-ho and Go Youn-jung. Cast profiles, plot analysis, filming locations, streaming info, and honest review.",
    "featured_media": media_id if media_id else 0
}

# Create/find tags
tag_names = [
    "Can This Love Be Translated",
    "Kim Seon-ho",
    "Go Youn-jung",
    "Netflix K-Drama",
    "K-Drama 2026",
    "Hong Sisters",
    "Korean Drama Review",
    "Sota Fukushi"
]

tag_ids = []
for tag_name in tag_names:
    # Try to find existing tag
    existing = s.get(f"{REST}/tags", params={"search": tag_name}, headers=h).json()
    found = False
    for t in existing:
        if t["name"].lower() == tag_name.lower():
            tag_ids.append(t["id"])
            found = True
            break
    if not found:
        # Create new tag
        resp = s.post(f"{REST}/tags", headers=h, json={"name": tag_name})
        if resp.status_code in [200, 201]:
            tag_ids.append(resp.json()["id"])
            print(f"Created tag: {tag_name}")
        else:
            print(f"Failed to create tag: {tag_name} - {resp.status_code}")

post_data["tags"] = tag_ids
print(f"Tags: {tag_ids}")

resp = s.post(f"{REST}/posts", headers=h, json=post_data)
print(f"Publish status: {resp.status_code}")

if resp.status_code in [200, 201]:
    result = resp.json()
    post_id = result["id"]
    post_url = result["link"]
    print(f"\n=== SUCCESS ===")
    print(f"Post ID: {post_id}")
    print(f"URL: {post_url}")
    print(f"Title: {result['title']['rendered']}")
else:
    print(f"Error: {resp.text[:500]}")
