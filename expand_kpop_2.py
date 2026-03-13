#!/usr/bin/env python3
"""Round 2: Add more content to posts under 2500 words."""
import sys, re
sys.path.insert(0, '/Users/choijooyong/wordpress')
import engine as e
s, h = e.login()
REST = e.REST

def add_content(pid, extra, insert_before):
    r = s.get(f'{REST}/posts/{pid}?_fields=content', headers=h)
    content = r.json()['content']['rendered']
    pt = content.find(insert_before)
    if pt == -1:
        print(f'  WARNING: insertion point not found for ID:{pid}')
        return 0
    new = content[:pt] + extra + '\n' + content[pt:]
    r2 = s.post(f'{REST}/posts/{pid}', headers=h, json={'content': new})
    if r2.status_code != 200:
        print(f'  ERROR: {r2.status_code} for ID:{pid}')
        return 0
    text = re.sub(r'<[^>]+>', '', r2.json()['content']['rendered'])
    wc = len(text.split())
    print(f'  ID:{pid} -> {wc} words')
    return wc

# ============================================================
# ID:411 — needs ~300 more words
# ============================================================
extra_411 = '''
<h2>The Extended and Rocking Vibe Versions</h2>
<p>BTS released multiple versions of "Fake Love," each revealing different emotional textures. The <strong>Extended Version</strong> adds a longer instrumental bridge that lets the song's despair breathe — the silence between sections becomes its own statement, the sound of someone too exhausted to keep pretending.</p>

<p>The <strong>Rocking Vibe Mix</strong> strips away the electronic production and replaces it with live rock instrumentation — distorted guitars, crashing cymbals, raw vocal delivery. This version transforms "Fake Love" from a polished pop production into something that sounds like it was recorded in a garage at 3 AM by someone who just had a breakdown. The rawness serves the message: when you strip away the production (the "fake"), the pain underneath is loud, messy, and unpolished.</p>

<h2>Fan Covers and Global Resonance</h2>
<p>"Fake Love" became one of the most covered BTS songs across cultures. What's fascinating is <em>how</em> different cultures interpret the song's message. Western covers tend to emphasize the romantic heartbreak angle. Japanese covers lean into the aesthetic melancholy. Southeast Asian covers often highlight the self-sacrifice theme, reflecting cultures where family and community expectations can demand similar self-erasure.</p>

<p>The song's universal appeal proves something important: the experience of losing yourself to please others isn't unique to Korean culture. It's a human condition. Whether it's called <em>nunchi</em> in Korea, <em>tatemae</em> in Japan, or "people-pleasing" in English-speaking countries, the core experience — performing a version of yourself for others until you forget who you really are — transcends language and borders.</p>

<div class="rk-info">
<strong>Global Milestone:</strong> "Fake Love" was the first Korean-language song to be certified Platinum by the RIAA (Recording Industry Association of America), signifying over 1 million units sold in the United States. This achievement shattered the assumption that non-English songs couldn't achieve mainstream commercial success in the world's largest music market.
</div>
'''

# ============================================================
# ID:409 — needs ~350 more words
# ============================================================
extra_409 = '''
<h2>The Dance Practice Video: Raw Vulnerability</h2>
<p>While most K-pop dance practice videos showcase precision and synchronized power, the "Black Swan" dance practice feels different. The members perform in all black against a simple backdrop, and their movements carry an emotional weight that's absent from the polished MV.</p>

<p>Choreographer Son Sungdeuk incorporated elements of <strong>contemporary dance</strong> — floor work, weight sharing, controlled falls — that are rarely seen in mainstream K-pop. The result is choreography that looks less like a performance and more like an emotional exorcism. Bodies collapse and rise. Members catch each other mid-fall. Solo moments emerge from group formations like thoughts surfacing from the subconscious.</p>

<p>The key sequence occurs during the "do your thang" section: all seven members execute the same movement but with slightly different timing, creating a visual ripple effect. This wasn't a mistake — it was choreographed to represent seven different people experiencing the same fear at different moments. The fear of losing passion doesn't hit everyone simultaneously. It creeps through a group like a wave.</p>

<h2>Connections to Other BTS Songs About Artistic Fear</h2>
<p>BTS has explored the tension between artistic passion and burnout throughout their career. "Black Swan" is the climax of a theme that appears in multiple earlier works:</p>

<p><strong>"Intro: What Am I to You" (2014):</strong> RM questions the relationship between artist and audience — does the music belong to him or to the fans?</p>

<p><strong>"Sea" (hidden track, 2017):</strong> The metaphor of the desert and the sea — success looks beautiful from the outside (the sea), but getting there means crossing an endless desert of doubt and exhaustion.</p>

<p><strong>"Interlude: Shadow" (2020):</strong> SUGA's solo from the same album directly precedes "Black Swan" thematically. In "Shadow," SUGA confronts the dark side of fame — the bigger you grow, the bigger your shadow grows. "Black Swan" takes the next step: what if the shadow <em>wins</em>?</p>

<p>Together, these songs form an honest portrait of artistic life that K-pop rarely shows. The industry projects constant excitement, gratitude, and energy. BTS's willingness to show exhaustion, doubt, and the fear of creative death is what makes them feel <strong>real</strong> in an industry built on carefully constructed personas.</p>
'''

