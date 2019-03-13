def get_DataArray(assets, start, end):
    '''
    Create pandas MultiIndex DataFrame of Yahoo data to Xarray to_pandas for
    using by zipline strategies.

    INPUTS:
    *******
    assets : list of ETFs
    start  : earliest date as datetime tz-aware
    end    : end date as datetime tz-aware

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
    import pandas_datareader as pdr
    import xarray as xr


    unable_to_trade = []
    for asset in assets:
        try:
            df = pdr.DataReader(asset,'yahoo',str((end.date() - BDay(3)).date()),
                          str(end.date()))
            print(asset,'OK')
        except:
            print('***',asset, '>>> UNABLE TO TRADE, DATE:',end)
            unable_to_trade.append(asset)
            continue

    if len(unable_to_trade) > 0:
        print ('*** WARNING - No longer trading : ', unable_to_trade)
        # Remove any unusable assets
        assets = [asset for asset in assets if asset not in unable_to_trade]

    df = pdr.DataReader(assets, 'yahoo', start, end)
    # print(df[-4:])

    # for funds, make sure that row df[-2:] has data (not nans)
    if (df[-2:-1].values>=0).all():
        # safe to forward-fill from df[-2:] downward
        df = df.ffill()
    else:
        print(' *** THERE IS A PROBLEM >>> PLS CHECK :', df[-4:])

    # Create DataArray
    Attributes = df.columns.levels[0].astype(str).str.lower()
    Symbols = [s for s in df.columns.levels[1]]
    Date = df.index

    da = xr.DataArray(df.values.transpose().reshape(len(Attributes), len(Symbols), len(Date)),
                      coords=[Attributes, Symbols, Date],
                      dims=['Attributes', 'Symbols', 'Date'])
    return da

if __name__ == "__main__":

    from datetime import datetime, timezone, timedelta
    import pytz

    assets = ['SPY','AAPL','VCVSX','QLTB','junk']
    start = datetime(2018, 1, 1, 0, 0, 0, 0, pytz.utc)
    end = datetime(2018, 1, 10, 0, 0, 0, 0, pytz.utc)
#     end = datetime.today().replace(tzinfo=timezone.utc)        # to test for 'today'

    da = get_DataArray(assets,start,end)

    print(da.to_pandas().transpose(1,2,0))

    # pass