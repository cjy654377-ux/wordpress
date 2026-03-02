import requests, re, json, os, sys

SITE = "https://rhythmicaleskimo.com"
USER = "cjy654377@gmail.com"
PASS = "Tony2026!!"
BASE = "/Users/choijooyong/projects/워드프레스_생생정보통"
CAT_ID = 149  # World News

s = requests.Session()
s.post(f"{SITE}/wp-login.php", data={
    "log": USER, "pwd": PASS, "wp-submit": "Log In",
    "redirect_to": f"{SITE}/wp-admin/", "testcookie": "1"
}, allow_redirects=True)
admin = s.get(f"{SITE}/wp-admin/post-new.php")
nonce = re.search(r'"nonce":"([a-f0-9]+)"', admin.text).group(1)
H = {"X-WP-Nonce": nonce}

def upload_img(filename):
    path = os.path.join(BASE, filename)
    with open(path, "rb") as f:
        data = f.read()
    slug = filename.replace(".png","")
    r = s.post(f"{SITE}/wp-json/wp/v2/media",
        headers={**H, "Content-Disposition": f"attachment; filename={slug}.png", "Content-Type": "image/png"},
        data=data)
    if r.status_code == 201:
        mid = r.json()["id"]
        print(f"  IMG {filename} -> {mid}")
        return mid
    print(f"  IMG FAIL {filename}: {r.status_code}")
    return 0

def make_tags(names):
    ids = []
    for t in names:
        r = s.post(f"{SITE}/wp-json/wp/v2/tags", headers=H, json={"name": t})
        if r.status_code == 201:
            ids.append(r.json()["id"])
        elif r.status_code == 400:
            tid = r.json().get("data",{}).get("term_id")
            if tid: ids.append(tid)
    return ids

