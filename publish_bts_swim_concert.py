#!/usr/bin/env python3
"""Publish 2 BTS posts: SWIM lyrics analysis + Gwanghwamun concert guide."""
import sys, re
sys.path.insert(0, '/Users/choijooyong/wordpress')
import engine as e
from PIL import Image, ImageDraw, ImageFont

# ─── Featured Images ───────────────────────────────────────────────────

def make_featured_image(filename, bg_color, lines, subtitle_lines=None):
    img = Image.new('RGB', (1200, 630), bg_color)
    draw = ImageDraw.Draw(img)
    # gradient overlay
    for y in range(630):
        alpha = int(80 * (y / 630))
        draw.line([(0, y), (1200, y)], fill=(0, 0, 0, alpha) if img.mode == 'RGBA' else tuple(max(0, c - alpha) for c in _hex(bg_color)))

    try:
        font_large = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 52)
        font_med = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 32)
        font_small = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 24)
    except:
        font_large = ImageFont.load_default()
        font_med = font_large
        font_small = font_large

    # Main title lines
    y_pos = 160
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font_large)
        w = bbox[2] - bbox[0]
        draw.text(((1200 - w) / 2, y_pos), line, fill='white', font=font_large)
        y_pos += 65

    # Subtitle
    if subtitle_lines:
        y_pos += 20
        for sl in subtitle_lines:
            bbox = draw.textbbox((0, 0), sl, font=font_med)
            w = bbox[2] - bbox[0]
            draw.text(((1200 - w) / 2, y_pos), sl, fill=(200, 200, 255), font=font_med)
            y_pos += 42

    # Site branding
    site = "rhythmicaleskimo.com"
    bbox = draw.textbbox((0, 0), site, font=font_small)
    draw.text(((1200 - (bbox[2]-bbox[0])) / 2, 570), site, fill=(180, 180, 180), font=font_small)

    img.save(f'/Users/choijooyong/wordpress/{filename}')
    print(f"  Image saved: {filename}")

def _hex(color):
    color = color.lstrip('#')
    return tuple(int(color[i:i+2], 16) for i in (0, 2, 4))

# Generate images
make_featured_image('featured_bts_swim.png', '#0a1628',
    ['BTS "SWIM" Lyrics Meaning', '& Music Video Analysis'],
    ['ARIRANG Album Lead Single | Deep Dive'])

make_featured_image('featured_bts_concert_seoul.png', '#1a0a28',
    ['BTS Free Comeback Concert', 'Seoul March 2026'],
    ['Gwanghwamun Square | Complete Guide'])

# ─── Post 1: BTS SWIM Lyrics ──────────────────────────────────────────

