# RESEARCH — AMD Developer Hackathon: ACT II (condensed dossier)

## Event
- lablab.ai × AMD × NativelyAI. Build phase July 6–11, 2026. Deadline July 11 (verify exact minute on Schedule tab — renders in local timezone). Solo allowed; team registration required for GPU pod (done: team-4479).
- Prize pool $21,000. Per track: $2,500/$1,500/$1,000. Plus Google DeepMind "Best Use of Gemma": $2,000 for Track 3.
- Required tech: AMD Developer Cloud (MI300X) and/or Fireworks AI API. All submissions containerized. Featured model: Gemma (Gemma 4, Apache 2.0, released Apr 2026).

## Track 3 (ours) judging
Human-judged: **creativity/originality · product/market potential · completeness · use of AMD platforms.** lablab's general rubric: application of technology, presentation, business value, originality.

## Submission requirements (lablab platform)
Working prototype accessible by URL · pitch video ≤5 min MP4 (target ≤3) · slide deck PDF · public GitHub repo with README (setup + usage, runnable by a stranger) · title/short+long description/tags/cover image. Containerized, `linux/amd64`.

## What wins (pattern library)
- Act I winner **REPOMIND**: on-prem air-gapped coding agent + cost router, 100% AMD, tamper-evident audit log. Pattern: enterprise-credible, compliance-anchored, one crisp cost/privacy story.
- lablab agent-era winners (Deals Machine, OlympusOS, Stylin'): one autonomous multi-step workflow, one obvious wow, clean UI, visible near-real-time result.
- lablab's own guidance: deployed demo is non-negotiable (local-only scores as zero); scope MVP to ~half the time; ≤3-min video with the product working on real input inside the first 60 seconds; keep the AI layer to one reliable call; originality = "only possible with this generation of AI"; judges evaluate investability.
- Failure modes: overscoping, undeployed demos, videos that bury the demo, sponsor tech used trivially.

## Infrastructure facts
- **Fireworks:** $50 hackathon credits (in hand). OpenAI-compatible: `base_url=https://api.fireworks.ai/inference/v1`, model IDs `accounts/fireworks/models/...`. Gemma served (verify exact ID via `/v1/models`).
- **AMD hackathon GPU pods** (notebooks.amd.com/hackathon): dedicated free infra, separate from AMD Developer Cloud credits. Currently 504/502 errors — organizers say stop requesting until resolved. Team quota 12h/24h. Two images: **ROCm 7.2 + vLLM 0.16.0 + PyTorch 2.9** (use this one) or Unsloth + llama.cpp for Radeon.
- **MI300X:** 192GB HBM3 — runs large Gemma variants on a single card. Day-0 vLLM-on-ROCm support for Gemma. `vllm serve google/gemma-...` → OpenAI-compatible endpoint → swap `OPENAI_BASE_URL`. Strictly a bonus (DEC-003).
- AMD Developer Cloud $100 credits = separate 2–3 day manual approval. Irrelevant to this build.

## Rules cautions
- Original work; check repo licensing (MIT for our code; Gemma is Apache 2.0).
- lablab allows a 6h post-deadline window only with prior organizer approval — do not rely on it.
- Discord (AMD + lablab) is the escalation path for infra issues and for confirming the exact Fireworks credit/key mechanics.
