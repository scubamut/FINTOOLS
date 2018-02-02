def highlight_pos_neg (strategy_value) :
    is_positive = strategy_value > 0
    return ['background-color : rgb(127,255,0)' if v else 'background-color : rgb(255,99,71)' for v in is_positive]