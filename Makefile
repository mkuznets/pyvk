SHELL := /usr/bin/env bash

test:
	pytest --cov-branch --cov=pyvk ./tests
	coverage report -m

.PHONY: test
