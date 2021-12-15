def getEventiCols(stb_data, getIdCols = False):
    cols = stb_data.columns
    if (getIdCols):
        return cols[cols.str.contains("err|warn|info|mac|time")]
    else:
        return cols[cols.str.contains("err|warn|info")]

def getEventiBackgroundCols(stb_data, getIdCols = False):
    cols = stb_data.columns
    if (getIdCols):
        return cols[~cols.str.contains("osm") & (cols.str.contains("err|warn|info|mac|time"))]
    else:
        return cols[~cols.str.contains("osm") & (cols.str.contains("err|warn|info"))]

def getEventiOsmCols(stb_data, getIdCols = False):
    cols = stb_data.columns
    if (getIdCols):
        return cols[cols.str.contains("osm|mac|time")]
    else:
        return cols[cols.str.contains("osm")]

def getStatiCols(stb_data, getIdCols = False):
    cols = stb_data.columns
    if (getIdCols):
        return cols[~cols.str.contains("err|warn|info") | cols.str.contains("mac|time")]
    else:
        return cols[~cols.str.contains("err|warn|info")]