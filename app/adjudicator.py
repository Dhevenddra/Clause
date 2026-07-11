"""Adjudication engine: one structured Gemma call via OpenAI-compatible endpoint.

Fireworks by default; an MI300X vLLM endpoint via the same env vars (DEC-003).
"""
from __future__ import annotations
import hashlib
import json
import os
import re
import time

from openai import OpenAI

from app.prompts import build_messages
from app.validation import validate_points

BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.fireworks.ai/inference/v1")
API_KEY = os.getenv("FIREWORKS_API_KEY") or os.getenv("OPENAI_API_KEY", "")
MODEL_ID = os.getenv("MODEL_ID", "accounts/fireworks/models/gemma-4-31b-it")  # verify via smoke_test --list

_client = OpenAI(base_url=BASE_URL, api_key=API_KEY)

_VALID_DECISIONS = {"APPROVE", "FLAG", "DENY"}


def _extract_json(raw: str) -> dict:
    """Parse model output into a dict, tolerating stray fences/prose."""
    raw = raw.strip()
    if raw.startswith("```"):
        raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw, flags=re.S)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        m = re.search(r"\{.*\}", raw, flags=re.S)
        if not m:
            raise
        return json.loads(m.group(0))


def _call_model(messages: list[dict]) -> dict:
    resp = _client.chat.completions.create(
        model=MODEL_ID,
        messages=messages,
        temperature=0.1,
        max_tokens=2000,
    )
    return _extract_json(resp.choices[0].message.content or "")


def adjudicate(policy: str, claim: str) -> dict:
    """Run one adjudication. One retry with error feedback on malformed output."""
    messages = build_messages(policy, claim)
    started = time.time()
    try:
        data = _call_model(messages)
    except (json.JSONDecodeError, KeyError) as exc:
        messages.append({"role": "user",
                         "content": f"Your previous output was invalid ({exc}). Respond again with ONLY the JSON object."})
        data = _call_model(messages)

    decision = str(data.get("decision", "FLAG")).upper()
    if decision not in _VALID_DECISIONS:
        decision = "FLAG"

    points = validate_points(policy, data.get("points", []) or [])

    return {
        "decision": decision,
        "risk_score": max(0, min(100, int(data.get("risk_score", 50) or 50))),
        "rationale": str(data.get("rationale", "")),
        "points": points,
        "missing_information": data.get("missing_information", []) or [],
        "audit": {
            "model_id": MODEL_ID,
            "base_url": BASE_URL,
            "policy_sha256": hashlib.sha256(policy.encode()).hexdigest(),
            "claim_sha256": hashlib.sha256(claim.encode()).hexdigest(),
            "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "latency_s": round(time.time() - started, 2),
            "citations_total": len(points),
            "citations_verified": sum(1 for p in points if p["verified"]),
        },
    }
