all: install

install:
	python setup.py install

test:
	python -m pytest --pyargs vega_datasets --doctest-modules

test-coverage:
	python -m pytest --pyargs vega_datasets --doctest-modules --cov=vega_datasets --cov-report term

test-coverage-html:
	python -m pytest --pyargs vega_datasets --doctest-modules --cov=vega_datasets --cov-report html
