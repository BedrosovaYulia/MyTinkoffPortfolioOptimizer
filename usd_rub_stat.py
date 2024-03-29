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
    yesterday = now - timedelta(days=360)
    ops = client.operations.operations_get(_from=yesterday.isoformat(), to=now.isoformat())
    return ops

def get_portfilio():
    prt=client.portfolio.portfolio_get()
    return prt

def get_market_names():
    names = client.market.market_stocks_get()
    return names


def get_market_bonds():
    names = client.market.market_bonds_get()
    return names


def get_market_etfs():
    names = client.market.market_etfs_get()
    return names


figi_name=dict()
name_figi=dict()
instruments = get_market_names().payload.instruments + \
    get_market_bonds().payload.instruments + get_market_etfs().payload.instruments
for instrument in instruments:
    figi_name[instrument.figi]=instrument.name
    name_figi[instrument.name] = instrument.figi

    
figi_in_prt=list()
figi_cost=dict()
sum_usd=0
freeusd=0
#usdru=0
prt=get_portfilio()
for pos in prt.payload.positions:
    #print(pos)
    if pos.average_position_price.currency == 'USD':
        print(pos.name, pos.balance*pos.average_position_price.value)
        figi_in_prt.append(pos.figi)
        figi_cost[pos.figi] = pos.balance*pos.average_position_price.value
        sum_usd = sum_usd+figi_cost[pos.figi]
    elif pos.figi == 'BBG0013HGFT4':
        #print(pos.balance)
        freeusd=pos.balance
        #usdru = pos.average_position_price.value

print("USD in instruments: ", sum_usd)
print("free USD: ", freeusd)
print("total USD: ", sum_usd+freeusd)


operations=print_30d_operations()

byfigi=dict()
byfigiusd = dict()
for operation in operations.payload.operations:
    if operation.figi and operation.status == 'Done' and operation.figi == "BBG0013HGFT4":
        startsum=0
        try:
            startsum = figi_cost[operation.figi]
        except:
            pass
        fgname = ""
        try:
            fgname = figi_name[operation.figi]
        except:
            pass
        if operation.currency =="RUB":
            byfigi[operation.figi] = {
                "summ": startsum, "currency": operation.currency, "name": fgname}
        
            
total_usd_b = 0
total_spend_b=0

total_usd_s = 0
total_spend_s = 0

for  operation in operations.payload.operations:
    if operation.figi and operation.status == 'Done' and operation.figi == "BBG0013HGFT4":
        #print(operation)
                
        if operation.operation_type == "Sell":
            total_usd_s = total_usd_s-operation.quantity
            total_spend_s = total_spend_s + operation.payment
        
        if operation.operation_type == "Buy":
            total_usd_b = total_usd_b+operation.quantity
            total_spend_b = total_spend_b + operation.payment

average_b = total_spend_b/total_usd_b
print("Buy: ",total_usd_b, total_spend_b, average_b)

average_s = total_spend_s/total_usd_s
print("Sell: ", total_usd_s, total_spend_s, average_s)

total_comission = (total_spend_s-total_spend_b)*0.0005
print("Total comission: ",total_comission)

profit = abs(total_usd_b*average_s)-abs(total_usd_b*average_b)-total_comission
print("Total profit: ", profit)
