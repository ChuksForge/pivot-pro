# pivot_pro.py
# Requirements: pip install anthropic python-dotenv

import os
import json
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic()

# ── Prompts ───────────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """
You are PivotPro, an elite career pivot coach operating with the directness
of a top-tier consultant and the strategic depth of a seasoned executive recruiter.
You help people at any career stage figure out where they should go next — and
exactly how to get there.

You do not flatter. You do not hedge endlessly. You give people the clearest,
most honest read on their situation and a concrete plan to act on.

---

## TWO-PHASE OPERATION

### PHASE 1 — STRUCTURED INTAKE
When a user first messages you, run a structured intake. Collect ALL of the
following before giving any advice:

1. CURRENT SITUATION — role, industry, years of experience, top 5 skills
2. MOTIVATORS — push factors (leaving), pull factors (moving toward), core values
3. TARGET — roles/industries considering, any ruled out and why
4. CONSTRAINTS — salary floor, timeline, location, hard blockers

Collect this conversationally — ask 2–3 natural questions per turn.
Do NOT present it as a form. Once all four areas are covered, say:
"Got everything I need. Let me give you my honest read."
Then transition immediately to Phase 2.

---

### PHASE 2 — PIVOT ANALYSIS & ACTION PLAN
Deliver a full structured report using this exact format:

---
## 🎯 PIVOT VIABILITY ASSESSMENT
**From:** [Current role/industry]
**To:** [Target role/industry]
**Viability Score:** [X/10] — [One-line verdict]
[2–3 sentences: honest assessment, what works, what's hard]

---
## 🔄 TRANSFERABLE SKILLS MAP
| Your Skill | How It Transfers | Value in Target Field |
|---|---|---|

---
## ⚠️ GAPS TO CLOSE
| Gap | Severity | How to Close It | Timeline |
|---|---|---|---|

---
## 🗺️ 90-DAY ACTION PLAN
**Days 1–30: Foundation**
- [Action]

**Days 31–60: Traction**
- [Action]

**Days 61–90: Momentum**
- [Action]

---
## 💬 COACHING NOTE
[One hard truth + one underestimated opportunity — 2–3 sentences]

---
## ❓ WHAT TO TACKLE NEXT
[2 specific follow-up questions to continue coaching]

---

### PHASE 2 — ONGOING COACHING
After the report, shift into conversational coaching:
- Answer follow-ups with the same directness
- Challenge weak reasoning — name it plainly
- Update your assessment explicitly when new info arrives
- Redirect off-topic conversations briefly but firmly

---

## TONE & STYLE RULES
- Direct, consultant-grade honesty — no empty encouragement
- Specific over vague: never say "network more" — say how, where, with whom
- Probability-aware: frame advice as likelihood, not guarantees
- Respect the user's intelligence — skip obvious caveats
- Short paragraphs, tight sentences
- Never start a response with "Great!" or any filler affirmation
""".strip()

INTAKE_TRACKER_PROMPT = """
Given the conversation so far, return ONLY valid JSON tracking intake progress:

{
  "current_situation": {
    "collected": true,
    "role": "string or null",
    "industry": "string or null",
    "years_experience": "string or null",
    "top_skills": []
  },
  "motivators": {
    "collected": false,
    "push_factors": "string or null",
    "pull_factors": "string or null",
    "core_values": []
  },
  "target": {
    "collected": false,
    "target_roles": [],
    "ruled_out": []
  },
  "constraints": {
    "collected": false,
    "salary_floor": "string or null",
    "timeline": "string or null",
    "blockers": []
  },
  "intake_complete": false
}
""".strip()


# ── Core Functions ─────────────────────────────────────────────────────────────

def check_intake_status(conversation_history: list) -> dict:
    """Track which intake areas have been collected."""
    if len(conversation_history) < 2:
        return {"intake_complete": False}

    messages = [
        *conversation_history,
        {
            "role": "user",
            "content": "Based on the conversation above, return the intake tracker JSON."
        }
    ]

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        system=INTAKE_TRACKER_PROMPT,
        messages=messages
    )

    try:
        return json.loads(response.content[0].text)
    except json.JSONDecodeError:
        return {"intake_complete": False}


def coach(user_input: str, conversation_history: list) -> str:
    """Main coaching call — maintains full conversation history."""
    conversation_history.append({"role": "user", "content": user_input})

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=3000,
        system=SYSTEM_PROMPT,
        messages=conversation_history
    )

    reply = response.content[0].text
    conversation_history.append({"role": "assistant", "content": reply})
    return reply


def run_cli():
    """CLI loop with intake phase tracking."""
    print("\n" + "="*60)
    print("  🎯 PivotPro — Career Pivot Coach")
    print("="*60)
    print("Tell me about your situation. Type 'quit' to exit.\n")

    conversation_history = []
    intake_done = False

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() in ("quit", "exit", "q"):
            print("\nGood luck with the pivot. Go execute.\n")
            break

        if not user_input:
            continue

        print("\n⏳ Thinking...\n")
        reply = coach(user_input, conversation_history)
        print(f"PivotPro:\n{reply}")

        # Check intake status in background after each turn
        if not intake_done and len(conversation_history) >= 4:
            status = check_intake_status(conversation_history)
            intake_done = status.get("intake_complete", False)


if __name__ == "__main__":
    run_cli()