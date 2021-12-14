import pandas as pd

def mostraSampleDati(stb_data, cols = None, numValoriSamplePerColonna = 10):
    # NB: NON mostra le prime N righe con nessuno valore NA.
    # I dati in ogni colonna sono slegati dai dati nelle altre colonne.
    # Mostra i primi N dati non-NA in ogni colonna.

    pd.set_option("max_columns", None)
    pd.set_option("max_rows", None)

    if (cols is None):
        cols = stb_data.columns

    vals = []
    for col in cols:
        sampleValoriColonna = stb_data[col].unique()[:numValoriSamplePerColonna]
        sampleValoriColonna = pd.Series(sampleValoriColonna).rename(col)
        vals.append(sampleValoriColonna)
    sample = pd.concat(vals, axis=1)
    return sample

def getDataframeConColonneOrdinate(stb_data):
    return stb_data.reindex(sorted(stb_data.columns), axis=1)