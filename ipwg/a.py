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

# The following function builds the signed *incidence matrix* of a $W\times H$
# grid graph.  It is a matrix of $n$ columns and $m$ rows.

def grid_incidence(h, w):
	""" Build the signed incidence matrix of a WxH grid graph """
	from scipy.sparse import eye, kron, vstack
	x = eye(w-1, w, 1) - eye(w-1, w)             # path graph of length W
	y = eye(h-1, h, 1) - eye(h-1, h)             # path graph of length H
	Bx = kron(eye(h), x)                         # H horizontal paths
	By = kron(y, eye(w))                         # W vertical paths
	B = vstack([Bx, By])                         # union of all paths
	return B

# A similar construction builds the *adjacency matrix*, which is square of size
# $n$.

def grid_adjacency(h, w):
	""" Build the adjacency matrix of a WxH grid graph """
	from scipy.sparse import eye, kronsum
	x = eye(w, w, 1)                             # oriented path of length W
	y = eye(h, h, 1)                             # oriented path of length H
	G = kronsum(x, y)                            # graph product
	A = G + G.T                                  # symmetrization
	return A

# We will also construct the *Laplacian matrix* of the graph, defined as
# $L=-B^\top B$.  There are many algebraic relationships between the Laplacian,
# adjacency and incidence matrices.
# The matrices $A$ and $L$ are square, each row of these matrices
# corresponding to one pixel of the original image domain.  Since these
# matrices are circulant, we can represent them by their effect on an isolated
# pixel; this is called the *stencil* of the linear operator associated to the
# matrix (or the kernel of the corresponding convolution operator):

# $$
# \mathrm{stencil}(A)=
# \begin{array}{|c|c|c|}\hline0&1&0\\\hline1&0&1\\\hline0&1&0\\\hline\end{array}
# 	\qquad
# 	\qquad
# \mathrm{stencil}(L)=
# \begin{array}{|c|c|c|}\hline0&1&0\\\hline1&\!\!\!-4\!\!\!&1\\\hline0&1&0\\\hline\end{array}
# $$

# We also define a few administrative functions to load and display
# images:

def image_read(f):
	""" Read an image from filename "f" into a numpy array """
	import iio
	x = iio.read(f).squeeze()
	return x

def image_write(f, x):
	""" Write the numpy array "x" into an image file "f" """
	import iio
	iio.write(f, x)
	return

def image_display(f):
	""" Inline display the image from filename "f" into a numpy array """
	import IPython.display
	s = f"<div><p><img src=\"{f}\" /> {f}</p></div>"
	IPython.display.display(IPython.display.HTML(s))
	return

def image_render(f, x):
	""" Write the numpy array "x" into an image file "f" and display it """
	image_write(f, x)
	image_display(f)
	return

# Let's try these functions with a trivial example:

x = image_read("x.png")            # load an image from current directory
h, w = x.shape                      # extract height and width (note the order)
x[:,:w//2] = 0                      # paint the left side in black
x = image_write("x_cut.png", x)    # save the modified image
image_display("x.png")             # display original image
image_display("x_cut.png")         # display modified image


# ## Morphological operators

# Mathematical morphology is based on applying the adjacency matrix as an
# operator acting on binary images.
# The neighborhood of each pixel, as defined by the graph, plays the role of the
# *structuring element*.

# First, we read the image data $x$ to use through the rest of this
# section, and build its adjacency matrix $A$.

x = image_read("x.png")
h, w = x.shape
x = x.flatten()
A = grid_adjacency(h, w)

# Now, let's be silly: what happens when we apply $A$ to $x$ ?

y = A @ x
image_render("x_A.png", y.reshape(h, w))

# The result is a bit difficult to interpret... the image looks much brighter
# and maybe a bit blurry.

# Now let's do some morphology



m = 1.0 * (x > 66)          # binarized image
E = A.copy();E.setdiag(1)   # structuring element E = A + I
y = E**6 @ m                # apply it 6 times
y1 = y > 0                  # extract dilation
y2 = 1 - (y < y.max())      # extract erosion
y3 = y > y.max()/2          # extract median filter

# save the results

image_render("x_binarized.png",    255 * m.reshape(h, w))
image_render("x_6_morphogray.png", 255 * y.reshape(h, w) / y.max())
image_render("x_6_dilation.png",   255 * y1.reshape(h, w))
image_render("x_6_erosion.png",    255 * y2.reshape(h, w))
image_render("x_6_median.png",     255 * y3.reshape(h, w))




def grid_structuring_element(h, w):
	""" Build the adjacency matrix of a WxH grid graph """
	from scipy.sparse import eye
	A = grid_adjacency(h, w)
	E = A + eye(w*h)
	return E

def dilation(E, x):
	from scipy.sparse import diags
	y = (diags(x.squeeze()) @ E).max(axis=0).A.T.squeeze()
	return y

# y = dilation(E, x)
# image_render("x_dilation.png", y.reshape(h,w))

def erosion(E, x):
	m = 1 + x.max()
	t = m - x
	y = m - dilation(E, t)
	return y


def opening(E, x):     return dilation(E, erosion(E, x))
def closing(E, x):     return erosion(E, dilation(E, x))
def egradient(E, x):   return x - erosion(E, x)
def igradient(E, x):   return dilation(E, x) - x
def cgradient(E, x):   return (igradient(E,x) + egradient(E,x))/2
def mlaplacian(E, x):  return (igradient(E,x) - egradient(E,x))/2
def msharpen(E, x):    return x - mlaplacian(E, x)
def mblur(E, x):       return x + mlaplacian(E, x)
def tophat(E, x):      return x - opening(E, x)
def bothat(E, x):      return closing(E, x) - x

E = grid_structuring_element(h, w)
E = 1.0 * (E**3 > 0)
image_render("x_dilation.png",   dilation(E,x).reshape(h,w))
image_render("x_erosion.png",    erosion(E,x).reshape(h,w))
image_render("x_opening.png",    opening(E,x).reshape(h,w))
image_render("x_closing.png",    closing(E,x).reshape(h,w))
image_render("x_egradient.png",  2*egradient(E,x).reshape(h,w))
image_render("x_igradient.png",  2*igradient(E,x).reshape(h,w))
image_render("x_cgradient.png",  2*cgradient(E,x).reshape(h,w))
image_render("x_mlaplacian.png", 127-4*mlaplacian(E,x).reshape(h,w))
image_render("x_msharpen.png",   msharpen(E,x).reshape(h,w))
image_render("x_mblur.png",      mblur(E,x).reshape(h,w))
image_render("x_tophat.png",     6*tophat(E,x).reshape(h,w))
image_render("x_bothat.png",     255-6*bothat(E,x).reshape(h,w))

ex = erosion(E, x)


ex.shape





# ## Local linear operators

# ## Linear differential equations

# ---
# format:
#     html:
#         self-contained: true
#         preserve-tabs: true
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


