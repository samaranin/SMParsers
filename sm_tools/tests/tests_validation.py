import unittest
from sm_tools import validation_tools


class TestInitialization(unittest.TestCase):
    EPSILON = 0.0001
    DEFAULT_DATA = [0.1, 0.08, 0.12]

    def __init__(self, *args, **kwargs):
        super(TestInitialization, self).__init__(*args, **kwargs)

    def tests_triple_collocation(self):
        with self.assertRaises(ValueError):
            validation_tools.triple_collocation('', '', '')

        with self.assertRaises(ValueError):
            validation_tools.triple_collocation([], [], [])

        error_data = validation_tools.triple_collocation(self.DEFAULT_DATA, self.DEFAULT_DATA, self.DEFAULT_DATA)
        self.assertIsInstance(error_data, dict)
        for value in error_data.values():
            self.assertEqual(value < 0.0001, True)

    def tests_bias(self):
        bias = validation_tools.bias(self.DEFAULT_DATA, self.DEFAULT_DATA)
        print(bias, type(bias))
        self.assertEqual(bias < self.EPSILON, True)


if __name__ == "__main__":
    unittest.main()
