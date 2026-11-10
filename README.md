# TWILIGHT + Twinity + LangChain agents

**A runtime security gateway for AI agents.** 
Agents have no direct access to tools: every action goes through TWILIGHT, which checks it (signature, policy, trust score, tamper-evident log) before it runs. Prototype: a fake "urgent" ₹9,000 refund is **allowed with the guard OFF and blocked with it ON**. Finalist (Top 15), Repoforge Hackathon.

## What this is
- **Twilight gateway** (M1–M3): attestation, policy, trust, audit
- **Frontend**: Twinity Bank UI (`frontend/`)
- **LangChain-style agents** (`langchain_agents/`):
  - TalkerLC, PoisonerLC (red team, words only)
  - SupportBotLC, CoordinatorLC (tools go through Twilight)

Without `GROQ_API_KEY` or `OPENAI_API_KEY`, agents use LangChain tools + offline planner.
With a key + `pip install langchain langchain-openai`, they use a real tool-calling LLM.

## Quick terminal demo (LangChain path)

```bash
cd twilight
python -m venv venv
# activate venv
pip install fastapi uvicorn pydantic pydantic-settings pyyaml pynacl httpx
# optional:
pip install langchain langchain-core langchain-openai
```

### First-time setup (once)
```bash
cp .env.example .env              # Windows: copy .env.example .env
python scripts/setup_keys.py      # generates signing keys (git-ignored)
python scripts/sign_manifests.py  # signs each agent's trusted config
python scripts/reset_db.py
```

### Run the attack
```bash
python scripts/run_langchain_attack.py --mode on
python scripts/run_langchain_attack.py --mode off
```

Expect: Talker + Poisoner speak → SupportBot tries `issue_refund(9000)` →
**ON = BLOCK**, **OFF = ALLOW**.

## Classic non-LC attack path

```bash
python scripts/run_attack.py --mode on --attacker both
```

## Gateway + UI

```bash
python scripts/reset_db.py
python -m uvicorn gateway.main:app --port 8000 --reload
cd frontend && python -m http.server 5500
```

(The gateway also serves the dashboard itself at http://127.0.0.1:8000/ui/, so the last line is optional.)

## Layout

```
twilight/
  gateway/ engine/ agents/ attackers/
  langchain_agents/     ← NEW small LC agents
  scripts/run_langchain_attack.py
  scripts/run_attack.py
  frontend/
```
