# DECISIONS.md — append-only

## DEC-001 — Track 3 (Unicorn Track) over Tracks 1/2
**Date:** 2026-07-11 · **Status:** Locked
Tracks 1 & 2 are automated leaderboards (token-routing, video captioning) already crowded with near-identical solutions; they reward grinding, not craft. Track 3 is human-judged on creativity/originality, product/market potential, completeness, and use of AMD platforms — exactly where a solo builder with strong product + full-stack skills wins. Largest single-project upside ($2,500 + $2,000 Best AMD-Hosted Gemma).

## DEC-002 — Project: CLAUSE, an auditable insurance-claims adjudicator
**Date:** 2026-07-11 · **Status:** Locked
Vertical "adjudicator" agent archetype (matches Act I winner pattern: enterprise-credible, compliance-anchored, agentic). Insurance claims chosen over other regulated workflows deliberately — clean distance from the builder's day-job domain (vendor onboarding). Two-document structure (policy + claim) makes citations meaningful and demoable.

## DEC-003 — Fireworks-first inference; MI300X as env-swap upgrade
**Date:** 2026-07-11 · **Status:** Locked
AMD hackathon GPU pods are erroring (504/502, organizers say stop requesting) and allocation can take hours. $50 Fireworks credits are live now. Architecture: OpenAI SDK + `OPENAI_BASE_URL`. Fireworks = `https://api.fireworks.ai/inference/v1`. If/when the MI300X pod comes up, `vllm serve` a Gemma model on it and point the same env var at it. Submission must be fully functional on Fireworks alone (CLAUDE.md hard rule 1).

## DEC-004 — Model: Gemma (open-weight) as the only adjudication model
**Date:** 2026-07-11 · **Status:** Locked
Gemma is the hackathon's featured partner model with a dedicated $2,000 Track 3 prize. Exact Fireworks model ID to be confirmed at build start via `scripts/smoke_test.py --list` (expected: a Gemma 4 instruction-tuned variant). Fallback if Gemma unavailable on Fireworks: any served Gemma size; do NOT switch model families.

## DEC-005 — Single container: FastAPI + vanilla-JS static frontend
**Date:** 2026-07-11 · **Status:** Locked
No React build step, no separate frontend deploy, no DB, no auth. One Dockerfile, one process, one public URL. Optimizes for the containerization requirement + deploy-early rule under a 9h budget.

## DEC-006 — Extractive citation validation is the core trust mechanism
**Date:** 2026-07-11 · **Status:** Locked
Model must return citations as verbatim quotes from the policy. `app/validation.py` verifies each quote via normalized exact-substring match against the source before render. Verified → green "✓ verified in source" + clause highlight. Unverified → visibly rejected ("✗ could not be verified — excluded from decision basis"). The rejection state is a demo feature, not an error path.

## DEC-007 — Deploy target: public URL by mid-build (Render / HF Spaces / Fly.io)
**Date:** 2026-07-11 · **Status:** Locked
lablab requires a judge-accessible working prototype URL. Deploy the walking skeleton by ~H4, then iterate on the deployed target. Local-only = zero.

## DEC-008 — Scope freeze (MVP list is final)
**Date:** 2026-07-11 · **Status:** Locked
MVP: paste/upload policy + claim → one structured Gemma call → decision (APPROVE/FLAG/DENY) + risk score + per-point verified citations → clause-highlight panel → downloadable JSON audit record → 3 pre-loaded demo scenarios. Explicitly OUT: multi-claim batching, PDF parsing (paste text only; a .txt/.md upload is fine), user accounts, history, fine-tuning, multi-agent anything.

## DEC-009 — Design signature: the verified-citation ledger
**Date:** 2026-07-11 · **Status:** Locked
UI's one memorable element: decision cards linked to highlighted source clauses, each stamped with its verification state; evidence quotes set in monospace like an audit ledger. Palette from the underwriting world (ink, paper, stamp-red/amber/green for DENY/FLAG/APPROVE) — see PRD design brief. Everything else stays quiet.

## DEC-010 — Gemma via Fireworks on-demand deployment; gpt-oss-120b as build-time stand-in
**Date:** 2026-07-11 · **Status:** Locked
H1 discovery: Fireworks rotated ALL Gemma variants off the serverless tier (every ID 404s; catalog pages confirm "serverless: not supported"). Gemma 4 now requires a dedicated on-demand deployment (~$7/hr H100, per-second billing) created in the web dashboard — the hackathon API key is inference-only (403 on control plane). Plan: user creates `clause-gemma` deployment (gemma-4-31b-it, min replicas 0 / max 1; NVFP4 variant if 2 GPUs demanded); build wiring proceeds on serverless `accounts/fireworks/models/gpt-oss-120b` as a TEMP stand-in. Credit protection: deployment runs in bursts only (tuning ~$4, demo recording ~$4), ~$40 preserved for the judging window. HARD CONSTRAINT: MODEL_ID flips to the Gemma deployment before demo/submission — the stand-in never ships (DEC-004 intact). AMD pod (ROCm 7.2 + vLLM 0.16.0) came alive mid-build; remains a post-H6 sidequest per KICKOFF.

## DEC-011 — Deploy host: Render, created via REST API (service srv-d98tvfss728c73cbn4k0)
**Date:** 2026-07-11 · **Status:** Locked
User chose Render (DEC-007 shortlist). User supplied a Render API key (also registered as an MCP server; tools load next session). Service created programmatically: Docker runtime, free plan, Singapore, healthCheckPath /health, auto-deploy on push to main. Public URL: https://clause-4vv4.onrender.com — verified live with a real-browser deny-flow run. Env vars (key, base URL, MODEL_ID) live in Render env, never the repo; MODEL_ID flip to Gemma happens via the same API. Free-tier note: sleeps after ~15 min idle (~50s cold start) — warm it before demo/judging or bump to starter for the window.

## DEC-012 — Gemma deployment live; prompt calibrated with one worked example; flag fixture sharpened
**Date:** 2026-07-11 · **Status:** Locked
Deployment: `gemma-4-31b-it-nvfp4` 1× B200 FP4 $10/hr, autoscale 0–1, 5-min scale-to-zero — referenced as `<base-model>#accounts/kgdhevenddra-28kx6z3/deployments/wwow7aos`. Discoveries: (a) this serving emits a `reasoning_content` stream before the JSON — max_tokens raised 2000→6000 after the cap swallowed a whole response as reasoning; (b) original flag fixture was legitimately deniable (door "unlocked but undamaged" = clear 2.2 exclusion) — rewritten so the deciding facts are genuinely pending (locksmith report, loss-date vs 60-day clock), which is what FLAG is for; (c) one worked FLAG example added to the system prompt (verbatim-quote + uncertainty→FLAG + risk-band calibration) — still ONE structured call (hard rule 4). Result on real Gemma: APPROVE 10 (4/4 cited), FLAG 50-60 (3/3), DENY 95 (1/1); 8/8 citations verified. Ops note: Render service has no GitHub webhook (API-created) — every push requires a manual `POST /deploys`; env-var changes also only apply on next deploy.
