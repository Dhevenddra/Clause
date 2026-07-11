# KICKOFF — CLAUSE v0.1 (submission build)

**Clock:** ~8 hours to lablab submission. Deadline July 11, 2026 (confirm exact minute on the event Schedule tab — it renders in local time). Submit with ≥45 min buffer.

## Definition of Done (submission checklist)
- [ ] Public URL where a judge can paste a policy + claim (or click a demo scenario) and get a cited decision
- [ ] Public GitHub repo, README with setup + usage that a stranger can follow
- [ ] Docker image builds `linux/amd64` and runs from README instructions
- [ ] Pitch video ≤3 min (MP4) — script in SUBMISSION.md
- [ ] Slide deck (PDF) — outline in SUBMISSION.md
- [ ] lablab submission form: title, short + long description, tags, cover image
- [ ] Gemma is the model (Gemma-prize eligible); AMD story stated in video + README

## Hour-by-hour
**H1 — Prove inference.** `.env` from example → `smoke_test.py --list` (pin exact Gemma model ID into MODEL_ID) → `smoke_test.py` runs demo scenario 1 through the real prompt + schema and prints validated citations. If Gemma structured output is flaky, tighten `app/prompts.py` (few-shot the JSON), don't add chains.

**H2–H3 — Core loop + UI.** Wire `POST /adjudicate` end-to-end. Build `static/index.html` per PRD §UI: two input panes, Adjudicate button, decision banner, citation ledger with clause highlighting, demo-scenario buttons, audit-record download. Vanilla JS; render from the JSON schema.

**H4 — Deploy the walking skeleton.** Render.com (or Fly.io/HF Spaces Docker). Env var set in dashboard, never in repo. From here on, verify on the DEPLOYED URL after every significant change.

**H5 — Trust polish.** Validation edge cases (whitespace/quote normalization already in validation.py — verify against real Gemma output), the rejected-citation visual state, risk-score display, loading state, error states with plain-language messages.

**H6 — Freeze + package.** Feature freeze. README final. Docker rebuild + clean-machine run from README. Push repo public. Tag `v0.1.0`.

**H7 — Video + deck.** Record ≤3 min per SUBMISSION.md script: 15s problem → live demo on deployed URL (scenario walk-through, show a verified citation AND a rejected one) → 20s AMD/Gemma architecture → 20s business case. Slides: 6, PDF.

**H8 — Submit.** lablab form complete, links verified in an incognito window, submit. Remaining time: buffer only. No new features after H6, no exceptions.

## Risk register
- **Gemma JSON discipline** → mitigation: strict schema in prompt + `response_format` if supported + one retry with error feedback; smoke test proves this in H1.
- **Fireworks model ID drift** → `--list` in H1; DEC-004 fallback.
- **Deploy friction** → that's why it's H4 not H8. If Render fights you >30 min, switch to HF Spaces Docker immediately.
- **MI300X pod comes alive mid-build** → optional 30-min sidequest AFTER H6 only: `vllm serve` Gemma on the pod, point a second env at it, capture 15s of footage for the video ("same app, Gemma on MI300X via ROCm"). If anything resists, abandon — Fireworks is the submission path.
