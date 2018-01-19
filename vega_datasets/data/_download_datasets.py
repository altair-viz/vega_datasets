from os.path import abspath, join, dirname
import sys

sys.path.insert(1, abspath(join(dirname(__file__), '..', '..')))
from vega_datasets import Dataset
from vega_datasets._compat import urlretrieve

DATASETS_TO_DOWNLOAD = ['iris', 'stocks']


def _download_datasets():
    """Utility to download datasets into package source"""
    for name in DATASETS_TO_DOWNLOAD:
        data = Dataset(name)
        url = data.url
        filename = join(abspath(dirname(__file__)), data.filename)
        print("retrieving data {0} -> {1}".format(url, filename))
        urlretrieve(url, filename)


if __name__ == '__main__':
    _download_datasets()
