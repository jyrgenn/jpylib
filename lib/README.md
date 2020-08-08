;; -*- text -*-

The lib/ directory
==================

Here are some files used in the build and test processes.

`README-pgetopt.source`: source of the pgetops README, with includes
for the ToC and the errors table, both of which are generated.

`README.md`: this README file.

`_morgue/`: obsolete/historic files; currently an aborted attempt to
implement an own testing mechanism. That pretty soon showed that the
effort would be just too much compared to an existing testing
framework. Actually, I am quite happy with Python's `unittest`
framewor now.

`doop`: a program used in the process tests.

`generrtable.py`: error table generator for the pgetops README.

`include.py`: include file processor for the pgetops README.

`secrets`: secrets example file for testing. Don't exert yourself,
the secrets in there are no longer used (or have never been)
elsewhere.

`read-secrets.py`: alternate secrets reader implementation to test
against.

`testconfig.conf`, `testconfig2.conf`, `testconfig3.conf`,
`testconfig5.conf`: test input for the config reader tests.
