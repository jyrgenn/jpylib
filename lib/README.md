;; -*- text -*-

The lib/ directory
==================

Here are some files used in the build and test processes.

`README.md`: this README file.

`_morgue/`: obsolete/historic files; currently an aborted attempt to
implement an own testing mechanism. That pretty soon showed that the
effort would be just too much compared to an existing testing
framework. Actually, I am quite happy with Python's `unittest`
framework now.

`doop`: a program used in the process tests.

`generrtable.py`: error table generator for the pgetops README.

`include.py`: include file processor for the pgetops README.

`jpylib`: a symlink to the jpylib under development, for the benefit
of `include.py`.

`make-toc`: table of contents generator for the doc file(s to be).

`read-secrets`: alternate secrets reader implementation to test
against.

`secrets`: secrets example file for testing. Don't exert yourself,
the secrets in there are no longer used (or have never been)
elsewhere.

`read-secrets.py`: alternate secrets reader implementation to test
against.

`testconfig.conf`, `testconfig2.conf`, `testconfig3.conf`,
`testconfig5.conf`: test input for the config reader tests.
