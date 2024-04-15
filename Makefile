SHELL := /usr/bin/env bash

clean:
	rm -rf .coverage .pytest_cache .tox build dist *.egg-info docs/_build

build-cloudflare-pages:
	git fetch --tags
	git fetch --unshallow
	python -m venv --clear .venv-cf
	.venv-cf/bin/pip install -U -r requirements-dev.lock
	. .venv-cf/bin/activate && cd docs && make html
