# PROGRESS.md

## Session 0 — 2026-07-11 (scaffold, via Claude on claude.ai)
**Done:**
- Deep research on hackathon rules, judging, prior winners → condensed into `docs/v0.1/RESEARCH.md`
- Track + project decided (DEC-001, DEC-002); full triad written (KICKOFF, PRD, RESEARCH)
- Scaffold: CLAUDE.md, DECISIONS.md (DEC-001–009), code skeleton (FastAPI app, adjudicator, validation, prompts, static UI shell), Dockerfile, smoke test, 3 demo scenarios, SUBMISSION.md
- Infra status: team-4479 registered; GPU pods erroring (504/502) — Fireworks-first confirmed (DEC-003); $50 Fireworks credits in hand

**Next (Session 1 — Claude Code, hour-by-hour in KICKOFF.md):**
1. `cp .env.example .env`, add FIREWORKS_API_KEY
2. `python scripts/smoke_test.py --list` → confirm exact Gemma model ID → set MODEL_ID
3. `python scripts/smoke_test.py` → first structured adjudication against demo scenario 1
4. Build per KICKOFF H2–H5; deploy walking skeleton by H4

**Blockers:** AMD GPU pod 504/502 (non-blocking by design). Exact Fireworks Gemma model ID unconfirmed until smoke test.

## Session 1 — 2026-07-11 (Claude Code, submission build)

### H1 — Prove inference: DONE (on stand-in; Gemma flip pending)
**Done:**
- `.env` created from example; `.env.example` sanitized (live key removed before any push)
- Deps installed (Python 3.14, openai/fastapi/uvicorn/pydantic/dotenv)
- `smoke_test.py --list` → **no Gemma on serverless tier** (all IDs 404; Fireworks rotated Gemma to on-demand-only, ~$7/hr H100). Hackathon key is inference-only (403 on control plane) → deployment must be created in user's dashboard. Logged as **DEC-010**
- Wiring proven on TEMP stand-in `gpt-oss-120b`: full smoke test on deny scenario → **DENY, risk 90, citations 2/2 verified with spans**, 4.2s latency, audit block complete
- AMD pod now reachable (ROCm 7.2 + vLLM 0.16.0 image) — parked as post-H6 sidequest per KICKOFF

**Position:** entering H2–H3 (core loop + UI pass per PRD §UI).

**Blockers:**
- Gemma deployment creation (user action, Fireworks dashboard: gemma-4-31b-it, min replicas 0/max 1, name `clause-gemma`). MODEL_ID **must** flip to it before demo/submission — stand-in never ships.

**Next action:** H2–H3 — wire `POST /adjudicate` verification on the running app, full UI pass on `static/index.html` (keep element IDs + fetch contract), then H4 deploy.
