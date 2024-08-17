def get_Dataset(assets, start, end, debug=False):
    '''
    Create pandas MultiIndex DataFrame of Yahoo data to Xarray to_pandas for
    using by zipline strategies.

    INPUTS:
    *******
    assets : list of ETFs
    start  : earliest date as datetime tz-aware
    end    : end date as datetime tz-aware
    debug  : True to print debug info

    NOTE: funds are not traded 'today', so 'today' prices are copied from yesterdays' prices

    OUTPUT:
    *******
    da         : DataArray with dims = ['Attributes', 'Symbols', 'Date'] where
    Attributes : ['high', 'low', 'open', 'close', 'volume', 'adj close']  NB: LowerCase!
    Symbols    : assets
    Date       :  df.index


    '''

    # 1. start/end dates should be 'utc'
    # 2. if end=today, the last day's fund price(s) duplicated with last day's price(s)
    # 3. asset is an untradable_asset unless any of last 3 days price(s) missing
    # 4. continue after dropping untradable_assets, with *** WARNING
    # 5. prices will be FORWARD-FILLED to remove missing data

    from pandas.tseries.offsets import BDay
    # import pandas_datareader as pdr
    import yfinance as yf
    import xarray as xr

    dict = {}
    unable_to_trade = []
    for asset in assets:
        try:
            df = yf.download(asset, str((end.date() - BDay(3)).date()),
                                str(end.date()))
            print(asset, 'OK\n')
        except:
            print('***', asset, '>>> UNABLE TO TRADE, DATE:', end, '\n')
            unable_to_trade.append(asset)
            continue

        df = yf.download(asset, start, end)
        dict[str(asset)] = df

        if debug:
            print(df[-4:], '\n')

        # for funds, make sure that row df[-2:] has data (not nans)
        if (df[-2:-1].values >= 0).all():
            # safe to forward-fill from df[-2:] downward
            df = df.ffill()
        else:
            print(' *** THERE IS A PROBLEM >>> PLS CHECK :', df[-4:], '\n')

    if len(unable_to_trade) > 0:
        print('*** UNUSABLE: ', unable_to_trade, '\n')

    return xr.Dataset(dict)

############################################################################################################
if __name__ == "__main__":

    from datetime import datetime, timezone, timedelta
    import pytz

    assets = ['SPY', 'AAPL', 'QLTB', 'VCVSX', 'junk']
    start = datetime(2018, 1, 1, 0, 0, 0, 0, pytz.utc)
    end = datetime(2018, 1, 10, 0, 0, 0, 0, pytz.utc)
    #     end = datetime.today().replace(tzinfo=timezone.utc)        # to test for 'today'

    ds = get_Dataset(assets, start, end)

    print(ds.to_dataframe())