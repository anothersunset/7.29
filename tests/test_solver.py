"""Tests for the baseline exhaustive matrix solver."""

import unittest

from src.encoding import encode_line
from src.solver import Matrix, solve


def assert_solution_valid(
    test_case: unittest.TestCase,
    matrix: Matrix,
    row_clues: tuple[tuple[int, ...], ...],
    col_clues: tuple[tuple[int, ...], ...],
) -> None:
    size = len(row_clues)
    test_case.assertEqual(len(matrix), size)
    test_case.assertTrue(all(len(row) == size for row in matrix))
    test_case.assertEqual(tuple(encode_line(row) for row in matrix), row_clues)
    columns = tuple(
        tuple(matrix[row_index][col_index] for row_index in range(size))
        for col_index in range(size)
    )
    test_case.assertEqual(tuple(encode_line(col) for col in columns), col_clues)


class BaselineSolverTests(unittest.TestCase):
    def test_single_zero_cell(self) -> None:
        result = solve(((0,),), ((0,),))
        self.assertTrue(result.exhausted)
        self.assertEqual(result.solutions, (((0,),),))

    def test_single_one_cell(self) -> None:
        result = solve(((1,),), ((1,),))
        self.assertTrue(result.exhausted)
        self.assertEqual(result.solutions, (((1,),),))

    def test_two_solution_permutation_puzzle(self) -> None:
        clues = ((1,), (1,))
        result = solve(clues, clues)
        expected = {
            ((1, 0), (0, 1)),
            ((0, 1), (1, 0)),
        }
        self.assertTrue(result.exhausted)
        self.assertEqual(result.solution_count, 2)
        self.assertEqual(set(result.solutions), expected)
        for matrix in result.solutions:
            assert_solution_valid(self, matrix, clues, clues)

    def test_solution_limit_marks_search_as_not_exhausted(self) -> None:
        clues = ((1,), (1,))
        result = solve(clues, clues, max_solutions=1)
        self.assertEqual(result.solution_count, 1)
        self.assertFalse(result.exhausted)
        assert_solution_valid(self, result.solutions[0], clues, clues)

    def test_inconsistent_puzzle_has_no_solution(self) -> None:
        result = solve(((2,), (2,)), ((1,), (1,)))
        self.assertTrue(result.exhausted)
        self.assertEqual(result.solution_count, 0)

    def test_five_by_five_statement_example(self) -> None:
        row_clues = ((3,), (2, 1), (4,), (2, 2), (2, 2))
        col_clues = ((1, 2), (5,), (3,), (3,), (4,))
        expected = (
            (1, 1, 1, 0, 0),
            (0, 1, 1, 0, 1),
            (0, 1, 1, 1, 1),
            (1, 1, 0, 1, 1),
            (1, 1, 0, 1, 1),
        )

        result = solve(row_clues, col_clues)

        self.assertTrue(result.exhausted)
        self.assertEqual(result.solution_count, 1)
        self.assertEqual(result.solutions[0], expected)
        assert_solution_valid(self, expected, row_clues, col_clues)

    def test_rejects_invalid_problem_shapes_and_limits(self) -> None:
        invalid_calls = [
            lambda: solve((), ()),
            lambda: solve(((1,),), ((1,), (1,))),
            lambda: solve(((1,),), ((1,),), max_solutions=0),
            lambda: solve(((1,),), ((1,),), max_solutions=True),
            lambda: solve(((2,),), ((1,),)),
        ]
        for call in invalid_calls:
            with self.subTest(call=call):
                with self.assertRaises(ValueError):
                    call()


if __name__ == "__main__":
    unittest.main()
