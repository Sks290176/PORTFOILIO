import requests
import json
import os
from datetime import datetime
import feedparser

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

FEEDS = [
    "https://www.fatf-gafi.org/en/publications/rss.xml",
    "https://www.fca.org.uk/news/rss.xml",
    "https://feeds.reuters.com/reuters/businessNews",
]

def fetch_headlines():
    headlines = []
    for url in FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:5]:
                title = entry.get("title", "")
                if any(kw in title.lower() for kw in ["fraud","aml","money launder","sanction","compliance","financial crime","enforcement","fine","penalty","crypto","ai","artificial intelligence"]):
                    headlines.append(title)
        except:
            pass
    return headlines[:10]

today = datetime.utcnow().strftime("%d %b %Y")
headlines = fetch_headlines()
headline_context = "\n".join(f"- {h}" for h in headlines) if headlines else ""

if ANTHROPIC_API_KEY:
    prompt = f"""You are a senior financial crime intelligence analyst with 25+ years of experience. Today is {today}.

Generate exactly 2 concise briefing highlights for a financial crime intelligence ticker:
1. One on financial crime — a specific enforcement action, regulatory development, or notable typology
2. One on AI in financial crime — AI adoption by compliance teams OR AI misuse by bad actors

{f'Use these real headlines as inspiration:{chr(10)}{headline_context}' if headline_context else ''}

Return ONLY valid JSON, no markdown:
[
  {{
    "type": "fc",
    "text": "2-sentence financial crime highlight, under 200 characters",
    "lens": "1-2 sentence takeaway for senior FC investigators and leaders — what action or awareness this demands"
  }},
  {{
    "type": "ai",
    "text": "2-sentence AI in financial crime highlight, under 200 characters",
    "lens": "1-2 sentence strategic or operational implication for FC leaders"
  }}
]

Make highlights professional, specific, with concrete details. The lens should be sharp and practical."""

    try:
        res = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "Content-Type": "application/json",
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01"
            },
            json={
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 600,
                "messages": [{"role": "user", "content": prompt}]
            }
        )
        data = res.json()
        raw = "".join(item.get("text", "") for item in data["content"])
        raw = raw.replace("```json", "").replace("```", "").strip()
        items = json.loads(raw)
        payload = {
            "date": datetime.utcnow().strftime("%Y-%m-%d"),
            "items": [
                {"type": items[0]["type"], "text": items[0]["text"], "lens": items[0].get("lens", "")},
                {"type": items[1]["type"], "text": items[1]["text"], "lens": items[1].get("lens", "")}
            ]
        }
    except Exception as e:
        print(f"Claude API failed: {e}, using fallback")
        ANTHROPIC_API_KEY = None

if not ANTHROPIC_API_KEY:
    fc_text = headlines[0][:200] if headlines else "Global AML enforcement activity remains elevated with regulators issuing record fines for compliance failures."
    ai_text = headlines[1][:200] if len(headlines) > 1 else "AI-driven transaction monitoring tools are being rapidly adopted by FIUs to counter synthetic identity fraud."
    payload = {
        "date": datetime.utcnow().strftime("%Y-%m-%d"),
        "items": [
            {"type": "fc", "text": fc_text, "lens": "Senior investigators should assess whether their institution's controls would withstand similar regulatory scrutiny."},
            {"type": "ai", "text": ai_text, "lens": "FC leaders should evaluate their AI readiness roadmap and benchmark against emerging industry standards."}
        ]
    }

with open("highlights.json", "w") as f:
    json.dump(payload, f, indent=2)

print(f"✅ highlights.json generated for {payload['date']}")
print(json.dumps(payload, indent=2))
