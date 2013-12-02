#
# Based on Makefile from https://github.com/mitsuhiko/flask/blob/master/Makefile
# at SHA-1: afd3c4532b8625729bed9ed37a3eddd0b7b3b5a9
#
.PHONY: clean-pyc test upload-docs docs

all: clean-pyc clean-docs test tox-test docs

clean: clean-pyc clean-docs

test:
	nosetests

tox-test:
	tox

release:
	python scripts/make-release.py

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

docs:
	$(MAKE) -C doc html
	
clean-docs:
	$(MAKE) -C doc clean

love:
	@echo not war
