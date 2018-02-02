from fintools import monthly_return_table

def show_return_table(strategy_value):
    df = monthly_return_table (strategy_value)
    return df.style.apply(highlight_pos_neg)