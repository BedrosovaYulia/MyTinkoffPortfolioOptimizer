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
    """#l = ["ATVI", "KO", "PGR", "T", "GNL", "WTTR"]
    l=[]
    result = calculate_sharp_table(l, f=datetime.now()-timedelta(days=7), t=datetime.now())
    
    l = result.sort_values(by="sharp", ascending=False).head(100)["index"].tolist()
    print(l)"""

    #************************************
    #l = ['ALB', 'ANAB', 'APTV', 'MNRO', 'SLB', 'RAMP', 'MCHP', 'KEYS', 'IFF', 'TEL', 'EDIT', 'NTRA', 'MTD', 'DHR', 'GTLS', 'MTG', 'XRX', 'ON', 'ENPH', 'FOCS', 'YETI', 'FCX', 'HPQ', 'CRMT', 'VREX', 'FOXF', 'COO', 'RYTM', 'ARW', 'MKSI', 'MYGN', 'UTHR', 'NXPI', 'BWA', 'GS', 'VEON', 'WTTR', 'NTUS', 'REGI', 'CF', 'BILI', 'OIS', 'UNVR', 'HOLX', 'KSU', 'SAVE', 'LFUS', 'CSWI', 'SIG',
    #     'PH', 'EQT', 'WFC', 'ONTO', 'FANG', 'XEC', 'NTES', 'CVCO', 'APH', 'DAR', 'CFG', 'AEO', 'MATX', 'AMAT', 'RF', 'XPO', 'PRLB', 'MS', 'LAD', 'CNXN', 'SONO', 'KRYS', 'LYB', 'WEX', 'IRDM', 'TKR', 'REZI', 'UNP', 'SEDG', 'TPIC', 'COF', 'PLXS', 'ROCK', 'TREX', 'MYRG', 'CRUS', 'MANH', 'ASH', 'KMT', 'URI', 'RH', 'TOT', 'IR', 'MSTR', 'EBS', 'SNX', 'WST', 'FITB', 'INSP', 'BMI', 'OVV']

    l=['TDC',"SPCE", "VNO", "SLG"]
    result = calculate_sharp_table(l, f=datetime.now()-timedelta(days=7), t=datetime.now())

    result2 = calculate_sharp_table(l, f=datetime.now()-timedelta(days=37), t=datetime.now()-timedelta(days=7))
    
    print(result.sort_values(by="sharp", ascending=True).head(20))
    print(result2.sort_values(by="sharp", ascending=True).head(20))

    m = (result.merge(result2, how='outer', on=['index'],suffixes=['', '_old'], indicator=True))
    print(m.sort_values(by="sharp_old", ascending=True).head(20))


if __name__ == '__main__':
    main()
