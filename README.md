# vega_datasets

[![build status](http://img.shields.io/travis/altair-viz/vega_datasets/master.svg?style=flat)](https://travis-ci.org/altair-viz/vega_datasets)

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
['7zip', 'airports', 'anscombe', 'barley', 'birdstrikes', 'budget', 'budgets', 'burtin', 'cars', 'climate', 'co2-concentration', 'countries', 'crimea', 'disasters', 'driving', 'earthquakes', 'ffox', 'flare', 'flare-dependencies', 'flights-10k', 'flights-200k', 'flights-20k', 'flights-2k', 'flights-3m', 'flights-5k', 'flights-airport', 'gapminder', 'gapminder-health-income', 'gimp', 'github', 'graticule', 'income', 'iris', 'jobs', 'londonBoroughs', 'londonCentroids', 'londonTubeLines', 'lookup_groups', 'lookup_people', 'miserables', 'monarchs', 'movies', 'normal-2d', 'obesity', 'points', 'population', 'population_engineers_hurricanes', 'seattle-temps', 'seattle-weather', 'sf-temps', 'sp500', 'stocks', 'udistrict', 'unemployment', 'unemployment-across-industries', 'us-10m', 'us-state-capitals', 'weather', 'weball26', 'wheat', 'world-110m', 'zipcodes']
```

To list local datasets (i.e. those that are bundled with the package and can be used without a web connection), use the ``local_data`` object instead:

```python
>>> from vega_datasets import local_data
>>> local_data.list_datasets()

['airports', 'anscombe', 'barley', 'burtin', 'cars', 'crimea', 'driving', 'iris', 'seattle-temps', 'seattle-weather', 'sf-temps', 'stocks']
```

We plan to add more local datasets in the future, subject to size and licensing constraints. See the [local datasets issue](https://github.com/altair-viz/vega_datasets/issues/1) if you would like to help with this.

## Dataset Information

If you want more information about any dataset, you can use the ``description`` property:

```python
>>> data.iris.description
'This classic dataset contains lengths and widths of petals and sepals for 150 iris flowers, drawn from three species. It was introduced by R.A. Fisher in 1936 [1]_.'
```

This information is also part of the ``data.iris`` doc string.
Descriptions are not yet included for all the datasets in the package; we hope to add more information on this in the future.
