# What Remains

Built for **"Agents, Everywhere: Bots, Channels, & More"** — the AI Tinkerers global hackathon, in partnership with Orange Digital Center Mali (Bamako, September 12, 2026).

## The problem

Around 63 million people die every year. Almost none of them leave behind any instructions for their digital accounts — subscriptions, bank auto-payments, cloud storage — which simply keep running. Studies show close to half of people have no plan at all for this. And the hardest part for the grieving family left behind is rarely *cancelling* an account once they know about it — it's *discovering* that it exists in the first place, buried across hundreds of emails, at the exact moment they have the least energy to look.

## The solution

**What Remains** is an agent that lives inside a deceased person's email history. Instead of sorting emails one by one like a generic inbox assistant, it:

1. **Groups emails by service** and reconstructs a single account profile from the relevant traces found in the analyzed inbox — a signup, a price change, a payment receipt — into one coherent history (e.g. *"Active since November 2025, price increased in July 2026, last payment in August 2026"*).
2. **Distinguishes what it's sure of from what it isn't.** A one-time promotional email is never treated as proof of an active paid account.
3. **Looks up the real cancellation procedure** for well-documented providers (a curated, verified guide — not a live, unverifiable web scrape), or honestly says it couldn't find one and offers to draft a support message instead.
4. **Never takes an irreversible action.** It never sends a message, cancels a service, or changes anything on its own — every action stays in the user's hands, at their own pace.
5. **Produces a tangible, shareable deliverable.** A full PDF report (evidence, reconstructed history, recommended steps, and any drafted messages) that can be shared with family members or a professional such as a notary, alongside a plain CSV export.

Built for the family member — not the tech-savvy user — who just needs a clear, prioritized answer to "what's left to deal with, and in what order."

### Why the email channel specifically matters

This isn't a generic "AI agent + email" pairing. The information needed to solve this problem — which accounts exist, which are still active — *only* exists scattered across a real inbox. An agent living anywhere else (a chat window, a form) couldn't reconstruct it. The channel is the problem's constitutive context, not an interchangeable delivery choice.

## Tech stack

- **Python + Streamlit** — single-file, no front/back split, fast to build solo under hackathon time constraints
- **LLM (OpenAI-compatible API — OpenRouter)** for email-group synthesis and draft-message generation
- **A curated cancellation-guide knowledge base** (`data/cancellation_guides.json`) for well-known providers, researched and verified offline using **Exa** (`src/scripts/research_cancellation_guide.py`) — deliberately not a live in-app web search, to avoid presenting unverified information with false confidence during actual use
- **CSV export** of the final prioritized checklist, and a **full PDF report** (`src/engine/report.py`, via `fpdf2`) with evidence, history, recommended steps, and any drafted messages — a tangible document a family member can keep or hand to a professional
- No database — session-scoped only, by design, for this MVP

## How to run it

Requires Python 3.10+ (the code uses modern type hints like `list[dict]` and `X | None`).

```bash
pip install -r requirements.txt
cp .env.example .env   # then fill in your own credentials, see below
streamlit run src/app.py
```

The app ships with a pre-computed analysis cache (`data/analysis_cache.json`) built from a simulated demo email export (`data/demo_emails.json`) — no real inbox, for obvious privacy reasons. Delete the cache file and it will regenerate live from the API on next run.

### Credentials and separate processes required

