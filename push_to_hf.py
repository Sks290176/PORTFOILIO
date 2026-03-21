import requests
import base64
import os
import json
from datetime import datetime

HF_TOKEN = os.environ.get("HF_TOKEN")
REPO_ID = "FinTuneAI/portfolio"
FILE_PATH = "highlights.json"

# Read the generated highlights.json
with open("highlights.json", "rb") as f:
    content = f.read()

encoded = base64.b64encode(content).decode("utf-8")

# Push to HuggingFace Space
response = requests.post(
    f"https://huggingface.co/api/spaces/{REPO_ID}/commit/main",
    headers={
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    },
    json={
        "commit_message": f"Auto-update highlights {datetime.utcnow().strftime('%Y-%m-%d')}",
        "operations": [
            {
                "key": FILE_PATH,
                "type": "file",
                "content": encoded,
                "encoding": "base64"
            }
        ]
    }
)

if response.status_code in [200, 201]:
    print(f"✅ Successfully pushed highlights.json to HuggingFace!")
else:
    print(f"❌ Failed: {response.status_code} — {response.text}")
    exit(1)
