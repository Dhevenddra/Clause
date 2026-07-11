# CLAUSE — every decision, cited

**Auditable AI claims adjudication.** CLAUSE reads an insurance policy and a claim, renders **APPROVE / FLAG / DENY** in seconds, and grounds every decision point in a verbatim policy clause — each citation **programmatically verified** to exist in the source before it is shown. Citations that fail verification are visibly rejected, never silently dropped. Trust enforced by code, not promised by prompt.

Built for the **AMD Developer Hackathon: ACT II** (Track 3 — Unicorn). Powered by open-weight **Google Gemma** served on **AMD**: Fireworks AI by default, or self-hosted on an **AMD Instinct MI300X** with vLLM on ROCm — switching is one environment variable.

## Quick start
```bash
cp .env.example .env        # add your FIREWORKS_API_KEY
pip install -r requirements.txt
python scripts/smoke_test.py --list   # confirm the served Gemma model ID → set MODEL_ID in .env
python scripts/smoke_test.py          # end-to-end adjudication of a demo scenario
uvicorn app.main:app --port 8000      # open http://localhost:8000
```

## Docker
```bash
docker build --platform linux/amd64 -t clause .
docker run -p 8000:8000 --env-file .env clause
```

## Run Gemma on an AMD MI300X instead
On an AMD GPU pod / Developer Cloud droplet (ROCm + vLLM image):
```bash
vllm serve google/gemma-4-31b-it   # any served Gemma variant works
```
Then in `.env`: `OPENAI_BASE_URL=http://<pod-address>:8000/v1` and set `MODEL_ID` to the served name. Same app, zero code changes.

## How the trust core works
1. One structured Gemma call returns a decision + points, each with a **verbatim** policy quote.
2. `app/validation.py` normalizes both sides (whitespace, unicode quotes/dashes) and requires an exact substring match, mapping the match back to a character span in the original text.
3. Verified points get a **✓ VERIFIED IN SOURCE** stamp and a click-to-highlight of the exact clause. Failed points render struck-through: **✗ NOT IN SOURCE — excluded from decision basis**.
4. Every adjudication produces a downloadable audit record: SHA-256 of both inputs, model ID, endpoint, timestamp, latency, per-citation validation results.

## Architecture
FastAPI + vanilla-JS single container · OpenAI-compatible client → Fireworks or vLLM/ROCm · no DB, no chains — one model call per adjudication.

## License
MIT. Gemma weights are Apache 2.0 (Google DeepMind).
