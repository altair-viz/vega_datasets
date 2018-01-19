# vega_datasets

[![build status](http://img.shields.io/travis/jakevdp/vega_datasets/master.svg?style=flat)](https://travis-ci.org/jakevdp/vega_datasets)

A Python package for offline access to [vega datasets](https://github.com/vega/vega-datasets).

This package has several goals:

- Provide straightforward access in Python to the datasets made available at [vega-datasets](https://github.com/vega/vega-datasets).
- return the results in the form of a Pandas dataframe.
- wherever dataset size and/or license constraints make it possible, bundle the dataset with the package so that datasets can be loaded in the absence of a web connection.

Currently the package bundles a half-dozen datasets, and falls back to using HTTP requests for the others.

## Installation

```
$ pip install vega_datasets
```

## Usage

The main object in this library is ``data``:

```python
>>> from vega_datasets import data
```

It contains attributes that access all available datasets, locally if
available. For example, here is the well-known iris dataset:

```python
>>> df = data.iris()
>>> df.head()
   petalLength  petalWidth  sepalLength  sepalWidth species
0          1.4         0.2          5.1         3.5  setosa
1          1.4         0.2          4.9         3.0  setosa
2          1.3         0.2          4.7         3.2  setosa
3          1.5         0.2          4.6         3.1  setosa
4          1.4         0.2          5.0         3.6  setosa
```

If you're curious about the source data, you can access the URL for any of the available datasets:

```python
>>> data.iris.url
'https://vega.github.io/vega-datasets/data/iris.json'
```

For datasets bundled with the package, you can also find their location on disk:

```python
>>> data.iris.filepath
'/lib/python3.6/site-packages/vega_datasets/data/iris.json'
```

## Available Datasets

To list all the available datsets, use ``list_datsets``:

```python
>>> data.list_datasets()
['airports', 'anscombe', 'barley', 'birdstrikes', 'budget', 'budgets', 'burtin', 'cars', 'climate', 'countries', 'crimea', 'driving', 'flare', 'flights-10k', 'flights-20k', 'flights-2k', 'flights-3m', 'flights-5k', 'flights-airport', 'gapminder', 'gapminder-health-income', 'github', 'iris', 'jobs', 'miserables', 'monarchs', 'movies', 'points', 'population', 'seattle-temps', 'seattle-weather', 'sf-temps', 'sp500', 'stocks', 'unemployment-across-industries', 'us-10m', 'weather', 'weball26', 'wheat', 'world-110m']
```

To list local datasets (i.e. those that are bundled with the package and can be used without a web connection), use ``list_local_datasets``:

```python
>>> data.list_local_datasets()
['cars', 'iris', 'seattle-temps', 'seattle-weather', 'sf-temps', 'stocks']
```

We plan to add more local datasets in the future.