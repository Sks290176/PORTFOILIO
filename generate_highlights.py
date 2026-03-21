import requests
import json
import os
from datetime import datetime
import feedparser

# Financial crime & AI news RSS feeds (all free, no API key needed)
FEEDS = [
    "https://www.fatf-gafi.org/en/publications/rss.xml",
    "https://www.fca.org.uk/news/rss.xml",
    "https://feeds.reuters.com/reuters/businessNews",
    "https://rss.app/feeds/financial-crime.xml",
]

def fetch_headlines():
    headlines = []
    for url in FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:3]:
                title = entry.get("title", "")
                if any(kw in title.lower() for kw in ["fraud","aml","money launder","sanction","compliance","financial crime","enforcement","fine","penalty","crypto","ai","artificial intelligence"]):
                    headlines.append(title)
        except:
            pass
    return headlines[:10]

today = datetime.utcnow().strftime("%d %b %Y")
headlines = fetch_headlines()
headline_text = "\n".join(f"- {h}" for h in headlines) if headlines else "No headlines fetched today."

fc_text = headlines[0] if len(headlines) > 0 else "Global AML enforcement activity remains elevated with regulators issuing record fines for compliance failures in 2025."
ai_text = headlines[1] if len(headlines) > 1 else "AI-driven transaction monitoring tools are being adopted rapidly by FIUs to counter synthetic identity fraud at scale."

# Trim to 170 chars
fc_text = fc_text[:170]
ai_text = ai_text[:170]

payload = {
    "date": datetime.utcnow().strftime("%Y-%m-%d"),
    "items": [
        {"type": "fc", "text": fc_text},
        {"type": "ai", "text": ai_text}
    ]
}

with open("highlights.json", "w") as f:
    json.dump(payload, f, indent=2)

print(f"✅ highlights.json generated for {payload['date']}")
print(json.dumps(payload, indent=2))
