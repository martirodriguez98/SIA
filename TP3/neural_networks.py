import random
from abc import ABC

import numpy as np


class NeuralNetworkConfig:
    def __init__(self):
        self.x_count: int = 0
        self.neural: str
        self.single: str
        self.simple: str


class NeuralNetwork(ABC):
    def __init__(self, config_neural: NeuralNetworkConfig):
        self.config_neural: NeuralNetworkConfig = config_neural

    def train(self, x: np.ndarray, y: np.ndarray):
        i: int = 0
        w = np.zeros(self.config_neural.x_count + 1)
        error: int = 1
        error_min = len(y) * 2
        while error > 0:
            i_x = random.randint(1, len(y))
            h = x[i_x].w
            # o = signo(h)
            # delta_w = n * (y[i_x] - o).x[i_x]
            # w = w + delta_w
            # error=calcular error
            if error < error_min:
                error_min = error
                w_min = w
            i = i + 1
        

class SingleNeuralNetwork(NeuralNetwork, ABC):

    def __init__(self, config: NeuralNetworkConfig):
        config.single = "en single"
        super().__init__(config)

    def train(self):
        super().train()


class SimpleNeuralNetwork(SingleNeuralNetwork):
    def __init__(self, config: NeuralNetworkConfig):
        config.simple = "en simple"
        super().__init__(config)
    # extiende a SingleNeuralN

# class LinearNeuralNetwork(SingleNeuralNetwork):
#     #extiende a SingleNeuralN
#
# class NonLinearNeuralNetwork(SingleNeuralNetwork):
#     #extiende a SingleNeuralN
#
#
# class MultilayerNeuralNetwork(NeuralNetwork):
#     #clase (no abs) para el multicapa (ej 3)
