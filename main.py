import pandas as pd
import os

import manipolazione
import inferenza

stb_data = pd.read_csv("data" + os.sep + "datiInput.csv", sep=",")
manipolazione.preparaDatiPerAnalisi(stb_data)
regoleAssociative = inferenza.getCausaliOsm(stb_data)
datiDeterminanti = inferenza.getDeterminantiOsmPrincipali(stb_data)

stb_data.to_csv("data" + os.sep + "datiOutputPuliti.csv")
regoleAssociative.to_csv("data" + os.sep + "dati_mba_v3.csv")
datiDeterminanti.to_csv("data" + os.sep + "datiDeterminanti_v2.csv")
