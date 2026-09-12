# Audit prompt for Codex (paste as-is)

You have full access to this project's folder: **What Remains**, a submission for the AI Tinkerers global hackathon "Agents, Everywhere." Before commenting on anything, read these files in this order:

1. `docs/brief-produit-digital-closure-v2-exhaustif.md` — the founder's original product brief (problem, target users, non-negotiable ethical/tone constraints, what the product must never do)
2. `README.md` — current product description, tech stack, how to run it, code heritage declaration
3. `docs/architecture.md` — full technical write-up: architecture, data flow, decisions made and why, known risks, and (section 7 specifically) known limitations around public deployment
4. Then the actual code: `src/app.py`, `src/engine/*.py`, `src/prompts/*.txt`, `data/*.json`

## Context you need before judging anything

- This was built solo, under real hackathon time pressure, by someone with a statistics/data background who is not a professional software engineer.
- The product deliberately pivoted mid-build from a generic "classify each email" agent to a "reconstruct one account from multiple scattered emails" agent, specifically to satisfy the hackathon's judging criteria around interaction novelty (not just environment novelty). Judge whether the code actually delivers on that pivot, not just whether the docs claim it.
- Several limitations are **known and already documented as deliberate**, not oversights — do not spend time re-flagging these unless you think the written justification for them is actually wrong:
  - No live web search for cancellation procedures (curated static guide only, researched offline via Exa)
  - The Gmail OAuth connection uses a desktop-style flow with a single shared local token file — explicitly documented as local/developer-only, not safe for public multi-user deployment (see architecture.md section 7)
  - No multi-user session persistence, no notary-specific export format, no live web search
  - The app never performs an irreversible action (no auto-send, no auto-cancel) — this is a hard ethical requirement from the brief, not a missing feature

## What I actually want from you

1. **Idea defensibility**: Would a hackathon judge find the "agent lives in email, reconstructs accounts across scattered messages" pitch genuinely differentiated, or does it still read as a generic email-sorting assistant? Be honest and specific — cite what in the code would or wouldn't convince a skeptical judge.
2. **Judging-criteria alignment**: Given the four criteria (Functionality, Innovation, Technical execution, Usefulness — each scored 1-5), where is this submission weakest, concretely?
3. **Code correctness bugs**: Anything actually broken or fragile that we likely haven't caught — edge cases in `classifier.py`'s grouping/synthesis, `resolver.py`'s fuzzy matching, `report.py`'s PDF generation, `app.py`'s Streamlit state handling.
4. **Security**: A fresh look at secret handling, HTML/PDF injection risk from LLM-generated or real-inbox-derived text, and anything else that would concern a security-conscious reviewer.
5. **Doc-vs-code consistency**: Anything the documentation claims that the code doesn't actually do (or vice versa).
6. **Ethical/tone fidelity to the brief**: Does the actual UI copy and behavior genuinely honor the brief's non-negotiable constraints (sober tone, no false certainty, reversibility always visible), or is there drift anywhere?

## How to report back

Prioritize findings by severity (critical / important / minor / nitpick). For each finding: what's wrong, where exactly (file + line if code), and why it matters for a hackathon judge or a real user — not just "this could be improved." Skip generic style nitpicks unless they're truly trivial to fix. I have limited time left before recording the demo video, so surface what's actually worth fixing now versus what's fine to leave as a documented limitation.
