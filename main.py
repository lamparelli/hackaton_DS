import pandas as pd
import numpy as np
import os

import manipolazione
import visualizzazione


stb_data = pd.read_csv("data" + os.sep + "datiOutput.csv", sep=",")
manipolazione.preparaDati(stb_data)
visualizzazione.mostraSampleDati(stb_data)
