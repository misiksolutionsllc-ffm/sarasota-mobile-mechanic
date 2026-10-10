#!/usr/bin/env python3
"""Extract the inlined hero JPEG to hero.jpg and reference it from GitHub raw."""
import re, base64, pathlib

D = pathlib.Path.home() / "workspace/site-deploy"
P = D / "index.html"
html = P.read_text(encoding="utf-8")

m = re.search(r"data:image/jpeg;base64,([A-Za-z0-9+/=]+)", html)
assert m, "no jpeg blob found"
(D / "hero.jpg").write_bytes(base64.b64decode(m.group(1)))
print("hero.jpg bytes:", (D / "hero.jpg").stat().st_size)

url = "https://raw.githubusercontent.com/misiksolutionsllc-ffm/sarasota-mobile-mechanic/main/hero.jpg"
html = html.replace(m.group(0), url, 1)
P.write_text(html, encoding="utf-8")
print("index.html bytes:", P.stat().st_size)
assert "data:image/jpeg;base64" not in html
print("OK")
