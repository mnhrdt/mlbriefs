# ---
# format:
#     html:
#         self-contained: true
# jupyter:
#   jupytext:
#     formats: py:light,qmd
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.7
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # Title of the notebook

import iio
from IPython.display import display,Image

x = iio.read("f/barbara.png")

x.shape

# Some math $\int_\Omega d\omega=\int_{\partial\Omega}\omega$

display(Image("f/barbara.png"))


