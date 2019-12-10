import pytesmo.scaling as scaling
import pytesmo.metrics as metrics


class SMValidator:
    """Class to apply validation methods to soil moisture data"""
    @staticmethod
    def triple_collocation(ground_station_data, satellite_data, model_data, scale=True):
        """
        Method to estimate the standard deviation of epsilon(error)
        Documentation: https://github.com/TUW-GEO/pytesmo/blob/master/docs/Triple%20collocation.ipynb

        :param ground_station_data: soil moisture observation from ground station or x in documentation
        :param satellite_data: soil moisture data from satellite image or y in documentation
        :param model_data: soil moisture data from math model or z in documentation
        :param scale: marker to add using or mean-standard deviation scaling for datasets
        :return: e_ground, e_satellite, e_model = estimated errors for all datasets
        """
        if len(ground_station_data) < 1 or len(satellite_data) < 1 or len(model_data) < 1:
            raise ValueError("Parameters must contain at least one value!"
                             "Check input data and try again.")

        if scale:
            try:
                satellite_data = scaling.mean_std(satellite_data, ground_station_data)
                model_data = scaling.mean_std(model_data, ground_station_data)
            except BaseException:
                raise ValueError("Error while data scaling!"
                                 "Input data must be np.array or list with numbers!"
                                 "Check input data and try again.") from None

        return metrics.tcol_error(ground_station_data, satellite_data, model_data)
