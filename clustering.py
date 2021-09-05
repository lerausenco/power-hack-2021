import matplotlib.pyplot as plt
import tensorflow as tf
import pandas as pd
import numpy as np

from tensorflow import keras
from tensorflow.keras import Model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout, RepeatVector, TimeDistributed
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans

np.random.seed(1)
tf.random.set_seed(1)


class AutoEncoder(Model):
    """
    A class that represents an autoencoder model.
    """

    def __init__(self, input_shape, encoder_layers, decoder_layers):
        # Prepares the model class variables
        super(AutoEncoder, self).__init__()

        # Generate the encoder model
        self.encoder_model = tf.keras.Sequential([
            *encoder_layers
        ], name="encoder")

        # Generate the decoder model
        self.decoder_model = tf.keras.Sequential([
            RepeatVector(input_shape[0], name="latent"),
            *decoder_layers,
            TimeDistributed(Dense(input_shape[1]))
        ], name="decoder")

        # Builds the subclass model
        self.build((None, *input_shape))

    def call(self, inputs, training=None, mask=None):
        latent_encoding = self.encoder_model(inputs)
        latent_decoding = self.decoder_model(latent_encoding)
        return latent_decoding

    def get_config(self):
        pass


if __name__ == "__main__":
    # Load the dataframe from file
    df = pd.read_pickle('meter_and_day_based_dataframe')

    # Shuffle the dataframe to a randomized order
    df = df.sample(frac=1)

    # Split dataset into test-train parts
    x_train, x_test = train_test_split(df, test_size=0.20, random_state=42)

    scaler = StandardScaler()
    scaler = scaler.fit(df.to_numpy())
    x_train = scaler.transform(x_train)
    x_test = scaler.transform(x_test)

    x_train = np.expand_dims(x_train, axis=-1)
    x_test = np.expand_dims(x_test, axis=-1)




    autoencoder = AutoEncoder(
        input_shape=(24, 1),
        encoder_layers=[
            keras.layers.LSTM(12, kernel_initializer='he_uniform', return_sequences=True, name='encoder_1'),
            keras.layers.LSTM(4, kernel_initializer='he_uniform', return_sequences=False, name='encoder_2')
        ],
        decoder_layers=[
            keras.layers.LSTM(4, kernel_initializer='he_uniform', return_sequences=True, name='decoder_1'),
            keras.layers.LSTM(12, kernel_initializer='he_uniform', return_sequences=True, name='decoder_2')
        ]
    )

    autoencoder.compile(loss="mse", optimizer='adam')
    print(autoencoder.summary())

    callback = keras.callbacks.EarlyStopping(monitor='val_loss', patience=3, mode='min')
    history = autoencoder.fit(x_train, x_train, epochs=10, batch_size=256, validation_split=0.1, callbacks=[callback], shuffle=False)

    plt.plot(history.history['loss'], label='Training loss')
    plt.plot(history.history['val_loss'], label='Validation loss')
    plt.legend()

    print("\nEvaluation: ")
    autoencoder.evaluate(x_test, x_test)




    # Extract latent vectors from 1000 different sequences to perform K-means clustering on
    visualization_sequences = x_test[0:1000]
    number_of_clusters = 2
    latent_vectors = autoencoder.encoder_model.predict(visualization_sequences)
    kmeans = KMeans(n_clusters=number_of_clusters)
    kmeans.fit(latent_vectors)




    # Perform TSNE to visualize clustering
    tsne = TSNE(n_components=2)
    point_list = tsne.fit_transform(latent_vectors)

    label_point_dictionary = dict({})
    for point, label in zip(point_list, kmeans.labels_):
        if label not in label_point_dictionary:
            label_point_dictionary[label] = []
        label_point_dictionary[label].append(point.tolist())

    figure, axes = plt.subplots()
    figure.suptitle('LATENT SPACE')
    for label, label_point_dictionary in label_point_dictionary.items():
        axes.scatter(*zip(*label_point_dictionary), label=label)
    axes.legend()
    plt.show()




    # Visualize the clustering
    median_sequences = {}
    for label in range(number_of_clusters):
        median_sequences[label] = []
    for sequence, label in zip(visualization_sequences, kmeans.labels_):
        median_sequences[label].append(sequence)
    for label in median_sequences.keys():
        figure = plt.figure()
        figure.suptitle('Label = {}'.format(label))
        plt.plot(np.median(np.stack(median_sequences[label]), axis=0))
        plt.show()