# ============================================================
# ID:184 — needs ~600 more words
# ============================================================
extra_184 = '''
<h2>Music Show Tapings: See K-Pop Live for Free</h2>
<p>One of Seoul's best-kept secrets for K-pop tourists is that you can attend live music show tapings — often for free. These are the weekly programs where K-pop groups perform their latest songs, and the energy in the studio is unlike anything you'll experience elsewhere.</p>

<div class="rk-tbl-wrap">
<table class="rk-tbl">
<tr><th>Show</th><th>Channel</th><th>Taping Day</th><th>How to Get Tickets</th></tr>
<tr><td>Music Bank</td><td>KBS</td><td>Friday</td><td>Fan cafe lottery (apply Mon-Wed)</td></tr>
<tr><td>Music Core</td><td>MBC</td><td>Saturday</td><td>Fan cafe lottery or on-site standby</td></tr>
<tr><td>Inkigayo</td><td>SBS</td><td>Sunday (pre-record Thurs)</td><td>Fan cafe lottery (most competitive)</td></tr>
<tr><td>M Countdown</td><td>Mnet</td><td>Thursday</td><td>Mnet Plus app lottery</td></tr>
<tr><td>Show Champion</td><td>MBC M</td><td>Wednesday</td><td>Easiest to attend — on-site registration often available</td></tr>
</table>
</div>

<p><strong>Pro tip for international fans:</strong> Show Champion on MBC M is the easiest music show to attend as a foreigner. The audience is smaller, the competition for tickets is less fierce, and on-site registration is sometimes available on the day. Arrive by 2 PM for a 6 PM taping.</p>

<p><strong>What to expect:</strong> Music show tapings involve a lot of waiting (2-4 hours), strict no-recording policies, and specific fan behavior rules. You'll need to stand for the entire performance duration. But seeing your favorite group perform live, just meters away, with professional lighting and sound — it's an experience no concert ticket can replicate.</p>

<h2>K-Pop Themed Cafes Worth Your Time</h2>
<p>Beyond the official agency spaces, Seoul has a thriving ecosystem of K-pop themed cafes. Some are officially licensed; most are fan-operated labors of love.</p>

<p><strong>Cup of Idol (Hongdae):</strong> A rotating-theme cafe that changes its entire interior decoration every few months to match a different K-pop group. Menu items are named after songs and albums. The attention to detail is remarkable — even the background music playlist is curated to match the current theme.</p>

<p><strong>Photo Card Trading Cafes (Various):</strong> These aren't traditional cafes — they're marketplaces disguised as cafes. Fans bring their duplicate photo cards, display them in binders, and trade with other fans. If you're a photo card collector, these cafes are where the real action happens. The largest concentration is in Hongdae and Sinchon, near university areas.</p>

<p><strong>Line Friends Store (Gangnam/Itaewon):</strong> While not exclusively K-pop, the BT21 characters (designed by BTS members) have their own massive section. The Gangnam flagship store has exclusive BT21 merchandise not available online.</p>

<h2>Getting the Most Out of Your K-Pop Day: Insider Tips</h2>
<p><strong>Portable charger is mandatory.</strong> You'll be taking hundreds of photos, using Naver Maps for navigation, and checking social media for real-time fan updates. A dead phone battery means a dead pilgrimage.</p>

<p><strong>Wear comfortable shoes.</strong> The Big 4 tour involves significant walking and subway transfers. Fashion sneakers, not heels. Your feet will thank you after 15,000+ steps.</p>

<p><strong>Learn basic Korean numbers.</strong> Merch stores can get chaotic during busy hours. Being able to say "hana" (one) or "dul" (two) when pointing at items speeds everything up. Our <a href="/how-to-read-korean-hangul-in-30-minutes-the-fastest-method-that-actually-works/">Hangul reading guide</a> covers the essentials.</p>

<p><strong>Bring a clear bag.</strong> Some venues require transparent bags for security. Having one ready saves you the hassle of transferring items at the door.</p>

<p><strong>Check social media before each stop.</strong> Fan accounts on X (Twitter) post real-time updates about special merch drops, pop-up events, and artist sightings in the agency areas. Search hashtags like #HYBEInsight, #SMTOWN, #JYPbuilding for the latest.</p>
'''

print('=== Round 2: Adding more content ===')
wc411 = add_content(411, extra_411, '<h2>You Might Also Like</h2>')
wc409 = add_content(409, extra_409, '<h2>You Might Also Like</h2>')
wc184 = add_content(184, extra_184, '<h2>You Might Also Enjoy</h2>')

print('\n=== Final Results ===')
for pid, wc in [(411, wc411), (409, wc409), (184, wc184)]:
    status = 'OK' if wc >= 2500 else 'STILL NEEDS MORE'
    print(f'  ID:{pid}: {wc}w [{status}]')
