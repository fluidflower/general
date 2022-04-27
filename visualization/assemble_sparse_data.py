#!/usr/bin/env python3
import os
import argparse
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import math

def visualizeRow(row, ax, title, ylabel, group, color, offset):
    if np.isfinite(row[1]):
        p10_mean = row[1]
    else:
        p10_mean = row[2]
    p50_mean = row[2]
    if np.isfinite(row[3]):
        p90_mean = row[3]
    else:
        p90_mean = row[2]


    if np.isfinite(row[4]):
        p10_dev = row[4]
    else:
        p10_dev = row[5]
    p50_dev = row[5]
    if np.isfinite(row[6]):
        p90_dev = row[6]
    else:
        p90_dev = row[5]

    # rect = mpatches.Rectangle((1+offset, p10_mean), 1, p90_mean - p10_mean, color=color, label=group)
    rect = mpatches.Polygon([[1+offset, p10_mean], [2+offset, p50_mean], [1+offset, p90_mean]], fill=True, linewidth=3, color=color, label=group)
    ax.add_patch(rect)

    ax.arrow(2.1+offset, p50_mean, 0, p10_dev, length_includes_head=True,
             head_width=0.05, head_length=1e-5, linewidth=2, fc='b', ec='b')
    ax.arrow(2.1+offset, p50_mean, 0, -p10_dev, length_includes_head=True,
             head_width=0.05, head_length=1e-5, linewidth=2, fc='b', ec='b')
    ax.arrow(2.2+offset, p50_mean, 0, p50_dev, length_includes_head=True,
             head_width=0.05, head_length=1e-5, linewidth=2, fc='k', ec='k')
    ax.arrow(2.2+offset, p50_mean, 0, -p50_dev, length_includes_head=True,
             head_width=0.05, head_length=1e-5, linewidth=2, fc='k', ec='k')
    ax.arrow(2.3+offset, p50_mean, 0, p90_dev, length_includes_head=True,
             head_width=0.05, head_length=1e-5, linewidth=2, fc='r', ec='r')
    ax.arrow(2.3+offset, p50_mean, 0, -p90_dev, length_includes_head=True,
             head_width=0.05, head_length=1e-5, linewidth=2, fc='r', ec='r')

    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xticks([])
    ax.set_xlim(1, 21)

def assembleSparseData():
    """Visualize sparse data for the FluidFlower benchmark"""

    parser = argparse.ArgumentParser(
        description="This script visualizes the sparse data "
                    "as required by the benchmark description."
    )

    fileNames = ["../../austin/sparse_data.csv",
                 "../../csiro/sparse_data.csv",
                 "../../delft/delft-DARSim/sparse_data.csv",
                 "../../delft/delft-DARTS/sparse_data.csv",
                 "../../herriot-watt/HWU-sparsedata-final.csv",
                 "../../imperial/sparse_data.csv",
                 "../../lanl/sparse_data.csv",
                 "../../melbourne/sparse_data.csv",
                 "../../stanford/sparse_data.csv",
                 "../../stuttgart/sparse_data.csv"]
    groups = ["Austin", "CSIRO", "Delft-DARSim", "Delft-DARTS", "Heriot-Watt", "Imperial", "LANL", "Melbourne", "Stanford", "Stuttgart"]
    colors = ["C0", "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9"]

    font = {'family' : 'normal',
            'weight' : 'normal',
            'size' : 16}
    matplotlib.rc('font', **font)

    figP, axsP = plt.subplots(2, 1, figsize=(12, 8))
    figT, axsT = plt.subplots(1, 1, figsize=(12, 8))
    figA, axsA = plt.subplots(2, 1, figsize=(12, 8))
    figB, axsB = plt.subplots(2, 1, figsize=(12, 8))
    figM, axsM = plt.subplots(1, 1, figsize=(12, 8))
    offset = 0.0

    for fileName, group, color in zip(fileNames, groups, colors):
        print(f'Processing {fileName}.')

        skip_header = 0
        with open(fileName, "r") as file:
            if not (file.readline()[0]).isnumeric():
                skip_header = 1

        delimiter = ','
        skip_footer = 0

        csvData = np.genfromtxt(fileName, delimiter=delimiter, skip_header=skip_header, skip_footer=skip_footer)
        visualizeRow(csvData[0], axsP[0], '1a: sensor 1', 'pressure [N/m2]', group, color, offset)
        visualizeRow(csvData[1], axsP[1], '1b: sensor 2', 'pressure [N/m2]', group, color, offset)

#        visualizeRow(csvData[2]/60, axsT[0], '2: max mobile free phase in Box A', 'time [min]', group, color, offset)
        visualizeRow(csvData[11]/60, axsT, '5: M exceeds 110% of Box C’s width', 'time [min]', group, color, offset)

        visualizeRow(1e3*csvData[3], axsA[0], '3a: mobile free phase', 'mass [g]', group, color, offset)
#        visualizeRow(1e3*csvData[4], axsA[0, 1], '3b: immobile free phase', 'mass [g]', group, color, offset)
        visualizeRow(1e3*csvData[5], axsA[1], '3c: dissolved in water', 'mass [g]', group, color, offset)
