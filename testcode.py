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

    def test_successors_and_predecessors(self):
        code = 0b10101110110110011011011111010101
        green_succ_of_0 = [0, 1, 2, 3]
        green_succ_of_1 = [2, 3]
        green_succ_of_2 = [0, 1, 2]
        green_succ_of_3 = [1, 3]
        green_pred_of_0 = [0, 2]
        green_pred_of_1 = [0, 2, 3]
        green_pred_of_2 = [0, 1, 2]
        green_pred_of_3 = [0, 1, 3]
        red_succ_of_0 = [0, 1]
        red_succ_of_1 = [2, 3]
        red_succ_of_2 = [1, 2]
        red_succ_of_3 = [0, 1, 2, 3]
        red_pred_of_0 = [0, 3]
        red_pred_of_1 = [0, 2, 3]
        red_pred_of_2 = [1, 2, 3]
        red_pred_of_3 = [1, 3]

        self.assertEqual(codes.get_green_successors(4, code, 0), green_succ_of_0)
        self.assertEqual(codes.get_green_successors(4, code, 1), green_succ_of_1)
        self.assertEqual(codes.get_green_successors(4, code, 2), green_succ_of_2)
        self.assertEqual(codes.get_green_successors(4, code, 3), green_succ_of_3)
        self.assertEqual(codes.get_green_predecessors(4, code, 0), green_pred_of_0)
        self.assertEqual(codes.get_green_predecessors(4, code, 1), green_pred_of_1)
        self.assertEqual(codes.get_green_predecessors(4, code, 2), green_pred_of_2)
        self.assertEqual(codes.get_green_predecessors(4, code, 3), green_pred_of_3)
        self.assertEqual(codes.get_red_successors(4, code, 0), red_succ_of_0)
        self.assertEqual(codes.get_red_successors(4, code, 1), red_succ_of_1)
        self.assertEqual(codes.get_red_successors(4, code, 2), red_succ_of_2)
        self.assertEqual(codes.get_red_successors(4, code, 3), red_succ_of_3)
        self.assertEqual(codes.get_red_predecessors(4, code, 0), red_pred_of_0)
        self.assertEqual(codes.get_red_predecessors(4, code, 1), red_pred_of_1)
        self.assertEqual(codes.get_red_predecessors(4, code, 2), red_pred_of_2)
        self.assertEqual(codes.get_red_predecessors(4, code, 3), red_pred_of_3)


if __name__ == '__main__':
    unittest.main()