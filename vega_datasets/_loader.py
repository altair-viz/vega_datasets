from vega_datasets._dataset import Dataset


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

    def _method_factory(self, name):
        def get_dataset(return_raw=False, use_local=True, **kwargs):
            return self._load_dataset(self._datasets[name],
                                      return_raw=return_raw,
                                      use_local=use_local,
                                      **kwargs)
        return get_dataset

    def _load_dataset(self, name, **kwargs):
        return Dataset(name).load(**kwargs)

    def __call__(self, name, return_raw=False, use_local=True, **kwargs):
        loader = getattr(self, name.replace('-', '_'))
        return loader(return_raw=False, use_local=True, **kwargs)

    def __getattr__(self, attr):
        if attr in self._datasets:
            return self._method_factory(attr)
        else:
            raise AttributeError("No dataset named '{0}'".format(attr))

    def __dir__(self):
        return list(self._datasets.keys())

    #--------------------------------------------------------------------------
    # specialized methods for individual datasets that need specific processing
    def stocks(self, pivoted=False, return_raw=False, use_local=True,
               parse_dates=('date',), **kwargs):
        """A time-series of stock prices from several tech companies

        Parameters
        ----------
        pivoted : boolean
            If True, then pivot the data so each company is in its own column.
            Not referenced if return_raw is True.
        """
        if type(parse_dates) is tuple:
            parse_dates=list(parse_dates)
        data = self._load_dataset('stocks',
                                  return_raw=return_raw,
                                  use_local=use_local,
                                  parse_dates=parse_dates, **kwargs)
        if pivoted and not return_raw:
            data = data.pivot(index='date', columns='symbol', values='price')
        return data
