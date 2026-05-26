import unittest

from backend.app.models import WordPool


class WordPoolModelTests(unittest.TestCase):
    def test_normalized_answer_is_sanitized_on_assignment(self) -> None:
        word = WordPool(clue="Gruß", normalized_answer="grüße")
        self.assertEqual(word.normalized_answer, "GRUESSE")


if __name__ == "__main__":
    unittest.main()
