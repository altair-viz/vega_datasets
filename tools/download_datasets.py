"""
Tool to download all local datasets and save them within the vega_datasets
source tree.

Usage:
$ python download_datasets.py
"""

from os.path import abspath, join, dirname
import sys
import json

sys.path.insert(1, abspath(join(dirname(__file__), '..')))
from vega_datasets.core import Dataset
from vega_datasets._compat import urlretrieve

DATASETS_TO_DOWNLOAD = ['airports',
                        'anscombe',
                        'barley',
                        'burtin',
                        'cars',
                        'crimea',
                        'driving',
                        'iowa-electricity',
                        'iris',
                        'la-riots',
                        'seattle-temps',
                        'seattle-weather',
                        'sf-temps',
                        'stocks']


def _download_datasets():
    """Utility to download datasets into package source"""
    def filepath(*args):
        return abspath(join(dirname(__file__), '..', 'vega_datasets', *args))
    dataset_listing = {}
    for name in DATASETS_TO_DOWNLOAD:
        data = Dataset(name)
        url = data.url
        filename = filepath('_data', data.filename)
        print("retrieving data {0} -> {1}".format(url, filename))
        urlretrieve(url, filename)
        dataset_listing[name] = '_data/{0}'.format(data.filename)
    with open(filepath('local_datasets.json'), 'w') as f:
        json.dump(dataset_listing, f, indent=2)


if __name__ == '__main__':
    _download_datasets()
