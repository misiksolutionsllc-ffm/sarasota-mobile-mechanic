#!/usr/bin/env python3
"""Extract shared CSS into style.css and link it from all pages."""
import re, pathlib

D = pathlib.Path.home() / "workspace/site-deploy"
pages = ["index.html", "siesta-key.html", "bradenton.html", "venice.html",
         "north-port.html", "osprey.html", "nokomis.html"]

# index.html head <style> is the shared core
index = (D / "index.html").read_text(encoding="utf-8")
core = re.search(r"<head>.*?<style>(.*?)</style>", index, re.S).group(1)

# city pages have extra rules after the core css; grab from one city page
city = (D / "bradenton.html").read_text(encoding="utf-8")
city_css = re.search(r"<style>(.*?)</style>", city, re.S).group(1)
extra = city_css.replace(core, "", 1).strip()

(D / "style.css").write_text("/* shared */\n" + core.strip() + "\n\n/* city pages */\n" + extra + "\n",
                             encoding="utf-8")

for p in pages:
    f = D / p
    html = f.read_text(encoding="utf-8")
    html2, n = re.subn(r"<style>.*?</style>", '<link rel="stylesheet" href="style.css" />', html, count=1, flags=re.S)
    assert n == 1, p
    f.write_text(html2, encoding="utf-8")
    print(p, len(html2), "bytes")

print("style.css", (D / "style.css").stat().st_size, "bytes")
total = sum((D / p).stat().st_size for p in pages) + (D / "style.css").stat().st_size
total += (D / "sitemap.xml").stat().st_size + (D / "robots.txt").stat().st_size
print("total deploy payload ~", total, "bytes")
