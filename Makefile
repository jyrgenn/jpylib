# Makefile for the pgetopt Python module

PREVIEW = tmp/pgetopt-README.html

default: doc test

doc: README-pgetopt.md
# uses the table of contents generator from
# https://github.com/ekalinin/github-markdown-toc.go
README-pgetopt.md: lib/README-pgetopt.md-sans-toc lib/include.py Makefile \
	   tmp/readme-pgetopt-toc tmp/readme-pgetopt-errtable
	rm -f $@
	echo "<!-- GENERATED FILE, DO NOT EDIT -->" > $@
	./lib/include.py $<>>$@
	chmod -w $@

tmp/readme-pgetopt-toc: lib/README-pgetopt.md-sans-toc Makefile tmp
	tail +2 $<| gh-md-toc --hide-header --hide-footer | tail +2 >$@

tmp/readme-pgetopt-errtable: jpylib/pgetopt.py lib/generrtable.py tmp
	lib/generrtable.py $<>$@

test:
	python3 -m unittest discover tests

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

preview: README.md
	markdown README-pgetopt.md > $(PREVIEW)
	open $(PREVIEW)

tmp:
	mkdir tmp

clean:
	-rm -rf tmp .coverage
	find . \( -name '*~' -o -name __pycache__ \) -exec rm -rf {} +
	cd package-pgetopt && $(MAKE) clean
	cd package-jpylib && $(MAKE) clean
