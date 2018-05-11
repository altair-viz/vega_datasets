import pandas as pd
import pytest

from vega_datasets import data, local_data
from vega_datasets.core import Dataset


@pytest.mark.parametrize('name', Dataset.list_local_datasets())
def test_load_local_dataset(name):
    loader = getattr(data, name.replace('-', '_'))
    local_loader = getattr(local_data, name.replace('-', '_'))

    df1 = data(name)
    df2 = loader()  # equivalent to data.dataset_name()
    df3 = local_data(name)
    df4 = local_loader()  # equivalent to local_data.dataset_name()
    assert df1.equals(df2)
    assert df1.equals(df3)
    assert df1.equals(df4)

    raw1 = loader.raw()
    raw2 = local_loader.raw()
    raw3 = data(name, return_raw=True)
    raw4 = local_data(name, return_raw=True)
    assert raw1 == raw2 == raw3 == raw4
    assert type(raw1) is type(raw2) is type(raw3) is type(raw4) is bytes


def test_iris_column_names():
    iris = data.iris()
    assert type(iris) is pd.DataFrame
    assert tuple(iris.columns) == ('petalLength', 'petalWidth', 'sepalLength',
                                   'sepalWidth', 'species')

    iris = data.iris.raw()
    assert type(iris) is bytes


def test_stocks_column_names():
    stocks = data.stocks()
    assert type(stocks) is pd.DataFrame
    assert tuple(stocks.columns) == ('symbol', 'date', 'price')

    stocks = data.stocks.raw()
    assert type(stocks) is bytes


def test_cars_column_names():
    cars = data.cars()
    assert type(cars) is pd.DataFrame
    assert tuple(cars.columns) == ('Acceleration', 'Cylinders', 'Displacement',
                                   'Horsepower', 'Miles_per_Gallon', 'Name',
                                   'Origin', 'Weight_in_lbs', 'Year')

    cars = data.cars.raw()
    assert type(cars) is bytes


@pytest.mark.parametrize('name,col', [('cars', 'Year',), ('stocks', 'date'),
                                      ('la-riots', 'death_date'),
                                      ('iowa-electricity', 'year'),
                                      ('seattle-weather', 'date'),
                                      ('seattle-temps', 'date'),
                                      ('sf-temps', 'date')])
def test_date_types(name, col):
    assert data(name)[col].dtype == 'datetime64[ns]'
