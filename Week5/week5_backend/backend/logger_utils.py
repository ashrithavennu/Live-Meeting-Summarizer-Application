import json
import os
from datetime import datetime

def save_log(transcript, summary):
    os.makedirs("logs", exist_ok=True)

    filename = f"logs/meeting_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    data = {
        "transcript": transcript,
        "summary": summary
    }

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

    print(f"✅ Log saved: {filename}")