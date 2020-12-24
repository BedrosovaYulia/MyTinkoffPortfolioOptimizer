import os
from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Any, List, Tuple
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import tinvest as ti
import edhec_risk_kit as erk
import itertools

class HTTPError(Exception):
    pass

class CustomClient(ti.SyncClient):
    def request(self, *args, **kwargs) -> Any:
        response = super().request(*args, **kwargs)
        if response.status_code != HTTPStatus.OK:
            raise HTTPError(response.parse_error().json())

        return response.parse_json().payload


client = CustomClient(os.getenv('TINVEST_SANDBOX_TOKEN', ''), use_sandbox=True)

api = ti.OpenApi(client)

def main():

    markets=api.market.market_stocks_get()
    
    budget = 10000

    #instruments = ["SBER", "MSFT", "GAZP", "BAC", "YNDX", "ROSN", "AFLT", "DSKY", "SBER", "LNTA"]
        
    instruments = list()
    for MI in markets.instruments:
        now = datetime.now()
        try:
            cndls = api.market.market_candles_get(MI.figi,
                                                    from_=now -
                                                    timedelta(days=1),
                                                    to=now,
                                                    interval=ti.CandleResolution.hour)
            cost = 0
            for cndl in cndls.candles:
                cost = cndl.c
                    
            if (MI.currency == MI.currency.rub) and (cost*MI.lot < budget/10):
                instruments.append(MI.ticker)

        except:
            pass
    
    #print(instruments)

    portfolious = itertools.combinations(instruments, 5)
    print(portfolious)
    for prt in portfolious:
        
        df = dict()
        dc = dict()
        k=0
        for MI in markets.instruments:
            if MI.ticker in prt:
                now = datetime.now()
                try:
                    cndls = api.market.market_candles_get(MI.figi,
                                                        from_=now -
                                                        timedelta(days=250),
                                                        to=now,
                                                        interval=ti.CandleResolution.day)
                    df2 = dict()
                    cost = 0
                    for cndl in cndls.candles:
                        cost = cndl.c
                        if MI.currency == MI.currency.usd:
                            cost = cost*70
                        dc[MI.ticker]=cost*MI.lot
                        df2[str(cndl.time)] = ((cndl.c-cndl.o)/cndl.o)*100
                        
                    if cost*MI.lot < budget/10:
                        df[MI.ticker] = df2
        
                except:
                    pass
                k=k+1
            
        pddf = pd.DataFrame(df)
        pddf.index = pd.to_datetime(pddf.index).to_period('d')

        #print(pddf)
        #Global Minimum Variance[GMV] Portfolio
    
        cov = pddf.cov()
        #print(cov)
        try:        
            gmv=erk.gmv(cov)
            i = 0
            result=list()
            for g in gmv:
                if round((g.round(4)*budget)/(dc[str(cov.index[i])]), 0) >0:
                    #print(cov.index[i], g.round(4)*budget, dc[str(cov.index[i])],
                    #    round((g.round(4)*budget)/(dc[str(cov.index[i])]),0))
                    result.append({
                        "name":cov.index[i], 
                        "sum":g.round(4)*budget, 
                        "price":dc[str(cov.index[i])], 
                        "quantity":round((g.round(4)*budget)/(dc[str(cov.index[i])]), 0)
                    })
                
                i=i+1
            
            #print(prt)
            #print(len(result))
            if len(result) == 5:
                print(prt)
                for r in result:
                    print(r["name"], r["quantity"])
                print("***************************************************")
                
        except:
            pass



    

if __name__ == '__main__':
    main()
