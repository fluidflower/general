#!/usr/bin/env python3

""""
Script to visualize the gas saturation and CO2 concentration
on an evenly spaced grid as required by the benchmark description
"""

import argparse
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable


def getFieldValues(fileName, nX, nY):
    print(f'Processing {fileName}.') 

    csvData = np.genfromtxt(fileName, delimiter=',', skip_header=1)
    saturation = np.empty([nY, nX])
    concentration = np.empty([nY, nX])
    for i in np.arange(0, nY):
        saturation[i, :] = csvData[i*nX:(i+1)*nX, 2]
        concentration[i, :] = csvData[i*nX:(i+1)*nX, 3]

    return saturation, concentration

def plotColorMesh(fig, x, y, z, timestep, name):
    ax = fig.add_subplot(230+timestep)
    im = ax.pcolormesh(x, y, z, shading='flat', cmap='coolwarm')
    ax.axis([x.min(), x.max(), y.min(), y.max()])
    ax.axis('scaled')
    ax.set_title(f'{name} at t = {timestep*24} h')
    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size='5%', pad=0.05)
    fig.colorbar(im, cax=cax, orientation='vertical')


def visualizeSpatialMaps():
    """Visualize a spatial map for the FluidFlower benchmark"""

    parser = argparse.ArgumentParser(
        description="This script visualizes the gas saturation and CO2 concentration "
                    "on an evenly spaced grid as required by the benchmark description."
    )
    parser.add_argument("-f", "--basefilename", default="spatial_map",
                        help="The base name of the csv files to visualize. "
                             "Assumes that the files are named 'basefilename_<X>h.csv' "
                             "with X = 24, 48, ..., 120. Defaults to 'spatial_map'.")

    cmdArgs = vars(parser.parse_args())
    baseFileName = cmdArgs["basefilename"]

    xSpace = np.arange(0.0, 2.87, 1.0e-2)
    ySpace = np.arange(0.0, 1.31, 1.0e-2)
    x, y = np.meshgrid(xSpace, ySpace)
    nX = xSpace.size - 1
    nY = ySpace.size - 1

    figS = plt.figure(figsize=(18, 6))
    figC = plt.figure(figsize=(18, 6))

    for timestep in np.arange(1, 6):
        fileName = f'{baseFileName}_{timestep*24}h.csv'

        saturation, concentration = getFieldValues(fileName, nX, nY)

        plotColorMesh(figS, x, y, saturation, timestep, 'saturation')
        plotColorMesh(figC, x, y, concentration, timestep, 'concentration')
    
    figS.savefig(f'{baseFileName}_saturation.png', bbox_inches='tight')
    figC.savefig(f'{baseFileName}_concentration.png', bbox_inches='tight')
    print(f'Files {baseFileName}_saturation.png and {baseFileName}_concentration.png have been generated.')

if __name__ == "__main__":
    visualizeSpatialMaps()
