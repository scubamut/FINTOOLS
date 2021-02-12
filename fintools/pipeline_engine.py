# REPLACES make_pipeline_engine()
####################################

def pipeline_engine(start_date, end_date, bundle_name):
    from zipline.data.bundles import load, register
    from zipline.pipeline.engine import SimplePipelineEngine
    from zipline.pipeline.loaders import USEquityPricingLoader

    register(bundle_name, [])
    bundle_data = load(bundle_name)

    # Set the dataloader
    pricing_loader = USEquityPricingLoader.without_fx(bundle_data.equity_daily_bar_reader,
                                                      bundle_data.adjustment_reader)

    # Define the function for the get_loader parameter
    def choose_loader(column):
        if column not in USEquityPricing.columns:
            raise Exception('Column not in USEquityPricing')
        return pricing_loader

    # Create a Pipeline engine
    engine = SimplePipelineEngine(get_loader=choose_loader, asset_finder=bundle_data.asset_finder)

    # Run pipeline for the given start and end dates
    pipeline_output = engine.run_pipeline(pipeline, start_date, end_date)

    return pipeline_output

if __name__ == "__main__":
    start_date = '2016-01-05'
    end_date = '2016-01-06'

    ##########################################################################################
    # CREATE A PIPELINE
    ###################
    from zipline.pipeline.factors import AverageDollarVolume
    from zipline.pipeline.data import USEquityPricing
    from zipline.pipeline import Pipeline
    from zipline.pipeline.domain import US_EQUITIES

    # Create a screen for our Pipeline
    universe = AverageDollarVolume(window_length=5).top(5)

    # Create an empty Pipeline with the given screen
    pipeline = Pipeline(screen=universe, domain=US_EQUITIES)
    pipeline.add(AverageDollarVolume(window_length=5), "Dollar Volume")
    ##########################################################################################

    pipeline_output = pipeline_engine(start_date, end_date, 'quantopian-quandl')

    print(pipeline_output.head)