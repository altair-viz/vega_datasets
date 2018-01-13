1. Update version in vega_datasets/__init__.py to, e.g. 0.2

2. Commit change and push to master

       git add vega_datasets -u
       git commit -m "MAINT: bump version to 0.2"
       git push origin master

3. Tag the release:

       git tag -a v0.2 -m "version 0.2 release"
       git push origin v0.2

4. publish to PyPI (Requires correct PyPI owner permissions)

       python setup.py sdist upload

5. update version in vega_datasets/__init__.py to, e.g. 0.3.0dev0

6. Commit change and push to master

       git add vega_datasets -u
       git commit -m "MAINT: bump version to 0.3.0dev"
       git push origin master

    