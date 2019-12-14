from vega_datasets.core import Dataset
from urllib.request import urlopen
from urllib.error import HTTPError, URLError


def connection_ok() -> bool:
    """Check web connection.
    Returns True if web connection is OK, False otherwise.
    """
    try:
        urlopen(Dataset.base_url, timeout=1)
        # if an index page is ever added, this will pass through
        return True
    except HTTPError:
        # There's no index for BASE_URL so Error 404 is expected
        return True
    except URLError:
        # This is raised if there is no internet connection
        return False
