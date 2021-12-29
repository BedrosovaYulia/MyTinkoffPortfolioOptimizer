import os
from datetime import datetime, timedelta
from typing import Any, List, Tuple
import pandas as pd
import edhec_risk_kit as erk
from openapi_client import openapi
from pytz import timezone


class HTTPError(Exception):
    pass

token = os.getenv('TINVEST_TOKEN', '')
client = openapi.api_client(token)

def get_market_names():
    names = client.market.market_stocks_get()
    return names

def main():

    markets = get_market_names().payload.instruments

    #l = ["ATVI", "KO", "INTC", "LPL", "MAT"]

    #l = ["SBER", "TATN", "PHOR", "CHMF", "MGNT", "GCHE", "GAZP", "LKOH", "ROSN"]

    l = ["GRNT", "UWGN", "MSST", "ETLN", "RUGR", "MTLR", "APTK", "RNFT", "ORUP", "PRFN", "LNTA", "DASB"]

    budget=1000

    
    df = dict()
    dc = dict()
    k=0
    for MI in markets:
        
        if MI.ticker in l:
            #print(MI)
            _from = datetime.now(tz=timezone('Europe/Moscow')) - timedelta(days=360*2)
            print(_from)
            print(type(_from))
            #try:
                
            
            cndls = client.market.market_candles_get(
                MI.figi, _from=_from.isoformat(), to=datetime.now(tz=timezone('Europe/Moscow')).isoformat(), interval='week')
            #print(cndls)
                
            df2 = dict()
            cost = 0
            
            for cndl in cndls.payload.candles:
                cost = cndl.c
                #if MI.currency == MI.currency.usd:
                #    cost = cost*70
                dc[MI.ticker]=cost*MI.lot
                df2[str(cndl.time)] = ((cndl.c-cndl.o)/cndl.o)*100
                    
            #if cost*MI.lot < 1000:
            df[MI.ticker] = df2
    
            #except:
                #pass
            k=k+1
        
    pddf = pd.DataFrame(df)
    pddf.index = pd.to_datetime(pddf.index).to_period('d')

    print(pddf)
    #Global Minimum Variance[GMV] Portfolio
    
    cov = pddf.cov()
    #print(cov)
    
    gmv=erk.gmv(cov)
    i=0
    print("name", "sum", "lot price", "lot quantity")
    for g in gmv:
        print(cov.index[i], g.round(4)*budget, dc[str(cov.index[i])],
              round((g.round(4)*budget)/(dc[str(cov.index[i])]),0))
        i=i+1


    

if __name__ == '__main__':
    main()
