def getEventCols(stb_data):
    cols = stb_data.columns
    return cols[(cols.str.contains("err") | cols.str.contains("info") | cols.str.contains("warn]"))]

def getNonOsmEventCols(stb_data):
    cols = stb_data.columns
    return cols[~cols.str.contains("osm") & (cols.str.contains("err") | cols.str.contains("info") | cols.str.contains("warn]"))]

def getOsmCols(stb_data):
    cols = stb_data.columns
    return cols[cols.str.contains("osm")]

def getStateCols(stb_data):
    cols = stb_data.columns
    return cols[~cols.str.contains("err") & ~cols.str.contains("info") & ~cols.str.contains("warn") & ~cols.contains("mac") & ~cols.contains("time")]