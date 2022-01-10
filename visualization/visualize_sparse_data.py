#!/usr/bin/env python3

""""
Script to visualize the sparse data
as required by the benchmark description
"""

import os
import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import math

def visualizeRow(row, ax, title, ylabel):
    p10_mean = row[1]
    p50_mean = row[2]
    p90_mean = row[3]
    p10_dev = row[4]
    p50_dev = row[5]
    p90_dev = row[6]

    rect = mpatches.Rectangle((1, p10_mean), 1, p90_mean - p10_mean, color = "purple")
    ax.add_patch(rect)

    ax.arrow(2.1, p50_mean, 0, p10_dev, length_includes_head=True,
             head_width=0.05, head_length=1e-5, linewidth=2, fc='b', ec='b',
             label='p50_mean +/- p10_dev')
    ax.arrow(2.1, p50_mean, 0, -p10_dev, length_includes_head=True,
             head_width=0.05, head_length=1e-5, linewidth=2, fc='b', ec='b')
    ax.arrow(2.2, p50_mean, 0, p50_dev, length_includes_head=True,
             head_width=0.05, head_length=1e-5, linewidth=2, fc='k', ec='k',
             label='p50_mean +/- p50_dev')
    ax.arrow(2.2, p50_mean, 0, -p50_dev, length_includes_head=True,
             head_width=0.05, head_length=1e-5, linewidth=2, fc='k', ec='k')
    ax.arrow(2.3, p50_mean, 0, p90_dev, length_includes_head=True,
             head_width=0.05, head_length=1e-5, linewidth=2, fc='r', ec='r',
             label='p50_mean +/- p90_dev')
    ax.arrow(2.3, p50_mean, 0, -p90_dev, length_includes_head=True,
             head_width=0.05, head_length=1e-5, linewidth=2, fc='r', ec='r')

    ax.set_xlim([1.5, 2.5])
    ax.set_ylim([0.95*min(p10_mean, p50_mean-p90_dev), 1.15*max(p90_mean, p50_mean+p90_dev)])
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xticks([])
    ax.set_yticks([p10_mean, p50_mean, p90_mean])
    ax.set_yticklabels([f'p10_mean\n={p10_mean:.3e}', f'p50_mean\n={p50_mean:.3e}', f'p90_mean\n={p90_mean:.3e}'])
    ax.legend()

def visualizeSparseData():
    """Visualize sparse data for the FluidFlower benchmark"""

    parser = argparse.ArgumentParser(
        description="This script visualizes the sparse data "
                    "as required by the benchmark description."
    )
    parser.add_argument("-f", "--filename", default="sparse_data.csv",
                        help="The name of the csv file to visualize. "
                             "Defaults to 'sparse_data.csv'.")

    cmdArgs = vars(parser.parse_args())
    fileName = cmdArgs["filename"]
    baseFileName = os.path.splitext(fileName)[0]

    skip_header = 0
    with open(fileName, "r") as file:
        if not (file.readline()[0]).isnumeric():
            skip_header = 1

    csvData = np.genfromtxt(fileName, delimiter=',', skip_header=skip_header)

    fig = plt.figure(figsize=(8, 4))
    ax = plt.subplot(121)
    visualizeRow(csvData[0], ax, '1a: sensor 1', 'pressure [N/m2]')
    ax = plt.subplot(122)
    visualizeRow(csvData[1], ax, '1b: sensor 2', '')
    fig.tight_layout()
    fig.savefig(f'{baseFileName}_pressure.png', bbox_inches='tight')

    fig = plt.figure(figsize=(8, 4))
    ax = plt.subplot(121)
    visualizeRow(csvData[2], ax, '2: max mobile free phase in Box A', 'time [s]')
    ax = plt.subplot(122)
    visualizeRow(csvData[11], ax, '5: M exceeds 110% of Box C’s width', '')
    fig.tight_layout()
    fig.savefig(f'{baseFileName}_time.png', bbox_inches='tight')

    fig = plt.figure(figsize=(16, 4))
    fig.suptitle('CO2 in Box A at 72h')
    ax = plt.subplot(141)
    visualizeRow(csvData[3], ax, '3a: mobile free phase', 'mass [kg]')
    ax = plt.subplot(142)
    visualizeRow(csvData[4], ax, '3b: immobile free phase', '')
    ax = plt.subplot(143)
    visualizeRow(csvData[5], ax, '3c: dissolved in water', '')
    ax = plt.subplot(144)
    visualizeRow(csvData[6], ax, '3d: seal', '')
    fig.tight_layout()
    fig.savefig(f'{baseFileName}_boxA.png', bbox_inches='tight')

    fig = plt.figure(figsize=(16, 4))
    fig.suptitle('CO2 in Box B at 72h')
    ax = plt.subplot(141)
    visualizeRow(csvData[7], ax, '4a: mobile free phase', 'mass [kg]')
    ax = plt.subplot(142)
    visualizeRow(csvData[8], ax, '4b: immobile free phase', '')
    ax = plt.subplot(143)
    visualizeRow(csvData[9], ax, '4c: dissolved in water', '')
    ax = plt.subplot(144)
    visualizeRow(csvData[10], ax, '4d: seal', '')
    fig.tight_layout()
    fig.savefig(f'{baseFileName}_boxB.png', bbox_inches='tight')

    fig, ax = plt.subplots(figsize=(4, 4))
    visualizeRow(csvData[12], ax, '6: total mass of CO2 in the top seal facies', 'mass [kg]')
    fig.tight_layout()
    fig.savefig(f'{baseFileName}_mass.png', bbox_inches='tight')

    print(f'Files {baseFileName}_{{pressure, time, box{{A, B}}, mass}}.png have been generated.')

if __name__ == "__main__":
    visualizeSparseData()
