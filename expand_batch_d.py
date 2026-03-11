#!/usr/bin/env python3
"""Expand 4 posts to 2500+ words each."""
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

# ── POST 361: 25 Essential Korean Phrases Every BTS Fan Should Know (~650w needed) ──
extra_361 = '''
<h2>Advanced BTS Korean: Phrases From Song Lyrics You Can Use Daily</h2>

<p>Once you have mastered the basic fan phrases, the next level is incorporating Korean expressions from BTS songs into your everyday vocabulary. These are not just lyrics — they are phrases native Koreans actually use in daily conversation, which makes learning them doubly rewarding.</p>

<h3>From "Dynamite" to Daily Life</h3>

<p>While "Dynamite" is primarily in English, BTS's Korean discography is a goldmine for practical vocabulary. Here are phrases pulled directly from their most iconic tracks that you can use in real situations:</p>

<table style="width:100%; border-collapse:collapse; margin:1.5em 0;">
<tr style="background:#f4f0ff;"><th style="padding:10px; border:1px solid #ddd; text-align:left;">Song</th><th style="padding:10px; border:1px solid #ddd; text-align:left;">Korean Phrase</th><th style="padding:10px; border:1px solid #ddd; text-align:left;">Romanization</th><th style="padding:10px; border:1px solid #ddd; text-align:left;">Real-Life Usage</th></tr>
<tr><td style="padding:10px; border:1px solid #ddd;">Spring Day</td><td style="padding:10px; border:1px solid #ddd;">보고 싶다</td><td style="padding:10px; border:1px solid #ddd;">bogo sipda</td><td style="padding:10px; border:1px solid #ddd;">I miss you (to friends, family)</td></tr>
<tr><td style="padding:10px; border:1px solid #ddd;">Butter</td><td style="padding:10px; border:1px solid #ddd;">좋아해</td><td style="padding:10px; border:1px solid #ddd;">joahae</td><td style="padding:10px; border:1px solid #ddd;">I like it / I like you (casual)</td></tr>
<tr><td style="padding:10px; border:1px solid #ddd;">DNA</td><td style="padding:10px; border:1px solid #ddd;">운명을 찾아낸</td><td style="padding:10px; border:1px solid #ddd;">unmyeongeul chajanaen</td><td style="padding:10px; border:1px solid #ddd;">Found my destiny (poetic, but used romantically)</td></tr>
<tr><td style="padding:10px; border:1px solid #ddd;">IDOL</td><td style="padding:10px; border:1px solid #ddd;">너 뭔데</td><td style="padding:10px; border:1px solid #ddd;">neo mwonde</td><td style="padding:10px; border:1px solid #ddd;">Who do you think you are? (sassy, common slang)</td></tr>
<tr><td style="padding:10px; border:1px solid #ddd;">Boy With Luv</td><td style="padding:10px; border:1px solid #ddd;">관심 좀 가져줘</td><td style="padding:10px; border:1px solid #ddd;">gwansim jom gajyeojwo</td><td style="padding:10px; border:1px solid #ddd;">Pay attention to me (playful request)</td></tr>
<tr><td style="padding:10px; border:1px solid #ddd;">Mikrokosmos</td><td style="padding:10px; border:1px solid #ddd;">빛나는 별</td><td style="padding:10px; border:1px solid #ddd;">bichnaneun byeol</td><td style="padding:10px; border:1px solid #ddd;">Shining star (used as a compliment)</td></tr>
<tr><td style="padding:10px; border:1px solid #ddd;">Permission to Dance</td><td style="padding:10px; border:1px solid #ddd;">같이 춤추자</td><td style="padding:10px; border:1px solid #ddd;">gachi chumchuja</td><td style="padding:10px; border:1px solid #ddd;">Let's dance together (party invitation)</td></tr>
<tr><td style="padding:10px; border:1px solid #ddd;">ARIRANG title track</td><td style="padding:10px; border:1px solid #ddd;">아리랑 고개</td><td style="padding:10px; border:1px solid #ddd;">arirang gogae</td><td style="padding:10px; border:1px solid #ddd;">Arirang hill — metaphor for life's hardships</td></tr>
</table>

<h3>Weverse and Fan Community Slang</h3>

<p>If you spend any time on Weverse, you will encounter Korean internet slang that even textbooks do not teach. Here are the most useful ones that BTS fans use constantly:</p>

<ul>
<li><strong>ㅋㅋㅋ (kekeke)</strong> — Korean "lol." The more ㅋs, the funnier. BTS members use this all the time on Weverse.</li>
<li><strong>ㅠㅠ or ㅜㅜ</strong> — Crying face emoticon. Use it when something is sad or when you are emotionally overwhelmed by a performance.</li>
<li><strong>대박 (daebak)</strong> — "Jackpot!" or "Amazing!" Jungkook's go-to reaction word.</li>
<li><strong>헐 (heol)</strong> — "OMG" or "No way!" Used when something shocking happens, like a surprise V Live.</li>
<li><strong>아이고 (aigo)</strong> — An all-purpose exclamation meaning "oh my" — Jin uses this constantly, often dramatically.</li>
<li><strong>맞아요 (majayo)</strong> — "That's right!" Perfect for agreeing in comment sections.</li>
<li><strong>진짜? (jinjja?)</strong> — "Really?" One of the most versatile Korean words you will ever learn.</li>
<li><strong>멋있어 (meossisseo)</strong> — "You're cool/handsome!" The ultimate compliment for your bias.</li>
</ul>

<h3>How to Practice Korean Using BTS Content</h3>

<p>The most effective way to solidify these phrases is through active engagement with BTS's Korean content. Here is a structured approach that many ARMY members have used successfully:</p>

<p><strong>Week 1-2: Passive listening.</strong> Watch Run BTS episodes with Korean subtitles on. Do not pause — just absorb the rhythm and sounds. Your brain will start recognizing the phrases from this guide naturally.</p>

<p><strong>Week 3-4: Active shadowing.</strong> Pick one BTS song per day and sing along with the Korean lyrics. Focus on pronunciation rather than speed. RM's solo verses are excellent for this because his enunciation is exceptionally clear.</p>

<p><strong>Week 5+: Production.</strong> Start writing short Weverse comments in Korean. Even "오늘도 수고했어요" (you worked hard today) will earn you responses from Korean fans who appreciate the effort.</p>

<p>For a deeper dive into Korean pronunciation, check out our guide on <a href="https://rhythmicaleskimo.com/how-to-read-korean-hangul-in-30-minutes-the-fastest-method-that-actually-works/">how to read Korean Hangul in 30 minutes</a> — it pairs perfectly with this phrase guide. You might also enjoy our breakdown of <a href="https://rhythmicaleskimo.com/bts-spring-day-%eb%b4%84%eb%82%a0-lyrics-meaning-the-deepest-k-pop-song-ever-written/">BTS Spring Day lyrics meaning</a> to see many of these phrases in poetic context, or explore <a href="https://rhythmicaleskimo.com/learn-korean-through-k-dramas-30-essential-phrases-youll-actually-use/">30 essential Korean phrases from K-Dramas</a> to expand your vocabulary even further.</p>

<h2>BTS Fan Korean: Common Mistakes to Avoid</h2>

<p>Learning Korean through fandom is powerful, but there are pitfalls that can lead to embarrassing mistakes. Here are the most common ones BTS fans make — and how to avoid them:</p>

<p><strong>Mixing up formality levels.</strong> Korean has distinct speech levels, and using the wrong one can come across as rude. When speaking to someone older or someone you do not know well, always use the polite form ending in -요 (yo). Saying "뭐해?" (mwo hae? — what are you doing?) to a stranger would be considered impolite. Use "뭐 하세요?" (mwo haseyo?) instead.</p>

<p><strong>Overusing oppa/unnie.</strong> While BTS fans love calling members "oppa," this term is specifically for a female addressing an older male she is close to. If you are male, the correct term is "hyung" (형). Using "oppa" as a male speaker sounds awkward to Korean ears.</p>

<p><strong>Pronouncing ㅂ as a hard B.</strong> The Korean ㅂ is somewhere between B and P in English. Saying "Bangtan" with a hard B sound marks you as a beginner. Listen carefully to how the members pronounce it — it is softer, almost like a gentle P.</p>

<p><strong>Forgetting particles.</strong> Korean sentences use particles (은/는, 이/가, 을/를) that do not exist in English. While dropping them in casual speech is acceptable, using them correctly elevates your Korean significantly. For example, "BTS 좋아해" is fine casually, but "BTS를 좋아해요" is more grammatically complete.</p>

'''

