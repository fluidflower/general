#!/usr/bin/env python3

""""
Script to visualize the time series quantities
as required by the benchmark description
"""

import os
import argparse
import numpy as np
import matplotlib.pyplot as plt


def visualizeTimeSeries():
    """Visualize time series for the FluidFlower benchmark"""

    parser = argparse.ArgumentParser(
        description="This script visualizes the time series quantities "
                    "as required by the benchmark description."
    )
    parser.add_argument("-f", "--filename", default="time_series.csv",
                        help="The name of the csv file to visualize. "
                             "Defaults to 'time_series.csv'.")

    cmdArgs = vars(parser.parse_args())
    fileName = cmdArgs["filename"]
    baseFileName = os.path.splitext(fileName)[0]

    skip_header = 0
    with open(fileName, "r") as file:
        if not (file.readline()[0]).isnumeric():
            skip_header = 1

    csvData = np.genfromtxt(fileName, delimiter=',', skip_header=skip_header)
    t = csvData[:, 0]/3600

    fig, ax = plt.subplots()
    ax.plot(t, csvData[:, 1], label='sensor 1')
    ax.plot(t, csvData[:, 2], label='sensor 2')
    ax.set_title('pressure')
    ax.set_xlabel('time [h]')
    ax.set_ylabel('pressure [N/m2]')
    ax.legend()
    fig.savefig(f'{baseFileName}_pressure.png', bbox_inches='tight')

    fig, ax = plt.subplots()
    ax.plot(t, csvData[:, 3], label='mobile')
    ax.plot(t, csvData[:, 4], label='immobile')
    ax.plot(t, csvData[:, 5], label='dissolved')
    ax.plot(t, csvData[:, 6], label='seal')
    ax.set_title('phase distribution in Box A')
    ax.set_xlabel('time [h]')
    ax.set_ylabel('CO2 [kg]')
    ax.legend()
    fig.savefig(f'{baseFileName}_boxA.png', bbox_inches='tight')

    fig, ax = plt.subplots()
    ax.plot(t, csvData[:, 7], label='mobile')
    ax.plot(t, csvData[:, 8], label='immobile')
    ax.plot(t, csvData[:, 9], label='dissolved')
    ax.plot(t, csvData[:, 10], label='seal')
    ax.set_title('phase distribution in Box B')
    ax.set_xlabel('time [h]')
    ax.set_ylabel('CO2 [kg]')
    ax.legend()
    fig.savefig(f'{baseFileName}_boxB.png', bbox_inches='tight')

    fig, ax = plt.subplots()
    ax.plot(t, csvData[:, 11], label='M')
    ax.set_title('convection in Box C')
    ax.set_xlabel('time [h]')
    ax.set_ylabel('M [m]')
    ax.legend()
    fig.savefig(f'{baseFileName}_boxC.png', bbox_inches='tight')

    print(f'Files {baseFileName}_pressure.png and {baseFileName}_box{{A, B, C}}.png have been generated.')

if __name__ == "__main__":
    visualizeTimeSeries()
