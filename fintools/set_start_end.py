def set_start_end(start=None, end=None):

    from datetime import datetime
    import pandas as pd

    def valid_date(date, proxy_date):

        if not isinstance(p.start, str) & isinstance(p.end, str):
            raise TypeError('format of date must be "YYYY-MM-DD')

        dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d')
        try:
            dateparse(date)
        except:
            date = proxy_date
        return date

    start = valid_date(start, '1986-01-01')
    end = valid_date(end, datetime.today().strftime('%Y-%m-%d'))

    if start < end:
        return start, end
    else:
        print("start must be < end : ", start, ' >= ', end)