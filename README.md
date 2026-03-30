# 🎯 PivotPro

A career pivot coaching AI agent that delivers consultant-grade honesty,
a viability assessment, transferable skills analysis, and a concrete
90-day action plan — for anyone at any career stage.

Built with Claude (Anthropic) · Python · Optional Gradio UI

---

## What It Does

Most career tools validate whatever you want to hear. PivotPro doesn't.

Tell it where you are and where you want to go. It will:

- Run a structured intake to understand your full situation
- Score your pivot viability honestly (1–10) with clear reasoning
- Map your transferable skills to the target field
- Identify your real gaps and exactly how to close them
- Give you a specific, sequenced 90-day action plan
- Coach you through follow-up questions with consultant-grade directness

---

## How It Works

**Phase 1 — Intake**
The agent asks natural, conversational questions across four areas:
current situation, motivators, target roles, and constraints.
No forms. No checklists. Just a focused conversation.

**Phase 2 — Pivot Report**
Once it has the full picture, it delivers a structured report:
viability score, skills map, gaps analysis, 90-day plan, and a
coaching note containing one hard truth and one underestimated opportunity.

**Phase 3 — Coaching**
After the report, it shifts into open coaching — answering follow-ups,
pressure-testing decisions, and updating its assessment as you share more.

---

## Quickstart
```bash
git clone https://github.com/ChuksForge/pivot-pro
cd pivot-pro
pip install -r requirements.txt
echo "ANTHROPIC_API_KEY=sk-your-key-here" > .env

# CLI
python pivot_pro.py

# UI
python ui.py
```

---

## Example Output
```
## 🎯 PIVOT VIABILITY ASSESSMENT
From: Marketing Manager
To: UX Researcher
Viability Score: 8/10 — Strong pivot with genuine transferable leverage

## ⚡ FOCUS STARTER
Your user research experience is credible enough to get interviews now.
The portfolio is what converts them — build that first.
```

---

## Design Decisions

- **Hybrid interaction model** — intake before advice prevents shallow 
  recommendations on incomplete information
- **Viability score** — forces a committed position, not endless hedging
- **Coaching Note** — always contains one hard truth, differentiating 
  PivotPro from tools that only validate the user
- **Intake state tracker** — lightweight supporting prompt prevents 
  re-asking questions already answered

---

## Project Structure
```
pivot-pro/
├── pivot_pro.py    # Core agent (CLI + logic)
├── ui.py           # Gradio web UI
├── requirements.txt
├── demo
└── README.md
```

---

## Built With

- [Anthropic Claude API](https://anthropic.com)
- Python 3.10+
- Gradio (optional UI)

---

## Author

Built by **[ChuksForge]**

- Portfolio: chuksforge.github.io
- GitHub: [github.com/ChuksForge](https://github.com/ChuksForge)
- Email: chuksprompts@gmail.com

## License

MIT