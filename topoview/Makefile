PDF  = $(shell ls *.tex | sed 's/\.tex/.pdf/')

pdf: $(PDF)

%.pdf : %.tex
	#./.process_verbatims $<
	grep ^%SCRIPT $< | cut -c9- | sh
	cat $< | pdflatexfilter > $@

clean :
	$(RM) $(PDF) f/*.png
