import manipolazione
import lettura_dati
import pandas as pd
import pandas_profiling as pf
import os

# Impostare a True i report che si vogliono generare
printReportEventi = True
printReportStati = False

stb_data = pd.read_csv("data" + os.sep + "datiInput.csv")
manipolazione.preparaDatiPerReport(stb_data)

pd.options.display.width = 0
pd.options.display.max_rows = 10000
pd.options.display.max_info_columns = 10000

if (printReportEventi):
    stb_data = stb_data[lettura_dati.getEventiCols(stb_data, True)]
    profile = pf.ProfileReport(stb_data)
    profile.to_file("outputEventi.html")

if (printReportStati):
    stb_data = stb_data[lettura_dati.getStatiCols(stb_data, True)]
    profile = pf.ProfileReport(stb_data)
    profile.to_file("outputStati.html")
