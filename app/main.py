"""CLAUSE — FastAPI entrypoint. Serves the static UI + /adjudicate + /demo scenarios."""
from __future__ import annotations
import json
import threading
import time
from collections import defaultdict, deque
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app.adjudicator import adjudicate, MODEL_ID

ROOT = Path(__file__).resolve().parent.parent
DEMO_DIR = ROOT / "demo"

app = FastAPI(title="CLAUSE", version="0.1.0")

# --- credit guard: the GPU behind /adjudicate bills per second while hot. ---
# In-memory throttle: per-IP and global hourly caps + a small concurrency gate.
# Generous for judges, hostile to loops. No dependencies, resets on restart.
_IP_LIMIT, _GLOBAL_LIMIT, _WINDOW_S = 15, 80, 3600
_ip_hits: dict[str, deque] = defaultdict(deque)
_all_hits: deque = deque()
_hits_lock = threading.Lock()
_concurrency = threading.Semaphore(2)


def _client_ip(request: Request) -> str:
    fwd = request.headers.get("x-forwarded-for")
    return fwd.split(",")[0].strip() if fwd else (request.client.host if request.client else "?")


def _check_rate(ip: str) -> None:
    now = time.time()
    with _hits_lock:
        for q in (_ip_hits[ip], _all_hits):
            while q and now - q[0] > _WINDOW_S:
                q.popleft()
        if len(_ip_hits[ip]) >= _IP_LIMIT or len(_all_hits) >= _GLOBAL_LIMIT:
            raise HTTPException(429, "Rate limit reached — CLAUSE runs on hackathon GPU credits. Please try again later.")
        _ip_hits[ip].append(now)
        _all_hits.append(now)


class AdjudicateRequest(BaseModel):
    policy: str = Field(min_length=40, max_length=60_000)
    claim: str = Field(min_length=20, max_length=30_000)


@app.post("/adjudicate")
def post_adjudicate(req: AdjudicateRequest, request: Request):
    _check_rate(_client_ip(request))
    if not _concurrency.acquire(timeout=90):
        raise HTTPException(429, "CLAUSE is busy with other adjudications — try again in a minute.")
    try:
        return adjudicate(req.policy, req.claim)
    except HTTPException:
        raise
    except Exception as exc:  # surface plainly; UI renders the message
        if "DEPLOYMENT_SCALING_UP" in str(exc):
            raise HTTPException(status_code=503,
                                detail="The Gemma GPU is waking from idle — this can take a couple of minutes. Please try again shortly.")
        raise HTTPException(status_code=502, detail=f"Adjudication failed: {exc}")
    finally:
        _concurrency.release()


@app.get("/demo/{name}")
def get_demo(name: str):
    """name in {approve, flag, deny} → {"policy": ..., "claim": ...}"""
    if name not in {"approve", "flag", "deny"}:
        raise HTTPException(404, "Unknown scenario")
    policy = (DEMO_DIR / "sample_policy.md").read_text(encoding="utf-8")
    claim = (DEMO_DIR / f"claim_{name}.md").read_text(encoding="utf-8")
    return {"policy": policy, "claim": claim}


@app.get("/health")
def health():
    return {"ok": True, "model": MODEL_ID}


app.mount("/", StaticFiles(directory=ROOT / "static", html=True), name="static")
