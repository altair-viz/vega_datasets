import pandas as pd

import pytest

from vega_datasets import data, Dataset
from vega_datasets._compat import urlopen, HTTPError, URLError

def connection_ok():
    """Check web connection.
    Returns True if web connection is OK, False otherwise.
    """
    try:
        response = urlopen(Dataset.base_url, timeout=1)
        # if an index page is ever added, this will pass through
        return True
    except HTTPError:
        # There's no index for BASE_URL so Error 404 is expected
        return True
    except URLError:
        # This is raised if there is no internet connection
        return False


def test_local_iris():
    assert Dataset('iris').is_local

    iris = data('iris', use_local=True)
    assert type(iris) is pd.DataFrame
    assert tuple(iris.columns) == ('petalLength', 'petalWidth', 'sepalLength',
                                   'sepalWidth', 'species')

@pytest.mark.skipif(not connection_ok(), reason="No internet connection")
def test_download_iris():
    iris = data('iris', use_local=False)
    assert type(iris) is pd.DataFrame
    assert tuple(iris.columns) == ('petalLength', 'petalWidth', 'sepalLength',
                                   'sepalWidth', 'species')
