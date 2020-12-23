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
    
    #l = ["AAPL", "SBER", "MSFT", "GAZP", "BAC", "KO", "CSCO", "YNDX", "ROSN", "AFLT", "NKE", "DSKY"]

    markets = api.market.market_stocks_get()
    df = dict()
    k = 0
    for MI in markets.instruments:
        if MI.ticker: #in l:
            print("Analizing "+MI.ticker)
            now = datetime.now()
            try:
                cndls = api.market.market_candles_get(MI.figi,
                                                    from_=now - timedelta(days=1),
                                                    to=now,
                                                    interval=ti.CandleResolution.min1)
                df2 = dict()
                for cndl in cndls.candles:
                    df2[str(cndl.time)] = cndl.c-cndl.o
                    #print(cndl)
                df[MI.ticker] = df2
            except:
                pass
            k = k+1

    pddf = pd.DataFrame(df)
    pddf.index = pd.to_datetime(pddf.index).to_period('h')

    print(pddf.head())

    result = pd.DataFrame(dict(minval=pddf.min(), mintime=pddf.idxmin())).reset_index()
    #print(result)
    result.to_csv("spred"+str(now.day)+".csv")

if __name__ == '__main__':
    main()
