SHELL := /bin/bash

PY2_DIR=.py2
PY3_DIR=.py3
REQUIREMENTS="requirements.txt"

all: test

test:
	py.test --cov-report term-missing --cov=pyvk

vcreate:
	virtualenv --always-copy $(PY2_DIR)
	pyvenv --copies $(PY3_DIR)

vsetup:
	( \
	  . $(PY2_DIR)/bin/activate ; \
	  pip install --upgrade -r $(REQUIREMENTS) ; \
	  deactivate ; \
	  . $(PY3_DIR)/bin/activate ; \
	  pip install --upgrade -r $(REQUIREMENTS) ; \
	  deactivate ; \
	)

vclean:
	rm -rf $(PY2_DIR) $(PY3_DIR)
