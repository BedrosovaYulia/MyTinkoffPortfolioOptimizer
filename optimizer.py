import os
from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Any, List, Tuple

import pandas as pd
import plotly.graph_objects as go

import tinvest as ti

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
    #print(type(markets))
    #print(markets.instruments)
    for MI in markets.instruments:
        print(MI.name, MI.ticker, MI.figi)
    
    now = datetime.now()
    cndls = api.market.market_candles_get("BBG004730N88",
                                            from_=now - timedelta(days=7),
                                            to=now,
                                            interval=ti.CandleResolution.hour)
    for cndl in cndls.candles:
        print (cndl.time, cndl.v, cndl.h, cndl.l)

if __name__ == '__main__':
    main()
