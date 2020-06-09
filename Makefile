# Makefile for the pgetopt Python module

PREVIEW = $$TMPDIR/pgetopt-README.html
PKGMAKE = cd package && $(MAKE)

default: doc test

doc: README.md
# uses the table of contents generator from
# https://github.com/ekalinin/github-markdown-toc.go
README.md: lib/README.md-sans-toc lib/include.py Makefile \
	   readme-toc.tmp readme-errtable.tmp
	rm -f $@
	echo "<!-- GENERATED FILE, DO NOT EDIT -->" > $@
	./lib/include.py $<>>$@
	chmod -w $@

readme-toc.tmp: lib/README.md-sans-toc Makefile
	tail +2 $<| gh-md-toc --hide-header --hide-footer | tail +2 >$@

readme-errtable.tmp: pgetopt.py lib/generrtable.py 
	lib/generrtable.py $<>$@

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
	-rm -rf *.tmp .coverage
	find . \( -name '*~' -o -name __pycache__ \) -exec rm -rf {} +
	cd package && $(MAKE) clean
