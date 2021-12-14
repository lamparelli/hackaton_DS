def getEventiCols(stb_data):
    cols = stb_data.columns
    return cols[(cols.str.contains("err") | cols.str.contains("info") | cols.str.contains("warn]"))]

def getEventiBackgroundCols(stb_data):
    cols = stb_data.columns
    return cols[~cols.str.contains("osm") & (cols.str.contains("err") | cols.str.contains("info") | cols.str.contains("warn]"))]

def getEventiOsmCols(stb_data):
    cols = stb_data.columns
    return cols[cols.str.contains("osm")]

def getStatiCols(stb_data):
    cols = stb_data.columns
    return cols[~cols.str.contains("err") & ~cols.str.contains("info") & ~cols.str.contains("warn") & ~cols.contains("mac") & ~cols.contains("time")]