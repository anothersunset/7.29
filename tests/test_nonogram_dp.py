import unittest

from src.analysis import analyze_solutions
from src.nonogram_dp import UNKNOWN, line_options, solve_nonogram


class NonogramDpTests(unittest.TestCase):
    def test_line_options(self):
        options = line_options((2,), (UNKNOWN, UNKNOWN, 0))
        self.assertEqual(options, (frozenset({1}), frozenset({1}), frozenset({0})))
        self.assertIsNone(line_options((2,), (0, 1, 0)))

    def test_single_cells(self):
        zero = solve_nonogram(((0,),), ((0,),))
        one = solve_nonogram(((1,),), ((1,),))
        self.assertTrue(zero.exhausted)
        self.assertTrue(one.exhausted)
        self.assertEqual(zero.solutions, (((0,),),))
        self.assertEqual(one.solutions, (((1,),),))

    def test_two_solution_permutation(self):
        clues = ((1,), (1,))
        result = solve_nonogram(clues, clues)
        self.assertTrue(result.exhausted)
        self.assertEqual(result.solution_count, 2)
        analysis = analyze_solutions(result.solutions)
        self.assertEqual(analysis.uncertain_count, 4)

    def test_solution_limit(self):
        clues = ((1,), (1,))
        result = solve_nonogram(clues, clues, max_solutions=1)
        self.assertEqual(result.solution_count, 1)
        self.assertFalse(result.exhausted)

    def test_invalid(self):
        with self.assertRaises(ValueError):
            solve_nonogram((), ())
        with self.assertRaises(ValueError):
            solve_nonogram(((1,),), ((1,), (1,)))
        with self.assertRaises(ValueError):
            solve_nonogram(((2,),), ((1,),))
        with self.assertRaises(ValueError):
            solve_nonogram(((1,),), ((1,),), max_solutions=0)


if __name__ == "__main__":
    unittest.main()
