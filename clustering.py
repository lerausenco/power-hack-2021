import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from tslearn.clustering import TimeSeriesKMeans

if __name__ == "__main__":
    dataframe = pd.read_pickle('powermeter_dataset')

    dataframe_subset = dataframe[0:10]
    x_train = dataframe_subset['volume'].to_numpy()

    # Collapse the data array from two one dimensional arrays into a single two dimensional array
    x_train = np.vstack(x_train)

    # Expand dimensions with empty last dimension as tslearn expects three dimensional input
    x_train = np.expand_dims(x_train, axis=-1)

    model = TimeSeriesKMeans(n_clusters=3, metric="dtw", max_iter=10)
    model.fit(x_train)
