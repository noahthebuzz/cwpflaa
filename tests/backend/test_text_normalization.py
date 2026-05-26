import unittest

from backend.app.services.text_normalization import normalize_answer


class NormalizeAnswerTests(unittest.TestCase):
    def test_umlauts_and_eszett_are_expanded(self) -> None:
        self.assertEqual(normalize_answer("grüße"), "GRUESSE")

    def test_invalid_characters_raise(self) -> None:
        with self.assertRaises(ValueError):
            normalize_answer("AB-CD")

    def test_whitespace_and_case_are_normalized(self) -> None:
        self.assertEqual(normalize_answer("  deadline  "), "DEADLINE")


if __name__ == "__main__":
    unittest.main()
