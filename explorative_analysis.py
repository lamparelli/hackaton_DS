import pandas as pd
import pandas_profiling as pf



pd.options.display.width = 0
pd.options.display.max_rows = 10000
pd.options.display.max_info_columns = 10000
profile = pf.ProfileReport(df, correlations={'phi_k':{'calculate': False}})
profile.to_file("output.html")