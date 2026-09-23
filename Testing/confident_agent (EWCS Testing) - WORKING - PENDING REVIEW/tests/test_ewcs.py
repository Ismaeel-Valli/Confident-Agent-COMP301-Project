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