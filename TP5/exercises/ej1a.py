from autoencoder import Autoencoder
from fonts.fonts import Font2, Font3, font3_labels
from utils import transform_input, print_bit_array, labeled_scatter, letter_heatmap
import numpy as np
from numpy import array




def ej1a():

    training_set = transform_input(Font3)
    letter_heatmap(training_set)

    layers = [25]
    autoencoder = Autoencoder(training_set, training_set,layers, 2, 130, 0.001)
    result = autoencoder.train()

    decoded_values = []
    for v in training_set:
        decoded_values.append(autoencoder.propagate(result.weights,v))


    letter_heatmap(decoded_values)
    # for r in range(len(decoded_values)):
    #     print_bit_array(decoded_values[r])
    #     print('\n\n')

    latent_values = []
    for val in training_set:
        latent_values.append(autoencoder.encode(val, result.weights))

    print(latent_values)
    x_values = []
    y_values = []
    for i in range(len(latent_values)):
        x_values.append(latent_values[i][0])
        y_values.append(latent_values[i][1])

    labeled_scatter(x_values,y_values,labels=font3_labels)



if __name__ == '__main__':
    ej1a()

