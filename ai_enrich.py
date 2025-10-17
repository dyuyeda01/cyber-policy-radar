import os, json, time
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

ROOT = Path(__file__).parent
DATA_PATH = ROOT / "public" / "data" / "articles.json"
OUT_PATH = ROOT / "public" / "data" / "articles_ai.json"

def main():
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️ No OpenAI API key found. Skipping AI enrichment.")
        return

    client = OpenAI(api_key=api_key)
    data = json.loads(DATA_PATH.read_text())
    items = data.get("items", [])
    enriched = []

    for idx, item in enumerate(items, 1):
        content = f"Title: {item['title']}\nSummary: {item.get('summary','')}"
        prompt = f"""You are a cyber policy analyst AI.
        Given this article title and summary, produce:
        - A concise summary (1-2 sentences)
        - Policy type (choose from: regulation, advisory, incident, defense, international)
        - Optional sentiment (positive/neutral/negative)
        Return as JSON: {{"summary_ai": "...", "policy_type": "...", "sentiment": "..."}}"""
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert in global cyber policy."},
                    {"role": "user", "content": prompt + "\n\n" + content}
                ],
                temperature=0.3,
            )
            item["ai_analysis"] = response.choices[0].message.content
            print(f"[{idx}/{len(items)}] ✅ Enriched: {item['title'][:70]}...")
            enriched.append(item)
            time.sleep(0.5)
        except Exception as e:
            print(f"[{idx}/{len(items)}] ⚠️ Error: {e}")
            enriched.append(item)

    OUT_PATH.write_text(json.dumps({"items": enriched}, indent=2))
    print(f"✨ AI enrichment complete → {OUT_PATH}")

if __name__ == "__main__":
    main()
