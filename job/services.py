from dotenv import load_dotenv
import requests
import json
import os

load_dotenv()


def is_ai_generated_report(text: str) -> bool:
    """
    Check if the text is AI-generated using the ZeroGPT API.
    """
    url = "https://api.zerogpt.com/api/detect/detectText"
    headers = {
        "ApiKey": os.getenv("ZERO_GPT_API_KEY"),
        "Content-Type": "application/json",
    }
    payload = json.dumps({"input_text": text})
    response = requests.post(url, headers=headers, data=payload)
    return response.json()