# Test script for the Earth movers distance to measure differences in distributions in 2d.
import ot
import argparse
import numpy as np
import cv2
from PIL import Image


def calculateEMD(inFileName1, inFileName2):
    # Define problem size
    # NOTE: ot has severe memory restrictions - cv2 has much more mild restrictions
    # Furthermore, computing the exact EMD has O(n**3) complexity and can therefore be
    # quite slow.

    # Define distributions
    im1 = Image.open(inFileName1).convert('L')
    im1 = im1.resize((140,60), Image.ANTIALIAS)
    Nx, Ny = im1.size
    #print(Nx, Ny)
    a = np.array(im1.getdata()).reshape(Nx, Ny)
    #print(np.sum(a))

    im2 = Image.open(inFileName2).convert('L')
    im2 = im2.resize(im1.size, Image.ANTIALIAS)
    b = np.array(im2.getdata()).reshape(Nx, Ny)
    #b = np.ones((140, 60))

    # Make a and b 'true' distributions
    # NOTE: cv2 will internally convert a and b to distributions (summing
    # up to 1), while ot is not.
    # Furthermore, it requires a and b to be compatible, i.e., that their
    # sums are equal. While cv2 does not, it is however also not clear
    # how to interpret the result for non-compatible signals.
    if True:
        a = a/np.sum(a)
        b = b/np.sum(b)

    # Determine EMD using ot
    if True:
        # OT takes 1d arrays as inputs
        a_flat = a.flatten(order = "F")
        b_flat = b.flatten(order = "F")
        
        # Cell centers of all cells - x and y coordinates.
        cc_x = np.zeros((Nx,Ny), dtype=float).flatten("F")
        cc_y = np.zeros((Nx,Ny), dtype=float).flatten("F")
        
        cc_x, cc_y = np.meshgrid(np.arange(Nx), np.arange(Ny), indexing="ij")
        
        cc_x_flat = cc_x.flatten("F")/Nx*2.8 + 5e-3*280/Nx
        cc_y_flat = cc_y.flatten("F")/Ny*1.2 + 5e-3*120/Ny
        #print(cc_x_flat, cc_y_flat)
        
        cc = np.vstack((cc_x_flat, cc_y_flat)).T
        
        # Distance matrix
        # NOTE the definition of this distance matrix is memory consuming and
        # does not allow for too large distributions.
        M = ot.dist(cc, cc, metric="euclidean")
        
        dist_ot = ot.emd2(a_flat, b_flat, M, numItermax=500000)
        print(f'{inFileName1}, {inFileName2}: {dist_ot}')

        return dist_ot

    # Determine EMD using cv2
    if False:
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

def emd():
    """Calculate the Wasserstein distance between two grayscale images"""

    parser = argparse.ArgumentParser(
        description="This script calculates the Wasserstein distance between two grayscale images."
    )
    parser.add_argument("-in1", "--infilename1",
                        help="The file name of the first image.")
    parser.add_argument("-in2", "--infilename2",
                        help="The file name of the second image.")

    cmdArgs = vars(parser.parse_args())

    calculateEMD(cmdArgs["infilename1"], cmdArgs["infilename2"])

if __name__ == "__main__":
    emd()
