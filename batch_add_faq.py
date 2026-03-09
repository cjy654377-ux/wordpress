#!/usr/bin/env python3
"""Batch add FAQ schema to posts that have 800+ words but no FAQ schema."""
import os, sys, re, json
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import login, REST

FAQS = {
    413: [
        ("What is the meaning of BTS Blood Sweat & Tears?", "Blood Sweat & Tears explores the tension between innocence and temptation, heavily inspired by Hermann Hesse's novel 'Demian' and the concept of Abraxas — a deity representing both good and evil."),
        ("What book inspired BTS Blood Sweat & Tears?", "The song is directly inspired by Hermann Hesse's 1919 novel 'Demian: The Story of Emil Sinclair's Youth.' The music video features visual references to Abraxas and Pieter Bruegel's paintings."),
        ("What does Abraxas mean in BTS Blood Sweat & Tears?", "Abraxas is a deity from Hesse's Demian that embodies both God and Devil — representing the idea that growth requires embracing both light and darkness."),
    ],
    411: [
        ("What is BTS Fake Love really about?", "Fake Love is about self-erasure in relationships — hiding your true self and pretending to be someone else to be loved. It explores the pain of losing your identity for someone else's approval."),
        ("What album is Fake Love from?", "Fake Love is the lead single from 'Love Yourself: Tear' (2018), the third installment in the Love Yourself series. It debuted at #10 on the Billboard Hot 100."),
    ],
    409: [
        ("What is the meaning of BTS Black Swan?", "Black Swan explores the fear of losing passion for music — what BTS considers their 'first death.' Inspired by Martha Graham's quote 'A dancer dies twice,' it asks what happens when the thing you love most no longer moves you."),
        ("Why is it called Black Swan?", "The title references both the ballet 'Swan Lake' and Martha Graham's concept of an artist's first death being the moment they lose their creative passion."),
    ],
    404: [
        ("Why does BTS Spring Day still chart years later?", "Spring Day has remained on Korean music charts for over 9 years due to its universal themes of loss and hope. Many listeners associate it with the 2014 Sewol Ferry disaster."),
        ("What does bogoshipda mean in Spring Day?", "Bogoshipda means 'I miss you' in Korean. It's the song's opening line and emotional core — a simple but powerful expression of longing."),
    ],
    394: [
        ("When does the BTS Arirang World Tour 2026 start?", "The BTS Arirang World Tour begins in April 2026, spanning 82 dates across 34 cities worldwide through October 2026."),
        ("How can I get BTS Arirang tour tickets?", "Tickets are available through Weverse (ARMY membership presale), Ticketmaster, and local platforms. ARMY members get priority presale access."),
    ],
    353: [
        ("When does the BTS Arirang album come out?", "BTS's fifth studio album 'Arirang' releases on March 20, 2026, followed by a free Netflix live concert event."),
        ("Is BTS Arirang a full group comeback?", "Yes, Arirang marks BTS's first full-group comeback with all seven members after completing military service."),
    ],
    347: [
        ("How is the Iran war affecting oil prices?", "The conflict caused oil prices to surge past $79/barrel, with Brent crude spiking over 13% as Iran's threats to the Strait of Hormuz endanger 20% of global oil supply."),
        ("What is the humanitarian impact of the Iran conflict?", "The conflict has triggered what experts call the largest refugee crisis in history, with millions displaced across the Middle East."),
    ],
    359: [
        ("How dependent is South Korea on Middle East oil?", "South Korea imports approximately 70% of its crude oil from the Middle East, making it one of the most vulnerable economies to Strait of Hormuz disruptions."),
        ("How has the Iran war affected the Korean won?", "The won has weakened significantly against the dollar as oil price surges increase Korea's import costs and worsen the trade balance."),
    ],
    357: [
        ("What are the biggest K-Beauty trends in 2026?", "Top trends include PDRN (salmon DNA) serums, exosome therapy, Medicube's AGE-R device, and science-backed skinimalism focusing on fewer but more potent ingredients."),
        ("What is PDRN in Korean skincare?", "PDRN (Polydeoxyribonucleotide) is derived from salmon DNA and promotes skin regeneration at the cellular level. Originally a clinic treatment, it's now available in K-Beauty serums."),
    ],
    393: [
        ("When does Boyfriend on Demand premiere on Netflix?", "Boyfriend on Demand premiered on Netflix on March 6, 2026, starring Blackpink's Jisoo and Seo In-guk."),
        ("What K-dramas should I watch before Boyfriend on Demand?", "We recommend 5 dramas with similar themes: romantic comedies with strong female leads and unique premises."),
    ],
    355: [
        ("Who stars in Boyfriend on Demand?", "Blackpink's Jisoo plays the lead alongside Seo In-guk, with 8 actors portraying virtual boyfriend options in this Netflix romantic comedy."),
    ],
    361: [
        ("What Korean phrases should I know for a BTS concert?", "Essential phrases include fan chants, 'saranghae' (I love you), 'fighting' (you can do it), and practical phrases for navigating Korean venues."),
        ("How do I learn BTS fan chants?", "Fan chants are posted on fan sites and YouTube before each comeback. Practice by watching fancam videos and following along with romanized lyrics."),
    ],
}


def build_faq_schema(faqs):
    entities = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]
    schema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": entities}
    return f'\n<script type="application/ld+json">\n{json.dumps(schema, indent=2)}\n</script>'


def main():
    s, h = login()
    updated = 0
    for post_id, faqs in FAQS.items():
        r = s.get(f"{REST}/posts/{post_id}", headers=h)
        if r.status_code != 200:
            print(f"SKIP {post_id}: fetch failed")
            continue
        post = r.json()
        content = post["content"]["rendered"]
        title = re.sub(r'&#\d+;', '', post["title"]["rendered"])[:50]
        if 'FAQPage' in content:
            print(f"SKIP {post_id}: already has FAQ | {title}")
            continue
        new_content = content + build_faq_schema(faqs)
        r = s.post(f"{REST}/posts/{post_id}", headers=h, json={"content": new_content})
        if r.status_code == 200:
            print(f"OK   {post_id}: +{len(faqs)} FAQs | {title}")
            updated += 1
        else:
            print(f"FAIL {post_id}: {r.status_code} | {title}")
    print(f"\nDone: {updated} updated")


if __name__ == "__main__":
    main()
