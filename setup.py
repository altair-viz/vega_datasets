import io
import os
import re

from setuptools import setup


def read(path, encoding='utf-8'):
    path = os.path.join(os.path.dirname(__file__), path)
    with io.open(path, encoding=encoding) as fp:
        return fp.read()


def version(path):
    """Obtain the packge version from a python file e.g. pkg/__init__.py
    See <https://packaging.python.org/en/latest/single_source_version.html>.
    """
    version_file = read(path)
    version_match = re.search(r"""^__version__ = ['"]([^'"]*)['"]""",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


DESCRIPTION = "A Python package for offline access to Vega datasets"
LONG_DESCRIPTION = """
A Python package for offline access to Vega datasets available at
https://github.com/vega/vega-datasets.

This package has several goals:

- Provide straightforward access to the datasets in vega-datasets
- return the results in the form of a Pandas dataframe.
- wherever dataset size and/or license constraints make it possible, bundle the dataset with the package so that datasets can be loaded in the absence of a web connection.

Development at http://github.com/altair-viz/vega_datasets
"""
NAME = "vega_datasets"
AUTHOR = "Jake VanderPlas"
AUTHOR_EMAIL = "jakevdp@gmail.com"
MAINTAINER = "Jake VanderPlas"
MAINTAINER_EMAIL = "jakevdp@gmail.com"
URL = 'http://github.com/altair-viz/vega_datasets'
DOWNLOAD_URL = 'http://github.com/altair-viz/vega_datasets'
LICENSE = 'MIT'

VERSION = version('vega_datasets/__init__.py')

setup(name=NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      maintainer=MAINTAINER,
      maintainer_email=MAINTAINER_EMAIL,
      url=URL,
      download_url=DOWNLOAD_URL,
      license=LICENSE,
      install_requires=["pandas"],
      tests_require=["pytest"],
      packages=['vega_datasets',
                'vega_datasets.tests',
            ],
      package_data={'vega_datasets': ['datasets.json',
                                      'dataset_info.json',
                                      'local_datasets.json',
                                      os.path.join('data', '*.json'),
                                      os.path.join('data', '*.csv'),
                                      os.path.join('data', '*.tsv')]},
      classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'],
     )
