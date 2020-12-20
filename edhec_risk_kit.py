import pandas as pd
import scipy.stats
import numpy as np

def drawdown(return_series: pd.Series):
    """
    Takes a time serios of asset returns
    Computes and returs a DataFrame that contains:
    the wealth index
    the previous peaks
    percent drawdowns
    """
    wealth_index=1000*(1+return_series).cumprod()
    previous_peaks=wealth_index.cummax()
    drawdowns = (wealth_index-previous_peaks)/previous_peaks
    return pd.DataFrame({
       "Wealth":wealth_index,
       "Peaks":previous_peaks,
       "Drawdown":drawdowns
    })

def get_ffme_returns():
    """
    Load the Fama-French Dataset for the returns of the Top and Bottom Deciles by MarketCap
    """
    me_m = pd.read_csv("Portfolios_Formed_on_ME_monthly_EW.csv",header=0,index_col=0,parse_dates=True, na_values=-99.99)
    rets=me_m[['Lo 10','Hi 10']]
    rets.columns=['SmallCap','LargeCap']
    rets=rets/100
    rets.index=pd.to_datetime(rets.index,format="%Y%m").to_period('M')
    return rets

def get_hfi_returns():
    """
    Load the Fama-French Dataset for the returns of the Top and Bottom Deciles by MarketCap
    """
    hfi = pd.read_csv("edhec-hedgefundindices.csv",header=0,index_col=0,parse_dates=True, na_values=-99.99)
    hfi=hfi/100
    hfi.index=pd.to_datetime(hfi.index,format="%Y%m").to_period('M')
    return hfi

def get_ind_returns():
    ind=pd.read_csv("ind30_m_vw_rets.csv", header=0, index_col=0, parse_dates=True)/100
    ind.index=pd.to_datetime(ind.index, format="%Y%m").to_period()
    ind.columns=ind.columns.str.strip()
    return ind

def skewness(r):
    """
    Alternative to scipy.stats.skew()
    """
    demeaned_r = r - r.mean()
    #use standard deviation dof=0
    sigma_r=r.std(ddof=0)
    exp=(demeaned_r**3).mean()
    return exp/sigma_r**3

def kurtosis(r):
    """
    Alternative to scipy.stats.kurtosis()
    """
    demeaned_r = r - r.mean()
    #use standard deviation dof=0
    sigma_r=r.std(ddof=0)
    exp=(demeaned_r**4).mean()
    return exp/sigma_r**4

def is_normal(r, level=0.01):
    """
    Aplly J-B test
    """
    statistic, p_value = scipy.stats.jarque_bera(r)
    return p_value>level
    
    
def semideviation(r):
    is_negative = r<0
    return r[is_negative].std(ddof=0)


def var_historic(r, level=5):
    if isinstance(r, pd.DataFrame):
        return r.aggregate(var_historic, level=level)
    elif isinstance(r, pd.Series):
        return -np.percentile(r,level)
    else:
        raise TypeError("Expected r to be Series or DataFrame")
        
from scipy.stats import norm
def var_gaussian(r, level=5, modified=False):
    z = norm.ppf(level/100)
    if modified:
        s=skewness(r)
        k=kurtosis(r)
        z=(z+
           (z**2 - 1)*s/6+
           (z**3 - 3*z)*(k-3)/24-
           (2*z**3 - 5*z)*(s**2)/36
          )
    return -(r.mean()+z*r.std(ddof=0))


def cvar_historic(r, level=5):
    if isinstance(r, pd.Series):
        is_beyond = r<=-var_historic(r, level=level)
        return -r[is_beyond].mean()
    elif isinstance(r, pd.DataFrame):
        return r.aggregate(cvar_historic, level=level)
    else:
        raise TypeError("Expected r to be Series or DataFrame")
        
        
def annualize_rets(r, periods_per_year):
    """
    Annualizes a set of returns
    We should infer the periods per year
    but that is currently left as an exercise
    to the reader :-)
    """
    compounded_growth = (1+r).prod()
    n_periods = r.shape[0]
    return compounded_growth**(periods_per_year/n_periods)-1


def annualize_vol(r, periods_per_year):
    """
    Annualizes the vol of a set of returns
    We should infer the periods per year
    but that is currently left as an exercise
    to the reader :-)
    """
    return r.std()*(periods_per_year**0.5)


def sharpe_ratio(r, riskfree_rate, periods_per_year):
    """
    Computes the annualized sharpe ratio of a set of returns
    """
    # convert the annual riskfree rate to per period
    rf_per_period = (1+riskfree_rate)**(1/periods_per_year)-1
    excess_ret = r - rf_per_period
    ann_ex_ret = annualize_rets(excess_ret, periods_per_year)
    ann_vol = annualize_vol(r, periods_per_year)
    return ann_ex_ret/ann_vol
























