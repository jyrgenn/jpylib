PREVIEW =  $$TMPDIR/pgetopt-README.html

default:
	@echo This Makefile has no actionable default target.


test:
	./test.py

pkg:
	cd package && $(MAKE) pkg

upload:
	cd package && $(MAKE) upload

install:
	cd package && $(MAKE) install

preview:
	markdown README.md > $(PREVIEW)
	open $(PREVIEW)

clean:
	-rm -rf *~
	cd package && $(MAKE) clean
