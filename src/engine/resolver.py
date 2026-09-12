import json
import os
import re

_ENGINE_DIR = os.path.dirname(__file__)
GUIDES_PATH = os.path.join(_ENGINE_DIR, "..", "..", "data", "cancellation_guides.json")

with open(GUIDES_PATH, encoding="utf-8") as f:
    _GUIDES = json.load(f)


def _words(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def get_cancellation_guide(service_name: str) -> dict | None:
    normalized = service_name.strip().lower()
    if not normalized:
        return None
    if normalized in _GUIDES:
        return _GUIDES[normalized]

    normalized_words = _words(normalized)
    for key, guide in _GUIDES.items():
        key_words = _words(key)
        if key_words and key_words.issubset(normalized_words):
            return guide
    return None
