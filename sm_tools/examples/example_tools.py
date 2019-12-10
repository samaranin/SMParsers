from sm_tools.tools import SMValidator
import json
import glob


if __name__ == "__main__":
    default_data_files_list = glob.glob("data/*.json")

    print("Example of triple collocation validation: ")
    for file_name in default_data_files_list:
        print(f"\nGet dataset from file \'{file_name}\'", end="\n")
        with open(file_name) as file:
            data = json.loads(file.read())

        print("  Extracted data: ")
        print("    {")
        for key, value in data.items():
            print(f'      \'{key}\': \'{value}\'')
        print("    }", end="\n")

        print("Triple collocation errors: ")
        for scale in (True, False):
            print(f"  \'{'With' if scale else 'Without'}\' mean-standard deviation scaling: ")
            e_ground, e_satellite, e_model = SMValidator.triple_collocation(data['ground_station'], data['satellite'],
                                                                            data['model'], scale=scale)
            print(f"    Estimated error of ground station data: {e_ground:.4f}")
            print(f"    Estimated error of satellite data estimated: {e_satellite:.4f}")
            print(f"    Estimated error of model data estimated: {e_model:.4f}")
