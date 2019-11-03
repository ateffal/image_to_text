from skimage import data, io, filters
from skimage.color import rgb2gray
from skimage import exposure
from skimage.feature import match_template
from skimage.measure import find_contours
from skimage.draw import line

from helper_functions import detect_lines
from helper_functions import detect_characters


import numpy as np


image_par_3 = io.imread("./image_samples/paragraphe_3.jpg")
io.imshow(image_par_3)
io.show()

image = image_par_3[:, :, 0]
io.imshow(image)
io.show()

h = image.shape[0]
w = image.shape[1]

treshold = 100

for i in range(h):
    for j in range(w):
        if image[i, j] < treshold:
            image[i, j] = 0
        else:
            image[i, j] = 255

io.imshow(image)
io.show()


x, li = detect_lines(image, 3)
io.imsave("./results/res3.jpg", x)

io.imshow(x)
io.show()


y = detect_characters(image, li, 30)
io.imsave("./results/res3.1.jpg", y)
io.imshow(y)
io.show()
