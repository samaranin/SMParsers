import unittest
from sm_parser.parsers import ISMNDataParser


class TestSearch(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestSearch, self).__init__(*args, **kwargs)
        self.ismn_parser = ISMNDataParser()
        self.default_network_name = "REMEDHUS"
        self.default_station_name = "Station25"
        self.default_station_id = 8

    def tests_get_network_by_name(self):
        with self.assertRaises(TypeError):
            self.ismn_parser.get_network_object_by_name(self.default_station_id)

        with self.assertRaises(ValueError):
            self.ismn_parser.get_network_object_by_name("")

        network = self.ismn_parser.get_network_object_by_name(self.default_network_name)
        self.assertIsNotNone(network)
        self.assertIsInstance(network, dict)

    def tests_get_station_by_name(self):
        with self.assertRaises(TypeError):
            self.ismn_parser.get_station_object_by_name(self.default_station_id)

        with self.assertRaises(ValueError):
            self.ismn_parser.get_station_object_by_name("")

        station = self.ismn_parser.get_station_object_by_name(self.default_station_name)
        self.assertIsNotNone(station)
        self.assertIsInstance(station, dict)


if __name__ == "__main__":
    unittest.main()
