# DEPRACATED - REPLACED BY pipeline_engine()
############################################

from datetime import datetime, timezone, timedelta
import pytz

from zipline.pipeline.loaders import USEquityPricingLoader
from zipline.utils.calendars import get_calendar
from zipline.data.bundles import register, load
from zipline.pipeline import Pipeline
from zipline.pipeline.data import USEquityPricing
from zipline.pipeline.filters import StaticAssets
from zipline.pipeline.engine import SimplePipelineEngine
from zipline.pipeline.domain import US_EQUITIES

def make_pipeline_engine(symbols=['SPY', 'TLT'], bundle='etfs_bundle', calendar='NYSE'):
    register(bundle, symbols)
    bundle_data = load(bundle)

    # Set up pipeline engine
    # Loader for pricing
    pipeline_loader = USEquityPricingLoader.without_fx(
        bundle_data.equity_daily_bar_reader,
        bundle_data.adjustment_reader,
    )

    def my_dispatcher(column):
        return loaders[column]

    def choose_loader(column):
        if column in USEquityPricing.columns:
            return pipeline_loader
        return my_dispatcher(column)

    trading_calendar = get_calendar(calendar)
    engine = SimplePipelineEngine(
        get_loader=choose_loader,
        # calendar=trading_calendar.all_sessions,
        asset_finder=bundle_data.asset_finder,
    )

    assets = bundle_data.asset_finder.lookup_symbols(symbols, as_of_date=None)
    return assets, engine

