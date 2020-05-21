
default:
	@echo This Makefile has no actionable default target.


test:
	./test.py

pkg:
	cd package && $(MAKE) pkg

upload:
	cd package && $(MAKE) upload