posts = [
    {
        "img": "news_hormuz.png",
        "title": "Strait of Hormuz Shutdown: How Iran's Blockade Could Trigger a Global Energy Crisis",
        "tags": ["Oil Prices", "Strait of Hormuz", "Iran", "Energy Crisis", "OPEC", "World News"],
        "excerpt": "Iran's IRGC has closed the Strait of Hormuz, blocking 20% of global oil supply. Brent crude surged 13%. Analysts warn prices could hit $100/barrel.",
        "content": """<!-- wp:paragraph -->
<p><strong>Updated: March 2, 2026</strong> — In one of the most consequential developments of the US-Israel-Iran conflict, Iran's Islamic Revolutionary Guard Corps (IRGC) has effectively shut down the <strong>Strait of Hormuz</strong> — the world's most critical oil chokepoint. Oil prices have surged dramatically, and analysts are warning of a potential global energy crisis.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2>What Is the Strait of Hormuz?</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>The Strait of Hormuz is a narrow waterway between Iran and Oman that connects the Persian Gulf to the Gulf of Oman and the Arabian Sea. It is the world's single most important oil transit chokepoint:</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul>
<li><strong>17 million barrels</strong> of crude oil and condensates pass through it daily</li>
<li>This represents approximately <strong>20% of global oil supply</strong></li>
<li>It also handles <strong>20% of global LNG (liquefied natural gas) supply</strong></li>
<li>At its narrowest point, it is only <strong>21 miles (33 km) wide</strong></li>
<li>Major exporters dependent on it include Saudi Arabia, UAE, Kuwait, Iraq, and Qatar</li>
</ul>
<!-- /wp:list -->

<!-- wp:heading -->
<h2>What Happened?</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>On February 28, 2026, following the joint US-Israeli strikes on Iran that killed Supreme Leader Khamenei, the IRGC announced that the Strait of Hormuz was "effectively closed." Vessels entering the strait began receiving messages stating: <em>"No ship is allowed to pass the Strait of Hormuz."</em></p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Tanker traffic through the strait has largely halted, with a self-imposed pause by shipowners and traders as the conflict spreads. Reports indicate that Iranian naval forces have positioned mines and fast-attack boats in the strait, creating an effective naval blockade.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2>Oil Price Impact</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div class="rk-tbl-wrap"><table class="rk-tbl" style="width:100%;border-collapse:collapse;margin:20px 0;">
<thead><tr style="background:#16213e;color:#fff;">
<th style="padding:12px;text-align:left;">Benchmark</th>
<th style="padding:12px;text-align:center;">Pre-Crisis (Feb 27)</th>
<th style="padding:12px;text-align:center;">Current (Mar 2)</th>
<th style="padding:12px;text-align:center;">Change</th>
</tr></thead>
<tbody>
<tr style="border-bottom:1px solid #ddd;"><td style="padding:10px;">Brent Crude</td><td style="padding:10px;text-align:center;">$72/bbl</td><td style="padding:10px;text-align:center;"><strong>$82+/bbl</strong></td><td style="padding:10px;text-align:center;color:red;">+13%</td></tr>
<tr style="border-bottom:1px solid #ddd;background:#f9f9f9;"><td style="padding:10px;">WTI Crude</td><td style="padding:10px;text-align:center;">$67/bbl</td><td style="padding:10px;text-align:center;"><strong>$72+/bbl</strong></td><td style="padding:10px;text-align:center;color:red;">+8%</td></tr>
</tbody></table></div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>Energy analysts and investment banks expect prices to surge further — potentially reaching <strong>$90-$100 per barrel</strong> this week if disruptions persist. Some worst-case scenarios project prices exceeding $150/bbl if the blockade continues for weeks.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2>Global Economic Impact</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>The closure threatens far-reaching economic consequences:</p>
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
<ol>
<li><strong>Fuel prices</strong> — Gasoline and diesel prices are expected to spike worldwide within days</li>
<li><strong>Inflation</strong> — Higher energy costs will feed into consumer prices across all sectors</li>
<li><strong>Manufacturing</strong> — Energy-intensive industries face production cost increases</li>
<li><strong>Shipping</strong> — Alternative routes around Africa add weeks and significant costs</li>
<li><strong>Developing nations</strong> — Oil-importing countries in Asia and Africa face the greatest vulnerability</li>
</ol>
<!-- /wp:list -->

<!-- wp:heading -->
<h2>Which Countries Are Most Affected?</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Countries that depend heavily on oil passing through the Strait of Hormuz include:</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul>
<li><strong>Japan</strong> — Imports approximately 80% of its oil through the strait</li>
<li><strong>South Korea</strong> — Roughly 70% of oil imports transit the strait</li>
<li><strong>India</strong> — Major importer of Middle Eastern crude</li>
<li><strong>China</strong> — Largest buyer of Iranian and Saudi oil</li>
<li><strong>European Union</strong> — Significant dependence on Gulf oil and LNG</li>
</ul>
<!-- /wp:list -->

<!-- wp:heading -->
<h2>Can the US Navy Reopen the Strait?</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>The US Fifth Fleet, based in Bahrain, maintains a significant naval presence in the region. However, forcibly reopening the strait would be extremely challenging:</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul>
<li>Iran has deployed <strong>anti-ship missiles, mines, and fast-attack boats</strong></li>
<li>The narrow geography favors the defender</li>
<li>Mine-clearing operations could take <strong>weeks to months</strong></li>
<li>Any naval confrontation risks further escalation of the conflict</li>
</ul>
<!-- /wp:list -->

<!-- wp:heading -->
<h2>What to Watch Next</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Key indicators that will shape the coming days and weeks:</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul>
<li>Whether OPEC+ members with strategic reserves will release emergency supplies</li>
<li>US Strategic Petroleum Reserve (SPR) release decisions</li>
<li>Insurance rates for tankers in the Persian Gulf</li>
<li>Diplomatic efforts to negotiate safe passage</li>
<li>The duration and effectiveness of Iran's naval blockade</li>
</ul>
<!-- /wp:list -->

<!-- wp:paragraph -->
<p><em>This is a developing story. We will continue to update as the situation evolves. Last updated: March 2, 2026.</em></p>
<!-- /wp:paragraph -->"""
    },
    {
        "img": "news_iran_retaliation.png",
        "title": "Iran Strikes Back: Missiles Hit Israel and Gulf States as Regional War Escalates",
        "tags": ["Iran", "Israel", "Middle East", "Gulf States", "Hezbollah", "World News"],
        "excerpt": "Iran launched retaliatory strikes targeting 27 US bases across 8 countries. Explosions reported in Dubai, Doha, and Kuwait City. Hezbollah joins the fight.",
        "content": """<!-- wp:paragraph -->
<p><strong>Updated: March 2, 2026</strong> — Iran has unleashed a massive retaliatory strike campaign following the US-Israeli attacks that killed Supreme Leader Ayatollah Ali Khamenei. The Islamic Revolutionary Guard Corps (IRGC) has launched waves of missiles and drones at targets across the Middle East, marking the most significant military escalation in the region in decades.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2>Scale of Iran's Retaliation</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>The IRGC announced it has launched attacks on <strong>27 military bases across the Middle East</strong> where US troops are stationed. The strikes have targeted not only Israel but multiple Gulf states that host American military installations:</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div class="rk-tbl-wrap"><table class="rk-tbl" style="width:100%;border-collapse:collapse;margin:20px 0;">
<thead><tr style="background:#8b0000;color:#fff;">
<th style="padding:12px;text-align:left;">Country</th>
<th style="padding:12px;text-align:left;">Targets / Impact</th>
</tr></thead>
<tbody>
<tr style="border-bottom:1px solid #ddd;"><td style="padding:10px;"><strong>Israel</strong></td><td style="padding:10px;">Multiple cities targeted; 9 killed in Beit Shemesh missile strike</td></tr>
<tr style="border-bottom:1px solid #ddd;background:#f9f9f9;"><td style="padding:10px;"><strong>UAE</strong></td><td style="padding:10px;">Explosions in Dubai and Abu Dhabi; airports shut down</td></tr>
<tr style="border-bottom:1px solid #ddd;"><td style="padding:10px;"><strong>Qatar</strong></td><td style="padding:10px;">Blasts reported in Doha; Al Udeid Air Base area targeted</td></tr>
<tr style="border-bottom:1px solid #ddd;background:#f9f9f9;"><td style="padding:10px;"><strong>Kuwait</strong></td><td style="padding:10px;">Iranian strike near US Embassy in Kuwait City</td></tr>
<tr style="border-bottom:1px solid #ddd;"><td style="padding:10px;"><strong>Bahrain</strong></td><td style="padding:10px;">US Fifth Fleet headquarters area targeted; explosions in Manama</td></tr>
<tr style="border-bottom:1px solid #ddd;background:#f9f9f9;"><td style="padding:10px;"><strong>Saudi Arabia</strong></td><td style="padding:10px;">Military installations targeted</td></tr>
<tr style="border-bottom:1px solid #ddd;"><td style="padding:10px;"><strong>Jordan</strong></td><td style="padding:10px;">US bases along the border targeted</td></tr>
<tr style="border-bottom:1px solid #ddd;background:#f9f9f9;"><td style="padding:10px;"><strong>Iraq / Oman</strong></td><td style="padding:10px;">Additional strikes reported</td></tr>
</tbody></table></div>
<!-- /wp:html -->

<!-- wp:heading -->
<h2>Hezbollah Opens Northern Front</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>In a significant escalation, Lebanon-based <strong>Hezbollah has launched missiles at Israel</strong>, declaring the strikes are "in revenge" for the killing of Iran's supreme leader. This opens a dangerous second front for Israel along its northern border with Lebanon. Israel has responded with strikes on Lebanese territory, raising fears of a full-scale conflict engulfing Lebanon.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2>American Casualties</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p><strong>Three US service members have been killed</strong> and five more seriously injured — the first American casualties since Operation Epic Fury began. President Trump acknowledged the deaths, saying "there will likely be more" and vowing to "avenge" the fallen soldiers. The location of the American casualties has not been officially disclosed for operational security reasons.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2>Iran's Military Capabilities</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Iran's retaliatory capability has surprised some Western analysts:</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul>
<li><strong>Ballistic missiles</strong> — Iran possesses the largest ballistic missile arsenal in the Middle East</li>
<li><strong>Cruise missiles</strong> — Advanced land-attack cruise missiles with precision guidance</li>
<li><strong>Drone swarms</strong> — Hundreds of Shahed-series kamikaze drones deployed simultaneously</li>
<li><strong>Proxy networks</strong> — Hezbollah, Houthis, and Iraqi militias acting in coordination</li>
<li><strong>Naval forces</strong> — Fast-attack boats and anti-ship missiles in the Persian Gulf</li>
</ul>
<!-- /wp:list -->

<!-- wp:heading -->
<h2>Civilian Impact</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>The strikes on Gulf states have had devastating effects on civilian life. Dubai — one of the world's busiest tourism and business hubs — has seen explosions for the first time in its modern history. Residents across the Gulf region are sheltering in place, and several nations have issued emergency alerts to their populations.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2>What This Means for the Region</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>The expansion of Iran's retaliation beyond Israel to include Gulf Arab states fundamentally changes the nature of this conflict. Key implications:</p>
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
<ol>
<li><strong>Multi-front war</strong> — Israel now faces threats from Iran, Hezbollah, and potentially other proxy groups simultaneously</li>
<li><strong>Gulf state security</strong> — The myth of Gulf state invulnerability has been shattered</li>
<li><strong>US force protection</strong> — American troops across the region are under direct threat</li>
<li><strong>Diplomatic collapse</strong> — Chances for negotiated de-escalation are rapidly diminishing</li>
<li><strong>Humanitarian crisis</strong> — Civilian populations across multiple countries are at risk</li>
</ol>
<!-- /wp:list -->

<!-- wp:paragraph -->
<p><em>This is a developing story. Last updated: March 2, 2026.</em></p>
<!-- /wp:paragraph -->"""
    },
    {
        "img": "news_pak_afg.png",
        "title": "Pakistan Declares 'Open War' on Afghanistan: Everything You Need to Know",
        "tags": ["Pakistan", "Afghanistan", "Taliban", "South Asia", "World News"],
        "excerpt": "Pakistan launches Operation Ghazab Lil Haq against Afghanistan's Taliban government. Kabul bombed, 500+ casualties reported. A second major war erupts.",
        "content": """<!-- wp:paragraph -->
<p><strong>Updated: March 2, 2026</strong> — While global attention is focused on the Iran crisis, another major conflict has erupted in South Asia. Pakistan has declared <strong>"open war"</strong> on Afghanistan's Taliban government, launching large-scale military operations that have already resulted in hundreds of casualties on both sides.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2>Background: How Did We Get Here?</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Relations between Pakistan and Afghanistan have steadily deteriorated since the Taliban returned to power in 2021. Key factors include:</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul>
<li><strong>TTP (Tehrik-i-Taliban Pakistan)</strong> — Pakistan accuses the Afghan Taliban of sheltering the Pakistani Taliban, which has carried out deadly attacks inside Pakistan</li>
<li><strong>Cross-border strikes</strong> — Both nations have been exchanging military strikes for months throughout 2025</li>
<li><strong>Failed ceasefire</strong> — A October 2025 ceasefire brokered by Turkey and Qatar collapsed within a month</li>
<li><strong>Afghan drone strikes</strong> — Afghanistan launched retaliatory drone strikes on Pakistani territory on February 26, 2026, triggering the full-scale response</li>
</ul>
<!-- /wp:list -->

<!-- wp:heading -->
<h2>Operation Ghazab Lil Haq</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>On February 27, Pakistan launched <strong>Operation Ghazab Lil Haq</strong> (meaning "Wrath for Justice") — a full-scale military operation against Taliban positions in Afghanistan. Pakistan's Defense Minister Khawaja Asif declared: <em>"There will be chaos and a reckoning."</em></p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Key military actions include:</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul>
<li>Pakistani air force struck <strong>46 locations across Afghanistan</strong></li>
<li><strong>Kabul was bombed</strong> — the first strikes on the Afghan capital since the US withdrawal in 2021</li>
<li>Pakistan claims to have killed <strong>415 Taliban soldiers</strong> for the loss of 12 of its own</li>
<li>Afghanistan counter-claims <strong>80 Pakistani soldiers killed</strong> and 27 military posts captured</li>
</ul>
<!-- /wp:list -->

<!-- wp:heading -->
<h2>Casualties and Humanitarian Concerns</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Casualty figures vary dramatically between the two sides, as is common in active conflicts. Independent verification is extremely difficult given the remote terrain and restricted media access. What is clear is that <strong>hundreds have been killed or wounded</strong> in just the first few days of fighting, with civilian casualties reported in both countries.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2>International Response</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>The international community has called for restraint:</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul>
<li><strong>Iran and EU</strong> have urged dialogue between the two nations</li>
<li><strong>China</strong> — Pakistan's closest ally — has called for de-escalation</li>
<li><strong>Turkey and Qatar</strong> — previous ceasefire brokers — are attempting renewed mediation</li>
<li><strong>The United States</strong> is largely focused on the Iran conflict and has limited bandwidth for South Asian diplomacy</li>
</ul>
<!-- /wp:list -->

<!-- wp:heading -->
<h2>Why This Matters</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>This conflict has significant implications beyond the two countries:</p>
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
<ol>
<li><strong>Nuclear risk</strong> — Pakistan is a nuclear-armed state, adding a dangerous dimension to any conflict escalation</li>
<li><strong>Refugee crisis</strong> — Millions of Afghans could be displaced by fighting</li>
<li><strong>Regional instability</strong> — Combined with the Iran war, the broader region from the Middle East to South Asia is now engulfed in conflict</li>
<li><strong>Superpower competition</strong> — Both China and the US have strategic interests in the Pakistan-Afghanistan corridor</li>
<li><strong>Counter-terrorism</strong> — The conflict could create new safe havens for extremist groups</li>
</ol>
<!-- /wp:list -->

<!-- wp:paragraph -->
<p><em>This is a developing story. Last updated: March 2, 2026.</em></p>
<!-- /wp:paragraph -->"""
    },
    {
        "img": "news_ai_pentagon.png",
        "title": "Trump Bans Anthropic, OpenAI Gets $200M Pentagon Deal: The AI Arms Race Heats Up",
        "tags": ["AI", "Anthropic", "OpenAI", "Pentagon", "Trump", "Technology", "World News"],
        "excerpt": "Trump blacklists Anthropic after it refused autonomous weapons. Hours later, OpenAI signs $200M Pentagon deal. The AI ethics vs. defense debate intensifies.",
        "content": """<!-- wp:paragraph -->
<p><strong>Updated: March 2, 2026</strong> — In a stunning sequence of events that has sent shockwaves through the technology industry, the Trump administration has <strong>banned all federal agencies from using Anthropic's AI technology</strong> after the company refused to allow its systems to power autonomous weapons. Just hours later, rival <strong>OpenAI announced a deal with the Pentagon</strong> worth up to $200 million.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2>What Happened?</h2>
<!-- /wp:heading -->

<!-- wp:heading {"level":3} -->
<h3>The Anthropic Dispute</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>The conflict began during contract negotiations between Anthropic and the Pentagon for a military AI contract worth up to <strong>$200 million</strong>. Anthropic — the maker of Claude AI — insisted on two non-negotiable conditions:</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul>
<li><strong>No mass surveillance</strong> of American citizens</li>
<li><strong>No use in lethal autonomous weapons systems</strong></li>
</ul>
<!-- /wp:list -->

<!-- wp:paragraph -->
<p>The Pentagon rejected these conditions, maintaining it must be allowed to employ AI systems for "any lawful use." When Anthropic refused to budge, Defense Secretary Pete Hegseth took the unprecedented step of designating Anthropic as a <strong>"supply chain risk to national security"</strong> — a classification normally reserved for companies with ties to foreign adversaries like China or Russia.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":3} -->
<h3>Trump's Executive Action</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>On February 27, President Trump ordered all federal agencies and military contractors to <strong>cease using Anthropic products and services</strong>. This effectively bars Anthropic from the entire government sector — one of the most lucrative markets for AI companies.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":3} -->
<h3>OpenAI Swoops In</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Just hours after the Anthropic blacklisting, OpenAI CEO Sam Altman announced that the company had <strong>struck a deal with the Department of Defense</strong> to deploy its AI models on classified military networks. Notably, Altman stated that the DoD agreed to OpenAI's own restrictions on mass surveillance and autonomous weapons — "reflecting these principles in law and policy."</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2>The Key Question: What's Different?</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>If OpenAI's deal also includes restrictions on autonomous weapons, why was Anthropic banned for the same stance? Analysts point to several possible explanations:</p>
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
<ol>
<li><strong>Political relationships</strong> — OpenAI has cultivated closer ties with the Trump administration</li>
<li><strong>Flexibility in language</strong> — OpenAI's restrictions may have been framed more flexibly than Anthropic's hard lines</li>
<li><strong>Timing and leverage</strong> — With Anthropic eliminated, the Pentagon may have had to accept OpenAI's terms</li>
<li><strong>Competitive dynamics</strong> — The government may have wanted to send a message about which companies are "cooperative"</li>
</ol>
<!-- /wp:list -->

<!-- wp:heading -->
<h2>Impact on the AI Industry</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>This episode has massive implications for the AI sector:</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul>
<li><strong>Anthropic's market position</strong> — Being labeled a "supply chain risk" could damage its commercial business far beyond government contracts</li>
<li><strong>AI safety debate</strong> — Companies now face a stark choice between safety principles and government business</li>
<li><strong>Defense AI spending</strong> — The Pentagon's AI budget is expected to exceed $15 billion in 2027</li>
<li><strong>Legal battle</strong> — Anthropic has threatened to sue, saying "We will challenge any supply chain risk designation in court"</li>
</ul>
<!-- /wp:list -->

<!-- wp:heading -->
<h2>What This Means for AI Users</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>For everyday users of AI tools like Claude (Anthropic) and ChatGPT (OpenAI), the immediate impact is limited. However, the long-term implications are significant: the relationship between AI companies and governments will shape how these technologies develop, what safety guardrails remain in place, and ultimately who controls the most powerful technology of our time.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p><em>Last updated: March 2, 2026.</em></p>
<!-- /wp:paragraph -->"""
    },
    {
        "img": "news_stocks.png",
        "title": "Markets in Turmoil: War Fears, AI Bubble Concerns Rattle Global Stock Markets",
        "tags": ["Stock Market", "Nasdaq", "S&P 500", "Oil", "Nvidia", "Economy", "World News"],
        "excerpt": "Nasdaq drops 1.18%, oil surges 13%, and the CAPE ratio hits dot-com bubble levels. War in Iran and AI uncertainty shake investor confidence worldwide.",
        "content": """<!-- wp:paragraph -->
<p><strong>Updated: March 2, 2026</strong> — Global financial markets are experiencing significant turbulence as multiple crises converge: the US-Israel-Iran military conflict, surging oil prices, and growing concerns about an AI investment bubble. Investors are fleeing risk assets while energy stocks and safe havens surge.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2>Market Snapshot</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div class="rk-tbl-wrap"><table class="rk-tbl" style="width:100%;border-collapse:collapse;margin:20px 0;">
<thead><tr style="background:#16213e;color:#fff;">
<th style="padding:12px;text-align:left;">Index / Asset</th>
<th style="padding:12px;text-align:center;">Recent Change</th>
<th style="padding:12px;text-align:left;">Key Driver</th>
</tr></thead>
<tbody>
<tr style="border-bottom:1px solid #ddd;"><td style="padding:10px;">Nasdaq Composite</td><td style="padding:10px;text-align:center;color:red;"><strong>-1.18%</strong></td><td style="padding:10px;">AI stocks sell-off, Nvidia -5%</td></tr>
<tr style="border-bottom:1px solid #ddd;background:#f9f9f9;"><td style="padding:10px;">S&P 500</td><td style="padding:10px;text-align:center;color:red;"><strong>-0.54%</strong></td><td style="padding:10px;">Broad risk-off sentiment</td></tr>
<tr style="border-bottom:1px solid #ddd;"><td style="padding:10px;">Brent Crude Oil</td><td style="padding:10px;text-align:center;color:green;"><strong>+13%</strong></td><td style="padding:10px;">Strait of Hormuz closure</td></tr>
<tr style="border-bottom:1px solid #ddd;background:#f9f9f9;"><td style="padding:10px;">Energy Sector (XLE)</td><td style="padding:10px;text-align:center;color:green;"><strong>+25% MTD</strong></td><td style="padding:10px;">Oil price surge, supply fears</td></tr>
<tr style="border-bottom:1px solid #ddd;"><td style="padding:10px;">Gold</td><td style="padding:10px;text-align:center;color:green;"><strong>Rising</strong></td><td style="padding:10px;">Safe-haven demand</td></tr>
</tbody></table></div>
<!-- /wp:html -->

<!-- wp:heading -->
<h2>The AI Bubble Question</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Despite Nvidia posting strong earnings, its stock <strong>fell over 5%</strong> on February 26 — a classic "sell the news" event that has raised alarm bells. The broader AI trade is showing signs of exhaustion:</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul>
<li>The <strong>CAPE ratio</strong> (Cyclically Adjusted Price-to-Earnings) is hovering around <strong>39</strong> — its highest since the dot-com bubble burst in 2000</li>
<li>A February 2026 Pew Research survey found <strong>72% of Americans</strong> have a negative view of the economy</li>
<li>Citrini Research published an "AI doomsday scenario" warning that white-collar unemployment from AI could trigger a recession</li>
<li>The "Magnificent Seven" tech stocks that drove 2024-2025 gains are showing divergent performance</li>
</ul>
<!-- /wp:list -->

<!-- wp:heading -->
<h2>War Premium in Energy</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>While tech stocks suffer, the energy sector is booming. The Iran conflict and Strait of Hormuz closure have created a massive "war premium" in oil prices. Energy stocks (XLE) have surged approximately 25% month-to-date, making them the clear winners in this environment. Defense stocks have also rallied sharply as military spending expectations increase.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2>What Should Investors Do?</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Financial advisors are recommending caution:</p>
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
<ol>
<li><strong>Diversify</strong> — Don't be overexposed to any single sector, especially tech</li>
<li><strong>Energy hedging</strong> — Consider energy ETFs or oil futures as portfolio insurance</li>
<li><strong>Cash reserves</strong> — Maintain adequate cash to weather volatility and buy opportunities</li>
<li><strong>Avoid panic selling</strong> — Historical data shows markets recover from geopolitical shocks</li>
<li><strong>Watch the Fed</strong> — Interest rate decisions will be critical in the coming months</li>
</ol>
<!-- /wp:list -->

<!-- wp:paragraph -->
<p><em>Disclaimer: This article is for informational purposes only and does not constitute financial advice. Last updated: March 2, 2026.</em></p>
<!-- /wp:paragraph -->"""
    },
    {
        "img": "news_aviation.png",
        "title": "19,000 Flights Delayed: Middle East Aviation Crisis Strands Travelers Worldwide",
        "tags": ["Aviation", "Travel", "Middle East", "Flights Cancelled", "Dubai Airport", "World News"],
        "excerpt": "3,500+ flights cancelled, 10 nations close airspace, Dubai Airport shut down indefinitely. Millions of travelers stranded from Australia to Brazil.",
        "content": """<!-- wp:paragraph -->
<p><strong>Updated: March 2, 2026</strong> — The US-Israel-Iran conflict has triggered the worst aviation disruption in Middle East history. Over <strong>3,500 flights have been cancelled</strong>, <strong>19,000 flights delayed</strong>, and airspace across 10 nations remains closed as military operations continue. Tens of thousands of travelers are stranded worldwide.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2>Which Airspaces Are Closed?</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>As of March 2, 2026, the following nations have announced at least partial airspace closures:</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div class="rk-tbl-wrap"><table class="rk-tbl" style="width:100%;border-collapse:collapse;margin:20px 0;">
<thead><tr style="background:#16213e;color:#fff;">
<th style="padding:12px;text-align:left;">Country</th>
<th style="padding:12px;text-align:center;">Status</th>
<th style="padding:12px;text-align:left;">Major Airports Affected</th>
</tr></thead>
<tbody>
<tr style="border-bottom:1px solid #ddd;"><td style="padding:10px;">Iran</td><td style="padding:10px;text-align:center;">🔴 Closed</td><td style="padding:10px;">All airports</td></tr>
<tr style="border-bottom:1px solid #ddd;background:#f9f9f9;"><td style="padding:10px;">Israel</td><td style="padding:10px;text-align:center;">🔴 Closed</td><td style="padding:10px;">Ben Gurion (TLV)</td></tr>
<tr style="border-bottom:1px solid #ddd;"><td style="padding:10px;">UAE</td><td style="padding:10px;text-align:center;">🔴 Closed</td><td style="padding:10px;">Dubai (DXB), Abu Dhabi (AUH)</td></tr>
<tr style="border-bottom:1px solid #ddd;background:#f9f9f9;"><td style="padding:10px;">Qatar</td><td style="padding:10px;text-align:center;">🔴 Closed</td><td style="padding:10px;">Hamad International (DOH)</td></tr>
<tr style="border-bottom:1px solid #ddd;"><td style="padding:10px;">Bahrain</td><td style="padding:10px;text-align:center;">🔴 Closed</td><td style="padding:10px;">Bahrain International (BAH)</td></tr>
<tr style="border-bottom:1px solid #ddd;background:#f9f9f9;"><td style="padding:10px;">Kuwait</td><td style="padding:10px;text-align:center;">🔴 Closed</td><td style="padding:10px;">Kuwait International (KWI)</td></tr>
<tr style="border-bottom:1px solid #ddd;"><td style="padding:10px;">Iraq</td><td style="padding:10px;text-align:center;">🔴 Closed</td><td style="padding:10px;">Baghdad, Erbil</td></tr>
<tr style="border-bottom:1px solid #ddd;background:#f9f9f9;"><td style="padding:10px;">Jordan</td><td style="padding:10px;text-align:center;">🟡 Partial</td><td style="padding:10px;">Queen Alia (AMM)</td></tr>
<tr style="border-bottom:1px solid #ddd;"><td style="padding:10px;">Saudi Arabia</td><td style="padding:10px;text-align:center;">🟡 Partial</td><td style="padding:10px;">Eastern region restrictions</td></tr>
<tr style="border-bottom:1px solid #ddd;background:#f9f9f9;"><td style="padding:10px;">Syria</td><td style="padding:10px;text-align:center;">🔴 Closed</td><td style="padding:10px;">Damascus International</td></tr>
</tbody></table></div>
<!-- /wp:html -->

<!-- wp:heading -->
<h2>Major Airlines: Cancellation Status</h2>
<!-- /wp:heading -->

<!-- wp:list -->
<ul>
<li><strong>Emirates & flydubai</strong> — All operations suspended indefinitely</li>
<li><strong>Qatar Airways</strong> — All flights cancelled from Doha</li>
<li><strong>Etihad Airways</strong> — Suspended all Abu Dhabi operations</li>
<li><strong>KLM</strong> — Cancelled Tel Aviv, Dubai, Riyadh, Dammam flights through March 5</li>
<li><strong>Delta Air Lines</strong> — New York to Tel Aviv cancelled until March 8</li>
<li><strong>United Airlines</strong> — Tel Aviv flights through March 6; Dubai through March 4</li>
<li><strong>Air Canada</strong> — Israel until March 8; Dubai until March 3</li>
</ul>
<!-- /wp:list -->

<!-- wp:heading -->
<h2>Global Ripple Effects</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Dubai International Airport (DXB) is the world's busiest airport for international passengers, handling over 87 million travelers annually. Its closure, combined with the shutdown of other major Gulf hubs, has created cascading effects worldwide. Travelers are stranded as far away as <strong>Australia, Brazil, and the Maldives</strong>. Passengers on flights between Southeast Asia and Europe should expect <strong>90 minutes to three hours of additional flight time</strong> due to route detours around closed airspace.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2>What to Do If You're Affected</h2>
<!-- /wp:heading -->

<!-- wp:list {"ordered":true} -->
<ol>
<li><strong>Check your airline's website</strong> — Most carriers are offering free rebooking or full refunds</li>
<li><strong>Contact your travel insurance provider</strong> — War/conflict exclusions may apply, but many policies cover trip interruption</li>
<li><strong>Register with your embassy</strong> — If stranded abroad, register with your country's consular services</li>
<li><strong>Avoid booking new Middle East travel</strong> — Until the situation stabilizes, avoid booking new trips to affected regions</li>
<li><strong>Monitor airspace updates</strong> — Follow Eurocontrol and FAA NOTAMs for the latest airspace status</li>
</ol>
<!-- /wp:list -->

<!-- wp:paragraph -->
<p><em>This is a developing story. Last updated: March 2, 2026.</em></p>
<!-- /wp:paragraph -->"""
    },
    {
        "img": "news_paralympics.png",
        "title": "Milano Cortina 2026 Winter Paralympics: Complete Guide to the Games (March 6-15)",
        "tags": ["Paralympics", "Milano Cortina 2026", "Winter Sports", "Italy", "Sports", "World News"],
        "excerpt": "665 athletes, 79 medal events, 6 sports. The Milano Cortina 2026 Winter Paralympics open March 6 at the Arena di Verona. Here's your complete guide.",
        "content": """<!-- wp:paragraph -->
<p>The <strong>Milano Cortina 2026 Paralympic Winter Games</strong> are set to open on <strong>March 6, 2026</strong> at the historic Arena di Verona in Italy. This will be the biggest Winter Paralympics in history, marking 50 years since the first Paralympic Winter Games in 1976. Here's everything you need to know.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2>Key Facts at a Glance</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div class="rk-tbl-wrap"><table class="rk-tbl" style="width:100%;border-collapse:collapse;margin:20px 0;">
<thead><tr style="background:#16213e;color:#fff;">
<th style="padding:12px;text-align:left;">Detail</th>
<th style="padding:12px;text-align:left;">Information</th>
</tr></thead>
<tbody>
<tr style="border-bottom:1px solid #ddd;"><td style="padding:10px;"><strong>Dates</strong></td><td style="padding:10px;">March 6 - 15, 2026</td></tr>
<tr style="border-bottom:1px solid #ddd;background:#f9f9f9;"><td style="padding:10px;"><strong>Opening Ceremony</strong></td><td style="padding:10px;">Arena di Verona, March 6</td></tr>
<tr style="border-bottom:1px solid #ddd;"><td style="padding:10px;"><strong>Athletes</strong></td><td style="padding:10px;">~665 Para athletes</td></tr>
<tr style="border-bottom:1px solid #ddd;background:#f9f9f9;"><td style="padding:10px;"><strong>Medal Events</strong></td><td style="padding:10px;">79 events (record)</td></tr>
<tr style="border-bottom:1px solid #ddd;"><td style="padding:10px;"><strong>Sports</strong></td><td style="padding:10px;">6 sports</td></tr>
<tr style="border-bottom:1px solid #ddd;background:#f9f9f9;"><td style="padding:10px;"><strong>Venues</strong></td><td style="padding:10px;">Milan, Verona, Tesero, Cortina d'Ampezzo</td></tr>
<tr style="border-bottom:1px solid #ddd;"><td style="padding:10px;"><strong>Ticket Prices</strong></td><td style="padding:10px;">From EUR 15 (89% under EUR 35)</td></tr>
</tbody></table></div>
<!-- /wp:html -->

<!-- wp:heading -->
<h2>The Six Sports</h2>
<!-- /wp:heading -->

<!-- wp:heading {"level":3} -->
<h3>1. Para Alpine Skiing</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>The most popular Winter Paralympic sport, featuring downhill, super-G, giant slalom, slalom, and super combined events. Athletes compete in three categories: standing, sitting (using a mono-ski), and visually impaired (with a guide).</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":3} -->
<h3>2. Para Biathlon</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Combines cross-country skiing with rifle shooting. Visually impaired athletes use an electronic acoustic sight that emits sounds to help them aim. Events range from 6km to 15km.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":3} -->
<h3>3. Para Cross-Country Skiing</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Athletes race on snow-covered courses using classical or freestyle techniques. Categories include standing, sitting (using a sit-ski), and visually impaired events.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":3} -->
<h3>4. Para Ice Hockey</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>One of the most exciting team sports, with athletes using specially designed sleds with two blades. Players use two sticks — one for propulsion and one for shooting. The tournament features 8 teams competing for gold.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":3} -->
<h3>5. Para Snowboard</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Athletes compete in snowboard-cross and banked slalom events. This is one of the newest Paralympic sports, having debuted at the Sochi 2014 Games.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":3} -->
<h3>6. Wheelchair Curling</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Teams of four compete in mixed-gender matches, delivering stones from their wheelchairs. No sweeping is allowed, making stone placement and strategy even more critical.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2>Historical Significance</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>These Games mark several important milestones:</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul>
<li><strong>50th anniversary</strong> of the first Paralympic Winter Games (Örnsköldsvik, Sweden, 1976)</li>
<li><strong>20 years</strong> since Italy last hosted (Torino 2006)</li>
<li><strong>Record participation</strong> — more athletes and medal events than any previous Winter Paralympics</li>
<li>The Paralympic Flame arrived in Milan on February 25, carried by 49 torchbearers through the city center</li>
</ul>
<!-- /wp:list -->

<!-- wp:heading -->
<h2>How to Watch</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>The Games will be broadcast globally through the International Paralympic Committee's broadcast partners. Check your local broadcaster for coverage details. Many events will also be available for streaming through the official Paralympic website and app.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p><em>The Opening Ceremony at the Arena di Verona on March 6 is expected to be a spectacular showcase of Italian culture and Paralympic values.</em></p>
<!-- /wp:paragraph -->"""
    },
    {
        "img": "news_fifa.png",
        "title": "FIFA World Cup 2026: Everything You Need to Know About the Biggest Tournament Ever",
        "tags": ["FIFA", "World Cup 2026", "Soccer", "Football", "USA", "Sports", "World News"],
        "excerpt": "48 teams, 104 matches, 3 host countries. The 2026 FIFA World Cup runs June 11 - July 19 across the US, Canada, and Mexico. Complete guide inside.",
        "content": """<!-- wp:paragraph -->
<p>The <strong>2026 FIFA World Cup</strong> is shaping up to be the biggest sporting event in history. For the first time, <strong>48 teams</strong> will compete across <strong>three host countries</strong> — the United States, Canada, and Mexico — in a tournament that will feature <strong>104 matches</strong> over 39 days. Here's your complete guide.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2>Key Tournament Details</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div class="rk-tbl-wrap"><table class="rk-tbl" style="width:100%;border-collapse:collapse;margin:20px 0;">
<thead><tr style="background:#16213e;color:#fff;">
<th style="padding:12px;text-align:left;">Detail</th>
<th style="padding:12px;text-align:left;">Information</th>
</tr></thead>
<tbody>
<tr style="border-bottom:1px solid #ddd;"><td style="padding:10px;"><strong>Dates</strong></td><td style="padding:10px;">June 11 - July 19, 2026</td></tr>
<tr style="border-bottom:1px solid #ddd;background:#f9f9f9;"><td style="padding:10px;"><strong>Host Countries</strong></td><td style="padding:10px;">USA, Canada, Mexico</td></tr>
<tr style="border-bottom:1px solid #ddd;"><td style="padding:10px;"><strong>Teams</strong></td><td style="padding:10px;">48 (expanded from 32)</td></tr>
<tr style="border-bottom:1px solid #ddd;background:#f9f9f9;"><td style="padding:10px;"><strong>Total Matches</strong></td><td style="padding:10px;">104 (up from 64)</td></tr>
<tr style="border-bottom:1px solid #ddd;"><td style="padding:10px;"><strong>Duration</strong></td><td style="padding:10px;">39 days</td></tr>
<tr style="border-bottom:1px solid #ddd;background:#f9f9f9;"><td style="padding:10px;"><strong>Opening Match</strong></td><td style="padding:10px;">Mexico vs South Africa, Estadio Azteca, June 11</td></tr>
<tr style="border-bottom:1px solid #ddd;"><td style="padding:10px;"><strong>Final</strong></td><td style="padding:10px;">MetLife Stadium, New Jersey, July 19</td></tr>
</tbody></table></div>
<!-- /wp:html -->

<!-- wp:heading -->
<h2>New Format Explained</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>The expanded 48-team format works as follows:</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul>
<li><strong>Group Stage</strong> — 12 groups of 4 teams each</li>
<li><strong>Advancement</strong> — Top 2 from each group + 8 best third-placed teams advance</li>
<li><strong>Round of 32</strong> — New knockout round (didn't exist before)</li>
<li><strong>Round of 16 → Quarterfinals → Semifinals → Final</strong></li>
</ul>
<!-- /wp:list -->

<!-- wp:heading -->
<h2>New Rule Changes</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>FIFA has adopted several new rules to speed up matches:</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul>
<li><strong>Off-field treatment rule</strong> — Injured players must leave the pitch for treatment to reduce time-wasting</li>
<li><strong>Expanded VAR scope</strong> — Now covers corner kick decisions and second yellow cards</li>
<li><strong>Stricter time-keeping</strong> — Enhanced stoppage time protocols to ensure 60+ minutes of actual play</li>
</ul>
<!-- /wp:list -->

<!-- wp:heading -->
<h2>Qualification Update (March 2026)</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Most of the 48 slots are already filled. The final qualifying matches are happening in March 2026:</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul>
<li><strong>UEFA playoffs</strong> — 4 remaining European spots to be decided</li>
<li><strong>Inter-confederation playoffs</strong> — 2 final spots via playoff tournament in Guadalajara and Monterrey (March 26-31)</li>
<li><strong>Iran's participation</strong> is uncertain given the ongoing military conflict</li>
</ul>
<!-- /wp:list -->

<!-- wp:heading -->
<h2>Key Storylines to Watch</h2>
<!-- /wp:heading -->

<!-- wp:list {"ordered":true} -->
<ol>
<li><strong>Messi's farewell?</strong> — Lionel Messi, 38, is reportedly preparing specifically for this World Cup as a potential final tournament</li>
<li><strong>Neymar's return</strong> — Brazil coach Carlo Ancelotti has set a March deadline for his World Cup decision on Neymar</li>
<li><strong>Mexico's security</strong> — FIFA President Infantino expressed "complete confidence" in Mexico despite cartel violence concerns</li>
<li><strong>USA as hosts</strong> — The US hasn't hosted since 1994; the tournament could transform soccer's popularity in America</li>
<li><strong>48-team experiment</strong> — Will the expanded format dilute quality or create more Cinderella stories?</li>
</ol>
<!-- /wp:list -->

<!-- wp:heading -->
<h2>Host Cities and Stadiums</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Matches will be played across 16 venues in three countries, including iconic stadiums like:</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul>
<li><strong>MetLife Stadium</strong> (New Jersey) — Final venue, capacity 82,500</li>
<li><strong>SoFi Stadium</strong> (Los Angeles) — Semifinal venue</li>
<li><strong>AT&T Stadium</strong> (Dallas) — Semifinal venue</li>
<li><strong>Estadio Azteca</strong> (Mexico City) — Opening match, historic World Cup venue</li>
<li><strong>BMO Field</strong> (Toronto) — Canada's primary venue</li>
</ul>
<!-- /wp:list -->

<!-- wp:paragraph -->
<p><em>Stay tuned for continued coverage as qualification wraps up and the tournament approaches. The world's biggest sporting event is just over three months away!</em></p>
<!-- /wp:paragraph -->"""
    }
]

# Publish all 8 posts
published = []
for i, post in enumerate(posts):
    print(f"\n[{i+1}/8] Publishing: {post['title'][:60]}...")
    
    # Upload image
    mid = upload_img(post["img"])
    
    # Create tags
    tids = make_tags(post["tags"])
    
    # Publish post
    r = s.post(f"{SITE}/wp-json/wp/v2/posts", headers=H, json={
        "title": post["title"],
        "content": post["content"],
        "status": "publish",
        "categories": [CAT_ID],
        "featured_media": mid,
        "tags": tids,
        "excerpt": post["excerpt"]
    })
    
    if r.status_code == 201:
        p = r.json()
        print(f"  ✅ ID={p['id']} URL={p['link']}")
        published.append({"id": p["id"], "title": post["title"][:50], "url": p["link"]})
    else:
        print(f"  ❌ FAIL: {r.status_code} {r.text[:200]}")

print(f"\n===== 발행 완료: {len(published)}/8 =====")
for p in published:
    print(f"  [{p['id']}] {p['title']}")
