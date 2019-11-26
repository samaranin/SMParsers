"""
StationID in Network->Stations
Start, End -> Dates
Depth_ID, Sensor_ID, Variable_ID -> Variables(StationID)
"""

import requests
import json


HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0",
           "Accept-Language": "en-US,en;q=0"}

NETWORKS_LINK = "https://www.geo.tuwien.ac.at/insitu/data_viewer/station_details/network_station_details.json"

DATA_LINK = "https://www.geo.tuwien.ac.at/insitu/data_viewer/server/dataviewer/dataviewer_load_variable.php?" \
            "station_id=375&start=2012%2F01%2F01&end=2013%2F01%2F01&depth_id=35&sensor_id=6&variable_id=8"

VARIABLES_LINK = "https://www.geo.tuwien.ac.at/insitu/data_viewer/server/dataviewer/dataviewer_get_variable_list.php?" \
                 "station_id=375&start=2018%2F11%2F26&end=2019%2F11%2F26"


test_data = "https://www.geo.tuwien.ac.at/insitu/data_viewer/server/dataviewer/dataviewer_load_variable.php?" \
            "station_id=3506&start=2017%2F01%2F01&end=2017%2F12%2F29&depth_id=256&sensor_id=8&variable_id=8"

session = requests.session()
request = session.get(test_data, headers=HEADERS)


if request.status_code == 200:
    with open("test_new.txt", "w") as file:
        file.write(str(json.loads(request.content)))
