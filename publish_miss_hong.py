#!/usr/bin/env python3
"""Publish Undercover Miss Hong article to rhythmicaleskimo.com"""
import requests
import re
import json
import os

SITE = "https://rhythmicaleskimo.com"
REST = f"{SITE}/wp-json/wp/v2"

# ── Auth ──
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

# ── Find K-Drama category ──
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

# ── Upload featured image ──
img_path = "/Users/choijooyong/wordpress/featured_miss_hong.png"
with open(img_path, "rb") as f:
    img_data = f.read()

media_resp = s.post(f"{REST}/media", headers={
    **h,
    "Content-Disposition": "attachment; filename=featured-undercover-miss-hong-2026.png",
    "Content-Type": "image/png"
}, data=img_data)
print(f"Media upload: {media_resp.status_code}")
media = media_resp.json()
media_id = media.get("id")
print(f"Media ID: {media_id}")

# Update alt text
if media_id:
    s.post(f"{REST}/media/{media_id}", headers=h, json={
        "alt_text": "Undercover Miss Hong K-Drama 2026 - Park Shin-hye Netflix review guide",
        "caption": "Undercover Miss Hong (언더커버 미쓰홍) - Netflix's biggest K-Drama hit of 2026"
    })

# ── Article HTML ──
article_html = """
<p>If you haven't watched <strong>Undercover Miss Hong</strong> (언더커버 미쓰홍) yet, you're missing the most talked-about K-drama of early 2026. This tvN workplace comedy, now streaming globally on Netflix, combines retro 1990s nostalgia with sharp financial crime thrills and laugh-out-loud office humor.</p>

<p>Starring <strong>Park Shin-hye</strong> as a fearless securities inspector who goes undercover as a 20-year-old rookie employee, the series climbed from a modest 3.5% premiere rating to a staggering <strong>14.6% peak</strong> — making it one of the highest-rated K-dramas of 2026.</p>

<p>In this complete guide, we break down everything you need to know: the cast, plot, episode highlights, where to stream it, and why fans are already demanding a second season.</p>

<h2>What Is Undercover Miss Hong About? Plot Synopsis (Spoiler-Free)</h2>

<p>Set against the turbulent financial landscape of <strong>1997 Seoul</strong> — just before the Asian financial crisis — Undercover Miss Hong follows <strong>Hong Geum-bo</strong>, a 35-year-old elite inspector at the Financial Supervisory Service's Capital Market Investigation Division.</p>

<p>When suspicious fund flows are detected at Hanmin Securities, Geum-bo volunteers for an audacious mission: disguise herself as a fresh-faced 20-year-old junior employee and infiltrate the firm from the inside.</p>

<p>What starts as a straightforward investigation quickly spirals into chaos when she discovers that the company's new CEO is none other than <strong>her former lover</strong>. Navigating workplace politics, hidden agendas, and her own complicated past, Geum-bo must balance her cover identity with the increasingly dangerous truths she uncovers.</p>

<p>The genius of the show lies in its tone. It seamlessly blends:</p>
<ul>
<li><strong>Office comedy</strong> — Geum-bo's hilarious attempts to act like a clueless 20-year-old</li>
<li><strong>Financial thriller</strong> — Real stakes involving slush funds, corporate corruption, and insider trading</li>
<li><strong>Romance</strong> — The slow-burn tension between Geum-bo and the CEO she once loved</li>
<li><strong>90s nostalgia</strong> — Pagers, cassette tapes, retro fashion, and pre-internet office culture</li>
</ul>

<p>Think of it as a K-drama version of <em>Undercover Boss</em> meets <em>The Big Short</em>, wrapped in a candy-colored 1990s aesthetic.</p>

<h2>Complete Cast Guide: Who Stars in Undercover Miss Hong?</h2>

<p>One of the biggest reasons Undercover Miss Hong became a breakout hit is its <strong>powerhouse ensemble cast</strong>. Here's your guide to every major player.</p>

<h3>Park Shin-hye as Hong Geum-bo</h3>

<p>Park Shin-hye delivers what many critics call her <strong>best performance in years</strong>. As Hong Geum-bo, she plays a sharp, determined financial inspector who must convincingly pass as a naive 20-year-old office newbie.</p>

<p>Park's career speaks for itself. Rising to fame through <em>Stairway to Heaven</em> (2003), <em>You're Beautiful</em> (2009), <em>The Heirs</em> (2013), and <em>Pinocchio</em> (2014), she's one of Korea's most bankable actresses. Her recent hits include <em>Doctor Slump</em> (2024) and <em>The Judge from Hell</em> (2024).</p>

<p>In Undercover Miss Hong, Park showcases remarkable range — switching between Geum-bo's fierce investigator persona and her bumbling undercover act, often in the same scene. Her comedic timing, especially those now-iconic <strong>eye rolls</strong>, became a viral sensation on social media.</p>

<h3>Ko Kyung-pyo as the Male Lead</h3>

<p>Ko Kyung-pyo plays the CEO of Hanmin Securities and Geum-bo's former lover, bringing layers of charm and ambiguity to a character who could easily have been one-dimensional.</p>

<p>Best known for <em>Reply 1988</em> (2015), <em>Chicago Typewriter</em> (2017), and his acclaimed supporting role in Park Chan-wook's <em>Decision to Leave</em> (2022), Ko has proven himself as one of the most versatile actors of his generation. His chemistry with Park Shin-hye is electric — their scenes together crackle with unresolved tension and witty banter.</p>

<h3>Ha Yoon-kyung as the Opportunistic Secretary</h3>

<p>Ha Yoon-kyung, beloved for her roles in <em>Extraordinary Attorney Woo</em> (2022) and <em>Hospital Playlist</em> (2020-2021), plays an opportunistic secretary navigating her own survival in the cutthroat corporate world. Her character adds a fascinating moral gray area to the story.</p>

<h3>Cho Han-gyeol as Albert Oh</h3>

<p>Rising star Cho Han-gyeol portrays Albert Oh, a free-spirited corporate heir whose carefree exterior hides deeper motivations. Born in 2002, Cho transitioned from a promising baseball career to acting, gaining attention in <em>The Haunted Palace</em> (2025) before breaking out in this role.</p>

<h3>ITZY's Yuna as Hong Jang-mi</h3>

<p>In her highly anticipated <strong>acting debut</strong>, ITZY member Yuna plays Hong Jang-mi, Geum-bo's younger sister. Despite being a first-time actress, Yuna impressed both critics and audiences with her natural screen presence, handling both comedic and emotional scenes alongside veteran performers.</p>

<div style="overflow-x:auto;max-width:100%">
<table style="width:100%;border-collapse:collapse;margin:1.5em 0">
<thead>
<tr style="background:#b91c1c;color:#fff">
<th style="padding:12px;text-align:left">Actor</th>
<th style="padding:12px;text-align:left">Character</th>
<th style="padding:12px;text-align:left">Known For</th>
</tr>
</thead>
<tbody>
<tr style="background:#fef2f2">
<td style="padding:10px">Park Shin-hye</td>
<td style="padding:10px">Hong Geum-bo</td>
<td style="padding:10px">The Heirs, Pinocchio, Doctor Slump</td>
</tr>
<tr>
<td style="padding:10px">Ko Kyung-pyo</td>
<td style="padding:10px">CEO / Former Lover</td>
<td style="padding:10px">Reply 1988, Decision to Leave</td>
</tr>
<tr style="background:#fef2f2">
<td style="padding:10px">Ha Yoon-kyung</td>
<td style="padding:10px">Secretary</td>
<td style="padding:10px">Extraordinary Attorney Woo</td>
</tr>
<tr>
<td style="padding:10px">Cho Han-gyeol</td>
<td style="padding:10px">Albert Oh</td>
<td style="padding:10px">The Haunted Palace</td>
</tr>
<tr style="background:#fef2f2">
<td style="padding:10px">Yuna (ITZY)</td>
<td style="padding:10px">Hong Jang-mi</td>
<td style="padding:10px">Acting debut</td>
</tr>
</tbody>
</table>
</div>

<h2>Episode Guide: 16 Episodes of Pure Entertainment</h2>

<p>Undercover Miss Hong aired on tvN every <strong>Saturday and Sunday at 9:10 PM KST</strong> from January 17 to March 8, 2026. All 16 episodes are now available on Netflix for international viewers.</p>

<h3>Rating Trajectory: From Sleeper to Sensation</h3>

<p>The drama's ratings tell a remarkable story of word-of-mouth growth:</p>

<div style="overflow-x:auto;max-width:100%">
<table style="width:100%;border-collapse:collapse;margin:1.5em 0">
<thead>
<tr style="background:#b91c1c;color:#fff">
<th style="padding:12px;text-align:left">Episode</th>
<th style="padding:12px;text-align:left">Date</th>
<th style="padding:12px;text-align:center">Nationwide</th>
<th style="padding:12px;text-align:center">Seoul</th>
</tr>
</thead>
<tbody>
<tr style="background:#fef2f2">
<td style="padding:10px">Ep 1 (Premiere)</td>
<td style="padding:10px">Jan 17</td>
<td style="padding:10px;text-align:center">3.5%</td>
<td style="padding:10px;text-align:center">3.2%</td>
</tr>
<tr>
<td style="padding:10px">Ep 4</td>
<td style="padding:10px">Jan 25</td>
<td style="padding:10px;text-align:center">7.0%+</td>
<td style="padding:10px;text-align:center">—</td>
</tr>
<tr style="background:#fef2f2">
<td style="padding:10px">Ep 8</td>
<td style="padding:10px">Feb 8</td>
<td style="padding:10px;text-align:center">9.4%</td>
<td style="padding:10px;text-align:center">10.0%+</td>
</tr>
<tr>
<td style="padding:10px">Ep 12</td>
<td style="padding:10px">Feb 22</td>
<td style="padding:10px;text-align:center">~11%</td>
<td style="padding:10px;text-align:center">—</td>
</tr>
<tr style="background:#fef2f2">
<td style="padding:10px">Ep 15 (Peak)</td>
<td style="padding:10px">Mar 7</td>
<td style="padding:10px;text-align:center"><strong>13.1%</strong></td>
<td style="padding:10px;text-align:center"><strong>14.0%</strong></td>
</tr>
<tr>
<td style="padding:10px">Ep 16 (Finale)</td>
<td style="padding:10px">Mar 8</td>
<td style="padding:10px;text-align:center">12.4%</td>
<td style="padding:10px;text-align:center">13.0%</td>
</tr>
</tbody>
</table>
</div>

<p>That's a <strong>3.7x growth</strong> from premiere to peak — almost unheard of in the competitive Korean TV landscape. The series maintained the <strong>#1 spot in its timeslot</strong> across all channels for multiple consecutive weeks.</p>

<h3>Key Story Arcs by Phase</h3>

<p><strong>Episodes 1-4: The Setup.</strong> Geum-bo accepts the undercover mission and transforms herself into a convincing 20-year-old. The comedy shines as she struggles with 90s slang, office hierarchy, and the shock of seeing her ex as the company boss.</p>

<p><strong>Episodes 5-8: The Investigation Deepens.</strong> As Geum-bo uncovers layers of financial fraud, she forms unlikely alliances with her dorm mates in Room 301. The show introduces the mysterious connection to events nine years in the past.</p>

<p><strong>Episodes 9-12: Rising Stakes.</strong> The villain Pil-beom's schemes become more dangerous, and Geum-bo's cover is nearly blown multiple times. The romance subplot gains momentum as old feelings resurface.</p>

<p><strong>Episodes 13-16: The Climax.</strong> The women of dorm 301 unite to take down the corrupt leadership. A jaw-dropping vote sequence, Geum-bo's parents hilariously taking out gangsters, and a satisfying justice-served finale made these the highest-rated episodes.</p>

<h3>Standout Moments Fans Can't Stop Talking About</h3>

<ul>
<li>Geum-bo's "kicking ass" montage replacing a typical romance sequence</li>
<li>The dorm 301 girls' late-night strategy sessions</li>
<li>Albert Oh's unexpected character reveal</li>
<li>The parents' tag-team gangster takedown scene</li>
<li>No-ra's shocking vote in the finale that turned the tide</li>
</ul>

<h2>Why Undercover Miss Hong Is 2026's Must-Watch K-Drama</h2>

<p>In a year already packed with strong K-drama releases, Undercover Miss Hong stands out for several reasons:</p>

<h3>1. Perfect Genre Balance</h3>

<p>Most K-dramas excel at one thing — romance, thriller, or comedy. Undercover Miss Hong masters all three simultaneously. You'll laugh at the office hijinks, bite your nails during the financial crime reveals, and root for the romance — all in the same episode.</p>

<h3>2. A Retro Setting That Feels Fresh</h3>

<p>The 1997 setting isn't just nostalgia bait. It serves the story perfectly: no smartphones mean Geum-bo can't just Google information, pre-digital finance means paper trails and face-to-face deception, and the looming Asian financial crisis adds real historical weight.</p>

<h3>3. Strong Female Characters</h3>

<p>This is fundamentally a story about <strong>women supporting women</strong>. Geum-bo, No-ra, Bok-hee, and Mi-sook — the women of dorm 301 — each have distinct personalities, motivations, and arcs. Their solidarity is the emotional backbone of the entire series.</p>

<h3>4. Consistent Quality Across 16 Episodes</h3>

<p>Many K-dramas suffer from a "mid-season slump." Undercover Miss Hong maintains its momentum from start to finish — the ratings trajectory proves it. Critics noted it "sustained itself without faltering for all 16 episodes."</p>

<h3>5. Netflix Global Reach</h3>

<p>On Netflix, the series entered the <strong>Global Top 10 for Non-English TV</strong> at #6 in its first week and peaked at <strong>#4</strong> during February 2-8. It introduced Park Shin-hye to millions of new international viewers.</p>

<p>If you enjoyed the clever twists of <a href="/sirens-kiss-complete-guide-cast-plot-episodes-where-to-watch-2026/">Siren's Kiss</a> or the intense storytelling of <a href="/phantom-lawyer-%ec%9c%a0%eb%a0%b9-%eb%b3%80%ed%98%b8%ec%82%ac-complete/">Phantom Lawyer</a>, Undercover Miss Hong delivers that same quality with a lighter, more comedic touch.</p>

<h2>Where to Watch Undercover Miss Hong: Streaming Guide & Prices</h2>

<p>All 16 episodes of Undercover Miss Hong are available to stream right now. Here's where to watch:</p>

<div style="overflow-x:auto;max-width:100%">
<table style="width:100%;border-collapse:collapse;margin:1.5em 0">
<thead>
<tr style="background:#b91c1c;color:#fff">
<th style="padding:12px;text-align:left">Platform</th>
<th style="padding:12px;text-align:left">Region</th>
<th style="padding:12px;text-align:left">Price (Monthly)</th>
<th style="padding:12px;text-align:center">Subtitles</th>
</tr>
</thead>
<tbody>
<tr style="background:#fef2f2">
<td style="padding:10px"><strong>Netflix</strong></td>
<td style="padding:10px">Global (190+ countries)</td>
<td style="padding:10px">$7.99 (with ads) / $17.99 / $24.99</td>
<td style="padding:10px;text-align:center">Yes (multi-language)</td>
</tr>
<tr>
<td style="padding:10px"><strong>TVING</strong></td>
<td style="padding:10px">South Korea</td>
<td style="padding:10px">₩7,900 - ₩17,000</td>
<td style="padding:10px;text-align:center">Korean only</td>
</tr>
<tr style="background:#fef2f2">
<td style="padding:10px"><strong>tvN (broadcast)</strong></td>
<td style="padding:10px">South Korea</td>
<td style="padding:10px">Free (cable TV)</td>
<td style="padding:10px;text-align:center">Korean only</td>
</tr>
</tbody>
</table>
</div>

<p><strong>Our recommendation:</strong> For international viewers, Netflix is the best option with high-quality subtitles in multiple languages. The Standard plan ($17.99/month) offers ad-free HD streaming on two devices.</p>

<p>Planning a trip to Korea after watching? Check out our guide to <a href="/top-10-k-drama-cafes-in-seoul-you-can-actually-visit-in-2026/">K-Drama filming cafes you can actually visit in Seoul</a>.</p>

<h2>Will There Be a Season 2? Everything We Know</h2>

<p>The short answer: <strong>not confirmed yet, but highly likely</strong>.</p>

<p>Here's what we know about the possibility of Undercover Miss Hong Season 2:</p>

<h3>Evidence FOR Season 2</h3>

<ul>
<li><strong>The finale set it up.</strong> The final episode showed Geum-bo taking on a new undercover assignment at an insurance firm investigating financial crimes — a clear setup for a potential second season.</li>
<li><strong>Massive viewer demand.</strong> Fans flooded social media with "Give us Season 2" campaigns immediately after the finale aired.</li>
<li><strong>Exceptional ratings.</strong> A drama that grows from 3.5% to 14.6% is a network's dream. tvN has every financial incentive to bring it back.</li>
<li><strong>Netflix global success.</strong> Reaching #4 globally demonstrates international demand, which Netflix heavily factors into renewal decisions.</li>
<li><strong>Precedent.</strong> Other tvN dramas like <em>Taxi Driver</em> and <em>Alchemy of Souls</em> returned for successful second seasons.</li>
</ul>

<h3>Potential Obstacles</h3>

<ul>
<li><strong>K-drama tradition.</strong> Most Korean dramas are designed as single-season stories. Multi-season runs are still the exception.</li>
<li><strong>Cast availability.</strong> Park Shin-hye and Ko Kyung-pyo are A-list actors with packed schedules. Coordinating everyone's calendars could delay production.</li>
<li><strong>Writer/director commitment.</strong> Writer Moon Hyun-kyung and directors Park Seon-ho and Na Ji-hyun would need to return for creative continuity.</li>
</ul>

<p><strong>Our prediction:</strong> Given the massive ratings, Netflix success, and the deliberate Season 2 setup in the finale, we expect an official announcement by mid-2026, with a potential air date in early 2027.</p>

<h2>Drama Details at a Glance</h2>

<div style="overflow-x:auto;max-width:100%">
<table style="width:100%;border-collapse:collapse;margin:1.5em 0">
<tbody>
<tr style="background:#fef2f2">
<td style="padding:10px;font-weight:bold;width:35%">Korean Title</td>
<td style="padding:10px">언더커버 미쓰홍</td>
</tr>
<tr>
<td style="padding:10px;font-weight:bold">Genre</td>
<td style="padding:10px">Comedy, Crime, Drama, Romance</td>
</tr>
<tr style="background:#fef2f2">
<td style="padding:10px;font-weight:bold">Episodes</td>
<td style="padding:10px">16</td>
</tr>
<tr>
<td style="padding:10px;font-weight:bold">Air Dates</td>
<td style="padding:10px">Jan 17 – Mar 8, 2026</td>
</tr>
<tr style="background:#fef2f2">
<td style="padding:10px;font-weight:bold">Network</td>
<td style="padding:10px">tvN (Sat-Sun 9:10 PM KST)</td>
</tr>
<tr>
<td style="padding:10px;font-weight:bold">Streaming</td>
<td style="padding:10px">Netflix (Global), TVING (Korea)</td>
</tr>
<tr style="background:#fef2f2">
<td style="padding:10px;font-weight:bold">Director</td>
<td style="padding:10px">Park Seon-ho, Na Ji-hyun</td>
</tr>
<tr>
<td style="padding:10px;font-weight:bold">Writer</td>
<td style="padding:10px">Moon Hyun-kyung</td>
</tr>
<tr style="background:#fef2f2">
<td style="padding:10px;font-weight:bold">Peak Rating</td>
<td style="padding:10px">14.6% (Seoul, Ep 15)</td>
</tr>
<tr>
<td style="padding:10px;font-weight:bold">IMDb Rating</td>
<td style="padding:10px">7.5/10</td>
</tr>
<tr style="background:#fef2f2">
<td style="padding:10px;font-weight:bold">Netflix Rank</td>
<td style="padding:10px">#4 Global Non-English TV</td>
</tr>
<tr>
<td style="padding:10px;font-weight:bold">Setting</td>
<td style="padding:10px">1997 Seoul, South Korea</td>
</tr>
</tbody>
</table>
</div>

<h2>How Undercover Miss Hong Compares to Other 2026 K-Dramas</h2>

<p>2026 has been a stellar year for K-dramas. Here's how Undercover Miss Hong stacks up against the competition:</p>

<p><strong>vs. <a href="/boyfriend-on-demand-jisoos-netflix-k-drama-complete-guide-cast-review-/">Boyfriend on Demand</a>:</strong> While Jisoo's Netflix debut focused on pure romance, Undercover Miss Hong offers a richer genre blend with comedy and crime elements. Both proved that star power drives viewership.</p>

<p><strong>vs. <a href="/mad-concrete-dreams-%eb%af%b8%ec%b9%9c-%ec%bd%98%ed%81%ac%eb%a6%ac%ed%8a%b8-k-drama-review-2026-cast-plot-episodes-why-its-the-years-most-intense-thriller/">Mad Concrete Dreams</a>:</strong> If Mad Concrete Dreams is 2026's darkest thriller, Undercover Miss Hong is its brightest comedy-thriller. Different tones, equally excellent execution.</p>

<p>For more great dramas to add to your watchlist, see our guide to <a href="/5-must-watch-k-dramas-before-boyfriend-on-demand-premieres-on-netflix/">5 must-watch K-dramas of 2026</a>.</p>

<h2>Frequently Asked Questions</h2>

<h3>How many episodes does Undercover Miss Hong have?</h3>
<p>Undercover Miss Hong has <strong>16 episodes</strong>, each approximately 70-80 minutes long. The series aired from January 17 to March 8, 2026, on tvN, with two episodes per week (Saturday and Sunday).</p>

<h3>Is Undercover Miss Hong on Netflix?</h3>
<p>Yes. All 16 episodes are available on <strong>Netflix</strong> for viewers in 190+ countries. Netflix plans start at $7.99/month (with ads). The show is also available on TVING in South Korea.</p>

<h3>Who plays the lead in Undercover Miss Hong?</h3>
<p><strong>Park Shin-hye</strong> stars as Hong Geum-bo, the securities inspector who goes undercover. The cast also includes Ko Kyung-pyo, Ha Yoon-kyung, Cho Han-gyeol, and ITZY's Yuna in her acting debut.</p>

<h3>What is the rating for Undercover Miss Hong?</h3>
<p>The drama peaked at <strong>13.1% nationwide</strong> and <strong>14.6% in Seoul</strong> for its penultimate episode. On IMDb, it holds a 7.5/10 rating. On Netflix, it reached #4 on the Global Non-English TV chart.</p>

<h3>Will there be a Season 2 of Undercover Miss Hong?</h3>
<p>No official announcement yet, but the finale's open ending — showing Geum-bo starting a new undercover investigation at an insurance firm — strongly hints at a second season. Given the ratings success and fan demand, a renewal announcement is widely expected in 2026.</p>

<h3>What year is Undercover Miss Hong set in?</h3>
<p>The drama is set in <strong>1997 Seoul</strong>, just before the Asian financial crisis (also known as the IMF crisis in Korea). The period setting adds both nostalgic charm and real historical stakes to the financial crime storyline.</p>

<h2>You Might Also Enjoy</h2>

<ul>
<li><a href="/sirens-kiss-complete-guide-cast-plot-episodes-where-to-watch-2026/">Siren's Kiss: Complete Guide — Cast, Plot, Episodes & Where to Watch (2026)</a></li>
<li><a href="/boyfriend-on-demand-jisoos-netflix-k-drama-complete-guide-cast-review-/">Boyfriend on Demand: Jisoo's Netflix K-Drama Complete Guide</a></li>
<li><a href="/5-must-watch-k-dramas-before-boyfriend-on-demand-premieres-on-netflix/">5 Must-Watch K-Dramas Before Boyfriend on Demand Premieres on Netflix</a></li>
</ul>

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "How many episodes does Undercover Miss Hong have?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Undercover Miss Hong has 16 episodes, each approximately 70-80 minutes long. The series aired from January 17 to March 8, 2026, on tvN, with two episodes per week (Saturday and Sunday)."
      }
    },
    {
      "@type": "Question",
      "name": "Is Undercover Miss Hong on Netflix?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes. All 16 episodes are available on Netflix for viewers in 190+ countries. Netflix plans start at $7.99/month (with ads). The show is also available on TVING in South Korea."
      }
    },
    {
      "@type": "Question",
      "name": "Who plays the lead in Undercover Miss Hong?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Park Shin-hye stars as Hong Geum-bo, the securities inspector who goes undercover. The cast also includes Ko Kyung-pyo, Ha Yoon-kyung, Cho Han-gyeol, and ITZY's Yuna in her acting debut."
      }
    },
    {
      "@type": "Question",
      "name": "What is the rating for Undercover Miss Hong?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "The drama peaked at 13.1% nationwide and 14.6% in Seoul for its penultimate episode. On IMDb, it holds a 7.5/10 rating. On Netflix, it reached #4 on the Global Non-English TV chart."
      }
    },
    {
      "@type": "Question",
      "name": "Will there be a Season 2 of Undercover Miss Hong?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "No official announcement yet, but the finale's open ending strongly hints at a second season. Given the ratings success and fan demand, a renewal announcement is widely expected in 2026."
      }
    },
    {
      "@type": "Question",
      "name": "What year is Undercover Miss Hong set in?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "The drama is set in 1997 Seoul, just before the Asian financial crisis (also known as the IMF crisis in Korea). The period setting adds both nostalgic charm and real historical stakes to the financial crime storyline."
      }
    }
  ]
}
</script>
"""

