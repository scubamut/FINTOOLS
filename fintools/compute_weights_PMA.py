def compute_weights_PMA(name, parameters):

    from fintools.Parameters import Parameters
    from fintools.get_DataArray import get_DataArray
    from fintools.endpoints import endpoints
    from fintools.backtest import backtest

    print(name)

    p = Parameters(parameters)

    tickers = p.assets.copy()
    if p.cash_proxy != 'CASHX':
        tickers = list(set(tickers + [p.cash_proxy]))
    try:
        if isinstance(p.risk_free, str):
            tickers = list(set(tickers + [p.risk_free]))
    except:
        pass

    da = get_DataArray(tickers, p.start, p.end)
    prices = da.to_pandas().transpose(1,2,0)[:,:,'close']

    end_points = endpoints(period=p.frequency, trading_days=prices.index)
    prices_m = prices.loc[end_points]

    # elligibility rule
    SMA = prices_m.rolling(p.risk_lookback).mean().dropna()
    rebalance_dates = SMA.index
    rule = prices_m.loc[rebalance_dates][p.assets] > SMA[p.assets]

    # fixed weight allocation
    weights = p.allocations * rule

    # downside protection
    weights[p.cash_proxy] = 1 - weights[p.assets].sum(axis=1)

    # backtest
    p_value, p_holdings, p_weights = backtest(prices, weights, 10000., offset=0, commission=10.)

    # p_value.plot(figsize=(15, 10), grid=True, legend=True, label=name)

    return p_value, p_holdings, p_weights, prices


if __name__ == "__main__":

    import pandas as pd
    from datetime import datetime, timezone, timedelta
    import pytz

    start = datetime(2010, 1, 1, 0, 0, 0, 0, pytz.utc)
    end = datetime(2011, 1, 1, 0, 0, 0, 0, pytz.utc)
#     end = datetime.today().replace(tzinfo=timezone.utc)        # to test for 'today'
    strategies = {

        'PMA003': {'assets': ['VCVSX', 'FAGIX', 'VGHCX'],
               'start':start, 'end':end,
               'risk_lookback': 2, 'frequency': 'M', 'allocations': [1./3., 1./3., 1./3.],
              'cash_proxy': 'VUSTX'}}

    p_value, p_holdings, p_weights, prices = compute_weights_PMA('PMA003', strategies['PMA003'])


    print(p_value[-5:])