import pandas as pd

import pytest

from vega_datasets import data
from vega_datasets.utils import connection_ok


skip_if_no_internet = pytest.mark.skipif(not connection_ok(),
                                         reason="No internet connection")


@skip_if_no_internet
def test_download_iris():
    iris = data.iris(use_local=False)
    assert type(iris) is pd.DataFrame
    assert tuple(iris.columns) == ('petalLength', 'petalWidth', 'sepalLength',
                                   'sepalWidth', 'species')

    iris = data.iris.raw(use_local=False)
    assert type(iris) is bytes


def test_stock_date_parsing():
    stocks = data.stocks()
    assert all(stocks.dtypes == ['object', 'datetime64[ns]', 'float64'])


def test_stock_pivoted():
    stocks = data.stocks(pivoted=True)
    assert stocks.index.name == 'date'
    assert all(stocks.columns == ['AAPL', 'AMZN', 'GOOG', 'IBM', 'MSFT'])


@skip_if_no_internet
def test_download_stock_parsing():
    stocks = data.stocks(use_local=False)
    assert all(stocks.dtypes == ['object', 'datetime64[ns]', 'float64'])


@skip_if_no_internet
def test_miserables_parsing():
    miserables = data.miserables()
    assert type(miserables) is tuple
    assert all(type(df) is pd.DataFrame for df in miserables)


@skip_if_no_internet
def test_us_10m_parsing():
    us_10m = data.us_10m()
    assert type(us_10m) is dict


@skip_if_no_internet
def test_world_110m_parsing():
    world_110m = data.world_110m()
    assert type(world_110m) is dict


@skip_if_no_internet
def test_unemployment_tsv():
    unemployment = data.unemployment()
    assert len(unemployment.columns) == 2


@skip_if_no_internet
def test_zipcodes_parsing():
    zipcodes = data.zipcodes()
    assert all(zipcodes.columns == ['zip_code', 'latitude', 'longitude',
                                    'city', 'state', 'county'])
    assert all(zipcodes.dtypes == ['object', 'float64', 'float64',
                                   'object', 'object', 'object'])
