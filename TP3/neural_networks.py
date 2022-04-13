from abc import ABC


class NeuralNetworkConfig:
    def __init__(self):
        x_count: int
        neural: str
        single: str
        simple: str

class NeuralNetwork(ABC):

     def __init__(self, config: NeuralNetworkConfig):
         config.neural = "en neural"

class SingleNeuralNetwork(NeuralNetwork, ABC):

    def __init__(self, config: NeuralNetworkConfig):
        config.single = "en single"
        super().__init__(config)

class SimpleNeuralNetwork(SingleNeuralNetwork):
    def __init__(self, config: NeuralNetworkConfig):
        config.simple = "en simple"
        super().__init__(config)
    #extiende a SingleNeuralN

# class LinearNeuralNetwork(SingleNeuralNetwork):
#     #extiende a SingleNeuralN
#
# class NonLinearNeuralNetwork(SingleNeuralNetwork):
#     #extiende a SingleNeuralN
#
#
# class MultilayerNeuralNetwork(NeuralNetwork):
#     #clase (no abs) para el multicapa (ej 3)