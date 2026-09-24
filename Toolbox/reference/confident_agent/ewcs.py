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