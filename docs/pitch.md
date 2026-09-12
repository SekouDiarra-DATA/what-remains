# Pitch script — What Remains (2:00 max)

> Target: ~180-200 spoken words, the rest of the 2 minutes is screen action. Rehearse with a timer before recording.

## 0:00–0:20 — The problem (hook)

> "Every year, about 63 million people die worldwide. Every single one of them leaves behind an active digital life — subscriptions, bank auto-payments, cloud storage — that keeps running with no one watching it.
>
> Studies show almost half of people have no plan at all for their digital accounts after death. And the hardest part for the family left behind isn't cancelling those accounts — it's *finding* them in the first place, buried in hundreds of emails, at the exact moment they have the least energy to look."

## 0:20–0:35 — The solution, one sentence

> "This is What Remains: an agent that reads through a deceased person's email history and reconstructs exactly what's still active — so a grieving family doesn't have to."

## 0:35–1:35 — Live demo (screen recording, minimal narration)

⚠️ **Exact current UI — check this against the running app before recording, it changes fast:**
- The consent screen's primary button is **"Connect a Gmail account"** — a real, live OAuth connection. **Do not use it for the recorded video** (it would expose real personal inbox content). Instead, use the secondary option below it.
- Click to expand **"No account to connect right now? Try a sample inbox"**, then click **"Load the sample email export"** inside it.

Steps to perform on screen while narrating briefly:
1. Show the consent screen — read the "what this tool never does" line out loud once. *("It never sends anything or cancels anything on its own — every action stays in the family's hands.")* Optionally mention: *("The primary way to use this is connecting the real account directly — for this recording, we'll use a safe simulated inbox instead, to respect privacy.")*
2. Check the box, expand "Try a sample inbox", click "Load the sample email export" — checklist appears instantly (cached).
3. Point out the **priority ordering** (high → low) and the **Confirmed / Unconfirmed** labels (colored left border + text, no icons).
4. Open **Netflix** or **Spotify** — point at the list of source emails shown (dates + subjects) and narrate explicitly: *"It didn't just read one email. It built one account profile from several separate traces — a signup, a price increase, a payment — not a checklist of individual messages."* (Say "one account profile from several traces" close to those exact words — it's the single sentence that separates this from a generic inbox sorter for a judge.)
5. Show the **real cancellation steps** for Netflix. *("For known providers, it found the actual steps — not a generic template.")*
6. Open **FitZone Gym** (no guide available) — click **"Draft a message to their support"** — show the generated draft. *("When it can't find a verified procedure, it says so honestly, and drafts a message instead — which is never sent automatically.")*
7. Scroll to the footer and click **"Download full report as PDF"** — briefly show the generated document. *("Everything — evidence, history, next steps, drafts — as one document the family can keep, or hand to a notary.")* A plain CSV export is also available.

## 1:35–1:50 — Why the context matters

> "This only works because the agent lives inside the actual email history — that's where the evidence is scattered, and that's the one place a generic assistant never looks with this purpose."

## 1:50–2:00 — Close

> "What Remains. Built with [stack/sponsors — see below]. Code is on GitHub — link in the description."

---

## Sponsor / stack line

> "Built with Streamlit and OpenRouter for the core agent, and Exa to research and verify the cancellation guide for well-known providers — offline, not live, so we never show an unverified answer with false confidence."

---

## Filming notes

- Record the demo dataset load in advance if possible — it's now instant thanks to a pre-computed cache (`data/analysis_cache.json`), so no live API wait during recording. Be honest about this if asked or if it feels relevant to mention on camera: *("This sample analysis is pre-computed for reliability — the same engine runs live against a real Gmail account, which we're not showing here for privacy.")* Don't let the instant load imply the cards are static content.
- If something breaks live, cut and restart that segment rather than narrating through an error.
- Keep the on-screen cursor deliberate and slow — judges are watching dozens of videos, clarity beats speed.
- **Do one dry run through the actual running app immediately before recording** and adjust this script if any button label or layout has changed — the UI has been iterated on throughout the build and this script may drift from it.
- Never click "Connect a Gmail account" during the recorded take — always use the "Try a sample inbox" secondary option.
