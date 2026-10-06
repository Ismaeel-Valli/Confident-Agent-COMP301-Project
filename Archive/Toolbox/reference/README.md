# Historical scoring reference

These files preserve the original V3 formula implementation for comparison. The repaired TypeScript implementation retains canonical weights/tier factors but changes missing-layer handling and delivery gates to match the latest progress report. It is no longer a line-for-line port. See `../FIXES_AND_SETUP.md`.

# Reference implementation

This folder holds the original, tested Python source that `src/confidenceAgentTools.ts`'s
`compute_ewcs` tool is ported from, kept here for comparison/maintenance:

- `confident_agent/ewcs.py` — the EWCS accumulator (`EWCS`, `LayerContribution`, `EWCSReport`,
  `LAYER_WEIGHTS`, `DEFAULT_TIER_FACTORS`). Ported line-for-line in logic into the
  `EWCSAccumulator` class in `../src/confidenceAgentTools.ts`.
- `confident_agent/schemas.py` — `LayerName`, `VerificationState`, `EvidenceTier`, `LayerResult`.
  Mirrored as TypeScript types in the same file.
- `EWCS_Documentation.txt` — the full technical write-up (formula, worked example, design
  rationale, the ten `test_ewcs.py` tests, failure modes). The worked example in §6.3 is used as
  a regression check for the TS port's arithmetic.

Not yet supplied, so not ported: `decision.py` (the real `DecisionPolicy` — `make_decision` in
the TS module is a placeholder two-rule stand-in) and `verify.py` (the six layer verifiers — the
`verify_*` tools in the TS module are an independent implementation, not a port).

These files aren't imported by the plugin (it's a Node/TypeScript project) — they're kept purely
as the source of truth to diff the TS port against if `ewcs.py` changes.
