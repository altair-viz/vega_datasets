from io import BytesIO
import os
import json
import pkgutil
import textwrap
from typing import Any, Dict, Iterable, List
from urllib.request import urlopen
import pandas as pd

# This is the tag in http://github.com/vega/vega-datasets from
# which the datasets in this repository are sourced.
SOURCE_TAG = "v1.29.0"


def _load_dataset_info() -> Dict[str, Dict[str, Any]]:
    """This loads dataset info from three package files:

    vega_datasets/datasets.json
    vega_datasets/dataset_info.json
    vega_datasets/local_datasets.json

    It returns a dictionary with dataset information.
    """

    def load_json(path: str) -> Dict[str, Any]:
        raw = pkgutil.get_data("vega_datasets", path)
        if raw is None:
            raise ValueError("Cannot locate package path vega_datasets:{}".format(path))
        return json.loads(raw.decode())

    info = load_json("datasets.json")
    descriptions = load_json("dataset_info.json")
    local_datasets = load_json("local_datasets.json")

    for name in info:
        info[name]["is_local"] = name in local_datasets
    for name in descriptions:
        info[name].update(descriptions[name])

    return info


class Dataset(object):
    """Class to load a particular dataset by name"""

    _instance_doc = """Loader for the {name} dataset.

    {data_description}

    {bundle_info}
    Dataset source: {url}

    Usage
    -----

        >>> from vega_datasets import data
        >>> {methodname} = data.{methodname}()
        >>> type({methodname})
        {return_type}

    Equivalently, you can use

        >>> {methodname} = data('{name}')

    To get the raw dataset rather than the dataframe, use

        >>> data_bytes = data.{methodname}.raw()
        >>> type(data_bytes)
        bytes

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

    {reference_info}
    """
    _additional_docs = ""
    _reference_info = """
    For information on this dataset, see https://github.com/vega/vega-datasets/
    """
    base_url = "https://cdn.jsdelivr.net/npm/vega-datasets@" + SOURCE_TAG + "/data/"
    _dataset_info = _load_dataset_info()
    _pd_read_kwds = {}  # type: Dict[str, Any]
    _return_type = pd.DataFrame

    @classmethod
    def init(cls, name: str) -> "Dataset":
        """Return an instance of this class or an appropriate subclass"""
        clsdict = {
            subcls.name: subcls
            for subcls in cls.__subclasses__()
            if hasattr(subcls, "name")
        }
        return clsdict.get(name, cls)(name)

    def __init__(self, name: str):
        info = self._infodict(name)
        self.name = name
        self.methodname = name.replace("-", "_")
        self.filename = info["filename"]
        self.url = self.base_url + info["filename"]
        self.format = info["format"]
        self.pkg_filename = "_data/" + self.filename
        self.is_local = info["is_local"]
        self.description = info.get("description", None)
        self.references = info.get("references", None)
        self.__doc__ = self._make_docstring()

    def _make_docstring(self) -> str:
        info = self._infodict(self.name)

        # construct, indent, and line-wrap dataset description
        description = info.get("description", "")
        if not description:
            description = (
                "This dataset is described at " "https://github.com/vega/vega-datasets/"
            )
        wrapper = textwrap.TextWrapper(
            width=70, initial_indent="", subsequent_indent=4 * " "
        )
        description = "\n".join(wrapper.wrap(description))

        # construct, indent, and join references
        reflist = info.get("references", [])  # type: Iterable[str]
        reflist = (".. [{0}] ".format(i + 1) + ref for i, ref in enumerate(reflist))
        wrapper = textwrap.TextWrapper(
            width=70, initial_indent=4 * " ", subsequent_indent=7 * " "
        )
        reflist = ("\n".join(wrapper.wrap(ref)) for ref in reflist)
        references = "\n\n".join(reflist)  # type: str
        if references.strip():
            references = "References\n    ----------\n" + references

        # add information about bundling of data
        if self.is_local:
            bundle_info = (
                "This dataset is bundled with vega_datasets; "
                "it can be loaded without web access."
            )
        else:
            bundle_info = (
                "This dataset is not bundled with vega_datasets; "
                "it requires web access to load."
            )

        return self._instance_doc.format(
            additional_docs=self._additional_docs,
            data_description=description,
            reference_info=references,
            bundle_info=bundle_info,
            return_type=self._return_type,
            **self.__dict__
        )

    @classmethod
    def list_datasets(cls) -> List[str]:
        """Return a list of names of available datasets"""
        return sorted(cls._dataset_info.keys())

    @classmethod
    def list_local_datasets(cls) -> List[str]:
        return sorted(
            name for name, info in cls._dataset_info.items() if info["is_local"]
        )

    @classmethod
    def _infodict(cls, name: str) -> Dict[str, str]:
        """load the info dictionary for the given name"""
        info = cls._dataset_info.get(name, None)
        if info is None:
            raise ValueError(
                "No such dataset {0} exists, "
                "use list_datasets() to get a list "
                "of available datasets.".format(name)
            )
        return info

    def raw(self, use_local: bool = True) -> bytes:
        """Load the raw dataset from remote URL or local file

        Parameters
        ----------
        use_local : boolean
            If True (default), then attempt to load the dataset locally. If
            False or if the dataset is not available locally, then load the
            data from an external URL.
        """
        if use_local and self.is_local:
            out = pkgutil.get_data("vega_datasets", self.pkg_filename)
            if out is not None:
                return out
            raise ValueError(
                "Cannot locate package path vega_datasets:{}".format(self.pkg_filename)
            )
        else:
            return urlopen(self.url).read()

    def __call__(self, use_local: bool = True, **kwargs) -> pd.DataFrame:
        """Load and parse the dataset from remote URL or local file

        Parameters
        ----------
        use_local : boolean
            If True (default), then attempt to load the dataset locally. If
            False or if the dataset is not available locally, then load the
            data from an external URL.
        **kwargs :
            additional keyword arguments are passed to data parser (usually
            pd.read_csv or pd.read_json, depending on the format of the data
            source)

        Returns
        -------
        data :
            parsed data
        """
        datasource = BytesIO(self.raw(use_local=use_local))

        kwds = self._pd_read_kwds.copy()
        kwds.update(kwargs)

        if self.format == "json":
            return pd.read_json(datasource, **kwds)
        elif self.format == "csv":
            return pd.read_csv(datasource, **kwds)
        elif self.format == "tsv":
            kwds.setdefault("sep", "\t")
            return pd.read_csv(datasource, **kwds)
        else:
            raise ValueError(
                "Unrecognized file format: {0}. "
                "Valid options are ['json', 'csv', 'tsv']."
                "".format(self.format)
            )

    @property
    def filepath(self) -> str:
        if not self.is_local:
            raise ValueError("filepath is only valid for local datasets")
        else:
            return os.path.abspath(
                os.path.join(os.path.dirname(__file__), "_data", self.filename)
            )


