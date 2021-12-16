import pandas as pd
import lettura_dati
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

minSupport = 0.005
minLift = 2

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
    # normalmente sono stringhe in formato frozenset, nelle quali non si può fare str.contains
    regoleAssociative["antecedents"] = regoleAssociative["antecedents"].astype(str).str.extract(r'\(\{(.+)\}\)')[0].str.replace("'", "").str.replace(", ", ",")
    regoleAssociative["consequents"] = regoleAssociative["consequents"].astype(str).str.extract(r'\(\{(.+)\}\)')[0].str.replace("'", "").str.replace(", ", ",")

def filtraOsmInConseguenze(regoleAssociative):
    return regoleAssociative[regoleAssociative["consequents"].str.contains("osm")]

def filtraOsmPrincipaliInConseguenze(regoleAssociative):
    osmPrincipali = ["syst_info_osm_bbdconnect_ott", "syst_info_osm_berr_atv", "syst_info_osm_contentnotfound", 
    "syst_info_osm_ottbuffering", "syst_info_osm_techfaultott_atv"]
    return regoleAssociative[regoleAssociative["consequents"].str.contains("|".join(osmPrincipali))]

def filtraRegole(regoleAssociative):
    # mantengo solo le regole che hanno come conseguenza associativa un osm
    return filtraOsmPrincipaliInConseguenze(regoleAssociative)

def getCausaliOsm(stb_data, support = None, lift = None):
    chosenSupport = minSupport
    chosenLift = minLift
    if (support is not None):
        chosenSupport = support
    if (lift is not None):
        chosenLift = lift

    datiBasket = getDatiBasket(stb_data)
    datiPresenza = datiBasket.applymap(convertiDatiBasketInInfoPresenza)
    setFrequenti = apriori(datiPresenza, min_support=chosenSupport, use_colnames=True)
    regoleAssociative = association_rules(setFrequenti, metric="lift", min_threshold=chosenLift)
    convertiFormatoDati(regoleAssociative)
    regoleAssociative = filtraRegole(regoleAssociative)
    return regoleAssociative.sort_values("lift", ascending=False)

def getDeterminantiDiUnOsm(regole, osm):
    regoleConOsmInConseguenti = regole[regole["consequents"].str.contains(osm)]
    gruppiAntecedentiDellOsm = regoleConOsmInConseguenti["antecedents"].str.split(",")

    determinanti = []

    for gruppoAntecedenti in gruppiAntecedentiDellOsm:
        for antecedente in gruppoAntecedenti:
            determinanti.append(antecedente)

    determinantiUnivoci = list(set(determinanti)) # rimuovo i duplicati
    dati = pd.DataFrame({"determinanti": determinantiUnivoci})
    dati["osm"] = osm
    return dati

def getDeterminantiOsmPrincipali(regole):
    osmPrincipali = ["syst_info_osm_bbdconnect_ott", "syst_info_osm_berr_atv", 
        "syst_info_osm_contentnotfound", "syst_info_osm_ottbuffering", "syst_info_osm_techfaultott_atv"]
    
    listeDeterminantiOsm = []
    for osm in osmPrincipali:
        determinantiOsm = getDeterminantiDiUnOsm(regole, osm)
        listeDeterminantiOsm.append(determinantiOsm)

    datiDeterminanti = pd.concat(listeDeterminantiOsm)
    return datiDeterminanti

def getDeterminantiProfilingPrincipali():
    # variabili di stato ad alta correlazione per ogni OSM principale trovate in pandas profiling
    return {
        "syst_info_osm_ottbuffering": 
            ["test_policyfail", "syst_info_osm_techfaultott_atv", "syst_info_osm_berr_atv"],
        "syst_info_osm_techfaultott_atv":
            ["syst_info_osm_ottbuffering"],
        "syst_info_osm_berr_atv":
            ["mem_wpenetworkprocess", "mem_wpewebprocess", "mem_rdkbrowser2", 
            "test_policyfail", "syst_info_osm_ottbuffering", "test_ipnotset", "aamp_abr_bw_split_nwbw"],
        "syst_info_osm_bbdconnect_ott":
            ["mem_wpenetworkprocess", "mem_wpewebprocess", "mem_rdkbrowser2", "rdk-10039",
            "mem_mediarite", "mem_tr69hostif", "test_ipnotset"],
        "syst_info_osm_contentnotfound":
            ["mem_wpenetworkprocess", "mem_wpewebprocess", "mem_rdkbrowser2", 
            "aamp_keystatus_spilt", "test_dns_fileempty", 
            "cpu_mediarite", "cpu_epg_ui", "cpu_tr69hostif", "test_bitratechange"
            ]
    }
