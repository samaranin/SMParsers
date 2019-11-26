"""
StationID in Network->Stations
Start, End -> Dates
Depth_ID, Sensor_ID, Variable_ID -> Variables(StationID)
"""

import requests
import json


class DataParser:

    DEFAULT_HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0",
                       "Accept-Language": "en-US,en;q=0"}

    NETWORKS_URL = "https://www.geo.tuwien.ac.at/insitu/data_viewer/station_details/network_station_details.json"

    VARS_LINK = "https://www.geo.tuwien.ac.at/insitu/data_viewer/server/dataviewer/dataviewer_get_variable_list.php?" \
                "station_id=375&start=2018%2F11%2F26&end=2019%2F11%2F26"

    DATA_URL = "https://www.geo.tuwien.ac.at/insitu/data_viewer/server/dataviewer/dataviewer_load_variable.php?" \
               "station_id=375&start=2012%2F01%2F01&end=2013%2F01%2F01&depth_id=35&sensor_id=6&variable_id=8"

    def __init__(self, headers=None):
        self.session = requests.session()
        self.headers = headers if headers is not None else self.DEFAULT_HEADERS
        self.__networks_objects_list = self.__get_networks_data()
        self.__stations_objects_list = self.__get_stations_data()

    def __get_networks_data(self):
        """
        Method to get all networks objects
        :return: list of networks with all inner data (stations, etc) or None
        """
        request = self.session.get(self.NETWORKS_URL, headers=self.headers)
        if request.status_code != 200:
            return None

        return json.loads(request.content.decode("utf-8"))["Networks"]

    def __get_stations_data(self):
        """
        Method to get all station objects form all networks

        :return: list of station objects or None
        """
        if self.__networks_objects_list is not None:
            return [station for network in self.__networks_objects_list for station in network["Stations"]]

        return None

    @property
    def network_names_list(self):
        """
        Method to get list of networks names from ISMN
        :return: list of dicts with networks or None
        """

        if self.__networks_objects_list is not None:
            return [network_object["networkID"] for network_object in self.__networks_objects_list]

        return None

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
            network_reference: "Peischl, S., Walker, J. P., Rüdiger, C., Ye, N., Kerr, Y. H., Kim, E., Bandara, R., and Allahmoradi, M.: The AACES field experiments: SMOS calibration and validation across the Murrumbidgee River catchment, Hydrology and Earth System Sciences, Discuss., 9, 2763-2795, doi:10.5194/hessd-9-2763-2012, 2012"
            network_sensors: "ThetaProbe ML2X,<br>"
            network_status: "inactive"
            network_type: "project"
            network_url: "http://www.moisturemap.monash.edu.au/"
            network_url_data: null
            network_variables: "soil moisture<br>soil temperature<br>precipitation<br>"
        }

        :return: list of networks objects or None
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

        :return: list of station objects or None
        """

        return self.__stations_objects_list

    @property
    def stations_names_list(self):
        """
        Method to get all available station names
        :return: list of stations names or None
        """
        if self.__stations_objects_list is not None:
            return [station["station_name"] for station in self.__stations_objects_list]

        return None
