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

    markets=api.market.market_stocks_get()
    
    df = dict()
    k=0
    for MI in markets.instruments:
        if (k<10):
            now = datetime.now()
            try:
                cndls = api.market.market_candles_get(MI.figi,
                                                    from_=now -
                                                    timedelta(days=30),
                                                    to=now,
                                                    interval=ti.CandleResolution.day)
                df2 = dict()
                for cndl in cndls.candles:
                    df2[str(cndl.time)] = ((cndl.c-cndl.o)/cndl.o)*100
                df[MI.ticker] = df2
            except:
                pass
            k=k+1
        
    pddf = pd.DataFrame(df)
    pddf.index = pd.to_datetime(pddf.index).to_period('d')

    print(pddf)

    #er = erk.annualize_rets(pddf, 12)
    #print(er)

    cov = pddf.cov()
    print(cov)
    
    gmv=erk.gmv(cov)
    i=0
    for g in gmv:
        print (cov.index[i],g.round(4)*100)
        i=i+1


    

if __name__ == '__main__':
    main()
