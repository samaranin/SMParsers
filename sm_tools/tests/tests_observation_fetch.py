import unittest
from sm_tools.parsers import ISMNDataParser


class TestObservations(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestObservations, self).__init__(*args, **kwargs)
        self.ismn_parser = ISMNDataParser()
        self.default_station_name = "fraye"
        self.default_sensor_id = 8
        self.default_wrong_id = 125482
        self.default_sensor_name = "soil_moisture(m3m-3 * 100)_0.05m ThetaProbe ML2X"

    def tests_get_sensor_observation_by_name(self):
        with self.assertRaises(ValueError):
            self.ismn_parser.get_sensor_observation_by_name("", "", "", "")

        data = self.ismn_parser.get_sensor_observation_by_name(self.default_station_name, self.default_sensor_name)
        self.assertIsNotNone(data)
        self.assertIsInstance(data, dict)
        for key in data.keys():
            self.assertIsNotNone(data[key])

        self.assertIn("dates", data)
        self.assertIsInstance(data["dates"], list)
        self.assertIn("observations", data)
        self.assertIsInstance(data["observations"], list)

        for date in data["dates"]:
            self.assertIsInstance(date, str)

        for observations in data["observations"]:
            self.assertIsInstance(observations, float)


if __name__ == "__main__":
    unittest.main()
