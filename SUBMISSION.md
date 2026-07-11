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
- [ ] Cover image (UI screenshot of a DENY with the citation ledger)
- [ ] Video uploaded (MP4, ≤5:00)
- [ ] Slides PDF
- [ ] GitHub repo public, tagged v0.1.0
- [ ] Demo URL live — verify in incognito immediately before submitting
