# cyber-policy-radar
This is a site to provide you with the latest cyber policy alerts for the US and UK. 

# Cyber Policy Radar (MVP)
Aggregates recent cyber policy articles by region/country. Runs free without AI; optional AI enrichment can be turned on with an OpenAI API key.

## Quick Start
```bash
pip install -r requirements.txt
python fetch_feeds.py
python -m http.server --directory public 8080
```

## Enable AI Enrichment
Create a `.env` file:
```
OPENAI_API_KEY=sk-your-key-here
```
Then run:
```bash
python ai_enrich.py
```
