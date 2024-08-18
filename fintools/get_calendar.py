def get_calendar(calendar_name='NYSE'):

    import pandas_market_calendars as mcal

    return mcal.get_calendar(calendar_name)