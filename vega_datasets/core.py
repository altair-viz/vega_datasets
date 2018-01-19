import os
import json
import pkgutil

import pandas as pd

from vega_datasets._compat import urlopen, BytesIO, lru_cache, bytes_decode


class Dataset(object):
    """Class to load a particular dataset by name"""

    _instance_doc = """Loader for the {name} dataset.

    Usage:

        >>> from vega_datasets import data
        >>> df = data.{methodname}()

    Equivalently, you can use

        >>> df = data('{name}')

    To get the raw dataset rather than the dataframe, use

        >>> df_bytes = data.{methodname}.raw()

    To find the dataset url, use

        >>> data.{methodname}.url
        '{url}'
    {additional_docs}
    Attributes
    ----------
    filename : string
        The filename in which the dataset is stored
    url : string
        The full URL of the dataset at http://vega.github.io
    format : string
        The format of the dataset: usually one of {{'csv', 'tsv', 'json'}}
    pkg_filename : string
        The path to the local dataset within the vega_datasets package
    is_local : bool
        True if the dataset is available locally in the package
    filepath : string
        If is_local is True, the local file path to the dataset.
    """
    _additional_docs = ""
    base_url = 'https://vega.github.io/vega-datasets/data/'

    @classmethod
    def init(cls, name):
        clsdict = {subcls.name: subcls for subcls in cls.__subclasses__()
                   if hasattr(subcls, 'name')}
        return clsdict.get(name, cls)(name)

    def __init__(self, name):
        info = self._infodict(name)
        self.name = name
        self.methodname = name.replace('-', '_')
        self.filename = info['filename']
        self.url = self.base_url + info['filename']
        self.format = info['format']
        self.pkg_filename = 'data/' + self.filename
        self.__doc__ = self._instance_doc.format(additional_docs=self._additional_docs,
                                                 **self.__dict__)

    @classmethod
    def list_datasets(cls):
        """Return a list of names of available datasets"""
        return sorted(cls._datasets_json().keys())

    @classmethod
    @lru_cache()
    def local_datasets(cls):
        listing = pkgutil.get_data('vega_datasets', 'data/listing.txt')
        return bytes_decode(listing).split()

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
        return self.name in self.local_datasets()

    def raw(self, use_local=True):
        """Load the raw dataset from remote URL or local file

        Parameters
        ----------
        use_local : boolean
            If True (default), then attempt to load the dataset locally. If
            False or if the dataset is not available locally, then load the
            data from an external URL.
        """
        if use_local and self.is_local:
            return pkgutil.get_data('vega_datasets', self.pkg_filename)
        else:
            return urlopen(self.url).read()

    def dataframe(self, use_local=True, **kwargs):
        """Load the dataset from remote URL or local file

        Parameters
        ----------
        use_local : boolean
            If True (default), then attempt to load the dataset locally. If
            False or if the dataset is not available locally, then load the
            data from an external URL.
        **kwargs :
            additional keyword arguments are passed to pd.read_json() or
            pd.read_csv(), depending on the format of the data source
        """
        datasource = BytesIO(self.raw(use_local))

        if self.format == 'json':
            return pd.read_json(datasource, **kwargs)
        elif self.format == 'csv':
            return pd.read_csv(datasource, **kwargs)
        elif self.format == 'tsv':
            kwargs['sep'] = '\t'
            return pd.read_csv(datasource, sep='\t', **kwargs)
        else:
            raise ValueError("Unrecognized file format: {0}. "
                             "Valid options are ['json', 'csv', 'tsv']."
                             "".format(self.format))

    __call__ = dataframe

    @property
    def filepath(self):
        if not self.is_local:
            raise ValueError("filepath is only valid for local datasets")
        else:
            return os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                'data', self.filename))


class Stocks(Dataset):
    name = 'stocks'
    _additional_docs = """
    The stocks dataset supports pivoted output using the `pivoted` keyword,
    which defaults to False:

        >>> df_pivoted = data.stocks(pivoted=True)
    """

    def dataframe(self, pivoted=False, use_local=True, **kwargs):
        if 'parse_dates' not in kwargs:
            kwargs['parse_dates'] = ['date']
        data = super(Stocks, self).dataframe(use_local=use_local, **kwargs)
        if pivoted:
            data = data.pivot(index='date', columns='symbol', values='price')
        return data

    __call__ = dataframe


class DataLoader(object):
    """Load a dataset from a local file or remote URL.

    There are two ways to call this; for example to load the iris dataset, you
    can call this object and pass the dataset name by string:

        >>> from vega_datasets import data
        >>> df = data('iris')

    or you can call the associated named method:

        >>> df = data.iris()

    Optionally, additional parameters can be passed to either of these

    Optional parameters
    -------------------
    return_raw : boolean
        If True, then return the raw string or bytes.
        If False (default), then return a pandas dataframe.
    use_local : boolean
        If True (default), then attempt to load the dataset locally. If
        False or if the dataset is not available locally, then load the
        data from an external URL.
    **kwargs :
        additional keyword arguments are passed to the pandas parsing function,
        either ``read_csv()`` or ``read_json()`` depending on the data format.
    """
    _datasets = {name.replace('-', '_'): name for name in Dataset.list_datasets()}

    def list_datasets(self):
        return Dataset.list_datasets()

    def __call__(self, name, return_raw=False, use_local=True, **kwargs):
        loader = getattr(self, name.replace('-', '_'))
        if return_raw:
            return loader.raw(use_local=use_local, **kwargs)
        else:
            return loader(use_local=use_local, **kwargs)

    def __getattr__(self, dataset_name):
        if dataset_name in self._datasets:
            return Dataset.init(self._datasets[dataset_name])
        else:
            raise AttributeError("No dataset named '{0}'".format(dataset_name))

    def __dir__(self):
        return list(self._datasets.keys())