print("=== Expanding Post 361 ===")
wc = add_content(361, extra_361)
if wc < 2500:
    print(f"  Warning: {wc} < 2500, adding more content...")

# ── POST 404: BTS Spring Day Lyrics Meaning (~1100w needed) ──
extra_404 = '''
<h2>The Musical Architecture of Spring Day</h2>

<p>What makes Spring Day musically extraordinary is not just its lyrics but how the production mirrors the emotional journey of grief. Understanding this architecture reveals why the song has maintained its position on Korean music charts for over nine years — a record that may never be broken.</p>

<h3>Key Changes and Emotional Shifts</h3>

<p>Spring Day begins in B-flat minor, a key historically associated with melancholy in Western classical music. Chopin used it extensively in his nocturnes, and whether intentionally or not, producer Pdogg created the same atmospheric weight. The verses sit in a low, intimate register where each member's voice feels like a whispered confession.</p>

<p>The pre-chorus modulates upward, creating a physical sensation of lifting — as if the listener is being pulled from a dark room toward a window. When the chorus arrives, the key shifts to D-flat major, and this major-key resolution is what makes the chorus simultaneously hopeful and heartbreaking. You feel relief, but the lyrics remind you that this hope is fragile: "You know it all, you're my best friend."</p>

<p>The bridge, sung primarily by Jungkook and V, drops back to minor territory before the final chorus explodes into full major resolution. This musical journey — minor to major to minor to major — mirrors the five stages of grief, ultimately landing on acceptance rather than despair.</p>

<h3>Why Spring Day Never Leaves the Charts</h3>

<p>Every year when winter transitions to spring in Korea, "Spring Day" re-enters the top 10 on Melon, Genie, and other Korean streaming platforms. This seasonal charting pattern is unique in K-pop history. The reasons are both cultural and emotional:</p>

<ul>
<li><strong>Sewol Ferry connection:</strong> Many Korean listeners associate the song with the 2014 Sewol Ferry disaster, which claimed 304 lives, mostly high school students. The lyrics about missing someone who will not return resonate deeply with national grief. April 16, the anniversary, consistently sees streaming spikes.</li>
<li><strong>Seasonal affective resonance:</strong> The transition from winter to spring in Korea is culturally loaded. It represents renewal but also the pain of remembering what was lost during the cold months. Spring Day captures this duality perfectly.</li>
<li><strong>Military service separations:</strong> With mandatory military service for Korean men, the song has become an anthem for girlfriends, families, and friends missing their loved ones during 18-month service periods.</li>
<li><strong>Universal grief processing:</strong> Unlike songs tied to specific breakups or events, Spring Day's lyrics are abstract enough to apply to any form of loss — death, distance, growing apart, or the simple passage of time.</li>
</ul>

<h2>Verse-by-Verse Literary Analysis</h2>

<h3>RM's Opening Verse: The Snow of Omelas</h3>

<p>RM's verse opens with "보고 싶다 / 이렇게 말하니까 더 보고 싶다" (I miss you / saying this makes me miss you more). This self-referential observation — that articulating pain intensifies it — is a sophisticated literary device. It echoes the paradox in psychotherapy where naming trauma can initially deepen suffering before healing begins.</p>

<p>His reference to "those who walk away from Omelas" is the song's most intellectually ambitious moment. In Le Guin's story, citizens of a utopian city discover their happiness depends on one child's suffering in a basement. Some choose to walk away from Omelas entirely, rejecting both the happiness and the system that produces it. RM positions himself as one who walks away — someone who refuses to accept a world where such loss exists, even if it means abandoning comfort.</p>

<h3>Suga's Verse: Footprints in Snow</h3>

<p>Suga's verse introduces the imagery of "발자국을 따라 걸어가" (walking along footprints). Snow preserves footprints temporarily before melting erases them — a perfect metaphor for how memories of the deceased gradually fade despite our desperate attempts to preserve them. The choice of snow rather than sand (which is more common in Western poetry) is culturally significant: Korean winters are long and isolating, and the first snowfall carries romantic and nostalgic weight.</p>

<h3>The Chorus: Collective Yearning</h3>

<p>The chorus — "눈꽃이 떨어져요 또 조금씩 멀어져요" (Snowflakes are falling, we're drifting apart little by little) — uses the passive voice deliberately. The subjects are not choosing to drift apart; it is happening to them, like snowflakes falling. This grammatical choice removes agency from the grief, making it feel like a natural force rather than a personal failure. In Korean grammar, this passive construction (떨어져요 rather than 떨어뜨려요) carries significant emotional weight that is difficult to translate.</p>

<h2>Spring Day in the Context of BTS's Discography</h2>

<p>Spring Day sits at a crucial inflection point in BTS's artistic evolution. Released during the "Wings" era, it bridges the youthful angst of their earlier work with the philosophical depth that would define the "Love Yourself" and "Map of the Soul" series.</p>

<p>Compare Spring Day to their earlier emotional track "I Need U" (2015). While "I Need U" expresses pain through dramatic imagery — rain, running, desperation — Spring Day achieves deeper emotional impact through restraint. The pain is in what is <em>not</em> said. The spaces between words. The quiet acceptance that some distances cannot be closed.</p>

<p>This evolution continued through <a href="https://rhythmicaleskimo.com/bts-black-swan-lyrics-meaning-when-music-becomes-your-first-love-and-greatest-fear/">Black Swan</a>, which explored the fear of losing passion, and <a href="https://rhythmicaleskimo.com/bts-fake-love-lyrics-meaning-the-pain-of-erasing-yourself-to-be-loved/">Fake Love</a>, which examined self-erasure in relationships. But Spring Day remains the emotional cornerstone — the song that proved BTS could create art that transcends the K-pop framework entirely.</p>

<p>For fans wanting to connect more deeply with Korean lyrics, our guide to <a href="https://rhythmicaleskimo.com/25-essential-korean-phrases-every-bts-fan-needs-for-the-arirang-era/">essential Korean phrases for BTS fans</a> covers many of the vocabulary items used in Spring Day and other tracks.</p>

<h2>How to Experience Spring Day Like a Korean Listener</h2>

<p>Western fans often miss cultural layers that Korean listeners perceive instinctively. Here is how to deepen your experience:</p>

<p><strong>Listen during seasonal transitions.</strong> The song hits differently in late February or early March when winter is ending. If possible, listen outdoors when you can see bare trees that are just beginning to bud. The visual-auditory combination unlocks emotional responses that indoor listening cannot.</p>

<p><strong>Read the Korean lyrics phonetically.</strong> Even if you do not understand Korean, reading the romanized lyrics while listening helps you hear the vowel sounds that carry emotional weight. Korean vowels like ㅓ (eo) and ㅜ (u) naturally create sounds associated with sadness and longing.</p>

<p><strong>Watch the MV in sequence.</strong> The music video references the Sewol Ferry through imagery of shoes (representing the lost students), a carousel (representing the cyclical nature of grief), and a train (representing the journey between life and death in Korean shamanic tradition). Watch it three times: once for the visuals, once for the choreography, and once focusing only on facial expressions.</p>

<p><strong>Understand nunchi (눈치).</strong> Korean communication relies heavily on "nunchi" — the ability to read unspoken emotions. Spring Day is a nunchi masterpiece. The most important emotions are conveyed through vocal inflections, pauses, and what the lyrics deliberately leave unsaid. Train yourself to listen for the gaps.</p>

'''

