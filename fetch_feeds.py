import json, time, hashlib, feedparser, yaml, requests
from datetime import datetime, timedelta, timezone
from dateutil import parser as dtp
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "data" / "articles.json"
HEADERS = {"User-Agent": "Mozilla/5.0 (CyberPolicyRadar/1.0)"}

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

def fetch_feed(feed, region=None, country=None):
    """Fetch and parse an RSS/Atom feed."""
    url = feed["url"]
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15, allow_redirects=True)
        content_type = resp.headers.get("Content-Type", "")
        if "xml" not in content_type and "rss" not in content_type:
            print(f"⚠️ {feed['name']}: not XML ({content_type}), skipping")
            return []
        d = feedparser.parse(resp.content)
        print(f"✅ {feed['name']}: HTTP {resp.status_code}, {len(d.entries)} entries")
        items = []
        for e in d.entries:
            # Try to find an image
            img = None
            if "media_content" in e and len(e.media_content) > 0:
                img = e.media_content[0].get("url")
            elif "media_thumbnail" in e and len(e.media_thumbnail) > 0:
                img = e.media_thumbnail[0].get("url")
            elif "links" in e:
                for l in e.links:
                    if l.get("type", "").startswith("image"):
                        img = l.get("href")
                        break
            if not img:
                img = "https://via.placeholder.com/640x360?text=Cyber+Policy+News"

            items.append({
                "id": hashlib.sha1((e.get("link") or e.get("id") or str(e)).encode()).hexdigest(),
                "title": e.get("title", "").strip(),
                "url": e.get("link"),
                "published": norm_date(e.get("published") or e.get("updated")),
                "summary": (e.get("summary") or "").strip(),
                "source": feed["name"],
                "region": region,
                "country": country,
                "image": img
            })
        return items
    except Exception as e:
        print(f"❌ {feed['name']} failed: {e}")
        return []

def main():
    feeds_file = ROOT / "feeds.yaml"
    if not feeds_file.exists():
        print("Missing feeds.yaml")
        return
    cfg = yaml.safe_load(feeds_file.read_text())
    all_items = []
    for region in cfg.get("regions", []):
        region_name = region["name"]
        for country in region.get("countries", []):
            for feed in country.get("feeds", []):
                items = fetch_feed(feed, region=region_name, country=country["code"])
                all_items.extend(items)
                time.sleep(0.5)
    # Deduplicate
    seen, deduped = set(), []
    for it in all_items:
        if it["id"] not in seen:
            seen.add(it["id"])
            deduped.append(it)
    # Filter to last 30 days
    week_ago = datetime.now(timezone.utc) - timedelta(days=30)
    filtered = [
        it for it in deduped
        if not it["published"] or dtp.parse(it["published"]).astimezone(timezone.utc) >= week_ago
    ]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "items": filtered
    }, indent=2))
    print(f"✨ Wrote {len(filtered)} articles → {OUT}")

if __name__ == "__main__":
    main()
