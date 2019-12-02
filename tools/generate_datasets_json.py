"""Tool to re-generate and save vega_datasets/datasets.json

Usage:
$ python generate_datasets_json.py /path/to/vega-datasets

The provided path should be to the local clone of
http://github.com/vega/vega-datasets/
"""

import os
import sys
import json


def main(vega_datasets_package):
    data_dir = os.path.join(vega_datasets_package, 'data')
    datasets_file = os.path.join(os.path.dirname(__file__),
                                 '..', 'vega_datasets',
                                 'datasets.json')

    datasets = {}
    for filename in os.listdir(data_dir):
        name, fmt = os.path.splitext(filename)
        datasets[name] = {'filename': filename, 'format': fmt[1:]}

    with open(datasets_file, 'w') as f:
        json.dump(datasets, f, indent=2, sort_keys=True)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print(__doc__)
