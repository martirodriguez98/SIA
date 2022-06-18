from autoencoder import Autoencoder
from fonts.fonts import Font2, Font3, font3_labels
from utils import transform_input, print_bit_array, labeled_scatter
import numpy as np




def ej1a():

    training_set = transform_input(Font3)

    layers = [15, 10, 7]
    autoencoder = Autoencoder(training_set, layers, 2, 1, 0.001)
    result, latent_space = autoencoder.train()
    print(result)
    for r in range(len(result)):
        print_bit_array(result[r])
        print('\n\n')

    print(latent_space)
    print(len(latent_space[:,0]))
    print(len(latent_space[:, 1]))
    start = 0
    count=26
    labeled_scatter(latent_space[:,0],latent_space[:,1],labels=font3_labels[start:start+count])



if __name__ == '__main__':
    ej1a()

