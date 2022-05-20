import unittest

import codes


class TestCodesMethods(unittest.TestCase):

    def test_bit(self):
        self.assertEqual(codes.bit(1, 0), 1)
        self.assertEqual(codes.bit(5, 0), 1)
        self.assertEqual(codes.bit(5, 1), 0)
        self.assertEqual(codes.bit(5, 2), 1)
        self.assertEqual(codes.bit(5, 3), 0)
        self.assertEqual(codes.bit(0, 0), 0)

    def test_old_code_to_new(self):
        self.assertEqual(codes.old_code_to_new(2, 0b11010010), 0b10110100)
        self.assertEqual(codes.old_code_to_new(3, 0b010011111011010010), 0b001111011000111100)


if __name__ == '__main__':
    unittest.main()