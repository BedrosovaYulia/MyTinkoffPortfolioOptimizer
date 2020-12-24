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
    
    #l = ["F", "MU", "PYPL", "SPCE", "FIVE", "SIBN",  "DSKY", "LNTA", "MGNT", "NLMK", "PHOR"]

    #l=["AAPL", "SBER", "MSFT", "GAZP", "BAC", "KO", "CSCO", "YNDX", "ROSN", "AFLT", "NKE", "DSKY"]

    #l=[ "KO", "INTC", "PFE", "YNDX", "GARP", "ROSN", "SBER"]

    #l = ["PHOR", "ATVI", "MGNT", "DSKY", "NLMK", "ROSN", "INTC", "MSFT"]
    
    #l = ["SIBN",  "DSKY", "MGNT", "PHOR", "NLMK", "ITCI"]
    #l = ["CHEP",  "MGNT", "FEES", "MRKC", "PHOR"]
    #l=["ITCI", "ATVI", "MAT", "INTC", "KO"]

    #l=["ATVI", "KO", "INTC", "ITCI", "MAT"]

    l = ["LNTA", "RUAL", "VTBR", "TATN", "MAGN"]
    
    budget = 10000

    
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
                if MI.currency == MI.currency.usd:
                    cost = cost*70
                    
            if cost*MI.lot < budget/10:
                instruments.append(MI.ticker)

        except:
            pass
    
    #print(instruments)

    """portfolious = itertools.combinations(instruments, 5)
    print(portfolious)
    for prt in portfolious:
        print(prt)"""


    df = dict()
    dc = dict()
    k=0
    for MI in markets.instruments:
        if MI.ticker in instruments:
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
    print(cov)
    
    gmv=erk.gmv(cov)
    i=0
    print("name", "sum", "lot price", "lot quantity")
    for g in gmv:
        print(cov.index[i], g.round(4)*budget, dc[str(cov.index[i])],
              round((g.round(4)*budget)/(dc[str(cov.index[i])]),0))
        i=i+1


    

if __name__ == '__main__':
    main()
