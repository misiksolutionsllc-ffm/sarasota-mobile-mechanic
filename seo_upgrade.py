#!/usr/bin/env python3
"""SEO + CRO upgrade for the exported Sarasota Mobile Mechanic site."""
import re, shutil, pathlib

SRC = pathlib.Path.home() / "workspace/your_files/sarasota-mobile-mechanic-website/sarasota-mobile-mechanic-website.html"
DST = pathlib.Path.home() / "workspace/site-deploy/index.html"
shutil.copyfile(SRC, DST)
html = DST.read_text(encoding="utf-8")

# 1. Title
html = html.replace(
    "<title>Sarasota Mobile Mechanic</title>",
    "<title>24/7 Emergency Roadside Assistance & Mobile Mechanic in Sarasota, FL | Sarasota Mobile Mechanic</title>",
    1,
)

# 2. Meta description
html = html.replace(
    '<meta name="description" content="Emergency roadside assistance and mobile auto repair in Sarasota, Florida. Call or text for priority dispatch and an upfront quote." />',
    '<meta name="description" content="Stranded in Sarasota? 24/7 emergency roadside assistance: jump starts, car lockouts, flat tire changes, fuel delivery. Plus mobile mechanic repairs at your location. Call (754) 465-4655 for immediate dispatch." />',
    1,
)

# 3. OG/Twitter + JSON-LD after the icon link
head_extras = '''<link rel="icon" href="data:," />
  <meta property="og:type" content="website" />
  <meta property="og:title" content="24/7 Emergency Roadside Assistance & Mobile Mechanic in Sarasota, FL" />
  <meta property="og:description" content="Jump starts, lockouts, flat tires, fuel delivery — dispatched 24/7. Mobile mechanic repairs daily 8 AM–8 PM. Call (754) 465-4655." />
  <meta property="og:url" content="__SITE_URL__" />
  <meta name="twitter:card" content="summary" />
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "AutoRepair",
    "name": "Sarasota Mobile Mechanic",
    "description": "24/7 emergency roadside assistance (jump starts, car lockouts, flat tire changes, fuel delivery, tow coordination) and mobile auto repair (brakes, batteries, alternators, starters, diagnostics, oil changes) across the Sarasota, FL area.",
    "telephone": "+1-754-465-4655",
    "url": "__SITE_URL__",
    "priceRange": "$$",
    "address": {
      "@type": "PostalAddress",
      "addressLocality": "Sarasota",
      "addressRegion": "FL",
      "addressCountry": "US"
    },
    "areaServed": [
      {"@type": "City", "name": "Sarasota"},
      {"@type": "City", "name": "Siesta Key"},
      {"@type": "City", "name": "Bradenton"},
      {"@type": "City", "name": "Venice"},
      {"@type": "City", "name": "North Port"},
      {"@type": "City", "name": "Osprey"},
      {"@type": "City", "name": "Nokomis"}
    ],
    "openingHoursSpecification": {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
      "opens": "08:00",
      "closes": "20:00"
    }
  }
  </script>
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {"@type": "Question", "name": "Do you really come to my location?",
       "acceptedAnswer": {"@type": "Answer", "text": "Yes — home, office, or parking lot anywhere in the Sarasota area: Sarasota, Siesta Key, Bradenton, Venice, North Port, Osprey and Nokomis. You don't come to us."}},
      {"@type": "Question", "name": "How fast can you get here?",
       "acceptedAnswer": {"@type": "Answer", "text": "Emergency roadside assistance is dispatched 24/7 — call (754) 465-4655 for an immediate ETA. Scheduled mobile mechanic repairs run daily 8:00 AM–8:00 PM, most jobs completed same day."}},
      {"@type": "Question", "name": "What are your hours?",
       "acceptedAnswer": {"@type": "Answer", "text": "Scheduled mobile mechanic repairs run daily 8:00 AM\u20138:00 PM. Emergency roadside assistance \u2014 jump starts, car lockouts, flat tire changes and fuel delivery \u2014 is dispatched 24/7. Call (754) 465-4655."}},
      {"@type": "Question", "name": "How much does it cost?",
       "acceptedAnswer": {"@type": "Answer", "text": "You get a fixed upfront quote before we dispatch — no hourly billing, no surprises. Jump starts $75–100, car lockouts $90–130, flat tire changes $90–120, fuel delivery $75–100 plus fuel."}},
      {"@type": "Question", "name": "Do you bring the parts?",
       "acceptedAnswer": {"@type": "Answer", "text": "Yes. Quality parts and batteries are included in every fixed quote. No parts runs, no waiting."}},
      {"@type": "Question", "name": "What if my car can't be fixed on the spot?",
       "acceptedAnswer": {"@type": "Answer", "text": "We coordinate a tow truck from our partner network to get you and your vehicle where they need to go."}},
      {"@type": "Question", "name": "How do I pay?",
       "acceptedAnswer": {"@type": "Answer", "text": "Card, tap-to-pay or payment link after the job is done. No payment until you're satisfied."}}
    ]
  }
  </script>'''
