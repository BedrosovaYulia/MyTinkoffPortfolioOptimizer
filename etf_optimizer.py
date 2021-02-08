import os
from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Any, List, Tuple
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import tinvest as ti
import edhec_risk_kit as erk


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

    markets = api.market.market_etfs_get()
    l = ["AKSP", "VTBA", "FXDE", "RUSE", "AKEU", "AKMB","FXRB", "VTBH", "FXRU", "SBRB", "VTBB", "FXGD"]
    #l = ["FXCN", "VTBE", "AKNX","FXIT","FXWO","FXUS","FXRW","SBSP","SBMX","FXRL","VTBX","FXKZ"]
    e = ["TIPO", "TBIO", "TMOS", "TECH", "TSPX",
         "TRUR", "TGLD", "TEUR", "TUSD"]

    budget=50000

    
    df = dict()
    dc = dict()
    k=0
    for MI in markets.instruments:
        if ((len(l) > 0 and MI.ticker in l) or (len(l) == 0 and MI.ticker)) and (MI.ticker not in e):
            now = datetime.now()
            try:
                cndls = api.market.market_candles_get(MI.figi,
                                                    from_=now -
                                                    timedelta(days=360),
                                                    to=now,
                                                    interval=ti.CandleResolution.day)
                df2 = dict()
                cost = 0
                for cndl in cndls.candles:
                    cost = cndl.c
                    if MI.currency == MI.currency.usd:
                        cost = cost*75
                    dc[MI.ticker]=cost*MI.lot
                    df2[str(cndl.time)] = ((cndl.c-cndl.o)/cndl.o)*100
                    
                #if cost*MI.lot < 1000:
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
    
    gmv=erk.gmv(cov)
    i=0
    print("name", "sum", "lot price", "lot quantity")
    for g in gmv:
        if round((g.round(4)*budget)/(dc[str(cov.index[i])]), 0) > 0:
            print(cov.index[i], g.round(4)*budget, dc[str(cov.index[i])], round((g.round(4)*budget)/(dc[str(cov.index[i])]),0))
        i=i+1


    

if __name__ == '__main__':
    main()
