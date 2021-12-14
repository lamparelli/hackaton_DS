import collections
import pandas as pd
import numpy as np
import lettura_dati

def rinominaColonne(stb_data):
    # rendo lowercase nomi colonne
    stb_data.columns = stb_data.columns.str.lower()

    # levo colonna vuota iniziale con id
    stb_data.rename(columns={stb_data.columns[0]: "ID"}, inplace=True)
    stb_data.drop(columns="ID", inplace=True)

    # rinomino time
    stb_data.rename(columns={"_time": "time"}, inplace=True)

    # rinomino ap_info_split; tutte le colonne evento (info/warn/err) devono essere counter; ap_info_split contiene dati
    stb_data.rename(columns={"ap_info_split": "ap_split"}, inplace=True)

def gestioneValoriMancanti(stb_data):
    eventCols = lettura_dati.getEventiCols(stb_data)
    for col in eventCols:
        stb_data[col].replace(np.nan, 0, inplace=True)

def eliminaOsmSecondari(stb_data):
    # il cliente ha detto di concentrarsi su queste colonne osm; sono secondarie le altre
    osmPrincipali = ["syst_info_osm_bbdconnect_ott", "syst_info_osm_berr_atv", "syst_info_osm_contentnotfound", "syst_info_osm_ottbuffering", "syst_info_osm_techfaultott_atv"]
    osmCols = lettura_dati.getEventiOsmCols(stb_data)
    osmColsDaEliminare = osmCols.drop(osmPrincipali) # sono da eliminare tutte le osm, tranne le principali
    stb_data.drop(columns = osmColsDaEliminare, inplace=True)

def eliminaEventiSecondari(stb_data):
    # il cliente ha suggerito di concentrarsi sugli eventi di tipo warn / err, e ignorare quelli info
    eventiBg = lettura_dati.getEventiBackgroundCols(stb_data)
    eventiBgDaDroppare = eventiBg[eventiBg.str.contains("info")]
    stb_data.drop(columns=eventiBgDaDroppare, inplace=True)

def eliminaColonne(stb_data):
    cols = pd.Series(stb_data.columns)

    # il cliente ha detto di lasciare, fra le colonne son split nel nome, solo aamp_abr_bw_split e ap_split
    colsDaEliminare = cols[(cols.str.contains("_split") & (~cols.str.contains("aamp_abr_bw_split") & (~cols.str.contains("ap_split"))))] 
    stb_data.drop(columns=colsDaEliminare, inplace=True) 

    # da valutare se filtrare o meno i dati secondari
    # eliminaOsmSecondari(stb_data)
    # eliminaEventiSecondari(stb_data)

def eliminaRigheSenzaOsm(stb_data):
    # In messaggi_presenti, c'è true nelle righe che hanno almeno un evento OSM, false altrimenti
    stb_data["messaggi_presenti"] = stb_data[lettura_dati.getEventiOsmCols(stb_data)].sum(axis=1) > 0
    stb_data.drop(stb_data[stb_data["messaggi_presenti"]].index, inplace=True)

def eliminaRighe(stb_data):
    eliminaRigheSenzaOsm(stb_data)

def processaColonneSplit(stb_data):
    stb_data['aamp_abr_bw_split_nwbw'] = stb_data['aamp_abr_bw_split'].str.extract(r'NwBW=([0-9]+)', expand=True)
    stb_data.drop(columns='aamp_abr_bw_split',inplace=True)

    stb_data['ap_split_rssi'] = stb_data['ap_split'].str.extract(r'rssi=(-?[0-9]+)', expand=True) 
    stb_data['ap_split_avgrssi']  = stb_data['ap_split'].str.extract(r'AvgRssi=(-?[0-9]+)', expand=True) 
    stb_data['ap_split_bandghz']  = stb_data['ap_split'].str.extract(r'Band=(2\.4|2,4|5)GHz', expand=True) 
    stb_data.drop(columns='ap_split',inplace=True) 

def processaColonneMem(stb_data):
    colsMem = ["mem_appsserviced", "mem_epg_ui", "mem_fogcli", 
    "mem_mediarite", "mem_netsrvmgr", "mem_rdkbrowser2", "mem_rmfstreamer", 
    "mem_skycobalt", "mem_subttxrend-app", "mem_tr69hostif", "mem_wpeframework", 
    "mem_wpenetworkprocess", "mem_wpeprocess", "mem_wpewebprocess", "mem_xcal-device"]

    for col in colsMem:
        stb_data[col] = stb_data[col].str.extract(r'^([0-9]+)m$', expand=True).astype(float)

def processaColonne(stb_data):
    #estraggo i valori di interesse da ogni colonna con dati innestati creando una nuova colonna per ogni dato
    processaColonneSplit(stb_data)
    processaColonneMem(stb_data)

def preparaDatiPerAnalisi(stb_data):
    rinominaColonne(stb_data)
    eliminaColonne(stb_data)
    eliminaRighe(stb_data)
    processaColonne(stb_data)
    gestioneValoriMancanti(stb_data)