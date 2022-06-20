from keras.layers import Input, Dense, Lambda
from keras import backend as K
from keras import metrics
from keras.models import Model
import tensorflow as tf
from tensorflow.python.framework.ops import disable_eager_execution

disable_eager_execution()
class VAE:
    def __init__(self, x, y, hidden_layers, latent_layer):
        self.latent_neurons = latent_layer
        self.hidden_layers = hidden_layers
        self.dim = len(x[0])

        #setting of VAE
        x = Input(shape=(self.dim), name="input")
        self.encoder = self.set_encoder(x)
        self.encoder.summary()
        self.decoder = self.set_decoder()
        self.decoder.summary()
        # grab the output. Recall, that we need to grab the 3rd element our sampling z
        output_combined = self.decoder(self.encoder(x)[2])
        # link the input and the overall output
        self.model = Model(x, output_combined)
        # print out what the overall model looks like
        self.model.summary()
        self.model.compile(loss=self.vae_loss)


    def set_encoder(self,x):
        h = None
        if(len(self.hidden_layers) != 0):
            aux_h = x
            for (i,neurons) in enumerate(self.hidden_layers[:-1]):
                h = Dense(neurons, name="encoding_{0}".format(i))(aux_h)
                aux_h = h
            h = Dense(self.hidden_layers[-1], activation="relu",
                      name="encoding_{0}".format(len(self.hidden_layers) - 1))(aux_h)
        self.z_mean = Dense(self.latent_neurons, name="mean")(h)
        self.z_log_var = Dense(self.latent_neurons, name="log-variance")(h)

        z = Lambda(self.sampling, output_shape=(self.latent_neurons))([self.z_mean, self.z_log_var])
        encoder = Model(x, [self.z_mean, self.z_log_var, z], name="encoder")
        return encoder

    def set_decoder(self):
        # Input to the decoder
        input_decoder = Input(shape=(self.latent_neurons,), name="decoder_input")
        reversed_layers = self.hidden_layers.copy()
        reversed_layers.reverse()
        h = None
        if (len(self.hidden_layers) != 0):
            aux_h = input_decoder
            for (i,neurons) in enumerate(reversed_layers[:-1]):
                h = Dense(neurons, name="encoding_{0}".format(i))(aux_h)
                aux_h = h
            h = Dense(reversed_layers[-1], activation="relu", name="encoding_{0}".format(len(self.hidden_layers) - 1))(aux_h)

        # getting the mean from the original dimension
        x_decoded = Dense(self.dim, activation='sigmoid', name="flat_decoded")(h)
        # defining the decoder as a keras model
        decoder = Model(input_decoder, x_decoded, name="decoder")
        return decoder

    def sampling(self, args: tuple):
        # we grab the variables from the tuple
        z_mean, z_log_var = args
        print(z_mean)
        print(z_log_var)
        epsilon = K.random_normal(shape=(K.shape(z_mean)[0], self.latent_neurons), mean=0.,
                                  stddev=1.0)
        return z_mean + K.exp(z_log_var / 2) * epsilon  # h(z)

    def vae_loss(self, x: tf.Tensor, x_decoded_mean: tf.Tensor):
        xent_loss = self.dim * metrics.binary_crossentropy(x, x_decoded_mean)
        kl_loss = -0.5 * K.sum(1 + self.z_log_var - K.square(self.z_mean) - K.exp(self.z_log_var), axis=-1)
        vae_loss = K.mean(xent_loss + kl_loss)
        return vae_loss

    def train(self, training_set, epochs, batch_size):
        self.model.fit(training_set, training_set, epochs=epochs, batch_size=batch_size, validation_data=(training_set, training_set))
