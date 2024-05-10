import unittest
from unittest.mock import patch
from lang import llama


class TestLlama(unittest.TestCase):
    def setUp(self):
        self.llama = llama()

    def test_USE(self):
        self.llama.USE("USE llama3")
        self.assertEqual(self.llama.model, "llama3")

    def test_PROMPT(self):
        self.llama.PROMPT("PROMPT prompt1")
        self.assertEqual(self.llama.data, "prompt1")

    def test_SYSTEM(self):
        self.llama.SYSTEM("SYSTEM system1")
        self.assertEqual(self.llama.system, [{"role": "system", "content": "system1"}])

    def test_INPUT_SYSTEM(self):
        with patch("builtins.input", return_value="system1"):
            self.llama.INPUT("SYSTEM")
        self.assertEqual(self.llama.system, [{"role": "system", "content": "system1"}])

    def test_INPUT_PROMPT(self):
        with patch("builtins.input", return_value="prompt1"):
            self.llama.INPUT("PROMPT")
        self.assertEqual(self.llama.data, "prompt1")

    def test_INPUT_invalid_command(self):
        with self.assertRaises(ValueError):
            self.llama.INPUT("INVALID")


if __name__ == "__main__":
    unittest.main()
