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


def getFieldValues(fileName, nX, nY, xSpace, ySpace):
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
    for i in np.arange(0, nY):
        saturation[i, :] = csvData[i*nX:(i+1)*nX, 2]
        concentration[i, :] = csvData[i*nX:(i+1)*nX, 3]

    xCont = []
    yCont = []
    threshold = 1e-1

    # bottom row:
    for j in np.arange(0, nX):
        if concentration[0, j] > threshold:
            xCont.append(0.5*(xSpace[j] + xSpace[j+1]))
            yCont.append(0.5*(ySpace[0] + ySpace[1]))

    # top row:
    for j in np.arange(0, nX):
        if concentration[nY-1, j] > threshold:
            xCont.append(0.5*(xSpace[j] + xSpace[j+1]))
            yCont.append(0.5*(ySpace[nY-1] + ySpace[nY]))

    # left column:
    for i in np.arange(0, nY):
        if concentration[i, 0] > threshold:
            xCont.append(0.5*(xSpace[0] + xSpace[1]))
            yCont.append(0.5*(ySpace[i] + ySpace[i+1]))

    # right column:
    for i in np.arange(0, nY):
        if concentration[i, nX-1] > threshold:
            xCont.append(0.5*(xSpace[nX-1] + xSpace[nX]))
            yCont.append(0.5*(ySpace[i] + ySpace[i+1]))

    # inner cells:
    for i in np.arange(1, nY-1):
        for j in np.arange(1, nX-1):
            if concentration[i, j] > threshold:
                if any(val < threshold for val in [concentration[i-1, j], concentration[i+1, j], concentration[i, j-1], concentration[i, j+1]]):
                    xCont.append(0.5*(xSpace[j] + xSpace[j+1]))
                    yCont.append(0.5*(ySpace[i] + ySpace[i+1]))

    return saturation, concentration, xCont, yCont

def plotContours(fig, x, y, z, xCont, yCont, outFileName):
    ax = fig.gca()
    vmin = 0.0
    vmax = 1.8

    ax.pcolormesh(x, y, z, shading='flat', cmap='gist_gray', vmin=vmin, vmax=vmax)
    ax.plot(xCont, yCont, color='r', linestyle='None', marker='o', markersize = 1.0)
    ax.axis([x.min(), x.max(), y.min(), y.max()])
    ax.axis('scaled')
    plt.axis('off')
    
    fig.savefig(outFileName, bbox_inches='tight', dpi=96, pad_inches=0)
    print(f'File {outFileName} has been generated.')

def generateContourLine(xMin, xMax, yMin, yMax, inFileName, outFileName):
    xSpace = np.arange(xMin, xMax + 5.0e-3, 1.0e-2)
    ySpace = np.arange(yMin, yMax + 5.0e-3, 1.0e-2)
    x, y = np.meshgrid(xSpace, ySpace)
    nX = xSpace.size - 1
    nY = ySpace.size - 1

    # The target size of the resulting image is 572x246 pixels, 2x2 pixels per reporting cell.
    # The added pixels correspond to the automatically added whitespace which can be removed
    # only when saving the figure to disk.
    my_dpi = 96
    fig = plt.figure(figsize=((286*2+170)/my_dpi, (123*2+74)/my_dpi), dpi=my_dpi)

    saturation, concentration, xCont, yCont = getFieldValues(inFileName, nX, nY, xSpace, ySpace)

    # The formula approximates the mass of CO2 in a cell by adding
    # the contributions from the gaseous and the liquid phase.
    # The factor '2.0' is the approximate density of CO2.
    plotContours(fig, x, y, 2.0*saturation + concentration*(1.0 - saturation), xCont, yCont, outFileName)

    return xCont, yCont

def generateContours():
    """Generate a grayscale spatial map with contours for the FluidFlower benchmark"""

    parser = argparse.ArgumentParser(
        description="This script visualizes the gas saturation and CO2 concentration "
                    "including contours on an evenly spaced grid."
    )
    parser.add_argument("-in", "--infilename", default="spatial_map_24h.csv",
                        help="The csv file to visualize. Defaults to \"spatial_map_24h.csv\".")
    parser.add_argument("-out", "--outfilename", default="spatial_map_grayscale.png",
                        help="The output image file name. Defaults to \"spatial_map_grayscale.png\".")
    parser.add_argument("-xmin", "--xmin", type=float, default=0.0,
                        help="The minimum x value of the domain. Defaults to 0.0.")
    parser.add_argument("-xmax", "--xmax", type=float, default=2.86,
                        help="The maximum x value of the domain. Defaults to 2.86.")
    parser.add_argument("-ymin", "--ymin", type=float, default=0.0,
                        help="The minimum y value of the domain. Defaults to 0.0.")
    parser.add_argument("-ymax", "--ymax", type=float, default=1.23,
                        help="The maximum y value of the domain. Defaults to 1.23.")

    cmdArgs = vars(parser.parse_args())

    generateContourLine(cmdArgs["xmin"], cmdArgs["xmax"], cmdArgs["ymin"], cmdArgs["ymax"], cmdArgs["infilename"], cmdArgs["outfilename"])

if __name__ == "__main__":
    generateContours()
