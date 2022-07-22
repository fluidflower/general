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
    for i in np.arange(0, nY):
        saturation[i, :] = csvData[i*nX:(i+1)*nX, 2]
        concentration[i, :] = csvData[i*nX:(i+1)*nX, 3]

    return saturation, concentration

def plotColorMesh(fig, x, y, z, fieldName, outFileName):
    ax = fig.gca()
    vmin = 0.0
    if fieldName == 'sat':
        vmax = 1.0
    else:
        vmax = 1.8

    if fieldName == 'sat' or fieldName == 'con':
        im = ax.pcolormesh(x, y, z, shading='flat', cmap='coolwarm', vmin=vmin, vmax=vmax)
    else:
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
    parser.add_argument("-field", "--field", default="both",
                        help="The field to be plotted, \"sat\" or \"con\" or \"both\". Defaults to \"both\".")
    parser.add_argument("-xmin", "--xmin", type=float, default=0.0,
                        help="The minimum x value of the domain. Defaults to 0.0.")
    parser.add_argument("-xmax", "--xmax", type=float, default=2.86,
                        help="The maximum x value of the domain. Defaults to 2.86.")
    parser.add_argument("-ymin", "--ymin", type=float, default=0.0,
                        help="The minimum y value of the domain. Defaults to 0.0.")
    parser.add_argument("-ymax", "--ymax", type=float, default=1.23,
                        help="The maximum y value of the domain. Defaults to 1.23.")

    cmdArgs = vars(parser.parse_args())

    xSpace = np.arange(cmdArgs["xmin"], cmdArgs["xmax"] + 5.0e-3, 1.0e-2)
    ySpace = np.arange(cmdArgs["ymin"], cmdArgs["ymax"] + 5.0e-3, 1.0e-2)
    x, y = np.meshgrid(xSpace, ySpace)
    nX = xSpace.size - 1
    nY = ySpace.size - 1

    # The target size of the resulting image is 572x246 pixels, 2x2 pixels per reporting cell.
    # The added pixels correspond to the automatically added whitespace which can be removed
    # only when saving the figure to disk.
    my_dpi = 96
    fig = plt.figure(figsize=((286*2+170)/my_dpi, (123*2+74)/my_dpi), dpi=my_dpi)

    inFileName = cmdArgs["infilename"]

    saturation, concentration = getFieldValues(inFileName, nX, nY)

    fieldName = cmdArgs["field"]
    outFileName = cmdArgs["outfilename"]
    if fieldName == "sat":
        plotColorMesh(fig, x, y, saturation, fieldName, outFileName)
    elif fieldName == "con":
        plotColorMesh(fig, x, y, concentration, fieldName, outFileName)
    else:
        plotColorMesh(fig, x, y, saturation + concentration, fieldName, outFileName)

if __name__ == "__main__":
    generateGrayScale()
