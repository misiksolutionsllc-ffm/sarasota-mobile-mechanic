#!/usr/bin/env python3
"""Generate local SEO city pages + sitemap + robots, link area pills on index."""
import re, json, pathlib

D = pathlib.Path.home() / "workspace/site-deploy"
BASE = "https://misiksolutionsllc-ffm.github.io/sarasota-mobile-mechanic"
PHONE = "+17544654655"
PHONE_TXT = "(754) 465-4655"

# Agent-readable service catalog (schema.org hasOfferCatalog). Prices are the
# on-file published ranges (pricing-and-dispatch-ops.md == site cards == GBP pack).
def _offer(name, lo=None, hi=None, desc=None):
    svc = {"@type": "Service", "name": name}
    if desc:
        svc["description"] = desc
    o = {"@type": "Offer", "itemOffered": svc}
    if lo is not None:
        o["priceSpecification"] = {"@type": "PriceSpecification",
                                   "priceCurrency": "USD",
                                   "minPrice": lo, "maxPrice": hi}
    return o

OFFER_CATALOG = [
    {"@type": "OfferCatalog", "name": "Emergency Roadside Assistance",
     "itemListElement": [
         _offer("Emergency Jump Start", 75, 100),
         _offer("Car Lockout Service", 90, 130),
         _offer("Flat Tire Change", 90, 120),
         _offer("Emergency Fuel Delivery", 75, 100,
                "Service charge for fuel delivery; the cost of the fuel itself is additional."),
         _offer("Tow Coordination", None, None,
                "Quoted on the spot before dispatch."),
     ]},
    {"@type": "OfferCatalog", "name": "Mobile Mechanic Repairs",
     "itemListElement": [
         _offer("Battery Replacement", 220, 300),
         _offer("Brake Pad Replacement", 300, 420),
         _offer("Brake Pads & Rotors", 480, 700),
         _offer("Alternator Replacement", 480, 750),
         _offer("Starter Replacement", 400, 650),
         _offer("Check Engine Diagnostics", 90, 130),
         _offer("Mobile Oil Change", 95, 140),
         _offer("Serpentine Belt Replacement", 200, 300),
         _offer("Pre-Purchase Inspection", 130, 180),
     ]},
]

index = (D / "index.html").read_text(encoding="utf-8")
css = re.search(r"<style>(.*?)</style>", index, re.S).group(1)

