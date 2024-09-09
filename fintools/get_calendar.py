def get_calendar(calendar_name='NYSE'):

    import exchange_calendars as excal

    return excal.get_calendar(calendar_name)