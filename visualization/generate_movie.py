#!/usr/bin/env python3

""""
Script to generate movies for the gas saturation and CO2 concentration
on an evenly spaced grid as required by the benchmark description
"""

import os
import re
import argparse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
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

def plotColorMesh(fig, x, y, z, timestep, name):
    ax = fig.add_subplot(230+timestep)
    im = ax.pcolormesh(x, y, z, shading='flat', cmap='coolwarm')
    ax.axis([x.min(), x.max(), y.min(), y.max()])
    ax.axis('scaled')
    ax.set_title(f'{name} at t = {timestep*24} h')
    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size='5%', pad=0.05)
    fig.colorbar(im, cax=cax, orientation='vertical')


def generateMovie():
    """Generate movies for the FluidFlower benchmark"""

    parser = argparse.ArgumentParser(
        description="This script generates movies for the gas saturation and CO2 concentration "
                    "on an evenly spaced grid as required by the benchmark description."
    )
    parser.add_argument("-f", "--basefilename", default="spatial_map",
                        help="The base name of the csv files to visualize. "
                             "Assumes that the files are named 'basefilename_<X>s.csv' "
                             "with X = 600, 1200, .... Defaults to 'spatial_map'.")
    parser.add_argument("-xmin", "--xmin", type=float, default=0.0,
                        help="The minimum x value of the domain. Defaults to 0.0.")
    parser.add_argument("-xmax", "--xmax", type=float, default=2.86,
                        help="The maximum x value of the domain. Defaults to 2.86.")
    parser.add_argument("-ymin", "--ymin", type=float, default=0.0,
                        help="The minimum y value of the domain. Defaults to 0.0.")
    parser.add_argument("-ymax", "--ymax", type=float, default=1.23,
                        help="The maximum y value of the domain. Defaults to 1.23.")
    parser.add_argument("-g", "--group", default="",
                        help="The name of the participating group.")

    cmdArgs = vars(parser.parse_args())
    baseFileName = cmdArgs["basefilename"]
    groupName = cmdArgs["group"]

    xSpace = np.arange(cmdArgs["xmin"], cmdArgs["xmax"] + 5.0e-3, 1.0e-2)
    ySpace = np.arange(cmdArgs["ymin"], cmdArgs["ymax"] + 5.0e-3, 1.0e-2)
    x, y = np.meshgrid(xSpace, ySpace)
    nX = xSpace.size - 1
    nY = ySpace.size - 1

    figS = plt.figure(figsize=(10, 4))
    axS = plt.axes(xlim=(0, 2.86), ylim=(0, 1.23))
    imS = axS.pcolormesh(x, y, 0*x, vmin=0, vmax=1, shading='flat', cmap='coolwarm')
    dividerS = make_axes_locatable(axS)
    caxS = dividerS.append_axes('right', size='5%', pad=0.05)
    figS.colorbar(imS, cax=caxS, orientation='vertical')

    figC = plt.figure(figsize=(10, 4))
    axC = plt.axes(xlim=(0, 2.86), ylim=(0, 1.23))
    imC = axC.pcolormesh(x, y, 0*x, vmin=0, vmax=2, shading='flat', cmap='coolwarm')
    dividerC = make_axes_locatable(axC)
    caxC = dividerC.append_axes('right', size='5%', pad=0.05)
    figC.colorbar(imC, cax=caxC, orientation='vertical')

    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

    csvFiles = [f for f in os.listdir('.') if re.match(f'{baseFileName}_[0-9]+s\.csv', f)]
    if not csvFiles:
        csvFiles = [f for f in os.listdir('.') if re.match(f'{baseFileName}_[0-9]+\.csv', f)]
    natsort = lambda s: [int(t) if t.isdigit() else t.lower() for t in re.split('(\d+)', s)]
    csvFiles = sorted(csvFiles, key=natsort)

    def initS():
        return imS

    def animateS(i):
        saturation, concentration = getFieldValues(csvFiles[i], nX, nY)
        imS.set_array(saturation)
        axS.set_title(f'saturation [-] at t = {(i+1)/6:2.2f} h')
        axS.text(0.02, 0.05, groupName, transform=axS.transAxes, fontsize=18,
                 horizontalalignment='left', verticalalignment='bottom', bbox=props)
        return imS

    animS = animation.FuncAnimation(figS, animateS, init_func=initS,
                                   frames=np.arange(len(csvFiles)), interval=10, repeat=False)
    animS.save(f'{groupName.lower()}_saturation.mp4', fps=15, extra_args=['-vcodec', 'libx264'])

    def initC():
        return imC

    def animateC(i):
        saturation, concentration = getFieldValues(csvFiles[i], nX, nY)
        imC.set_array(concentration)
        axC.set_title(f'concentration [kg/m3] at t = {(i+1)/6:2.2f} h')
        axC.text(0.02, 0.05, groupName, transform=axC.transAxes, fontsize=18,
                 horizontalalignment='left', verticalalignment='bottom', bbox=props)
        return imC

    animC = animation.FuncAnimation(figC, animateC, init_func=initC,
                                   frames=np.arange(len(csvFiles)), interval=10, repeat=False)
    animC.save(f'{groupName.lower()}_concentration.mp4', fps=15, extra_args=['-vcodec', 'libx264'])

if __name__ == "__main__":
    generateMovie()
