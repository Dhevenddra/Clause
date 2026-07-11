"""CLAUSE — FastAPI entrypoint. Serves the static UI + /adjudicate + /demo scenarios."""
from __future__ import annotations
import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app.adjudicator import adjudicate, MODEL_ID

ROOT = Path(__file__).resolve().parent.parent
DEMO_DIR = ROOT / "demo"

app = FastAPI(title="CLAUSE", version="0.1.0")


class AdjudicateRequest(BaseModel):
    policy: str = Field(min_length=40, max_length=60_000)
    claim: str = Field(min_length=20, max_length=30_000)


@app.post("/adjudicate")
def post_adjudicate(req: AdjudicateRequest):
    try:
        return adjudicate(req.policy, req.claim)
    except Exception as exc:  # surface plainly; UI renders the message
        raise HTTPException(status_code=502, detail=f"Adjudication failed: {exc}")


@app.get("/demo/{name}")
def get_demo(name: str):
    """name in {approve, flag, deny} → {"policy": ..., "claim": ...}"""
    if name not in {"approve", "flag", "deny"}:
        raise HTTPException(404, "Unknown scenario")
    policy = (DEMO_DIR / "sample_policy.md").read_text()
    claim = (DEMO_DIR / f"claim_{name}.md").read_text()
    return {"policy": policy, "claim": claim}


@app.get("/health")
def health():
    return {"ok": True, "model": MODEL_ID}


app.mount("/", StaticFiles(directory=ROOT / "static", html=True), name="static")
