import os
from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Any, List, Tuple
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import tinvest as ti
import edhec_risk_kit as erk
import csv


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

    markets = api.market.market_stocks_get()
    df = dict()
    k = 0
    for MI in markets.instruments:
        print ("Analizing "+MI.ticker)
        now = datetime.now()
        try:
            cndls = api.market.market_candles_get(MI.figi,
                                                    from_=now -
                                                    timedelta(days=250),
                                                    to=now,
                                                    interval=ti.CandleResolution.day)
            df2 = dict()
            for cndl in cndls.candles:
                df2[str(cndl.time)] = ((cndl.c-cndl.o)/cndl.o)*100
            df[MI.ticker] = df2
        except:
            pass
        k = k+1

    pddf = pd.DataFrame(df)
    pddf.index = pd.to_datetime(pddf.index).to_period('d')

    # 250 because 250 trading days a year
    valotil = erk.annualize_vol(pddf, 250)
    a_rets = erk.annualize_rets(pddf, 250)
    sharp_r = erk.sharpe_ratio(pddf, 0.1, 250)

    
    result = pd.DataFrame(dict(vol=valotil, rets=a_rets, sharp=sharp_r)).reset_index()
    print(result.head())

    result.to_csv("volatility2.csv")
   


if __name__ == '__main__':
    main()
