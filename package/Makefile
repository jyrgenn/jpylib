# create and maybe upload a package for the vrf-mlg library

MODULE = pgetopt
PKGNAME = pgetopt-jyrgenn
PKGVERS = $(shell date +%Y.%m%d.%H%M | sed 's/\.00*/./g')
#PYPIUPLD = https://test.pypi.org/legacy/
PYPIUPLD = https://upload.pypi.org/legacy/
#PYPIDNLD = https://test.pypi.org/simple/
PYPIDNLD = https://pypi.org/simple/
PRODUCTS = $(MODULE) *.egg-info build dist \
           $(shell find . -name __pycache__)
PYPICRED = -u jyrgenn -p $$(getsecret pypi/jyrgenn)

default:
	@echo This Makefile has no actionable default target.
	@echo "Use 'pkg' to build the package, 'upload' to upload."

# create the package; ensure old versions are gone (they are a pain
# when twine tries to upload dist/* to the package repository)
pkg: copy
	-rm -f dist/*
	PKG_VERSION=$(PKGVERS) python3 setup.py sdist bdist_wheel
	git diff --exit-code --raw && \
          git tag -a -m "created package version $(PKGVERS)" v$(PKGVERS) || \
	  { printf "\nthere are uncommitted changes!\n\n"; exit 1 ; }
	git push --tags

# copy the actual module in place; set the version number in a variable
copy:
	mkdir -p $(MODULE)
	sed 's/\$$__package_version\$$/$(PKGVERS)/g' ../$(MODULE).py \
	    > $(MODULE)/__init__.py

upload:
	python3 -m twine upload $(PYPICRED) --repository-url $(PYPIUPLD) dist/*

install:
	python3 -m pip install -U --index-url $(PYPIDNLD) --no-deps $(PKGNAME)

clean:
	-rm -rf $(PRODUCTS) *~
