"""Tests for run-length clue parsing and encoding."""

import unittest

from src.encoding import encode_line, parse_clue


class ParseClueTests(unittest.TestCase):
    def test_supported_inputs(self) -> None:
        cases = [
            (5, (5,)),
            (5.0, (5,)),
            ("1,2,3", (1, 2, 3)),
            (" 1, 2 ", (1, 2)),
            (0, (0,)),
            ("0", (0,)),
            (None, (0,)),
            ("", (0,)),
            ((3, 1), (3, 1)),
        ]
        for value, expected in cases:
            with self.subTest(value=value):
                self.assertEqual(parse_clue(value), expected)

    def test_invalid_inputs(self) -> None:
        for value in [True, -1, 1.5, "1,,2", "a,2", (2, 0, 1), (2, -1)]:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    parse_clue(value)


class EncodeLineTests(unittest.TestCase):
    def test_known_lines(self) -> None:
        cases = [
            ((1, 1, 1, 1), (4,)),
            ((0, 1, 0, 1, 1), (1, 2)),
            ((0, 0, 0, 0), (0,)),
            ((0, 0, 1, 1, 1, 0, 1, 1, 0, 0), (3, 2)),
            ((1, 0, 1, 0, 1), (1, 1, 1)),
        ]
        for line, expected in cases:
            with self.subTest(line=line):
                self.assertEqual(encode_line(line), expected)

    def test_invalid_lines(self) -> None:
        for line in [(), (0, 2, 1), (0, -1), (0, 0.5)]:
            with self.subTest(line=line):
                with self.assertRaises(ValueError):
                    encode_line(line)


if __name__ == "__main__":
    unittest.main()
