import unittest
from shortener import generate_random_code
from constants import ALPHABET, MAX_CODE_LEN,MIN_CODE_LEN

class TestShortener(unittest.TestCase):

    def test_generate_random_code_no_len(self):
        code = generate_random_code()

        has_valid_size = len(code) <= MAX_CODE_LEN and len(code) >= MIN_CODE_LEN
        self.assertEqual(has_valid_size, True)
        for char in code:
            self.assertTrue(char in ALPHABET)

    def test_generate_random_code_fixed_len(self):
        code = generate_random_code(5)

        has_valid_size = len(code) == 5 
        self.assertEqual(has_valid_size, True)
        for char in code:
            self.assertTrue(char in ALPHABET)