class Stocks(Dataset):
    name = "stocks"
    _additional_docs = """
    For convenience, the stocks dataset supports pivoted output using the
    optional `pivoted` keyword. If pivoted is set to True, each company's
    price history will be returned in a separate column:

        >>> df = data.stocks()  # not pivoted
        >>> df.head(3)
          symbol       date  price
        0   MSFT 2000-01-01  39.81
        1   MSFT 2000-02-01  36.35
        2   MSFT 2000-03-01  43.22

        >>> df_pivoted = data.stocks(pivoted=True)
        >>> df_pivoted.head()
        symbol       AAPL   AMZN  GOOG     IBM   MSFT
        date
        2000-01-01  25.94  64.56   NaN  100.52  39.81
        2000-02-01  28.66  68.87   NaN   92.11  36.35
        2000-03-01  33.95  67.00   NaN  106.11  43.22
    """
    _pd_read_kwds = {"parse_dates": ["date"]}

    def __call__(self, pivoted=False, use_local=True, **kwargs):
        """Load and parse the dataset from remote URL or local file

        Parameters
        ----------
        pivoted : boolean, default False
            If True, then pivot data so that each stock is in its own column.
        use_local : boolean
            If True (default), then attempt to load the dataset locally. If
            False or if the dataset is not available locally, then load the
            data from an external URL.
        **kwargs :
            additional keyword arguments are passed to data parser (usually
            pd.read_csv or pd.read_json, depending on the format of the data
            source)

        Returns
        -------
        data : DataFrame
            parsed data
        """
        __doc__ = super(Stocks, self).__call__.__doc__  # noqa:F841
        data = super(Stocks, self).__call__(use_local=use_local, **kwargs)
        if pivoted:
            data = data.pivot(index="date", columns="symbol", values="price")
        return data


