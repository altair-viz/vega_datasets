import pytest

from vega_datasets import data, local_data
from vega_datasets.core import Dataset


def test_undefined_dataset():
    with pytest.raises(AttributeError) as err:
        data("blahblahblah")
    assert str(err.value) == "No dataset named 'blahblahblah'"
    with pytest.raises(AttributeError) as err:
        local_data("blahblahblah")
    assert str(err.value) == "No dataset named 'blahblahblah'"


def test_undefined_infodict():
    with pytest.raises(ValueError) as err:
        Dataset._infodict("blahblahblah")
    assert str(err.value).startswith("No such dataset blahblahblah exists")


@pytest.mark.parametrize(
    "name", (set(Dataset.list_datasets()) - set(Dataset.list_local_datasets()))
)
def test_local_dataset_error(name):
    with pytest.raises(ValueError) as err:
        local_data(name)
    assert str(err.value).startswith(
        "'{0}' dataset is not available locally" "".format(name.replace("-", "_"))
    )
