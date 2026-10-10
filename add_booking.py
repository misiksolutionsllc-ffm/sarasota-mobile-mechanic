#!/usr/bin/env python3
"""Add appointment-request section + form JS + hero link."""
import pathlib, re

D = pathlib.Path.home() / "workspace/site-deploy"
P = D / "index.html"
html = P.read_text(encoding="utf-8")

# 1. Hero link under the action buttons
old_hero = "Text us</a>\n            </div>"
new_hero = ("Text us</a>\n            </div>\n"
            '            <p class="hero-book"><a href="#book">or book an appointment &rarr;</a></p>')
assert old_hero in html, "hero anchor missing"
html = html.replace(old_hero, new_hero, 1)

# 2. Booking section before the coverage section
section = '''    <section class="book" id="book" aria-labelledby="book-title">
      <div class="wrap">
        <div class="section-head">
          <h2 id="book-title">Book an<br>appointment.</h2>
          <p class="section-intro">Pick a service, date and time window — we text you back to confirm. For roadside emergencies, <a href="tel:+17544654655">call now</a> instead of waiting on a form.</p>
        </div>
        <form id="appt-form" class="appt-form" novalidate>
          <div class="field"><label for="f-name">Your name</label><input id="f-name" type="text" autocomplete="name" required /></div>
          <div class="field"><label for="f-phone">Phone number</label><input id="f-phone" type="tel" autocomplete="tel" placeholder="(___) ___-____" required /></div>
          <div class="field"><label for="f-service">Service</label><select id="f-service" required>
            <option value="" disabled selected>Select a service</option>
            <option>Battery Replacement</option><option>Brake Pad Replacement</option>
            <option>Brake Pads &amp; Rotors</option><option>Alternator Replacement</option>
            <option>Starter Replacement</option><option>Check Engine Diagnostics</option>
            <option>Mobile Oil Change</option><option>Serpentine Belt Replacement</option>
            <option>Pre-Purchase Inspection</option><option>Something else</option>
          </select></div>
          <div class="field"><label for="f-date">Preferred date</label><input id="f-date" type="date" required /></div>
          <div class="field"><label for="f-time">Time window</label><select id="f-time" required>
            <option value="" disabled selected>Select a window</option>
            <option>Morning (8 AM - 12 PM)</option><option>Midday (12 PM - 4 PM)</option>
            <option>Evening (4 PM - 8 PM)</option>
          </select></div>
          <div class="field"><label for="f-vehicle">Vehicle <span class="opt">(optional)</span></label><input id="f-vehicle" type="text" placeholder="e.g. 2018 Honda Civic" /></div>
          <div class="field field-wide"><label for="f-loc">Where should we come?</label><input id="f-loc" type="text" placeholder="Street address, city" autocomplete="street-address" required /></div>
          <div class="field field-wide"><label for="f-notes">Notes <span class="opt">(optional)</span></label><textarea id="f-notes" rows="3" placeholder="What is going on with the car?"></textarea></div>
          <p class="form-error" id="form-error" role="alert" hidden>Please fill in your name, phone, service, date, time window and location.</p>
          <button class="btn btn-primary" type="submit">Send appointment request</button>
          <p class="form-note">Tapping send opens your messaging app with the request ready — just press send. We confirm every appointment by text, usually within minutes. On a computer? Just call <a href="tel:+17544654655">(754) 465-4655</a>.</p>
        </form>
      </div>
    </section>
    <script>
    (function(){
      var form = document.getElementById('appt-form');
      var dateEl = document.getElementById('f-date');
      var err = document.getElementById('form-error');
      dateEl.min = new Date().toISOString().split('T')[0];
      form.addEventListener('submit', function(e){
        e.preventDefault();
        if(!form.checkValidity()){ err.hidden = false; form.reportValidity(); return; }
        err.hidden = true;
        var v = function(id){ return document.getElementById(id).value.trim(); };
        var msg = 'APPOINTMENT REQUEST - Sarasota Mobile Mechanic\\n'
          + 'Name: ' + v('f-name') + '\\n'
          + 'Phone: ' + v('f-phone') + '\\n'
          + 'Service: ' + v('f-service') + '\\n'
          + 'When: ' + v('f-date') + ', ' + v('f-time') + '\\n'
          + 'Where: ' + v('f-loc')
          + (v('f-vehicle') ? '\\nVehicle: ' + v('f-vehicle') : '')
          + (v('f-notes') ? '\\nNotes: ' + v('f-notes') : '');
        window.location.href = 'sms:+17544654655?&body=' + encodeURIComponent(msg);
      });
    })();
    </script>
'''
anchor = '    <section class="coverage" aria-labelledby="coverage-title">'
assert anchor in html, "coverage anchor missing"
html = html.replace(anchor, section + anchor, 1)
P.write_text(html, encoding="utf-8")

# 3. CSS appended to style.css
css = """
.hero-book { margin:18px 0 0; }
.hero-book a { color:var(--lime); font-weight:700; text-decoration:none; }
.hero-book a:hover { text-decoration:underline; }
.book { background:var(--surface); }
.appt-form { display:grid; grid-template-columns:1fr 1fr; gap:18px; max-width:880px; background:var(--paper); border:1px solid var(--line); border-radius:var(--radius-md); padding:clamp(24px,4vw,44px); }
.field { display:flex; flex-direction:column; gap:8px; min-width:0; }
.field-wide { grid-column:1 / -1; }
.field label { font-weight:700; font-size:16px; }
.field .opt { font-weight:500; color:var(--ink-soft); }
.field input, .field select, .field textarea { font:inherit; font-size:17px; padding:14px 16px; border:1px solid var(--line); border-radius:var(--radius-sm); background:var(--surface); color:var(--ink); width:100%; }
.field textarea { resize:vertical; }
.field input:focus, .field select:focus, .field textarea:focus { outline:2px solid var(--accent); outline-offset:1px; border-color:var(--accent); }
.form-error { grid-column:1 / -1; color:var(--accent-dark); font-weight:700; margin:0; }
.appt-form .btn { grid-column:1 / -1; justify-self:start; cursor:pointer; }
.form-note { grid-column:1 / -1; margin:0; color:var(--ink-soft); font-size:15px; }
.form-note a { color:inherit; }
@media (max-width:640px){ .appt-form { grid-template-columns:1fr; } .appt-form .btn { width:100%; } }
"""
with open(D / "style.css", "a", encoding="utf-8") as f:
    f.write(css)
print("booking section added; index.html bytes:", P.stat().st_size)
