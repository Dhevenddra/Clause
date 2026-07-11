# CLAUSE — Auditable AI Claims Adjudicator

**Hackathon:** AMD Developer Hackathon: ACT II (lablab.ai) — Track 3 (Unicorn Track)
**Deadline:** July 11, 2026 — ~8 working hours remain. Every decision optimizes for a submitted, deployed, demo-ready product. No gold-plating.

## One-sentence pitch
CLAUSE reads an insurance policy and a claim, renders APPROVE / FLAG / DENY in seconds, and cites every decision point to a verbatim policy clause — with each citation **programmatically verified** to exist in the source before it is shown. Powered by open-weight **Gemma** running on **AMD** (Fireworks API primary; MI300X + vLLM/ROCm via env swap).

## Why this wins (judging map)
- **Use of AMD platforms:** Gemma served via Fireworks (AMD Instinct-backed) and/or self-hosted on an MI300X droplet with vLLM on ROCm — one env var switches between them.
- **Originality:** not a chatbot. Zero-hallucination-by-construction: extractive citations + span validation. Unverified citations are visibly rejected in the UI.
- **Business value:** claims adjudication is a costly, regulated, "hair-on-fire" workflow; auditability is the blocker for AI adoption there.
- **Completeness:** end-to-end — upload/paste → decision → cited evidence → exportable audit record. Deployed at a public URL. Containerized.

## Stack (frozen — do not renegotiate)
- Python 3.11, FastAPI + Uvicorn, single container, `linux/amd64`
- Inference: OpenAI SDK → `OPENAI_BASE_URL` (Fireworks default; vLLM/MI300X optional)
- Model: Gemma (see `.env.example`; verify exact Fireworks model ID via `scripts/smoke_test.py --list`)
- Frontend: single `static/index.html` (vanilla JS + CSS, no build step), served by FastAPI
- No database, no auth, no user accounts. State lives in the request.

## Commands
- Run dev: `uvicorn app.main:app --reload --port 8000`
- Smoke test inference: `python scripts/smoke_test.py`
- List available models: `python scripts/smoke_test.py --list`
- Docker: `docker build --platform linux/amd64 -t clause . && docker run -p 8000:8000 --env-file .env clause`

## Environment
Copy `.env.example` → `.env`. Required: `FIREWORKS_API_KEY`. Never commit `.env`.

## Working method (established discipline)
- `DECISIONS.md` is append-only (DEC-NNN). Log every significant choice.
- `PROGRESS.md` updated at session end via `/session-end`.
- Build spec lives in `docs/v0.1/` (KICKOFF + PRD + RESEARCH). Read all three before writing code.
- Scope freeze is DEC-008. If a feature is not in the PRD's MVP list, it does not get built before submission.

## Hard rules
1. The app must work end-to-end on Fireworks alone. MI300X is an upgrade, never a dependency.
2. Every citation shown to the user MUST pass `app/validation.py` (exact-substring match against source). Failed citations render as rejected, never silently dropped — the rejection is a feature.
3. Deploy early (by mid-build), not at the end. A local-only demo scores as if it doesn't exist.
4. Keep the LLM layer to ONE structured call per adjudication. No chains.
