class Parameters():

    def __init__(self, parameters):

        if 'symbols' in parameters:
            self.symbols = parameters['symbols']
		else:
			None
        if 'prices' in parameters:
            self.prices = parameters['prices']
		else:
			None
        if 'start' in parameters:
            self.start = parameters['start']
		else:
			None
        if 'end' in parameters:
            self.end = parameters['end']
		else:
			None
        if 'risk_free' in parameters:
            self.risk_free = parameters['risk_free']
		else:
			None
        if 'cash_proxy' in parameters:
            self.cash_proxy = parameters['cash_proxy']
		else:
			None
        if 'rs_lookback' in parameters:
            self.rs_lookback = parameters['rs_lookback']
		else:
			None
        if 'risk_lookback' in parameters:
            self.risk_lookback = parameters['risk_lookback']
		else:
			None
        if 'n_top' in parameters:
            self.n_top = parameters['n_top']
		else:
			None
        if 'frequency' in parameters:
            self.frequency = parameters['frequency']
		else:
			None
        if 'allocations' in parameters:
            self.allocations = parameters['allocations']
		else:
			None
