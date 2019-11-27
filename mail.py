from ISMNParser.parser import DataParser


if __name__ == "__main__":
    parser = DataParser()
    print(parser.get_sensors_list_for_station_by_name("Station25", "2017/01/01", "2017/31/12"))
