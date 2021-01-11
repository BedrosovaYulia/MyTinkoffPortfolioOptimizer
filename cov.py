from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import tinkoff_data as td
import edhec_risk_kit as erk
import csv

l=[]
e = ["SRPT", "TSLA"]

pddf = td.getTinkoffLastYearPrices(l)
print(pddf.head())
pddf.index = pd.to_datetime(pddf.index).to_period('d')
pd.set_option("display.float_format", "{:.2f}".format)

cov = pddf.cov()
#print(cov)
cov.to_csv("cov.csv")

print(cov.idxmin().head())
#print(cov.min())
cov.idxmin().to_csv("cov_min.csv")