post1_html = """
<article>

<p>On March 20, 2026, BTS releases their fifth studio album <strong>ARIRANG</strong> — and at its heart sits Track 7, <strong>"SWIM,"</strong> the lead single that has already sent shockwaves through the global music community. After more than three years of silence while all seven members completed their mandatory military service, BTS returns not with a bombastic anthem but with something far more profound: a meditation on resilience, self-paced growth, and the radical act of choosing to keep moving forward.</p>

<p>In this deep-dive analysis, we break down every layer of "SWIM" — from its lyrics and musical architecture to its visual symbolism and cultural significance within BTS's decade-long artistic journey.</p>

<h2>The Meaning Behind "SWIM": Navigating Life's Waves at Your Own Pace</h2>

<p>"SWIM" centers on a deceptively simple metaphor: life as an ocean, and the act of swimming as a conscious choice to persist. But BTS — and particularly RM, who holds primary songwriting credit — layers this metaphor with remarkable depth.</p>

<p>The song's central thesis, as described by Big Hit Music, is about "the resolve to keep moving forward despite life's turbulent waves." But what makes "SWIM" extraordinary is its rejection of the typical K-pop comeback narrative. BTS isn't declaring victory or promising domination. Instead, they're saying something far more vulnerable: <em>I'll keep going, at my own speed, because that itself is enough.</em></p>

<h3>Verse-by-Verse Breakdown</h3>

<p>The opening verse establishes the ocean metaphor immediately. Rather than fighting against currents — a common trope in motivational music — the lyrics suggest <strong>coexistence with difficulty</strong>. The waves aren't enemies to be conquered; they're the medium through which the swimmers move.</p>

<p>This is a significant philosophical shift from earlier BTS anthems. In "Fire" (2016), the message was essentially "burn everything down and rise." In "Not Today" (2017), it was "fight and resist." "SWIM" proposes something more mature: <strong>acceptance without surrender</strong>.</p>

<p>The pre-chorus introduces the concept of pace — swimming at your own speed rather than matching others. This resonates deeply with the members' post-military experience. Each member served in different units, at different times, processing different experiences. They're reuniting not as the synchronized unit of 2019 but as seven individuals who've grown in divergent directions.</p>

<p>The chorus expands the metaphor into something universal. The act of swimming becomes "an expression of love for life itself." This framing transforms what could be a simple perseverance anthem into something existential. BTS isn't just saying "don't give up" — they're saying <strong>"the act of continuing is itself the point."</strong></p>

<h3>The Bridge: Where "SWIM" Gets Emotional</h3>

<p>The bridge section reportedly contains the song's most emotionally charged moment. Multiple reports suggest a vocal arrangement where all seven members layer their voices in a building wave pattern — literally embodying the ocean metaphor in the song's sonic architecture.</p>

<p>This section draws a line between drowning and choosing to float. The distinction is critical: drowning is passive, something that happens <em>to</em> you. Floating is active, a decision made moment by moment. "SWIM" argues that even floating — not powerfully stroking forward, just keeping your head above water — is an act of courage.</p>

<div style="overflow-x:auto;max-width:100%">
<table style="width:100%;border-collapse:collapse;margin:20px 0">
<caption style="font-weight:bold;margin-bottom:10px">Thematic Evolution: BTS's Approach to Adversity Through Their Career</caption>
<tr style="background:#1a1a2e;color:white"><th style="padding:12px;text-align:left">Era</th><th style="padding:12px;text-align:left">Song</th><th style="padding:12px;text-align:left">Message</th><th style="padding:12px;text-align:left">Metaphor</th></tr>
<tr style="border-bottom:1px solid #ddd"><td style="padding:10px">2016</td><td style="padding:10px">Fire</td><td style="padding:10px">Burn and rise</td><td style="padding:10px">Flames</td></tr>
<tr style="border-bottom:1px solid #ddd;background:#f9f9f9"><td style="padding:10px">2017</td><td style="padding:10px">Not Today</td><td style="padding:10px">Fight back</td><td style="padding:10px">Battlefield</td></tr>
<tr style="border-bottom:1px solid #ddd"><td style="padding:10px">2018</td><td style="padding:10px">IDOL</td><td style="padding:10px">Self-acceptance</td><td style="padding:10px">Performance</td></tr>
<tr style="border-bottom:1px solid #ddd;background:#f9f9f9"><td style="padding:10px">2020</td><td style="padding:10px">ON</td><td style="padding:10px">Embrace the pain</td><td style="padding:10px">March forward</td></tr>
<tr style="border-bottom:1px solid #ddd"><td style="padding:10px">2022</td><td style="padding:10px">Yet To Come</td><td style="padding:10px">The best is ahead</td><td style="padding:10px">Journey</td></tr>
<tr style="background:#f0f0ff"><td style="padding:10px"><strong>2026</strong></td><td style="padding:10px"><strong>SWIM</strong></td><td style="padding:10px"><strong>Keep moving, at your pace</strong></td><td style="padding:10px"><strong>Ocean / Water</strong></td></tr>
</table>
</div>

<h2>Musical Architecture: How "SWIM" Sounds Different From Everything BTS Has Done</h2>

<p>"SWIM" is described as an <strong>"upbeat alternative pop"</strong> track, but early previews and producer credits suggest something more nuanced. The song was produced by <strong>Tyler Spry and Leclair</strong>, with RM leading the songwriting alongside a team of collaborators.</p>

<h3>Production Credits and What They Tell Us</h3>

<p>Tyler Spry's involvement is particularly interesting. Known for blending organic instrumentation with electronic textures, Spry's production style suggests "SWIM" won't be a typical synth-heavy K-pop track. Instead, expect layered acoustic elements — possibly including water-inspired sound design — woven through an electronic foundation.</p>

<p>The choice of producers for the entire ARIRANG album reveals BTS's ambition. The 14-track album features contributions from <strong>Diplo, Kevin Parker (Tame Impala), El Guincho, Mike WiLL Made-It, Ryan Tedder, Flume,</strong> and <strong>JPEGMAFIA</strong> — a roster that spans EDM, psychedelic rock, experimental hip-hop, and mainstream pop.</p>

<p>RM appears on songwriting credits for <strong>13 of the 14 tracks</strong>, with all six performing members (RM, Suga, J-Hope, Jimin, V, and Jungkook) holding credits across the album. This level of member involvement suggests ARIRANG is BTS's most personal and creatively controlled project to date.</p>

<h3>The "SWIM" Sound: What to Expect</h3>

<p>Based on the producers involved and Big Hit's description, "SWIM" likely features:</p>

<ul>
<li><strong>Organic instrumentation</strong> — Guitar, piano, or string elements layered beneath electronic production</li>
<li><strong>Dynamic vocal arrangements</strong> — All seven members with distinct sections rather than heavy unison</li>
<li><strong>Rhythmic fluidity</strong> — A tempo that mimics the push-pull of ocean waves rather than a strict 4/4 beat</li>
<li><strong>Atmospheric production</strong> — Spacious mixing that creates a sense of vastness (the ocean metaphor extending to the sonics)</li>
<li><strong>Minimal drop</strong> — Unlike earlier BTS title tracks, expect a build-and-release structure rather than an EDM-style drop</li>
</ul>

<div style="overflow-x:auto;max-width:100%">
<table style="width:100%;border-collapse:collapse;margin:20px 0">
<caption style="font-weight:bold;margin-bottom:10px">Complete ARIRANG Tracklist</caption>
<tr style="background:#1a1a2e;color:white"><th style="padding:12px;text-align:left">#</th><th style="padding:12px;text-align:left">Title</th><th style="padding:12px;text-align:left">Notes</th></tr>
<tr style="border-bottom:1px solid #ddd"><td style="padding:10px">1</td><td style="padding:10px">Body to Body</td><td style="padding:10px">Opening track</td></tr>
<tr style="border-bottom:1px solid #ddd;background:#f9f9f9"><td style="padding:10px">2</td><td style="padding:10px">Hooligan</td><td style="padding:10px"></td></tr>
<tr style="border-bottom:1px solid #ddd"><td style="padding:10px">3</td><td style="padding:10px">Aliens</td><td style="padding:10px"></td></tr>
<tr style="border-bottom:1px solid #ddd;background:#f9f9f9"><td style="padding:10px">4</td><td style="padding:10px">FYA</td><td style="padding:10px"></td></tr>
<tr style="border-bottom:1px solid #ddd"><td style="padding:10px">5</td><td style="padding:10px">2.0</td><td style="padding:10px"></td></tr>
<tr style="border-bottom:1px solid #ddd;background:#f9f9f9"><td style="padding:10px">6</td><td style="padding:10px">No. 29</td><td style="padding:10px"></td></tr>
<tr style="border-bottom:1px solid #ddd;background:#f0f0ff"><td style="padding:10px"><strong>7</strong></td><td style="padding:10px"><strong>SWIM</strong></td><td style="padding:10px"><strong>Lead Single / Title Track</strong></td></tr>
<tr style="border-bottom:1px solid #ddd;background:#f9f9f9"><td style="padding:10px">8</td><td style="padding:10px">Merry Go Round</td><td style="padding:10px"></td></tr>
<tr style="border-bottom:1px solid #ddd"><td style="padding:10px">9</td><td style="padding:10px">NORMAL</td><td style="padding:10px"></td></tr>
<tr style="border-bottom:1px solid #ddd;background:#f9f9f9"><td style="padding:10px">10</td><td style="padding:10px">Like Animals</td><td style="padding:10px"></td></tr>
<tr style="border-bottom:1px solid #ddd"><td style="padding:10px">11</td><td style="padding:10px">they don't know 'bout us</td><td style="padding:10px"></td></tr>
<tr style="border-bottom:1px solid #ddd;background:#f9f9f9"><td style="padding:10px">12</td><td style="padding:10px">One More Night</td><td style="padding:10px"></td></tr>
<tr style="border-bottom:1px solid #ddd"><td style="padding:10px">13</td><td style="padding:10px">Please</td><td style="padding:10px"></td></tr>
<tr><td style="padding:10px">14</td><td style="padding:10px">Into the Sun</td><td style="padding:10px">Closing anthem</td></tr>
</table>
</div>

<h2>Visual Symbolism: The ARIRANG Concept and What It Means for "SWIM"</h2>

<p>The ARIRANG album campaign has been rich with visual symbolism, and understanding this context deepens the meaning of "SWIM" significantly.</p>

<h3>The Phonograph Cylinder Metaphor</h3>

<p>In the ARIRANG trailer, <strong>six phonograph cylinders</strong> are visible at the beginning, with a <strong>seventh cylinder</strong> being inserted and played later. Big Hit Music has stated that the album explores "six forms of love," and if each cylinder represents one form, then the seventh cylinder — the one that plays — may represent the synthesis of all six, or perhaps the love that encompasses them all.</p>

<p>"SWIM," as Track 7, occupies this pivotal position. On the tracklist graphic, it's the only song highlighted in <strong>black against the red strips</strong> of the other 13 tracks. This visual distinction underscores its role as the thematic center of the album.</p>

<h3>Water as a Recurring BTS Motif</h3>

<p>Water has appeared throughout BTS's discography as a symbol of both danger and salvation:</p>

<ul>
<li><strong>"Sea" (2017)</strong> — A hidden track about finding hope within despair, where the desert and ocean coexist in the same landscape</li>
<li><strong>"Whalien 52" (2015)</strong> — About a whale that sings at 52 Hz, a frequency no other whale can hear, representing isolation</li>
<li><strong>"<a href="https://rhythmicaleskimo.com/bts-spring-day-%eb%b4%84%eb%82%a0-lyrics-meaning-the-deepest-k-pop-song-ever-written/">Spring Day</a>" (2017)</strong> — Features imagery of snow and melting ice, water as the passage of time and grief</li>
<li><strong>"<a href="https://rhythmicaleskimo.com/bts-black-swan-lyrics-meaning-when-music-becomes-your-first-death/">Black Swan</a>" (2020)</strong> — The music video features an underwater sequence representing artistic death and rebirth</li>
</ul>

<p>"SWIM" brings this water motif to its most direct expression. Where previous songs used water as a backdrop or secondary symbol, "SWIM" makes it the entire framework. The evolution from "Sea" (observing the water) to "SWIM" (actively moving through it) mirrors BTS's own growth from observers of their success to active participants in their own narrative.</p>

<h3>Connection to "Fake Love" and "Blood Sweat & Tears"</h3>

<p>The thematic arc from <a href="https://rhythmicaleskimo.com/bts-fake-love-lyrics-meaning-the-pain-of-erasing-yourself-to-be-loved/">"Fake Love"</a> (2018) to "SWIM" (2026) is particularly striking. "Fake Love" was about drowning in inauthentic love — losing yourself to meet someone else's expectations. "SWIM" inverts this entirely: it's about finding authentic motion through genuine self-acceptance.</p>

<p>Similarly, <a href="https://rhythmicaleskimo.com/bts-blood-sweat-tears-lyrics-meaning-demian-abraxas-the-art-of-temptation/">"Blood Sweat & Tears"</a> (2016) explored the temptation to sacrifice everything for beauty and art. "SWIM" suggests a healthier relationship with ambition — moving forward not through self-sacrifice but through self-preservation.</p>

<h2>Cultural Context: Why BTS Chose "SWIM" as the ARIRANG Lead Single</h2>

<h3>The Post-Military Reunion Context</h3>

<p>Every BTS member completed their mandatory military service between 2022 and 2025, making ARIRANG their first group release in over three years. The choice of "SWIM" as the lead single carries enormous symbolic weight.</p>

<p>Military service in South Korea is a universal male experience, but it's also a deeply isolating one. For 18 months, each member was separated from the group dynamic that had defined their identity since 2013. "SWIM" can be read as a post-reunion statement: <em>we've all been swimming separately, and now we're back in the same ocean.</em></p>

<h3>The ARIRANG Connection</h3>

<p>The album title itself — ARIRANG — references Korea's most iconic folk song, a tune about separation and longing that has been sung for centuries. Big Hit Music stated that ARIRANG <strong>"captures BTS' identity as a group that began in Korea."</strong></p>

<p>By naming their comeback album after this cultural touchstone and leading with "SWIM," BTS draws a line between personal resilience and national identity. Arirang is fundamentally about crossing a hill (the "arirang pass") — a journey that requires effort and perseverance. "SWIM" transposes this journey from land to water, modernizing the metaphor while preserving its emotional core.</p>

<p>For fans planning to experience this music live, BTS will perform "SWIM" for the first time at their <a href="https://rhythmicaleskimo.com/bts-arirang-world-tour-2026-complete-city-by-city-date-guide-and-how-to-get-tickets/">ARIRANG World Tour 2026</a>, which kicks off shortly after the album release. The <a href="https://rhythmicaleskimo.com/bts-arirang-album-the-cultural-meaning-behind-every-song-han-heung-and-600-years-of-korean-soul/">complete cultural analysis of every ARIRANG track</a> provides deeper context for understanding the album's thematic architecture.</p>

<h3>The Songwriting Sessions: LA, Summer 2025</h3>

<p>Reports indicate that the BTS members held songwriting sessions in Los Angeles during the summer of 2025, working alongside the album's roster of international producers. These sessions reportedly took place as the final members were completing or had just completed their military service.</p>

<p>The LA sessions are significant because they represent BTS choosing to create outside of Korea — in a neutral space, away from the pressures and expectations of the Korean entertainment industry. This geographic distance may have contributed to "SWIM"'s thematic freedom, its willingness to reject the conventional comeback formula.</p>

<h2>How "SWIM" Compares to Other BTS Title Tracks</h2>

<h3>A Departure from the BTS Formula</h3>

<p>BTS title tracks have traditionally followed a pattern: high-energy choreography, dramatic music videos, and lyrics that oscillate between personal vulnerability and anthemic declaration. "SWIM" appears to break this pattern in several ways:</p>

<ul>
<li><strong>Tempo:</strong> "Upbeat alternative pop" suggests a mid-tempo groove rather than the high-BPM energy of tracks like "Butter" or "Dynamite"</li>
<li><strong>Message:</strong> Instead of "we will overcome," the message is "I choose to continue" — a subtle but crucial distinction</li>
<li><strong>Production style:</strong> Tyler Spry and Leclair's involvement suggests a more organic, less maximalist sound than previous title tracks</li>
<li><strong>Emotional register:</strong> The song operates in a register of quiet determination rather than explosive emotion</li>
</ul>

<h3>Where "SWIM" Sits in the BTS Emotional Spectrum</h3>

<p>If we map BTS's title tracks on a spectrum from "aggressive defiance" to "gentle acceptance," "SWIM" sits firmly at the gentle end — perhaps the furthest BTS has ever pushed in this direction for a lead single. This is the maturity of seven men in their late twenties and early thirties who have experienced both the highest highs and the most isolating lows of public life.</p>

<p>The closest comparison might be "<a href="https://rhythmicaleskimo.com/bts-spring-day-%eb%b4%84%eb%82%a0-lyrics-meaning-the-deepest-k-pop-song-ever-written/">Spring Day</a>," which also operated in a register of gentle longing. But where "Spring Day" was about waiting and missing, "SWIM" is about moving and choosing. It's the active counterpart to "Spring Day"'s passive grief.</p>

<h2>What "SWIM" Means for ARMY: A Fan's Perspective</h2>

<p>For ARMY — BTS's dedicated global fandom — "SWIM" arrives at a uniquely emotional moment. The three-year wait during military service was the longest period of BTS inactivity since their 2013 debut. Many fans have described the wait in terms that mirror the song's water metaphor: treading water, staying afloat, waiting for the tide to turn.</p>

<p>"SWIM" validates this experience. It says that the waiting — the treading — was not wasted time. It was its own form of swimming. The song offers ARMY not just entertainment but emotional recognition, a quality that has always distinguished BTS from their peers.</p>

<p>For those wanting to deepen their connection to BTS's Korean roots, learning <a href="https://rhythmicaleskimo.com/25-essential-korean-phrases-every-bts-fan-needs-for-the-arirang-world-tour-2026/">essential Korean phrases for the ARIRANG tour</a> can transform the concert experience from observation to participation.</p>

<h3>The Music Video: What We Know So Far</h3>

<p>While the full music video hasn't been released as of this writing (March 15, 2026), the ARIRANG trailer and concept photos provide substantial clues about the visual direction.</p>

<p>The trailer's phonograph cylinder concept suggests the MV may incorporate vintage or analog visual elements — a departure from the CGI-heavy productions of recent K-pop. The black-against-red color coding of "SWIM" on the tracklist graphic hints at a visually stark aesthetic, possibly featuring high-contrast cinematography.</p>

<p>Given the water metaphor, expect stunning aquatic visuals — but knowing BTS's creative team, don't expect literal ocean footage. Instead, look for abstract representations of water: flowing fabrics, liquid-like choreography, or the play of light through transparent surfaces.</p>

<h2>Recommended BTS Albums and Merch</h2>

<p>If "SWIM" has reignited your passion for BTS's discography, here are essential items to complete your collection:</p>

<ul>
<li><strong>ARIRANG Album (All Versions)</strong> — Available for pre-order at major retailers. The physical album includes photobooks and exclusive photocards. <a href="https://www.amazon.com/s?k=BTS+ARIRANG+album&tag=rhythmicalesk-20" target="_blank" rel="nofollow noopener">Shop BTS ARIRANG on Amazon</a></li>
<li><strong>BTS Proof (Anthology Album)</strong> — The perfect companion to ARIRANG, collecting the best of BTS's first chapter. <a href="https://www.amazon.com/s?k=BTS+Proof+album&tag=rhythmicalesk-20" target="_blank" rel="nofollow noopener">Shop BTS Proof on Amazon</a></li>
<li><strong>ARMY Bomb (Official Light Stick)</strong> — Essential for the upcoming <a href="https://rhythmicaleskimo.com/bts-arirang-world-tour-2026-complete-city-by-city-date-guide-and-how-to-get-tickets/">ARIRANG World Tour</a>. <a href="https://www.amazon.com/s?k=BTS+ARMY+bomb+lightstick&tag=rhythmicalesk-20" target="_blank" rel="nofollow noopener">Shop ARMY Bomb on Amazon</a></li>
</ul>

<h2>Frequently Asked Questions</h2>

<h3>What is the meaning of BTS "SWIM"?</h3>
<p>"SWIM" is about the resolve to keep moving forward through life's turbulent waves. Rather than fighting against difficulty, the song frames choosing to move at your own pace as an expression of love for life itself. RM leads the songwriting, and the track serves as a metaphor for resilience and self-acceptance.</p>

<h3>Who produced BTS "SWIM"?</h3>
<p>"SWIM" was produced by Tyler Spry and Leclair, with RM as the primary songwriter. The song is Track 7 on the ARIRANG album, which features an international roster of producers including Diplo, Kevin Parker (Tame Impala), and Ryan Tedder.</p>

<h3>When does the BTS ARIRANG album release?</h3>
<p>ARIRANG releases worldwide on March 20, 2026. It is BTS's fifth studio album (tenth overall) and their first group release in over three years, following the completion of all members' military service.</p>

<h3>How does "SWIM" connect to other BTS water-themed songs?</h3>
<p>"SWIM" continues a water motif that runs through BTS's discography, including "Sea" (2017), "Whalien 52" (2015), and underwater imagery in the "Black Swan" music video. While "Sea" was about observing the water, "SWIM" is about actively moving through it — representing BTS's evolution from observers to active participants in their own narrative.</p>

<h3>What genre is BTS "SWIM"?</h3>
<p>Big Hit Music describes "SWIM" as an "upbeat alternative pop" track. Based on the producers involved (Tyler Spry and Leclair), the song likely blends organic instrumentation with electronic textures, creating a mid-tempo groove that differs from BTS's typically high-energy title tracks.</p>

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is the meaning of BTS SWIM?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "SWIM is about the resolve to keep moving forward through life's turbulent waves. Rather than fighting against difficulty, the song frames choosing to move at your own pace as an expression of love for life itself. RM leads the songwriting, and the track serves as a metaphor for resilience and self-acceptance."
      }
    },
    {
      "@type": "Question",
      "name": "Who produced BTS SWIM?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "SWIM was produced by Tyler Spry and Leclair, with RM as the primary songwriter. The song is Track 7 on the ARIRANG album, which features producers including Diplo, Kevin Parker (Tame Impala), and Ryan Tedder."
      }
    },
    {
      "@type": "Question",
      "name": "When does the BTS ARIRANG album release?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "ARIRANG releases worldwide on March 20, 2026. It is BTS's fifth studio album and their first group release in over three years, following the completion of all members' military service."
      }
    },
    {
      "@type": "Question",
      "name": "How does SWIM connect to other BTS water-themed songs?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "SWIM continues a water motif through BTS's discography, including Sea (2017), Whalien 52 (2015), and underwater imagery in the Black Swan music video. While Sea was about observing the water, SWIM is about actively moving through it."
      }
    },
    {
      "@type": "Question",
      "name": "What genre is BTS SWIM?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Big Hit Music describes SWIM as an upbeat alternative pop track. Based on the producers involved (Tyler Spry and Leclair), the song likely blends organic instrumentation with electronic textures, creating a mid-tempo groove."
      }
    }
  ]
}
</script>

</article>
"""

