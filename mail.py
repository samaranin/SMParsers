from soil_moisture_parsers.parsers import ISMNDataParser


if __name__ == "__main__":
    parser = ISMNDataParser()
    print(parser.get_sensors_list_for_station_by_name("Station25", "2017/01/01", "2017/31/12"))
