all: install

install:
	python setup.py install

test:
	black .
	python -m flake8 vega_datasets
	python -m mypy vega_datasets
	rm -r build
	python setup.py build &&\
	  cd build/lib &&\
	  python -m pytest --pyargs --doctest-modules vega_datasets

test-coverage:
	python setup.py build &&\
	  cd build/lib &&\
	  python -m pytest --pyargs --doctest-modules --cov=vega_datasets --cov-report term vega_datasets

test-coverage-html:
	python setup.py build &&\
	  cd build/lib &&\
	  python -m pytest --pyargs --doctest-modules --cov=vega_datasets --cov-report html vega_datasets