html = html.replace('<link rel="icon" href="data:," />', head_extras, 1)

# 4. FAQ section before the coverage section
faq = '''<section class="faq" aria-labelledby="faq-title"><div class="wrap">
      <div class="section-head"><h2 id="faq-title">Questions,<br>answered.</h2>
      <p class="section-intro">Straight answers before you call. Anything else — <a href="tel:+17544654655">call (754) 465-4655</a>, we pick up.</p></div>
      <div class="faq-list">
        <details class="faq-item"><summary>Do you really come to my location?</summary><p>Yes — that's the whole idea. Home, office, or parking lot anywhere in Sarasota, Siesta Key, Bradenton, Venice, North Port, Osprey and Nokomis. You don't come to us.</p></details>
        <details class="faq-item"><summary>How fast can you get here?</summary><p>Emergency roadside assistance is dispatched <strong>24/7</strong> — call for an immediate ETA. Scheduled mobile mechanic repairs run daily 8:00 AM–8:00 PM, and most jobs are completed same day.</p></details>
        <details class="faq-item"><summary>What are your hours?</summary><p>Scheduled mobile mechanic repairs run daily 8:00 AM\u20138:00 PM. Emergency roadside assistance \u2014 jump starts, car lockouts, flat tire changes and fuel delivery \u2014 is dispatched <strong>24/7</strong>. Call (754) 465-4655.</p></details>
        <details class="faq-item"><summary>How much does it cost?</summary><p>A fixed upfront quote before we dispatch — no hourly billing, no surprises. Jump starts $75–100, car lockouts $90–130, flat tire changes $90–120, fuel delivery $75–100 plus fuel.</p></details>
        <details class="faq-item"><summary>Do you bring the parts?</summary><p>Yes. Quality parts and batteries are included in every fixed quote. No parts runs, no waiting.</p></details>
        <details class="faq-item"><summary>What if my car can't be fixed on the spot?</summary><p>We coordinate a tow truck from our partner network to get you and your vehicle where they need to go.</p></details>
        <details class="faq-item"><summary>How do I pay?</summary><p>Card, tap-to-pay, or payment link after the job is done. No payment until you're satisfied.</p></details>
      </div>
    </div></section>
    <style>
      .faq-list { border-top:2px solid var(--ink); max-width:860px; }
      .faq-item { border-bottom:1px solid var(--line); }
      .faq-item summary { cursor:pointer; padding:20px 8px 20px 0; font-family:"Archivo",sans-serif; font-weight:700; font-size:clamp(18px,2.2vw,23px); letter-spacing:-.02em; list-style:none; display:flex; justify-content:space-between; align-items:center; gap:16px; }
      .faq-item summary::-webkit-details-marker { display:none; }
      .faq-item summary::after { content:"+"; font-size:26px; color:var(--accent); font-weight:400; flex:none; }
      .faq-item[open] summary::after { content:"\\2013"; }
      .faq-item p { margin:0 0 22px; color:var(--ink-soft); font-size:17px; max-width:700px; }
      .faq-item a { color:inherit; }
    </style>
'''
anchor = '<section class="coverage" aria-labelledby="coverage-title">'
assert anchor in html, "coverage anchor not found"
html = html.replace(anchor, faq + "    " + anchor, 1)

# 5. Footer: add keyword line
html = html.replace(
    "<span>Sarasota Mobile Mechanic · Booking and dispatch service in Sarasota, FL</span>",
    "<span>Sarasota Mobile Mechanic · 24/7 emergency roadside assistance &amp; mobile auto repair — Sarasota, Siesta Key, Bradenton, Venice, North Port, Osprey, Nokomis, FL · © 2026</span>",
    1,
)

DST.write_text(html, encoding="utf-8")
print("OK, bytes:", DST.stat().st_size)
print("title:", re.search(r"<title>(.*?)</title>", html).group(1)[:80])
print("jsonld count:", html.count('application/ld+json'))
print("faq items:", html.count('class="faq-item"'))
