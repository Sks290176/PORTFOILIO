import os
import json
from datetime import datetime

HF_TOKEN = os.environ.get("HF_TOKEN")

# Install huggingface_hub
os.system("pip install huggingface_hub -q")

from huggingface_hub import HfApi

api = HfApi(token=HF_TOKEN)

api.upload_file(
    path_or_fileobj="highlights.json",
    path_in_repo="highlights.json",
    repo_id="SunilKSingh/portfolio",
    repo_type="space",
    commit_message=f"Auto-update highlights {datetime.utcnow().strftime('%Y-%m-%d')}"
)

print("✅ Successfully pushed highlights.json to HuggingFace!")
