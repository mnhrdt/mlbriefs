PDF  = $(shell ls *.tex | sed 's/\.tex/.pdf/')

pdf: $(PDF)

%.pdf : %.tex
	cat $< | grep ^%SCRIPT | cut -c9- | bash
	cat $< | pdflatexfilter > $@

clean :
	$(RM) $(PDF)
