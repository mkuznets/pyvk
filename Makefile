SHELL := /usr/bin/env bash

test:
	coverage run --branch --source pyvk -m pytest
	coverage report -m

.PHONY: test
