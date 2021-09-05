import pandas as pd
import numpy as np
import requests
from pathlib import Path

METERPOINT_URL = "https://power-hack.azurewebsites.net/Meteringpoint"
VOLUME_URL = "https://power-hack.azurewebsites.net/Volumes"
STANDARD_VOLUME_LIST_LENGTH = 20470


def __get_meters():
    response_body = requests.get(METERPOINT_URL).json()

    return response_body


def __get_consumption(id, start_date="2019-04-01", end_date="2021-08-01"):
    request_body = {"MeteringpointId": id, "Start": start_date, "End": end_date}
    response_body = requests.get(VOLUME_URL, request_body).json()

    # Attempt to interpolate the dataframe
    df = pd.DataFrame(response_body)
    df['measurementTime'] = pd.to_datetime((df['measurementTime']), yearfirst=True, format="%Y-%m-%d %H")
    df.set_index('measurementTime', inplace=True)
    df = df.resample(rule='H').ffill().reset_index()

    # Create a new series based around the timestamp
    series = pd.Series(df['value'].tolist())
    index_ = df['measurementTime'].tolist()
    series.index = index_

    return series


def __download_raw_powermeter_dataframe():
    meter_information_dictionary = __get_meters()

    df = pd.DataFrame(meter_information_dictionary)
    df['series'] = pd.Series(dtype=object)
    for index, row in df.iterrows():
        print("Loading index {current} out of {total}".format(current=index, total=len(df.index)))
        df.at[index, 'series'] = __get_consumption(row['meteringpointId'], start_date='2020-01-01', end_date='2021-01-01')

    return df


def generate_raw_powermeter_dataframe_file():
    df = __download_raw_powermeter_dataframe()
    df.to_pickle('raw_powermeter_dataframe')


def generate_meter_and_day_based_dataframe_file():
    powermeter_df = pd.read_pickle('raw_powermeter_dataframe')

    # Dictionary to insert the data in the meter & day format
    meter_and_day_based_dictionary = {}
    for index, row in powermeter_df.iterrows():
        print("Working on row index {current} out of {total}".format(current=index, total=len(powermeter_df.index)))

        # Extracts all of the unique dates (yyyy-mm-dd)
        unique_datetime_list = np.unique(row['series'].index.date).tolist()

        for datetime in unique_datetime_list:
            # Finds all in the series with the given date (yyyy-mm-dd) in their string
            filtered_series = row['series'][row['series'].index.date == datetime]

            # Inserts the specific meters day based hourly values into the dictionary
            # (But only if we actually have 24 hours worth of data!)
            if len(filtered_series) == 24:
                meter_and_day_based_dictionary[(row['meteringpointId'], datetime.__str__())] = filtered_series.to_numpy()

    # Constructs the new dataframe and saves it to file
    day_based_dataframe = pd.DataFrame.from_dict(meter_and_day_based_dictionary, orient='index')
    day_based_dataframe.to_pickle('meter_and_day_based_dataframe')


if __name__ == "__main__":
    if not Path("raw_powermeter_dataframe").is_file():
        print("Raw powermeter dataframe file does not exist, beginning to download data")
        generate_raw_powermeter_dataframe_file()

    print("Generating meter and day based dataframe file from raw powermeter dataframe file")
    generate_meter_and_day_based_dataframe_file()
