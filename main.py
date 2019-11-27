from soil_moisture_parsers.parsers import ISMNDataParser


if __name__ == "__main__":
    parser = ISMNDataParser()
    print(parser.get_sensor_observation_by_name("fraye", "soil_moisture(m3m-3 * 100)_0.05m ThetaProbe ML2X",
                                                "2017/01/01", "2017/12/29"))
