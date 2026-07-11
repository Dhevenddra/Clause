"""Edge-case checks for app/validation.py (H5 trust polish).

Run: python scripts/test_validation.py — prints a table, exits 1 on any failure.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.validation import find_span

SRC = (
    "The policy’s “grace period” — thirty (30) days – applies to    all renewals.\n"
    "Section 2: Flood damage is excluded.\n"
    "Deductible: INR 5,000 per event."
)

# (name, quote, should_verify)
CASES = [
    ("exact match",             "Flood damage is excluded.",                       True),
    ("curly->straight quotes",  'The policy\'s "grace period"',                    True),
    ("em/en-dash unification",  "- thirty (30) days -",                            True),
    ("whitespace collapse",     "applies to all renewals.",                        True),
    ("case-insensitive",        "FLOOD DAMAGE IS EXCLUDED.",                       True),
    ("nbsp handling",           "Deductible: INR 5,000 per event.",                True),
    ("span across newline",     "all renewals. Section 2",                         True),
    ("paraphrase must FAIL",    "Flood damage is not covered",                     False),
    ("fabrication must FAIL",   "All claims require a certified inspection.",      False),
    ("empty quote must FAIL",   "",                                                False),
    ("whitespace-only FAIL",    "   \n\t ",                                        False),
]


def main() -> int:
    failures = 0
    for name, quote, should in CASES:
        span = find_span(SRC, quote)
        got = span is not None
        ok = got == should
        failures += not ok
        extract = f" -> {SRC[span[0]:span[1]]!r}" if span else ""
        print(f"{'PASS' if ok else 'FAIL'}  {name:26} verified={got}{extract}")
    print(f"\n{len(CASES) - failures}/{len(CASES)} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
