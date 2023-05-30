import unittest
from zAlgorithm import naive_z_algorithm
from zAlgorithm import z_algorithm


class MyTestCase(unittest.TestCase):
    def test_naive_z(self):
        naive_z_actual = naive_z_algorithm('ababac')
        naive_z_expected = [6, 0, 3, 0, 1, 0]
        self.assertEqual(naive_z_expected, naive_z_actual)

    def test1(self):
        test1_actual = z_algorithm('aabcaabxaay')
        test1_expected = [11, 1, 0, 0, 3, 1, 0, 0, 2, 1, 0]
        self.assertEqual(test1_expected, test1_actual)

    def test2(self):
        test2_actual = z_algorithm('abab')
        test2_expected = [4, 0, 2, 0]
        self.assertEqual(test2_expected, test2_actual)

    def test3(self):
        # a | b | a | b | a | c
        # - | 0 | 3 | 0 | 1 | 0
        # - | bc | c1 | c2a | c2b | c1
        test3_actual = z_algorithm('ababac')
        test3_expected = [6, 0, 3, 0, 1, 0]
        self.assertEqual(test3_expected, test3_actual)


if __name__ == '__main__':
    unittest.main()
