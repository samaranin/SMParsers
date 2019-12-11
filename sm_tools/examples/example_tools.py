from sm_tools.validation_tools import get_all_validation_values
import json
import glob


if __name__ == '__main__':
    default_data_files_list = glob.glob('data/*.json')

    print('Example of validation usage: ')
    for file_name in default_data_files_list:
        print(f'\nGet dataset from file \'{file_name}\'', end='\n')
        with open(file_name) as file:
            data = json.loads(file.read())

        print('  Extracted data: ')
        print('  {')
        for key, value in data.items():
            print(f'    \'{key}\': {value}')
        print('  }', end='\n\n')

        print('  Validation data:')
        print('  {')
        validation_data = get_all_validation_values(data['ground_station'], data['model'],
                                                    satellite_data=data['satellite'], scale=True)
        for method, data in validation_data.items():
            if isinstance(data, dict):
                print(f'    \'{method}\': {{')
                for key, value in data.items():
                    print(f'      \'{key}\': {value:.6f}')
                print('    }')
            else:
                print(f'    \'{method}\': {data:.6f}')
        print('  }', end='\n')
