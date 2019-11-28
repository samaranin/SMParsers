import unittest
from sm_parser.parsers import ISMNDataParser


class TestInitialization(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestInitialization, self).__init__(*args, **kwargs)
        self.ismn_parser = ISMNDataParser()
        self.default_network_name = "REMEDHUS"
        self.default_station_name = "Station25"

    def test_initialization(self):
        self.assertIsNotNone(self.ismn_parser)
        self.assertIsNotNone(self.ismn_parser.DEFAULT_HEADERS)
        self.assertIsNotNone(self.ismn_parser.NETWORKS_URL)
        self.assertIsNotNone(self.ismn_parser.SENSOR_URL)
        self.assertIsNotNone(self.ismn_parser.DATA_URL)
        self.assertIsNotNone(self.ismn_parser.headers)
        self.assertIsNotNone(self.ismn_parser.request_timeout)

    def test_networks_names(self):
        self.assertIsNotNone(self.ismn_parser.network_names_list)
        self.assertIsInstance(self.ismn_parser.network_names_list, list)
        self.assertIn(self.default_network_name, self.ismn_parser.network_names_list)

    def test_networks_objects(self):
        self.assertIsNotNone(any(self.ismn_parser.networks_objects))
        self.assertIsInstance(self.ismn_parser.networks_objects, list)

    def test_stations_names(self):
        self.assertIsNotNone(self.ismn_parser.stations_names_list)
        self.assertIsInstance(self.ismn_parser.stations_names_list, list)
        self.assertIn(self.default_station_name, self.ismn_parser.stations_names_list)

    def test_stations_objects(self):
        self.assertIsNotNone(any(self.ismn_parser.stations_objects))
        self.assertIsInstance(self.ismn_parser.stations_objects, list)


if __name__ == "__main__":
    unittest.main()
