import json
import os
import re
import time
from collections import defaultdict

from dotenv import load_dotenv
from openai import OpenAI, RateLimitError

load_dotenv()

_ENGINE_DIR = os.path.dirname(__file__)
PROMPT_PATH = os.path.join(_ENGINE_DIR, "..", "prompts", "synthesize.txt")
DEMO_DATA_PATH = os.path.join(_ENGINE_DIR, "..", "..", "data", "demo_emails.json")
CACHE_PATH = os.path.join(_ENGINE_DIR, "..", "..", "data", "analysis_cache.json")

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


def _sender_domain(email_address: str) -> str:
    return email_address.split("@")[-1].lower() if "@" in email_address else email_address.lower()


_NAME_NOISE_WORDS = {
    "the", "team", "support", "billing", "notifications", "notification",
    "noreply", "no-reply", "official", "help", "info", "service", "services",
}


def _normalize_name(name: str) -> str:
    """Strips generic words ("The Netflix Team" -> "netflix") so the same
    service isn't fragmented by minor display-name variation, while
    unrelated services sharing a domain (Google One vs Google Play) still
    keep their distinguishing words and stay separate."""
    words = re.findall(r"[a-z0-9]+", name.lower())
    core = [w for w in words if w not in _NAME_NOISE_WORDS]
    return " ".join(core) or " ".join(words)


def group_by_service(emails: list[dict]) -> dict[tuple[str, str], list[dict]]:
    """Groups by (sending domain, normalized display name) rather than
    either alone. Domain alone is too coarse — large providers (e.g.
    google.com) send for many unrelated services, which would wrongly
    merge Google One and Google Play into one account. Raw display name
    alone is too loose in the other direction — two genuinely different
    senders can share a display name (seen in testing: two different
    "AI Tinkerers" senders on different domains), and one real service can
    vary its own display name slightly ("Netflix" vs "The Netflix Team").
    Normalizing the name before comparing handles that last case too."""
    groups = defaultdict(list)
    for email in emails:
        key = (_sender_domain(email["from_email"]), _normalize_name(email["from_name"]))
        groups[key].append(email)
    for group in groups.values():
        group.sort(key=lambda e: e["date"])
    return groups


def synthesize_account(from_name: str, emails: list[dict]) -> dict:
    model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

    emails_block = "\n\n".join(
        f"[{e['date']}] From: {e['from_name']} <{e['from_email']}>\n"
        f"Subject: {e['subject']}\n{e['body']}"
        for e in emails
    )
    user_content = f"Sender: {from_name}\n\nEmails found (chronological):\n\n{emails_block}"

    max_retries = 5
    for attempt in range(max_retries):
        try:
            response = get_client().chat.completions.create(
                model=model,
                response_format={"type": "json_object"},
                temperature=0,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_content},
                ],
            )
            break
        except RateLimitError:
            if attempt == max_retries - 1:
                raise
            wait = 15 * (attempt + 1)
            print(f"Rate limit hit for {from_name}, waiting {wait}s before retry...")
            time.sleep(wait)

    try:
        raw = json.loads(response.choices[0].message.content)
    except (json.JSONDecodeError, TypeError):
        raw = {}
    if not isinstance(raw, dict):
        raw = {}

    result = {
        "service_name": str(raw.get("service_name") or from_name),
        "category": str(raw.get("category") or "other"),
        "status": raw.get("status") if raw.get("status") in ("certain", "uncertain") else "uncertain",
        "urgency": raw.get("urgency") if raw.get("urgency") in ("high", "medium", "low") else "low",
        "evidence": str(raw.get("evidence") or "No further detail was provided."),
        "reasoning": str(raw.get("reasoning") or ""),
        "history_summary": str(raw.get("history_summary") or ""),
    }
    result["source_email_ids"] = [e["id"] for e in emails]
    result["source_emails"] = [
        {"date": e["date"], "subject": e["subject"]} for e in emails
    ]
    result["last_email_date"] = emails[-1]["date"]
    return result


def synthesize_all(emails: list[dict]) -> list[dict]:
    groups = group_by_service(emails)
    delay = float(os.environ.get("SYNTH_CALL_DELAY_SECONDS", "2"))
    results = []
    for i, ((domain, _name), group) in enumerate(groups.items()):
        label = group[0]["from_name"] or domain
        if i > 0:
            time.sleep(delay)
        results.append(synthesize_account(label, group))
    return results


def load_cached_accounts() -> list[dict] | None:
    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, encoding="utf-8") as f:
            return json.load(f)
    return None


def save_cache(accounts: list[dict]) -> None:
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(accounts, f, indent=2)


def get_accounts(emails: list[dict], force_refresh: bool = False) -> list[dict]:
    """Returns cached analysis results when available (instant, used by the
    live demo) or runs the real synthesis and caches it (used to prepare or
    refresh that cache ahead of time)."""
    if not force_refresh:
        cached = load_cached_accounts()
        if cached is not None:
            return cached
    accounts = synthesize_all(emails)
    save_cache(accounts)
    return accounts


if __name__ == "__main__":
    with open(DEMO_DATA_PATH, encoding="utf-8") as f:
        demo_emails = json.load(f)

    for account in get_accounts(demo_emails, force_refresh=True):
        print(json.dumps(account, indent=2))
        print("-" * 60)