class Cars(Dataset):
    name = "cars"
    _pd_read_kwds = {"convert_dates": ["Year"]}


class Climate(Dataset):
    name = "climate"
    _pd_read_kwds = {"convert_dates": ["DATE"]}


class Github(Dataset):
    name = "github"
    _pd_read_kwds = {"parse_dates": ["time"]}


class IowaElectricity(Dataset):
    name = "iowa-electricity"
    _pd_read_kwds = {"parse_dates": ["year"]}


class LARiots(Dataset):
    name = "la-riots"
    _pd_read_kwds = {"parse_dates": ["death_date"]}


class Miserables(Dataset):
    name = "miserables"
    _return_type = tuple
    _additional_docs = """
    The miserables data contains two dataframes, ``nodes`` and ``links``,
    both of which are returned from this function.
    """

    def __call__(self, use_local=True, **kwargs):
        __doc__ = super(Miserables, self).__call__.__doc__  # noqa:F841
        dct = json.loads(self.raw(use_local=use_local).decode(), **kwargs)
        nodes = pd.DataFrame.from_records(dct["nodes"], index="index")
        links = pd.DataFrame.from_records(dct["links"])
        return nodes, links


class SeattleTemps(Dataset):
    name = "seattle-temps"
    _pd_read_kwds = {"parse_dates": ["date"]}


class SeattleWeather(Dataset):
    name = "seattle-weather"
    _pd_read_kwds = {"parse_dates": ["date"]}


class SFTemps(Dataset):
    name = "sf-temps"
    _pd_read_kwds = {"parse_dates": ["date"]}


class Sp500(Dataset):
    name = "sp500"
    _pd_read_kwds = {"parse_dates": ["date"]}


class UnemploymentAcrossIndustries(Dataset):
    name = "unemployment-across-industries"
    _pd_read_kwds = {"convert_dates": ["date"]}


class US_10M(Dataset):
    name = "us-10m"
    _return_type = dict
    _additional_docs = """
    The us-10m dataset is a TopoJSON file, with a structure that is not
    suitable for storage in a dataframe. For this reason, the loader returns
    a simple Python dictionary.
    """

    def __call__(self, use_local=True, **kwargs):
        __doc__ = super(US_10M, self).__call__.__doc__  # noqa:F841
        return json.loads(self.raw(use_local=use_local).decode(), **kwargs)


class World_110M(Dataset):
    name = "world-110m"
    _return_type = dict
    _additional_docs = """
    The world-100m dataset is a TopoJSON file, with a structure that is not
    suitable for storage in a dataframe. For this reason, the loader returns
    a simple Python dictionary.
    """

    def __call__(self, use_local=True, **kwargs):
        __doc__ = super(World_110M, self).__call__.__doc__  # noqa:F841
        return json.loads(self.raw(use_local=use_local).decode(), **kwargs)


class ZIPCodes(Dataset):
    name = "zipcodes"
    _pd_read_kwds = {"dtype": {"zip_code": "object"}}


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

    _datasets = {name.replace("-", "_"): name for name in Dataset.list_datasets()}

    def list_datasets(self):
        return Dataset.list_datasets()

    def __call__(self, name, return_raw=False, use_local=True, **kwargs):
        loader = getattr(self, name.replace("-", "_"))
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


class LocalDataLoader(DataLoader):
    _datasets = {name.replace("-", "_"): name for name in Dataset.list_local_datasets()}

    def list_datasets(self):
        return Dataset.list_local_datasets()

    def __getattr__(self, dataset_name):
        if dataset_name in self._datasets:
            return Dataset.init(self._datasets[dataset_name])
        elif dataset_name in DataLoader._datasets:
            raise ValueError(
                "'{0}' dataset is not available locally. To "
                "download it, use ``vega_datasets.data.{0}()"
                "".format(dataset_name)
            )
        else:
            raise AttributeError("No dataset named '{0}'".format(dataset_name))
