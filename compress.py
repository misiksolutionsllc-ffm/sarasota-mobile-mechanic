#!/usr/bin/env python3
"""Recompress the inlined hero JPEG to a web-sane size."""
import re, base64, io, pathlib
from PIL import Image

P = pathlib.Path.home() / "workspace/site-deploy/index.html"
html = P.read_text(encoding="utf-8")

m = re.search(r"data:image/jpeg;base64,([A-Za-z0-9+/=]+)", html)
assert m, "no jpeg blob found"
raw = base64.b64decode(m.group(1))
img = Image.open(io.BytesIO(raw))
print("original:", img.size, len(raw), "bytes")

# Cap width at 1400px (plenty for hero), keep aspect
if img.size[0] > 1400:
    img = img.resize((1400, int(img.size[1] * 1400 / img.size[0])), Image.LANCZOS)
buf = io.BytesIO()
img.convert("RGB").save(buf, "JPEG", quality=70, optimize=True, progressive=True)
small = base64.b64encode(buf.getvalue()).decode()
print("recompressed:", img.size, len(buf.getvalue()), "bytes")

html = html.replace(m.group(0), "data:image/jpeg;base64," + small, 1)
P.write_text(html, encoding="utf-8")
print("final file bytes:", P.stat().st_size)
