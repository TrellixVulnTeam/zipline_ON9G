import os
from pandas import Timestamp
from zipline.data.bundles import load
from zipline.data.data_portal import DataPortal
from zipline.utils.calendars import get_calendar

from datetime import datetime
import pandas as pd
import pytz
from zipline_binance import create_bundle, register, CurrencyPair

# adjust the following lines to your needs
start_session = pd.Timestamp('2018-01-01', tz='utc')
end_session = pd.Timestamp('2018-01-31', tz='utc')

register(
    'binance',
    create_bundle(
        [CurrencyPair(quote='XLM', base='BTC'),
         CurrencyPair(quote='ETH', base='BTC')],
        start_session,
        end_session,
    ),
    calendar_name='POLONIEX',
    minutes_per_day=24 * 60,
    start_session=start_session,
    end_session=end_session
)


now = Timestamp(datetime(2018, 1, 25, 10, tzinfo=pytz.UTC))
# print('now=', now)

# instantiate zipline data objects
# https://github.com/quantopian/zipline/issues/2023

bundle = load('binance', os.environ, now)
calendar = get_calendar('NYSE')
dp = DataPortal(
    bundle.asset_finder,
    calendar,
    first_trading_day=bundle.equity_minute_bar_reader.first_trading_day,
    equity_minute_reader=bundle.equity_minute_bar_reader,
    equity_daily_reader=bundle.equity_daily_bar_reader,
    adjustment_reader=bundle.adjustment_reader
)

# get apple equity and timeseries
i = bundle.asset_finder.lookup_symbol('ETH-BTC', now)
ts = dp.get_history_window(
    [i],
    now,
    bar_count=50,
    frequency='1m',
    field='close',
    data_frequency='minute'
)

print(ts[0])
# # this should be populated
# print('AAPL_asset_name=', i.asset_name)
#
# # this shouldn't have NaNs
# print('AAPL_timeseries=', ts[0])