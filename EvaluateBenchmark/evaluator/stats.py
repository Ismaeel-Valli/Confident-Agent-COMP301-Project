"""Statistics for the evaluation (EVALUATION_PLAN.md §6), standard library only."""
from __future__ import annotations

import math
import random
from collections import defaultdict


def mcnemar_exact(b: int, c: int) -> float:
    """Two-sided exact McNemar test: b and c are the discordant pairs."""
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    tail = sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n
    return min(1.0, 2 * tail)


def paired_difference(pairs: list) -> float:
    """pairs: (baseline_event, intervention_event) as 0/1; returns baseline rate - intervention rate."""
    return sum(b - i for b, i in pairs) / len(pairs) if pairs else float("nan")


def bootstrap_ci(pairs: list, clusters: list | None = None, resamples: int = 10000, seed: int = 301) -> tuple:
    """95% percentile interval of the paired difference. With clusters, whole clusters
    (operation families) are resampled, so related tasks are not treated as independent."""
    if not pairs:
        return (float("nan"), float("nan"))
    rng = random.Random(seed)
    if clusters is None:
        groups = [[p] for p in pairs]
    else:
        by = defaultdict(list)
        for p, c in zip(pairs, clusters):
            by[c].append(p)
        groups = list(by.values())
    estimates = []
    for _ in range(resamples):
        sample = [p for _ in groups for p in rng.choice(groups)]
        estimates.append(paired_difference(sample))
    estimates.sort()
    return (estimates[int(0.025 * resamples)], estimates[int(0.975 * resamples) - 1])


def holm(pvalues: dict) -> dict:
    """Holm-adjusted p-values for several runs."""
    order = sorted(pvalues, key=pvalues.get)
    adjusted, running = {}, 0.0
    for rank, key in enumerate(order):
        running = max(running, min(1.0, (len(order) - rank) * pvalues[key]))
        adjusted[key] = running
    return adjusted


def auc(positives: list, negatives: list) -> float | None:
    """Probability that a correct candidate scores higher than a hallucinated one."""
    if not positives or not negatives:
        return None
    wins = sum(1.0 if p > n else 0.5 if p == n else 0.0 for p in positives for n in negatives)
    return wins / (len(positives) * len(negatives))


def cohen_kappa(a: list, b: list) -> float | None:
    if not a or len(a) != len(b):
        return None
    labels = sorted(set(a) | set(b))
    n = len(a)
    observed = sum(x == y for x, y in zip(a, b)) / n
    expected = sum((a.count(l) / n) * (b.count(l) / n) for l in labels)
    return 1.0 if expected == 1 else (observed - expected) / (1 - expected)


def wilson(k: int, n: int) -> tuple:
    if n == 0:
        return (float("nan"), float("nan"))
    p, z = k / n, 1.96
    centre = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return (centre - half, centre + half)
