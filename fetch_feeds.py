import json, time, hashlib, feedparser, yaml, requests
from datetime import datetime, timedelta, timezone
from dateutil import parser as dtp
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "public" / "data" / "articles.json"

HEADERS = {"User-Agent": "Mozilla/5.0 (CyberPolicyRadar/1.0; +https://example.com)"}

def norm_date(s):
    if not s:
        return None
    try:
        dt = dtp.parse(s)
        if not dt.tzinfo:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc).isoformat()
    except Exception:
        return None

def fetch_feed(feed):
    """Try to fetch a feed via HTTP and parse it."""
    url = feed["url"]
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15, allow_redirects=True)
        content_type = resp.headers.get("Content-Type", "")
        if "xml" not in content_type and "rss" not in content_type:
            print(f"⚠️ {feed['name']}: not XML ({content_type}), skipping or HTML page")
            return []
        d = feedparser.parse(resp.content)
        print(f"✅ {feed['name']}: HTTP {resp.status_code}, {len(d.entries)} entries")
        items = []
        for e in d.entries:
            items.append({
                "id": hashlib.sha1((e.get("link") or e.get("id") or str(e)).encode()).hexdigest(),
                "title": e.get("title", "").strip(),
                "url": e.get("link"),
                "published": norm_date(e.get("published") or e.get("updated")),
                "summary": (e.get("summary") or "").strip(),
                "source": feed["name"],
            })
        return items
    except Exception as e:
        print(f"❌ {feed['name']} failed: {e}")
        return []

def collect(cfg):
    all_items = []
    for region in cfg["regions"]:
        for country in region["countries"]:
            for feed in country["feeds"]:
                items = fetch_feed(feed)
                for it in items:
                    it["country"] = country["code"]
                    it["region"] = region["name"]
                all_items.extend(items)
                time.sleep(0.5)
    return all_items

def dedupe(items):
    seen, out = set(), []
    for it in items:
        if it["id"] not in seen:
            seen.add(it["id"])
            out.append(it)
    return out

def main():
    cfg = yaml.safe_load((ROOT / "feeds.yaml").read_text())
    items = collect(cfg)
    items = dedupe(items)
    if not items:
        print("⚠️ No feed items found. Try different feeds or check network access.")
    week_ago = datetime.now(timezone.utc) - timedelta(days=30)
    filtered = [it for it in items if not it["published"] or dtp.parse(it["published"]).astimezone(timezone.utc) >= week_ago]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"items": filtered}, indent=2))
    print(f"✨ Wrote {len(filtered)} articles → {OUT}")

if __name__ == "__main__":
    main()
