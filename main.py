import pandas as pd
import numpy as np
import os


def preparaDati(stb_data):
    stb_data = pd.read_csv("data" + os.sep + "datiOutput.csv", sep=",")

    # levo colonna vuota iniziale con id
    stb_data.rename(columns={stb_data.columns[0]: "ID"}, inplace=True)
    stb_data.drop(columns="ID", inplace=True)
    return stb_data


stb_data = pd.read_csv("data" + os.sep + "datiOutput.csv", sep=",")
stb_data = preparaDati(stb_data)
print(stb_data)
