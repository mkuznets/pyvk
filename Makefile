SHELL := /usr/bin/env bash

clean:
	rm -rf .coverage .pytest_cache .tox build dist *.egg-info docs/_build

build-cloudflare-pages:
	git fetch --tags
	python -m venv --clear .venv-cf
	.venv-cf/bin/pip install -r requirements-dev.lock
	. .venv-cf/bin/activate && cd docs && make html
