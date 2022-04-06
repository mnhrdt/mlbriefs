SRC = a.py
QMD = $(SRC:.py=.qmd)
HTM = $(SRC:.py=.html)

default : $(HTM)
%.html  : %.qmd  ; quarto render $< -o $@
%.qmd   : %.py   ; jupytext $< --to qmd

clean   :        ; $(RM) $(QMD) $(HTM) x_*.png
.PRECIOUS: $(QMD)
