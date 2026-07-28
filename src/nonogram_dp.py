"""Dynamic-programming nonogram solver for large run-length puzzles."""
from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from functools import lru_cache
from numbers import Integral

from .encoding import parse_clue

UNKNOWN = -1
Line = tuple[int, ...]
Matrix = tuple[Line, ...]
State = tuple[str, int, int]


@dataclass(frozen=True, slots=True)
class NonogramSolveResult:
    """Complete or bounded result of a nonogram search."""

    solutions: tuple[Matrix, ...]
    exhausted: bool
    visited_nodes: int
    propagation_rounds: int

    @property
    def solution_count(self) -> int:
        return len(self.solutions)


def _normalize_clue(clue: Sequence[int], length: int) -> tuple[int, ...]:
    normalized = parse_clue(clue)
    if normalized != (0,) and sum(normalized) + len(normalized) - 1 > length:
        raise ValueError(f"clue cannot fit length {length}: {normalized}")
    return normalized


@lru_cache(maxsize=None)
def _automaton(clue: tuple[int, ...]) -> tuple[
    tuple[State, ...], dict[State, dict[int, State]], State, frozenset[State]
]:
    runs = () if clue == (0,) else clue
    states: list[State] = [("gap", index, 0) for index in range(len(runs) + 1)]
    for run_index, run_length in enumerate(runs):
        states.extend(("run", run_index, used) for used in range(1, run_length + 1))

    transitions: dict[State, dict[int, State]] = {}
    for state in states:
        kind, run_index, used = state
        outgoing: dict[int, State] = {}
        if kind == "gap":
            outgoing[0] = state
            if run_index < len(runs):
                outgoing[1] = ("run", run_index, 1)
        elif used < runs[run_index]:
            outgoing[1] = ("run", run_index, used + 1)
        elif run_index == len(runs) - 1:
            outgoing[0] = ("gap", len(runs), 0)
        else:
            outgoing[0] = ("gap", run_index + 1, 0)
        transitions[state] = outgoing

    start = ("gap", 0, 0)
    accepts = {("gap", len(runs), 0)}
    if runs:
        accepts.add(("run", len(runs) - 1, runs[-1]))
    return tuple(states), transitions, start, frozenset(accepts)


@lru_cache(maxsize=200_000)
def line_options(
    clue: tuple[int, ...], known: tuple[int, ...]
) -> tuple[frozenset[int], ...] | None:
    """Return feasible values at each cell, or ``None`` if the line is impossible."""
    normalized = _normalize_clue(clue, len(known))
    if any(value not in (UNKNOWN, 0, 1) for value in known):
        raise ValueError("known cells must be -1, 0, or 1")

    states, transitions, start, accepts = _automaton(normalized)
    forward = [set() for _ in range(len(known) + 1)]
    forward[0].add(start)
    for index, value in enumerate(known):
        bits = (0, 1) if value == UNKNOWN else (value,)
        for state in forward[index]:
            for bit in bits:
                target = transitions[state].get(bit)
                if target is not None:
                    forward[index + 1].add(target)
        if not forward[index + 1]:
            return None
    if not forward[-1].intersection(accepts):
        return None

    backward = [set() for _ in range(len(known) + 1)]
    backward[-1] = set(accepts)
    for index in range(len(known) - 1, -1, -1):
        bits = (0, 1) if known[index] == UNKNOWN else (known[index],)
        for state in states:
            if any(
                transitions[state].get(bit) in backward[index + 1] for bit in bits
            ):
                backward[index].add(state)

    result: list[frozenset[int]] = []
    for index, value in enumerate(known):
        bits = (0, 1) if value == UNKNOWN else (value,)
        possible = frozenset(
            bit
            for bit in bits
            if any(
                transitions[state].get(bit) in backward[index + 1]
                for state in forward[index]
            )
        )
        if not possible:
            return None
        result.append(possible)
    return tuple(result)


def solve_nonogram(
    row_clues: Sequence[Sequence[int]],
    col_clues: Sequence[Sequence[int]],
    max_solutions: int | None = None,
) -> NonogramSolveResult:
    """Solve a square nonogram by line DP, propagation, and cell branching."""
    if not row_clues or len(row_clues) != len(col_clues):
        raise ValueError("clues must define a non-empty square")
    if max_solutions is not None and (
        isinstance(max_solutions, bool)
        or not isinstance(max_solutions, Integral)
        or max_solutions <= 0
    ):
        raise ValueError("max_solutions must be positive or None")

    size = len(row_clues)
    rows = tuple(_normalize_clue(clue, size) for clue in row_clues)
    cols = tuple(_normalize_clue(clue, size) for clue in col_clues)
    solutions: list[Matrix] = []
    visited_nodes = 0
    propagation_rounds = 0

    def propagate(grid: list[list[int]]) -> bool:
        nonlocal propagation_rounds
        changed = True
        while changed:
            propagation_rounds += 1
            changed = False
            for row_index, clue in enumerate(rows):
                options = line_options(clue, tuple(grid[row_index]))
                if options is None:
                    return False
                for col_index, values in enumerate(options):
                    if len(values) == 1 and grid[row_index][col_index] == UNKNOWN:
                        grid[row_index][col_index] = next(iter(values))
                        changed = True
            for col_index, clue in enumerate(cols):
                known = tuple(grid[row_index][col_index] for row_index in range(size))
                options = line_options(clue, known)
                if options is None:
                    return False
                for row_index, values in enumerate(options):
                    if len(values) == 1 and grid[row_index][col_index] == UNKNOWN:
                        grid[row_index][col_index] = next(iter(values))
                        changed = True
        return True

    def search(grid: list[list[int]]) -> bool:
        nonlocal visited_nodes
        if max_solutions is not None and len(solutions) >= max_solutions:
            return False
        visited_nodes += 1
        if not propagate(grid):
            return True

        unknown = [
            (row_index, col_index)
            for row_index in range(size)
            for col_index in range(size)
            if grid[row_index][col_index] == UNKNOWN
        ]
        if not unknown:
            solutions.append(tuple(tuple(row) for row in grid))
            return True

        row_unknown = [sum(value == UNKNOWN for value in row) for row in grid]
        col_unknown = [
            sum(grid[row_index][col_index] == UNKNOWN for row_index in range(size))
            for col_index in range(size)
        ]
        row_index, col_index = min(
            unknown,
            key=lambda cell: row_unknown[cell[0]] + col_unknown[cell[1]],
        )
        for value in (1, 0):
            if max_solutions is not None and len(solutions) >= max_solutions:
                return False
            child = [row[:] for row in grid]
            child[row_index][col_index] = value
            if not search(child):
                return False
        return True

    exhausted = search([[UNKNOWN] * size for _ in range(size)])
    return NonogramSolveResult(
        solutions=tuple(solutions),
        exhausted=exhausted,
        visited_nodes=visited_nodes,
        propagation_rounds=propagation_rounds,
    )
