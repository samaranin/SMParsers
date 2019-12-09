import pytesmo.scaling as scaling
import pytesmo.metrics as metrics


class SMValidator:

    def __init__(self):
        pass

    @staticmethod
    def triple_collocation(ground_station_data, satellite_data, model_data, normalize=True):
        if not normalize:
            e_ground, e_satellite, e_model = metrics.tcol_error(ground_station_data, satellite_data, model_data)
        else:
            satellite_data_scaled = scaling.mean_std(satellite_data, ground_station_data)
            model_data_scaled = scaling.mean_std(model_data, ground_station_data)
            e_ground, e_satellite, e_model = metrics.tcol_error(ground_station_data,
                                                                satellite_data_scaled, model_data_scaled)

        print("Data was normalized" if normalize else "Data was not normalized")
        print("Error of ground station data estimated: {:.4f}".format(e_ground))
        print("Error of satellite data estimated: {:.4f}".format(e_satellite))
        print("Error of model data estimated: {:.4f}".format(e_model))
        return e_ground, e_satellite, e_model
