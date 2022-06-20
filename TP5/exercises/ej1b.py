from autoencoder import Autoencoder
from fonts.fonts import Font3
from utils import transform_input, add_noise, letter_heatmap
from numpy import array

if __name__ == "__main__":
    training_set = transform_input(Font3)
    set_with_noise = add_noise(training_set)
    # letter_heatmap(training_set)
    letter_heatmap(set_with_noise)

    layers = [25,15,10]
    autoencoder = Autoencoder(set_with_noise, training_set, layers, 2, 15,0.001)
    result = autoencoder.train()

    decoded_values = []
    for v in set_with_noise:
        decoded_values.append(autoencoder.propagate(result.weights, v))

    letter_heatmap(decoded_values)

    layers = [25, 15]
    autoencoder = Autoencoder(set_with_noise, training_set, layers, 2, 15, 0.001)
    result = autoencoder.train()

    decoded_values = []
    for v in set_with_noise:
        decoded_values.append(autoencoder.propagate(result.weights, v))

    letter_heatmap(decoded_values)

    layers = [10]
    autoencoder = Autoencoder(set_with_noise, training_set, layers, 2, 15, 0.001)
    result = autoencoder.train()

    decoded_values = []
    for v in set_with_noise:
        decoded_values.append(autoencoder.propagate(result.weights, v))

    letter_heatmap(decoded_values)
