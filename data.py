import pandas as pd
import numpy as np
import requests

METERPOINT_URL = "https://power-hack.azurewebsites.net/Meteringpoint"
VOLUME_URL = "https://power-hack.azurewebsites.net/Volumes"


def __get_meters():
    response_body = requests.get(METERPOINT_URL).json()

    return response_body


def __get_volumes_and_dates(id, start_date="2019-04-01", end_date="2021-08-01"):
    request_body = {"MeteringpointId": id, "Start": start_date, "End": end_date}
    response_body = requests.get(VOLUME_URL, request_body).json()

    volumes_df = pd.DataFrame(response_body)
    volumes_df['measurementTime'] = pd.to_datetime((volumes_df['measurementTime']), yearfirst=True, format="%Y-%m-%d %H")
    volumes_df.set_index('measurementTime', inplace=True)
    volumes_df = volumes_df.resample(rule='H').ffill().reset_index()

    volumes = volumes_df['value'].to_numpy()
    timestamps = volumes_df['measurementTime'].to_numpy()
    datetimes = np.vectorize(lambda timestamp: timestamp.to_pydatetime())(timestamps)

    return volumes, datetimes


def load_dataframe_from_api_to_file():
    meter_information_dictionary = __get_meters()
    dataframe = pd.DataFrame(meter_information_dictionary)
    dataframe['volume'] = pd.Series(dtype=object)

    for index, row in dataframe.iterrows():
        print("Loading index {current} out of {total}. Retrieving volume for meter with identity = {id}".format(current=index, total=len(dataframe.index), id=row['meteringpointId']))
        volume_array, date_array = __get_volumes_and_dates(row['meteringpointId'])
        dataframe.at[index, 'volume'] = volume_array
        dataframe.at[index, 'date'] = date_array

    dataframe.to_pickle('powermeter_dataset')


if __name__ == "__main__":
    load_dataframe_from_api_to_file()
