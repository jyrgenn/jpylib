# Makefile for the pgetopt Python module

PREVIEW = $$TMPDIR/pgetopt-README.html
PKGMAKE = cd package && $(MAKE)

default: doc

doc: README.md
# uses the table of contents generator from
# https://github.com/ekalinin/github-markdown-toc.go
README.md: lib/README.md-sans-toc Makefile
	gh-md-toc --hide-header --hide-footer $< | tail +2 > README.toc
	./lib/include.py $<>$@

test:
	./tests/run-tests.py

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
	-rm -rf *~ README.toc __pycache__
	cd package && $(MAKE) clean
