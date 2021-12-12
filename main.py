import pandas as pd
import numpy as np
import os


def rinominaColonne(stb_data):
    # levo colonna vuota iniziale con id
    stb_data.rename(columns={stb_data.columns[0]: "ID"}, inplace=True)
    stb_data.drop(columns="ID", inplace=True)

    # rinomino time
    stb_data.rename(columns={"_time": "time"}, inplace=True)

    # rendo lowercase nomi colonne
    stb_data.columns = stb_data.columns.str.lower()


def manipolaColonne(stb_data):
    print("todo, manipolazione colonne")


def preparaDati(stb_data):
    rinominaColonne(stb_data)
    manipolaColonne(stb_data)


stb_data = pd.read_csv("data" + os.sep + "datiOutput.csv", sep=",")
preparaDati(stb_data)
print(stb_data)
