import unittest
from llamascript import llama


# Unit tests
class TestLlama(unittest.TestCase):
    def setUp(self):
        self.llama = llama()

    def test_USE(self):
        with self.assertRaises(ValueError):
            self.llama.USE("llama3")

    def test_PROMPT(self):
        with self.assertRaises(ValueError):
            self.llama.PROMPT("say something")

    def test_SYSTEM(self):
        with self.assertRaises(ValueError):
            self.llama.SYSTEM("respond in piglatin")

    def test_CHAT(self):
        with self.assertRaises(ValueError):
            self.llama.CHAT()


if __name__ == "__main__":
    unittest.main()
