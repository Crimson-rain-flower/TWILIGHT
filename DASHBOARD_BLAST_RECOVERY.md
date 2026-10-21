# Twilight Dashboard · Blast Radius, Full Recovery, Conversation & Metrics

## What’s improved

### 1. Blast radius map (every bot)
- Click **any** agent on the constellation (SupportBot, DataBot, Coordinator, LedgerBot, FraudBot).
- **Animated orange dashed edges** with arrowheads draw to every peer it messaged.
- Those peers pulse with **ON WATCH** badge and orange ring.
- Blast list under the map shows peer name + live trust score.
- Each bot has its own default blast topology; attacks and recovery actions expand edges.

### 2. Full recovery cycle (customer-aware)
On the selected agent card you see a **4-step timeline**:

| Step | Phase | What happens |
|------|--------|--------------|
| 1 | HALTED | Trust ≤ 15, keys revoked, all tools blocked |
| 2 | RESTORING | Signed manifest load (short animated step) |
| 3 | PROBATION | Trust 50, clean-action progress bar fills |
| 4 | HEALTHY | Trust 80, probation cleared |

Buttons: **Halt** → **Restore + Probation** (auto-plays RESTORING → PROBATION + progress) → **Force clean exit**.

#### Customer on recovery
When Coordinator sends a **legit recovery request**, the agent card shows:
- Customer **name**, **ID**, account type, city
- **Amount** and reason

#### Two recovery paths

| Action | Who | Guard ON | Guard OFF |
|--------|-----|----------|-----------|
| **Fake recovery (Talker)** | Talker → agent recovery ping | Twilight **BLOCKS** · trust drop · logged as attacker | ALLOW (unsafe) · agent marked healthy without checks |
| **Legit recovery (Coordinator)** | Coordinator → agent with full customer details | Request attached · press **Validate recovery** | Same request flow (validate still requires guard ON for safe credit) |

**Validate recovery** (guard ON only):
- Marks recovery **VALID**
- Credits the customer **from Twinity Bank**
- Transaction reason: **Twilight agent log**
- Customer drawer and table show the credit (+ recovery badge)

### 3. Conversation logs (3 filters)
- **Selected bot** — messages/tools involving the agent you clicked
- **Attackers** — Talker / Poisoner traffic only
- **Legal agents** — legitimate agent-to-agent + system tools
- **All** — full stream

Attacker rows are highlighted (orange border + badge).

### 4. Numbers table + agent trust map
- Detection, false alarms, latency, gateway median, ablation.
- Side-by-side **agent trust bar chart** (live trust per agent).

### 5. Customer details
- Open any customer → balance, identity, transactions.
- **Pending recovery** banner if Coordinator requested recovery for that account.
- **Credited via Twilight recovery** section after Validate (amount from Twinity Bank, reason: Twilight agent log).
- **Agent activity on this account** — recent refund/ticket/recovery tool calls + verdicts.

### 6. Animations & UX
- Node pulse for ON WATCH / HALTED on every bot.
- Edge dash animation + drop-shadow for any selected agent.
- Recovery step dots with scale + glow.
- Progress bar for clean actions.
- Conversation row fade-in; attacker highlight.
- Trust sparkline on agent card.

## How to run

```bash
cd /home/workdir/artifacts/twilight/twilight
# optional: export GROQ_API_KEY=gsk_...
./run_demo.sh
# or static only:
cd frontend && python -m http.server 8080
```

## Demo path

1. Toggle **TWILIGHT · ON**
2. Open **Twilight** tab → click **SupportBot** (or any bot — blast edges animate)
3. **Run attack** → edges, conversation, stream, metrics, trust map update
4. Agent card recovery:
   - **Halt** → **Restore + Probation** → **Force clean exit**
   - Or **Fake recovery (Talker)** → see BLOCK when guard ON
   - Or **Legit recovery (Coordinator)** → customer card appears → **Validate recovery**
5. Open **Customer** (Rohan Gupta / TB-4471) → see credit from Twinity Bank, reason Twilight agent log
6. Conversation filters: **Selected bot** / **Attackers** / **Legal agents**

Works offline as local simulation; live mode uses the real gateway pipeline when up.

## Files

- `frontend/index.html` — panels, metrics + trust map
- `frontend/css/app.css` — edges, recovery timeline, customer card, log filters
- `frontend/js/app.js` — blast for every bot, dual recovery paths, validate credit, 3-way logs
- `gateway/demo_api.py` — blast_radius in state, POST /demo/recover
