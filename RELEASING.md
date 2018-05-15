1. Update version in vega_datasets/__init__.py to, e.g. 0.5

2. Make sure CHANGES.md is up to date for the release

3. Commit change and push to master

       git add . -u
       git commit -m "MAINT: bump version to 0.5"
       git push origin master

4. Tag the release:

       git tag -a v0.5 -m "version 0.5 release"
       git push origin v0.5

5. Build the distributions

       rm -r dist build  # clean old builds & distributions
       python setup.py sdist  # create a source distribution
       python setup.py bdist_wheel  # create a universal wheel

6. publish to PyPI (Requires correct PyPI owner permissions)

       twine upload dist/*

7. update version in vega_datasets/__init__.py to, e.g. 0.6.0dev0

8. add a new changelog entry for the unreleased version

9. Commit change and push to master

       git add . -u
       git commit -m "MAINT: bump version to 0.6.0dev"
       git push origin master


10. Update the conda-forge package with a pull request to
    http://github.com/conda-forge/vega_datasets-feedstock

    