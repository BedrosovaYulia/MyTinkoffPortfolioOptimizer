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
    
    """result = calculate_sharp_table(l, f=datetime.now()-timedelta(days=1), t=datetime.now())
    l = result.sort_values(by="sharp", ascending=False).head(100)["index"].tolist()
    print(l)"""
    
    l = ['GH', 'HIBB', 'URBN', 'GCO', 'BC', 'CPS', 'IFF', 'MOV', 'KZOSP', 'WWW', 'PSN', 'OLLI', 'ENTA', 'CROX', 'RRC', 'ACIA', 'AMAT', 'DPZ', 'RGNX', 'MRNA', 'BIG', 'TGKBP', 'DDOG', 'BBBY', 'TGKB', 'BECN', 'TPX', 'DECK', 'OSUR', 'FOXF', 'ATGE', 'DRNA', 'BBY', 'YETI', 'WSM', 'INGN', 'CRWD', 'UTHR', 'PRG', 'TXG', 'SIG', 'EQT', 'TCBI', 'CEVA', 'PBF', 'INDB', 'COHR', 'LEVI', 'DKNG',
         'GM', 'CRI', 'CVS', 'XLNX', 'ETRN', 'FOCS', 'XOM', 'NEO', 'AMD', 'RUAL', 'WTFC', 'BOOT', 'GRA', 'DBX', 'AVY', 'RIG', 'WAL', 'ZEN', 'VPG', 'OKE', 'MELI', 'LPLA', 'GNRC', 'ASH', 'NARI', 'SHW', 'BLUE', 'SWBI', 'SKX', 'GOSS', 'AGIO', 'TGKD', 'TER', 'AEO', 'SF', 'NDSN', 'AFKS', 'IQV', 'TCRR', 'BBIO', 'RH', 'ESPR', 'COG', 'CNST', 'BLD', 'PB', 'MAS', 'RPD', 'NLSN', 'SONO', 'JEF']

    result = calculate_sharp_table(l, f=datetime.now()-timedelta(days=7), t=datetime.now())

    result2 = calculate_sharp_table(l, f=datetime.now()-timedelta(days=37), t=datetime.now()-timedelta(days=7))
    
    print(result.sort_values(by="sharp", ascending=True).head(20))
    print(result2.sort_values(by="sharp", ascending=True).head(20))

    m = (result.merge(result2, how='outer', on=['index'],suffixes=['', '_old'], indicator=True))
    print(m.sort_values(by="sharp_old", ascending=True).head(20))

if __name__ == '__main__':
    main()
