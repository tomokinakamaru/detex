.PHONY: all
all: setup

.PHONY: setup
setup: venv/bin/flake8 venv/bin/mypy
	venv/bin/pip install .

.PHONY: test
test: venv/bin/tox
	venv/bin/tox

.PHONY: clean
clean:
	rm -rf venv .coverage .tox htmlcov *.egg-info
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete

venv:
	python3 -m venv venv --without-pip

venv/bin/pip: venv
	curl -sfS https://bootstrap.pypa.io/get-pip.py | venv/bin/python

venv/bin/flake8: venv/bin/pip
	venv/bin/pip install flake8

venv/bin/mypy: venv/bin/pip
	venv/bin/pip install mypy

venv/bin/tox: venv/bin/pip
	venv/bin/pip install tox
