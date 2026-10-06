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