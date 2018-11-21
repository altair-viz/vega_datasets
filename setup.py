import io
import os
import re

from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))


def read(path, encoding='utf-8'):
    path = os.path.join(here, path)
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


setup(name="vega_datasets",
      version=version('vega_datasets/__init__.py'),
      description="A Python package for offline access to Vega datasets",
      long_description=read('README.md'),
      long_description_content_type="text/markdown",
      author="Jake VanderPlas",
      author_email="jakevdp@gmail.com",
      maintainer="Jake VanderPlas",
      maintainer_email="jakevdp@gmail.com",
      url='http://github.com/altair-viz/vega_datasets',
      download_url='http://github.com/altair-viz/vega_datasets',
      license="MIT",
      install_requires=["pandas"],
      tests_require=["pytest"],
      packages=find_packages(exclude=['tools']),
      package_data={
          'vega_datasets': ['datasets.json',
                            'dataset_info.json',
                            'local_datasets.json',
                            os.path.join('_data', '*.json'),
                            os.path.join('_data', '*.csv'),
                            os.path.join('_data', '*.tsv'),
          ]
      },
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
      ],
      project_urls={
          'Bug Reports': 'https://github.com/altair-viz/vega_datasets/issues',
          'Source': 'https://github.com/altair-viz/vega_datasets',
      },
)
