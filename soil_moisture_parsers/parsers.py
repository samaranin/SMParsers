"""
StationID in Network->Stations
Start, End -> Dates
Depth_ID, Sensor_ID, Variable_ID -> Variables(StationID)
"""

import requests
import json


def is_networks_exists(func):
    """
    Decorator to check is networks data exists
    """
    def _decorator(self, *args, **kwargs):
        if getattr(self, '_networks_objects_list') is not None:
            return func(self, *args, **kwargs)
        raise ValueError("Networks or stations data not found!")
    return _decorator


class ISMNDataParser:

    # default headers for request if there was no headers passed to constructor
    DEFAULT_HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0",
                       "Accept-Language": "en-US,en;q=0"}

    # url to get all networks data
    NETWORKS_URL = "https://www.geo.tuwien.ac.at/insitu/data_viewer/station_details/network_station_details.json"

    # base url for sensors data requests
    BASE_URL = "https://www.geo.tuwien.ac.at/insitu/data_viewer/server/dataviewer/dataviewer_get_variable_list.php"

    DATA_URL = "https://www.geo.tuwien.ac.at/insitu/data_viewer/server/dataviewer/dataviewer_load_variable.php?" \
               "station_id=375&start=2012%2F01%2F01&end=2013%2F01%2F01&depth_id=35&sensor_id=6&variable_id=8"

    def __init__(self, headers=None):
        # creating new session on object creation
        self.session = requests.session()
        # setting headers for request - passed to constructor or default headers
        self.headers = headers if headers is not None else self.DEFAULT_HEADERS
        # set requests timeout
        self.request_timeout = 20
        # fetching all networks data on object initialization
        self._networks_objects_list = self.__get_networks_data()
        # getting all stations data from all networks
        self._stations_objects_list = self.__get_stations_data()

    def __get_networks_data(self):
        """
        Method to get all networks objects
        :return: list of dicts - networks with all inner data (stations, etc) or None
        """
        # making request to ISMN server to get all networks data with timeout
        request = self.session.get(self.NETWORKS_URL, headers=self.headers, timeout=self.request_timeout)
        # if request wasn't successful - raise error
        if request.status_code != 200:
            raise ConnectionError("Can not connect to server!")

        # return parsed network data
        return json.loads(request.content.decode("utf-8"))["Networks"]

    @is_networks_exists
    def __get_stations_data(self):
        """
        Method to get all station objects form all networks

        :return: list of dicts - all station objects or None
        """
        return [station for network in self._networks_objects_list for station in network["Stations"]]

    @property
    @is_networks_exists
    def network_names_list(self):
        """
        Method to get list of networks names from ISMN
        :return: list of strings - networks names or None
        """
        return [network_object["networkID"] for network_object in self._networks_objects_list]

    @property
    @is_networks_exists
    def networks_objects(self):
        """
        Method to get all networks objects wit all inner data

        Network object example:
        {
            Stations: [list of station objects],
            networkID: "AACES"
            network_abstract: null
            network_acknowledge: null
            network_constraints: null
            network_continent: "Australia"
            network_country: "Australia"
            network_depths: "0.00 - 0.05 m <br>0.00 - 0.06 m <br>0.25 - 0.25 m <br>"
            network_op_end: "2010-09-26"
            network_op_start: "2010-01-18"
            network_reference: "Peischl, S., Walker, J. P..."
            network_sensors: "ThetaProbe ML2X,<br>"
            network_status: "inactive"
            network_type: "project"
            network_url: "http://www.moisturemap.monash.edu.au/"
            network_url_data: null
            network_variables: "soil moisture<br>soil temperature<br>precipitation<br>"
        }

        :return: list of dicts - networks objects or None
        """
        return self._networks_objects_list

    @property
    @is_networks_exists
    def stations_objects(self):
        """
        Method to get all available stations objects

        Station object example:
        {
            comment: null
            depthText: "0.00 - 0.06 m <br>0.25 - 0.25 m <br>"
            extMetadata: null
            lat: "-34.780428"
            lng: "147.140801"
            maximum: "2010/02/10 01:00:00"
            minimum: "2010/02/08 00:00:00"
            sensorText: "Delta-T Devices, ThetaProbe ML2X,<br>"
            stationID: "2134"
            station_abbr: "25"
            station_name: "Station25"
            variableText: "soil moisture<br>soil temperature<br>precipitation<br>"
        }

        :return: list of dicts - station objects or None
        """

        return self._stations_objects_list

    @property
    @is_networks_exists
    def stations_names_list(self):
        """
        Method to get all available station names
        :return: list of strings - stations names or None
        """
        return [station["station_name"] for station in self._stations_objects_list]

    @is_networks_exists
    def get_network_object_by_name(self, network_name):
        """
        Method to get network object using name
        :param network_name: string - network name
        :return: dict - network object with this name or None
        """
        for network in self._networks_objects_list:
            if network_name == network["networkID"]:
                return network

        raise ValueError("Not found network with name '" + network_name + "'")

    @is_networks_exists
    def get_station_object_by_name(self, station_name):
        """
        Method to get station object by name
        :param station_name: string - station name
        :return: dict - station object with this name or None
        """
        for station in self._stations_objects_list:
            if station_name == station["station_name"]:
                return station

        raise ValueError("Not found station with name '" + station_name + "'")

    @is_networks_exists
    def get_stations_objects_list_for_network(self, network_name):
        """
        Method to get list of station objects for this network
        :param network_name: string - network name
        :return: list of dicts - station objects or None
        """
        network = self.get_network_object_by_name(network_name)
        if network is None:
            raise ValueError("Not found network with name '" + network_name + "'")

        return network["Stations"]

    @is_networks_exists
    def get_stations_names_list_for_network(self, network_name):
        """
        Method to get list of station names for this network
        :param network_name: string - network name
        :return: list of strings - station names or None
        """
        network = self.get_stations_objects_list_for_network(network_name)
        if network is None:
            raise ValueError("Not found network with name '" + network_name + "'")

        return [station["station_name"] for station in network]

    @is_networks_exists
    def get_station_id_by_name(self, station_name):
        """
        Method to get station ID for this station name
        :param station_name: string - station name
        :return: int - station ID
        """
        station = self.get_station_object_by_name(station_name)
        if station is None:
            raise ValueError("Not found station with name '" + station_name + "'")

        return int(station["stationID"])

    @is_networks_exists
    def get_sensors_list_for_station_by_id(self, station_id, start_date, end_date):
        """
        Method to get sensors objects list for current station
        :param station_id: int - station ID
        :param start_date: string - date format YYYY/MM/DD
        :param end_date: string - date format YYYY/MM/DD
        :return: list of dicts - sensors objects
        """
        # generating request url based on parameters
        request_url = self.BASE_URL + "?station_id={0}&start={1}&end={2}".format(station_id, start_date, end_date)
        # making request to server
        request = self.session.get(request_url, headers=self.headers, timeout=self.request_timeout)
        # if there was no response - raise error
        if request.status_code != 200:
            raise ConnectionError("Can not connect to server! Check input data!")

        # return parsed network data
        return json.loads(request.content.decode("utf-8"))["variables"]

    @is_networks_exists
    def get_sensors_list_for_station_by_name(self, station_name, start_date, end_date):
        """
        Method to get sensors objects list for current station
        :param station_name: string - station name
        :param start_date: string - date format YYYY/MM/DD
        :param end_date: string - date format YYYY/MM/DD
        :return: list of dicts - sensors objects
        """
        station_id = self.get_station_id_by_name(station_name)
        if station_id is None:
            raise ValueError("Not found station with name '" + station_name + "'")

        return self.get_sensors_list_for_station_by_id(station_id, start_date, end_date)
