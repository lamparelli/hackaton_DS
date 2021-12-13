import pandas as pd

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

def eliminaColonne(stb_data):
    pd.set_option("max_rows", None)
    cols = pd.Series(stb_data.columns)
    #tutte le colonne da eliminare in quanto hanno _split
    colsDaEliminare = cols[(cols.str.contains("_split") & (~cols.str.contains("aamp_abr_bw_split") & (~cols.str.contains("ap_info_split"))))] 
    #elimino le colonne
    stb_data.drop(columns=colsDaEliminare, inplace=True) 

def preparaDati(stb_data):
    rinominaColonne(stb_data)
    eliminaColonne(stb_data)
    manipolaColonne(stb_data)