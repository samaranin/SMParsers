import requests
import json
import datetime
import re


class ISMNDataParser:
    """
    Class for parsing data from ISMN - https://www.geo.tuwien.ac.at/insitu/data_viewer/
    """

    # default headers for request if there was no headers passed to constructor
    DEFAULT_HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0",
                       "Accept-Language": "en-US,en;q=0"}

    # url to get all networks data
    NETWORKS_URL = "https://www.geo.tuwien.ac.at/insitu/data_viewer/station_details/network_station_details.json"

    # base url for sensors data requests
    SENSOR_URL = "https://www.geo.tuwien.ac.at/insitu/data_viewer/server/dataviewer/dataviewer_get_variable_list.php"

    # base url for observations data requests
    DATA_URL = "https://www.geo.tuwien.ac.at/insitu/data_viewer/server/dataviewer/dataviewer_load_variable.php"

    def __init__(self, headers=None):
        # creating new session on object creation
        self.__session = requests.session()
        # setting headers for request - passed to constructor or default headers
        self.headers = headers if headers is not None else self.DEFAULT_HEADERS
        # set requests timeout
        self.request_timeout = 20
        # fetching all networks data on object initialization
        self.__networks_objects_list = self.__get_networks_data()
        # getting all stations data from all networks
        self.__stations_objects_list = self.__get_stations_data()

    def __del__(self):
        self.__session.close()

    def __get_networks_data(self):
        """
        Method to get all networks objects
        :return: list of dicts - networks with all inner data (stations, etc) or None
        """
        # making request to ISMN server to get all networks data with timeout
        request = self.__session.get(self.NETWORKS_URL, headers=self.headers, timeout=self.request_timeout)
        # if request wasn't successful - raise error
        if request.status_code != 200:
            raise ConnectionError("Can not connect to server!")

        # return parsed network data
        try:
            return json.loads(request.content.decode("utf-8"))["Networks"]
        except json.decoder.JSONDecodeError:
            raise ValueError("Error while server response processing! "
                             "Check input parameters or https://www.geo.tuwien.ac.at/ server status.") from None

    def __get_stations_data(self):
        """
        Method to get all station objects form all networks

        :return: list of dicts - all station objects or None
        """
        return [station for network in self.__networks_objects_list for station in network["Stations"]]

    @property
    def network_names_list(self):
        """
        Method to get list of networks names from ISMN
        :return: list of strings - networks names or None
        """
        return [network_object["networkID"] for network_object in self.__networks_objects_list]

    @property
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
        return self.__networks_objects_list

    @property
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

        return self.__stations_objects_list

    @property
    def stations_names_list(self):
        """
        Method to get all available station names
        :return: list of strings - stations names or None
        """
        return [station["station_name"] for station in self.__stations_objects_list]

    def get_network_object_by_name(self, network_name):
        """
        Method to get network object using name
        :param network_name: string - network name
        :return: dict - network object with this name or None
        """
        name = str(network_name)
        for network in self.__networks_objects_list:
            if name == network["networkID"]:
                return network

        raise ValueError(f"Not found network with name \'{name}\'")

    def get_station_object_by_name(self, station_name):
        """
        Method to get station object by name
        :param station_name: string - station name
        :return: dict - station object with this name or None
        """
        name = str(station_name)
        for station in self.__stations_objects_list:
            if name == station["station_name"]:
                return station

        raise ValueError(f"Not found station with name \'{name}\'")

    def get_stations_objects_list_for_network(self, network_name):
        """
        Method to get list of station objects for this network
        :param network_name: string - network name
        :return: list of dicts - station objects or None
        """
        return self.get_network_object_by_name(network_name)["Stations"]

    def get_stations_names_list_for_network(self, network_name):
        """
        Method to get list of station names for this network
        :param network_name: string - network name
        :return: list of strings - station names or None
        """
        network = self.get_stations_objects_list_for_network(network_name)
        return [station["station_name"] for station in network]

    def get_station_id_by_name(self, station_name):
        """
        Method to get station ID for this station name
        :param station_name: string - station name
        :return: int - station ID
        """
        station = self.get_station_object_by_name(station_name)
        return int(station["stationID"])

    def get_sensors_objects_list_for_station_by_id(self, station_id,
                                                   start_date="2017/01/01", end_date="2017/12/31"):
        """
        Method to get sensors objects list for current station by station ID
        :param station_id: int or string - station ID
        :param start_date: string - date format YYYY/MM/DD
        :param end_date: string - date format YYYY/MM/DD
        :return: list of dicts - sensors objects
        """
        try:
            start_date_object = datetime.datetime.strptime(start_date, '%Y/%m/%d')
            end_date_object = datetime.datetime.strptime(end_date, '%Y/%m/%d')
        except Exception:
            raise ValueError("Start and end dates must be in YYYY/MM/DD format!")

        if start_date_object > end_date_object:
            raise ValueError("Start date must be earlier then end date!")

        # generating request url based on parameters
        request_url = self.SENSOR_URL + f"?station_id={station_id}&start={start_date}&end={end_date}"
        # making request to server
        request = self.__session.get(request_url, headers=self.headers, timeout=self.request_timeout)
        # if there was no response - raise error
        if request.status_code != 200:
            raise ConnectionError("Can not connect to server! Check input data!")

        # return parsed network data
        try:
            return json.loads(request.content.decode("utf-8"))["variables"]
        except json.decoder.JSONDecodeError:
            raise ValueError("Error while server response processing! "
                             "Check input parameters or https://www.geo.tuwien.ac.at/ server status.") from None

    def get_sensors_objects_list_for_station_by_name(self, station_name,
                                                     start_date="2017/01/01", end_date="2017/12/31"):
        """
        Method to get sensors objects list for current station by station name
        :param station_name: string - station name
        :param start_date: string - date format YYYY/MM/DD
        :param end_date: string - date format YYYY/MM/DD
        :return: list of dicts - sensors objects
        """
        station_id = self.get_station_id_by_name(station_name)
        return self.get_sensors_objects_list_for_station_by_id(station_id, start_date, end_date)

    def get_sensors_names_list_for_station_by_id(self, station_id,
                                                 start_date="2017/01/01", end_date="2017/12/31"):
        """
        Method to get sensors objects names list for current station by station ID
        :param station_id: int - station ID
        :param start_date: string - date format YYYY/MM/DD
        :param end_date: string - date format YYYY/MM/DD
        :return: list of strings - sensors names
        """
        sensors_list = self.get_sensors_objects_list_for_station_by_id(station_id, start_date, end_date)
        return [sensor["variableName"] for sensor in sensors_list]

    def get_sensors_names_list_for_station_by_name(self, station_name,
                                                   start_date="2017/01/01", end_date="2017/12/31"):
        """
        Method to get sensors objects names list for current station by station name
        :param station_name: string - station name
        :param start_date: string - date format YYYY/MM/DD
        :param end_date: string - date format YYYY/MM/DD
        :return: list of strings - sensors names
        """
        sensors_list = self.get_sensors_objects_list_for_station_by_name(station_name, start_date, end_date)
        return [sensor["variableName"] for sensor in sensors_list]

    def get_sensor_object_by_id(self, station_name, sensor_id):
        """
        Method to get sensor data by it`s ID
        :param station_name: string - station name where sensor placed
        :param sensor_id: int - sensor ID for station
        :return: dict - sensor object
        """
        sensors = self.get_sensors_objects_list_for_station_by_name(station_name)
        for sensor in sensors:
            if sensor["sensorId"] == str(sensor_id):
                return sensor

        raise ValueError("Sensor with ID " + sensor_id + " not found!")

    def get_sensor_object_by_name(self, station_name, sensor_name):
        """
        Method to get sensor data by it`s name
        :param station_name: string - station name where sensor placed
        :param sensor_name: string - sensor name for station
        :return: dict - sensor object
        """
        sensors = self.get_sensors_objects_list_for_station_by_name(station_name)
        for sensor in sensors:
            if sensor["variableName"] == sensor_name:
                return sensor

        raise ValueError("Sensor with name " + sensor_name + " not found!")

    @staticmethod
    def get_sensor_type_and_depth_by_name(sensor_name):
        """
        Method to extract sensor type and sensor depth from sensor name
        :param sensor_name: string - sensor name
        :return:
        """
        if not sensor_name:
            raise ValueError("You need to specify correct sensor name!")

        sensor_type = sensor_name.split("(")[0]
        sensor_depth = re.search(r"(\d\.\d+[a-z])?[-]?(\d\.\d+[a-z])", sensor_name).group(0)
        return {"sensor_type": sensor_type, "sensor_depth": sensor_depth}

    def get_sensor_observation_by_id(self, station_name, sensor_id,
                                     start_date="2017/01/01", end_date="2017/12/31", normalize=True):
        """
        Method to get observation data for sensor in station by sensor ID
        :param station_name: string - station name
        :param sensor_id: int - sensor ID
        :param start_date: string - date format YYYY/MM/DD
        :param end_date: string - date format YYYY/MM/DD
        :param normalize: bool - use absolute values if True, otherwise - values * 100
        :return: dict - {"dates": list of observation dates, "observation": list of observations}
        """
        try:
            start_date_object = datetime.datetime.strptime(start_date, '%Y/%m/%d')
            end_date_object = datetime.datetime.strptime(end_date, '%Y/%m/%d')
        except Exception:
            raise ValueError("Start and end dates must be in YYYY/MM/DD format!")

        if start_date_object > end_date_object:
            raise ValueError("Start date must be earlier then end date!")

        # gather all data we need for request
        station_id = self.get_station_id_by_name(station_name)
        sensor_object = self.get_sensor_object_by_id(station_name, sensor_id)
        variable_id, depth_id = sensor_object["variableId"], sensor_object["depthId"]

        # preparing url for request
        request_url = self.DATA_URL + f"?station_id={station_id}&start={start_date}&end={end_date}&" \
            f"depth_id={depth_id}&sensor_id={sensor_id}&variable_id={variable_id}"

        request = self.__session.get(request_url, headers=self.headers, timeout=self.request_timeout)
        if request.status_code != 200:
            raise ConnectionError("Can not get data from server! Check parameters!")

        # preparing data
        try:
            observation_data = json.loads(request.content.decode("utf-8"))
        except json.decoder.JSONDecodeError:
            raise ValueError("Error while server response processing! "
                             "Check input parameters or https://www.geo.tuwien.ac.at/ server status.") from None

        observations = [float(obs) for obs in observation_data[1]]
        observations = [round(float(obs) / 100, 5) for obs in observation_data[1]] if normalize else observations
        return {"dates": observation_data[0], "observations": observations}

    def get_sensor_observation_by_name(self, station_name, sensor_name,
                                       start_date="2017/01/01", end_date="2017/12/31", normalize=True):
        """
        Method to get observation data for sensor in station by sensor name
        :param station_name:  string - station name
        :param sensor_name: string - sensor name
        :param start_date: string - date format YYYY/MM/DD
        :param end_date: string - date format YYYY/MM/DD
        :param normalize: bool - use absolute values if True, otherwise - values * 100
        :return: dict - {"dates": list of observation dates, "observation": list of observations}
        """
        sensor_id = self.get_sensor_object_by_name(station_name, sensor_name)["sensorId"]
        return self.get_sensor_observation_by_id(station_name, sensor_id, start_date, end_date, normalize)
