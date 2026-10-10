#!/usr/bin/env python3
"""Upload all site files to Vercel and create a production deployment."""
import base64, hashlib, json, pathlib, subprocess

D = pathlib.Path.home() / "workspace/site-deploy"
FILES = ["index.html", "siesta-key.html", "bradenton.html", "venice.html",
         "north-port.html", "osprey.html", "nokomis.html",
         "hero.jpg", "sitemap.xml", "robots.txt"]

def call(name, args):
    cmd = ["vercel", "call-tool", "--name", name, "--arguments-json", json.dumps(args)]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    return json.loads(r.stdout)

uploaded = []
for fn in FILES:
    raw = (D / fn).read_bytes()
    b64 = base64.b64encode(raw).decode()
    digest = hashlib.sha1(raw).hexdigest()
    up = call("upload_file", {"contentLength": len(raw), "xVercelDigest": digest, "requestBody": b64})
    err = up["result"].get("isError")
    print(fn, len(raw), "bytes ->", "OK" if not err else "FAIL: " + up["result"]["content"][0]["text"][:200])
    assert not err, fn
    uploaded.append({"file": fn, "sha": digest, "size": len(raw)})

dep = call("create_deployment", {
    "requestBody": {
        "name": "sarasota-mobile-mechanic",
        "target": "production",
        "files": uploaded,
    },
})
c = dep["result"]["content"][0]["text"]
print("deploy isError:", dep["result"].get("isError"))
print(c[:1200])
