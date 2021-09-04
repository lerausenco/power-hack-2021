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

    volumes_df = pd.DataFrame(response_body)
    volumes_df['measurementTime'] = pd.to_datetime((volumes_df['measurementTime']),
                                                   yearfirst=True,
                                                   format="%Y-%m-%d %H")

    volumes_df.set_index('measurementTime', inplace=True)
    volumes_df = volumes_df.resample(rule='H').ffill().reset_index()
    #print("Length: ", len(volumes_df))

    return response_body


def load_dataframe_from_api_to_file():
    meter_information_dictionary = __get_meters()
    dataframe = pd.DataFrame(meter_information_dictionary)
    dataframe['volume'] = pd.Series(dtype=object)

    for index, row in dataframe.iterrows():
        print("Loading index {current} out of {total}. Retrieving volume for meter with identity = {id}"
              .format(current=index, total=len(dataframe.index), id=row['meteringpointId']))
        dataframe.at[index, 'volume'] = __get_volumes(row['meteringpointId'])

    dataframe.to_pickle('powermeter_dataset')


if __name__ == "__main__":
    load_dataframe_from_api_to_file()
