from . import monthly_return_table

def highlight_pos_neg (strategy_value) :
    is_positive = strategy_value > 0
    return ['background-color : rgb(127,255,0)' if v else 'background-color : rgb(255,99,71)' for v in is_positive]

def show_return_table(strategy_value):
    df = monthly_return_table (strategy_value)
    return df.style.format('{:.2f}').applymap(lambda x: "background-color: rgb(127,255,0)" 
                                             if x>0 else "background-color: rgb(255,99,71)")