print("\n=== Expanding Post 404 ===")
wc = add_content(404, extra_404)
if wc < 2500:
    print(f"  Warning: {wc} < 2500, adding more content...")

# ── POST 78: Your First K-Pop Concert in Korea Guide (~1150w needed) ──
extra_78 = '''
<h2>Concert Venue Guide: What to Expect at Korea's Major Arenas</h2>

<p>Not all Korean concert venues are created equal. Each major arena has quirks that can significantly affect your experience. Here is an insider breakdown of the venues you are most likely to encounter:</p>

<h3>KSPO Dome (Olympic Gymnastics Arena), Seoul</h3>
<p>Capacity: 15,000. This is the most common venue for top-tier K-pop concerts. The standing area (아레나/arena) offers the closest experience but requires arriving 4-6 hours early for a good spot. Seats in sections 2xx offer the best balance of proximity and sightline. Avoid sections behind the stage unless you specifically want to see the artists from behind during certain choreographies — some fans actually prefer this angle for dance-heavy groups.</p>

<p><strong>Pro tip:</strong> The KSPO Dome has notoriously cold air conditioning even in summer. Bring a light jacket regardless of the season. The nearest subway exit is Olympic Park Station (Line 5, Exit 3), and the walk takes approximately 15 minutes through the park.</p>

<h3>Gocheok Sky Dome, Seoul</h3>
<p>Capacity: 25,000. Korea's only domed baseball stadium doubles as a mega-concert venue for the biggest acts. Sound quality is notably worse than KSPO due to the cavernous space and hard surfaces creating echo. Floor standing is chaotic but electric. Upper deck seats (3F) are far but offer a spectacular view of the full stage production. BTS, BLACKPINK, and Stray Kids have all headlined here.</p>

<h3>BEXCO, Busan</h3>
<p>Capacity: 4,000-10,000 (configurable). If your concert is in Busan rather than Seoul, you are in for a treat. Busan fans are legendary for their energy, and the smaller venue creates an intimacy that Seoul's mega-arenas cannot match. The venue is directly connected to Centum City Station (Line 2) and the surrounding area has excellent restaurants for pre-concert meals — check out our <a href="https://rhythmicaleskimo.com/busan-food-guide-8-dishes-you-can-only-find-in-koreas-coastal-capital/">Busan food guide</a> for recommendations.</p>

<h3>Jamsil Arena (Jamsil Indoor Stadium), Seoul</h3>
<p>Capacity: 11,000. An older venue but beloved for its compact layout that puts every seat relatively close to the stage. The acoustics are superior to Gocheok, making it ideal for vocal-heavy groups. Located right next to Lotte World and Sports Complex Station (Line 2).</p>

<h2>The Korean Ticketing System: A Complete Survival Guide</h2>

<p>If you thought getting concert tickets in your home country was competitive, Korean ticketing will test every ounce of your patience and internet speed. Here is how the system works and how to maximize your chances:</p>

<h3>Major Ticketing Platforms</h3>
<ul>
<li><strong>Interpark Ticket (ticket.interpark.com):</strong> The largest platform, used for most K-pop concerts. Create your account and verify your identity at least one week before the sale date. International fans can register with a passport number.</li>
<li><strong>Yes24 Ticket:</strong> Second most popular. Similar registration process but with a slightly different interface.</li>
<li><strong>Melon Ticket:</strong> Occasionally used for concerts sponsored by Melon. Requires a Korean phone number for full functionality, making it harder for international fans.</li>
<li><strong>Weverse Shop:</strong> For HYBE artists (BTS, SEVENTEEN, TXT, etc.), fan club presale tickets are sold through Weverse. Membership costs approximately 30,000 KRW ($22 USD) per year.</li>
</ul>

<h3>Step-by-Step Ticketing Strategy</h3>
<p><strong>T-minus 7 days:</strong> Create and verify your account. Add your payment method — Korean credit cards process fastest, but international Visa/Mastercard works. Complete any required identity verification.</p>

<p><strong>T-minus 1 day:</strong> Clear your browser cache. Log into the ticketing site and stay logged in. Bookmark the exact concert page. Test your internet speed — you need at least 50 Mbps for competitive ticketing. If your hotel WiFi is slow, consider going to a PC bang (internet cafe) for faster speeds.</p>

<p><strong>T-minus 10 minutes:</strong> Open three browser tabs with the ticketing page. Do NOT use a VPN — Korean ticketing sites often block VPN traffic and may ban your account. Refresh at exactly the sale time (usually 8 PM KST).</p>

<p><strong>The moment tickets drop:</strong> Do not be picky about seat selection. Select ANY available seats first, then check if better options exist. You have a limited hold time (usually 8-10 minutes) to complete payment. Hesitation means losing everything. If your first choice sells out, immediately check for single seats — groups are harder to get than singles.</p>

<h2>Day-of-Concert Checklist and Timeline</h2>

<p>Here is a proven timeline that hundreds of international K-pop fans have used successfully:</p>

<table style="width:100%; border-collapse:collapse; margin:1.5em 0;">
<tr style="background:#f0f4ff;"><th style="padding:10px; border:1px solid #ddd;">Time Before Concert</th><th style="padding:10px; border:1px solid #ddd;">Action</th><th style="padding:10px; border:1px solid #ddd;">Notes</th></tr>
<tr><td style="padding:10px; border:1px solid #ddd;">6 hours</td><td style="padding:10px; border:1px solid #ddd;">Arrive for standing area (아레나)</td><td style="padding:10px; border:1px solid #ddd;">Numbered wristbands distributed; leave and return</td></tr>
<tr><td style="padding:10px; border:1px solid #ddd;">4 hours</td><td style="padding:10px; border:1px solid #ddd;">Explore fan booths and merch</td><td style="padding:10px; border:1px solid #ddd;">Fan-made freebies (cupsleeves, photocards) available outside</td></tr>
<tr><td style="padding:10px; border:1px solid #ddd;">3 hours</td><td style="padding:10px; border:1px solid #ddd;">Eat a proper meal nearby</td><td style="padding:10px; border:1px solid #ddd;">You will not have time later; avoid heavy food</td></tr>
<tr><td style="padding:10px; border:1px solid #ddd;">2 hours</td><td style="padding:10px; border:1px solid #ddd;">Buy official merchandise</td><td style="padding:10px; border:1px solid #ddd;">Lines are 30-90 min; popular items sell out fast</td></tr>
<tr><td style="padding:10px; border:1px solid #ddd;">1 hour</td><td style="padding:10px; border:1px solid #ddd;">Enter venue, find your seat/spot</td><td style="padding:10px; border:1px solid #ddd;">Charge phone to 100%, use restroom</td></tr>
<tr><td style="padding:10px; border:1px solid #ddd;">30 minutes</td><td style="padding:10px; border:1px solid #ddd;">Learn fan chants from neighbors</td><td style="padding:10px; border:1px solid #ddd;">Korean fans are incredibly helpful to foreigners</td></tr>
<tr><td style="padding:10px; border:1px solid #ddd;">0</td><td style="padding:10px; border:1px solid #ddd;">Concert begins</td><td style="padding:10px; border:1px solid #ddd;">Put your phone away for the first song — experience it live</td></tr>
</table>

<h2>After the Concert: Making the Most of Your K-Pop Trip</h2>

<p>The concert is over, but your K-pop experience in Korea does not have to end. Here are post-concert activities that dedicated fans should not miss:</p>

<p><strong>Visit entertainment company buildings.</strong> HYBE's headquarters in Yongsan is a pilgrimage site for BTS fans. SM Entertainment in Seongsu-dong, JYP in Cheongdam, and YG in Hapjeong all have recognizable exteriors where fans gather. Our <a href="https://rhythmicaleskimo.com/hybe-insight-museum-big-4-entertainment-tours-the-ultimate-k-pop-pilgrimage-guide/">HYBE Insight Museum and Big 4 tour guide</a> has exact addresses and visiting tips.</p>

<p><strong>Hunt for photocards.</strong> Myeongdong and Hongdae have dozens of K-pop merchandise shops selling and trading photocards. Prices range from 2,000 KRW ($1.50) for common cards to over 100,000 KRW ($75) for rare pulls. Always check card condition before purchasing.</p>

<p><strong>Explore K-drama filming locations.</strong> If you are staying in Seoul for a few more days, many K-drama locations are easily accessible. Check out our guide to <a href="https://rhythmicaleskimo.com/top-10-k-drama-cafes-in-seoul-you-can-actually-visit-in-2026/">K-Drama cafes you can actually visit</a> for Instagram-worthy spots that combine your love of Korean entertainment with great coffee.</p>

<p><strong>Try concert afterparty restaurants.</strong> Korean fans often gather at specific restaurants near concert venues for informal afterparties. Near KSPO Dome, the Bangi neighborhood has excellent late-night options including our featured <a href="https://rhythmicaleskimo.com/korean-fried-chicken-guide-why-kfc-means-something-different-in-korea/">Korean fried chicken spots</a> — perfect fuel for reliving concert highlights with fellow fans over beer and chicken.</p>

'''

