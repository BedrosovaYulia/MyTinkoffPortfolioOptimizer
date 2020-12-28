from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import tinkoff_data as td
import edhec_risk_kit as erk
import csv


def main():
    l = ["ATVI", "KO", "INTC", "LPL", "MAT", "FIVE", "SIBN", "LNTA"]
    #pddf = td.getTinkoffLastYearPrices(l, resolution='day')
    #pddf = td.getTinkoffLastYearPrices(l, resolution='month')
    pddf = td.getTinkoffLastYearPrices(resolution='month')


    pddf.index = pd.to_datetime(pddf.index).to_period('d')
    
    returns = pddf.pct_change()[1:]
    print(returns.head())
    print(returns.shape)

    valotil = erk.annualize_vol(returns, returns.shape[0])
    a_rets = erk.annualize_rets(returns, returns.shape[0])
    sharp_r = erk.sharpe_ratio(returns, 0.03, returns.shape[0])
    
    result = pd.DataFrame(dict(
        vol=valotil*100, 
        rets=a_rets*100, 
        sharp=sharp_r*100
        )).reset_index()

    pd.set_option("display.float_format", "{:.2f}".format)

    print(result.sort_values(by="sharp", ascending=False).head(20))

    result.to_csv("volatility_"+str(datetime.now().date())+".csv")
   


if __name__ == '__main__':
    main()
