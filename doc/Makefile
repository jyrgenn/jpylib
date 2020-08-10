
all: pgetopt.md

%.md: source/%.source ../lib/include.py ../lib/make-toc Makefile
	rm -f $@
	echo "<!-- GENERATED FILE, DO NOT EDIT -->" > $@
	../lib/include.py $<>>$@ || { rm -f $@; exit 1; }
	chmod -w $@

