import unittest
from sm_tools import validation_tools


class TestInitialization(unittest.TestCase):
    EPSILON = 0.0001
    DEFAULT_DATA = [0.1, 0.08, 0.12]

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
        with self.assertRaises(ValueError):
            validation_tools.bias('', '')

        with self.assertRaises(ValueError):
            validation_tools.bias([], [])

        bias = validation_tools.bias(self.DEFAULT_DATA, self.DEFAULT_DATA)
        self.assertIsInstance(bias, float)
        self.assertEqual(bias < self.EPSILON, True)

    def tests_average_absolute_deviation(self):
        with self.assertRaises(ValueError):
            validation_tools.average_absolute_deviation('', '')

        with self.assertRaises(ValueError):
            validation_tools.average_absolute_deviation([], [])

        aad = validation_tools.average_absolute_deviation(self.DEFAULT_DATA, self.DEFAULT_DATA)
        self.assertIsInstance(aad, float)
        self.assertEqual(aad < self.EPSILON, True)

    def tests_median_absolute_deviation(self):
        with self.assertRaises(ValueError):
            validation_tools.median_absolute_deviation('', '')

        with self.assertRaises(ValueError):
            validation_tools.median_absolute_deviation([], [])

        mad = validation_tools.median_absolute_deviation(self.DEFAULT_DATA, self.DEFAULT_DATA)
        self.assertIsInstance(mad, float)
        self.assertEqual(mad < self.EPSILON, True)

    def tests_nash_sutcliffe_coefficient(self):
        with self.assertRaises(ValueError):
            validation_tools.nash_sutcliffe_coefficient('', '')

        with self.assertRaises(ValueError):
            validation_tools.nash_sutcliffe_coefficient([], [])

        e = validation_tools.nash_sutcliffe_coefficient(self.DEFAULT_DATA, self.DEFAULT_DATA)
        self.assertIsInstance(e, float)
        self.assertEqual(e + self.EPSILON > 1, True)

    def tests_index_of_agreement(self):
        with self.assertRaises(ValueError):
            validation_tools.index_of_agreement('', '')

        with self.assertRaises(ValueError):
            validation_tools.index_of_agreement([], [])

        ioa = validation_tools.index_of_agreement(self.DEFAULT_DATA, self.DEFAULT_DATA)
        self.assertIsInstance(ioa, float)
        self.assertEqual(ioa + self.EPSILON > 1, True)

    def tests_pearson_correlation(self):
        with self.assertRaises(ValueError):
            validation_tools.pearson_correlation('', '')

        with self.assertRaises(ValueError):
            validation_tools.pearson_correlation([], [])

        pearson = validation_tools.pearson_correlation(self.DEFAULT_DATA, self.DEFAULT_DATA)
        self.assertIsInstance(pearson, dict)
        self.assertEqual(pearson['r'] + self.EPSILON > 1, True)
        self.assertEqual(pearson['p_value'] < self.EPSILON, True)

    def tests_spearman_correlation(self):
        with self.assertRaises(ValueError):
            validation_tools.spearman_correlation('', '')

        with self.assertRaises(ValueError):
            validation_tools.spearman_correlation([], [])

        spearman = validation_tools.spearman_correlation(self.DEFAULT_DATA, self.DEFAULT_DATA)
        self.assertIsInstance(spearman, dict)
        self.assertEqual(spearman['r'] + self.EPSILON > 1, True)
        self.assertEqual(spearman['p_value'] < self.EPSILON, True)

    def tests_rmsd(self):
        with self.assertRaises(ValueError):
            validation_tools.rmsd('', '')

        with self.assertRaises(ValueError):
            validation_tools.rmsd([], [])

        rmsd = validation_tools.rmsd(self.DEFAULT_DATA, self.DEFAULT_DATA)
        self.assertIsInstance(rmsd, float)
        self.assertEqual(rmsd < self.EPSILON, True)

    def tests_nrmsd(self):
        with self.assertRaises(ValueError):
            validation_tools.nrmsd('', '')

        with self.assertRaises(ValueError):
            validation_tools.nrmsd([], [])

        nrmsd = validation_tools.nrmsd(self.DEFAULT_DATA, self.DEFAULT_DATA)
        self.assertIsInstance(nrmsd, float)
        self.assertEqual(nrmsd < self.EPSILON, True)

    def tests_ubrmsd(self):
        with self.assertRaises(ValueError):
            validation_tools.ubrmsd('', '')

        with self.assertRaises(ValueError):
            validation_tools.ubrmsd([], [])

        ubrmsd = validation_tools.ubrmsd(self.DEFAULT_DATA, self.DEFAULT_DATA)
        self.assertIsInstance(ubrmsd, float)
        self.assertEqual(ubrmsd < self.EPSILON, True)

    def tests_mean_square_error(self):
        with self.assertRaises(ValueError):
            validation_tools.mean_square_error('', '')

        with self.assertRaises(ValueError):
            validation_tools.mean_square_error([], [])

        mean_square_error = validation_tools.mean_square_error(self.DEFAULT_DATA, self.DEFAULT_DATA)
        self.assertIsInstance(mean_square_error, dict)
        for value in mean_square_error.values():
            self.assertEqual(value < self.EPSILON, True)

    def tests_get_all_validation_values(self):
        with self.assertRaises(ValueError):
            validation_tools.get_all_validation_values('', '')

        with self.assertRaises(ValueError):
            validation_tools.get_all_validation_values([], [])

        validation_data = validation_tools.get_all_validation_values(self.DEFAULT_DATA, self.DEFAULT_DATA)
        self.assertIsInstance(validation_data, dict)
        for method, data in validation_data.items():
            if isinstance(data, dict):
                for value in data.values():
                    self.assertIsInstance(value, float)
                    self.assertEqual(value < self.EPSILON or value + self.EPSILON > 1, True)
                continue

            if method == "triple_collocation":
                self.assertIsInstance(data, str)
                self.assertEqual(data, "Can not make triple collocation on two datasets!")
            else:
                self.assertIsInstance(data, float)
                self.assertEqual(data < self.EPSILON or data + self.EPSILON > 1, True)


if __name__ == "__main__":
    unittest.main()
