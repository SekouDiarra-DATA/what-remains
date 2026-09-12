import csv
import html
import io
import json
import os
import sys

import streamlit as st

sys.path.append(os.path.dirname(__file__))
from engine.classifier import get_accounts, synthesize_all
from engine.drafter import generate_draft
from engine.prioritizer import sort_by_urgency
from engine.report import build_pdf_report
from engine.resolver import get_cancellation_guide

DEMO_DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "demo_emails.json")

st.set_page_config(page_title="What Remains", layout="centered")

PRIORITY_WORD = {"high": "High priority", "medium": "Medium priority", "low": "Low priority"}
STATUS_WORD = {"certain": "Confirmed", "uncertain": "Unconfirmed — please verify"}
STATUS_CLASS = {"certain": "confirmed", "uncertain": "unconfirmed"}

CSS = """
<style>
:root {
    --wr-background: #F5F2EC;
    --wr-surface: #FFFCF7;
    --wr-surface-subtle: #EEEAE3;

    --wr-text-primary: #243238;
    --wr-text-muted: #5E6B70;

    --wr-border: #D8D1C6;
    --wr-border-strong: #B9B1A5;

    --wr-high: #7A4D3C;
    --wr-high-fill: #F0E5DF;

    --wr-medium: #80662E;
    --wr-medium-fill: #F1EADF;

    --wr-low: #4F6866;
    --wr-low-fill: #E7EFED;

    --wr-confirmed: #2E5A4D;
    --wr-confirmed-fill: #E5EEE8;

    --wr-unconfirmed: #675B4E;
    --wr-unconfirmed-fill: #EEEAE3;

    --wr-link: #2F5D5A;
    --wr-focus: #507C76;

    --wr-radius: 10px;
    --wr-control-radius: 8px;
    --wr-shadow: 0 2px 12px rgba(36, 50, 56, 0.05);
}

html, body, .stApp, [data-testid="stAppViewContainer"] {
    background: var(--wr-background);
    color: var(--wr-text-primary);
}

body, button, input, textarea, select, [data-testid="stMarkdownContainer"] {
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

.block-container {
    max-width: 760px;
    padding-top: 48px;
    padding-right: 20px;
    padding-bottom: 64px;
    padding-left: 20px;
}

[data-testid="stHeader"] { background: transparent; }

[data-testid="stMarkdownContainer"] p {
    color: var(--wr-text-primary);
    font-size: 16px;
    line-height: 1.55;
}

[data-testid="stMarkdownContainer"] strong {
    color: var(--wr-text-primary);
    font-weight: 650;
}

[data-testid="stCaptionContainer"], .stCaption, [data-testid="stMarkdownContainer"] small {
    color: var(--wr-text-muted);
    font-size: 14px;
    line-height: 1.4;
}

a {
    color: var(--wr-link);
    text-decoration-line: underline;
    text-decoration-thickness: 0.08em;
    text-underline-offset: 0.18em;
}
a:hover { color: var(--wr-text-primary); }

.wr-title-block { margin-bottom: 32px; }

.wr-product-title {
    margin: 0;
    color: var(--wr-text-primary);
    font-family: Georgia, "Times New Roman", serif;
    font-size: 40px;
    font-weight: 600;
    letter-spacing: -0.02em;
    line-height: 1.1;
}

.wr-page-title {
    margin: 0 0 12px 0;
    color: var(--wr-text-primary);
    font-size: 24px;
    font-weight: 650;
    letter-spacing: -0.01em;
    line-height: 1.25;
}

.wr-intro { max-width: 650px; margin-bottom: 24px; }
.wr-intro p { margin-bottom: 12px; }

.wr-rule { height: 1px; margin: 24px 0 28px 0; background: var(--wr-border); }

.wr-reassurance {
    margin: 0 0 24px 0;
    padding: 16px 18px;
    border: 1px solid #C8DAD2;
    border-left: 5px solid var(--wr-confirmed);
    border-radius: var(--wr-radius);
    background: #F2F7F4;
    color: var(--wr-text-primary);
    font-size: 16px;
    line-height: 1.5;
}
.wr-reassurance strong { font-weight: 700; }
.wr-reassurance p { margin: 0; }

.stButton > button {
    min-height: 44px;
    width: 100%;
    padding: 10px 16px;
    border: 1px solid var(--wr-border-strong);
    border-radius: var(--wr-control-radius);
    background: var(--wr-surface);
    color: var(--wr-text-primary);
    font-size: 16px;
    font-weight: 600;
    line-height: 1.2;
    box-shadow: none;
}
.stButton > button:hover {
    border-color: var(--wr-text-primary);
    background: #F0ECE5;
    color: var(--wr-text-primary);
}
.stButton > button[kind="primary"], .stButton > button[data-testid="baseButton-primary"] {
    border-color: var(--wr-low);
    background: var(--wr-low);
    color: #FFFFFF;
}
.stButton > button[kind="primary"]:hover, .stButton > button[data-testid="baseButton-primary"]:hover {
    border-color: #415754;
    background: #415754;
    color: #FFFFFF;
}

div[class*="st-key-footer_actions"] .stButton > button,
div[class*="st-key-top_actions"] .stButton > button {
    width: auto;
    min-height: 40px;
    padding: 8px 12px;
    font-size: 14px;
    font-weight: 550;
}

[data-testid="stCheckbox"] label { color: var(--wr-text-primary); font-size: 16px; line-height: 1.45; }
[data-testid="stCheckbox"] { margin: 8px 0 16px 0; }

[data-testid="stExpander"] {
    margin: 0 0 12px 0;
    border: 1px solid var(--wr-border);
    border-left: 4px solid var(--wr-border-strong);
    border-radius: var(--wr-radius);
    background: var(--wr-surface);
    box-shadow: var(--wr-shadow);
    overflow: hidden;
}
[data-testid="stExpander"] details { border: 0; background: transparent; }
[data-testid="stExpander"] summary {
    min-height: 64px;
    padding: 18px 20px;
    color: var(--wr-text-primary);
    font-size: 17px;
    font-weight: 600;
    line-height: 1.35;
}
[data-testid="stExpander"] summary:hover { background: #FAF7F1; }
[data-testid="stExpander"] summary:focus-visible { outline: 3px solid var(--wr-focus); outline-offset: -3px; }
[data-testid="stExpander"] [data-testid="stExpanderDetails"],
[data-testid="stExpander"] .streamlit-expanderContent {
    border-top: 1px solid var(--wr-border);
    padding: 20px;
}

[data-testid="stExpander"]:has(.wr-card-hook.wr-priority-high) { border-left-width: 5px; border-left-color: var(--wr-high); }
[data-testid="stExpander"]:has(.wr-card-hook.wr-priority-medium) { border-left-width: 4px; border-left-color: var(--wr-medium); }
[data-testid="stExpander"]:has(.wr-card-hook.wr-priority-low) { border-left-width: 3px; border-left-color: var(--wr-low); }
[data-testid="stExpander"]:has(.wr-card-hook.wr-status-confirmed) summary { font-weight: 650; }
[data-testid="stExpander"]:has(.wr-card-hook.wr-status-unconfirmed) summary { font-weight: 550; }
.wr-card-hook { display: none; }

.wr-tag-row { display: flex; flex-wrap: wrap; gap: 8px; margin: 0 0 16px 0; }
.wr-tag {
    display: inline-flex;
    align-items: center;
    min-height: 28px;
    padding: 5px 9px;
    border: 1px solid currentColor;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 650;
    line-height: 1;
    white-space: nowrap;
}
.wr-priority-high { color: var(--wr-high); background: var(--wr-high-fill); }
.wr-priority-medium { color: var(--wr-medium); background: var(--wr-medium-fill); }
.wr-priority-low { color: var(--wr-low); background: var(--wr-low-fill); }
.wr-status-confirmed { color: var(--wr-confirmed); background: var(--wr-confirmed-fill); }
.wr-status-unconfirmed { color: var(--wr-unconfirmed); background: var(--wr-unconfirmed-fill); }

.wr-evidence { margin: 0 0 16px 0; color: var(--wr-text-primary); font-size: 16px; line-height: 1.55; }
.wr-history {
    margin: 0 0 8px 0;
    padding: 14px 16px;
    border-left: 3px solid var(--wr-border-strong);
    background: #FAF7F1;
    color: var(--wr-text-primary);
    font-size: 16px;
    line-height: 1.5;
}
.wr-source-count { margin: 0 0 4px 0; color: var(--wr-text-muted); font-size: 14px; line-height: 1.4; }
.wr-source-list { margin: 0 0 24px 0; padding-left: 20px; color: var(--wr-text-muted); font-size: 13px; line-height: 1.5; }

.wr-next-step { margin-top: 20px; padding-top: 20px; border-top: 1px solid var(--wr-border); }
.wr-next-step-heading { margin: 0 0 12px 0; color: var(--wr-text-primary); font-size: 17px; font-weight: 650; line-height: 1.35; }
.wr-next-step ol, .wr-next-step ul { margin-top: 8px; margin-bottom: 16px; padding-left: 24px; color: var(--wr-text-primary); font-size: 16px; line-height: 1.55; }
.wr-next-step li + li { margin-top: 8px; }

.wr-caveat {
    margin: 16px 0;
    padding: 12px 14px;
    border-left: 3px solid var(--wr-medium);
    background: var(--wr-medium-fill);
    color: var(--wr-text-primary);
    font-size: 14px;
    line-height: 1.45;
}
.wr-no-procedure {
    margin: 0 0 16px 0;
    padding: 14px 16px;
    border: 1px solid var(--wr-border);
    border-radius: 8px;
    background: var(--wr-surface-subtle);
    color: var(--wr-text-primary);
    font-size: 16px;
    line-height: 1.5;
}
.wr-draft-note { margin: 8px 0 12px 0; color: var(--wr-text-muted); font-size: 14px; line-height: 1.4; }

.stTextArea textarea, .stTextInput input {
    border: 1px solid var(--wr-border-strong);
    border-radius: var(--wr-control-radius);
    background: var(--wr-surface);
    color: var(--wr-text-primary);
    font-size: 16px;
    line-height: 1.5;
}
.stTextArea textarea { min-height: 180px; padding: 14px; }
.stTextArea textarea:focus, .stTextInput input:focus { border-color: var(--wr-focus); box-shadow: 0 0 0 1px var(--wr-focus); }

.wr-footer { margin-top: 32px; padding-top: 24px; border-top: 1px solid var(--wr-border); }
.wr-footer-caption { margin-top: 8px; color: var(--wr-text-muted); font-size: 14px; line-height: 1.4; }

:where(button, a, input, textarea, select, [role="button"]):focus-visible {
    outline: 3px solid var(--wr-focus);
    outline-offset: 2px;
}

[data-testid="stAlert"] svg { display: none; }
[data-testid="stAlert"] {
    border-radius: var(--wr-radius);
    border-left: 5px solid var(--wr-confirmed);
    background: #F2F7F4;
    color: var(--wr-text-primary);
}

@media (max-width: 640px) {
    .block-container { padding-top: 32px; padding-right: 16px; padding-bottom: 48px; padding-left: 16px; }
    .wr-product-title { font-size: 34px; }
    [data-testid="stExpander"] summary { min-height: 60px; padding: 16px; }
    [data-testid="stExpander"] [data-testid="stExpanderDetails"],
    [data-testid="stExpander"] .streamlit-expanderContent { padding: 16px; }
}

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms;
        animation-iteration-count: 1;
        scroll-behavior: auto;
        transition-duration: 0.01ms;
    }
}
</style>
"""


