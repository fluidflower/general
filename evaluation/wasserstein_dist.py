import cv2
import numpy as np
from matplotlib import pyplot as plt
  
path = r'../../stuttgart/figures/stuttgart_gray_24h.png'

img = cv2.imread(path)
hst = cv2.calcHist(img, [0], None, [256], [0,256])
print(hst)
cv2.imshow('image', img)

#plt.plot(hst)
#plt.title('Histogram for gray scale image')
#plt.show()

# import numpy as np
# import skimage.color
# import skimage.io
# import matplotlib.pyplot as plt

# # read the image of a plant seedling as grayscale from the outset
# image = skimage.io.imread(fname="../../experiment/snapshots/box_A_c3_1_24h_211215_time110714_DSC04550_con_gray.jpg",
#                           as_gray=True)
# #image = skimage.io.imread(fname="plant-seedling.jpg", as_gray=True)

# # display the image
# #fig, ax = plt.subplots()
# #plt.imshow(image, cmap="gray")
# #plt.show()

# # create the histogram
# histogram, bin_edges = np.histogram(image, bins=256, range=(0, 1))
# print(histogram)

# # configure and draw the histogram figure
# plt.figure()
# plt.title("Grayscale Histogram")
# plt.xlabel("grayscale value")
# plt.ylabel("pixel count")
# #plt.yscale("log")
# plt.xlim([0.0, 1.0])  # <- named arguments do not work here

# plt.plot(bin_edges[0:-1], histogram)  # <- or here
# plt.show()
