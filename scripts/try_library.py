"""Adjudicate a demo/library pair through the local API (or direct engine).

Usage: python scripts/try_library.py motor|travel
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.adjudicator import adjudicate

name = sys.argv[1] if len(sys.argv) > 1 else "motor"
lib = Path(__file__).resolve().parent.parent / "demo" / "library"
policy = (lib / f"{name}_policy.md").read_text(encoding="utf-8")
claim = (lib / f"{name}_claim.md").read_text(encoding="utf-8")

r = adjudicate(policy, claim)
a = r["audit"]
print(f'{r["decision"]} risk={r["risk_score"]} verified={a["citations_verified"]}/{a["citations_total"]} {a["latency_s"]}s')
for p in r["points"]:
    print(f'  [{"OK" if p["verified"] else "XX"}] ({p["supports"]}) {p["finding"][:90]}')
if r["missing_information"]:
    print("  missing:", "; ".join(r["missing_information"])[:200])
