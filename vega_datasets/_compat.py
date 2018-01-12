# Python 2/3 compatibility

try:
    from urllib.error import URLError, HTTPError
    from urllib.request import urlopen, urlretrieve
except ImportError:
    # Python 2.X
    from urllib2 import URLError, HTTPError, urlopen
    from urllib import urlretrieve

try:
    from functools import lru_cache
except ImportError:
    # Python 2.X: function not available
    lru_cache = lambda maxsize=128, typed=False: (lambda y: y)
