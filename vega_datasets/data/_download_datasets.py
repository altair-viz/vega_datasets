from os.path import abspath, join, dirname
import sys

sys.path.insert(1, abspath(join(dirname(__file__), '..', '..')))
from vega_datasets import dataset_url
from vega_datasets._compat import urlretrieve

DATASETS_TO_DOWNLOAD = ['iris']


def _download_datasets():
    """Utility to download datasets into package source"""
    for name in DATASETS_TO_DOWNLOAD:
        url = dataset_url(name)
        filename = join(abspath(dirname(__file__)), url.split('/')[-1])
        print("retrieving data {0} -> {1}".format(url, filename))
        urlretrieve(url, filename)


if __name__ == '__main__':
    _download_datasets()