if __name__ == "__main__":

    def make_pipeline(assets):
        pipe = Pipeline(
        columns={
            'price': USEquityPricing.close.latest,
        },
        screen=StaticAssets(assets)
                    )
        return pipe

    etfs = [
        # ----------------------------------------- #
        # SPDRS/State Street Global Advisors (SSGA)
        'XLY',  # Select SPDR U.S. Consumer Discretionary
        'XLP',  # Select SPDR U.S. Consumer Staples
        'XLE',  # Select SPDR U.S. Energy
        'XLF',  # Select SPDR U.S. Financials
        'XLV',  # Select SPDR U.S. Healthcare
        'XLI',  # Select SPDR U.S. Industrials
        'XLB',  # Select SPDR U.S. Materials
        'XLK',  # Select SPDR U.S. Technology
        'XLU',  # Select SPDR U.S. Utilities
        'KRE',  # SPDR S&P Regional Banking ETF
        'KBE',  # SPDR S&P Bank ETF
        'XOP',  # SPDR S&P Oil & Gas Explor & Product
        'GLD',  # SPDR Gold Trust
        'SLV',  # SPDR Silver Trust
        'SPY',  # SPDR S&P 500
        'JNK',  # SPDR Barclays Capital High Yield Bond ETF
        'DIA',  # SPDR Dow Jones Industrial Avg. ETF
        'XHB',  # SPDR Homebuilders ETF
        'MDY',  # SPDR S&P MidCap 400 ETF
        'FEZ',  # SPDR Euro Stoxx 50 ETF
        # ----------------------------------------- #
        # iShares
        'AGG',  # iShares Core U.S. Aggregate Bond ETF
        'IAU',  # iShares Gold Trust
        'IXC',  # iShares Global Energy ETF
        'IWR',  # iShares Russell Mid-Cap ETF
        'IWB',  # iShares Russell 1000 ETF
        'IJR',  # iShares Core S&P Small-Cap ETF
        'IJH',  # iShares Core S&P Mid-Cap ETF
        'EWT',  # iShares MSCI Taiwan ETF
        'EEM',  # iShares MSCI Emerging Markets ETF
        'IWM',  # iShares Russell 2000 ETF
        'EWG',  # iShares MSCI Germany ETF
        'EWJ',  # iShares MSCI Japan ETF
        'EFA',  # iShares MSCI EAFE ETF
        'EWZ',  # iShares MSCI Brazil Capped ETF
        'TLT',  # iShares 20+ Year Treasury Bond ETF
        'INDA',  # iShares MSCI India ETF
        'ECH',  # iShares MSCI Chile Capped ETF
        'EWU',  # iShares MSCI United Kingdom ETF
        'EWI',  # iShares MSCI Italy Capped ETF
        'EWP',  # iShares MSCI Spain Capped ETF
        'EWQ',  # iShares MSCI France ETF
        'EWL',  # iShares MSCI Switzerland Capped ETF
        'EWD',  # iShares MSCI Sweden ETF
        'EWT',  # iShares MSCI Taiwan ETF
        'EWY',  # iShares MSCI South Korea Capped ETF
        'EWA',  # iShares MSCI Australia ETF
        'EWS',  # iShares MSCI Singapore ETF
        'IYM',  # iShares Dow Jones U.S. Basic Materials Index
        'IYK',  # iShares Dow Jones U.S. Consumer Goods Index
        'IYC',  # iShares Dow Jones U.S. Consumer Services Index
        'IYE',  # iShares Dow Jones U.S. Energy Index
        'IYF',  # iShares Dow Jones U.S. Financial Sector Index
        'IYG',  # iShares Dow Jones U.S. Financial Services Index
        'IYH',  # iShares Dow Jones U.S. Healthcare Index
        'IYJ',  # iShares Dow Jones U.S. Industrial Index
        'IYR',  # iShares Dow Jones U.S. Real Estate Index
        'IYW',  # iShares Dow Jones U.S. Technology Index
        'IYZ',  # iShares Dow Jones U.S. Telecommunications Index
        'IYT',  # iShares Dow Jones Transportation Average Index
        'IDU',  # iShares Dow Jones U.S. Utilities Index
        'ICF',  # iShares Cohen & Steers Realty Majors Index
        'AAXJ',  # iShares MSCI All Country Asia ex Japan ETF
        'FXI',  # iShares China Large-Cap ETF
        'ACWI',  # iShares MSCI ACWI ETF
        'EZU',  # iShares MSCI Eurozone ETF
        'EWH',  # iShares MSCI Hong Kong ETF
        'EWM',  # iShares MSCI Malaysia ETF
        # ----------------------------------------- #
        # Vanguard
        'VGK',  # Vanguard FTSE Europe ETF
        'VEA',  # Vanguard Developed Market FTSE
        'VPU',  # Vangaurd Utilities ETF
        'VDE',  # Vanguard Energy ETF
        'VEU',  # Vanguard FTSE All-World ex-US ETF
        'VXUS',  # VanguardTotal Int'l Stock ETF
        'VOO',  # Vanguard S&P 500
        'VO',  # Vanguard Mid-Cap ETF
        'VB',  # Vanguard Small-Cap ETF
        'VOX',  # Vanguard Telecom Services ETF
        # ----------------------------------------- #
        # Market Vectors
        'SMH',  # Market Vectors Semiconductor ETF
        'GDX',  # Market Vectors TR Gold Miners
        'OIH',  # Market Vectors Oil Services ETF
        'RSX',  # Market Vectors Russia ETF
        'GDXJ',  # Market Vectors Junior Gold Miners ETF
        # ----------------------------------------- #
        # Powershares (Invesco)
        'QQQ',  # Powershares (Invesco) NASDAQ 100
        # ----------------------------------------- #
        # Uncategorized
        'AMLP',  # Alerian MLP ETF
        #           'HACK' , # Purefunds ISE Cyber Security ETF
        'FDN',  # First Trust Dow Jones Internet Index ETF
        'HEDJ',  # WisdomTree Europe Hedged Equity ETF
        'EPI']  # WisdomTree India Earnings ETF

    start = datetime(2016, 1, 5, 0, 0, 0, 0, pytz.utc)
    end = datetime(2016, 1, 7, 0, 0, 0, 0, pytz.utc)
    # pipeline engine, Equity() assets
    assets, engine = make_pipeline_engine(symbols=etfs, bundle='etfs_bundle')
    #run pipeline
    pipeline_output = engine.run_pipeline(make_pipeline(assets),start,end)
    print(pipeline_output[:5])





