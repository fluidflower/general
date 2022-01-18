#!/usr/bin/env python3
import os
import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import math

def visualizeRow(row, ax, title, ylabel, group, color, offset):
    p10_mean = row[1]
    p50_mean = row[2]
    p90_mean = row[3]
    p10_dev = row[4]
    p50_dev = row[5]
    p90_dev = row[6]

    rect = mpatches.Rectangle((1+offset, p10_mean), 1, p90_mean - p10_mean, color=color, label=group)
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
    ax.legend()

def assembleSparseData():
    """Visualize sparse data for the FluidFlower benchmark"""

    parser = argparse.ArgumentParser(
        description="This script visualizes the sparse data "
                    "as required by the benchmark description."
    )

    fileNames = ["../../austin/sparse_data.csv",
                 "../../csiro/sparse_data.csv",
                 "../../delft/sparse_data.csv",
                 "../../herriot-watt/sparse_data_HW.csv",
                 "../../lanl/sparse_data.csv",
                 "../../melbourne/sparse_data.csv"]
    groups = ["Austin", "CSIRO", "Delft", "Herriot-Watt", "LANL", "Melbourne"]
    colors = ["C0", "C1", "C2", "C3", "C4", "C5"]

    figP, axsP = plt.subplots(2, 1, figsize=(12, 8))
    figT, axsT = plt.subplots(2, 1, figsize=(12, 8))
    figA, axsA = plt.subplots(2, 2, figsize=(16, 8))
    figB, axsB = plt.subplots(2, 2, figsize=(16, 8))
    offset = 0.0

    for fileName, group, color in zip(fileNames, groups, colors):
        print(f'Processing {fileName}.')

        skip_header = 0
        with open(fileName, "r") as file:
            if not (file.readline()[0]).isnumeric():
                skip_header = 1

        delimiter = ','
        skip_footer = 0
        if group == 'Melbourne':
            delimiter = '\t'
            skip_footer = 7

        csvData = np.genfromtxt(fileName, delimiter=delimiter, skip_header=skip_header, skip_footer=skip_footer)

        if group != "Herriot-Watt":
            visualizeRow(csvData[0], axsP[0], '1a: sensor 1', 'pressure [N/m2]', group, color, offset)
            visualizeRow(csvData[1], axsP[1], '1b: sensor 2', 'pressure [N/m2]', group, color, offset)

        visualizeRow(csvData[2], axsT[0], '2: max mobile free phase in Box A', 'time [s]', group, color, offset)
        # axsT[0].set_ylim(0.0, 1e6)
        axsT[0].set_yscale('log')

        if group != "Melbourne":
            visualizeRow(csvData[3], axsA[0, 0], '3a: mobile free phase', 'mass [kg]', group, color, offset)
            visualizeRow(csvData[4], axsA[0, 1], '3b: immobile free phase', 'mass [kg]', group, color, offset)
            visualizeRow(csvData[5], axsA[1, 0], '3c: dissolved in water', 'mass [kg]', group, color, offset)
            visualizeRow(csvData[6], axsA[1, 1], '3d: seal', 'mass [kg]', group, color, offset)
            visualizeRow(csvData[7], axsB[0, 0], '4a: mobile free phase', 'mass [kg]', group, color, offset)
            visualizeRow(csvData[8], axsB[0, 1], '4b: immobile free phase', 'mass [kg]', group, color, offset)
            visualizeRow(csvData[9], axsB[1, 0], '4c: dissolved in water', 'mass [kg]', group, color, offset)
            visualizeRow(csvData[10], axsB[1, 1], '4d: seal', 'mass [kg]', group, color, offset)
            visualizeRow(csvData[11], axsT[1], '5: M exceeds 110% of Box C’s width', 'time [s]', group, color, offset)
        axsT[1].set_ylim(1e4, 1e8)
        axsT[1].set_yscale('log')

        offset = offset + 2.0

    # fig = plt.figure(figsize=(8, 4))
    # ax = plt.subplot(121)
    # visualizeRow(csvData[2], ax, '2: max mobile free phase in Box A', 'time [s]')
    # ax = plt.subplot(122)
    # visualizeRow(csvData[11], ax, '5: M exceeds 110% of Box C’s width', '')
    # fig.tight_layout()
    # fig.savefig(f'{baseFileName}_time.png', bbox_inches='tight')

    # fig, ax = plt.subplots(figsize=(4, 4))
    # visualizeRow(csvData[12], ax, '6: total mass of CO2 in the top seal facies', 'mass [kg]')
    # fig.tight_layout()
    # fig.savefig(f'{baseFileName}_mass.png', bbox_inches='tight')

    #     if group != "Delft":
    #         axsP[0].plot(t, csvData[:, 1], label=group)
    #     else:
    #         axsP[0].plot(t, 1e5*csvData[:, 1], label=group)
    #     axsP[0].set_title('sensor 1')
    #     axsP[0].set_xlabel('time [h]')
    #     axsP[0].set_ylabel('pressure [N/m2]')
    #     axsP[0].set_ylim(0.9e5, 1.3e5)
    #     axsP[0].set_xlim(-1.0, 125.0)

    figP.tight_layout()
    figP.savefig('sparse_data_pressure.png', bbox_inches='tight')
    figT.savefig('sparse_data_time.png', bbox_inches='tight')
    figA.savefig('sparse_data_boxA.png', bbox_inches='tight')
    figB.savefig('sparse_data_boxB.png', bbox_inches='tight')

if __name__ == "__main__":
    assembleSparseData()
