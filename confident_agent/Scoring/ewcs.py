"""Evidence-Weighted Confidence Score (EWCS).

The EWCS aggregates one LayerResult per verification layer into an
immutable EWCSReport. It is the primary confidence metric for the
Confident Agent.

Formula:
                      Σ (w_l × tier_factor_l)
    EWCS = ─────────────────────────────────────────
                      Σ (w_l)

    Numerator:   over layers where state = VERIFIED_CORRECT
    Denominator: over all applicable layers (state ≠ NOT_APPLICABLE)

Signed score:
                      Σ (w_l × s_l)
    signed = ─────────────────────────────
                      Σ (w_l)

    where s_l ∈ {+tier_factor, −tier_factor, 0.0} for
    CORRECT, INCORRECT, UNVERIFIABLE respectively.

Design:
    - Accumulate-then-finalise. No partial scores.
    - One result per layer. Duplicate layer records raise ValueError.
    - Missing layers are filled as UNVERIFIABLE with weight 0 at finalise,
      so they do not affect the denominator.
    - Thread-safe: record() and finalise() are guarded by a lock.
    - Idempotent finalise(): repeated calls return the same report.
    - Completeness is enforced by types: DecisionPolicy requires an
      EWCSReport, and only finalise() can produce one.
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


DEFAULT_TIER_FACTORS: dict[EvidenceTier, float] = {
    EvidenceTier.TIER_1: 1.00,
    EvidenceTier.TIER_2: 0.80,
    EvidenceTier.TIER_3: 0.90,
    EvidenceTier.TIER_4: 0.50,
    EvidenceTier.NONE: 0.00,
}


EXPECTED_LAYERS: tuple[LayerName, ...] = (
    LayerName.INTERFACE,
    LayerName.IDENTIFIER,
    LayerName.ACCESS_POINT,
    LayerName.INPUT_CONTRACT,
    LayerName.OUTPUT_CONTRACT,
    LayerName.CONTEXTUAL,
)


@dataclass(frozen=True)
class LayerContribution:
    """One layer's contribution to the EWCS.

    Attributes:
        layer: The verification layer.
        state: The layer's verification state.
        tier: The evidence tier supporting the state.
        weight: The layer's declared weight.
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
    """

    task_id: str
    ewcs: float
    signed_score: float
    has_incorrect_layer: bool
    total_applicable_weight: int
    positive_weight: float
    contributions: tuple[LayerContribution, ...]


class EWCS:
    """Accumulates LayerResult objects and computes the EWCS.

    Usage:
        ewcs = EWCS(task_id="t-001")
        for result in layer_results:
            ewcs.record(result)
        report = ewcs.finalise()
    """

    def __init__(
        self,
        task_id: str,
        tier_factors: Optional[dict[EvidenceTier, float]] = None,
    ) -> None:
        self._task_id = task_id
        self._tier_factors = dict(tier_factors or DEFAULT_TIER_FACTORS)
        self._results: dict[LayerName, LayerResult] = {}
        self._finalised: Optional[EWCSReport] = None
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def record(self, result: LayerResult) -> None:
        """Record one layer's result. Order-independent.

        Raises:
            RuntimeError: If called after finalise().
            ValueError: If the layer has already been recorded.
        """
        with self._lock:
            if self._finalised is not None:
                raise RuntimeError(
                    "Cannot record a result after finalise()."
                )
            if result.layer in self._results:
                raise ValueError(
                    f"Layer {result.layer.value} already recorded. "
                    "EWCS accepts one result per layer."
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
        results = self._fill_missing()

        contributions = tuple(
            self._contribution(results[layer])
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
        )

    def _fill_missing(self) -> dict[LayerName, LayerResult]:
        """Return results with every expected layer present.

        Missing layers are filled as UNVERIFIABLE with weight 0, so they
        are flagged in the report but do not affect the denominator.
        """
        filled = dict(self._results)
        for layer in EXPECTED_LAYERS:
            if layer not in filled:
                filled[layer] = LayerResult(
                    layer=layer,
                    state=VerificationState.UNVERIFIABLE,
                    tier=EvidenceTier.NONE,
                    weight=0,
                    evidence_source="none",
                    evidence_detail="Layer did not report",
                    hallucination_type=None,
                )
        return filled

    def _contribution(self, result: LayerResult) -> LayerContribution:
        """Convert a LayerResult into a LayerContribution."""
        factor = self._tier_factors.get(result.tier, 0.0)

        if result.state == VerificationState.VERIFIED_CORRECT:
            positive = result.weight * factor
            signed = result.weight * factor
        elif result.state == VerificationState.VERIFIED_INCORRECT:
            positive = 0.0
            signed = -result.weight * factor
        else:
            # UNVERIFIABLE and NOT_APPLICABLE contribute nothing.
            positive = 0.0
            signed = 0.0

        return LayerContribution(
            layer=result.layer,
            state=result.state,
            tier=result.tier,
            weight=result.weight,
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