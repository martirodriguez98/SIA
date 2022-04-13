from typing import Callable, Dict, Type

import numpy as np
import pandas as pd
from schema import Schema, And, Or, Optional

from config import Param, Config
from neural_networks import NeuralNetwork, NeuralNetworkConfig, SimpleNeuralNetwork

_NeuralNetworkTypeCall = Callable[[NeuralNetworkConfig, Param], Callable[[],NeuralNetwork]]

def get_set(file: str, line_count: int) -> np.ndarray:
    set: np.ndarray = pd.read_csv(file, delim_whitespace=True, header=None).values
    #todo check for other exercises
    return set

def validate_params(params: Param) -> Param:
    return Config.validate_param(params, Schema({
        'type': And(str, Or(*tuple(_neural_networks_types.keys()))),
        Optional('network_params', default=None): dict,
    }, ignore_extra_keys=True))

def build_network_config(network_params: Param, x_count: int) -> NeuralNetworkConfig:
    config: NeuralNetworkConfig = NeuralNetworkConfig()
    config.x_count = x_count
    #todo complete with params
    return config

def get_neural_network(neural_network_params: Param, x_count: int) -> Callable[[], NeuralNetwork]:
    neural_network_params = validate_params(neural_network_params)
    network_config: NeuralNetworkConfig = build_network_config(neural_network_params,x_count)
    neural_network_caller: _NeuralNetworkTypeCall = _neural_networks_types[neural_network_params['type']]
    return neural_network_caller(network_config, neural_network_params['network_params'])

def _get_simple_perceptron(config: NeuralNetworkConfig, params: Param) -> Callable[[], NeuralNetwork]:
    return lambda: SimpleNeuralNetwork(config)

# def _get_linear_perceptron(neural_network_config: NeuralNetworkConfig, params: Param) -> LinearNeuralNetwork:
#     return LinearNeuralNetwork(neural_network_config)


_neural_networks_types: Dict[str, _NeuralNetworkTypeCall] = {
    'simple': _get_simple_perceptron,
    # 'linear': _get_linear_perceptron,
    #todo complete others
}
