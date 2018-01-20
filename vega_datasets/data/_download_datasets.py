from os.path import abspath, join, dirname
import sys

sys.path.insert(1, abspath(join(dirname(__file__), '..', '..')))
from vega_datasets.core import Dataset
from vega_datasets._compat import urlretrieve

DATASETS_TO_DOWNLOAD = ['anscombe', 'iris', 'stocks', 'cars',
                        'seattle-temps', 'sf-temps', 'seattle-weather']


def _download_datasets():
    """Utility to download datasets into package source"""
    def filepath(*args):
        return abspath(join(dirname(__file__), *args))
    for name in DATASETS_TO_DOWNLOAD:
        data = Dataset(name)
        url = data.url
        filename = filepath(data.filename)
        print("retrieving data {0} -> {1}".format(url, filename))
        urlretrieve(url, filename)
    with open(filepath('listing.txt'), 'w') as f:
        f.write('\n'.join(DATASETS_TO_DOWNLOAD) + '\n')


if __name__ == '__main__':
    _download_datasets()
