import pytest

from vega_datasets import data
from vega_datasets.core import Dataset


def test_metadata():
    all_datasets = Dataset.list_datasets()
    local_datasets = Dataset.list_local_datasets()
    for name in all_datasets:
        dataobj = getattr(data, name.replace('-', '_'))

        if name in local_datasets:
            # Local datasets should all have a description defined
            assert len(dataobj.description) > 0
            assert len(dataobj.filepath) > 0
        else:
            with pytest.raises(ValueError) as err:
                path = dataobj.filepath
            assert str(err.value) == "filepath is only valid for local datasets"

        # Descriptions should either be defined, or be None
        assert dataobj.description is None or len(dataobj.description) > 0

        # References should either be a list, or be None
        assert dataobj.references is None or type(dataobj.references) is list
