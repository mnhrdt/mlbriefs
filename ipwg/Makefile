SRC = a.py
QMD = $(SRC:.py=.qmd)
HTM = $(SRC:.py=.html)
NTB = $(SRC:.py=.ipynb)

default : $(HTM)
%.html  : %.qmd  ; quarto render $< -o $@
%.qmd   : %.py   ; jupytext $< --to qmd
%.ipynb : %.py   ; jupytext $< --to ipynb

clean   :        ; $(RM) $(QMD) $(HTM) $(NTB) x_*.png
.PRECIOUS: $(QMD)

deploy: $(SRC) a.ipynb
	mv a.ipynb demo/ipwg/main.ipynb
	tar -C demo -zcvhf ../docs/ipwg.tar.gz ipwg
