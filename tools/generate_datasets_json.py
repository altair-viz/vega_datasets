"""Tool to re-generate and save vega_datasets/datasets.json

Usage:
$ python generate_datasets_json.py v1.24.0

The second argument is the name of the desired version tag within
http://github.com/vega/vega-datasets/
"""

import json
import os
import subprocess
import sys


def main(tag):
    cwd = os.path.dirname(__file__)
    datasets_src = os.path.join(cwd, "vega-datasets")
    if not os.path.exists(datasets_src):
        print("Cloning vega-datsets...")
        subprocess.check_call(
            ["git", "clone", "http://github.com/vega/vega-datasets.git"], cwd=cwd
        )
    print(f"Checking out '{tag}'")
    subprocess.check_call(["git", "checkout", tag], cwd=datasets_src)

    data_dir = os.path.abspath(os.path.join(datasets_src, "data"))
    datasets_file = os.path.abspath(
        os.path.join(cwd, "..", "vega_datasets", "datasets.json")
    )
    core_file = os.path.abspath(os.path.join(cwd, "..", "vega_datasets", "core.py"))

    print(f"Extracting datasets from {data_dir}")
    datasets = {}
    for filename in os.listdir(data_dir):
        name, fmt = os.path.splitext(filename)
        datasets[name] = {"filename": filename, "format": fmt[1:]}

    print(f"Writing datsets to {datasets_file}")
    with open(datasets_file, "w") as f:
        json.dump(datasets, f, indent=2, sort_keys=True)

    print("Updating SOURCE_TAG in core file")
    subprocess.check_call(
        ["sed", "-i", ".bak", f"s/SOURCE_TAG.*/SOURCE_TAG = {tag!r}/g", core_file]
    )
    subprocess.check_call(["rm", f"{core_file}.bak"])


if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print(__doc__)
