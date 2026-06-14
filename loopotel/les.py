"""Point-in-loop LES proxies (v0.1 — effectiveness-focused)."""

from __future__ import annotations

DEFAULT_GOAL_TARGET = 0.8


def effectiveness(goal_score: float, goal_target: float = DEFAULT_GOAL_TARGET) -> float:
    if goal_target <= 0:
        return 0.0
    return max(0.0, min(1.0, goal_score / goal_target))


def cumulative_les(scores: list[float], goal_target: float = DEFAULT_GOAL_TARGET) -> float:
    if not scores:
        return 0.0
    values = [effectiveness(s, goal_target) for s in scores]
    return round(sum(values) / len(values), 4)
