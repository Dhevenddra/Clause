# PRD — CLAUSE v0.1

## Problem
Insurers and TPAs spend enormous manual effort adjudicating routine claims, and regulated environments can't adopt LLMs because outputs aren't auditable. A wrong or unexplainable denial is a compliance event.

## Solution
An adjudication engine whose every conclusion is grounded in a verbatim, machine-verified policy clause. If the model can't ground a point in the source text, the point is visibly rejected. Trust is enforced by code, not promised by prompt.

## MVP features (DEC-008 — final)
1. **Inputs:** two text panes — Policy and Claim. Paste text, or upload .txt/.md. Three one-click demo scenarios (approve / flag / deny) pre-loaded from `demo/`.
2. **Adjudicate:** one structured Gemma call → decision object (schema below).
3. **Decision banner:** APPROVE (green) / FLAG (amber) / DENY (red) + risk score 0–100 + one-paragraph plain-language rationale.
4. **Citation ledger (signature element):** each decision point as a card — the point, the verbatim quoted clause (monospace), the verification stamp. Clicking a card scrolls-to and highlights the clause span in the Policy pane.
5. **Rejected citations:** any quote failing validation renders in a struck, greyed state: "✗ could not be verified in policy — excluded from decision basis." Never hidden.
6. **Audit record:** "Download audit record" → JSON file: inputs' SHA-256 hashes, model ID, timestamp, full decision object, per-citation validation results.

## Adjudication JSON schema (contract between prompt, backend, UI)
```json
{
  "decision": "APPROVE | FLAG | DENY",
  "risk_score": 0,
  "rationale": "2-4 sentence plain-language summary",
  "points": [
    {
      "finding": "one-sentence decision point",
      "citation": "verbatim quote copied exactly from the POLICY text",
      "supports": "APPROVE | FLAG | DENY"
    }
  ],
  "missing_information": ["optional list of facts that would change the decision"]
}
```
Backend adds per-point after validation: `"verified": true|false`, `"span": [start, end] | null`.

## UI design brief (for the frontend pass — read with frontend-design skill)
- **Subject world:** underwriting desks, audit ledgers, rubber stamps, policy paper. NOT a chatbot, NOT a dashboard.
- **Palette (tokens):** `--ink #1B1F2A` (near-black blue ink), `--paper #FAFAF7`, `--stamp-red #B3372E` (DENY), `--amber #B07C24` (FLAG), `--verified #2E6B4F` (APPROVE/verified), `--rule #D8D6CE` (hairlines). Avoid the cream+terracotta AI-default look; this is ink-on-paper, cooler and harder.
- **Type:** characterful grotesque for display (e.g., 'Archivo' or 'Space Grotesk' via Google Fonts), quiet humanist body ('Inter'), **monospace for all quoted evidence** ('IBM Plex Mono') — evidence looks like evidence.
- **Signature:** the verification stamp on each citation card — a small bordered seal, "✓ VERIFIED IN SOURCE" / "✗ NOT IN SOURCE", with the clause highlight sweeping in on click. Spend the boldness here; everything else disciplined.
- **Motion:** one orchestrated moment — decision banner + cards cascade in once on adjudication. Respect reduced-motion. No ambient effects.
- **States:** loading (adjudicating…, with the input hashes shown — signals integrity), empty (invitation: "Load a demo scenario or paste a policy"), errors in plain language ("The model returned malformed output. Retried once. Try again or simplify the claim.").
- Responsive to mobile; visible keyboard focus.

## Non-goals (do not build)
PDF parsing, OCR, multi-claim queues, accounts, persistence, chat, agent frameworks, model comparison UI.

## Success = a judge, in 60 seconds on the deployed URL, clicks "Deny scenario", watches CLAUSE deny it, clicks a citation, sees the exact clause light up in the policy, and sees one hallucinated citation get visibly rejected.
