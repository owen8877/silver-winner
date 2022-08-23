import secret  # noqa

import qnt.ta as qnta
import qnt.data as qndata
import qnt.backtester as qnbk

import xarray as xr

import datetime as dt


def load_data(period):
    data = qndata.stocks_load_data(min_date=dt.date(2020, 6, 1), max_date=dt.date(2022, 6, 1), tail=period)
    return data


def strategy(data):
    close = data.sel(field='close')
    sma200 = qnta.sma(close, 200).isel(time=-1)
    sma20 = qnta.sma(close, 20).isel(time=-1)
    return xr.where(sma200 < sma20, 1, -1)


qnbk.backtest(
    competition_type="futures",
    load_data=load_data,
    lookback_period=365,
    test_period=2 * 365,
    strategy=strategy
)
