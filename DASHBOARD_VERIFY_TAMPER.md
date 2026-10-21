# Verify chain · Tamper log · Attack types · Coordinator approval

## Strongest demo: break the audit chain

1. Open **Twilight** tab.
2. Click **Verify chain** → tag stays green “Chain intact”.
3. Click **Tamper log** → one audit row is edited (verdict prefixed with `TAMPERED-`).
4. Verify runs again automatically → **metric turns red** (“BROKEN @ #N”).
5. Works **live** via `GET /demo/verify-chain` + `POST /demo/tamper-log` (real `audit.verify.verify_chain()`).
6. Works **offline** with a local simulated hash chain when gateway is down.
7. Banner shows **Gateway offline · running local simulation** or **Gateway online**.

Backend fix: `/audit/verify` no longer always returns valid; it calls `verify_chain()`.

## SupportBot · Talker honey-talk

- **Run attack** with guard **OFF**: Talker sweet-talks SupportBot → `issue_refund(TB-4471, 9000)` **ALLOW** → ledger and customer balance drop.
- Guard **ON**: same path **BLOCK** (max amount / untrusted ticket) → SupportBot FLAGGED, blast radius to Coordinator + DataBot.

## Coordinator · pending approval

After a guard-ON attack (or **Legit recovery**):

1. Click **Coordinator** on the constellation.
2. See **Pending approval** card: customer name, account, **TX-812**, ticket #812, amount ₹9,000, trust, status.
3. Guard **OFF**: FLAGGED only — no approve button (“turn TWILIGHT ON”).
4. Guard **ON**: **Approve & credit customer** → credits ₹9,000 as  
   **“Twinity Bank (approved by Twilight)”** on the customer statement.
5. Full recovery still available: Halt → Restore + Probation → Force clean exit.

## Other UX

- Tooltips (`?`) on trust score, guard mode, audit depth, charts.
- Topology lower area: **Actions/min** and **Block rate %** sparklines.
- Mobile layout for sidebar / grids / drawer.
- Empty conversation / blast states kept clear.

## Groq

Set `GROQ_API_KEY` and use `POST /demo/run-attack?flavor=langchain` for live LangChain attacks.

## Paths

- `gateway/main.py` — real `/audit/verify`
- `gateway/demo_api.py` — `/demo/verify-chain`, `/demo/tamper-log`, `/demo/recover`
- `frontend/index.html` — Verify/Tamper buttons, banner, topology charts
- `frontend/js/app.js` — offline chain sim, coordinator panel, attack seeding
- `frontend/css/app.css` — red chain, tooltips, mobile, charts