CITIES = {
    "siesta-key": {"name": "Siesta Key", "intro": (
        "Stuck near the beach with a dead battery or a flat tire? Sarasota Mobile Mechanic dispatches "
        "emergency roadside assistance across Siesta Key — from Siesta Beach Village to the south end of the key. "
        "Jump starts, car lockouts, flat tire changes and fuel delivery, 24/7. Our mobile mechanics also handle "
        "brakes, batteries, alternators, starters and diagnostics right where you're parked — no tow to the mainland, no waiting rooms."),
        "faq": [
            ("I'm stuck at Siesta Beach with a dead battery. How fast can you get here?",
             "Call now for an immediate ETA — our 24/7 roadside dispatch covers the entire key, and most jump starts take minutes on arrival."),
            ("Can you change a flat tire in a beach parking lot?",
             "Yes. We install your spare on the spot and check pressures, wherever you're parked on Siesta Key."),
        ]},
    "bradenton": {"name": "Bradenton", "intro": (
        "Just north of Sarasota across the Manatee River, Bradenton drivers get the same 24/7 emergency roadside "
        "assistance: jump starts, car lockouts, flat tire changes, fuel delivery and tow coordination — dispatched "
        "around the clock. Need more than roadside help? Our mobile mechanics come to your home or office in Bradenton "
        "for brakes, batteries, alternators, starters, diagnostics and oil changes, with fixed upfront pricing."),
        "faq": [
            ("Do you serve Bradenton or only Sarasota?",
             "We fully serve Bradenton — emergency roadside 24/7 and scheduled mobile mechanic work daily 8:00 AM–8:00 PM."),
            ("My car won't start in my Bradenton driveway. What do I do?",
             "Call or text us. We'll triage by phone, quote a fixed price, and dispatch a mechanic or roadside tech to you."),
        ]},
    "venice": {"name": "Venice", "intro": (
        "Down in Venice, a dead battery or locked car doesn't have to ruin your day. Sarasota Mobile Mechanic brings "
        "24/7 emergency roadside assistance to Venice — jump starts, lockouts, flat tire changes, fuel delivery — plus "
        "full mobile mechanic service at your home or workplace: brakes, batteries, alternators, starters, diagnostics "
        "and oil changes. Fixed pricing agreed before we roll."),
        "faq": [
            ("How much is a jump start in Venice?",
             "Fixed $75–100, quoted upfront before dispatch. Battery test included on the spot."),
            ("Do you work on cars at homes in Venice?",
             "Yes — driveway, garage or workplace. Most scheduled jobs are completed the same day."),
        ]},
    "north-port": {"name": "North Port", "intro": (
        "North Port's neighborhoods spread wide — and we cover all of them. Sarasota Mobile Mechanic dispatches 24/7 "
        "emergency roadside assistance across North Port: jump starts, car lockouts, flat tire changes, fuel delivery "
        "and tow coordination. Our mobile mechanics also serve North Port homes and offices daily 8:00 AM–8:00 PM for "
        "brakes, batteries, alternators, starters, diagnostics and oil changes."),
        "faq": [
            ("I'm on I-75 near North Port with a flat. Can you come?",
             "Yes — call now. We'll dispatch roadside help to your location and install your spare on the spot."),
            ("Do you charge extra for coming to North Port?",
             "No trip surcharges inside our service area. Your quote is fixed upfront."),
        ]},
    "osprey": {"name": "Osprey", "intro": (
        "Between Sarasota and Venice, Osprey drivers are right in our core coverage zone. Sarasota Mobile Mechanic "
        "provides 24/7 emergency roadside assistance in Osprey — jump starts, lockouts, flat tire changes, fuel "
        "delivery — and scheduled mobile mechanic repairs at your location: brakes, batteries, alternators, starters, "
        "diagnostics and oil changes, all with upfront fixed pricing."),
        "faq": [
            ("Can you reach Osprey quickly?",
             "Osprey sits in the middle of our service area — call for a live ETA, roadside dispatch runs 24/7."),
            ("Do you do pre-purchase inspections in Osprey?",
             "Yes — 100+ point mobile inspection at the seller's location before you buy."),
        ]},
    "nokomis": {"name": "Nokomis", "intro": (
        "In Nokomis, help is one call away any time of day or night. Sarasota Mobile Mechanic dispatches 24/7 "
        "emergency roadside assistance across Nokomis — jump starts, car lockouts, flat tire changes, fuel delivery "
        "and tow coordination. Prefer scheduled service? Our mobile mechanics come to you daily 8:00 AM–8:00 PM for "
        "brakes, batteries, alternators, starters, diagnostics and oil changes."),
        "faq": [
            ("It's 2 AM and my car is dead in Nokomis. Are you really available?",
             "Yes — emergency roadside dispatch runs 24/7. Call now and we'll roll."),
            ("How do I pay?",
             "Card, tap-to-pay or payment link after the job is done. No payment until you're satisfied."),
        ]},
}

all_cities = [("Sarasota", "index.html")] + [(v["name"], f"{k}.html") for k, v in CITIES.items()]

def area_links(current):
    return " ".join(
        f'<a class="area" href="{fn}">{nm}</a>' if fn != current else f'<span class="area">{nm}</span>'
        for nm, fn in all_cities)

