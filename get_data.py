import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import keras
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import json
import requests

#get meter ids
def get_meterIDs():

    response = requests.get("https://power-hack.azurewebsites.net/Meteringpoint")
    json_data = json.loads(response.text)
    df = pd.DataFrame(json_data)

    ids = df.iloc[:, 0]
    return ids

def get_values(ids, start_date, end_date):

    vol_array = []

    for met_id in ids:

        get_string = "https://power-hack.azurewebsites.net/Volumes?Start=05%2F01%2F2019&End=10%2F01%2F2019&MeteringpointId=" + met_id
        response = requests.get(get_string)
        json_data = json.loads(response.text)
        df = pd.DataFrame(json_data)

        vol_values = np.array(df['value'])
        vol_array.append(vol_values)
    return np.hstack((vol_array, ids))

ids = get_meterIDs()
np.set_printoptions(precision=3)
print(get_values(ids[:10], 1, 0))

#print(get_meterIDs())
