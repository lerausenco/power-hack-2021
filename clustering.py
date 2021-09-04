import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from tslearn.metrics import dtw
from tslearn.clustering import TimeSeriesKMeans

if __name__ == "__main__":
    dataframe = pd.read_pickle('powermeter_dataset')

    # volume_data_1 = np.array([dictionary['value'] for dictionary in dataframe.at[0, 'volume']])
    # plt.plot(volume_data_1[0:24])

    # volume_data_2 = np.array([dictionary['value'] for dictionary in dataframe.at[1, 'volume']])
    # plt.plot(volume_data_2[0:24])

    # dtw_score = dtw(volume_data_1, volume_data_2)

    dataframe_subset = dataframe[0:100]
    x_train = dataframe_subset['volume'].to_numpy()

    [len(data) for data in x_train]
    x_train.reshape((x_train.shape[0], 20470))

    model = TimeSeriesKMeans(n_clusters=3, metric="dtw", max_iter=10)
    model.fit(x_train)
