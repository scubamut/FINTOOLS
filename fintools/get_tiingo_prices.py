def get_tiingo_prices(assets,startDate,endDate):

    '''
    Download pandas DataFrame of Tiingo data of adjusted close prices

    :param assets: list of asset symbols
    :param startDate: start date in format '%Y-%m-%d'
    :param endDate: end date in format '%Y-%m-%d'
    :return: pandas DataFrame
    '''

    from tiingo import TiingoClient

    TIINGO_API_KEY = 'c5ec6d8655e80ab3318af299a695443c62494efe'

    config = {
        'api_key': TIINGO_API_KEY,
        'session': True  # Reuse HTTP sessions across API calls for better performance
    }

    # Throughout the rest of this notebook, you'll use the "client" to interact with the Tiingo backend services.
    client = TiingoClient(config)

    return client.get_dataframe(assets,
                               frequency='daily',
                               metric_name='close',
                               startDate=startDate,
                               endDate=endDate)

if __name__ == "__main__":

    from datetime import datetime, timezone, timedelta
    import pytz

    assets = ['SPY', 'BND']

    start = datetime(2018, 1, 1, 0, 0, 0, 0, pytz.utc)
    end = datetime(2018, 3, 31, 0, 0, 0, 0, pytz.utc)

    startDate = start.strftime("%Y-%m-%d")
    endDate = end.strftime("%Y-%m-%d")

    df = get_tiingo_prices(assets,startDate,endDate)

    print(df)