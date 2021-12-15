import manipolazione
import pandas as pd
import pandas_profiling as pf
import os

stb_data = pd.read_csv("data" + os.sep + "datiOutput.csv")
#manipolazione.preparaDatiPerReportStati(stb_data)
manipolazione.preparaDatiPerReportEventi(stb_data)

pd.options.display.width = 0
pd.options.display.max_rows = 10000
pd.options.display.max_info_columns = 10000
profile = pf.ProfileReport(stb_data)
profile.to_file("outputEventi.html")

