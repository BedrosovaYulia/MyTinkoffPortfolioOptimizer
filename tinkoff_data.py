import tinvest as ti
import os
from http import HTTPStatus
from typing import Any, List, Tuple
from datetime import datetime, timedelta
import pandas as pd
import numpy as np


class HTTPError(Exception):
    pass


class CustomClient(ti.SyncClient):
    def request(self, *args, **kwargs) -> Any:
        response = super().request(*args, **kwargs)
        if response.status_code != HTTPStatus.OK:
            raise HTTPError(response.parse_error().json())

        return response.parse_json().payload


def getTinkoffLastYearPrices(l=[], resolution='day'):
    client = CustomClient(os.getenv('TINVEST_SANDBOX_TOKEN', ''), use_sandbox=True)
    api = ti.OpenApi(client)

    markets = api.market.market_stocks_get()
    df = dict()
    k = 0
    for MI in markets.instruments:
        if (len(l) > 0 and MI.ticker in l) or (len(l) == 0 and MI.ticker):
            now = datetime.now()
            try:
                if resolution=='day':
                    cndls = api.market.market_candles_get(MI.figi,
                                                        from_=now -
                                                        timedelta(days=7),
                                                        to=now,
                                                        interval=ti.CandleResolution.day)
                elif resolution == 'month':
                    cndls = api.market.market_candles_get(MI.figi,
                                                          from_=now -
                                                          timedelta(days=3650),
                                                          to=now,
                                                          interval=ti.CandleResolution.month)

                df2 = dict()
                for cndl in cndls.candles:
                    df2[str(cndl.time)] = cndl.c
                df[MI.ticker] = df2
            except:
                pass
            k = k+1
    pddf = pd.DataFrame(df)
    return pddf


def getTinkoffDailyPrices(l=[], f=datetime.now()-timedelta(days=7), t=datetime.now()):
    print(f, t)
    client = CustomClient(
        os.getenv('TINVEST_SANDBOX_TOKEN', ''), use_sandbox=True)
    api = ti.OpenApi(client)

    markets = api.market.market_stocks_get()
    df = dict()
    k = 0
    for MI in markets.instruments:
        if (len(l) > 0 and MI.ticker in l) or (len(l) == 0 and MI.ticker):
            now = datetime.now()
            try:
                cndls = api.market.market_candles_get(MI.figi,
                                                      from_=f,
                                                      to=t,
                                                      interval=ti.CandleResolution.day)

                df2 = dict()
                for cndl in cndls.candles:
                    df2[str(cndl.time)] = cndl.c
                df[MI.ticker] = df2
            except:
                pass
            k = k+1
    pddf = pd.DataFrame(df)
    return pddf


def getTinkoffETFsLYPrices(l=[], resolution='day'):
    client = CustomClient(
        os.getenv('TINVEST_SANDBOX_TOKEN', ''), use_sandbox=True)
    api = ti.OpenApi(client)

    markets = api.market.market_etfs_get()
    df = dict()
    k = 0
    for MI in markets.instruments:
        if (len(l) > 0 and MI.ticker in l) or (len(l) == 0 and MI.ticker):
            now = datetime.now()
            try:
                if resolution == 'day':
                    cndls = api.market.market_candles_get(MI.figi,
                                                          from_=now -
                                                          timedelta(days=90),
                                                          to=now,
                                                          interval=ti.CandleResolution.day)
                elif resolution == 'month':
                    cndls = api.market.market_candles_get(MI.figi,
                                                          from_=now -
                                                          timedelta(days=3650),
                                                          to=now,
                                                          interval=ti.CandleResolution.month)

                df2 = dict()
                for cndl in cndls.candles:
                    df2[str(cndl.time)] = cndl.c
                df[MI.ticker] = df2
            except:
                pass
            k = k+1
    pddf = pd.DataFrame(df)
    return pddf

def getActualPrices():
    client = CustomClient(
        os.getenv('TINVEST_SANDBOX_TOKEN', ''), use_sandbox=True)
    api = ti.OpenApi(client)
    markets = api.market.market_etfs_get()
    dc = dict()
    for MI in markets.instruments:
        now = datetime.now()
        try:
            cndls = api.market.market_candles_get(MI.figi,
                                                from_=now -
                                                timedelta(days=7),
                                                to=now,
                                                interval=ti.CandleResolution.day)
            df2 = dict()
            cost = 0
            for cndl in cndls.candles:
                cost = cndl.c
                dc[MI.ticker] = cost*MI.lot
        except:
            pass

    return dc
