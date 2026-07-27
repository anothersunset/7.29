"""Independent validation for reconstructed matrices."""
from __future__ import annotations
from collections.abc import Sequence
from dataclasses import dataclass
from .encoding import encode_line, parse_clue
from .solver import Clue, Matrix

@dataclass(frozen=True, slots=True)
class ValidationReport:
    valid: bool
    calculated_row_clues: tuple[Clue, ...]
    calculated_col_clues: tuple[Clue, ...]
    row_mismatches: tuple[int, ...]
    col_mismatches: tuple[int, ...]

def validate_matrix(matrix: Sequence[Sequence[int]], row_clues: Sequence[Sequence[int]], col_clues: Sequence[Sequence[int]]) -> ValidationReport:
    rows = tuple(parse_clue(c) for c in row_clues); cols = tuple(parse_clue(c) for c in col_clues); n = len(rows)
    if n == 0 or len(cols) != n: raise ValueError("clues must define a non-empty square")
    if len(matrix) != n or any(len(row) != n for row in matrix): raise ValueError(f"matrix must have shape {n}x{n}")
    normalized: Matrix = tuple(tuple(row) for row in matrix)
    actual_rows = tuple(encode_line(row) for row in normalized)
    actual_cols = tuple(encode_line(tuple(normalized[i][j] for i in range(n))) for j in range(n))
    row_bad = tuple(i for i,(a,e) in enumerate(zip(actual_rows,rows,strict=True),1) if a != e)
    col_bad = tuple(j for j,(a,e) in enumerate(zip(actual_cols,cols,strict=True),1) if a != e)
    return ValidationReport(not row_bad and not col_bad, actual_rows, actual_cols, row_bad, col_bad)
