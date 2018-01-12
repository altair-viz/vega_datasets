import pandas as pd
from vega_datasets import data


def test_download():
    iris = data('iris')
    assert type(iris) is pd.DataFrame

    assert tuple(iris.columns) == ('petalLength', 'petalWidth', 'sepalLength',
                                   'sepalWidth', 'species')
