def compute_weights_RS_DM(name, parameters):
    import pandas as pd
    from fintools.Parameters import Parameters
    from fintools.get_DataArray import get_DataArray
    from fintools.endpoints import endpoints
    from fintools.backtest import backtest

    import yfinance as yf

    print('Strategy : {}'.format(name))

    p = Parameters(parameters)

    tickers = p.assets.copy()
    if p.cash_proxy != 'CASHX':
        tickers = list(set(tickers + [p.cash_proxy]))
    try:
        if isinstance(p.risk_free, str):
            tickers = list(set(tickers + [p.risk_free]))
    except:
        pass

    prices = yf.download(tickers, p.start, p.end, auto_adjust=True)['Close'].ffill().dropna()

    end_points = endpoints(period=p.frequency, trading_days=prices.index)
    prices_m = prices.loc[end_points]

    returns = prices_m[p.assets].pct_change(p.rs_lookback)[p.rs_lookback:]

    if isinstance(p.risk_free, int):
        excess_returns = returns
    else:
        risk_free_returns = prices_m[p.risk_free].pct_change(p.rs_lookback)[p.rs_lookback:]
        excess_returns = returns.subtract(risk_free_returns, axis=0).dropna()

    absolute_momentum = prices_m[p.assets].pct_change(p.risk_lookback)[p.risk_lookback:]
    absolute_momentum_rule = absolute_momentum > 0
    rebalance_dates = excess_returns.index.join(absolute_momentum_rule.index, how='inner')

    # relative strength ranking
    ranked = excess_returns.loc[rebalance_dates][p.assets].rank(ascending=False, axis=1, method='dense')
    # elligibility rule - top n_top ranked securities
    elligible = ranked[ranked <= p.n_top] > 0

    # equal weight allocations
    elligible = elligible.multiply(1. / elligible.sum(1), axis=0)

    # downside protection
    weights = pd.DataFrame(0., index=elligible.index, columns=prices.columns)
    if p.cash_proxy == 'CASHX':
        weights[p.cash_proxy] = 0
        prices[p.cash_proxy] = 1.
    weights[p.assets] = (elligible * absolute_momentum_rule).dropna()
    weights[p.cash_proxy] += 1 - weights[p.assets].sum(axis=1)

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

        'RS0001': {'assets': ['CWB', 'HYG', 'MBB', 'IEF', 'HYD'],
                   'start': start, 'end': end,
                   'rs_lookback': 1, 'risk_lookback': 1, 'n_top': 2, 'frequency': 'M',
                   'cash_proxy': 'CASHX', 'risk_free': 0}}

    p_value, p_holdings, p_weights, prices = compute_weights_RS_DM('RS0001', strategies['RS0001'])

    print(p_value[-5:])