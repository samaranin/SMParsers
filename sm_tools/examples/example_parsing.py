from sm_tools.parsers import ISMNDataParser


if __name__ == '__main__':
    # create new parser instance
    parser = ISMNDataParser()

    # default values for demonstration
    default_network_name = 'REMEDHUS'
    default_station_name = 'fraye'
    default_sensor_name = 'soil_moisture(m3m-3 * 100)_0.05m ThetaProbe ML2X'
    default_start_date = '2016/01/01'
    default_end_date = '2016/12/31'

    # demonstration
    # full network data by name, also exists same method for ID
    print(f'Get all data for network \'{default_network_name}\'')
    print(parser.get_network_object_by_name(default_network_name), end='\n\n')

    # list of stations names for network by name, also exists same method for ID
    print(f'Get list of stations names for network \'{default_network_name}\'')
    print(parser.get_stations_names_list_for_network(default_network_name), end='\n\n')

    # full station data by name, also exists same method for ID
    print(f'Get all data for station \'{default_station_name}\'')
    print(parser.get_station_object_by_name(default_station_name), end='\n\n')

    print(f'Get station observation time for \'{default_station_name}\'')
    print(parser.get_station_sensors_metadata_list_by_name(default_station_name,
                                                           start_date="2006/01/01",
                                                           end_date=default_end_date), end='\n\n')

    # list of sensors names by station name, also exists same method for ID
    print('Get list of sensors names for station '' + default_station_name + ''')
    print(parser.get_sensors_names_list_for_station_by_name(default_station_name), end='\n\n')

    # full sensor data for station by name
    print(f'Get all data for sensor \'{default_sensor_name}\' in \'{default_station_name}\' station')
    print(parser.get_sensor_object_by_name(default_station_name, default_sensor_name), end='\n\n')

    # get type and depth data from sensor name
    print(f'Get type and depth sensor \'{default_sensor_name}\'')
    print(parser.get_sensor_type_and_depth_by_name(default_sensor_name), end='\n\n')

    # get observation for sensor on station in date range by name
    print(f'Get observations for sensor \'{default_sensor_name}\' on \'{default_station_name}\' station '
          f'(start date: \'{default_start_date}\' and end date: \'{default_end_date}\')')

    for normalize in (True, False):
        print(f"  {'N' if normalize else 'Not n'}ormalized: ")
        data = parser.get_sensor_observation_by_name(default_station_name, default_sensor_name,
                                                     default_start_date, default_end_date, normalize=normalize)
        print('    {')
        for key in data.keys():
            print(f'      \'{key}\': {data[key]}')
        print('    }', end='\n\n')