| Variable / file | Required for | How to get it |
|---|---|---|
| `OPENAI_API_KEY`, `OPENAI_MODEL`, `OPENAI_BASE_URL` | Core agent (email synthesis, draft generation) — works with any OpenAI-compatible provider | An OpenRouter, OpenAI, or Google AI Studio key (`.env.example` has ready-made presets for each) |
| `EXA_API_KEY` | Optional — only needed to re-run `src/scripts/research_cancellation_guide.py` and add/refresh an entry in `data/cancellation_guides.json` | [dashboard.exa.ai](https://dashboard.exa.ai) |
| `data/gmail_oauth_credentials.json` (not committed) | Optional — only needed for the real-Gmail connection path (`src/engine/gmail_client.py`), not used in the demo dataset path | Google Cloud Console → enable Gmail API → OAuth consent screen (readonly scope) → OAuth client ID (Desktop app) |

No credential, token, or account secret is committed to this repository (see `.gitignore`) — none is required to review the code, and the demo dataset path only needs the first row above to run.

## Connecting a real account vs. the sample inbox

The app's primary, most-emphasized action is connecting a real Gmail account, read-only (`src/engine/gmail_client.py`) — this is the actual product experience: sign in, approve read-only access, see the results. It was validated against a real personal inbox and correctly reconstructed 20 distinct services, marking only the ones with real billing evidence as confirmed and leaving the rest honestly unconfirmed.

A simulated, privacy-safe "sample inbox" is available as a secondary, collapsed option for anyone without an account to connect right now (including judges reviewing this repo). **The public demo video and this submission's screenshots use only the sample inbox path** — never the real Gmail connection — for obvious privacy reasons. See [`docs/architecture.md`](docs/architecture.md) section 7 for why the real-account path is a local/developer feature at this stage, not yet a public-deployment-ready one (Google app verification and a multi-user-safe OAuth flow would both be required first).

## What this MVP deliberately does not do

(See [`docs/architecture.md`](docs/architecture.md) for the full technical write-up and rationale.)

- No live web search for cancellation procedures (curated guide only, for a small set of providers, researched offline via Exa)
- No multi-user session sharing or persistent session resumption
- No legal or financial advice — every recommendation is phrased as guidance to verify independently

## Code heritage declaration

This is a net-new build created during the official hackathon build session, not a pre-existing project resubmitted under a new name.

**Written before the event (scaffolding only, no functionality):** empty folder structure (`src/`, `docs/`, `data/`, `demo/`), a blank README skeleton, `.gitignore`, and empty placeholder files — no product logic, prompts, or working code of any kind.

**Built entirely during the event:** the product idea and its pivot from a generic "email sorter" to a multi-email account-synthesis agent; every prompt (`src/prompts/`); the classification/synthesis engine, cancellation-guide resolver, draft generator, prioritizer, and PDF report generator (`src/engine/`); the Streamlit UI and its visual design system (`src/app.py`, `.streamlit/config.toml`); the demo dataset (`data/demo_emails.json`); the curated cancellation guide and its Exa-research script (`data/cancellation_guides.json`, `src/scripts/research_cancellation_guide.py`); the real Gmail read-only connection (`src/engine/gmail_client.py`); and all documentation (`docs/architecture.md`, `docs/pitch.md`, `docs/design_prompt.md`).

No third-party starter kit, template repository, or prior project was used as a base for the application code.

`docs/brief-produit-digital-closure-v2-exhaustif.md` and `docs/prompt-etape-2-claude-code.md` are the founder's own product brief and build instructions, written for this hackathon before implementation started — kept in the repo for transparency into the design process, not application code.

## Team

- Sekou Diarra ([diarrasekou9985@gmail.com](mailto:diarrasekou9985@gmail.com))

## Demo video

[Watch on YouTube](https://youtube.com/watch?v=_G-3qxbSdNg)

---

## Submission materials

### Written description (paste into the submission form)

> What Remains is an agent that reads through a deceased person's email history and reconstructs which digital accounts and subscriptions are still active — built for the grieving family member who has to "deal with the accounts," not the tech-savvy user. Rather than sorting emails one by one, it groups the relevant billing-related traces of a service found in the analyzed inbox (a signup, a price change, a receipt) into one account history, clearly separates what it's certain of from what's ambiguous, and — for well-known providers — surfaces the real, Exa-researched cancellation steps instead of a generic template. It never takes an irreversible action itself: every draft message or cancellation step stays in the user's hands, and the full findings can be exported as a shareable PDF report for family or a professional. This only works because the agent lives inside the actual email history — that's the one place the scattered evidence exists, and the one context a generic inbox assistant never searches with this purpose.

### Social media post draft

> We built **What Remains** at #AgentsEverywhere (@AITinkerers) — an agent that reads a deceased person's emails to find out which subscriptions and accounts are still active, so a grieving family doesn't have to hunt through hundreds of messages alone. It never cancels anything on its own — every action stays in the family's hands.
>
> Built with @OpenRouterAI and @ExaAILabs.
> Code: [repo link]
> Demo: [video link]

⚠️ Before posting: verify the exact official social handles for AI Tinkerers, OpenRouter, and Exa (they may differ by platform) — check the event page or ask an organizer rather than guessing, to make sure the tags actually land on the right accounts.

## Hackathon submission checklist

- [x] Project title
- [x] Written description (what, for whom, why the context matters)
- [x] Public GitHub repository with working code
- [x] 2-minute demo video
- [x] Public social media post tagging event sponsors

Submitted to the hackathon portal.
