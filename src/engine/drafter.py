import os
import time

from dotenv import load_dotenv
from openai import OpenAI, RateLimitError

load_dotenv()

_ENGINE_DIR = os.path.dirname(__file__)
PROMPT_PATH = os.path.join(_ENGINE_DIR, "..", "prompts", "draft.txt")

with open(PROMPT_PATH, encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

_client = None


def get_client() -> OpenAI:
    global _client
    if _client is None:
        kwargs = {"api_key": os.environ["OPENAI_API_KEY"]}
        base_url = os.environ.get("OPENAI_BASE_URL")
        if base_url:
            kwargs["base_url"] = base_url
        _client = OpenAI(**kwargs)
    return _client


def generate_draft(account: dict) -> str:
    model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
    user_content = (
        f"Service: {account['service_name']}\n"
        f"Category: {account['category']}\n"
        f"Evidence: {account['evidence']}\n"
        f"History: {account.get('history_summary', '')}\n"
    )

    max_retries = 5
    for attempt in range(max_retries):
        try:
            response = get_client().chat.completions.create(
                model=model,
                temperature=0.3,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_content},
                ],
            )
            return response.choices[0].message.content.strip()
        except RateLimitError:
            if attempt == max_retries - 1:
                raise
            time.sleep(15 * (attempt + 1))
