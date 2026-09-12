_URGENCY_ORDER = {"high": 0, "medium": 1, "low": 2}


def sort_by_urgency(accounts: list[dict]) -> list[dict]:
    return sorted(accounts, key=lambda a: _URGENCY_ORDER.get(a.get("urgency"), 3))
