# vega_datasets

[![build status](http://img.shields.io/travis/altair-viz/vega_datasets/master.svg?style=flat)](https://travis-ci.org/altair-viz/vega_datasets)
[![github actions](https://github.com/altair-viz/vega_datasets/workflows/build/badge.svg)](https://github.com/altair-viz/vega_datasets/actions?query=workflow%3Abuild)
[![github actions](https://github.com/altair-viz/vega_datasets/workflows/lint/badge.svg)](https://github.com/altair-viz/vega_datasets/actions?query=workflow%3Alint)
[![code style black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A Python package for offline access to [vega datasets](https://github.com/vega/vega-datasets).

This package has several goals:

- Provide straightforward access in Python to the datasets made available at [vega-datasets](https://github.com/vega/vega-datasets).
- return the results in the form of a Pandas dataframe.
- wherever dataset size and/or license constraints make it possible, bundle the dataset with the package so that datasets can be loaded in the absence of a web connection.

Currently the package bundles a half-dozen datasets, and falls back to using HTTP requests for the others.

## Installation
``vega_datasets`` is compatible with Python 3.5 or newer. Install with:
```
$ pip install vega_datasets
```

## Usage

The main object in this library is ``data``:

```python
>>> from vega_datasets import data
```

It contains attributes that access all available datasets, locally if
available. For example, here is the [Palmer penguins](https://github.com/allisonhorst/palmerpenguins) dataset:

```python
>>> df = data.penguins()
>>> df.head()
  Species     Island  Beak Length (mm)  Beak Depth (mm)  Flipper Length (mm)  Body Mass (g)     Sex
0  Adelie  Torgersen              39.1             18.7                181.0         3750.0    MALE
1  Adelie  Torgersen              39.5             17.4                186.0         3800.0  FEMALE
2  Adelie  Torgersen              40.3             18.0                195.0         3250.0  FEMALE
3  Adelie  Torgersen               NaN              NaN                  NaN            NaN    None
4  Adelie  Torgersen              36.7             19.3                193.0         3450.0  FEMALE
```

If you're curious about the source data, you can access the URL for any of the available datasets:

```python
>>> data.penguins.url
'https://cdn.jsdelivr.net/npm/vega-datasets@2.1.0/data/penguins.json'
```

For datasets bundled with the package, you can also find their location on disk:

```python
>>> data.penguins.filepath
'/lib/python3.8/site-packages/vega_datasets/data/penguins.json'
```

## Available Datasets

To list all the available datsets, use ``list_datasets``:

```python
>>> data.list_datasets()
['7zip', 'airports', 'annual-precip', 'anscombe', 'barley', 'birdstrikes', 'budget', 'budgets', 'burtin', 'cars', 'co2-concentration', 'countries', 'crimea', 'disasters', 'driving', 'earthquakes', 'ffox', 'flare', 'flare-dependencies', 'flights-10k', 'flights-200k', 'flights-20k', 'flights-2k', 'flights-3m', 'flights-5k', 'flights-airport', 'football', 'gapminder', 'gapminder-health-income', 'gimp', 'github', 'income', 'iowa-electricity', 'jobs', 'la-riots', 'londonBoroughs', 'londonCentroids', 'londonTubeLines', 'lookup_groups', 'lookup_people', 'miserables', 'monarchs', 'movies', 'normal-2d', 'obesity', 'ohlc', 'penguins', 'points', 'political-contributions', 'population', 'population_engineers_hurricanes', 'seattle-weather', 'seattle-weather-hourly-normals', 'sp500', 'stocks', 'udistrict', 'unemployment', 'unemployment-across-industries', 'uniform-2d', 'us-10m', 'us-employment', 'us-state-capitals', 'volcano', 'weather', 'wheat', 'windvectors', 'world-110m', 'zipcodes']
```

To list local datasets (i.e. those that are bundled with the package and can be used without a web connection), use the ``local_data`` object instead:

```python
>>> from vega_datasets import local_data
>>> local_data.list_datasets()
['airports', 'anscombe', 'barley', 'burtin', 'cars', 'crimea', 'driving', 'iowa-electricity', 'la-riots', 'ohlc', 'penguins', 'seattle-weather', 'seattle-weather-hourly-normals', 'stocks', 'us-employment', 'wheat']
```

We plan to add more local datasets in the future, subject to size and licensing constraints. See the [local datasets issue](https://github.com/altair-viz/vega_datasets/issues/1) if you would like to help with this.

## Dataset Information

If you want more information about any dataset, you can use the ``description`` property:

```python
>>> data.penguins.description
'Palmer Archipelago (Antarctica) penguin data collected and made available by Dr. Kristen Gorman and the Palmer Station, Antarctica LTER, a member of the Long Term Ecological Research Network. For more information visit https://github.com/allisonhorst/penguins.'
```

This information is also part of the ``data.penguins`` doc string.
Descriptions are not yet included for all the datasets in the package; we hope to add more information on this in the future.
