def get_DataArray(assets, start, end):
    '''
    Create pandas MultiIndex DataFrame of Yahoo data to Xarray to_pandas for
    using by zipline strategies.

    INPUTS:
    *******
    assets : list of ETFs
    start  : earliest date as 'yyyy-mm-dd'
    end    : end date as 'yyyy-mm-dd'

    OUTPUT:
    *******
    da         : DataArray with dims = ['Attributes', 'Symbols', 'Date'] where
    Attributes : ['high', 'low', 'open', 'close', 'volume', 'adj close']  NB: LowerCase!
    Symbols    : assets
    Date       :  df.index


    '''

    import pandas_datareader as pdr
    import datetime as dt
    import pytz
    import xarray as xr

    try:
        df = pdr.DataReader(assets, 'yahoo', start, end)
    except:

        print('** UNKNOWN ASSET -> ')

    # for funds, today's data is unavailable
    # so forward-fill last 2 days
    df[-1:] = df[-2:-1].values
    unusable_assets = [s for s in assets if df['Close'][s][-2:].ffill().any() == False]
    if len(unusable_assets) > 0:
        print ('*** WARNING - No longer trading : ', unusable_assets)
        # Remove any unusable assets
        df = df.T.drop(unusable_assets, level=1).T

    # FORWARD-FILL to remove missing data
    df = df.ffill()

    # Create DataArray
    Attributes = df.columns.levels[0].astype(str).str.lower()
    Symbols = [s for s in df.columns.levels[1] if s not in unusable_assets]
    Date = df.index

    da = xr.DataArray(df.values.transpose().reshape(len(Attributes), len(Symbols), len(Date)),
                      coords=[Attributes, Symbols, Date],
                      dims=['Attributes', 'Symbols', 'Date'])


    return da

