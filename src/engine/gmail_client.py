import base64
import os
import pickle
from datetime import datetime
from email.utils import parseaddr, parsedate_to_datetime

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

_ENGINE_DIR = os.path.dirname(__file__)
CREDENTIALS_PATH = os.path.join(_ENGINE_DIR, "..", "..", "data", "gmail_oauth_credentials.json")
TOKEN_PATH = os.path.join(_ENGINE_DIR, "..", "..", "data", "gmail_token.pickle")

MAX_BODY_CHARS = 2000


def get_gmail_service():
    creds = None
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, "rb") as f:
            creds = pickle.load(f)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, "wb") as f:
            pickle.dump(creds, f)

    return build("gmail", "v1", credentials=creds)


def _decode_part(data: str) -> str:
    padded = data + "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(padded).decode("utf-8", errors="replace")


def _extract_body(payload: dict) -> str:
    if payload.get("mimeType") == "text/plain" and payload.get("body", {}).get("data"):
        return _decode_part(payload["body"]["data"])

    for part in payload.get("parts", []) or []:
        text = _extract_body(part)
        if text:
            return text

    if payload.get("mimeType", "").startswith("text/") and payload.get("body", {}).get("data"):
        return _decode_part(payload["body"]["data"])

    return ""


def _header(headers: list[dict], name: str) -> str:
    for h in headers:
        if h["name"].lower() == name.lower():
            return h["value"]
    return ""


BILLING_QUERY = (
    "receipt OR subscription OR renewal OR renewed OR invoice OR payment "
    "OR billing OR membership OR plan"
)


def fetch_recent_emails(max_results: int = 150, query: str = BILLING_QUERY) -> list[dict]:
    """Reads emails from the connected inbox (read-only) and converts them
    into the same {id, date, from_name, from_email, subject, body} shape the
    rest of the pipeline already expects.

    Gmail's inbox can hold years of history, so this targets billing-related
    keywords (query) rather than only the most recent N messages — a
    six-month-old renewal notice is exactly the kind of evidence this tool
    needs, and a purely recency-based fetch would miss it. This still isn't
    a full-mailbox scan (see docs/architecture.md section 7)."""
    service = get_gmail_service()
    message_ids = []
    page_token = None
    while len(message_ids) < max_results:
        response = (
            service.users()
            .messages()
            .list(
                userId="me",
                q=query,
                maxResults=min(100, max_results - len(message_ids)),
                pageToken=page_token,
            )
            .execute()
        )
        message_ids.extend(m["id"] for m in response.get("messages", []))
        page_token = response.get("nextPageToken")
        if not page_token:
            break

    emails = []
    for msg_id in message_ids:
        msg = service.users().messages().get(userId="me", id=msg_id, format="full").execute()
        headers = msg["payload"]["headers"]

        from_name, from_email = parseaddr(_header(headers, "From"))
        if not from_name:
            from_name = from_email or "Unknown sender"
        if not from_email:
            continue

        date_header = _header(headers, "Date")
        try:
            date = parsedate_to_datetime(date_header).strftime("%Y-%m-%d")
        except Exception:
            date = datetime.fromtimestamp(int(msg["internalDate"]) / 1000).strftime("%Y-%m-%d")

        body = _extract_body(msg["payload"])[:MAX_BODY_CHARS] or msg.get("snippet", "")

        emails.append(
            {
                "id": msg_id,
                "date": date,
                "from_name": from_name,
                "from_email": from_email,
                "subject": _header(headers, "Subject"),
                "body": body,
            }
        )

    return emails
