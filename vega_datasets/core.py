import os
import json

import pandas as pd

from vega_datasets._compat import lru_cache
from vega_datasets._compat import URLError, HTTPError, urlopen


BASE_URL = 'https://vega.github.io/vega-datasets/data/'
    

@lru_cache()
def _datasets_json():
    json_file = os.path.join(os.path.dirname(__file__), 'datasets.json')
    with open(json_file) as f:
        return json.loads(f.read())


@lru_cache()
def _dataset_info(name):
    dataset_info = _datasets_json().get(name, None)
    if dataset_info is None:
        raise ValueError('No such dataset {0} exists, '
                         'use list_datasets to get a list'.format(name))
    return dataset_info

def dataset_info(name):
    # return a copy of the lru_cached object in case the user modifies it
    return _dataset_info(name).copy()


def dataset_url(name):
    dataset_info = _dataset_info(name)    
    return BASE_URL + dataset_info['filename']


def dataset_format(name):
    dataset_info = _dataset_info(name)
    return dataset_info['format']


def list_datasets():
    """List the available datasets."""
    return sorted(_datasets_json().keys())


def _download_dataset(name):
    """Load a dataset by name as a pandas.DataFrame.

    The dataset is cached within each Python session using lru_cache.

    Parameters
    ----------
    name : string
        The name of the dataset, which must match one of the names in
        vega_datasets.list_datasets()

    Returns
    -------
    response : HTTPResponse
        The HTTP response (response.read() will yield the raw dataset contents)
    format : string
        The dataset format (i.e. 'json', 'csv', 'tsv')
    """
    dataset_info = _dataset_info(name)    
    url = BASE_URL + dataset_info['filename']
    fmt = dataset_info['format']

    return urlopen(url), fmt
    
    
def data(name, return_raw=False):
    """Load a dataset by name"""
    response, fmt = _download_dataset(name)
    
    if return_raw:
        return response.read()
    elif fmt == 'json':
        return pd.read_json(response)
    elif fmt == 'csv':
        return pd.read_csv(response)
    elif fmt == 'tsv':
        return pd.read_csv(response, sep='\t')
    else:
        raise ValueError("Unrecognized file format: {0}. "
                         "Valid options are ['json', 'csv', 'tsv']."
                         "".format(fmt))
