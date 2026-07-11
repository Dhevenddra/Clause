# SUBMISSION.md — video script, deck outline, lablab checklist

## Pitch video (target ≤3:00, MP4)
- **0:00–0:15 — Problem.** "Insurers can't use AI for claims because AI can't be audited. One unexplainable denial is a compliance event. CLAUSE fixes the trust problem, not the chat problem."
- **0:15–1:45 — Live demo (deployed URL, not localhost).** Click "Deny case" → adjudication runs → DENY banner + risk score. Click a citation → the exact exclusion clause lights up in the policy. Then the money shot: point at a rejected citation — "When the model paraphrases instead of quoting, CLAUSE catches it in code and excludes it from the decision basis. On camera. That's the product." Download the audit record, show the hashes.
- **1:45–2:15 — Tech.** "Open-weight Gemma, one structured call, on AMD — Fireworks in production, and the identical app pointed at Gemma on an MI300X via vLLM on ROCm with a single env var." (If pod footage exists, 10s of it here.)
- **2:15–2:45 — Business.** Claims processing cost + regulatory pressure; CLAUSE is the adjudication layer insurers can actually deploy: auditable, on-prem-capable, open-weight.
- **2:45–3:00 — Close.** "CLAUSE. Every decision, cited." + URL + repo.

## Slide deck (6 slides, PDF)
1. CLAUSE — every decision, cited (cover, one-line pitch)
2. The problem: unauditable AI can't touch regulated decisions
3. The product: decision + verified-citation ledger (screenshot)
4. The trust core: extractive citations + span validation (diagram)
5. On AMD: Gemma · Fireworks · MI300X/vLLM/ROCm — one env var
6. Market + ask

## lablab form checklist
- [ ] Title: "CLAUSE — every decision, cited"
- [ ] Short description (≤1 sentence pitch)
- [ ] Long description (README intro + trust core section)
- [ ] Tags: Gemma, AMD, Fireworks, FastAPI, agents/fintech as available
- [x] Cover image (UI screenshot of a DENY with the citation ledger) → `docs/assets/cover.png`
- [ ] Video uploaded (MP4, ≤5:00)
- [ ] Slides PDF
- [x] GitHub repo public, tagged v0.1.0 → https://github.com/Dhevenddra/Clause
- [ ] Demo URL live — verify in incognito immediately before submitting → https://clause-4vv4.onrender.com

## Demo-day runbook (record + judge window)
1. **Warm both layers 5 min before recording/judging:** open https://clause-4vv4.onrender.com (wakes Render, ~50s), then click "Case 03 — Deny" → Adjudicate (wakes the Gemma GPU, ~1–2 min first call). Second call onward is fast (~15–30s incl. reasoning).
2. Model = `gemma-4-31b-it-nvfp4` on the dedicated Fireworks deployment; scale-to-zero 5 min → each warm demo click ≈ $0.85–1.
3. Live latencies on real Gemma: APPROVE ~17s · FLAG ~29s · DENY ~11s. Narrate over the loading state (it shows the input SHA-256 hashes — that's a feature, point at it).
4. Video beat "trust under attack" (replaces "show a rejected citation" — tested: Gemma resists fabrication, which is the stronger story): paste `demo/claim_adversarial.md` as the Claim with the standard demo policy. Observed result: **FLAG, 3/3 verified** — the model refuses to ground the fake "guaranteed replacement value" / "welcome pack guarantee" and checks the inflated ₹25,000/week ask against the real ₹15,000 clause. Narrate: "The claimant invented three policy provisions. CLAUSE grounded none of them — every point on screen is a real clause, verified in code."
5. To show the ✗ rejected-citation state itself (it's a real code path, verified by `scripts/test_validation.py` — paraphrase and fabrication both rejected): include the 3-second UI still from the test fixture, or run `python scripts/test_validation.py` on camera — 11/11 with explicit "paraphrase must FAIL" lines. Never fake a live rejection.
