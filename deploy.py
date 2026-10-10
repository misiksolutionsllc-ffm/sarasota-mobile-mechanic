#!/usr/bin/env python3
"""Upload index.html to Vercel file storage, then create a production deployment."""
import base64, hashlib, json, pathlib, subprocess, sys

TEAM = "team_ANUpYw9Ad4NLE01ptniAQUcm"
P = pathlib.Path.home() / "workspace/site-deploy/index.html"
raw = P.read_bytes()
b64 = base64.b64encode(raw).decode()
digest = hashlib.sha1(raw).hexdigest()
print("file bytes:", len(raw), "b64 chars:", len(b64), "sha1:", digest)

def call(name, args):
    cmd = ["vercel", "call-tool", "--name", name, "--arguments-json", json.dumps(args)]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    try:
        return json.loads(r.stdout)
    except Exception:
        print("RAW:", r.stdout[:500], r.stderr[:500]); raise

# 1. upload file
up = call("upload_file", {"teamId": TEAM, "contentLength": len(raw), "xVercelDigest": digest, "requestBody": b64})
print("upload resp:", json.dumps(up)[:600])
content = up["result"]["content"][0]["text"]
try:
    sha = json.loads(content)
    if isinstance(sha, dict):
        sha = sha.get("sha") or sha.get("hash") or sha.get("id")
except Exception:
    sha = content.strip().strip('"')
print("sha:", sha)

# 2. create deployment
dep = call("create_deployment", {
    "teamId": TEAM,
    "requestBody": {
        "name": "sarasota-mobile-mechanic",
        "target": "production",
        "files": [{"file": "index.html", "sha": sha, "size": len(raw)}],
    },
})
print("deploy resp:", json.dumps(dep)[:1500])
