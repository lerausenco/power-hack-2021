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
    dataframe_subset['volume'] = dataframe_subset['volume'].apply(lambda dictionary_list: np.array([dictionary['value'] for dictionary in dictionary_list]))
    x_train = dataframe_subset['volume'].to_numpy()

    # dataframe_subset['volume'] = dataframe_subset['volume'].apply(lambda dictionary_list: np.array([dictionary['value'] for dictionary in dictionary_list]))
    # dataframe.to_pickle('powermeter_dataset')

    model = TimeSeriesKMeans(n_clusters=3, metric="dtw", max_iter=10)
    model.fit(x_train)
