#!/usr/bin/env python3

""""
Script to generate a grayscale image of the combined gas saturation
and CO2 concentration values on an evenly spaced grid as required
by the benchmark description
"""

import os
import argparse
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable


def getFieldValues(fileName, nX, nY):
    saturation = np.zeros([nY, nX])
    concentration = np.zeros([nY, nX])

    if os.path.isfile(fileName):
        print(f'Processing {fileName}.')
    else:
        print(f'No file {fileName} found. Returning 0 values.')
        return saturation, concentration

    skip_header = 0
    with open(fileName, "r") as file:
        if not (file.readline()[0]).isnumeric():
            skip_header = 1

    csvData = np.genfromtxt(fileName, delimiter=',', skip_header=skip_header)
    # Treat results from Heriot-Watt in a special way, as they are
    # reported with respect to the laser grid already.
    if 'watt' in fileName:
        for i in np.arange(0, nY):
            saturation[i, :] = csvData[i*nX:(i+1)*nX, 2]
            concentration[i, :] = csvData[i*nX:(i+1)*nX, 3]
    else:
        for i in np.arange(0, nY):
            # Shift in x-direction as 6 more values have been reported,
            # 3 to the left and 3 to the right.
            # Analogously, shift in y-direction and
            # start with the fourth reported row of values due to the offset
            # between the lasergrid and the model coordinate system.
            saturation[i, :] = csvData[(i+3)*(nX+6)+3:(i+4)*(nX+6)-3, 2]
            concentration[i, :] = csvData[(i+3)*(nX+6)+3:(i+4)*(nX+6)-3, 3]

    return saturation, concentration

def plotColorMesh(fig, x, y, z, outFileName):
    ax = fig.gca()
    vmin = 0.0
    vmax = 1.8

    im = ax.pcolormesh(x, y, z, shading='flat', cmap='gist_gray', vmin=vmin, vmax=vmax)
    ax.axis([x.min(), x.max(), y.min(), y.max()])
    ax.axis('scaled')
    plt.axis('off')
    
    fig.savefig(outFileName, bbox_inches='tight', dpi=96, pad_inches=0)
    print(f'File {outFileName} has been generated.')


def generateGrayScale():
    """Generate a grayscale a spatial map for the FluidFlower benchmark"""

    parser = argparse.ArgumentParser(
        description="This script visualizes the gas saturation and CO2 concentration "
                    "on an evenly spaced grid as required by the benchmark description."
    )
    parser.add_argument("-in", "--infilename", default="spatial_map_24h.csv",
                        help="The csv file to visualize. Defaults to \"spatial_map_24h.csv\".")
    parser.add_argument("-out", "--outfilename", default="spatial_map_grayscale.png",
                        help="The output image file name. Defaults to \"spatial_map_grayscale.png\".")

    cmdArgs = vars(parser.parse_args())

    xSpace = np.arange(0.03, 2.83 + 5.0e-3, 1.0e-2)
    ySpace = np.arange(0.03, 1.23 + 5.0e-3, 1.0e-2)
    x, y = np.meshgrid(xSpace, ySpace)
    nX = xSpace.size - 1
    nY = ySpace.size - 1

    # The target size of the resulting image is 280x120 pixels, one pixel per reporting cell.
    # The added pixels correspond to the automatically added whitespace which can be removed
    # only when saving the figure to disk.
    my_dpi = 96
    fig = plt.figure(figsize=((280+82)/my_dpi, (120+37)/my_dpi), dpi=my_dpi)

    inFileName = cmdArgs["infilename"]

    saturation, concentration = getFieldValues(inFileName, nX, nY)

    outFileName = cmdArgs["outfilename"]
    # The formula approximates the mass of CO2 in a cell by adding
    # the contributions from the gaseous and the liquid phase.
    # The factor '2.0' is the approximate density of CO2.
    plotColorMesh(fig, x, y, 2.0*saturation + concentration*(1.0 - saturation), outFileName)

if __name__ == "__main__":
    generateGrayScale()
