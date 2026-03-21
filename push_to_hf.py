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

# Use the correct HuggingFace upload API
url = f"https://huggingface.co/api/spaces/{REPO_ID}/upload/main"

response = requests.post(
    url,
    headers={
        "Authorization": f"Bearer {HF_TOKEN}",
    },
    files={
        "file": (FILE_PATH, content, "application/json")
    },
    data={
        "path_in_repo": FILE_PATH,
        "commit_message": f"Auto-update highlights {datetime.utcnow().strftime('%Y-%m-%d')}"
    }
)

if response.status_code in [200, 201]:
    print(f"✅ Successfully pushed highlights.json to HuggingFace!")
else:
    print(f"❌ Failed: {response.status_code} — {response.text}")
    exit(1)
