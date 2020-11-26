Change Log
==========

Release v0.9 (Nov 26, 2020)
---------------------------
- Change urls to use jsDelivr (a fast CDN) with a fixed version number, instead of GitHub.
  This fixes the URLs broken by the vega-datasets 2.0 release.

Release v0.8 (Dec 14, 2019)
---------------------------
- Include all data from [vega-datasets v1.29.0](https://github.com/vega/vega-datasets/releases/tag/v1.29.0)
- Add ohlc to local datasets

Release v0.7 (Dec 7, 2018)
-------------------------
- Add wheat to local datasets

Release v0.6 (November 20, 2018)
-------------------------
- Add us-unemployment local dataset

Release v0.5 (May 15, 2018)
---------------------------
- Add iowa-electricity local dataset

Release v0.4.1 (March 15, 2018)
-------------------------------
- Move package to altair-viz organization
- Add MANIFEST.in to include all relevant files in build artifact

Release v0.4 (February 25, 2018)
--------------------------------
- Added ``vega_datasets.local_data`` object to more easily use local-only data
- Removed ``data.list_local_datasets()`` in favor of ``local_data.list_datsets()``
- Changed handling of "miserables", "us-10m", and "world-110m" datasets to return valid non-dataframe results rather than raising a ValueError.
- Re-synced with the vega-datasets repository to add access to a few dozen more datasets

Release v0.3 (January 24, 2018)
-------------------------------
- Added dataset_info.json to store all descriptions and references in one location. Docstrings are automatically constructed from this file.
- Added default date conversions for a number of datasets
- Bundled several more datasets: [airports, anscombe, barley, burtin, crimea]

Release v0.2 (January 19, 2018)
-------------------------------
- Substantial API changes, including ability to tab-complete dataset names
- Added individualized dataset doc strings
- bundled datasets: [iris, stocks, cars, seattle-temps, seattle-weather, sf-temps]

Release v0.1 (January 12, 2018)
-------------------------------

- Initial release with simple API
- bundled datasets: iris
