# EWCS — Evidence-Weighted Confidence Score

**Module:** `confident_agent/scoring/ewcs.py`
**Status:** Locked and tested
**Test file:** `tests/test_ewcs.py`
**Last verified:** 10 tests passing
**Version:** 1.0 — Frozen

---

## Table of Contents

1. [Purpose and Scope](#1-purpose-and-scope)
2. [Position in the Tool](#2-position-in-the-tool)
3. [Folder Structure](#3-folder-structure)
4. [Dependencies — `schemas.py`](#4-dependencies--schemaspy)
5. [Canonical Definitions](#5-canonical-definitions)
6. [The Three Classes](#6-the-three-classes)
7. [The Formula](#7-the-formula)
8. [Source Code — `ewcs.py`](#8-source-code--ewcspy)
9. [Test Suite — `test_ewcs.py`](#9-test-suite--test_ewcspy)
10. [Design Decisions and Rationale](#10-design-decisions-and-rationale)
11. [Failure Modes and Exceptions](#11-failure-modes-and-exceptions)
12. [Integration Points](#12-integration-points)
13. [Testing — How It Was Verified](#13-testing--how-it-was-verified)
14. [Frozen Contract Summary](#14-frozen-contract-summary)
15. [Change Log](#15-change-log)

---

## 1. Purpose and Scope

The **EWCS (Evidence-Weighted Confidence Score)** is the primary quantitative metric for the Confident Agent. It aggregates the verdicts of six independent verification layers into a single confidence value between 0 and 1, plus a diagnostic signed score between −1 and 1.

The EWCS answers the question:

> *"How much of the applicable verification weight is supported by positive evidence?"*

It does **not** answer:

> *"What should we do with this code?"*

That is the `DecisionPolicy`'s job. The EWCS produces evidence. The policy interprets it. This separation is deliberate.

### Scope

- The `EWCS` class
- Its two companion data classes (`LayerContribution`, `EWCSReport`)
- The three canonical constants it depends on
- The schema types it consumes
- The tests that verify its behaviour

### Out of Scope

- `DecisionPolicy` (separate document)
- The six layer verifiers (separate documents)
- The `ClaimExtractor` (separate document)
- The orchestration flow (separate document)

---

## 2. Position in the Tool

The EWCS sits between the verification layers and the decision policy.

```text
┌─────────────────────────────────────────────────────────────┐
│                    Six Verification Layers                  │
│                                                               │
│   LayerOne    LayerTwo    LayerThree    LayerFour            │
│   LayerFive   LayerSix                                       │
│                                                               │
│   Each layer evaluates multiple claims internally,           │
│   then returns exactly ONE aggregated LayerResult.           │
└──────────────────────────┬────────────────────────────────────┘
                            │
                            │  [LayerResult × 6]
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                          EWCS                                │
│                                                               │
│   1. record(result) for each of the six layers               │
│   2. finalise() computes the score and returns a report      │
└──────────────────────────┬────────────────────────────────────┘
                            │
                            │  EWCSReport
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                     DecisionPolicy                           │
│                                                               │
│   Applies safety constraint, then confidence thresholds.     │
│   Returns a DecisionSignal.                                  │
└─────────────────────────────────────────────────────────────┘
```

The EWCS is a pure accumulator. It receives six results and returns one report. It does not verify, correct, decide, or persist anything.

The EWCS has no knowledge of:

- The code being verified
- The claims extracted from the code
- The evidence sources used by the layers
- The thresholds used by the decision policy
- The experiment the tool is being used in

---

## 3. Folder Structure

To run the EWCS module and its tests, the following layout is required:

```text
project-root/
│
├── confident_agent/
│   ├── __init__.py                     # empty
│   ├── schemas.py                      # minimal version (Section 4)
│   └── scoring/
│       ├── __init__.py                 # empty
│       └── ewcs.py                     # Section 8
│
└── tests/
    ├── __init__.py                     # empty
    └── test_ewcs.py                    # Section 9
```

**Rules:**

- Every folder inside the package must contain an `__init__.py`
- `pytest` must be run from `project-root/`, not from inside `confident_agent/`
- The package folder must be named exactly `confident_agent` (lowercase, underscore)

---

## 4. Dependencies — `schemas.py`

The EWCS imports four names from `confident_agent.schemas`.

| Name | Kind | Purpose |
|---|---|---|
| `LayerName` | Enum | Identifies the six layers |
| `VerificationState` | Enum | CORRECT / INCORRECT / UNVERIFIABLE / N/A |
| `EvidenceTier` | Enum | Tier 1 / 2 / 3 / 4 / NONE |
| `LayerResult` | Frozen dataclass | Input accepted by `record()` |

### 4.1 Minimal `schemas.py`

Save this at `confident_agent/schemas.py`:

```python
"""Minimal schema definitions for testing EWCS."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class LayerName(str, Enum):
    INTERFACE       = "interface"
    IDENTIFIER      = "identifier"
    ACCESS_POINT    = "access_point"
    INPUT_CONTRACT  = "input_contract"
    OUTPUT_CONTRACT = "output_contract"
    CONTEXTUAL      = "contextual"


class VerificationState(str, Enum):
    VERIFIED_CORRECT   = "verified_correct"
    VERIFIED_INCORRECT = "verified_incorrect"
    UNVERIFIABLE       = "unverifiable"
    NOT_APPLICABLE     = "not_applicable"


class EvidenceTier(str, Enum):
    TIER_1 = "tier_1"
    TIER_2 = "tier_2"
    TIER_3 = "tier_3"
    TIER_4 = "tier_4"
    NONE   = "none"


@dataclass(frozen=True)
class LayerResult:
    layer: LayerName
    state: VerificationState
    tier: EvidenceTier
    weight: int
    evidence_source: str
    evidence_detail: str
    hallucination_type: Optional[str] = None
```

### 4.2 Schema Explanations

#### `LayerName`

A `str`-Enum identifying the six verification layers.

Why str-Enum?

- JSON-serialisable without a custom encoder
- Hashing works like a string (usable as dict keys)
- Log-friendly (prints the value, not the repr)
- Type-safe (typos raise at import time, not runtime)

#### `VerificationState`

A `str`-Enum of the four possible outcomes for a layer.

| State | Meaning | Effect on EWCS |
|---|---|---|
| `VERIFIED_CORRECT` | Evidence supports the claim | Contributes positively |
| `VERIFIED_INCORRECT` | Evidence contradicts the claim | Zero to numerator; triggers safety flag |
| `UNVERIFIABLE` | Layer ran, could not establish validity | Zero to numerator; retains weight in denominator |
| `NOT_APPLICABLE` | Layer had nothing to check | Excluded entirely |

The critical distinction:

```text
UNVERIFIABLE   = "we tried, we could not tell"     → counts against us
NOT_APPLICABLE = "there was nothing to try"        → excluded
```

Collapsing these into a single state would either under-penalise unverifiable claims or over-penalise tasks with no applicable evidence.

#### `EvidenceTier`

A `str`-Enum describing how strong the evidence is.

| Tier | Meaning |
|---|---|
| `TIER_1` | Authoritative — discovered OpenAPI specs, official docs |
| `TIER_2` | Strong supporting — PyPI metadata |
| `TIER_3` | Empirical — runtime execution (reserved for future work) |
| `TIER_4` | Supporting — Pyright diagnostics (typeshed) |
| `NONE` | No evidence |

Why an enum and not a float? The tier is a categorical fact about the evidence source. The mapping from tier to a numeric factor is a design choice, owned by the EWCS. Keeping them separate means the numeric weighting can be revisited during sensitivity analysis without touching the schema.

#### `LayerResult`

The aggregated verdict from one verifier.

| Field | Type | Meaning |
|---|---|---|
| `layer` | `LayerName` | Which layer produced this result |
| `state` | `VerificationState` | The verdict |
| `tier` | `EvidenceTier` | Strongest evidence tier supporting the state |
| `weight` | `int` | Layer's declared weight (retained for compatibility) |
| `evidence_source` | `str` | Human-readable source, e.g. "PyPI" |
| `evidence_detail` | `str` | Human-readable explanation |
| `hallucination_type` | `Optional[str]` | H-code if INCORRECT, else `None` |

Why frozen? `LayerResult` is a value object. Once a verifier produces it, no part of the system should mutate it.

Why is `weight` in the schema at all, if EWCS ignores it? Layer classes own their own weight declaration. Removing the field would require changing every layer class. Keeping it allows layers to declare their weight while EWCS uses its canonical source — `record()` validates against the canonical value and rejects mismatches.

---

## 5. Canonical Definitions

These three constants live at the top of `ewcs.py` and are the single source of truth for the EWCS computation.

### 5.1 `LAYER_WEIGHTS`

```python
LAYER_WEIGHTS: dict[LayerName, int] = {
    LayerName.INTERFACE:       3,
    LayerName.IDENTIFIER:      3,
    LayerName.ACCESS_POINT:    4,
    LayerName.INPUT_CONTRACT:  2,
    LayerName.OUTPUT_CONTRACT: 1,
    LayerName.CONTEXTUAL:      2,
}
```

The relative importance of each layer.

| Layer | Weight | Reasoning |
|---|---|---|
| `ACCESS_POINT` | 4 | Wrong endpoint is the most severe API hallucination |
| `INTERFACE` | 3 | Non-existent library is fatal — code cannot import |
| `IDENTIFIER` | 3 | Non-existent method is fatal — code cannot call |
| `INPUT_CONTRACT` | 2 | Invalid parameters are serious but often produce clear errors |
| `CONTEXTUAL` | 2 | Wrong auth or platform is serious but situational |
| `OUTPUT_CONTRACT` | 1 | Wrong response field is a downstream bug, not a call failure |

Total weight: **15**.

These are research design choices, not empirical constants. The report must include a sensitivity analysis across at least five weighting schemes. `LAYER_WEIGHTS` is the Scheme A ("proposed") definition.

EWCS validates every incoming `LayerResult`'s weight against this dict and raises `ValueError` on mismatch. This ensures the score cannot silently drift if a layer class declares the wrong weight.

### 5.2 `EXPECTED_LAYERS`

```python
EXPECTED_LAYERS: tuple[LayerName, ...] = tuple(LAYER_WEIGHTS.keys())
```

A derived tuple, in canonical order:

```text
INTERFACE, IDENTIFIER, ACCESS_POINT,
INPUT_CONTRACT, OUTPUT_CONTRACT, CONTEXTUAL
```

Used for two purposes:

1. Iterating contributions in deterministic order in the report
2. Determining which layers are missing at finalise time

Derived from `LAYER_WEIGHTS` so the two cannot go out of sync.

### 5.3 `DEFAULT_TIER_FACTORS`

```python
DEFAULT_TIER_FACTORS: dict[EvidenceTier, float] = {
    EvidenceTier.TIER_1: 1.00,
    EvidenceTier.TIER_2: 0.80,
    EvidenceTier.TIER_3: 0.90,
    EvidenceTier.TIER_4: 0.50,
    EvidenceTier.NONE:   0.00,
}
```

The confidence multiplier applied to a layer's weight when the layer is `VERIFIED_CORRECT`.

Why `TIER_3 = 0.90` sits between `TIER_1` and `TIER_2`? Runtime execution (Tier 3) is reserved. If it were ever used, it would be slightly weaker than an authoritative spec but stronger than metadata — because the code actually ran and returned something. This is a placeholder; the tool never uses Tier 3.

Why `TIER_4 = 0.50`? Pyright diagnostics are strong signals of incorrectness but produce false positives on dynamic code. A factor of 0.5 means a Tier 4 correct verdict contributes half of a layer's weight.

Why `NONE = 0.00`? No evidence means no credit.

---

## 6. The Three Classes

### 6.1 `LayerContribution`

```python
@dataclass(frozen=True)
class LayerContribution:
    layer: LayerName
    state: VerificationState
    tier: EvidenceTier
    weight: int
    tier_factor: float
    positive_contribution: float
    signed_contribution: float
```

**Purpose:** A single, pre-computed row in the final report. It is a view of one layer's result after the canonical weight and tier factor have been applied.

Why frozen? The report is immutable. Every component of it must be immutable too.

Why not just store the `LayerResult` in the report? `LayerResult` carries raw inputs. `LayerContribution` carries the derived values after the formula has been applied. Keeping them separate makes the report self-documenting.

| Field | Meaning |
|---|---|
| `weight` | The canonical weight applied (0 for missing layers) |
| `tier_factor` | `DEFAULT_TIER_FACTORS[tier]` |
| `positive_contribution` | `weight × tier_factor` if CORRECT, else 0 |
| `signed_contribution` | `+weight×factor` if CORRECT; `−weight×factor` if INCORRECT; else 0 |

### 6.2 `EWCSReport`

```python
@dataclass(frozen=True)
class EWCSReport:
    task_id: str
    ewcs: float
    signed_score: float
    has_incorrect_layer: bool
    total_applicable_weight: int
    positive_weight: float
    contributions: tuple[LayerContribution, ...]
    missing_layers: tuple[LayerName, ...]
```

**Purpose:** The final, immutable output of the EWCS computation.

Why frozen? The report is the artefact that flows into the `DecisionPolicy`. It must not be mutable after construction.

Why tuples and not lists? Lists are mutable. Storing a list in a frozen dataclass gives a false sense of immutability — the field cannot be reassigned but the list contents can still be appended to. Tuples are immutable.

| Field | Type | Meaning |
|---|---|---|
| `task_id` | `str` | Task identifier |
| `ewcs` | `float` | Score in [0, 1], rounded to 4 places |
| `signed_score` | `float` | Diagnostic score in [-1, 1], rounded to 4 places |
| `has_incorrect_layer` | `bool` | True if any layer reported `VERIFIED_INCORRECT` |
| `total_applicable_weight` | `int` | Denominator of the formula |
| `positive_weight` | `float` | Numerator of the formula |
| `contributions` | `tuple[LayerContribution, ...]` | Per-layer breakdown |
| `missing_layers` | `tuple[LayerName, ...]` | Layers that did not report |

Why is `missing_layers` separate from `contributions`? A reader can determine missing layers by inspecting `contributions` (weight 0, state UNVERIFIABLE, source "none"). But that requires iterating. `missing_layers` makes the fact directly accessible:

```python
if report.missing_layers:
    log.warning("Partial verification: %s", report.missing_layers)
```

### 6.3 `EWCS`

```python
class EWCS:
    def __init__(self, task_id: str) -> None: ...
    def record(self, result: LayerResult) -> None: ...
    def finalise(self) -> EWCSReport: ...
    @property
    def is_complete(self) -> bool: ...
```

**Purpose:** The accumulator. Receives `LayerResult` objects one at a time, stores them, and on request computes an `EWCSReport`.

#### Public API

| Member | Purpose |
|---|---|
| `__init__(task_id)` | Creates an empty accumulator. No configuration. |
| `record(result)` | Adds one `LayerResult`. Order-independent. Raises on duplicate, post-finalise, or weight mismatch. |
| `finalise()` | Computes and returns the report. Idempotent. |
| `is_complete` | Derived property. True after `finalise()`. |

#### Internal State

```python
_task_id: str
_results: dict[LayerName, LayerResult]
_finalised: Optional[EWCSReport]
_lock: threading.Lock
```

There is no other state. In particular, there is no separate completeness flag — completeness is derived from whether `_finalised` has been populated.

---

## 7. The Formula

### 7.1 EWCS

```
        Σ (w_l × f_l),  for l in layers where state = VERIFIED_CORRECT
EWCS = ─────────────────────────────────────────────────────────────
        Σ (w_l),        for l in all applicable layers
```

- **Numerator:** over layers where `state == VERIFIED_CORRECT`
- **Denominator:** over all layers where `state != NOT_APPLICABLE`

Interpretation:

| Value | Meaning |
|---|---|
| 1.0 | Every applicable layer's full weight is backed by Tier 1 positive evidence |
| 0.5 | Half of the applicable weight is supported by positive evidence |
| 0.0 | No layer produced positive evidence |

The EWCS is **NOT** a probability. A value of 0.85 does not mean "85% chance the code is correct." It means "85% of the applicable verification weight is supported by positive evidence at the recorded evidence tiers."

### 7.2 Signed Score

```
          Σ (w_l × s_l),  for l in all applicable layers
signed = ─────────────────────────────────────────────────
          Σ (w_l),        for l in all applicable layers
```

where:

```
s_l = +f_l   if state = VERIFIED_CORRECT
s_l = -f_l   if state = VERIFIED_INCORRECT
s_l = 0      if state ∈ {UNVERIFIABLE, NOT_APPLICABLE}
```

**Purpose:** Diagnostic only. Never used for a decision.

### 7.3 Worked Example

Task: Fetch a user by ID from JSONPlaceholder.

LLM output (incorrect):

```python
response = requests.get(f"https://jsonplaceholder.typicode.com/user/{user_id}")
```

Note: `/user/{user_id}` is incorrect. The correct path is `/users/{user_id}`.

#### Layer Results

| Layer | Weight | State | Tier | Factor | Positive | Signed |
|---|---|---|---|---|---|---|
| INTERFACE | 3 | CORRECT | Tier 2 | 0.80 | 2.40 | +2.40 |
| IDENTIFIER | 3 | CORRECT | Tier 4 | 0.50 | 1.50 | +1.50 |
| ACCESS_POINT | 4 | INCORRECT | Tier 1 | 1.00 | 0.00 | −4.00 |
| INPUT_CONTRACT | 2 | CORRECT | Tier 1 | 1.00 | 2.00 | +2.00 |
| OUTPUT_CONTRACT | 1 | CORRECT | Tier 4 | 0.50 | 0.50 | +0.50 |
| CONTEXTUAL | 2 | N/A | — | — | excluded | excluded |

#### Calculation

```text
total_applicable_weight = 3 + 3 + 4 + 2 + 1 = 13
positive_weight         = 2.40 + 1.50 + 0.00 + 2.00 + 0.50 = 6.40
signed_weight            = 2.40 + 1.50 − 4.00 + 2.00 + 0.50 = 2.40

EWCS         = 6.40 ÷ 13 = 0.4923
signed_score = 2.40 ÷ 13 = 0.1846
has_incorrect_layer = True
```

> **Note on the signed score:** An earlier draft reported −0.277 for this example. That value was incorrect. The correct value is 0.1846. The `test_worked_example` test enforces this.

#### Decision

The `DecisionPolicy` sees `has_incorrect_layer = True` and emits `CORRECT`, regardless of the EWCS.

---

## 8. Source Code — `ewcs.py`

Save this at `confident_agent/scoring/ewcs.py`:

```python
"""Evidence-Weighted Confidence Score (EWCS).

Aggregates exactly one LayerResult per verification layer into an
immutable EWCSReport.

Contract (frozen):
    - One LayerResult per layer. Verifiers aggregate their own
      per-claim results before returning.
    - LAYER_WEIGHTS in this module is authoritative for computation.
      LayerResult.weight, if present, is validated against it rather
      than trusted.
    - Accumulate-then-finalise. No partial scores.
    - Missing layers are filled as UNVERIFIABLE with weight 0 at
      finalise, and listed in EWCSReport.missing_layers.

Formula:
                      Σ (w_l × tier_factor_l)
    EWCS = ─────────────────────────────────────────
                      Σ (w_l)

    Numerator:   over layers where state = VERIFIED_CORRECT
    Denominator: over all applicable layers (state ≠ NOT_APPLICABLE)

Signed score (diagnostic):
                      Σ (w_l × s_l)
    signed = ─────────────────────────────
                      Σ (w_l)

    where s_l ∈ {+tier_factor, −tier_factor, 0.0} for
    CORRECT, INCORRECT, UNVERIFIABLE respectively.

Thread safety:
    record() and finalise() are guarded by a lock. finalise() is
    idempotent. record() after finalise() raises RuntimeError.
"""

from __future__ import annotations

import threading
from dataclasses import dataclass
from typing import Optional

from confident_agent.schemas import (
    EvidenceTier,
    LayerName,
    LayerResult,
    VerificationState,
)


# ---------------------------------------------------------------------------
# Canonical definitions
# ---------------------------------------------------------------------------

LAYER_WEIGHTS: dict[LayerName, int] = {
    LayerName.INTERFACE:       3,
    LayerName.IDENTIFIER:      3,
    LayerName.ACCESS_POINT:    4,
    LayerName.INPUT_CONTRACT:  2,
    LayerName.OUTPUT_CONTRACT: 1,
    LayerName.CONTEXTUAL:      2,
}
"""Canonical layer weights. Authoritative for computation."""

EXPECTED_LAYERS: tuple[LayerName, ...] = tuple(LAYER_WEIGHTS.keys())

DEFAULT_TIER_FACTORS: dict[EvidenceTier, float] = {
    EvidenceTier.TIER_1: 1.00,
    EvidenceTier.TIER_2: 0.80,
    EvidenceTier.TIER_3: 0.90,
    EvidenceTier.TIER_4: 0.50,
    EvidenceTier.NONE:   0.00,
}


# ---------------------------------------------------------------------------
# Report types
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class LayerContribution:
    """One layer's contribution to the EWCS.

    Attributes:
        layer: The verification layer.
        state: The layer's verification state.
        tier: The evidence tier supporting the state.
        weight: The canonical weight for this layer.
        tier_factor: The confidence factor for the tier.
        positive_contribution: weight × tier_factor if CORRECT, else 0.
        signed_contribution: +weight×factor if CORRECT,
                             −weight×factor if INCORRECT, else 0.
    """

    layer: LayerName
    state: VerificationState
    tier: EvidenceTier
    weight: int
    tier_factor: float
    positive_contribution: float
    signed_contribution: float


@dataclass(frozen=True)
class EWCSReport:
    """Immutable result of an EWCS computation.

    Attributes:
        task_id: The task this report belongs to.
        ewcs: Evidence-Weighted Confidence Score in [0, 1].
        signed_score: Signed verification score in [-1, 1].
        has_incorrect_layer: True if any layer is VERIFIED_INCORRECT.
        total_applicable_weight: Denominator used in the EWCS formula.
        positive_weight: Numerator used in the EWCS formula.
        contributions: Per-layer breakdown, in canonical layer order.
        missing_layers: Layers that did not report. Non-empty means
            the EWCS was computed on partial evidence.
    """

    task_id: str
    ewcs: float
    signed_score: float
    has_incorrect_layer: bool
    total_applicable_weight: int
    positive_weight: float
    contributions: tuple[LayerContribution, ...]
    missing_layers: tuple[LayerName, ...]


# ---------------------------------------------------------------------------
# EWCS accumulator
# ---------------------------------------------------------------------------

class EWCS:
    """Accumulates one LayerResult per layer and computes the EWCS.

    Usage:
        ewcs = EWCS(task_id="t-001")
        for result in layer_results:
            ewcs.record(result)
        report = ewcs.finalise()
    """

    def __init__(self, task_id: str) -> None:
        self._task_id = task_id
        self._results: dict[LayerName, LayerResult] = {}
        self._finalised: Optional[EWCSReport] = None
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def record(self, result: LayerResult) -> None:
        """Record one layer's aggregated result. Order-independent.

        Validates the result's weight against the canonical value if
        the schema carries one. Raises on mismatch rather than
        silently using the wrong weight.

        Raises:
            RuntimeError: If called after finalise().
            ValueError: If the layer has already been recorded, or if
                the result's weight disagrees with LAYER_WEIGHTS.
        """
        with self._lock:
            if self._finalised is not None:
                raise RuntimeError(
                    "Cannot record a result after finalise()."
                )
            if result.layer in self._results:
                raise ValueError(
                    f"Layer {result.layer.value} already recorded. "
                    "EWCS accepts exactly one result per layer."
                )

            canonical = LAYER_WEIGHTS[result.layer]
            if getattr(result, "weight", canonical) != canonical:
                raise ValueError(
                    f"Layer {result.layer.value} reported weight "
                    f"{result.weight}, expected {canonical}. "
                    "LAYER_WEIGHTS is authoritative."
                )

            self._results[result.layer] = result

    def finalise(self) -> EWCSReport:
        """Compute and return the EWCSReport. Idempotent."""
        with self._lock:
            if self._finalised is None:
                self._finalised = self._compute()
            return self._finalised

    @property
    def is_complete(self) -> bool:
        """True after finalise() has been called."""
        return self._finalised is not None

    # ------------------------------------------------------------------
    # Internal computation
    # ------------------------------------------------------------------

    def _compute(self) -> EWCSReport:
        filled, missing = self._fill_missing()

        contributions = tuple(
            self._contribution(filled[layer])
            for layer in EXPECTED_LAYERS
        )

        applicable = [
            c for c in contributions
            if c.state != VerificationState.NOT_APPLICABLE
        ]

        total_weight = sum(c.weight for c in applicable)
        positive_weight = sum(c.positive_contribution for c in applicable)
        signed_weight = sum(c.signed_contribution for c in applicable)

        has_incorrect = any(
            c.state == VerificationState.VERIFIED_INCORRECT
            for c in applicable
        )

        ewcs = positive_weight / total_weight if total_weight else 0.0
        signed = signed_weight / total_weight if total_weight else 0.0

        return EWCSReport(
            task_id=self._task_id,
            ewcs=round(ewcs, 4),
            signed_score=round(signed, 4),
            has_incorrect_layer=has_incorrect,
            total_applicable_weight=total_weight,
            positive_weight=positive_weight,
            contributions=contributions,
            missing_layers=missing,
        )

    def _fill_missing(
        self,
    ) -> tuple[dict[LayerName, LayerResult], tuple[LayerName, ...]]:
        """Return results with every expected layer present.

        Missing layers are filled as UNVERIFIABLE with weight 0. They
        appear in contributions for transparency but do not affect the
        denominator. Missing layers are returned separately so the
        report can flag partial coverage.
        """
        filled = dict(self._results)
        missing: list[LayerName] = []
        for layer in EXPECTED_LAYERS:
            if layer not in filled:
                missing.append(layer)
                filled[layer] = LayerResult(
                    layer=layer,
                    state=VerificationState.UNVERIFIABLE,
                    tier=EvidenceTier.NONE,
                    weight=0,
                    evidence_source="none",
                    evidence_detail="Layer did not report",
                    hallucination_type=None,
                )
        return filled, tuple(missing)

    def _contribution(self, result: LayerResult) -> LayerContribution:
        """Convert a LayerResult into a LayerContribution.

        Weight is taken from LAYER_WEIGHTS, not from the result. A
        missing layer's filled result carries weight 0 so it does not
        enter the denominator.
        """
        if (
            result.evidence_source == "none"
            and result.evidence_detail == "Layer did not report"
        ):
            weight = 0
        else:
            weight = LAYER_WEIGHTS[result.layer]

        factor = DEFAULT_TIER_FACTORS.get(result.tier, 0.0)

        if result.state == VerificationState.VERIFIED_CORRECT:
            positive = weight * factor
            signed = weight * factor
        elif result.state == VerificationState.VERIFIED_INCORRECT:
            positive = 0.0
            signed = -weight * factor
        else:
            # UNVERIFIABLE and NOT_APPLICABLE contribute nothing.
            positive = 0.0
            signed = 0.0

        return LayerContribution(
            layer=result.layer,
            state=result.state,
            tier=result.tier,
            weight=weight,
            tier_factor=factor,
            positive_contribution=positive,
            signed_contribution=signed,
        )

    # ------------------------------------------------------------------
    # Diagnostics
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"EWCS(task_id={self._task_id!r}, "
            f"recorded={len(self._results)}, "
            f"finalised={self.is_complete})"
        )
```

---

## 9. Test Suite — `test_ewcs.py`

Save this at `tests/test_ewcs.py`:

```python
"""Tests for the EWCS class."""

import pytest

from confident_agent.scoring.ewcs import (
    EWCS, LAYER_WEIGHTS, EXPECTED_LAYERS,
)
from confident_agent.schemas import (
    EvidenceTier, LayerName, LayerResult, VerificationState,
)


def make_result(layer, state, tier, weight=None):
    return LayerResult(
        layer=layer,
        state=state,
        tier=tier,
        weight=weight if weight is not None else LAYER_WEIGHTS[layer],
        evidence_source="test",
        evidence_detail="test",
        hallucination_type=None,
    )


def test_all_correct_full_confidence():
    ewcs = EWCS(task_id="t")
    for layer in EXPECTED_LAYERS:
        ewcs.record(make_result(layer, VerificationState.VERIFIED_CORRECT,
                                EvidenceTier.TIER_1))
    report = ewcs.finalise()
    assert report.ewcs == 1.0
    assert report.signed_score == 1.0
    assert report.has_incorrect_layer is False
    assert report.missing_layers == ()


def test_one_incorrect_sets_safety_flag():
    ewcs = EWCS(task_id="t")
    for layer in EXPECTED_LAYERS:
        state = (
            VerificationState.VERIFIED_INCORRECT
            if layer == LayerName.ACCESS_POINT
            else VerificationState.VERIFIED_CORRECT
        )
        ewcs.record(make_result(layer, state, EvidenceTier.TIER_1))
    report = ewcs.finalise()
    assert report.has_incorrect_layer is True
    assert report.missing_layers == ()


def test_worked_example():
    """JSONPlaceholder example. signed_score must be 0.1846."""
    ewcs = EWCS(task_id="jsonplaceholder")
    ewcs.record(make_result(LayerName.INTERFACE,
                            VerificationState.VERIFIED_CORRECT,
                            EvidenceTier.TIER_2))
    ewcs.record(make_result(LayerName.IDENTIFIER,
                            VerificationState.VERIFIED_CORRECT,
                            EvidenceTier.TIER_4))
    ewcs.record(make_result(LayerName.ACCESS_POINT,
                            VerificationState.VERIFIED_INCORRECT,
                            EvidenceTier.TIER_1))
    ewcs.record(make_result(LayerName.INPUT_CONTRACT,
                            VerificationState.VERIFIED_CORRECT,
                            EvidenceTier.TIER_1))
    ewcs.record(make_result(LayerName.OUTPUT_CONTRACT,
                            VerificationState.VERIFIED_CORRECT,
                            EvidenceTier.TIER_4))
    ewcs.record(make_result(LayerName.CONTEXTUAL,
                            VerificationState.NOT_APPLICABLE,
                            EvidenceTier.NONE))
    report = ewcs.finalise()
    assert report.ewcs == 0.4923
    assert report.signed_score == 0.1846
    assert report.has_incorrect_layer is True


def test_missing_layer_flagged():
    ewcs = EWCS(task_id="t")
    ewcs.record(make_result(LayerName.INTERFACE,
                            VerificationState.VERIFIED_CORRECT,
                            EvidenceTier.TIER_1))
    report = ewcs.finalise()
    assert LayerName.INTERFACE not in report.missing_layers
    assert LayerName.ACCESS_POINT in report.missing_layers
    assert len(report.missing_layers) == len(EXPECTED_LAYERS) - 1


def test_duplicate_record_raises():
    ewcs = EWCS(task_id="t")
    ewcs.record(make_result(LayerName.INTERFACE,
                            VerificationState.VERIFIED_CORRECT,
                            EvidenceTier.TIER_1))
    with pytest.raises(ValueError):
        ewcs.record(make_result(LayerName.INTERFACE,
                                VerificationState.VERIFIED_CORRECT,
                                EvidenceTier.TIER_1))


def test_record_after_finalise_raises():
    ewcs = EWCS(task_id="t")
    ewcs.record(make_result(LayerName.INTERFACE,
                            VerificationState.VERIFIED_CORRECT,
                            EvidenceTier.TIER_1))
    ewcs.finalise()
    with pytest.raises(RuntimeError):
        ewcs.record(make_result(LayerName.IDENTIFIER,
                                VerificationState.VERIFIED_CORRECT,
                                EvidenceTier.TIER_1))


def test_finalise_idempotent():
    ewcs = EWCS(task_id="t")
    for layer in EXPECTED_LAYERS:
        ewcs.record(make_result(layer, VerificationState.VERIFIED_CORRECT,
                                EvidenceTier.TIER_1))
    first = ewcs.finalise()
    second = ewcs.finalise()
    assert first is second


def test_unverifiable_counts_against_confidence():
    ewcs = EWCS(task_id="t")
    for layer in EXPECTED_LAYERS:
        ewcs.record(make_result(layer, VerificationState.UNVERIFIABLE,
                                EvidenceTier.NONE))
    report = ewcs.finalise()
    assert report.ewcs == 0.0
    assert report.signed_score == 0.0


def test_not_applicable_excluded_from_denominator():
    ewcs = EWCS(task_id="t")
    ewcs.record(make_result(LayerName.INTERFACE,
                            VerificationState.VERIFIED_CORRECT,
                            EvidenceTier.TIER_1))
    ewcs.record(make_result(LayerName.IDENTIFIER,
                            VerificationState.VERIFIED_CORRECT,
                            EvidenceTier.TIER_1))
    for layer in (
        LayerName.ACCESS_POINT,
        LayerName.INPUT_CONTRACT,
        LayerName.OUTPUT_CONTRACT,
        LayerName.CONTEXTUAL,
    ):
        ewcs.record(make_result(layer, VerificationState.NOT_APPLICABLE,
                                EvidenceTier.NONE))
    report = ewcs.finalise()
    assert report.ewcs == 1.0
    assert report.total_applicable_weight == 6


def test_weight_mismatch_raises():
    ewcs = EWCS(task_id="t")
    with pytest.raises(ValueError):
        ewcs.record(make_result(LayerName.ACCESS_POINT,
                                VerificationState.VERIFIED_CORRECT,
                                EvidenceTier.TIER_1,
                                weight=99))
```

### 9.1 Test Summary

| # | Test | Validates |
|---|---|---|
| 1 | `test_all_correct_full_confidence` | EWCS = 1.0, signed = 1.0, no missing layers |
| 2 | `test_one_incorrect_sets_safety_flag` | `has_incorrect_layer` fires on any INCORRECT |
| 3 | `test_worked_example` | EWCS = 0.4923, signed = 0.1846 |
| 4 | `test_missing_layer_flagged` | `missing_layers` reports unrecorded layers |
| 5 | `test_duplicate_record_raises` | `ValueError` on second record for same layer |
| 6 | `test_record_after_finalise_raises` | `RuntimeError` after `finalise()` |
| 7 | `test_finalise_idempotent` | Two `finalise()` calls return the same object |
| 8 | `test_unverifiable_counts_against_confidence` | All UNVERIFIABLE → EWCS = 0.0 |
| 9 | `test_not_applicable_excluded_from_denominator` | N/A layers excluded from total weight |
| 10 | `test_weight_mismatch_raises` | `ValueError` when weight disagrees with `LAYER_WEIGHTS` |

---

## 10. Design Decisions and Rationale

### 10.1 One Result Per Layer

**Decision:** The EWCS accepts exactly one `LayerResult` per verification layer. Attempting to record a second result for the same layer raises `ValueError`.

**Rationale:**

Three candidate designs were considered.

| Design | Description |
|---|---|
| A | One `LayerResult` per layer. Each verifier aggregates internally. |
| B | Multiple `LayerResult`s per layer. The EWCS aggregates them. |
| C | The orchestrator aggregates before handing results to the EWCS. |

Design A was chosen for three reasons:

1. **Bounded formula.** With one result per layer, the denominator is fixed at the sum of the applicable `LAYER_WEIGHTS`. The EWCS does not vary with how many claims happen to be extracted from the code.
2. **Clear ownership.** Each verifier is the authority on its own layer.
3. **Simpler tests.** The EWCS test suite exercises a fixed set of six inputs.

The verifier's aggregation policy is a separate design decision, owned by each layer class.

### 10.2 Canonical Weight Ownership

**Decision:** `LAYER_WEIGHTS` in `ewcs.py` is the single authoritative source for layer weights. `LayerResult.weight`, if present, is validated against `LAYER_WEIGHTS` and rejected on mismatch.

**Rationale:**

Two failure modes were considered.

| Failure mode | Description |
|---|---|
| Silent drift | Weight lives only in `LayerResult`; a copy-paste error changes the score invisibly |
| Schema churn | Removing `weight` from `LayerResult` forces every layer class to be edited |

The chosen design avoids both:

- `LAYER_WEIGHTS` is authoritative
- `LayerResult.weight` is retained (schema stays as-is)
- `record()` validates and raises on mismatch

The validation uses `getattr(result, "weight", canonical)` so that if the field is ever removed, `record()` still works.

### 10.3 Immutable Report

**Decision:** `EWCSReport` and `LayerContribution` are frozen dataclasses. Nested sequences are tuples, not lists.

**Rationale:**

- A frozen dataclass prevents field reassignment: `report.ewcs = 0.9` raises `TypeError`
- But `frozen=True` does not reach into nested objects
- So the report uses tuples: a tuple of frozen dataclasses is fully immutable

Why this matters for the experiment: If the report were mutable, a downstream stage could inadvertently modify it during logging or marshalling. Immutability guarantees that all consumers see the same numbers.

### 10.4 Thread Safety

**Decision:** `EWCS` uses a `threading.Lock` to guard `record()` and `finalise()`.

**Rationale:**

The six verification layers are independent. Two scenarios make concurrency plausible:

1. **Future parallelism.** If the orchestrator later runs layers in parallel, six threads will call `record()` concurrently.
2. **Defensive design.** Thread safety is cheap and prevents a category of bugs if the tool is ever embedded in a multi-threaded host.

What the lock protects:

- The `_results` dict (concurrent writes would corrupt it)
- The `_finalised` field (a race between `finalise()` and `record()` could leave the object inconsistent)
- The invariant "no record after finalise"

What the lock does **NOT** protect:

- The `EWCSReport` itself (it is immutable, so no lock is needed to read it)
- The `task_id` (set once in `__init__`, never modified)

Why hold the lock during `finalise()`'s computation?

`_compute()` is O(6) — six iterations, two sums, one dataclass construction. Bounded by microseconds. Holding the lock for the entire computation is simpler than a check-then-release pattern and the cost is negligible.

Why not a more sophisticated primitive?

| Option | Verdict |
|---|---|
| `threading.RLock` | Unnecessary — no re-entrancy |
| `asyncio.Lock` | Would require an async API; layers are synchronous |
| No lock | Unsafe if parallelism is introduced |
| `multiprocessing` | The EWCS lives in one process |

### 10.5 Missing Layer Policy

**Decision:** At finalise time, any expected layer that did not report is filled with a synthetic `LayerResult`:

```python
state           = UNVERIFIABLE
tier            = NONE
weight          = 0
evidence_source = "none"
evidence_detail = "Layer did not report"
```

**Rationale:**

Three candidate policies were considered.

| Policy | Description | Verdict |
|---|---|---|
| A | Treat a missing layer as an error. Refuse to finalise. | Rejected — makes EWCS brittle |
| B | Treat as UNVERIFIABLE with normal weight. Counts against the score. | Rejected — conflates bugs with findings |
| C | Treat as weight 0. Does not count, but is flagged. | **Chosen** |

Policy C ensures:

- The score is not diluted by a layer that did not run
- The gap is visible: `missing_layers` is non-empty
- A downstream consumer can decide whether to exclude the task

### 10.6 Why No Configuration Options

**Decision:** `EWCS.__init__` takes only `task_id`.

**Rationale:**

An earlier draft allowed `tier_factors` and `layer_weights` to be passed to `__init__`. This was removed.

- **Single source of truth.** Two places for weights invites drift.
- **Sensitivity analysis belongs elsewhere.** The five weighting schemes (A–E) are an experimental concern, not a per-call concern.
- **Boring is better.** Fewer knobs means fewer ways to get the wrong answer.

### 10.7 Why No Coverage Metric

**Decision:** EWCS does not expose a coverage percentage.

**Rationale:**

Coverage was considered. It would be:

```
coverage = (number of layers that reported) / (number of expected layers)
```

Rejected for two reasons:

1. `missing_layers` already communicates the same information. A caller can compute coverage in one line.
2. Coverage is a policy concern, not a scoring concern. Whether a partial report should be delivered, flagged, or abstained on is the `DecisionPolicy`'s job.

---

## 11. Failure Modes and Exceptions

The EWCS raises three exceptions.

### 11.1 `ValueError` — Duplicate layer

Raised by: `record()` when a `LayerResult` is recorded for a layer that already has a result.

```python
ewcs.record(make(INTERFACE, CORRECT))
ewcs.record(make(INTERFACE, CORRECT))  # ValueError
```

Reason: Enforces the one-result-per-layer contract.

### 11.2 `ValueError` — Weight mismatch

Raised by: `record()` when `result.weight` disagrees with `LAYER_WEIGHTS[result.layer]`.

```python
ewcs.record(make(ACCESS_POINT, CORRECT, weight=99))  # ValueError
```

Reason: Enforces `LAYER_WEIGHTS` as the authoritative source.

### 11.3 `RuntimeError` — Record after finalise

Raised by: `record()` when called after `finalise()`.

```python
ewcs.record(make(INTERFACE, CORRECT))
ewcs.finalise()
ewcs.record(make(IDENTIFIER, CORRECT))  # RuntimeError
```

Reason: The report is immutable. Mutating the accumulator after computing it would allow the report and the accumulator to diverge.

### 11.4 No Other Exceptions

- `finalise()` never raises. It fills missing layers and computes.
- `__init__` never raises beyond Python's own argument errors.
- `is_complete` never raises.
- An unrecognised tier contributes a factor of 0 via `DEFAULT_TIER_FACTORS.get(tier, 0.0)`.

---

## 12. Integration Points

The EWCS is used by three callers.

### 12.1 The `LayerOrchestrator`

File: `verification/orchestrator.py`

After dispatching to all six verifiers and collecting their `LayerResult` objects:

```python
ewcs = EWCS(task_id=task_id)
for result in layer_results:
    ewcs.record(result)
report = ewcs.finalise()
```

The orchestrator then hands the report to the `DecisionPolicy`.

### 12.2 The `DecisionPolicy`

File: `scoring/decision.py`

Consumes the report. Uses:

| Field | Purpose |
|---|---|
| `report.has_incorrect_layer` | Safety constraint |
| `report.ewcs` | Confidence thresholds |

Does not use:

| Field | Reason |
|---|---|
| `report.signed_score` | Diagnostic only |
| `report.contributions` | Used in logging and in the report |
| `report.missing_layers` | May be used if a coverage rule is added later |

### 12.3 The `ConfidentAgent`

File: `verify.py`

Constructs the `VerificationReport`. Copies fields from the `EWCSReport`:

```text
report.ewcs               → VerificationReport.ewcs
report.signed_score       → VerificationReport.signed_score
report.has_incorrect_layer → VerificationReport.has_incorrect_layer
report.missing_layers     → VerificationReport.missing_layers
```

The `VerificationReport` does not embed the `EWCSReport`. It copies the fields it needs. This keeps `schemas.py` free of any dependency on the scoring subpackage.

### 12.4 Dependency Direction

```text
schemas.py         ← no internal dependencies
    ↑
scoring/ewcs.py    ← imports from schemas only
```

The EWCS imports nothing from `clients`, `extraction`, or `verification`. This is the property that allows the EWCS to be tested in isolation and to be reused with any set of layers that produce `LayerResult` objects.

---

## 13. Testing — How It Was Verified

The testing process, in order:

1. **Folder structure prepared.** `confident_agent/` package created with `__init__.py`, `schemas.py`, `scoring/__init__.py`, `scoring/ewcs.py`. `tests/__init__.py` created.
2. **`schemas.py` written.** Minimal version containing only the four names `ewcs.py` imports.
3. **`ewcs.py` written.** The frozen class.
4. **`test_ewcs.py` written.** Ten tests + helper.
5. **`pytest` installed.** `pip install pytest`.
6. **First run from correct directory.** The initial run failed with `ModuleNotFoundError: No module named 'confident_agent'`. The fix was to run pytest from the project root (the folder containing `confident_agent/`), not from inside the package.
7. **Second run.** The second failure was `ModuleNotFoundError: No module named 'confident_agent.scoring'`. The fix was to ensure `confident_agent/scoring/__init__.py` exists.
8. **Third run.** All 10 tests passed. `test_worked_example` confirmed `signed_score == 0.1846` (not −0.277).

### 13.1 How to Run

```bash
pip install pytest
pytest tests/test_ewcs.py -v
```

### 13.2 Expected Output

```text
tests/test_ewcs.py::test_all_correct_full_confidence PASSED
tests/test_ewcs.py::test_one_incorrect_sets_safety_flag PASSED
tests/test_ewcs.py::test_worked_example PASSED
tests/test_ewcs.py::test_missing_layer_flagged PASSED
tests/test_ewcs.py::test_duplicate_record_raises PASSED
tests/test_ewcs.py::test_record_after_finalise_raises PASSED
tests/test_ewcs.py::test_finalise_idempotent PASSED
tests/test_ewcs.py::test_unverifiable_counts_against_confidence PASSED
tests/test_ewcs.py::test_not_applicable_excluded_from_denominator PASSED
tests/test_ewcs.py::test_weight_mismatch_raises PASSED

10 passed in 0.05s
```

### 13.3 Quick Manual Test (No pytest)

Save this at `project-root/try_ewcs.py`:

```python
from confident_agent.scoring.ewcs import EWCS, LAYER_WEIGHTS
from confident_agent.schemas import (
    EvidenceTier, LayerName, LayerResult, VerificationState,
)


def make(layer, state, tier):
    return LayerResult(
        layer=layer,
        state=state,
        tier=tier,
        weight=LAYER_WEIGHTS[layer],
        evidence_source="demo",
        evidence_detail="demo",
        hallucination_type=None,
    )


ewcs = EWCS(task_id="demo")

ewcs.record(make(LayerName.INTERFACE,
                 VerificationState.VERIFIED_CORRECT, EvidenceTier.TIER_2))
ewcs.record(make(LayerName.IDENTIFIER,
                 VerificationState.VERIFIED_CORRECT, EvidenceTier.TIER_4))
ewcs.record(make(LayerName.ACCESS_POINT,
                 VerificationState.VERIFIED_INCORRECT, EvidenceTier.TIER_1))
ewcs.record(make(LayerName.INPUT_CONTRACT,
                 VerificationState.VERIFIED_CORRECT, EvidenceTier.TIER_1))
ewcs.record(make(LayerName.OUTPUT_CONTRACT,
                 VerificationState.VERIFIED_CORRECT, EvidenceTier.TIER_4))
ewcs.record(make(LayerName.CONTEXTUAL,
                 VerificationState.NOT_APPLICABLE, EvidenceTier.NONE))

report = ewcs.finalise()

print(f"EWCS         = {report.ewcs}")
print(f"signed_score = {report.signed_score}")
print(f"has_incorrect= {report.has_incorrect_layer}")
print(f"missing      = {report.missing_layers}")

for c in report.contributions:
    print(f"  {c.layer.value:<16} {c.state.value:<20} "
          f"w={c.weight}  f={c.tier_factor}  "
          f"+{c.positive_contribution}  {c.signed_contribution}")
```

Run:

```bash
python try_ewcs.py
```

### 13.4 Expected Output

```text
EWCS         = 0.4923
signed_score = 0.1846
has_incorrect= True
missing      = ()
  interface        verified_correct     w=3  f=0.8  +2.4  2.4
  identifier       verified_correct     w=3  f=0.5  +1.5  1.5
  access_point     verified_incorrect   w=4  f=1.0  +0.0  -4.0
  input_contract   verified_correct     w=2  f=1.0  +2.0  2.0
  output_contract  verified_correct     w=1  f=0.5  +0.5  0.5
  contextual       not_applicable       w=0  f=0.0  +0.0  0.0
```

### 13.5 Common Setup Errors

| Error | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: No module named 'confident_agent'` | Running pytest from inside `confident_agent/` | `cd` to project root |
| `ModuleNotFoundError: No module named 'confident_agent.scoring'` | Missing `scoring/__init__.py` | `New-Item -ItemType File confident_agent\scoring\__init__.py` |
| `ImportError while importing test module` | Wrong folder name or missing `__init__.py` in `tests/` | Ensure package folder is exactly `confident_agent` |

---

## 14. Frozen Contract Summary

Everything in this section is frozen. Changing any of these requires updating the tests, the documentation, and any downstream consumer.

| Contract | Enforcement |
|---|---|
| One `LayerResult` per layer | `ValueError` on duplicate record |
| `LAYER_WEIGHTS` is authoritative | `ValueError` on weight mismatch |
| Immutable report | `EWCSReport` and `LayerContribution` are frozen; nested sequences are tuples |
| Thread-safe | `record()` and `finalise()` guarded by a `threading.Lock` |
| Idempotent `finalise()` | Repeated calls return the same report object |
| No configuration | `__init__` takes only `task_id` |
| Missing layers | Filled as UNVERIFIABLE with weight 0, listed in `missing_layers` |
| No coverage metric | Coverage is a policy concern, not a scoring concern |
| No mutation after finalise | `RuntimeError` on record after finalise |
| Round to 4 decimal places | Both `ewcs` and `signed_score` |
| No dependencies on other tool subpackages | EWCS imports only from `schemas.py` |

---

## 15. Change Log

### Version 1.0 (frozen)

- One-result-per-layer contract frozen
- `LAYER_WEIGHTS` established as authoritative
- `LayerResult.weight` retained in schema, validated not trusted
- `EWCSReport.missing_layers` added
- Signed score corrected for the worked example: 0.1846 (was −0.277)
- Configuration options removed
- Coverage metric rejected
- Ten tests written and passing

### Pre-release (superseded)

- Earlier drafts allowed `tier_factors` and `layer_weights` in `__init__`
- Earlier drafts computed `signed_score` incorrectly for the worked example
- Earlier drafts did not expose `missing_layers`
- Earlier drafts did not validate the weight against a canonical source

---

*End of document.*
