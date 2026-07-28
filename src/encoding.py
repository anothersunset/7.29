"""Utilities for parsing and computing binary run-length clues."""

from __future__ import annotations

from collections.abc import Sequence
from numbers import Integral, Real
from typing import Final

ZERO_CLUE: Final[tuple[int, ...]] = (0,)


def _validate_clue_parts(parts: Sequence[int]) -> tuple[int, ...]:
    """Validate and normalize clue parts.

    ``(0,)`` is the canonical representation of an all-zero line. Every
    non-zero clue must contain only strictly positive run lengths.
    """
    if not parts:
        return ZERO_CLUE

    normalized: list[int] = []
    for part in parts:
        if isinstance(part, bool) or not isinstance(part, Integral):
            raise ValueError(f"clue entries must be integers, got {part!r}")
        normalized.append(int(part))

    clue = tuple(normalized)
    if clue == ZERO_CLUE:
        return ZERO_CLUE
    if any(part <= 0 for part in clue):
        raise ValueError(
            "a non-zero clue must contain only positive run lengths; "
            f"got {clue!r}"
        )
    return clue


def parse_clue(value: object) -> tuple[int, ...]:
    """Parse an Excel-style clue into a canonical tuple.

    Examples:
        ``5 -> (5,)``
        ``"1, 2, 3" -> (1, 2, 3)``
        ``None``, ``""`` and ``0`` -> ``(0,)``
    """
    if value is None:
        return ZERO_CLUE

    if isinstance(value, str):
        text = value.strip()
        if not text:
            return ZERO_CLUE
        raw_parts = text.split(",")
        if any(not part.strip() for part in raw_parts):
            raise ValueError(f"malformed clue string: {value!r}")
        try:
            return _validate_clue_parts(tuple(int(part.strip()) for part in raw_parts))
        except ValueError as exc:
            raise ValueError(f"invalid clue string: {value!r}") from exc

    if isinstance(value, bool):
        raise ValueError("boolean values are not valid clues")

    if isinstance(value, Integral):
        return _validate_clue_parts((int(value),))

    if isinstance(value, Real):
        numeric = float(value)
        if not numeric.is_integer():
            raise ValueError(f"numeric clue must be an integer, got {value!r}")
        return _validate_clue_parts((int(numeric),))

    if isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray)):
        return _validate_clue_parts(value)

    raise ValueError(f"unsupported clue value: {value!r}")


def encode_line(line: Sequence[int]) -> tuple[int, ...]:
    """Return lengths of maximal consecutive-one runs in a binary line."""
    if not line:
        raise ValueError("a binary line must not be empty")

    runs: list[int] = []
    current_run = 0

    for value in line:
        if isinstance(value, bool):
            bit = int(value)
        elif isinstance(value, Integral) and int(value) in (0, 1):
            bit = int(value)
        else:
            raise ValueError(f"binary line entries must be 0 or 1, got {value!r}")

        if bit == 1:
            current_run += 1
        elif current_run:
            runs.append(current_run)
            current_run = 0

    if current_run:
        runs.append(current_run)

    return tuple(runs) if runs else ZERO_CLUE
