SHELL := /usr/bin/env bash

test:
	pytest --cov-branch --cov=pyvk ./tests
	coverage report -m

clean:
	rm -rf .coverage .pytest_cache .tox build dist *.egg-info docs/_build

.PHONY: test
