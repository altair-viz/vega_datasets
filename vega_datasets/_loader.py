from vega_datasets._dataset import Dataset


class DataLoader(object):
    """Load a dataset from a local file or remote URL.

    There are two ways to call this; for example to load the iris dataset, you
    can call this object and pass the dataset name by string:

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
        def get_dataset(return_raw=False, use_local=True):
            return self(self._datasets[name], return_raw=return_raw, use_local=use_local)
        return get_dataset

    def __call__(self, name, return_raw=False, use_local=True, **kwds):
        return Dataset(name).load(return_raw=return_raw, use_local=use_local, **kwds)

    def __getattr__(self, attr):
        if attr in self._datasets:
            return self._method_factory(attr)
        else:
            raise AttributeError("No dataset named '{0}'".format(attr))

    def __dir__(self):
        return list(self._datasets.keys())
