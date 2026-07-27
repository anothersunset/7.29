"""Baseline exhaustive solver using row search and column-prefix pruning."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from numbers import Integral

from .encoding import parse_clue
from .patterns import Pattern, generate_patterns

Clue = tuple[int, ...]
Matrix = tuple[Pattern, ...]


@dataclass(frozen=True, slots=True)
class SolveResult:
    """Result of a matrix reconstruction search.

    ``exhausted`` is true only when the complete search space was traversed.
    When a solution limit prevents another branch from being inspected, it is
    false even if all returned matrices are valid.
    """

    solutions: tuple[Matrix, ...]
    exhausted: bool
    visited_nodes: int

    @property
    def solution_count(self) -> int:
        return len(self.solutions)


def _normalize_problem(
    row_clues: Sequence[Sequence[int]],
    col_clues: Sequence[Sequence[int]],
) -> tuple[tuple[Clue, ...], tuple[Clue, ...]]:
    if not row_clues or not col_clues:
        raise ValueError("row and column clues must not be empty")
    if len(row_clues) != len(col_clues):
        raise ValueError(
            "the puzzle must be square: "
            f"got {len(row_clues)} rows and {len(col_clues)} columns"
        )

    rows = tuple(parse_clue(clue) for clue in row_clues)
    cols = tuple(parse_clue(clue) for clue in col_clues)
    return rows, cols


def solve(
    row_clues: Sequence[Sequence[int]],
    col_clues: Sequence[Sequence[int]],
    max_solutions: int | None = None,
) -> SolveResult:
    """Enumerate matrices satisfying all row and column run-length clues.

    The baseline algorithm chooses rows from top to bottom. After adding a row,
    every current column prefix must occur as a prefix of at least one complete
    legal pattern for that column.
    """
    if max_solutions is not None:
        if (
            isinstance(max_solutions, bool)
            or not isinstance(max_solutions, Integral)
            or int(max_solutions) <= 0
        ):
            raise ValueError("max_solutions must be a positive integer or None")
        max_solutions = int(max_solutions)

    rows, cols = _normalize_problem(row_clues, col_clues)
    size = len(rows)

    row_domains = tuple(generate_patterns(size, clue) for clue in rows)
    col_domains = tuple(generate_patterns(size, clue) for clue in cols)

    column_prefixes: tuple[tuple[frozenset[Pattern], ...], ...] = tuple(
        tuple(
            frozenset(pattern[:depth] for pattern in domain)
            for depth in range(size + 1)
        )
        for domain in col_domains
    )

    solutions: list[Matrix] = []
    current_rows: list[Pattern] = []
    current_columns: list[Pattern] = [tuple() for _ in range(size)]
    visited_nodes = 0
    stopped_early = False

    def search(row_index: int) -> None:
        nonlocal visited_nodes, stopped_early
        visited_nodes += 1

        if row_index == size:
            solutions.append(tuple(current_rows))
            return

        for row_pattern in row_domains[row_index]:
            if max_solutions is not None and len(solutions) >= max_solutions:
                stopped_early = True
                return

            next_columns: list[Pattern] = []
            feasible = True
            for col_index, bit in enumerate(row_pattern):
                prefix = current_columns[col_index] + (bit,)
                if prefix not in column_prefixes[col_index][row_index + 1]:
                    feasible = False
                    break
                next_columns.append(prefix)

            if not feasible:
                continue

            previous_columns = current_columns[:]
            current_columns[:] = next_columns
            current_rows.append(row_pattern)
            search(row_index + 1)
            current_rows.pop()
            current_columns[:] = previous_columns

    search(0)

    return SolveResult(
        solutions=tuple(solutions),
        exhausted=not stopped_early,
        visited_nodes=visited_nodes,
    )
