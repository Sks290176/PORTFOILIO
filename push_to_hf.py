import requests
import base64
import os
from datetime import datetime

HF_TOKEN = os.environ.get("HF_TOKEN")
REPO_ID = "FinTuneAI/portfolio"
FILE_PATH = "highlights.json"

with open("highlights.json", "rb") as f:
    content = f.read()

encoded = base64.b64encode(content).decode("utf-8")

# Correct HuggingFace Hub API endpoint
response = requests.post(
    f"https://huggingface.co/api/repos/FinTuneAI/portfolio/commit/main",
    headers={
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    },
    json={
        "summary": f"Auto-update highlights {datetime.utcnow().strftime('%Y-%m-%d')}",
        "files": [
            {
                "path": FILE_PATH,
                "content": encoded,
                "encoding": "base64"
            }
        ]
    },
    params={"repoType": "space"}
)

if response.status_code in [200, 201]:
    print(f"✅ Successfully pushed highlights.json to HuggingFace!")
    print(response.json())
else:
    print(f"❌ Failed: {response.status_code} — {response.text}")
    exit(1)
