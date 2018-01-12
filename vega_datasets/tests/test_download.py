import pandas as pd
from vega_datasets import data, Dataset


def test_local_iris():
    assert Dataset('iris').is_local
    
    iris = data('iris', use_local=True)
    assert type(iris) is pd.DataFrame
    assert tuple(iris.columns) == ('petalLength', 'petalWidth', 'sepalLength',
                                   'sepalWidth', 'species')

def test_download_iris():
    iris = data('iris', use_local=False)
    assert type(iris) is pd.DataFrame
    assert tuple(iris.columns) == ('petalLength', 'petalWidth', 'sepalLength',
                                   'sepalWidth', 'species')
