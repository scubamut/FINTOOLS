from . import monthly_return_table

def show_annual_returns(strategy_value):
    df = monthly_return_table (strategy_value)
    frame = df['Annual Returns'].to_frame()
    frame['positive'] = df['Annual Returns'] >= 0
    frame['Annual Returns'].plot(figsize=(15,10),kind='bar',color=frame.positive.map({True: 'g', False: 'r'}), grid=True)