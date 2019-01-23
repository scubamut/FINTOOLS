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

    df = pdr.DataReader(assets, 'yahoo', start, end)

    # Find any assets which may no longer exist
    unusable_assets = [s for s in assets if df['Close'][s][-1:].any() == False]
    if len(unusable_assets) > 0:
        print ('*** WARNING - No longer trading : ', unusable_assets)
    # Remove any unusable assets
    df = df.T.drop(unusable_assets, level=1).T
    assets = [asset for asset in assets if asset not in unusable_assets]

    Attributes = df.columns.levels[0].astype(str).str.lower()
    Symbols = assets
    Date = df.index

    da = xr.DataArray(df.values.transpose().reshape(len(Attributes), len(Symbols), len(Date)),
                      coords=[Attributes, Symbols, Date],
                      dims=['Attributes', 'Symbols', 'Date'])

    # Check for missing data
    diff = da.ffill('Date')[0].count(axis=1) - da[0].count(axis=1)
    for t in [(a.data.tolist(), a.Symbols.data.tolist()) for a in diff]:
        if t[0] >= 1:
            print ('*** WARNING : ', t[1], ' MISSING DATA FOR ', t[0], 'VALUES')

    return da

# to show panel
# da.to_pandas().transpose(1,2,0)

