from vega_datasets import data, local_data
from vega_datasets.core import Dataset


def test_data_dirlist():
    assert set(dir(data)) == {name.replace('-', '_')
                              for name in data.list_datasets()}

def test_local_data_dirlist():
    assert set(dir(local_data)) == {name.replace('-', '_')
                                    for name in Dataset.list_local_datasets()}
