# Makefile for the pgetopt Python module

PREVIEW = tmp/pgetopt.html


default: documentation test

release: documentation test coverage pkg upload

pdoc:
	python3 -m pdoc jpylib

documentation:
	cd doc && $(MAKE)

test:
	python3 -m unittest discover tests

coverage:
	python3 -m coverage run -m unittest discover tests
	python3 -m coverage report -m

pkg: test
	cd package && $(MAKE) pkg

upload:
	cd package && $(MAKE) upload

install:
	cd package && $(MAKE) install

preview:
	cd doc && $(MAKE)
	markdown doc/pgetopt.md > $(PREVIEW)
	open $(PREVIEW)

clean:
	-rm -rf tmp .coverage
	find . \( -name '*~' -o -name __pycache__ \) -exec rm -rf {} +
	cd package && $(MAKE) clean
