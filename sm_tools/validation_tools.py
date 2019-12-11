import pytesmo.scaling as scaling
import pytesmo.metrics as metrics
import numpy as np
import inspect
import sys


def __arguments_validator(func):
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


@__arguments_validator
def triple_collocation(ground_station_data, satellite_data, model_data, scale=True):
    """
    Wrapper for pytesmo.metrics.tcol_error to estimate the standard deviation of epsilon(error)
    Documentation: https://github.com/TUW-GEO/pytesmo/blob/master/docs/Triple%20collocation.ipynb

    :param ground_station_data: numpy.ndarray - soil moisture observation from ground station or x in documentation
    :param satellite_data: numpy.ndarray - soil moisture data from satellite image or y in documentation
    :param model_data: numpy.ndarray - soil moisture data from math model or z in documentation
    :param scale: marker to add using or mean-standard deviation scaling for datasets
    :return (e_ground, e_satellite, e_model): tuple - estimated errors for all input datasets
    """
    if scale:
        try:
            satellite_data = scaling.mean_std(satellite_data, ground_station_data)
            model_data = scaling.mean_std(model_data, ground_station_data)
        except BaseException:
            raise ValueError("Error while data scaling!"
                             "Check input data and try again.") from None

    return metrics.tcol_error(ground_station_data, satellite_data, model_data)


@__arguments_validator
def aad(ground_station_data, model_data):
    """
    Wrapper for pytesmo.metrics.RSS - method to get average absolute deviation
    :param ground_station_data: numpy.ndarray - soil moisture observation data from ground station
    :param model_data: numpy.ndarray - soil moisture data from math model
    :return aad: float - mean absolute deviation
    """
    return metrics.aad(ground_station_data, model_data)


@__arguments_validator
def bias(ground_station_data, model_data):
    """
    Wrapper for pytesmo.metrics.bias - method to get difference of the mean values
    :param ground_station_data: numpy.ndarray - soil moisture observation data from ground station
    :param model_data: numpy.ndarray - soil moisture data from math model
    :return bias: float -- mean(ground_station_data) - mean(model_data)
    """
    return metrics.bias(ground_station_data, model_data)


@__arguments_validator
def index_of_agreement(ground_station_data, model_data):
    """
    Wrapper for pytesmo.metrics.index_of_agreement - method to get index of agreement between two vars
    method to get the ratio of the mean square error and the potential error
    :param ground_station_data: numpy.ndarray - soil moisture observation data from ground station
    :param model_data: numpy.ndarray - soil moisture data from math model
    :return index_of_agreement: float - index of agreement
    """
    return metrics.index_of_agreement(ground_station_data, model_data)


@__arguments_validator
def mad(ground_station_data, model_data):
    """
    Wrapper for pytesmo.metrics.mad - method to get median absolute deviation
    :param ground_station_data: numpy.ndarray - soil moisture observation data from ground station
    :param model_data: numpy.ndarray - soil moisture data from math model
    :return mad: float - median absolute deviation
    """
    return metrics.mad(ground_station_data, model_data)


@__arguments_validator
def mse(ground_station_data, model_data):
    """
    Wrapper for pytesmo.metrics.mse - method to get mean square error
    :param ground_station_data: numpy.ndarray - soil moisture observation data from ground station
    :param model_data: numpy.ndarray - soil moisture data from math model
    :return (mse, mse_corr, mse_bias, mse var): tuple - mse and it`s components
    """
    return metrics.mse(ground_station_data, model_data, len(ground_station_data))


@__arguments_validator
def nash_sutcliffe(ground_station_data, model_data):
    """
    Wrapper for pytesmo.metrics.nash_sutcliffe - method to get Nash Sutcliffe model efficiency coefficient E
    :param ground_station_data: numpy.ndarray - soil moisture observation data from ground station
    :param model_data: numpy.ndarray - soil moisture data from math model
    :return E: float - Nash Sutcliffe model efficiency coefficient E
    """
    return metrics.nash_sutcliffe(ground_station_data, model_data)


@__arguments_validator
def nrmsd(ground_station_data, model_data):
    """
    Wrapper for pytesmo.metrics.nrmsd - method to get normalized root-mean-square deviation (nRMSD)
    :param ground_station_data: numpy.ndarray - soil moisture observation data from ground station
    :param model_data: numpy.ndarray - soil moisture data from math model
    :return nrmsd: float – Normalized root-mean-square deviation (nRMSD)
    """
    return metrics.nrmsd(ground_station_data, model_data)


@__arguments_validator
def pearson_correlation(ground_station_data, model_data):
    """
    Wrapper for pytesmo.metrics.pearsonr - method to get Pearson correlation coefficient
    and the p-value for testing non-correlation
    :param ground_station_data: numpy.ndarray - soil moisture observation data from ground station
    :param model_data: numpy.ndarray - soil moisture data from math model
    :return (r, p_value): tuple - Pearson’s correlation coefficient and 2 tailed p-value
    """
    return metrics.pearsonr(ground_station_data, model_data)


@__arguments_validator
def rmsd(ground_station_data, model_data):
    """
    Wrapper for pytesmo.metrics.rmsd - method to get root-mean-square deviation
    and the p-value for testing non-correlation
    :param ground_station_data: numpy.ndarray - soil moisture observation data from ground station
    :param model_data: numpy.ndarray - soil moisture data from math model
    :return rmsd: float -  root-mean-square deviation
    """
    return metrics.rmsd(ground_station_data, model_data, len(ground_station_data) - 1)


@__arguments_validator
def spearman_correlation(ground_station_data, model_data):
    """
    Wrapper for pytesmo.metrics.spearmanr - method to get Spearman rank-order correlation coefficient
    and the p-value to test for non-correlation
    :param ground_station_data: numpy.ndarray - soil moisture observation data from ground station
    :param model_data: numpy.ndarray - soil moisture data from math model
    :return (rho, p_value): tuple - Spearman correlation coefficient
    and the two-sided p-value for a hypothesis test whose null hypothesis is that two sets of data are uncorrelated
    """
    return metrics.spearmanr(ground_station_data, model_data)


@__arguments_validator
def ubrmsd(ground_station_data, model_data):
    """
    Wrapper for pytesmo.metrics.ubrmsd - method to get unbiased root-mean-square deviation (uRMSD)
    and the p-value to test for non-correlation
    :param ground_station_data: numpy.ndarray - soil moisture observation data from ground station
    :param model_data: numpy.ndarray - soil moisture data from math model
    :return ubrmsd: float - unbiased root-mean-square deviation (uRMSD)
    """
    return metrics.ubrmsd(ground_station_data, model_data, len(ground_station_data) - 1)


@__arguments_validator
def get_all_validation_values(ground_station_data, model_data, satellite_data=None, scale=True):
    # get all validation functions in this module
    # except private decorator and current function
    # and save it to dict
    validators = {name: obj for name, obj in inspect.getmembers(sys.modules[__name__])
                  if inspect.isfunction(obj) and "__" not in name and name != "get_all_validation_values"}

    validation_values = dict()
    for name, func in validators.items():
        if name != "triple_collocation":
            validation_values[name] = func(ground_station_data, model_data)
        else:
            if satellite_data is not None:
                validation_values[name] = func(ground_station_data, satellite_data, model_data, scale=scale)
            else:
                validation_values[name] = "Can not make triple collocation on two datasets!"

    return validation_values