# ─── Post 2: BTS Free Concert Seoul ───────────────────────────────────

post2_html = """
<article>

<p>On March 21, 2026, BTS will take the stage at <strong>Gwanghwamun Square</strong> in central Seoul for <strong>"BTS THE COMEBACK LIVE | ARIRANG"</strong> — a free concert marking their first live performance since completing military service. With an estimated <strong>260,000 fans</strong> expected to flood the area, this is shaping up to be the largest free K-pop concert in history.</p>

<p>Whether you won the ticket lottery, plan to watch from Seoul Plaza's overflow screens, or are still figuring out how to get there, this guide covers absolutely everything you need to know — from transportation logistics and accommodation strategies to nearby restaurants, essential Korean phrases, and what to pack for a March night in Seoul.</p>

<h2>Event Details: Everything Confirmed About the BTS Gwanghwamun Concert</h2>

<div style="overflow-x:auto;max-width:100%">
<table style="width:100%;border-collapse:collapse;margin:20px 0">
<tr style="background:#1a1a2e;color:white"><th style="padding:12px;text-align:left;width:35%">Detail</th><th style="padding:12px;text-align:left">Information</th></tr>
<tr style="border-bottom:1px solid #ddd"><td style="padding:10px"><strong>Official Name</strong></td><td style="padding:10px">BTS THE COMEBACK LIVE | ARIRANG</td></tr>
<tr style="border-bottom:1px solid #ddd;background:#f9f9f9"><td style="padding:10px"><strong>Date</strong></td><td style="padding:10px">March 21, 2026 (Saturday)</td></tr>
<tr style="border-bottom:1px solid #ddd"><td style="padding:10px"><strong>Time</strong></td><td style="padding:10px">8:00 PM KST</td></tr>
<tr style="border-bottom:1px solid #ddd;background:#f9f9f9"><td style="padding:10px"><strong>Duration</strong></td><td style="padding:10px">Approximately 1 hour</td></tr>
<tr style="border-bottom:1px solid #ddd"><td style="padding:10px"><strong>Location</strong></td><td style="padding:10px">Gwanghwamun Square, Jongno-gu, Seoul</td></tr>
<tr style="border-bottom:1px solid #ddd;background:#f9f9f9"><td style="padding:10px"><strong>Main Venue Capacity</strong></td><td style="padding:10px">15,000 (ticketed area)</td></tr>
<tr style="border-bottom:1px solid #ddd"><td style="padding:10px"><strong>Overflow Viewing</strong></td><td style="padding:10px">Seoul Plaza — 13,000 additional via large screens</td></tr>
<tr style="border-bottom:1px solid #ddd;background:#f9f9f9"><td style="padding:10px"><strong>Total Expected Crowd</strong></td><td style="padding:10px">~260,000 across the area</td></tr>
<tr style="border-bottom:1px solid #ddd"><td style="padding:10px"><strong>Cost</strong></td><td style="padding:10px">Free (reservation fee applies for lottery winners)</td></tr>
<tr style="border-bottom:1px solid #ddd;background:#f9f9f9"><td style="padding:10px"><strong>Live Stream</strong></td><td style="padding:10px">Weverse Live + Netflix (32 languages, 190 countries)</td></tr>
<tr><td style="padding:10px"><strong>Sponsor</strong></td><td style="padding:10px">Seoul Metropolitan Government (official sponsorship)</td></tr>
</table>
</div>

<p>This concert takes place just <strong>one day after</strong> the release of BTS's ARIRANG album (March 20), making it the first time fans will hear the new songs performed live. The Seoul Metropolitan Government has officially sponsored the event, deploying comprehensive crowd control, medical support, and multilingual assistance infrastructure.</p>

<h3>How the Ticket Lottery Worked</h3>

<p>Access to the main 15,000-capacity viewing area at Gwanghwamun Square was determined through a <strong>raffle (lottery) system</strong> on the NOL World ticketing platform. Here's what the process looked like:</p>

<ul>
<li><strong>Eligibility:</strong> Active ARMY Membership on Weverse required</li>
<li><strong>Platform:</strong> NOL World (world.nol.com) — account creation required</li>
<li><strong>Application Period:</strong> February 16 at 2:00 PM — February 18 at 2:00 PM (KST)</li>
<li><strong>Key Detail:</strong> Applying at any time during the window gave the exact same chance — no first-come advantage</li>
<li><strong>Cost:</strong> Free tickets with a separate reservation fee at booking</li>
</ul>

<p>If you didn't win the lottery, don't despair. The overflow viewing area at Seoul Plaza accommodates an additional 13,000 fans with large-screen broadcasts of the performance. No ticket is required for Seoul Plaza — it's completely open to the public on a first-come, first-served basis.</p>

<h2>How to Get There: Transportation Guide for Gwanghwamun Square</h2>

<p>Getting to and from the concert will be the biggest logistical challenge. The Seoul Metropolitan Government has implemented extensive traffic controls, and several subway stations will be affected. Plan your route carefully.</p>

<h3>From Incheon Airport (ICN)</h3>

<div style="overflow-x:auto;max-width:100%">
<table style="width:100%;border-collapse:collapse;margin:20px 0">
<tr style="background:#1a1a2e;color:white"><th style="padding:12px;text-align:left">Option</th><th style="padding:12px;text-align:left">Route</th><th style="padding:12px;text-align:left">Time</th><th style="padding:12px;text-align:left">Cost</th></tr>
<tr style="border-bottom:1px solid #ddd"><td style="padding:10px"><strong>AREX (Best)</strong></td><td style="padding:10px">Airport → Seoul Station → Subway Line 1 to City Hall → Walk 10 min</td><td style="padding:10px">~70 min</td><td style="padding:10px">₩4,150 (~$3)</td></tr>
<tr style="border-bottom:1px solid #ddd;background:#f9f9f9"><td style="padding:10px"><strong>AREX Express</strong></td><td style="padding:10px">Airport → Seoul Station (non-stop) → Subway or taxi</td><td style="padding:10px">~55 min</td><td style="padding:10px">₩9,500 (~$7)</td></tr>
<tr style="border-bottom:1px solid #ddd"><td style="padding:10px"><strong>Airport Limousine Bus</strong></td><td style="padding:10px">Bus 6015 to Gwanghwamun area</td><td style="padding:10px">~80-100 min</td><td style="padding:10px">₩17,000 (~$12)</td></tr>
<tr><td style="padding:10px"><strong>Taxi</strong></td><td style="padding:10px">Direct to Gwanghwamun (expect traffic)</td><td style="padding:10px">~60-90 min</td><td style="padding:10px">₩70,000-100,000 (~$50-70)</td></tr>
</table>
</div>

<h3>Subway: Critical Station Bypass Information</h3>

<p><strong>Warning:</strong> Seoul Metro has announced that several stations near the venue will <strong>bypass without stopping</strong> on concert day:</p>

<ul>
<li><strong>Gwanghwamun Station (Line 5)</strong> — BYPASS, no stop</li>
<li><strong>Gyeongbokgung Station (Line 3)</strong> — BYPASS, no stop</li>
<li><strong>City Hall Station (Lines 1 & 2)</strong> — BYPASS, no stop</li>
</ul>

<p>Instead, use these alternative stations and walk:</p>

<ul>
<li><strong>Anguk Station (Line 3)</strong> — 15-minute walk to Gwanghwamun Square</li>
<li><strong>Jonggak Station (Line 1)</strong> — 12-minute walk south to the venue</li>
<li><strong>Seodaemun Station (Line 5)</strong> — 15-minute walk east</li>
<li><strong>Euljiro 1-ga Station (Line 2)</strong> — 18-minute walk northwest</li>
</ul>

<p><strong>Post-Concert Transport:</strong> Seoul Metro will run <strong>12 temporary trains with 24 additional runs</strong> on Lines 2, 3, and 5 after the concert ends. Expect extremely crowded conditions — consider waiting 30-60 minutes after the concert ends before heading to the subway.</p>

<h3>Taxi and Ride-Hailing Tips</h3>

<p>Do NOT plan to use a taxi immediately after the concert. With 260,000 people dispersing simultaneously, the surrounding roads will be gridlocked. If you must take a taxi:</p>

<ul>
<li>Walk at least 1 km away from the venue before hailing</li>
<li>Use <strong>Kakao T</strong> app (Korea's Uber equivalent) — download and set up before concert day</li>
<li>Consider walking to Myeong-dong area (20-minute walk south) for easier taxi access</li>
<li>International taxis can be called via the <strong>1330 Korea Travel Hotline</strong></li>
</ul>

<h2>Where to Stay: Accommodation Strategy for the BTS Gwanghwamun Concert</h2>

<h3>The Price Reality</h3>

<p>Let's be honest about accommodation prices. The BTS effect on Seoul hotel rates has been dramatic:</p>

<div style="overflow-x:auto;max-width:100%">
<table style="width:100%;border-collapse:collapse;margin:20px 0">
<tr style="background:#1a1a2e;color:white"><th style="padding:12px;text-align:left">Hotel Type</th><th style="padding:12px;text-align:left">Normal Weekend</th><th style="padding:12px;text-align:left">Concert Weekend</th><th style="padding:12px;text-align:left">Price Increase</th></tr>
<tr style="border-bottom:1px solid #ddd"><td style="padding:10px">4-Star Gwanghwamun</td><td style="padding:10px">₩200,000 (~$139)</td><td style="padding:10px">₩600,000+ (~$417+)</td><td style="padding:10px">+200%</td></tr>
<tr style="border-bottom:1px solid #ddd;background:#f9f9f9"><td style="padding:10px">Shilla Stay Gwanghwamun</td><td style="padding:10px">₩365,000 (~$254)</td><td style="padding:10px">₩627,000 (~$436)</td><td style="padding:10px">+72%</td></tr>
<tr style="border-bottom:1px solid #ddd"><td style="padding:10px">Mid-Range Myeong-dong</td><td style="padding:10px">₩120,000 (~$83)</td><td style="padding:10px">₩300,000+ (~$209+)</td><td style="padding:10px">+150%</td></tr>
<tr><td style="padding:10px">Budget Guesthouse</td><td style="padding:10px">₩40,000 (~$28)</td><td style="padding:10px">₩100,000+ (~$70+)</td><td style="padding:10px">+150%</td></tr>
</table>
</div>

<p>The Seoul Metropolitan Government has <strong>strengthened price monitoring</strong> across lodging facilities to prevent unfair surcharges, but market-rate increases are still substantial.</p>

<h3>Smart Accommodation Strategies</h3>

<p><strong>Option 1: Stay in a Nearby Neighborhood (Best Value)</strong></p>
<p>Instead of paying premium Gwanghwamun prices, consider these areas — all within 20-30 minutes by subway:</p>

<ul>
<li><strong>Hongdae Area</strong> — Vibrant, affordable, great nightlife for after the concert. Budget hotels from ₩60,000-80,000</li>
<li><strong>Dongdaemun</strong> — Shopping district with many mid-range hotels. 20 minutes by subway to Gwanghwamun</li>
<li><strong>Itaewon/Hannam</strong> — International-friendly area with English-speaking staff. Walking distance from alternative subway stations</li>
<li><strong>Mapo Area</strong> — Close to Gwanghwamun via Line 5, significantly cheaper hotels</li>
</ul>

<p><strong>Option 2: Jjimjilbang (Korean Spa)</strong></p>
<p>For the truly budget-conscious, Seoul's 24-hour jjimjilbangs (Korean spas) offer overnight stays with sleeping areas, showers, and saunas for ₩12,000-20,000 (~$8-14). Popular options near the venue include Dragon Hill Spa in Yongsan and Siloam Sauna near Seoul Station.</p>

<p><strong>Option 3: Book NOW for the ARIRANG World Tour Dates</strong></p>
<p>If you missed the Gwanghwamun concert, BTS's <a href="https://rhythmicaleskimo.com/bts-arirang-world-tour-2026-complete-city-by-city-date-guide-and-how-to-get-tickets/">ARIRANG World Tour 2026</a> will visit cities worldwide. Book accommodation early to avoid the same price surge.</p>

<h2>Nearby Restaurants and Food: What to Eat Before the Concert</h2>

<p>The Gwanghwamun area is one of Seoul's culinary hotspots. Arrive early and explore these dining options before the concert. For a deeper dive into Seoul's food scene, check out our guide to <a href="https://rhythmicaleskimo.com/seouls-hidden-alley-restaurants-7-places-only-locals-know-about/">Seoul's hidden alley restaurants</a>.</p>

<h3>Korean BBQ and Traditional Cuisine</h3>

<ul>
<li><strong>Songchu Kamakoru IN URBAN Gwanghwamun</strong> — Legendary Korean BBQ since 1993. Their galbi-tang (short rib soup) is perfect for a cold March evening. Budget: ₩15,000-25,000 per person</li>
<li><strong>Gwanghwaro</strong> — Unique pork restaurant where whole belly is grilled at 500°C for 2 minutes. An unforgettable textural experience. Budget: ₩18,000-30,000 per person</li>
<li><strong>Tosokchon Samgyetang</strong> — A 10-minute walk north, this iconic restaurant serves ginseng chicken soup (samgyetang) — the ultimate Korean comfort food. Expect a 30-60 minute wait. Budget: ₩17,000 per person</li>
</ul>

<h3>Quick Bites for Time-Pressed Fans</h3>

<ul>
<li><strong>Insadong Street Food</strong> — 10-minute walk east. Hotteok (sweet pancakes), tteokbokki (spicy rice cakes), and ssiat hotteok (seed-filled pancakes). Budget: ₩3,000-8,000</li>
<li><strong>Convenience Store Strategy</strong> — GS25 and CU stores near Gwanghwamun offer surprisingly good onigiri, kimbap, and hot foods. Perfect for eating while waiting in line. Budget: ₩2,000-5,000</li>
<li><strong>Seochon Hanok Village Cafes</strong> — West of Gyeongbokgung Palace. Charming traditional-house cafes with excellent coffee and Korean desserts. Perfect for a pre-concert warmup. Budget: ₩5,000-10,000</li>
</ul>

<h3>International Cuisine Options</h3>

<ul>
<li><strong>Osteria Sotti</strong> — Authentic Neapolitan pizza, a welcome option if you're craving non-Korean food. Budget: ₩15,000-25,000</li>
<li><strong>Mutan Gwanghwamun</strong> — Chinese restaurant with private rooms, 5-minute walk from Gwanghwamun Station. Budget: ₩12,000-20,000</li>
<li><strong>Okawa Sushi</strong> — Hidden basement sushi spot next to Gwanghwamun Station. Affordable omakase-style experience. Budget: ₩20,000-40,000</li>
</ul>

<h2>What to Pack: Essential Items for a March Concert in Seoul</h2>

<h3>Weather Preparation</h3>

<p>March 21 in Seoul is early spring — temperatures typically range from <strong>2°C to 12°C (36°F to 54°F)</strong>. Standing outdoors for several hours (including queue time) means you need to prepare for cold conditions:</p>

<ul>
<li><strong>Thermal base layer</strong> — Heattech or similar moisture-wicking thermal underwear. <a href="https://www.amazon.com/s?k=thermal+base+layer+lightweight&tag=rhythmicalesk-20" target="_blank" rel="nofollow noopener">Shop thermal layers on Amazon</a></li>
<li><strong>Down jacket</strong> — Packable puffer jacket that you can compress if the temperature rises</li>
<li><strong>Hand warmers</strong> — Korean convenience stores sell them (핫팩, "hot pack"), or bring your own. <a href="https://www.amazon.com/s?k=hand+warmers+disposable&tag=rhythmicalesk-20" target="_blank" rel="nofollow noopener">Shop hand warmers on Amazon</a></li>
<li><strong>Beanie and gloves</strong> — Nighttime temperatures can drop below 5°C</li>
<li><strong>Comfortable shoes</strong> — You'll be standing for hours and walking significant distances from alternative subway stations</li>
</ul>

<h3>Concert Essentials</h3>

<ul>
<li><strong>ARMY Bomb (Official Light Stick)</strong> — Syncs with the concert via Bluetooth. Make sure it's fully charged. <a href="https://www.amazon.com/s?k=BTS+ARMY+bomb+lightstick&tag=rhythmicalesk-20" target="_blank" rel="nofollow noopener">Shop ARMY Bomb on Amazon</a></li>
<li><strong>Portable battery pack</strong> — Your phone will drain fast from photos, videos, and navigation. Bring a 20,000mAh+ pack. <a href="https://www.amazon.com/s?k=portable+charger+20000mah&tag=rhythmicalesk-20" target="_blank" rel="nofollow noopener">Shop portable chargers on Amazon</a></li>
<li><strong>Clear bag</strong> — Security will be tight; a transparent bag speeds up entry</li>
<li><strong>Printed ticket/QR code</strong> — Don't rely solely on your phone. Screenshot and print your lottery confirmation</li>
<li><strong>Snacks and water</strong> — Standing in the queue for hours requires sustenance</li>
</ul>

<h3>Tech Setup</h3>

<ul>
<li><strong>Weverse app</strong> — Download and log in before concert day. Concert updates and post-show content will appear here</li>
<li><strong>Kakao T app</strong> — Korea's ride-hailing app. Set up with an international card before you need it</li>
<li><strong>Naver Map or Kakao Map</strong> — Google Maps works in Korea but Naver/Kakao are significantly more accurate for walking directions and public transit</li>
<li><strong>T-money card</strong> — Korea's transit card. Available at convenience stores and subway stations. Load at least ₩20,000</li>
</ul>

<h2>Essential Korean Phrases for Concert Day</h2>

<p>Knowing a few Korean phrases will dramatically improve your experience. For a comprehensive guide, see our article on <a href="https://rhythmicaleskimo.com/25-essential-korean-phrases-every-bts-fan-needs-for-the-arirang-world-tour-2026/">25 essential Korean phrases for BTS fans</a>, and if you want to start reading Korean signs and menus, our <a href="https://rhythmicaleskimo.com/how-to-read-korean-hangul-in-30-minutes-the-fastest-method-that-actually-works/">30-minute Hangul guide</a> is the fastest way to learn.</p>

<div style="overflow-x:auto;max-width:100%">
<table style="width:100%;border-collapse:collapse;margin:20px 0">
<tr style="background:#1a1a2e;color:white"><th style="padding:12px;text-align:left">Situation</th><th style="padding:12px;text-align:left">Korean</th><th style="padding:12px;text-align:left">Romanization</th><th style="padding:12px;text-align:left">Meaning</th></tr>
<tr style="border-bottom:1px solid #ddd"><td style="padding:10px">Asking directions</td><td style="padding:10px">광화문 광장 어디예요?</td><td style="padding:10px">Gwanghwamun gwangjang eodiyeyo?</td><td style="padding:10px">Where is Gwanghwamun Square?</td></tr>
<tr style="border-bottom:1px solid #ddd;background:#f9f9f9"><td style="padding:10px">Finding entrance</td><td style="padding:10px">입구가 어디예요?</td><td style="padding:10px">Ipguga eodiyeyo?</td><td style="padding:10px">Where is the entrance?</td></tr>
<tr style="border-bottom:1px solid #ddd"><td style="padding:10px">Bathroom</td><td style="padding:10px">화장실 어디예요?</td><td style="padding:10px">Hwajangsil eodiyeyo?</td><td style="padding:10px">Where is the restroom?</td></tr>
<tr style="border-bottom:1px solid #ddd;background:#f9f9f9"><td style="padding:10px">Emergency</td><td style="padding:10px">도와주세요!</td><td style="padding:10px">Dowajuseyo!</td><td style="padding:10px">Please help me!</td></tr>
<tr style="border-bottom:1px solid #ddd"><td style="padding:10px">Subway</td><td style="padding:10px">지하철역 어디예요?</td><td style="padding:10px">Jihacheol-yeok eodiyeyo?</td><td style="padding:10px">Where is the subway station?</td></tr>
<tr style="border-bottom:1px solid #ddd;background:#f9f9f9"><td style="padding:10px">Ordering food</td><td style="padding:10px">이거 주세요</td><td style="padding:10px">Igeo juseyo</td><td style="padding:10px">This one, please</td></tr>
<tr style="border-bottom:1px solid #ddd"><td style="padding:10px">Thank you</td><td style="padding:10px">감사합니다</td><td style="padding:10px">Gamsahamnida</td><td style="padding:10px">Thank you (formal)</td></tr>
<tr style="border-bottom:1px solid #ddd;background:#f9f9f9"><td style="padding:10px">Cheering BTS</td><td style="padding:10px">방탄소년단 사랑해요!</td><td style="padding:10px">Bangtan Sonyeondan saranghaeyo!</td><td style="padding:10px">BTS, I love you!</td></tr>
<tr><td style="padding:10px">Photo request</td><td style="padding:10px">사진 찍어주세요</td><td style="padding:10px">Sajin jjigeo juseyo</td><td style="padding:10px">Please take my photo</td></tr>
</table>
</div>

<h2>Watching from Home: Netflix and Weverse Live Stream</h2>

<p>If you can't make it to Seoul, BTS has ensured global accessibility for this historic comeback:</p>

<ul>
<li><strong>Netflix</strong> — Live simulcast available in <strong>190 countries</strong> with subtitles in <strong>32 languages</strong>. No additional subscription required beyond your standard Netflix plan</li>
<li><strong>Weverse Live</strong> — Free live stream on the Weverse platform. ARMY Membership may unlock additional camera angles and backstage content</li>
<li><strong>Watch Party Tips</strong> — Organize or join local ARMY watch parties. Many K-pop cafes and venues worldwide will host screenings</li>
</ul>

<p>For the best home viewing experience:</p>
<ul>
<li>Test your internet connection beforehand — stream quality requires at least 25 Mbps for 4K</li>
<li>Connect to a large screen via HDMI or casting</li>
<li>Prepare your ARMY Bomb — it can sync even during live streams via Bluetooth</li>
<li>Join the Weverse fan community for real-time reactions and translations</li>
</ul>

<h2>Safety and Security: What Seoul Is Doing</h2>

<p>The Seoul Metropolitan Government is treating this concert as a major public safety event. Here's what's been announced:</p>

<ul>
<li><strong>Dedicated safety website</strong> — Launched March 12, providing real-time updates on traffic control zones, subway detours, restroom locations, and medical clinic positions</li>
<li><strong>Medical clinics on-site</strong> — Multiple first-aid stations throughout the venue area</li>
<li><strong>Multilingual information centers</strong> — Guidance available in Korean, English, Chinese, and Japanese</li>
<li><strong>1330 Korea Travel Hotline</strong> — 24/7 multilingual tourist assistance. Call if you're lost, need translation help, or encounter any issues</li>
<li><strong>Enhanced police presence</strong> — Seoul has toughened security measures specifically for this event</li>
</ul>

<h3>Personal Safety Tips</h3>

<ul>
<li><strong>Share your location</strong> — Use KakaoTalk or WhatsApp to share live location with friends</li>
<li><strong>Designate a meeting point</strong> — If attending with a group, agree on a reunion spot in case you get separated. Sejong statue at the south end of the square is a well-known landmark</li>
<li><strong>Stay hydrated but plan bathroom trips</strong> — Portable restrooms will be available but expect long lines</li>
<li><strong>Know the exit routes</strong> — Familiarize yourself with the square's layout before the event</li>
<li><strong>Keep valuables secure</strong> — Large crowds attract pickpockets. Use a crossbody bag or money belt</li>
</ul>

<h2>Making the Most of Your Seoul Trip: Before and After the Concert</h2>

<p>If you're traveling to Seoul specifically for the concert, don't miss the opportunity to explore. The Gwanghwamun area is surrounded by Seoul's most iconic landmarks.</p>

<h3>Pre-Concert Activities (March 20-21 Daytime)</h3>

<ul>
<li><strong>Gyeongbokgung Palace</strong> — Korea's main royal palace, directly north of Gwanghwamun Square. Wear hanbok (traditional clothing) for free entry. Opens 9 AM - 6 PM</li>
<li><strong>National Museum of Korea</strong> — Free admission, world-class collection. Take the subway to Ichon Station</li>
<li><strong>Bukchon Hanok Village</strong> — Traditional Korean houses on a hillside, 15-minute walk from Anguk Station. Best visited in the morning before crowds</li>
<li><strong>HYBE Insight Museum</strong> — BTS's label headquarters features an immersive K-pop experience. For the full guide, read our <a href="https://rhythmicaleskimo.com/hybe-insight-museum-big-4-entertainment-tours-the-ultimate-k-pop-pilgrimage-in-seoul/">HYBE Insight and Big 4 entertainment tours article</a></li>
</ul>

<h3>Post-Concert (March 22+)</h3>

<ul>
<li><strong>BTS-themed locations</strong> — Visit the filming locations from BTS music videos scattered across Seoul</li>
<li><strong>K-pop merchandise shopping</strong> — Myeong-dong and Hongdae are packed with K-pop stores. BTS ARIRANG merchandise will be available at pop-up stores</li>
<li><strong>DMZ Tour</strong> — A unique day trip to the Korean Demilitarized Zone, bookable through most hotels</li>
<li><strong>Korean cooking class</strong> — Learn to make bibimbap or kimchi. Classes available in English in the Insadong and Jongno areas</li>
</ul>

<h2>Frequently Asked Questions</h2>

<h3>Is the BTS Gwanghwamun concert really free?</h3>
<p>Yes, the concert itself is free. However, access to the main 15,000-capacity viewing area at Gwanghwamun Square was determined by a ticket lottery through NOL World, and winners paid a small reservation fee. The overflow viewing area at Seoul Plaza (13,000 capacity) is open to the public without any ticket. The concert is also streamed for free on Weverse Live and available on Netflix worldwide.</p>

<h3>Can I still attend without a lottery ticket?</h3>
<p>Yes. Seoul Plaza, adjacent to Gwanghwamun Square, will have large screens broadcasting the concert live for an additional 13,000 fans. This area is first-come, first-served with no ticket required. Additionally, the surrounding streets will likely have visibility, though viewing quality will vary.</p>

<h3>What time should I arrive at Gwanghwamun Square?</h3>
<p>For lottery ticket holders, gates open several hours before the 8 PM start time. Arrive at least 3-4 hours early for the best experience. For Seoul Plaza overflow viewing, arriving by 4-5 PM is recommended to secure a good spot. Many fans will camp out from the early morning.</p>

<h3>Will there be BTS merchandise available at the venue?</h3>
<p>Official ARIRANG merchandise is expected to be available at pop-up stores near the venue. Arrive early if you want to purchase before items sell out. Bring cash (Korean won) as backup — card machines can fail in crowded conditions.</p>

<h3>What songs will BTS perform at the Gwanghwamun concert?</h3>
<p>The setlist hasn't been officially announced, but expect a mix of new ARIRANG tracks (including the lead single "SWIM") and classic BTS hits. The concert duration is approximately one hour, so expect around 8-10 songs.</p>

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Is the BTS Gwanghwamun concert really free?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes, the concert itself is free. Access to the main 15,000-capacity viewing area was determined by a ticket lottery through NOL World with a small reservation fee. The overflow viewing at Seoul Plaza (13,000 capacity) is open to the public. The concert also streams free on Weverse Live and Netflix worldwide."
      }
    },
    {
      "@type": "Question",
      "name": "Can I still attend without a lottery ticket?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes. Seoul Plaza will have large screens broadcasting the concert live for 13,000 fans on a first-come, first-served basis. No ticket required."
      }
    },
    {
      "@type": "Question",
      "name": "What time should I arrive at Gwanghwamun Square?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "For lottery ticket holders, arrive at least 3-4 hours early. For Seoul Plaza overflow, arriving by 4-5 PM is recommended. Many fans camp out from early morning."
      }
    },
    {
      "@type": "Question",
      "name": "Will there be BTS merchandise at the venue?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Official ARIRANG merchandise is expected at pop-up stores near the venue. Arrive early and bring cash as backup since card machines can fail in crowds."
      }
    },
    {
      "@type": "Question",
      "name": "What songs will BTS perform at the Gwanghwamun concert?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "The setlist hasn't been officially announced, but expect new ARIRANG tracks including SWIM plus classic BTS hits. The concert is approximately one hour, so expect 8-10 songs."
      }
    }
  ]
}
</script>

</article>
"""