#        visualizeRow(1e3*csvData[6], axsA[1, 1], '3d: seal', 'mass [g]', group, color, offset)
        visualizeRow(1e3*csvData[7], axsB[0], '4a: mobile free phase', 'mass [g]', group, color, offset)
#        visualizeRow(1e3*csvData[8], axsB[0, 1], '4b: immobile free phase', 'mass [g]', group, color, offset)
        visualizeRow(1e3*csvData[9], axsB[1], '4c: dissolved in water', 'mass [g]', group, color, offset)
#        visualizeRow(1e3*csvData[10], axsB[1, 1], '4d: seal', 'mass [g]', group, color, offset)

        visualizeRow(1e3*csvData[12], axsM, '6: total CO2 mass in top seal facies', 'mass [g]', group, color, offset)

        offset = offset + 2.0

    axsP[0].set_ylim(1.09e5, 1.14e5)
    axsP[1].set_ylim(1.035e5, 1.065e5)
    axsP[1].legend(loc='center left', bbox_to_anchor=(1, 0.5))


    rect = mpatches.Rectangle([21, 200], 1, 6, fill=True, linewidth=3, color='k', label='experiment lower')
    axsT.add_patch(rect)
    axsT.arrow(22.5, 195.7, 0, 14.6, length_includes_head=True,
             head_width=0.05, head_length=1e-5, linewidth=2, fc='b', ec='b')
    rect = mpatches.Rectangle([23, 296.833], 1, 6, fill=True, linewidth=3, color='k', label='experiment upper')
    axsT.add_patch(rect)
    axsT.arrow(24.5, 262.2, 0, 75, length_includes_head=True,
             head_width=0.05, head_length=1e-5, linewidth=2, fc='b', ec='b')
    axsT.set_xlim(1, 25)

    axsT.set_ylim(8.0e1, 2.2e3)
    # axsT[1].set_yscale('log')
    axsT.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    rect = mpatches.Rectangle([21, 0.335], 1, 0.05, fill=True, linewidth=3, color='k', label='experiment')
    axsA[0].add_patch(rect)
    axsA[0].arrow(22.5, 0.23, 0, 0.26, length_includes_head=True,
             head_width=0.05, head_length=1e-5, linewidth=2, fc='b', ec='b')
    axsA[0].set_xlim(1, 23)

    rect = mpatches.Rectangle([21, 3.475], 1, 0.05, fill=True, linewidth=3, color='k', label='experiment')
    axsA[1].add_patch(rect)
    axsA[1].arrow(22.5, 3.42, 0, 0.16, length_includes_head=True,
             head_width=0.05, head_length=1e-5, linewidth=2, fc='b', ec='b')
    axsA[1].set_xlim(1, 23)


    rect = mpatches.Rectangle([21, -0.005], 1, 0.01, fill=True, linewidth=3, color='k', label='experiment')
    axsB[0].add_patch(rect)
    axsB[0].set_xlim(1, 23)

    rect = mpatches.Rectangle([21, 0.525], 1, 0.05, fill=True, linewidth=3, color='k', label='experiment')
    axsB[1].add_patch(rect)
    axsB[1].arrow(22.5, 0.23, 0, 0.64, length_includes_head=True,
             head_width=0.05, head_length=1e-5, linewidth=2, fc='b', ec='b')
    axsB[1].set_xlim(1, 23)


    axsA[0].set_ylim(0.0, 3e-0)
#    axsA[0][1].set_ylim(0.0, 5e-0)
    axsA[1].set_ylim(0.0, 5e-0)
#    axsA[1][1].set_ylim(0.0, 1e-0)
    axsB[0].set_ylim(0.0, 3e-1)
#    axsB[0][1].set_ylim(0.0, 4e-2)
    axsB[1].set_ylim(0.0, 2.2e-0)
#    axsB[1][1].set_ylim(0.0, 6e-1)
    axsA[1].legend(loc='center left', bbox_to_anchor=(1, 1))
    axsB[1].legend(loc='center left', bbox_to_anchor=(1, 1))

    rect = mpatches.Rectangle([21, 0.3775], 1, 0.005, fill=True, linewidth=3, color='k', label='experiment')
    axsM.add_patch(rect)
    axsM.arrow(22.5, 0.333, 0, 0.094, length_includes_head=True,
             head_width=0.05, head_length=1e-5, linewidth=2, fc='b', ec='b')
    axsM.set_xlim(1, 23)
    axsM.set_ylim(0.0, 7e-1)
    axsM.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    figP.tight_layout()
    figP.savefig('sparse_data_pressure.png', bbox_inches='tight')
    figT.savefig('sparse_data_time.png', bbox_inches='tight')
    figA.savefig('sparse_data_boxA.png', bbox_inches='tight')
    figB.savefig('sparse_data_boxB.png', bbox_inches='tight')
    figM.savefig('sparse_data_topseal.png', bbox_inches='tight')

if __name__ == "__main__":
    assembleSparseData()
