import pandas as pd
import numpy as np
from multiprocessing import Pool
from tslearn.clustering import TimeSeriesKMeans


def main():
    # volume_data = get_volume_data(year=2020)
    # clustering_by_months = cluster_months(volume_data)
    # np.savetxt("clustering_by_months.txt", X=clustering_by_months)
    clustering_by_months = np.loadtxt("clustering_by_months.txt").T
    np.savetxt("monthly_clustering_by_id.txt", X=clustering_by_months)
    clustering_by_year = cluster_time_series_KMeans(clustering_by_months)
    np.savetxt("clustering_by_year.txt", X=clustering_by_year)


def get_volume_data(year):
    data = pd.read_pickle('powermeter_dataset')
    volume_data = []
    index = 0

    for row in data.itertuples():
        currentMonth = 0
        volume_data.append([])
        for entry, volume in enumerate(row.volume):
            if year == row.date[entry].year:
                if currentMonth < row.date[entry].month:
                    currentMonth = row.date[entry].month
                    volume_data[index].append([])

                volume_data[index][currentMonth - 1].append(volume)
        # Done this way because DataFrame skips some rows
        index += 1

    return volume_data


def cluster_months(volume_data):
    monthly_volumes = []
    pool = Pool(processes=12)
    for month in range(12):
        monthly_volumes.append([volumes[month] for volumes in volume_data])

    return pool.map(cluster_time_series_KMeans, monthly_volumes)


def cluster_time_series_KMeans(data):
    x_train = np.vstack(data)
    x_train = np.expand_dims(x_train, axis=-1)
    model = TimeSeriesKMeans(metric="dtw", n_jobs=-1)

    return model.fit_predict(x_train)


if __name__ == "__main__":
    main()
