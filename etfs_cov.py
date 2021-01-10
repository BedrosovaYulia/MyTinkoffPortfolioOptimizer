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
print(cov)
cov.to_csv("etfs_cov.csv")

print(cov.idxmin())
print(cov.min())
cov.idxmin().to_csv("etfs_cov_min.csv")

#returns = pddf.pct_change()[1:]
#print(returns)
