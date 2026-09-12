from datetime import datetime

from fpdf import FPDF

from engine.resolver import get_cancellation_guide

PRIORITY_COLOR = {
    "high": (122, 77, 60),
    "medium": (128, 102, 46),
    "low": (79, 104, 102),
}
STATUS_COLOR = {
    "certain": (46, 90, 77),
    "uncertain": (103, 91, 78),
}
PRIORITY_WORD = {"high": "High priority", "medium": "Medium priority", "low": "Low priority"}
STATUS_WORD = {"certain": "Confirmed", "uncertain": "Unconfirmed - please verify"}

INK = (36, 50, 56)
MUTED = (94, 107, 112)
RULE = (216, 209, 198)


def _clean(text: str) -> str:
    replacements = {
        "—": " - ",
        "–": "-",
        "‘": "'",
        "’": "'",
        "“": '"',
        "”": '"',
        "…": "...",
    }
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    return text.encode("latin-1", "replace").decode("latin-1")


class ReportPDF(FPDF):
    report_date = ""

    def block(self, text, h=6, **kwargs):
        """multi_cell that always resets the cursor to the left margin on
        the next line — fpdf2's own default leaves the cursor at the right
        edge of the cell, which breaks any block written right after."""
        self.multi_cell(0, h, _clean(text), new_x="LMARGIN", new_y="NEXT", **kwargs)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*MUTED)
        self.cell(0, 10, _clean(f"What Remains - generated {self.report_date}"), align="C")


def _render_account(pdf: ReportPDF, account: dict, draft_text: str | None):
    priority = account.get("urgency", "low")
    status = account.get("status", "uncertain")

    if pdf.get_y() > 250:
        pdf.add_page()

    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(*INK)
    pdf.block(account["service_name"], h=8)

    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*PRIORITY_COLOR.get(priority, MUTED))
    pdf.cell(50, 6, _clean(PRIORITY_WORD.get(priority, priority)))
    pdf.set_text_color(*STATUS_COLOR.get(status, MUTED))
    pdf.cell(0, 6, _clean(STATUS_WORD.get(status, status)), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)

    pdf.set_text_color(*INK)
    pdf.set_font("Helvetica", "", 10)
    pdf.block(account.get("evidence", ""))

    if account.get("history_summary"):
        pdf.ln(1)
        pdf.set_fill_color(250, 247, 241)
        pdf.set_font("Helvetica", "", 10)
        pdf.block(account["history_summary"], fill=True)

    pdf.ln(1)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MUTED)
    pdf.block(f"Based on {len(account.get('source_email_ids', []))} email(s) found.", h=5)
    pdf.ln(2)

    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*INK)
    pdf.block("Recommended next step")

    guide = get_cancellation_guide(account["service_name"])
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*INK)
    if guide:
        for i, step in enumerate(guide["steps"], start=1):
            pdf.block(f"{i}. {step}")
        pdf.ln(1)
        pdf.set_font("Helvetica", "I", 8)
        pdf.set_text_color(*PRIORITY_COLOR["medium"])
        pdf.block(guide.get("note", ""), h=5)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(47, 93, 90)
        pdf.block(guide.get("url", ""), h=5)
    else:
        pdf.block(
            "We could not find a specific, verified cancellation "
            "procedure for this provider. We recommend checking their "
            "website directly or contacting their support."
        )
        if draft_text:
            pdf.ln(2)
            pdf.set_font("Helvetica", "B", 9)
            pdf.set_text_color(*INK)
            pdf.block("Draft message (not sent - review before sending):", h=5)
            pdf.set_font("Helvetica", "", 9)
            pdf.set_fill_color(255, 252, 247)
            pdf.block(draft_text, h=5, border=1, fill=True)

    pdf.ln(3)
    pdf.set_draw_color(*RULE)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
    pdf.ln(5)


def build_pdf_report(accounts: list[dict], drafts: dict | None = None) -> bytes:
    drafts = drafts or {}

    pdf = ReportPDF(format="A4")
    pdf.report_date = datetime.now().strftime("%Y-%m-%d")
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.set_margins(18, 18, 18)
    pdf.add_page()

    pdf.set_font("Times", "B", 24)
    pdf.set_text_color(*INK)
    pdf.block("What Remains", h=12)

    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*MUTED)
    pdf.block(f"Account discovery report - generated {pdf.report_date}")
    pdf.ln(3)

    pdf.set_fill_color(242, 247, 244)
    pdf.set_draw_color(200, 218, 210)
    pdf.set_text_color(*INK)
    pdf.set_font("Helvetica", "", 10)
    pdf.block(
        "Nothing has been sent or changed. This report lists what was "
        "found from the emails analyzed, for your own review at your own "
        "pace. Every action described below stays entirely in your hands.",
        border=1,
        fill=True,
    )
    pdf.ln(5)

    confirmed = sum(1 for a in accounts if a.get("status") == "certain")
    unconfirmed = len(accounts) - confirmed
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(*INK)
    pdf.block(
        f"{len(accounts)} account(s) found - {confirmed} confirmed, "
        f"{unconfirmed} unconfirmed.",
        h=7,
    )
    pdf.ln(4)

    if not accounts:
        pdf.set_font("Helvetica", "", 10)
        pdf.block(
            "No active accounts or subscriptions were found in what was "
            "analyzed."
        )

    for i, account in enumerate(accounts):
        unique_key = f"{i}_{account['service_name']}"
        _render_account(pdf, account, drafts.get(unique_key))

    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MUTED)
    pdf.block(
        "This report is not legal, financial, or professional advice. "
        "Verify details independently, especially where noted above.",
        h=5,
    )

    return bytes(pdf.output())
