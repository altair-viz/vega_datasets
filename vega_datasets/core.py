import os
import json
import pkgutil

import pandas as pd

from vega_datasets._compat import URLError, HTTPError, urlopen


class Dataset(object):
    """Class to extract and orgainize information about a dataset"""
    base_url = 'https://vega.github.io/vega-datasets/data/'
    data_path = os.path.join(os.path.dirname(__file__), 'data')

    def __init__(self, name):
        info = self._infodict(name)
        self.filename = info['filename']
        self.url = self.base_url + info['filename']
        self.format = info['format']
        self.pkgutil_filename = 'data/' + self.filename

    @property
    def is_local(self):
        try:
            pkgutil.get_data('vega_datasets', self.pkgutil_filename)
        except FileNotFoundError:
            return False
        else:
            return True

    @classmethod
    def _datasets_json(cls):
        datasets = pkgutil.get_data('vega_datasets', 'datasets.json')
        return json.loads(datasets)

    @classmethod
    def _infodict(cls, name):
        info = cls._datasets_json().get(name, None)
        if info is None:
            raise ValueError('No such dataset {0} exists, '
                             'use list_datasets() to get a list '
                             'of available datasets.'.format(name))
        return info

    def load(self, return_raw=False, use_local=True):
        if use_local and self.is_local:
            data = pkgutil.get_data('vega_datasets', self.pkgutil_filename)
            if return_raw:
                return data
        else:
            data = urlopen(self.url)
            if return_raw:
                return data.read()

        if self.format == 'json':
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
    """List the available datasets."""
    return sorted(Dataset._datasets_json().keys())


def data(name, return_raw=False, use_local=True):
    """Load a dataset by name"""
    return Dataset(name).load(return_raw=return_raw, use_local=use_local)
