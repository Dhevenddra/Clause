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

### H2–H3 — Core loop + UI: DONE · H5 largely done · H6 Docker check done early
**Done:**
- Full UI pass on `static/index.html` per PRD §UI (ink-on-paper ledger, Archivo/Inter/IBM Plex Mono, rubber-stamp verdict with texture mask, verification seals, clause-highlight sweep, cascade-in reveal with reduced-motion respect, loading state w/ client-side SHA-256, empty/error states, .txt/.md upload, responsive). IDs + fetch contract intact
- Verified in browser via Playwright: deny flow end-to-end, clause highlight, rejected-citation state (injected fixture: struck quote + red "✗ NOT IN SOURCE" seal)
- Bug fixes: `load_dotenv()` missing in adjudicator (uvicorn 502), UTF-8 reads for demo files (Windows cp1252 mojibake)
- H5: `scripts/test_validation.py` — 11/11 edge cases pass (curly quotes, dashes, nbsp, whitespace, cross-newline spans; paraphrase/fabrication correctly rejected)
- H6 (early): Docker image builds `linux/amd64` and adjudicates through the container (DENY, 2/2 verified, 5.5s)
- H4 prep: `render.yaml` blueprint + PORT-aware Dockerfile CMD pushed; exact Render steps given to user
- `scripts/mi300x_serve.sh` ready for the post-H6 pod sidequest
- Astryx (Meta design system) suggested by user → deferred to post-submission v0.2 (DEC-005/DEC-008: no build step, scope frozen)

**Position:** H4 (deploy) in flight — blueprint ready, awaiting user's Render account setup.

**Blockers (both user actions, in progress):**
1. Render deploy → need the public URL once the blueprint is applied
2. Fireworks Gemma deployment (`clause-gemma`, 1-GPU shape, min 0/max 1) → need the deployment/model ID to flip MODEL_ID and tune prompts against real Gemma

**Next action:** on Render URL — verify deployed deny flow in incognito; on Gemma ID — smoke test, check citation verification rate, tighten prompts.py rule 2 with one few-shot verbatim-quote example if <70%.

### H4 — Deploy: DONE ✅
**Done:**
- Render service created **via REST API** (user's key; no dashboard needed) — DEC-011. Docker runtime, free plan, Singapore, /health check, auto-deploy from main
- **Public URL live: https://clause-4vv4.onrender.com** — verified twice: REST (DENY, 1/1, 2.7s) and full real-browser pass (deny flow, citation ledger, seals, clean UTF-8)
- Render MCP server registered (tools available next session; REST API suffices meanwhile)

**Position:** H4 done ahead of schedule. H5 mostly done. H6 Docker check done. Remaining core work: Gemma flip + prompt tuning (H5 tail), README/tag freeze (H6), video+deck (H7), submit (H8).

**Blockers:**
- Fireworks Gemma deployment: 31B IT offers only 4-GPU shapes ($28–40/hr!). User trying smaller/quantized Gemma variants (NVFP4 → 26B A4B → E4B) per my guidance; also told to cut Scale-to-Zero Window from 60 min to seconds (credit protection)

**Next action:** user reports NVFP4 shape/price → lock deployment → flip MODEL_ID (local .env + Render env via API) → smoke test real Gemma → tune prompts.py rule 2 if verification <70%.

### H5 — Gemma live + trust polish: DONE ✅
**Done:**
- Fireworks deployment created by user: gemma-4-31b-it-nvfp4, 1× B200 FP4 $10/hr, autoscale 0–1, 5-min scale-to-zero (DEC-012)
- MODEL_ID flipped locally + on Render (API); **deployed URL runs real Gemma** — verified: FLAG 3/3 verified, 28s, model string in /health
- Calibration: worked FLAG example + uncertainty→FLAG rule in prompt; max_tokens 6000 (reasoning stream); flag fixture rewritten to be genuinely pending-evidence
- All scenarios on real Gemma: APPROVE 10 (4/4), FLAG 50 (3/3), DENY 95 (1/1) — **8/8 citations verified (100%)**, no rule-2 tightening needed
- README final: live URL, dedicated-deployment MODEL_ID guidance
- Ops discovery: no GitHub webhook on the API-created Render service → **manual POST /deploys after every push** (env changes also need it)

**Position:** H6 (freeze + package) — README done, Docker verified earlier. Next: tag v0.1.0, then H7 video/deck prep.

**Blockers:** none. Credits: ~$45 Fireworks remaining (est.), Render free tier fine.

**Next action:** tag v0.1.0 + push → H7: cover image, deck outline, video walkthrough on the deployed URL (user records), warm both host + GPU right before recording.

### H6 — Freeze + package: DONE ✅ · H7 — assets DONE, recording with user
**Done:**
- Feature freeze; tagged **v0.1.0** and pushed; repo public with final README (live URL + dedicated-deployment MODEL_ID guidance)
- **Slide deck**: `docs/assets/CLAUSE-deck.pdf` (6 slides, app design language, generated from `slides.html` via headless Edge; footer-overlap fixed and verified)
- **Cover image**: `docs/assets/cover.png` (real DENY run on the live URL)
- **Adversarial demo**: `demo/claim_adversarial.md` — tested on real Gemma: FLAG 3/3 verified, refuses to ground three fabricated provisions. Video beat reframed ("trust under attack") since Gemma resists hallucination bait — rejected-state shown honestly via test suite (11/11) or fixture still, never faked live
- **Demo-day runbook** added to SUBMISSION.md: warm-up sequence (Render ~50s + GPU ~1–2 min), per-click cost ≈ $1, live latencies per scenario

**Position:** end of H7 prep. Remaining: user records ≤3-min video per SUBMISSION.md script → H8 lablab form + final incognito URL check.

**Blockers:** video recording + lablab form are user actions. Credits: est. ~$43 Fireworks remaining.

**Next action (user):** warm both layers per runbook → record video → fill lablab form (checklist in SUBMISSION.md; cover + deck ready in docs/assets/). Then verify URL in incognito and submit with ≥45 min buffer.

### Post-freeze hardening + judge library: DONE and LIVE ✅ (DEC-013)
**Done:**
- Rate limiting on /adjudicate (15/IP/hr · 80 global/hr · concurrency 2) — spam can no longer drain GPU credits
- Cold-start fix: retry through DEPLOYMENT_SCALING_UP 503 (240s budget) — first judge click now succeeds instead of erroring (verified through a live 139s wake)
- demo/library/: motor + travel copy-pastable pairs, both verified on real Gemma (FLAG 6/6, DENY 1/1) + adversarial claim; linked from README
- README: Deployment + test-library sections; v0.2 design notes (Litmus scrape + Astryx plan) in docs/
- PII sweep clean; accidental reference-screenshot commit scrubbed from history
- Deployed and converged: Render live on repo HEAD, /health = Gemma deployment

**Position:** everything code-side is DONE. Remaining: user records video (script + runbook in SUBMISSION.md) → lablab form (full field table prepared) → incognito check → submit ≥45 min early.

**Blockers:** video + form are user actions. Est. credits: ~$40 Fireworks.

**Next action (user):** say "warm it" → record → submit. Optional post-submission sidequest: MI300X pod footage via scripts/mi300x_serve.sh (confirm GPU with rocm-smi first; stop the pod if unused).
