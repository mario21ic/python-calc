import unittest

from src.modules.calc import Calc


class TestCalc(unittest.TestCase):

    def test_add(self):
        calc = Calc()
        result = calc.add(12, 5)
        self.assertEqual(17.0, result)

    def test_sub(self):
        calc = Calc()
        result = calc.sub(12, 5)
        self.assertEqual(7.0, result)

    def test_mul(self):
        calc = Calc()
        result = calc.mul(10, 5)
        self.assertEqual(50.0, result)

    def test_div(self):
        calc = Calc()
        result = calc.div(25, 5)
        self.assertEqual(5.0, result)

    """
    def test_div_by_zero(self):
        calc = Calc()
        result = calc.div(25, 0)
        self.assertEqual(5.0, result)

    def test_mod(self):
        calc = Calc()
        result = calc.mod(11, 3)
        self.assertEqual(2.0, result)
    """


if __name__ == '__main__':
    unittest.main()
