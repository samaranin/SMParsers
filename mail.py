from ISMNParser.parser import DataParser


if __name__ == "__main__":
    parser = DataParser()
    print(parser.get_station_id_by_name("Station25"))
