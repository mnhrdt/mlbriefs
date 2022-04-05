a.html: a.qmd
	quarto render a.qmd -o a.html

a.qmd: a.py
	jupytext a.py --to qmd

clean:
	$(RM) a.qmd a.html
