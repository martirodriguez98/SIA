from typing import Callable, Dict, Type, Tuple

import numpy as np
import pandas as pd
from schema import Schema, And, Or, Optional

from config import Param, Config
from neural_networks import NeuralNetwork, NeuralNetworkConfig, SimpleNeuralNetwork, LinearNeuralNetwork, \
    NonLinearNeuralNetwork

_NeuralNetworkTypeCall = Callable[[NeuralNetworkConfig], Callable[[], NeuralNetwork]]
SigmoidFunction = Callable[[float], float]
SigmoidFunctionDer = Callable[[float], float]

def get_set(file: str, line_count: int, normalize: bool) -> np.ndarray:
    set: np.ndarray = pd.read_csv(file, delim_whitespace=True, header=None).values
    if normalize:
        maxcols = set.max(axis=0)
        mincols = set.min(axis=0)
        data_shape = set.shape
        data_rows = data_shape[0]
        data_cols = data_shape[1]
        t=np.empty((data_rows,data_cols))
        for i in range(data_cols):
            t[:,i]=(set[:,i]-mincols[i])/(maxcols[i]-mincols[i])
        return t
    return set


def validate_params(params: Param) -> Param:
    return Config.validate_param(params, Schema({
        'type': And(str, Or(*tuple(_neural_networks_types.keys()))),
        Optional('sigmoid_fn', default=None): dict,
    }, ignore_extra_keys=True))


def build_network_config(network_params: Param, x_count: int) -> NeuralNetworkConfig:
    config: NeuralNetworkConfig = NeuralNetworkConfig()
    config.x_count = x_count
    if network_params["sigmoid_fn"] is not None:
        config.sigmoid_fn = network_params["sigmoid_fn"]
    # todo complete with params
    return config

def get_neural_network(neural_network_params: Param, x_count: int) -> Callable[[], NeuralNetwork]:
    neural_network_params = validate_params(neural_network_params)
    network_config: NeuralNetworkConfig = build_network_config(neural_network_params, x_count)
    neural_network_caller: _NeuralNetworkTypeCall = _neural_networks_types[neural_network_params['type']]
    return neural_network_caller(network_config)


def _get_simple_perceptron(config: NeuralNetworkConfig) -> Callable[[], NeuralNetwork]:
    return lambda: SimpleNeuralNetwork(config)


def _get_linear_perceptron(neural_network_config: NeuralNetworkConfig) -> Callable[[], NeuralNetwork]:
    return lambda: LinearNeuralNetwork(neural_network_config)

# def _validate_non_linear_params(params: Param) -> Param:
#     return Config.validate_param(params, Schema({
#
#     }, ignore_extra_keys=True))

def _get_non_linear_perceptron(neural_network_config: NeuralNetworkConfig) -> Callable[[], NeuralNetwork]:
    # params = _validate_non_linear_params(params)
    return lambda: NonLinearNeuralNetwork(neural_network_config)



_neural_networks_types: Dict[str, _NeuralNetworkTypeCall] = {
    'simple': _get_simple_perceptron,
    'linear': _get_linear_perceptron,
    'nonlinear': _get_non_linear_perceptron
    # todo complete others
}

