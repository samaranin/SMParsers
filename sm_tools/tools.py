import pytesmo.scaling as scaling
import pytesmo.metrics as metrics
import numpy as np


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
        try:
            ground_station_data = np.array(ground_station_data)
            satellite_data = np.array(satellite_data)
            model_data = np.array(model_data)
        except BaseException:
            raise ValueError("Input data must be np.array or list with numbers!"
                             "Check input data and try again.") from None

        if not scale:
            e_ground, e_satellite, e_model = metrics.tcol_error(ground_station_data, satellite_data, model_data)
        else:
            satellite_data_scaled = scaling.mean_std(satellite_data, ground_station_data)
            model_data_scaled = scaling.mean_std(model_data, ground_station_data)
            e_ground, e_satellite, e_model = metrics.tcol_error(ground_station_data,
                                                                satellite_data_scaled, model_data_scaled)

        return e_ground, e_satellite, e_model
