import pytesmo.scaling as scaling
import pytesmo.metrics as metrics
import numpy as np


def arguments_validator(func):
    """
    Method to check and convert function parameters to np.ndarray
    :param func: function to check parameters
    :return: function with validated parameters
    """
    def validator(*args, **kwargs):
        converted_args = []
        for arg in args:
            if len(arg) < 1:
                raise ValueError("Parameters must be np.ndarray or list and contain at least one value!"
                                 "Check input data and try again.")

            try:
                converted_arg = np.array(arg)
            except BaseException:
                raise ValueError("Error while converting argument to nd.array!"
                                 "Parameters must be np.ndarray or list and contain at least one value!"
                                 "Check input data and try again.")
            converted_args.append(converted_arg)
        return func(*converted_args, **kwargs)

    return validator


class SMValidator:
    """Class to apply validation methods to soil moisture data"""

    @staticmethod
    @arguments_validator
    def triple_collocation(ground_station_data, satellite_data, model_data, scale=True):
        """
        Wrapper for pytesmo.metrics.tcol_error to estimate the standard deviation of epsilon(error)
        Documentation: https://github.com/TUW-GEO/pytesmo/blob/master/docs/Triple%20collocation.ipynb

        :param ground_station_data: numpy.ndarray - soil moisture observation from ground station or x in documentation
        :param satellite_data: numpy.ndarray - soil moisture data from satellite image or y in documentation
        :param model_data: numpy.ndarray - soil moisture data from math model or z in documentation
        :param scale: marker to add using or mean-standard deviation scaling for datasets
        :return: float e_ground, e_satellite, e_model - estimated errors for all input datasets
        """
        if scale:
            try:
                satellite_data = scaling.mean_std(satellite_data, ground_station_data)
                model_data = scaling.mean_std(model_data, ground_station_data)
            except BaseException:
                raise ValueError("Error while data scaling!"
                                 "Check input data and try again.") from None

        return metrics.tcol_error(ground_station_data, satellite_data, model_data)

    @staticmethod
    @arguments_validator
    def rss(ground_station_data, model_data):
        """
        Wrapper for pytesmo.metrics.RSS - method to get residual sum of squares
        :param ground_station_data: numpy.ndarray - soil moisture observation data from ground station
        :param model_data: numpy.ndarray - soil moisture data from math model
        :return: float residual sum of squares
        """
        return metrics.RSS(ground_station_data, model_data)

    @staticmethod
    @arguments_validator
    def aad(ground_station_data, model_data):
        """
        Wrapper for pytesmo.metrics.RSS - method to get average absolute deviation
        :param ground_station_data: numpy.ndarray - soil moisture observation data from ground station
        :param model_data: numpy.ndarray - soil moisture data from math model
        :return: float mean absolute deviation
        """
        return metrics.aad(ground_station_data, model_data)

    @staticmethod
    @arguments_validator
    def bias(ground_station_data, model_data):
        """
        Wrapper for pytesmo.metrics.bias - method to get difference of the mean values
        :param ground_station_data: numpy.ndarray - soil moisture observation data from ground station
        :param model_data: numpy.ndarray - soil moisture data from math model
        :return: float bias -- mean(ground_station_data) - mean(model_data)
        """
        return metrics.bias(ground_station_data, model_data)

    @staticmethod
    @arguments_validator
    def index_of_agreement(ground_station_data, model_data):
        """
        Wrapper for pytesmo.metrics.index_of_agreement - method to get index of agreement between two vars
        method to get the ratio of the mean square error and the potential error
        :param ground_station_data: numpy.ndarray - soil moisture observation data from ground station
        :param model_data: numpy.ndarray - soil moisture data from math model
        :return: float index of agreement
        """
        return metrics.index_of_agreement(ground_station_data, model_data)

    @staticmethod
    @arguments_validator
    def mad(ground_station_data, model_data):
        """
        Wrapper for pytesmo.metrics.mad - method to get median absolute deviation
        :param ground_station_data: numpy.ndarray - soil moisture observation data from ground station
        :param model_data: numpy.ndarray - soil moisture data from math model
        :return: float median absolute deviation
        """
        return metrics.mad(ground_station_data, model_data)
