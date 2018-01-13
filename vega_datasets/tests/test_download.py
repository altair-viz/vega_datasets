import pandas as pd

import pytest

from vega_datasets import data, Dataset
from vega_datasets.utils import connection_ok


def test_local_iris():
    assert Dataset('iris').is_local

    iris = data('iris', use_local=True)
    assert type(iris) is pd.DataFrame
    assert tuple(iris.columns) == ('petalLength', 'petalWidth', 'sepalLength',
                                   'sepalWidth', 'species')

    iris = data('iris', use_local=True, return_raw=True)
    assert type(iris) is bytes


@pytest.mark.skipif(not connection_ok(), reason="No internet connection")
def test_download_iris():
    iris = data('iris', use_local=False)
    assert type(iris) is pd.DataFrame
    assert tuple(iris.columns) == ('petalLength', 'petalWidth', 'sepalLength',
                                   'sepalWidth', 'species')

    iris = data('iris', use_local=False, return_raw=True)
    assert type(iris) is bytes
