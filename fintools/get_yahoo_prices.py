def get_yahoo_prices(p):
    
    import yfinance as yf
    
    tickers = p.assets.copy()
    
    if p.cash_proxy != 'CASHX':
        tickers = list(set(tickers + [p.cash_proxy]))
    try:
        if isinstance(p.risk_free, str):
            tickers = list(set(tickers + [p.risk_free]))
    except:
        pass

    close = yf.download(tickers, p.start, p.end)['Adj Close'].sort_index(ascending=True)

    return close.copy().dropna()