for slug, c in CITIES.items():
    name = c["name"]
    faq_items = c["faq"] + [(f"What are your hours in {name}?",
        f"Scheduled mobile mechanic repairs run daily 8:00 AM\u20138:00 PM in {name}. Emergency roadside assistance \u2014 jump starts, car lockouts, flat tire changes and fuel delivery \u2014 is dispatched 24/7. Call {PHONE_TXT}.")]
    faq_json = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq_items]
    faq_schema = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faq_json}, indent=2)
    faq_html = "\n".join(
        f'        <details class="faq-item"><summary>{q}</summary><p>{a}</p></details>' for q, a in faq_items)
    page = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
  <meta name="description" content="Stranded in {name}, FL? 24/7 emergency roadside assistance: jump starts, car lockouts, flat tire changes, fuel delivery. Mobile mechanic repairs at your location. Call {PHONE_TXT}." />
  <link rel="canonical" href="{BASE}/{slug}.html" />
  <meta property="og:type" content="website" />
  <meta property="og:title" content="24/7 Emergency Roadside Assistance & Mobile Mechanic in {name}, FL" />
  <meta property="og:description" content="Jump starts, lockouts, flat tires, fuel delivery — dispatched 24/7 in {name}, FL. Call {PHONE_TXT}." />
  <title>24/7 Emergency Roadside Assistance & Mobile Mechanic in {name}, FL | Sarasota Mobile Mechanic</title>
  <style>{css}
      .page-hero {{ padding:34px 0 54px; }}
      .page-hero h1 {{ font-size:clamp(40px,6vw,72px); }}
      .city-body p {{ font-size:19px; color:var(--ink-soft); max-width:720px; }}
      .area[href] {{ color:inherit; text-decoration:none; }}
      .area[href]:hover {{ border-color:var(--accent); }}
      .back {{ display:inline-block; margin-bottom:18px; color:var(--ink-soft); font-weight:600; }}
  </style>
  <script type="application/ld+json">
  {json.dumps({"@context": "https://schema.org", "@type": "AutoRepair", "name": "Sarasota Mobile Mechanic",
    "description": f"24/7 emergency roadside assistance and mobile auto repair serving {name}, FL.",
    "telephone": "+1-754-465-4655", "url": f"{BASE}/{slug}.html", "priceRange": "$$",
    "address": {"@type": "PostalAddress", "addressLocality": "Sarasota", "addressRegion": "FL", "addressCountry": "US"},
    "areaServed": {"@type": "City", "name": name},
    "openingHoursSpecification": {"@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
      "opens": "08:00", "closes": "20:00"},
    "hasOfferCatalog": OFFER_CATALOG}, indent=2)}
  </script>
  <script type="application/ld+json">
  {faq_schema}
  </script>
