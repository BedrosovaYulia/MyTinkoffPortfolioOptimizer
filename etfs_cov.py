from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import tinkoff_data as td
import edhec_risk_kit as erk
import csv

l=[]
pddf = td.getTinkoffETFsLYPrices(l)
pddf.index = pd.to_datetime(pddf.index).to_period('d')

cov = pddf.cov()
print(cov)


#returns = pddf.pct_change()[1:]
#print(returns)