# ─── Login & Publish ───────────────────────────────────────────────────

print("Logging in...")
s, h = e.login()
print("  Login successful")

cat_id = e.get_or_create_category(s, h, "K-Pop", "k-pop")
print(f"  Category K-Pop: ID {cat_id}")

# Publish Post 1: SWIM
print("\n--- Publishing Post 1: BTS SWIM ---")
data1 = {
    "title": "BTS SWIM Lyrics Meaning & Music Video Analysis: ARIRANG Lead Single Deep Dive",
    "content": post1_html,
    "status": "publish",
    "categories": [cat_id],
    "excerpt": "Complete analysis of BTS's SWIM — the lead single from their 2026 ARIRANG album. Deep dive into lyrics meaning, musical architecture, visual symbolism, and how it connects to BTS's decade-long artistic journey."
}
r1 = s.post(f"{e.REST}/posts", headers=h, json=data1)
if r1.status_code == 201:
    pid1 = r1.json()["id"]
    link1 = r1.json()["link"]
    print(f"  Published: ID:{pid1} → {link1}")

    # Tags
    tags1 = e.get_or_create_tags(s, h, ["BTS", "SWIM", "ARIRANG", "K-Pop", "Lyrics Analysis", "BTS Comeback 2026"])
    if tags1:
        s.post(f"{e.REST}/posts/{pid1}", headers=h, json={"tags": tags1})

    # Word count
    import re as re2
    wc1 = len(re2.sub(r'<[^>]+>', '', post1_html).split())
    print(f"  Word count: {wc1}")
