import unittest

from generate_parentheses import generate_parentheses


class GenerateParenthesesTest(unittest.TestCase):
    def test_zero_pairs(self):
        self.assertEqual(generate_parentheses(0), [""])

    def test_one_pair(self):
        self.assertEqual(generate_parentheses(1), ["()"])

    def test_three_pairs(self):
        self.assertEqual(
            generate_parentheses(3),
            ["((()))", "(()())", "(())()", "()(())", "()()()"],
        )

    def test_negative_pairs_are_invalid(self):
        with self.assertRaises(ValueError):
            generate_parentheses(-1)


if __name__ == "__main__":
    unittest.main()
