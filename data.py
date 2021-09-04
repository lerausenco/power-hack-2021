import pandas as pd
import requests

METERPOINT_URL = "https://power-hack.azurewebsites.net/Meteringpoint"
VOLUME_URL = "https://power-hack.azurewebsites.net/Volumes"


def __get_meters():
    response_body = requests.get(METERPOINT_URL).json()

    return response_body


def __get_volumes(id, start_date="2019-04-01", end_date="2021-08-01"):
    request_body = {"MeteringpointId": id, "Start": start_date, "End": end_date}
    response_body = requests.get(VOLUME_URL, request_body).json()

    return response_body


def load_dataset():
    meter_information_dictionary = __get_meters()
    dataframe = pd.DataFrame(meter_information_dictionary)

    dataframe['volume'] = pd.Series(dtype=object)
    for index, row in dataframe.iterrows():
        dataframe.at[index, 'volume'] = __get_volumes(row['meteringpointId'])

    return dataframe


if __name__ == "__main__":
    dataframe = load_dataset()
