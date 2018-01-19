import pandas as pd

import pytest

from vega_datasets import data, Dataset
from vega_datasets.utils import connection_ok


skip_if_no_internet = pytest.mark.skipif(not connection_ok(),
                                         reason="No internet connection")


def test_iris_two_ways():
    iris1 = data.iris()
    iris2 = data('iris')
    assert iris1.equals(iris2)


def test_local_iris():
    assert Dataset('iris').is_local

    iris = data.iris(use_local=True)
    assert type(iris) is pd.DataFrame
    assert tuple(iris.columns) == ('petalLength', 'petalWidth', 'sepalLength',
                                   'sepalWidth', 'species')

    iris = data.iris(use_local=True, return_raw=True)
    assert type(iris) is bytes


@skip_if_no_internet
def test_download_iris():
    iris = data.iris(use_local=False)
    assert type(iris) is pd.DataFrame
    assert tuple(iris.columns) == ('petalLength', 'petalWidth', 'sepalLength',
                                   'sepalWidth', 'species')

    iris = data.iris(use_local=False, return_raw=True)
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
