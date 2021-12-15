def getEventiCols(stb_data):
    cols = stb_data.columns
    return cols[cols.str.contains("err|warn|info")]

def getEventiBackgroundCols(stb_data):
    cols = stb_data.columns
    return cols[~cols.str.contains("osm") & (cols.str.contains("err|warn|info"))]

def getEventiOsmCols(stb_data):
    cols = stb_data.columns
    return cols[cols.str.contains("osm")]

def getStatiCols(stb_data):
    cols = stb_data.columns
    return cols[~cols.str.contains("err|warn|info") & ~cols.str.contains("mac|time")]