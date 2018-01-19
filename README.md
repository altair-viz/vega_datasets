# vega_datasets

[![build status](http://img.shields.io/travis/jakevdp/vega_datasets/master.svg?style=flat)](https://travis-ci.org/jakevdp/vega_datasets)

A Python package for offline access to [vega datasets](https://github.com/vega/vega-datasets).

This package has several goals:

- Provide straightforward access to the datasets in [vega-datasets](https://github.com/vega/vega-datasets).
- return the results in the form of a Pandas dataframe.
- wherever dataset size and/or license constraints make it possible, bundle the dataset with the package so that datasets can be loaded in the absence of a web connection.

## Installation

```
$ pip install vega_datasets
```