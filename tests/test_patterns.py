"""Tests for valid binary pattern generation."""

import unittest

from src.encoding import encode_line
from src.patterns import count_patterns, generate_patterns


class PatternGenerationTests(unittest.TestCase):
    def test_known_example(self) -> None:
        self.assertEqual(
            generate_patterns(5, (2, 1)),
            (
                (1, 1, 0, 1, 0),
                (1, 1, 0, 0, 1),
                (0, 1, 1, 0, 1),
            ),
        )

    def test_generated_patterns_are_complete_and_valid(self) -> None:
        cases = [
            (5, (2, 1)),
            (10, (3, 3, 1)),
            (10, (1, 1, 1, 2)),
            (15, (3, 1, 2, 1)),
            (4, (0,)),
        ]
        for length, clue in cases:
            with self.subTest(length=length, clue=clue):
                patterns = generate_patterns(length, clue)
                self.assertEqual(len(patterns), count_patterns(length, clue))
                self.assertEqual(len(patterns), len(set(patterns)))
                self.assertTrue(all(len(pattern) == length for pattern in patterns))
                self.assertTrue(all(encode_line(pattern) == clue for pattern in patterns))

    def test_all_zero_clue(self) -> None:
        self.assertEqual(count_patterns(6, (0,)), 1)
        self.assertEqual(generate_patterns(6, (0,)), ((0, 0, 0, 0, 0, 0),))

    def test_invalid_requests(self) -> None:
        cases = [(0, (0,)), (-1, (1,)), (4, (3, 1)), (5, (2, 0, 1))]
        for length, clue in cases:
            with self.subTest(length=length, clue=clue):
                with self.assertRaises(ValueError):
                    generate_patterns(length, clue)
                with self.assertRaises(ValueError):
                    count_patterns(length, clue)


if __name__ == "__main__":
    unittest.main()
