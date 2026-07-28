"""Generation and counting of valid binary line patterns."""

from __future__ import annotations

from collections.abc import Sequence
from math import comb
from numbers import Integral

from .encoding import ZERO_CLUE, parse_clue

Pattern = tuple[int, ...]


def _validated_inputs(length: int, clue: Sequence[int]) -> tuple[int, tuple[int, ...]]:
    if isinstance(length, bool) or not isinstance(length, Integral) or int(length) <= 0:
        raise ValueError(f"line length must be a positive integer, got {length!r}")

    normalized_length = int(length)
    normalized_clue = parse_clue(clue)

    if normalized_clue != ZERO_CLUE:
        minimum_required = sum(normalized_clue) + len(normalized_clue) - 1
        if minimum_required > normalized_length:
            raise ValueError(
                "clue cannot fit in the requested line length: "
                f"length={normalized_length}, clue={normalized_clue}"
            )

    return normalized_length, normalized_clue


def count_patterns(length: int, clue: Sequence[int]) -> int:
    """Count valid patterns using the stars-and-bars formula."""
    length, normalized_clue = _validated_inputs(length, clue)
    if normalized_clue == ZERO_CLUE:
        return 1

    run_count = len(normalized_clue)
    occupied = sum(normalized_clue)
    return comb(length - occupied + 1, run_count)


def generate_patterns(length: int, clue: Sequence[int]) -> tuple[Pattern, ...]:
    """Generate every binary pattern matching ``clue`` exactly.

    Patterns are emitted deterministically from the leftmost placement to the
    rightmost placement, which keeps tests and experiment outputs reproducible.
    """
    length, normalized_clue = _validated_inputs(length, clue)
    if normalized_clue == ZERO_CLUE:
        return ((0,) * length,)

    results: list[Pattern] = []

    def place(run_index: int, minimum_start: int, current: list[int]) -> None:
        if run_index == len(normalized_clue):
            results.append(tuple(current))
            return

        run_length = normalized_clue[run_index]
        later_runs = normalized_clue[run_index + 1 :]
        minimum_later_space = sum(later_runs) + len(later_runs)
        maximum_start = length - run_length - minimum_later_space

        for start in range(minimum_start, maximum_start + 1):
            candidate = current.copy()
            candidate[start : start + run_length] = [1] * run_length
            place(run_index + 1, start + run_length + 1, candidate)

    place(0, 0, [0] * length)

    expected = count_patterns(length, normalized_clue)
    if len(results) != expected:
        raise RuntimeError(
            "internal candidate generation error: "
            f"expected {expected}, generated {len(results)}"
        )

    return tuple(results)
