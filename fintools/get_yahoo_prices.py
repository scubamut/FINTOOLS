def get_yahoo_prices(p):
    from pandas_datareader import data
    from fintools import set_start_end

    if not isinstance(p.start, str) & isinstance(p.end, str):
        raise TypeError('format of start & end must be "YYYY-MM-DD')

    if isinstance(p.prices, str):
        if p.prices == 'yahoo':
            tickers = p.symbols.copy()
            if p.cash_proxy != 'CASHX':
                tickers = list(set(tickers + [p.cash_proxy]))
            try:
                if isinstance(p.risk_free, str):
                    tickers = list(set(tickers + [p.risk_free]))
            except:
                pass

            if p.start >= p.end:
                raise ValueError('start must be < end')

            if not isinstance(p.start, str) & isinstance(p.end, str):
                raise TypeError('format of start and end must be "YYYY-MM-DD"')

            start, end = set_start_end(start=p.start, end=p.end)

            data_panel = data.DataReader(tickers, "yahoo", start, end)

            close = data_panel['Adj Close'].sort_index(ascending=True)

            return close.copy().dropna()
    else:
        return p.prices