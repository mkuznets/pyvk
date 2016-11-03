SHELL := /bin/bash

PY2_DIR=.py2
PY3_DIR=.py3
REQUIREMENTS="requirements.txt"
REQUIREMENTS_TEST="requirements-test.txt"

all: test

test:
	coverage run --branch --source pyvk -m py.test
	coverage report -m

vcreate:
	virtualenv --always-copy $(PY2_DIR)
	pyvenv --copies $(PY3_DIR)

vsetup:
	( \
	  . $(PY2_DIR)/bin/activate ; \
	  pip install -U pip ; \
	  pip install -U -r $(REQUIREMENTS) -r $(REQUIREMENTS_TEST) ; \
	  deactivate ; \
	  . $(PY3_DIR)/bin/activate ; \
	  pip install -U pip ; \
	  pip install -U -r $(REQUIREMENTS) -r $(REQUIREMENTS_TEST) ; \
	  deactivate ; \
	)

vclean:
	rm -rf $(PY2_DIR) $(PY3_DIR)
