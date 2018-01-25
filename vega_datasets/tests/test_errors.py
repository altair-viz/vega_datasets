import pytest

from vega_datasets import data
from vega_datasets.core import Dataset


def test_undefined_dataset():
    with pytest.raises(AttributeError) as err:
        data('blahblahblah')
    assert str(err.value) == "No dataset named 'blahblahblah'"


def test_undefined_infodict():
    with pytest.raises(ValueError) as err:
        info = Dataset._infodict('blahblahblah')
    assert str(err.value).startswith('No such dataset blahblahblah exists')
