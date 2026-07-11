"""Generate per-scene narration MP3s with edge-tts and print durations.

Run: python video/narration.py
"""
import asyncio
import json
import subprocess
from pathlib import Path

import edge_tts

VOICE = "en-US-AndrewNeural"
OUT = Path(__file__).parent / "audio"
OUT.mkdir(exist_ok=True)

SCENES = {
    "s1_problem": (
        "Insurers can't use AI to adjudicate claims. Not because the models aren't smart enough — "
        "but because they can't be audited. One unexplainable denial is a compliance event. "
        "CLAUSE fixes the trust problem."
    ),
    "s2_intro": (
        "This is CLAUSE, live on the web, powered by open-weight Gemma. Everything you're about to "
        "see is real inference on the deployed product. Let's load a real case: a homeowner claiming "
        "for rot damage, discovered months after it began."
    ),
    "s3_verdict": (
        "One click. While Gemma works, CLAUSE displays the SHA-256 hashes of exactly what is being "
        "adjudicated. The verdict: DENY, risk ninety-five — with a plain-language rationale a "
        "policyholder could actually understand."
    ),
    "s4_ledger": (
        "And here is the product. The citation ledger. Every decision point quotes the policy "
        "verbatim — and CLAUSE verifies each quote, character for character, against the source "
        "before it is ever shown. Click a citation — and the exact clause lights up in the policy."
    ),
    "s5_adversarial": (
        "Now let's attack it. This claim invents three policy provisions that don't exist: a "
        "replacement-value guarantee, an emergency-response promise, and an inflated weekly "
        "allowance. CLAUSE grounds none of them. It flags the claim, checks the inflated ask "
        "against the real clause, and lists exactly what information is missing. And if a quote "
        "ever fails verification, it is rejected on screen — struck through, never hidden."
    ),
    "s6_audit": (
        "Every adjudication exports an audit record: input hashes, model identity, timestamp, and "
        "per-citation verification results. That is what a regulator actually wants to see."
    ),
    "s7_tech": (
        "Under the hood: one structured call to Gemma. No chains. No agents. Served on Fireworks "
        "A.I. — and the identical app runs Gemma on an AMD Instinct MI300X with v.L.L.M. on ROCm, "
        "by changing a single environment variable."
    ),
    "s8_close": (
        "Claims adjudication is a massive, regulated, hair-on-fire workflow — and CLAUSE is the "
        "version of AI that compliance can say yes to. CLAUSE. Every decision, cited."
    ),
}


async def synth(name: str, text: str) -> None:
    await edge_tts.Communicate(text, VOICE, rate="+4%").save(str(OUT / f"{name}.mp3"))


def duration(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "quiet", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        capture_output=True, text=True)
    return round(float(out.stdout.strip()), 2)


async def main() -> None:
    await asyncio.gather(*(synth(n, t) for n, t in SCENES.items()))
    durs = {n: duration(OUT / f"{n}.mp3") for n in SCENES}
    total = round(sum(durs.values()), 1)
    print(json.dumps(durs, indent=2))
    print(f"total narration: {total}s")
    (OUT / "durations.json").write_text(json.dumps(durs))


if __name__ == "__main__":
    asyncio.run(main())
