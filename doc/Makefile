
all: pgetopts.md

%.md: source/%.source ../lib/include.py ../lib/make-toc ../lib/generrtable.py \
      Makefile
	rm -f $@
	echo "<!-- GENERATED FILE, DO NOT EDIT -->" > $@
	../lib/include.py $<>>$@ || { rm -f $@; exit 1; }
	chmod -w $@

