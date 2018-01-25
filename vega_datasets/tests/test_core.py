from vega_datasets import data


def test_data_dirlist():
    assert set(dir(data)) == {name.replace('-', '_')
                              for name in data.list_datasets()}