def inject_css():
    st.markdown(CSS, unsafe_allow_html=True)


def run_analysis():
    with open(DEMO_DATA_PATH, encoding="utf-8") as f:
        emails = json.load(f)
    accounts = get_accounts(emails)
    return sort_by_urgency(accounts)


def render_consent_screen():
    st.markdown(
        '<div class="wr-title-block"><h1 class="wr-product-title">What Remains</h1></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="wr-intro">
        <p>A quiet way to find out what still needs attention.</p>
        <p>When someone passes away, their digital accounts and subscriptions
        don't stop on their own. Finding out what is still active is often
        the hardest part — not cancelling it, but discovering it in the
        first place.</p>
        <p><strong>What this tool does:</strong> it reads through a set of
        emails and reconstructs which accounts and subscriptions appear to
        still be active, organized by how urgent they are.</p>
        <p><strong>Where that analysis happens:</strong> email content is
        sent to a third-party AI provider (an OpenAI-compatible API) to be
        analyzed. Nothing is stored by this tool beyond your current
        session.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="wr-reassurance"><p><strong>What this tool never does:</strong>
        it never sends a message, cancels a service, or changes anything on
        your behalf. Every action stays in your hands, at your own pace.</p></div>
        """,
        unsafe_allow_html=True,
    )

    consent = st.checkbox(
        "I understand, and I have the right to access this information."
    )

    st.markdown('<div class="wr-rule"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="wr-page-title">Connect the account</div>',
        unsafe_allow_html=True,
    )
    st.caption(
        "Sign in with the account's own email address. Only read access is "
        "requested — nothing is read, sent, or changed without you seeing "
        "it happen here first."
    )

    try:
        import engine.gmail_client as gmail_client  # noqa: F401

        gmail_ready = True
    except ImportError:
        gmail_ready = False

    if st.button(
        "Connect a Gmail account",
        disabled=not consent or not gmail_ready,
        type="primary",
    ):
        progress = st.empty()
        try:
            progress.info(
                "Opening a browser window to sign in — please approve "
                "read-only access, then return here."
            )
            emails = gmail_client.fetch_recent_emails()

            if not emails:
                progress.empty()
                st.warning(
                    "No emails were found in this account. If this seems "
                    "wrong, try a different email address the person may "
                    "have used, or check a recent bank statement for clues "
                    "about active accounts."
                )
            else:
                progress.info(
                    f"Read {len(emails)} recent emails. Reconstructing "
                    f"account history for each service — this can take a "
                    f"while for a real inbox with many senders..."
                )
                accounts = sort_by_urgency(synthesize_all(emails))
                progress.empty()
                st.session_state.accounts = accounts
                st.rerun()
        except FileNotFoundError:
            progress.empty()
            st.error(
                "Gmail connection isn't fully configured on this machine "
                "yet — a required setup file is missing. See the project "
                "README for setup steps."
            )
        except Exception:
            progress.empty()
            st.error(
                "Something went wrong while reading or analyzing this "
                "inbox. Nothing was changed. You can try again, or use the "
                "sample inbox below in the meantime."
            )

    if not gmail_ready:
        st.caption(
            "Gmail connection isn't installed on this machine yet — see "
            "the README for setup steps."
        )

    st.markdown('<div class="wr-rule"></div>', unsafe_allow_html=True)
    with st.expander("No account to connect right now? Try a sample inbox"):
        st.caption(
            "For demonstration purposes — a simulated, privacy-safe set of "
            "emails, not a real inbox."
        )
        if st.button("Load the sample email export", disabled=not consent):
            progress = st.empty()
            progress.info("Reading emails and grouping them by sender...")
            progress.info("Reconstructing account history for each service...")
            accounts = run_analysis()
            progress.empty()
            st.session_state.accounts = accounts
            st.rerun()


def _csv_safe(value: str) -> str:
    """Neutralizes leading =, +, -, @ so spreadsheet apps (Excel, Sheets)
    never interpret a cell as a formula — the source text comes from
    LLM output derived from email content we don't control."""
    text = str(value)
    if text and text[0] in ("=", "+", "-", "@"):
        return "'" + text
    return text


def build_csv(accounts):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(
        ["Service", "Category", "Status", "Urgency", "Evidence", "History", "Emails found"]
    )
    for a in accounts:
        writer.writerow(
            [
                _csv_safe(a["service_name"]),
                _csv_safe(a["category"]),
                a["status"],
                a["urgency"],
                _csv_safe(a["evidence"]),
                _csv_safe(a.get("history_summary", "")),
                len(a["source_email_ids"]),
            ]
        )
    return output.getvalue()


def render_card_hook(urgency: str, status: str):
    status_class = STATUS_CLASS.get(status, "unconfirmed")
    st.markdown(
        f'<span class="wr-card-hook wr-priority-{urgency} wr-status-{status_class}" '
        f'aria-hidden="true"></span>',
        unsafe_allow_html=True,
    )


def render_tag_row(urgency: str, status: str):
    status_class = STATUS_CLASS.get(status, "unconfirmed")
    priority_word = PRIORITY_WORD.get(urgency, urgency)
    status_word = STATUS_WORD.get(status, status)
    st.markdown(
        f"""
        <div class="wr-tag-row">
            <span class="wr-tag wr-priority-{urgency}">{priority_word}</span>
            <span class="wr-tag wr-status-{status_class}">{status_word}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def reset_session():
    del st.session_state.accounts
    st.session_state.drafts = {}
    st.rerun()


def render_results_screen():
    accounts = st.session_state.accounts
    if "drafts" not in st.session_state:
        st.session_state.drafts = {}

    top_left, top_right = st.columns([3, 1])
    with top_left:
        st.markdown(
            '<div class="wr-page-title">What Remains</div>', unsafe_allow_html=True
        )
    with top_right:
        with st.container(key="top_actions"):
            if st.button("← Back", key="back_top"):
                reset_session()

    st.markdown(
        """
        <div class="wr-reassurance"><p>Here is what we found from the emails
        analyzed. Nothing has been sent or changed — this is entirely yours
        to review, at your own pace.</p></div>
        """,
        unsafe_allow_html=True,
    )

    if not accounts:
        st.markdown(
            """
            <div class="wr-no-procedure">We couldn't find any active
            accounts or subscriptions in what was analyzed. This can happen
            if the inbox was lightly used, or is an older address. It may
            help to try another email address the person used, or to check
            a recent bank or card statement for recurring charges.</div>
            """,
            unsafe_allow_html=True,
        )

    for i, account in enumerate(accounts):
        priority_word = PRIORITY_WORD.get(account["urgency"], account["urgency"])
        status_word = STATUS_WORD.get(account["status"], account["status"])
        header = f"{account['service_name']} — {priority_word} · {status_word}"
        unique_key = f"{i}_{account['service_name']}"

        with st.expander(header):
            render_card_hook(account["urgency"], account["status"])
            render_tag_row(account["urgency"], account["status"])

            st.markdown(
                f'<div class="wr-evidence">{html.escape(account["evidence"])}</div>',
                unsafe_allow_html=True,
            )
            if account.get("history_summary"):
                st.markdown(
                    f'<div class="wr-history">{html.escape(account["history_summary"])}</div>',
                    unsafe_allow_html=True,
                )
            source_emails = account.get("source_emails") or []
            if source_emails:
                rows = "".join(
                    f"<li>{html.escape(e.get('date', ''))} — "
                    f"{html.escape(e.get('subject', ''))}</li>"
                    for e in source_emails
                )
                st.markdown(
                    f'<div class="wr-source-count">Based on '
                    f'{len(source_emails)} email(s) found in the analyzed '
                    f'export:</div><ul class="wr-source-list">{rows}</ul>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f'<div class="wr-source-count">Based on '
                    f'{len(account["source_email_ids"])} email(s) found in '
                    f'the analyzed export.</div>',
                    unsafe_allow_html=True,
                )

            guide = get_cancellation_guide(account["service_name"])
            if guide:
                steps_html = "".join(
                    f"<li>{html.escape(step)}</li>" for step in guide["steps"]
                )
                safe_url = html.escape(guide["url"])
                st.markdown(
                    f"""
                    <div class="wr-next-step">
                        <div class="wr-next-step-heading">Recommended next step</div>
                        <ol>{steps_html}</ol>
                        <div class="wr-caveat">{html.escape(guide["note"])}</div>
                        <p><a href="{safe_url}" target="_blank" rel="noopener noreferrer">Official page</a></p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    """
                    <div class="wr-next-step">
                        <div class="wr-next-step-heading">Recommended next step</div>
                        <div class="wr-no-procedure">We could not find a
                        specific, verified cancellation procedure for this
                        provider. We recommend checking their website
                        directly or contacting their support.</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if account["status"] != "certain":
                    st.markdown(
                        '<div class="wr-draft-note">We are not confident '
                        "this is an active account, so we won't draft a "
                        "message stating it should be closed. Verify it "
                        "directly first.</div>",
                        unsafe_allow_html=True,
                    )
                else:
                    if st.button(
                        "Draft a message to their support",
                        key=f"draft_btn_{unique_key}",
                    ):
                        with st.spinner("Drafting a message — nothing will be sent."):
                            st.session_state.drafts[unique_key] = generate_draft(account)
                        st.rerun()
                    if unique_key in st.session_state.drafts:
                        draft_area_key = f"draft_area_{unique_key}"
                        st.text_area(
                            "Draft message — not sent, review and adapt before sending",
                            value=st.session_state.drafts[unique_key],
                            height=160,
                            key=draft_area_key,
                        )
                        st.session_state.drafts[unique_key] = st.session_state[draft_area_key]
                        st.markdown(
                            '<div class="wr-draft-note">This message has not '
                            "been sent anywhere. Copy it, adjust it if needed, "
                            "and send it yourself through your usual "
                            "channel.</div>",
                            unsafe_allow_html=True,
                        )

    st.markdown('<div class="wr-footer"></div>', unsafe_allow_html=True)
    with st.container(key="footer_actions"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.download_button(
                "Download checklist as CSV",
                data=build_csv(accounts),
                file_name="what_remains_checklist.csv",
                mime="text/csv",
            )
        with col2:
            st.download_button(
                "Download full report as PDF",
                data=build_pdf_report(accounts, st.session_state.drafts),
                file_name="what_remains_report.pdf",
                mime="application/pdf",
            )
        with col3:
            if st.button("Start over", key="back_bottom"):
                reset_session()
    st.markdown(
        '<div class="wr-footer-caption">The PDF report includes every '
        "account, the evidence found, and any draft messages you generated "
        "— ready to share with family or a professional if needed.</div>",
        unsafe_allow_html=True,
    )


inject_css()

if "accounts" not in st.session_state:
    render_consent_screen()
else:
    render_results_screen()
