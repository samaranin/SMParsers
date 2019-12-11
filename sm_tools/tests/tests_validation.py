import unittest
from sm_tools.validation_tools import *


class TestInitialization(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestInitialization, self).__init__(*args, **kwargs)

    def tests_triple_collocation(self):
        with self.assertRaises(ValueError):
            triple_collocation('', '', '')

        with self.assertRaises(ValueError):
            triple_collocation([], [], [])

        for error in triple_collocation([0.1, 0.08], [0.2, 0.18], [0.04, 0.03]):
            self.assertEqual(error < 0.0001, True)


if __name__ == "__main__":
    unittest.main()