else:
    print(f"  FAILED: {r1.status_code} {r1.text[:200]}")
    pid1 = None

# Publish Post 2: Concert Guide
print("\n--- Publishing Post 2: BTS Concert Guide ---")
data2 = {
    "title": "Free BTS Comeback Concert Seoul March 2026: Complete Guide to Attending at Gwanghwamun Square",
    "content": post2_html,
    "status": "publish",
    "categories": [cat_id],
    "excerpt": "Everything you need to know about BTS's free comeback concert at Gwanghwamun Square on March 21, 2026. Transportation, accommodation, restaurants, Korean phrases, packing list, and safety tips."
}
r2 = s.post(f"{e.REST}/posts", headers=h, json=data2)
if r2.status_code == 201:
    pid2 = r2.json()["id"]
    link2 = r2.json()["link"]
    print(f"  Published: ID:{pid2} → {link2}")

    # Tags
    tags2 = e.get_or_create_tags(s, h, ["BTS", "Seoul Concert", "Gwanghwamun", "K-Pop", "BTS Comeback 2026", "Korea Travel"])
    if tags2:
        s.post(f"{e.REST}/posts/{pid2}", headers=h, json={"tags": tags2})

    wc2 = len(re2.sub(r'<[^>]+>', '', post2_html).split())
    print(f"  Word count: {wc2}")
else:
    print(f"  FAILED: {r2.status_code} {r2.text[:200]}")
    pid2 = None

# Upload featured images
print("\n--- Uploading Featured Images ---")
for pid, fname in [(pid1, 'featured_bts_swim.png'), (pid2, 'featured_bts_concert_seoul.png')]:
    if pid:
        with open(f'/Users/choijooyong/wordpress/{fname}', 'rb') as f:
            r = s.post(f"{e.REST}/media",
                      headers={**h, 'Content-Disposition': f'attachment; filename={fname}'},
                      files={'file': (fname, f, 'image/png')})
            if r.status_code == 201:
                media_id = r.json()['id']
                s.post(f"{e.REST}/posts/{pid}", headers=h, json={'featured_media': media_id})
                print(f"  {fname} → Media ID:{media_id} → Post ID:{pid}")
            else:
                print(f"  FAILED uploading {fname}: {r.status_code}")

print("\n=== DONE ===")
print(f"Post 1 Word Count: {wc1 if pid1 else 'N/A'}")
print(f"Post 2 Word Count: {wc2 if pid2 else 'N/A'}")
print(f"Total Words: {(wc1 or 0) + (wc2 or 0)}")
