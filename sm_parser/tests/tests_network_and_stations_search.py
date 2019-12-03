import unittest
from sm_parser.parsers import ISMNDataParser


class TestSearch(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestSearch, self).__init__(*args, **kwargs)
        self.ismn_parser = ISMNDataParser()
        self.default_network_name = "REMEDHUS"
        self.default_station_name = "fraye"
        self.default_station_id = 3506
        self.default_wrong_id = 125482
        self.default_sensor_id = 8
        self.default_sensor_name = "soil_moisture(m3m-3 * 100)_0.05m ThetaProbe ML2X"
        self.additional_sensor_name = "soil_temperature(C)_0.00m-0.05m LI-COR Temperature Sensors"
        self.sensor_name_with_minus = "air_temperature(C)_-1.5m Platinum Resistance Thermometer"

    def tests_get_network_by_name(self):
        with self.assertRaises(ValueError):
            self.ismn_parser.get_network_object_by_name(self.default_station_id)

        with self.assertRaises(ValueError):
            self.ismn_parser.get_network_object_by_name("")

        network = self.ismn_parser.get_network_object_by_name(self.default_network_name)
        self.assertIsNotNone(network)
        self.assertIsInstance(network, dict)

    def tests_get_station_by_name(self):
        with self.assertRaises(ValueError):
            self.ismn_parser.get_station_object_by_name(self.default_station_id)

        with self.assertRaises(ValueError):
            self.ismn_parser.get_station_object_by_name("")

        station = self.ismn_parser.get_station_object_by_name(self.default_station_name)
        self.assertIsNotNone(station)
        self.assertIsInstance(station, dict)

    def tests_get_stations_objects_for_network(self):
        with self.assertRaises(ValueError):
            self.ismn_parser.get_stations_objects_list_for_network(self.default_station_id)

        with self.assertRaises(ValueError):
            self.ismn_parser.get_stations_objects_list_for_network("")

        network = self.ismn_parser.get_stations_objects_list_for_network(self.default_network_name)
        self.assertIsNotNone(network)
        self.assertIsInstance(network, list)
        for station in network:
            self.assertIsInstance(station, dict)

    def tests_get_stations_names_list_for_network(self):
        with self.assertRaises(ValueError):
            self.ismn_parser.get_stations_names_list_for_network(self.default_station_id)

        with self.assertRaises(ValueError):
            self.ismn_parser.get_stations_names_list_for_network("")

        network = self.ismn_parser.get_stations_names_list_for_network(self.default_network_name)
        self.assertIsNotNone(network)
        self.assertIsInstance(network, list)
        for station in network:
            self.assertIsInstance(station, str)

    def tests_get_station_id_by_name(self):
        with self.assertRaises(ValueError):
            self.ismn_parser.get_station_id_by_name(self.default_station_id)

        with self.assertRaises(ValueError):
            self.ismn_parser.get_station_id_by_name("")

        station_id = self.ismn_parser.get_station_id_by_name(self.default_station_name)
        self.assertIsNotNone(station_id)
        self.assertIsInstance(station_id, int)
        self.assertEqual(station_id, self.default_station_id)

    def get_sensors_objects_list_for_station_by_id(self):
        with self.assertRaises(ValueError):
            self.ismn_parser.get_sensors_objects_list_for_station_by_id(self.default_station_id, "", "")

        with self.assertRaises(ValueError):
            self.ismn_parser.get_sensors_objects_list_for_station_by_id(self.default_wrong_id, "", "")

        with self.assertRaises(ValueError):
            self.ismn_parser.get_sensors_objects_list_for_station_by_id("")

        sensors = self.ismn_parser.get_station_id_by_name(self.default_station_id)
        self.assertIsNotNone(sensors)
        self.assertIsInstance(sensors, list)
        for sensor in sensors:
            self.assertIsInstance(sensor, dict)

    def tests_get_sensors_objects_list_for_station_by_name(self):
        with self.assertRaises(ValueError):
            self.ismn_parser.get_sensors_objects_list_for_station_by_name(self.default_station_id, "", "")

        with self.assertRaises(ValueError):
            self.ismn_parser.get_sensors_objects_list_for_station_by_name("")

        sensors = self.ismn_parser.get_sensors_objects_list_for_station_by_name(self.default_station_name)
        self.assertIsNotNone(sensors)
        self.assertIsInstance(sensors, list)
        for sensor in sensors:
            self.assertIsInstance(sensor, dict)

    def tests_get_sensors_names_list_for_station_by_id(self):
        with self.assertRaises(ValueError):
            self.ismn_parser.get_sensors_names_list_for_station_by_id(self.default_station_id, "", "")

        with self.assertRaises(ValueError):
            self.ismn_parser.get_sensors_objects_list_for_station_by_id(self.default_wrong_id, "", "")

        with self.assertRaises(ValueError):
            self.ismn_parser.get_sensors_names_list_for_station_by_id("")

        sensors = self.ismn_parser.get_sensors_names_list_for_station_by_id(self.default_station_id)
        self.assertIsNotNone(sensors)
        self.assertIsInstance(sensors, list)
        for sensor in sensors:
            self.assertIsInstance(sensor, str)

    def tests_get_sensors_names_list_for_station_by_name(self):
        with self.assertRaises(ValueError):
            self.ismn_parser.get_sensors_names_list_for_station_by_name(self.default_station_id, "", "")

        with self.assertRaises(ValueError):
            self.ismn_parser.get_sensors_names_list_for_station_by_name("")

        sensors = self.ismn_parser.get_sensors_names_list_for_station_by_name(self.default_station_name)
        self.assertIsNotNone(sensors)
        self.assertIsInstance(sensors, list)
        for sensor in sensors:
            self.assertIsInstance(sensor, str)

    def tests_get_sensor_objects_list_by_id(self):
        with self.assertRaises(ValueError):
            self.ismn_parser.get_sensor_objects_list_by_id("", "")

        with self.assertRaises(ValueError):
            self.ismn_parser.get_sensors_objects_list_for_station_by_id(self.default_wrong_id, "", "")

        sensors = self.ismn_parser.get_sensor_objects_list_by_id(self.default_station_name, self.default_sensor_id)
        self.assertIsNotNone(sensors)
        self.assertIsInstance(sensors, list)
        for sensor in sensors:
            self.assertIsInstance(sensor, dict)

    def tests_get_sensor_object_by_name(self):
        with self.assertRaises(ValueError):
            self.ismn_parser.get_sensor_object_by_name("", "")

        sensor = self.ismn_parser.get_sensor_object_by_name(self.default_station_name, self.default_sensor_name)
        self.assertIsNotNone(sensor)
        self.assertIsInstance(sensor, dict)

    def tests_get_sensor_type_and_depth_by_name(self):
        with self.assertRaises(ValueError):
            self.ismn_parser.get_sensor_type_and_depth_by_name("")

        data = self.ismn_parser.get_sensor_type_and_depth_by_name(self.default_sensor_name)
        self.assertIsNotNone(data)
        self.assertIsInstance(data, dict)
        self.assertEqual(data["sensor_type"], "soil_moisture")
        self.assertEqual(data["sensor_depth"], "0.05m")

        data = self.ismn_parser.get_sensor_type_and_depth_by_name(self.additional_sensor_name)
        self.assertIsNotNone(data)
        self.assertIsInstance(data, dict)
        self.assertEqual(data["sensor_type"], "soil_temperature")
        self.assertEqual(data["sensor_depth"], "0.00m-0.05m")

        data = self.ismn_parser.get_sensor_type_and_depth_by_name(self.sensor_name_with_minus)
        self.assertIsNotNone(data)
        self.assertIsInstance(data, dict)
        self.assertEqual(data["sensor_type"], "air_temperature")
        self.assertEqual(data["sensor_depth"], "-1.5m")


if __name__ == "__main__":
    unittest.main()
