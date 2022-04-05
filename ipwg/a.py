# # Image processing with graphs

# A graph is a sparse matrix.  Thus, libraries for doing linear algebra are the
# appropriate tool to deal with graphs.  In this notebook we show how to
# implement some common operations in image processing using a graph formalism.
# In this formalism, images are functions that assign a number to each vertex
# of a grid graph.  Here the graph will always be a grid, but all the
# operations can be defined over an arbitrary graph.
#
# This version of the notebook uses python/numpy.  There are other equivalent
# versions with octave and julia.

# ## Construction of the grid graph

# An image of size $W\times H$ has $n=WH$ pixels.  These are the vertices
# of our grid graph.  The edges connect the—up to four—neighbors of each pixel.
# Thus there are $H$ rows of $W-1$ horizontal edges each, and $W$ columns of
# $H-1$ vertical edges, for a total of $m$ edges

# $$m=H(W-1)+W(H-1)$$

# The following function builds the signed incidence matrix of a $W\times H$
# grid graph.

def incidence_grid(w, h):
	""" Build the signed incidence matrix of a WxH grid graph """
	from scipy.sparse import eye, kron, vstack
	x = eye(w-1, w, 1) - eye(w-1, w)             # path graph of length W
	y = eye(h-1, h, 1) - eye(h-1, h)             # path graph of length H
	Bx = kron(eye(h), x)                         # H horizontal paths
	By = kron(y, eye(w))                         # W vertical paths
	B = vstack([Bx, By])                         # union of all paths
	return B

B = incidence_grid(2,3)

# ## Morphological operators

# ## Local linear operators

# ## Linear differential equations

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
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---



# vim:set tw=79 filetype=python spell spelllang=en:
