import pandas as pd
import lettura_dati
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

def getDatiEventiWideToLong(stb_data):
    stb_data2 = stb_data.copy()
    stb_data2["id"] = stb_data["mac"] + "_" + stb_data["time"]
    stb_data_long = pd.melt(stb_data2, id_vars="id", value_vars=lettura_dati.getEventiCols(stb_data2))
    stb_data_long.rename(columns={"variable": "event", "value": "event_count"}, inplace=True)
    return stb_data_long

def getDatiBasket(stb_data):
    stb_data_long = getDatiEventiWideToLong(stb_data)
    basket = pd.pivot_table(data=stb_data_long, index='id',columns='event',values='event_count', aggfunc='sum',fill_value=0)
    return basket

def convertiDatiBasketInInfoPresenza(datoBasket):
    if datoBasket > 0:
        return 1
    else:
        return 0

def convertiFormatoDati(regoleAssociative):
    regoleAssociative["antecedents"] = regoleAssociative["antecedents"].astype(str).str.extract(r'\(\{\'(.+)\'\}\)')
    regoleAssociative["consequents"] = regoleAssociative["consequents"].astype(str).str.extract(r'\(\{\'(.+)\'\}\)')

def getCausaliOsm(stb_data):
    datiBasket = getDatiBasket(stb_data)
    datiPresenza = datiBasket.applymap(convertiDatiBasketInInfoPresenza)
    setFrequenti = apriori(datiPresenza, min_support=0.05, use_colnames=True)
    regoleAssociative = association_rules(setFrequenti, metric="lift", min_threshold=2)
    convertiFormatoDati(regoleAssociative)
    return regoleAssociative.sort_values("lift", ascending=False)


