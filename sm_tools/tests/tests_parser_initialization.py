import unittest
from sm_tools.parsers import ISMNDataParser


class TestInitialization(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestInitialization, self).__init__(*args, **kwargs)
        self.ismn_parser = ISMNDataParser()
        self.default_network_name = "REMEDHUS"
        self.default_station_name = "Station25"

    def tests_initialization(self):
        self.assertIsNotNone(self.ismn_parser)
        self.assertIsNotNone(self.ismn_parser.DEFAULT_HEADERS)
        self.assertIsNotNone(self.ismn_parser.NETWORKS_URL)
        self.assertIsNotNone(self.ismn_parser.SENSOR_URL)
        self.assertIsNotNone(self.ismn_parser.DATA_URL)
        self.assertIsNotNone(self.ismn_parser.headers)
        self.assertIsNotNone(self.ismn_parser.request_timeout)

    def tests_networks_names(self):
        networks = self.ismn_parser.network_names_list
        self.assertIsNotNone(networks)
        self.assertIsInstance(networks, list)
        self.assertIn(self.default_network_name, networks)
        for network in networks:
            self.assertIsInstance(network, str)

    def tests_networks_objects(self):
        networks = self.ismn_parser.networks_objects
        self.assertIsNotNone(networks)
        self.assertIsInstance(networks, list)
        for network in networks:
            self.assertIsInstance(network, dict)

    def tests_stations_names(self):
        stations = self.ismn_parser.stations_names_list
        self.assertIsNotNone(stations)
        self.assertIsInstance(stations, list)
        self.assertIn(self.default_station_name, stations)
        for station in stations:
            self.assertIsInstance(station, str)

    def tests_stations_objects(self):
        stations = self.ismn_parser.stations_objects
        self.assertIsNotNone(stations)
        self.assertIsInstance(stations, list)
        for station in stations:
            self.assertIsInstance(station, dict)


if __name__ == "__main__":
    unittest.main()