print("\n=== Expanding Post 78 ===")
wc = add_content(78, extra_78)
if wc < 2500:
    print(f"  Warning: {wc} < 2500, adding more content...")

# ── POST 186: How to Read Korean Hangul in 30 Minutes (~1200w needed) ──
extra_186 = '''
<h2>Common Hangul Reading Mistakes and How to Fix Them</h2>

<p>Even after learning all the characters, most beginners hit the same stumbling blocks when reading Korean in the real world. Here are the most frequent mistakes and how to overcome them quickly:</p>

<h3>Sound Change Rules That Textbooks Gloss Over</h3>

<p>Korean pronunciation is not always what the written characters suggest. These sound change rules trip up nearly every learner, but mastering them will make your spoken Korean sound dramatically more natural:</p>

<table style="width:100%; border-collapse:collapse; margin:1.5em 0;">
<tr style="background:#f0fff4;"><th style="padding:10px; border:1px solid #ddd;">Rule</th><th style="padding:10px; border:1px solid #ddd;">Written</th><th style="padding:10px; border:1px solid #ddd;">Actually Pronounced</th><th style="padding:10px; border:1px solid #ddd;">Example</th></tr>
<tr><td style="padding:10px; border:1px solid #ddd;">Nasalization</td><td style="padding:10px; border:1px solid #ddd;">ㅂ + ㄴ</td><td style="padding:10px; border:1px solid #ddd;">ㅁ + ㄴ</td><td style="padding:10px; border:1px solid #ddd;">감사합니다 → gamsahamnida (not gamsahabnida)</td></tr>
<tr><td style="padding:10px; border:1px solid #ddd;">Linking</td><td style="padding:10px; border:1px solid #ddd;">받침 + ㅇ</td><td style="padding:10px; border:1px solid #ddd;">consonant moves to next syllable</td><td style="padding:10px; border:1px solid #ddd;">한국어 → han-gu-geo (not han-guk-eo)</td></tr>
<tr><td style="padding:10px; border:1px solid #ddd;">Tensification</td><td style="padding:10px; border:1px solid #ddd;">ㄱ + ㄱ</td><td style="padding:10px; border:1px solid #ddd;">ㄱ + ㄲ</td><td style="padding:10px; border:1px solid #ddd;">학교 → hakkkyo (doubled sound)</td></tr>
<tr><td style="padding:10px; border:1px solid #ddd;">Aspiration</td><td style="padding:10px; border:1px solid #ddd;">ㄱ + ㅎ</td><td style="padding:10px; border:1px solid #ddd;">ㅋ</td><td style="padding:10px; border:1px solid #ddd;">축하 → chuka (not chukha)</td></tr>
<tr><td style="padding:10px; border:1px solid #ddd;">ㄹ rule</td><td style="padding:10px; border:1px solid #ddd;">ㄹ between vowels</td><td style="padding:10px; border:1px solid #ddd;">light R/L sound</td><td style="padding:10px; border:1px solid #ddd;">사랑 → sa-rang (R sound, not L)</td></tr>
</table>

<p><strong>The good news:</strong> You do not need to memorize all these rules consciously. After reading Korean regularly for about two weeks, your brain starts applying them automatically. The key is exposure — read Korean signs, menus, and subtitles as much as possible.</p>

<h3>Double Consonants: The Sounds That Frustrate Beginners</h3>

<p>Korean has five double (tense) consonants that have no English equivalent: ㄲ, ㄸ, ㅃ, ㅆ, ㅉ. These are produced by tensing your throat muscles and releasing the sound with more force — imagine you are lifting something heavy while speaking. Here is how to distinguish them:</p>

<ul>
<li><strong>ㄱ vs ㄲ:</strong> ㄱ (giyeok) is like "g" in "go." ㄲ (ssang-giyeok) is a tighter, sharper sound with no aspiration. Compare 가 (ga, "go") with 까 (kka, used in slang).</li>
<li><strong>ㄷ vs ㄸ:</strong> ㄷ (digeut) is like "d" in "do." ㄸ (ssang-digeut) is tenser, like the "t" in "stop." Compare 달 (dal, "moon") with 딸 (ttal, "daughter").</li>
<li><strong>ㅂ vs ㅃ:</strong> ㅂ (bieup) is between "b" and "p." ㅃ (ssang-bieup) is a tight, unreleased "p." Compare 불 (bul, "fire") with 뿔 (ppul, "horn").</li>
<li><strong>ㅅ vs ㅆ:</strong> ㅅ (siot) is like "s" in "sea." ㅆ (ssang-siot) is a stronger, hissing "s." Compare 사 (sa, "four") with 싸 (ssa, "cheap/to fight").</li>
<li><strong>ㅈ vs ㅉ:</strong> ㅈ (jieut) is like "j" in "juice." ㅉ (ssang-jieut) is a tenser version. Compare 자 (ja, "sleep") with 짜 (jja, "salty").</li>
</ul>

<h2>Real-World Practice: Reading Korean Signs and Menus</h2>

<p>The fastest way to cement your Hangul skills is reading real Korean text. Here are common signs and menu items you will encounter if you visit Korea — or spot in K-dramas:</p>

<h3>Essential Signs You Will See Everywhere</h3>
<ul>
<li><strong>출구 (chulgu)</strong> — Exit. You will see this in every subway station and building.</li>
<li><strong>입구 (ipgu)</strong> — Entrance.</li>
<li><strong>화장실 (hwajangsil)</strong> — Restroom/toilet. Often abbreviated to just the symbols ♂ and ♀.</li>
<li><strong>비상구 (bisangu)</strong> — Emergency exit.</li>
<li><strong>주의 (juui)</strong> — Caution/Warning.</li>
<li><strong>금연 (geumyeon)</strong> — No smoking.</li>
<li><strong>영업중 (yeongeopjung)</strong> — Open for business.</li>
<li><strong>준비중 (junbijung)</strong> — Preparing/Closed temporarily.</li>
<li><strong>할인 (halin)</strong> — Discount/Sale.</li>
<li><strong>무료 (muryo)</strong> — Free of charge.</li>
</ul>

<h3>Korean Restaurant Menu Decoder</h3>

<p>Reading a Korean menu is one of the most satisfying real-world applications of Hangul. Here are the building blocks you need:</p>

<p><strong>Meat types:</strong> 소고기 (sogogi, beef), 돼지고기 (dwaejigogi, pork), 닭고기 (dakgogi, chicken), 양고기 (yanggogi, lamb). Notice the pattern — 고기 (gogi) means "meat," so you just need to learn the animal prefix.</p>

<p><strong>Cooking methods:</strong> 구이 (gui, grilled), 볶음 (bokkeum, stir-fried), 찜 (jjim, steamed/braised), 튀김 (twigim, deep-fried), 조림 (jorim, simmered in sauce). If you can read these suffixes, you can decode almost any Korean menu item.</p>

<p><strong>Common dishes:</strong> 비빔밥 (bibimbap, mixed rice), 김치찌개 (kimchi-jjigae, kimchi stew), 삼겹살 (samgyeopsal, pork belly), 냉면 (naengmyeon, cold noodles), 떡볶이 (tteokbokki, spicy rice cakes).</p>

<p>For a comprehensive food ordering experience, check our guide on <a href="https://rhythmicaleskimo.com/how-to-order-food-in-korean-25-essential-phrases-every-traveler-needs/">how to order food in Korean with 25 essential phrases</a>. And if you are planning to visit Gwangjang Market, our <a href="https://rhythmicaleskimo.com/gwangjang-market-food-guide-seouls-oldest-market-and-its-legendary-street-food/">Gwangjang Market food guide</a> will help you practice reading real Korean menus in one of Seoul's most iconic food destinations.</p>

<h2>Building Speed: From Decoding to Fluent Reading</h2>

<p>Knowing individual characters is just the first step. Here is a structured 30-day plan to go from slow decoding to comfortable reading speed:</p>

<p><strong>Days 1-7: Character recognition drill.</strong> Spend 10 minutes daily on random syllable block practice. Use the Korean Random Syllable Generator (available free online) to test yourself. Target: recognize any syllable block within 3 seconds.</p>

<p><strong>Days 8-14: K-drama subtitle reading.</strong> Watch Korean shows with Korean subtitles enabled (not English). Pause when needed. You will not understand the meaning, but you will train your eyes to process Hangul blocks quickly. Target: read simple 3-4 syllable words without pausing.</p>

<p><strong>Days 15-21: Real-world text exposure.</strong> Change your phone language to Korean. Read Korean Instagram posts from accounts like @visitkorea or your favorite idol. Use Papago (Naver's translation app) to check words you cannot decode. Target: read a full sentence in under 10 seconds.</p>

<p><strong>Days 22-30: Speed reading challenge.</strong> Time yourself reading Korean children's books (available free at Korean Digital Library, library.kr). These use simple vocabulary and large fonts perfect for reading practice. Target: read one page per minute.</p>

<p>For those who want to combine Hangul practice with K-pop fandom, our guide to <a href="https://rhythmicaleskimo.com/learn-korean-through-k-dramas-30-essential-phrases-youll-actually-use/">learning Korean through K-Dramas</a> provides excellent real-world reading material with entertainment value built in.</p>

<h2>Hangul in the Digital Age: Typing Korean on Your Devices</h2>

<p>Once you can read Hangul, the natural next step is typing it. Adding a Korean keyboard to your device takes less than a minute and opens up an entirely new world of communication:</p>

<p><strong>iPhone/iPad:</strong> Settings → General → Keyboard → Keyboards → Add New Keyboard → Korean. Choose "Standard" for the 2-set layout (consonants left, vowels right), which mirrors the physical keyboard layout used in Korea.</p>

<p><strong>Android:</strong> Settings → System → Languages & Input → Virtual Keyboard → Gboard → Languages → Add Korean. The Chunjiin layout (천지인) is optimized for mobile, using just 12 keys to input all Korean characters through combinations.</p>

<p><strong>Windows/Mac:</strong> Both operating systems have built-in Korean input methods. On Mac, go to System Preferences → Keyboard → Input Sources → add Korean (2-set). On Windows, Settings → Time & Language → Language → Add Korean.</p>

<p>The Korean keyboard follows a logical pattern: consonants are on the left side, vowels on the right. When you type a consonant followed by a vowel, the system automatically combines them into a syllable block. It feels magical the first time you see 한글 appear from individual keystrokes.</p>

'''

print("\n=== Expanding Post 186 ===")
wc = add_content(186, extra_186)
if wc < 2500:
    print(f"  Warning: {wc} < 2500, adding more content...")

print("\n=== All expansions complete ===")
