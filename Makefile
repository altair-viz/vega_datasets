test:
	python -m pytest --pyargs vega_datasets --doctest-modules

test-coverage:
	python -m pytest --pyargs vega_datasets --doctest-modules --cov=vega_datasets --cov-report html
