import os

import pandas as pd
from zipline.data import bundles as bundles_module
from zipline_binance import create_bundle, register, CurrencyPair

# adjust the following lines to your needs
start_session = pd.Timestamp('2018-01-05', tz='utc')
end_session = pd.Timestamp('2018-01-31', tz='utc')


register(
    'binance',
    create_bundle(
        [CurrencyPair(quote='ETH', base='BTC'), CurrencyPair(quote='XLM', base='BTC')],
        start_session,
        end_session,
    ),
    calendar_name='POLONIEX',
    minutes_per_day=24 * 60,
    start_session=start_session,
    end_session=end_session
)

if __name__ == '__main__':
    bundle = 'binance'

    bundles_module.ingest(
        bundle,
        os.environ,
        pd.Timestamp.utcnow(),
        (),
        True
    )
