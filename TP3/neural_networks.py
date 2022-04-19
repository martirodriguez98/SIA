import random
from abc import ABC
from plot import plot
import numpy as np

# chequear si la tenemos que definir nosotras o la pasan como parametro
COTA = 10
n = 0.1


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
        p: int = len(y)
        i: int = 0
        w = np.zeros(self.config_neural.x_count)
        all_w: list = []
        all_w.append(w)
        error: int = 1
        error_min = p * 2
        while error > 0 and i < COTA:
            i_x = random.randint(1, len(y)-1)
            h = np.dot(x[i_x],w)
            o = np.sign(h)
            delta_w = np.dot((n * (y[i_x] - o))[0],x[i_x])
            # delta_w = n * (y[i_x] - o).x[i_x]
            w = w + delta_w
            all_w.append(w)
            error = self.calcular_error(x, y, w, p)
            if error < error_min:
                error_min = error
                w_min = w
            i = i + 1
        plot(all_w)
        
    def calcular_error(self, x: np.ndarray, y: np.ndarray, w: np.array, p: int):
        return 1


class SingleNeuralNetwork(NeuralNetwork, ABC):

    def __init__(self, config: NeuralNetworkConfig):
        config.single = "en single"
        super().__init__(config)

    def train(self,  x: np.ndarray, y: np.ndarray):
        super().train(x, y)


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
