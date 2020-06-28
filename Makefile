SHELL := /usr/bin/env bash

test:
	coverage run --branch --source pyvk -m py.test
	coverage report -m

.PHONY: test
