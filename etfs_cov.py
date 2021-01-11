from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import tinkoff_data as td
import edhec_risk_kit as erk
import csv

#l=[]
l=["TIPO", "TGLD", "TUSD", "TSPX", "TBIO", "TECH"]

pddf = td.getTinkoffETFsLYPrices(l)
pddf.index = pd.to_datetime(pddf.index).to_period('d')
pd.set_option("display.float_format", "{:.2f}".format)

cov = pddf.cov()
#print(cov)
cov.to_csv("etfs_cov.csv")

print(cov.idxmin())
#print(cov.min())
cov.idxmin().to_csv("etfs_cov_min.csv")

returns = pddf.pct_change()[1:]
#print(returns.head())
#print(returns.shape)

valotil = erk.annualize_vol(returns, returns.shape[0])
a_rets = erk.annualize_rets(returns, returns.shape[0])
sharp_r = erk.sharpe_ratio(returns, 0.03, returns.shape[0])

result = pd.DataFrame(dict(
    vol=valotil*100,
    rets=a_rets*100,
    sharp=sharp_r*100
)).reset_index()

pd.set_option("display.float_format", "{:.2f}".format)

print(result.sort_values(by="sharp", ascending=False).head(20))