# ── Tags ──
tag_names = [
    "Undercover Miss Hong", "Park Shin-hye", "Ko Kyung-pyo",
    "Netflix K-Drama", "K-Drama 2026", "tvN drama",
    "Korean drama review", "Ha Yoon-kyung", "ITZY Yuna",
    "workplace comedy", "1997 Seoul"
]
tag_ids = []
for tag_name in tag_names:
    # Check if tag exists
    existing = s.get(f"{REST}/tags", params={"search": tag_name}, headers=h).json()
    if existing and existing[0]["name"].lower() == tag_name.lower():
        tag_ids.append(existing[0]["id"])
    else:
        resp = s.post(f"{REST}/tags", headers=h, json={"name": tag_name})
        if resp.status_code in (200, 201):
            tag_ids.append(resp.json()["id"])
print(f"Tags: {tag_ids}")

# ── Publish post ──
post_data = {
    "title": "Undercover Miss Hong: Netflix's Biggest K-Drama Hit [2026]",
    "content": article_html,
    "status": "publish",
    "categories": [kdrama_id],
    "tags": tag_ids,
    "excerpt": "Complete guide to Undercover Miss Hong (언더커버 미쓰홍) — Park Shin-hye's 2026 Netflix hit. Cast profiles, episode guide, ratings, streaming info, and Season 2 predictions.",
    "featured_media": media_id if media_id else 0,
    "slug": "undercover-miss-hong-netflix-biggest-k-drama-hit-2026-review"
}

resp = s.post(f"{REST}/posts", headers=h, json=post_data)
print(f"Publish status: {resp.status_code}")

if resp.status_code in (200, 201):
    post = resp.json()
    print(f"\n✅ Published successfully!")
    print(f"Post ID: {post['id']}")
    print(f"URL: {post['link']}")
    print(f"Title: {post['title']['raw']}")
else:
    print(f"Error: {resp.text[:500]}")
