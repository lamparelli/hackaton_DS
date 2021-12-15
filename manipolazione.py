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

def fillValoriMancantiEventi(stb_data):
    eventCols = lettura_dati.getEventiCols(stb_data)
    for col in eventCols:
        stb_data[col].replace(np.nan, 0, inplace=True)

def eliminaOsmSuperflui(stb_data):
    stb_data.drop(columns = ["syst_info_osm_ottbuff"], inplace=True)

def eliminaEventiSecondari(stb_data):
    # il cliente ha suggerito di concentrarsi sugli eventi di tipo warn / err, e ignorare quelli info
    eventiBg = lettura_dati.getEventiBackgroundCols(stb_data)
    eventiBgDaDroppare = eventiBg[eventiBg.str.contains("info")]
    stb_data.drop(columns=eventiBgDaDroppare, inplace=True)

def eliminaSplitNonRichiesti(stb_data):
    # il cliente ha detto di lasciare, fra le colonne son split nel nome, solo aamp_abr_bw_split e ap_split
    cols = stb_data.columns
    colsDaEliminare = cols[(cols.str.contains("_split") & (~cols.str.contains("aamp_abr_bw_split") & (~cols.str.contains("ap_split"))))] 
    stb_data.drop(columns=colsDaEliminare, inplace=True) 

def eliminaColonneEventiMaiAvvenuti(stb_data):
    # da chiamare dopo il filtro che lascia solo le righe con almeno un OSM; 
    # rimuove le colonne di eventi (background) che non si verificano mai quando ci sono OSM
    colsDaRimuovere = []
    for col in lettura_dati.getEventiBackgroundCols(stb_data):
        if (stb_data[col].sum() == 0):
            colsDaRimuovere.append(col)
    stb_data.drop(columns=colsDaRimuovere, inplace=True)

def lasciaSoloOsmPrincipali(stb_data):
    osmPrincipali = ["syst_info_osm_bbdconnect_ott", "syst_info_osm_berr_atv", "syst_info_osm_contentnotfound", "syst_info_osm_ottbuffering", "syst_info_osm_techfaultott_atv"]
    osmCols = lettura_dati.getEventiOsmCols(stb_data)
    osmColsDaEliminare = osmCols.drop(osmPrincipali) # sono da eliminare tutte le osm, tranne le principali
    stb_data.drop(columns = osmColsDaEliminare, inplace=True)

def eliminaRigheSenzaOsm(stb_data):
    # In messaggi_presenti, c'è true nelle righe che hanno almeno un evento OSM, false altrimenti
    stb_data["messaggi_presenti"] = stb_data[lettura_dati.getEventiOsmCols(stb_data)].sum(axis=1) > 0
    stb_data.drop(stb_data[~stb_data["messaggi_presenti"]].index, inplace=True)

def eliminaRighe(stb_data):
    eliminaRigheSenzaOsm(stb_data)

def processaColonneSplit(stb_data):
    stb_data['aamp_abr_bw_split_nwbw'] = stb_data['aamp_abr_bw_split'].str.extract(r'NwBW=([0-9]+)', expand=True).astype(float)
    stb_data.drop(columns='aamp_abr_bw_split',inplace=True)

    stb_data['ap_split_rssi'] = stb_data['ap_split'].str.extract(r'rssi=(-?[0-9]+)', expand=True).astype(float)
    stb_data['ap_split_avgrssi']  = stb_data['ap_split'].str.extract(r'AvgRssi=(-?[0-9]+)', expand=True).astype(float)
    stb_data['ap_split_bandghz']  = stb_data['ap_split'].str.extract(r'Band=(2\.4GHz|2,4GHz|5GHz)', expand=True) 
    stb_data.drop(columns='ap_split',inplace=True) 

def processaColonneMem(stb_data):
    colsMem = ["mem_appsserviced", "mem_epg_ui", "mem_fogcli", 
    "mem_mediarite", "mem_netsrvmgr", "mem_rdkbrowser2", "mem_rmfstreamer", 
    "mem_skycobalt", "mem_subttxrend-app", "mem_tr69hostif", "mem_wpeframework", 
    "mem_wpenetworkprocess", "mem_wpeprocess", "mem_wpewebprocess", "mem_xcal-device"]

    for col in colsMem:
        stb_data[col] = stb_data[col].str.extract(r'^([0-9]+)m$', expand=True).astype(float)

def processColonnaCarico(stb_data):
    stb_data["load1"] = stb_data["load_average"].str.extract(r'^([0-9]+\.[0-9]+) [0-9]+\.[0-9]+ [0-9]+\.[0-9]+').astype(float)
    stb_data["load2"] = stb_data["load_average"].str.extract(r'^[0-9]+\.[0-9]+ ([0-9]+\.[0-9]+) [0-9]+\.[0-9]+').astype(float)
    stb_data["load3"] = stb_data["load_average"].str.extract(r'^[0-9]+\.[0-9]+ [0-9]+\.[0-9]+ ([0-9]+\.[0-9]+)').astype(float)
    
    stb_data["avg_load"] = stb_data[["load1", "load2", "load3"]].mean(axis=1)
    stb_data["max_load"] = stb_data[["load1", "load2", "load3"]].max(axis=1)
    stb_data.drop(columns=["load_average", "load1", "load2", "load3"], inplace=True)

def processaColonne(stb_data):
    #estraggo i valori di interesse da ogni colonna con dati innestati creando una nuova colonna per ogni dato
    processaColonneSplit(stb_data)
    processaColonneMem(stb_data)
    processColonnaCarico(stb_data)

def rimuoviDuplicati(stb_data):
    stb_data.drop_duplicates(inplace=True)

def preparaDati(stb_data):
    rinominaColonne(stb_data)
    eliminaSplitNonRichiesti(stb_data)
    processaColonne(stb_data)
    fillValoriMancantiEventi(stb_data)
    rimuoviDuplicati(stb_data)

def preparaDatiPerAnalisi(stb_data):
    preparaDati(stb_data)
    eliminaOsmSuperflui(stb_data)
    eliminaEventiSecondari(stb_data)
    eliminaColonneEventiMaiAvvenuti(stb_data)
    eliminaRighe(stb_data)

def preparaDatiPerReport(stb_data):
    preparaDati(stb_data)
