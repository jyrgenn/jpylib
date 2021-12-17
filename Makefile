# Makefile for the pgetopt Python module

PREVIEW = tmp/pgetopt.html
TESTINPUT = examples/testdata/input_lines_stdin

default: documentation test

documentation:
	cd doc && $(MAKE)

test:
	python3 -m unittest discover tests < $(TESTINPUT)

coverage:
	coverage run -m unittest discover tests
	coverage report -m

pkg-pgetopt: test
	cd package-pgetopt && $(MAKE) pkg

pkg-jpylib: test
	cd package-jpylib && $(MAKE) pkg

upload-pgetopt:
	cd package-pgetopt && $(MAKE) upload

upload-jpylib:
	cd package-jpylib && $(MAKE) upload

install-pgetopt:
	cd package-pgetopt && $(MAKE) install

install-jpylib:
	cd package-jpylib && $(MAKE) install

preview: doc/pgetopt.md
	markdown doc/pgetopt.md > $(PREVIEW)
	open $(PREVIEW)

clean:
	-rm -rf tmp .coverage
	find . \( -name '*~' -o -name __pycache__ \) -exec rm -rf {} +
	cd package-pgetopt && $(MAKE) clean
	cd package-jpylib && $(MAKE) clean
