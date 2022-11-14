# Test script for the Earth movers distance to measure differences in distributions in 2d.

import ot
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

# Define problem size
# NOTE: ot has severe memory restrictions - cv2 has much more mild restrictions
# Furthermore, computing the exact EMD has O(n**3) complexity and can therefore be
# quite slow.

# Define distributions
im = Image.open('../visualization/test.png').convert('L')
Nx, Ny = im.size
print(Nx, Ny)
a = np.array(im.getdata()).reshape(Nx, Ny)

#a = np.zeros((Nx,Ny), dtype=float)
b = np.zeros((Nx,Ny), dtype=float)

#a[1,1] = 0.25
#a[1,2] = 0.25
b[1,1] = 0.5

# Make a and b 'true' distributions
# NOTE: cv2 will internally convert a and b to distributions (summing
# up to 1), while ot is not.
# Furthermore, it requires a and b to be compatible, i.e., that their
# sums are equal. While cv2 does not, it is however also not clear
# how to interpret the result for non-compatible signals.
if True:
    a = a/np.sum(a)
    b = b/np.sum(b)
    print(np.unique(a))

# Determine EMD using ot
if False:
    # OT takes 1d arrays as inputs
    a_flat = a.flatten(order = "F")
    b_flat = b.flatten(order = "F")
    
    # Cell centers of all cells - x and y coordinates.
    cc_x = np.zeros((Nx,Ny), dtype=float).flatten("F")
    cc_y = np.zeros((Nx,Ny), dtype=float).flatten("F")
    
    cc_x, cc_y = np.meshgrid(np.arange(Nx), np.arange(Ny), indexing="ij")
    
    cc_x_flat = cc_x.flatten("F")
    cc_y_flat = cc_y.flatten("F")
    
    cc = np.vstack((cc_x_flat, cc_y_flat)).T
    
    # Distance matrix
    # NOTE the definition of this distance matrix is memory consuming and
    # does not allow for too large distributions.
    M = ot.dist(cc, cc, metric="euclidean")
    
    dist_ot = ot.emd2(a_flat,b_flat,M)
    print(dist_ot)

# Determine EMD using cv2
if True:
    # CV2 requires a transformation.
    def img_to_sig(arr, dx=1):
        """Convert a 2D array to a signature for cv2.EMD"""
    
        # cv2.EMD requires single-precision, floating-point input
        sig = np.empty((arr.size, 3), dtype=np.float32)
        count = 0
        for i in range(arr.shape[0]):
            for j in range(arr.shape[1]):
                sig[count] = np.array([arr[i,j], i * dx, j * dx])
                count += 1
        return sig
    
    # CV2 takes signals that contain both data and coordinates
    a_sig = img_to_sig(a, dx=1)
    b_sig = img_to_sig(b, dx=1)
    
    dist_cv2, _, _ = cv2.EMD(a_sig, b_sig, cv2.DIST_L2)
    print(dist_cv2)
