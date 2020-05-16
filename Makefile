help:
	@echo "clean - clean build, pyc, test, coverage"
	@echo "clean-all - clean build, pyc, test, coverage, eggs"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-test - remove pytest cache"
	@echo "clean-cov - remove coverage artifacts"
	@echo "clean-eggs - remove cached eggs"
	@echo "build - build so file from pyx"
	@echo "install - install implements and dependencies"
	@echo "install-all - install implements, dependencies and dev packages"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "test-all - run tests on every Python version with tox"
	@echo "version - show package version"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "release - package and upload a release"
	@echo "dist - package"

.PHONY: clean
clean: clean-build clean-pyc clean-test clean-cov

.PHONY: clean
clean-all: clean clean-eggs

.PHONY: clean-build
clean-build:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info

.PHONY: clean-pyc
clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

.PHONY: clean-test
clean-test:
	rm -rf __pycache__/
	rm -rf .pytest_cache/

.PHONY: clean-cov
clean-cov:
	rm -f .coverage
	rm -rf htmlcov/

.PHONY: clean-eggs
clean-eggs:
	rm -rf .eggs/

.PHONY: build
build: clean-build clean-eggs
	python3 setup.py build_ext --inplace

.PHONY: install
install: clean-build clean-eggs
	python3 setup.py install

.PHONY: install-all
install-all:
	pip install -e .[all_packages]

.PHONY: lint
lint:
	pytest --flake8 implements.py tests.py

.PHONY: test
test:
	python3 setup.py test

.PHONY: test-all
test-all:
	tox

.PHONY: version
version:
	python3 setup.py --version

.PHONY: coverage
coverage:
	coverage run --source implements setup.py test
	coverage report -m
	coverage html
	xdg-open htmlcov/index.html

.PHONY: docs
docs:
	rm -f docs/implements.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ implements
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	xdg-open docs/_build/html/index.html

.PHONY: release
release: clean build
	python setup.py sdist bdist_wheel
	twine upload dist/*

.PHONY: dist
dist: clean build
	python3 setup.py sdist
	python3 setup.py bdist_wheel
	ls -l dist