</head>
<body>
  <main>
    <section class="page-hero" aria-labelledby="city-title">
      <div class="wrap">
        <a class="back" href="index.html">&larr; Sarasota Mobile Mechanic</a>
        <p class="eyebrow">24/7 emergency roadside dispatch · {name}</p>
        <h1 id="city-title">Stranded in {name}?<br>We come to you.</h1>
        <div class="city-body"><p>{c["intro"]}</p></div>
        <div class="hero-actions">
          <a class="btn btn-primary" href="tel:{PHONE}">Call {PHONE_TXT}</a>
          <a class="btn btn-secondary" href="sms:{PHONE}">Text us</a>
        </div>
        <p class="priority-note"><span class="dispatch-badge">24/7 Emergency Dispatch</span>
        <span class="priority-note-text">Roadside calls get priority dispatch, day and night.</span></p>
      </div>
    </section>
    <section class="services" aria-labelledby="rs-title">
      <div class="wrap">
        <div class="section-head"><h2 id="rs-title">Roadside help<br>in {name}.</h2>
        <p class="section-intro">Fixed upfront pricing, quoted before we dispatch. No hourly billing, no surprises.</p></div>
        <div class="service-list">
          <div class="service-row"><span class="service-index">01</span><div><h3 class="service-name">Emergency Jump Start</h3><p class="service-description">Dead battery? Fast jump start plus battery health check at your location in {name}.</p></div><span class="service-price">$75–100</span></div>
          <div class="service-row"><span class="service-index">02</span><div><h3 class="service-name">Car Lockout Service</h3><p class="service-description">Keys locked inside? Damage-free vehicle entry with professional tools.</p></div><span class="service-price">$90–130</span></div>
          <div class="service-row"><span class="service-index">03</span><div><h3 class="service-name">Flat Tire Change</h3><p class="service-description">Flat on the road? We install your spare on the spot and check pressures.</p></div><span class="service-price">$90–120</span></div>
          <div class="service-row"><span class="service-index">04</span><div><h3 class="service-name">Emergency Fuel Delivery</h3><p class="service-description">Out of gas? We bring enough fuel to get you to the nearest station.</p></div><span class="service-price long">$75–100 + fuel</span></div>
          <div class="service-row"><span class="service-index">05</span><div><h3 class="service-name">Tow Coordination</h3><p class="service-description">Can't be fixed roadside? We dispatch a tow truck from our partner network.</p></div><span class="service-price">Quoted</span></div>
        </div>
        <p class="quote-note">Need brakes, battery replacement, alternator, starter, diagnostics or an oil change? <a href="index.html">See our mobile mechanic services</a> — at your home or office in {name}, daily 8:00 AM–8:00 PM.</p>
      </div>
    </section>
    <section aria-labelledby="faq-title">
      <div class="wrap">
        <div class="section-head"><h2 id="faq-title">{name}<br>questions.</h2></div>
        <div class="faq-list">
{faq_html}
        </div>
      </div>
    </section>
    <section class="coverage" aria-labelledby="cov-title">
      <div class="wrap coverage-grid">
        <div><h2 id="cov-title">Also serving<br>nearby.</h2><p>One dispatch network across the Sarasota area.</p></div>
        <div class="area-list">{area_links(slug + ".html")}</div>
      </div>
    </section>
    <section class="contact" aria-labelledby="ct-title">
      <div class="wrap"><div class="contact-card">
        <div><h2 id="ct-title">Stuck in {name}? Call now.</h2><p>Emergency roadside dispatch 24/7. Scheduled mechanic work daily, 8:00 AM–8:00 PM.</p></div>
        <a class="btn" href="tel:{PHONE}">{PHONE_TXT}</a>
      </div></div>
    </section>
  </main>
  <footer><div class="wrap footer-row"><span>Sarasota Mobile Mechanic · 24/7 emergency roadside assistance &amp; mobile auto repair — {name}, FL · © 2026</span><a href="index.html">Home</a></div></footer>
  <div class="mobile-bar"><a class="btn btn-primary" href="tel:{PHONE}">Call now</a><a class="btn text-btn" href="sms:{PHONE}">Text us</a></div>
</body>
</html>
"""
    (D / f"{slug}.html").write_text(page, encoding="utf-8")
    print("wrote", slug + ".html", len(page), "bytes")

# Link area pills on index to city pages
for slug, c in CITIES.items():
    old = f'<span class="area">{c["name"]}</span>'
    new = f'<a class="area" href="{slug}.html">{c["name"]}</a>'
    assert old in index, f"pill not found: {c['name']}"
    index = index.replace(old, new, 1)
# make linked pills look right
index = index.replace(".area { padding:13px 17px;",
                      ".area[href] { color:inherit; text-decoration:none; } .area[href]:hover { border-color:var(--accent); } .area { padding:13px 17px;", 1)
(D / "index.html").write_text(index, encoding="utf-8")
print("index pills linked")

# sitemap.xml + robots.txt
urls = [f"{BASE}/"] + [f"{BASE}/{s}.html" for s in CITIES]
(D / "sitemap.xml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    "\n".join(f"  <url><loc>{u}</loc></url>" for u in urls) + "\n</urlset>\n", encoding="utf-8")
(D / "robots.txt").write_text("User-agent: *\nAllow: /\n\nSitemap: " + BASE + "/sitemap.xml\n", encoding="utf-8")
print("sitemap + robots written")
