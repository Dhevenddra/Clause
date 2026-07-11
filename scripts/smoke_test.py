"""H1 smoke test.

  python scripts/smoke_test.py --list   # list served models; find the exact Gemma ID, put it in .env
  python scripts/smoke_test.py          # full adjudication of demo scenario 'deny' + validation report
"""
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI  # noqa: E402


def list_models():
    client = OpenAI(base_url=os.getenv("OPENAI_BASE_URL", "https://api.fireworks.ai/inference/v1"),
                    api_key=os.getenv("FIREWORKS_API_KEY") or os.getenv("OPENAI_API_KEY", ""))
    models = client.models.list()
    gemma = [m.id for m in models.data if "gemma" in m.id.lower()]
    print(f"{len(models.data)} models served. Gemma models:")
    for m in gemma or ["  (none found — check Discord for the served Gemma ID)"]:
        print(" ", m)


def run_adjudication():
    from app.adjudicator import adjudicate, MODEL_ID
    demo = Path(__file__).resolve().parent.parent / "demo"
    policy = (demo / "sample_policy.md").read_text()
    claim = (demo / "claim_deny.md").read_text()
    print(f"Model: {MODEL_ID}\nAdjudicating demo 'deny' scenario…\n")
    result = adjudicate(policy, claim)
    print(json.dumps(result, indent=2))
    ok = result["audit"]["citations_verified"]
    total = result["audit"]["citations_total"]
    print(f"\n=== {result['decision']} · risk {result['risk_score']} · citations verified {ok}/{total} ===")
    if result["decision"] != "DENY":
        print("WARNING: expected DENY for this scenario — inspect rationale, consider tightening prompts.py")
    if total and ok / total < 0.7:
        print("WARNING: verification rate below 70% — Gemma is paraphrasing; strengthen rule 2 in the system prompt")


if __name__ == "__main__":
    if "--list" in sys.argv:
        list_models()
    else:
        run_adjudication()
