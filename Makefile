# Makefile for the pgetopt Python module

PREVIEW = $$TMPDIR/pgetopt-README.html
PKGMAKE = cd package && $(MAKE)

default: doc

doc: README.md
# uses the table of contents generator from
# https://github.com/ekalinin/github-markdown-toc.go
README.md: lib/README.md-sans-toc lib/include.py Makefile README.toc
	./lib/include.py $<>$@

README.toc: lib/README.md-sans-toc
	gh-md-toc --hide-header --hide-footer $< | tail +2 > README.toc

test:
	python3 -m unittest discover tests

coverage:
	coverage run -m unittest discover tests
	coverage report -m

pkg:
	$(PKGMAKE) pkg

upload:
	$(PKGMAKE) upload

install:
	$(PKGMAKE) install

preview: README.md
	markdown README.md > $(PREVIEW)
	open $(PREVIEW)

clean:
	-rm -rf README.toc
	find . \( -name '*~' -o -name __pycache__ \) -exec rm -rf {} +
	cd package && $(MAKE) clean
