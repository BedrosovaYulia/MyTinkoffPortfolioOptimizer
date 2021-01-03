import os
from openapi_client import openapi
from datetime import datetime, timedelta
from pytz import timezone
import pandas as pd
import numpy as np


token = os.getenv('TINVEST_TOKEN', '')
client = openapi.api_client(token)

def print_30d_operations():
    now = datetime.now(tz=timezone('Europe/Moscow'))
    yesterday = now - timedelta(days=30)
    ops = client.operations.operations_get(_from=yesterday.isoformat(), to=now.isoformat())
    return ops

def get_portfilio():
    prt=client.portfolio.portfolio_get()
    return prt

def get_market_names():
    names = client.market.market_stocks_get()
    return names

figi_name=dict()
name_figi=dict()
instruments = get_market_names()
#print(instruments.payload.instruments)
for instrument in instruments.payload.instruments:
    figi_name[instrument.figi]=instrument.name
    name_figi[instrument.name] = instrument.figi

#print(figi_name)
    
figi_in_prt=list()
prt=get_portfilio()
for pos in prt.payload.positions:
    figi_in_prt.append(pos.figi)

operations=print_30d_operations()

byfigi=dict()
for operation in operations.payload.operations:
    if operation.figi and operation.status == 'Done' and (operation.figi not in figi_in_prt):
        byfigi[operation.figi] = {
            "summ": 0, "currency": operation.currency, "name": figi_name[operation.figi]}
        
for  operation in operations.payload.operations:
    if operation.figi and operation.status == 'Done' and (operation.figi not in figi_in_prt):
        byfigi[operation.figi]["summ"] = byfigi[operation.figi]["summ"] + operation.payment
        
        
pddf = pd.DataFrame(byfigi)

print(pddf)
pddf.to_csv("income.csv")
