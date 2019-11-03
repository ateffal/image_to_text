from skimage import data, io, filters
from skimage.color import rgb2gray
from skimage import exposure
from skimage.feature import match_template

# from skimage.exposure import match_histograms


image = data.coffee()
io.imshow(image)
io.show()




# rgb to grayscale
image_gs = rgb2gray(image)
io.imshow(image_gs)
io.show()

# edges
edges = filters.sobel(image[:,:,2])
io.imshow(edges)
io.show()

# histogramme matching
image2 = data.astronaut()
io.imshow(image2)

# matched = match_histograms(image, image2, multichannel=True)
# io.imshow(matched)

# Equalization
img_eq = exposure.equalize_hist(image)
io.imshow(img_eq)


image3 = io.imread("D:/Shared/a.teffal/Mes documents/TEFFAL/Formation Python/foot-images/image1.jpg")
io.imshow(image3)



ball = io.imread("D:/Shared/a.teffal/Mes documents/TEFFAL/Formation Python/foot-images/football2.jpg")
result = match_template(image3, ball)
