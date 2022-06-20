from autoencoder import Autoencoder
from fonts.fonts import Font3, font3_labels
from numpy import array
from utils import transform_input, letter_heatmap, latent_layer_plot

if __name__ == "__main__":
    training_set = transform_input(Font3)
    layers = [25, 15, 10]
    # autoencoder = Autoencoder(training_set, layers, 2, 50, 0.001)


    autoencoder = Autoencoder(training_set,training_set, layers, 2, 15, 0.001)
    result = autoencoder.train()
    decoded_values = []
    for val in training_set:
        decoded_values.append(autoencoder.propagate(result.weights, val))
    # letter_heatmap(decoded_values)

    latent_values = []
    for v in training_set:
        latent_values.append(autoencoder.encode(v, result.weights))

    latent_layer_plot(array(latent_values), font3_labels)
    direction = latent_values[4] - latent_values[2]

    parts = 5

    direction_latent_values = [latent_values[2]]
    direction_font_letters = [font3_labels[2]]

    proportion = direction / parts

    for i in range(1, parts):
        direction_latent_values.append(latent_values[2] + proportion * i)
        direction_font_letters.append('*')
    direction_latent_values.append(latent_values[4])
    direction_font_letters.append(font3_labels[4])

    latent_layer_plot(array(direction_latent_values), direction_font_letters)

    direction_letters = []
    for val in direction_latent_values:
        direction_letters.append(autoencoder.decode(val, result.weights))

    letter_heatmap(direction_letters)