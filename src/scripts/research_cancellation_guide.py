import json
import os
import sys

import requests
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from engine.classifier import get_client

load_dotenv()

_SCRIPTS_DIR = os.path.dirname(__file__)
PROMPT_PATH = os.path.join(_SCRIPTS_DIR, "..", "prompts", "guide_from_research.txt")
GUIDES_PATH = os.path.join(_SCRIPTS_DIR, "..", "..", "data", "cancellation_guides.json")

with open(PROMPT_PATH, encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()


def exa_search(query: str, num_results: int = 3) -> list[dict]:
    response = requests.post(
        "https://api.exa.ai/search",
        headers={
            "x-api-key": os.environ["EXA_API_KEY"],
            "content-type": "application/json",
        },
        json={
            "query": query,
            "numResults": num_results,
            "contents": {"text": {"maxCharacters": 2000}},
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json().get("results", [])


def build_guide(service_name: str) -> dict:
    results = exa_search(f"how to cancel {service_name} subscription official steps")

    excerpts = "\n\n---\n\n".join(
        f"Source: {r.get('url', '')}\n{r.get('text', '')}" for r in results
    )
    user_content = f"Service: {service_name}\n\nSearch results:\n\n{excerpts}"

    model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
    response = get_client().chat.completions.create(
        model=model,
        response_format={"type": "json_object"},
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ],
    )
    return json.loads(response.choices[0].message.content)


def add_guide(service_key: str, service_name: str):
    with open(GUIDES_PATH, encoding="utf-8") as f:
        guides = json.load(f)

    guides[service_key] = build_guide(service_name)

    with open(GUIDES_PATH, "w", encoding="utf-8") as f:
        json.dump(guides, f, indent=2)

    print(json.dumps(guides[service_key], indent=2))


if __name__ == "__main__":
    service = sys.argv[1] if len(sys.argv) > 1 else "Spotify"
    add_guide(service.lower(), service)
