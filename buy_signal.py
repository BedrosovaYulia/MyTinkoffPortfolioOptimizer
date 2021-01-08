from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import tinkoff_data as td
import edhec_risk_kit as erk
import csv


def calculate_sharp_table(l=[], f=datetime.now()-timedelta(days=7), t=datetime.now()):

    pddf = td.getTinkoffDailyPrices(l, f=f, t=t)
    pddf.index = pd.to_datetime(pddf.index).to_period('d')
    returns = pddf.pct_change()[1:]

    valotil = erk.annualize_vol(returns, returns.shape[0])
    a_rets = erk.annualize_rets(returns, returns.shape[0])
    sharp_r = erk.sharpe_ratio(returns, 0.03, returns.shape[0])

    result = pd.DataFrame(dict(
        vol=valotil*100,
        rets=a_rets*100,
        sharp=sharp_r*100
    )).reset_index()

    return result


def main():
    pd.set_option("display.float_format", "{:.2f}".format)
    l=list()
    #************************************
    
    """result = calculate_sharp_table(l, f=datetime.now()-timedelta(days=7), t=datetime.now())
    l = result.sort_values(by="sharp", ascending=False).head(100)["index"].tolist()
    print(l)"""
    
    l=['XRX', 'APTV', 'BRKR', 'IBP', 'CEVA', 'FRPT', 'ENV', 'MPC', 'RRGB', 'NTLA', 'RAVN', 'WING', 'ON', 'ROL', 'NMIH', 'ALB', 'IFF', 'RGEN', 'GTLS', 'BILI', 'VEON', 'SSD', 'LTHM', 'SIG', 'ROG', 'UNVR', 'MOS', 'INSP', 'AAN', 'PKI', 'FOXF', 'AVAV', 'EDIT', 'PTCT', 'SWAV', 'VLO', 'EOG', 'SLB', 'DAR', 'TSLA', 'SYNA', 'OII', 'BJRI', 'BC', 'BKR', 'TRMB', 'MYGN', 'INDB', 'THO', 'AEO', 'PRSC', 'MTG', 'AMAT', 'DXCM', 'R', 'EXP', 'ROCK', 'NTES', 'CFX', 'MSTR', 'NTUS', 'DVN', 'CRMT', 'OKE', 'PRFT', 'ITT', 'HES', 'AN', 'LAD', 'SEDG', 'RS', 'GKOS', 'ALTR', 'CFG', 'VALE', 'NTCT', 'NSC', 'ASH', 'TRIP', 'ONTO', 'KMT', 'WTTR', 'SPCE', 'HHC', 'TCBI', 'QRVO', 'CVS', 'WFC', 'COF', 'VCYT', 'CLF', 'CVCO', 'EVER', 'CLH', 'OXY', 'DKS', 'FITB', 'UTHR', 'ANAB', 'EAT']

    result = calculate_sharp_table(l, f=datetime.now()-timedelta(days=7), t=datetime.now())

    result2 = calculate_sharp_table(l, f=datetime.now()-timedelta(days=37), t=datetime.now()-timedelta(days=7))
    
    print(result.sort_values(by="sharp", ascending=True).head(20))
    print(result2.sort_values(by="sharp", ascending=True).head(20))

    m = (result.merge(result2, how='outer', on=['index'],suffixes=['', '_old'], indicator=True))
    print(m.sort_values(by="sharp_old", ascending=True).head(20))

if __name__ == '__main__':
    main()
