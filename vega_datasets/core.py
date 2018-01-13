import json
import pkgutil

import pandas as pd

from vega_datasets._compat import urlopen, BytesIO, lru_cache, bytes_decode


class Dataset(object):
    """Class to extract and orgainize information about a dataset

    Parameters
    ----------
    name : string
        The name of the dataset. This should be one of the options available
        in Dataset.list_datasets()

    Attributes
    ----------
    filename : string
        The filename in which the dataset is stored
    url : string
        The full URL of the dataset at http://vega.github.io
    format : string
        The format of the dataset: usually one of {'csv', 'tsv', 'json'}
    pkg_filename : string
        The path to the local dataset within the vega_datasets package
    is_local : bool
        True if the dataset is available locally in the package
    """
    base_url = 'https://vega.github.io/vega-datasets/data/'

    def __init__(self, name):
        info = self._infodict(name)
        self.filename = info['filename']
        self.url = self.base_url + info['filename']
        self.format = info['format']
        self.pkg_filename = 'data/' + self.filename

    @classmethod
    def list_datasets(cls):
        """Return a list of names of available datasets"""
        return sorted(cls._datasets_json().keys())

    @classmethod
    @lru_cache()
    def _datasets_json(cls):
        """load the datasets.json file"""
        datasets = pkgutil.get_data('vega_datasets', 'datasets.json')
        return json.loads(bytes_decode(datasets))

    @classmethod
    @lru_cache()
    def _infodict(cls, name):
        """load the info dictionary for the given name"""
        info = cls._datasets_json().get(name, None)
        if info is None:
            raise ValueError('No such dataset {0} exists, '
                             'use list_datasets() to get a list '
                             'of available datasets.'.format(name))
        return info

    @property
    def is_local(self):
        try:
            pkgutil.get_data('vega_datasets', self.pkg_filename)
        except FileNotFoundError:
            return False
        else:
            return True

    def load(self, return_raw=False, use_local=True):
        """Load the dataset from remote URL or local file

        Parameters
        ----------
        return_raw : boolean
            If True, then return the raw string or bytes.
            If False (default), then return a pandas dataframe.
        use_local : boolean
            If True (default), then attempt to load the dataset locally. If
            False or if the dataset is not available locally, then load the
            data from an external URL.
        """
        if use_local and self.is_local:
            data = BytesIO(pkgutil.get_data('vega_datasets', self.pkg_filename))
        else:
            data = urlopen(self.url)

        if return_raw:
            return data.read()
        elif self.format == 'json':
            return pd.read_json(data)
        elif self.format == 'csv':
            return pd.read_csv(data)
        elif self.format == 'tsv':
            return pd.read_csv(data, sep='\t')
        else:
            raise ValueError("Unrecognized file format: {0}. "
                             "Valid options are ['json', 'csv', 'tsv']."
                             "".format(self.format))


def list_datasets():
    """Return a list of the available dataset names."""
    return Dataset.list_datasets()


def data(name, return_raw=False, use_local=True):
    """Load a dataset from a local file or remote URL.

    Parameters
    ----------
    name : string
        The name of the dataset. This should be one of the options available
        in list_datasets()
    return_raw : boolean
        If True, then return the raw string or bytes.
        If False (default), then return a pandas dataframe.
    use_local : boolean
        If True (default), then attempt to load the dataset locally. If
        False or if the dataset is not available locally, then load the
        data from an external URL.
    """
    return Dataset(name).load(return_raw=return_raw, use_local=use_local)
