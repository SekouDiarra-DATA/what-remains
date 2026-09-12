# Design prompt — for an AI design tool (paste as-is)

You are designing the visual identity and UI polish for a working web app called **What Remains**. Read the full context below before proposing anything — the emotional register of this product is unusually load-bearing for the design decisions.

## What the product is

What Remains is an agent that reads through a deceased person's email history and reconstructs which digital accounts and subscriptions are still active (subscriptions, bank auto-payments, cloud storage), so a grieving family member doesn't have to hunt through hundreds of emails alone at the worst possible moment. It groups scattered email evidence per service into one account history, distinguishes what it's certain of from what's ambiguous, and — for well-documented providers — shows the real cancellation steps; for others, it offers to draft a support message. It never takes an irreversible action itself.

## Who is using it, and in what state

The primary user is a grieving family member (spouse, adult child), often not especially tech-confident, in a state of decision fatigue, guilt, and fear of "breaking something." They are not a target user who wants delight, gamification, or reassurance-through-cheerfulness. They want clarity, calm, and the unmistakable sense that nothing irreversible will happen without their explicit say-so.

## Non-negotiable tone constraints (from the product brief — do not deviate)

- **No emojis anywhere in the interface.** Not for status, not for urgency, not for decoration. This is the primary reason this redesign is happening — the current build uses emoji badges (🔴🟡⚪✅❔) as a placeholder and they must be replaced with a proper, quiet visual language (color, type weight, iconography via SVG/icon font if truly needed — but prefer typographic and color solutions over icons).
- No humor, no exclamation marks, no celebratory or "delightful" micro-interactions, no gamification, no bright alarm-style red/green traffic-light coloring that reads as urgent or corporate-dashboard-like.
- The product must never look like generic "grief tech" (no candles, doves, soft-focus photography, or sentimental clichés) — it is a practical tool, not an emotional-simulation product. It also must not look like a cold enterprise SaaS dashboard. The target feeling is something like: a quiet, competent, trustworthy document — closer to a well-designed official form or a calm piece of editorial design than to a startup product.
- Every reassurance about reversibility ("nothing has been sent or changed") must remain visually prominent, not buried as fine print.
- Must clearly, calmly distinguish **confirmed** findings from **unconfirmed/ambiguous** ones, and distinguish **priority levels** (high / medium / low) — without relying on emoji or stoplight-red/yellow/green. Think instead in terms of: subtle left-border accent color, type weight/size hierarchy, muted color tags with text labels, or ordering plus a quiet label.

## Current technical constraints

- Built in **Python + Streamlit** (single-page app, no custom frontend framework). Deliverables need to be realistically implementable via:
  - Streamlit's native theme config (`.streamlit/config.toml`: primaryColor, backgroundColor, secondaryBackgroundColor, textColor, font), and/or
  - Custom CSS injected once via `st.markdown("<style>...</style>", unsafe_allow_html=True)`.
  - Please provide actual hex values and actual CSS (selectors can target Streamlit's default class names, e.g. `.stButton>button`, `[data-testid="stExpander"]`, etc.) rather than only abstract descriptions, so it can be pasted directly.
- Single centered column layout, max-width comfortable for reading (Streamlit's "centered" layout, roughly 700-800px content width).
- Must remain legible and well-composed when screen-recorded for a 2-minute demo video at laptop resolution — avoid overly small text or low-contrast combinations.
- Prioritize a single polished **light theme**. A dark-mode variant is a bonus only if it costs little additional effort.

## Screens and components to design (in order of the actual user flow)

1. **Consent / landing screen**: product name, one-line tagline, a short explanatory paragraph ("what this tool does" / "what this tool never does" — two short paragraphs), a consent checkbox, and two entry-point buttons ("Load the demo email export" as primary action, "Connect a Gmail account (read-only)" as a secondary/lesser-emphasized action), plus a small caption below.
2. **Checklist / results screen**: a top reassurance banner ("Here is what we found... nothing has been sent or changed..."), then a vertical list of account cards/rows, each collapsed by default, showing: service name, a priority indicator (high/medium/low — no emoji), a status indicator (confirmed/unconfirmed — no emoji). Needs a visual hierarchy so "high priority + confirmed" items feel naturally more attention-worthy than "low priority + unconfirmed" ones, without alarm-red urgency framing.
3. **Expanded account card**: evidence sentence, a one-line reconstructed history summary, a small caption noting how many source emails were used, then a "Recommended next step" section that is either (a) a short numbered/bulleted list of real steps plus a caveat note plus an outbound link, or (b) an honest "we couldn't find a verified procedure" message plus a button to generate a draft support message, which — once generated — appears in an editable text area with a caption reminding the user nothing has been sent.
4. **Footer actions**: a CSV export button and a "start over" button, visually secondary to the main content.

## What to deliver

1. A short design rationale (a few sentences) explaining the mood/feeling you're aiming for and why, tied back to the emotional context above.
2. A concrete design system: color palette with hex values and named roles (background, surface, text-primary, text-muted, border, accent-high-priority, accent-medium-priority, accent-low-priority, confirmed-tag, unconfirmed-tag), a type scale (font family choice — web-safe or Google Fonts-available, sizes/weights for title, section heading, body, caption), spacing scale, and border-radius/shadow conventions.
3. Ready-to-paste CSS (and `.streamlit/config.toml` theme block) implementing that system against the components listed above.
4. A short note on how priority and confirmation status are visually communicated without emoji or icons if possible (color + type + label text is preferred), and how that stays legible/accessible (contrast ratios).

Do not propose changes to the actual copy/wording, the information architecture, or the interaction flow — those are fixed. This is a visual design and CSS pass only.
