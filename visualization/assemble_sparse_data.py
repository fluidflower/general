#!/usr/bin/env python3
import os
import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib

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

    rect = mpatches.Rectangle((1+offset, p10_mean), 1, p50_mean - p10_mean, color=color, label=group, fill=False, linewidth=2)
    ax.add_patch(rect)
    rect = mpatches.Rectangle((1+offset, p50_mean), 1, p90_mean - p50_mean, color=color, fill=False, linewidth=2)
    ax.add_patch(rect)

    ax.plot([1.5+offset, 1.5+offset], [p50_mean-p50_dev, p50_mean+p50_dev], linewidth=1, linestyle='dashed', color=color)
    ax.plot([1.4+offset, 1.6+offset], [p50_mean-p50_dev, p50_mean-p50_dev], linewidth=1, color=color)
    ax.plot([1.4+offset, 1.6+offset], [p50_mean+p50_dev, p50_mean+p50_dev], linewidth=1, color=color)

    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xticks([])
    ax.set_xlim(0.5, 18.5)

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
                 "../../lanl/sparse_data.csv",
                 "../../melbourne/sparse_data.csv",
                 "../../stanford/sparse_data.csv",
                 "../../stuttgart/sparse_data.csv"]
    groups = ["Austin", "CSIRO", "Delft-DARSim", "Delft-DARTS", "Heriot-Watt", "LANL", "Melbourne", "Stanford", "Stuttgart"]
    colors = ["C0", "C1", "C2", "C3", "#9932CC", "#FF1493", "C7", "C8", "C9"]

    font = {'family' : 'normal',
            'weight' : 'normal',
            'size' : 14}
    matplotlib.rc('font', **font)
    plt.rcParams.update({
        "text.usetex": True,
        "font.family": "monospace",
        "legend.columnspacing": 1.0,
        "legend.handlelength": 1.2
    })

    figP, axsP = plt.subplots(2, 1, figsize=(9, 6))
    figT, axsT = plt.subplots(2, 1, figsize=(9, 6))
    figA, axsA = plt.subplots(2, 2, figsize=(12, 6))
    figB, axsB = plt.subplots(2, 2, figsize=(12, 6))
    figS, axsS = plt.subplots(1, 1, figsize=(10, 4))
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
        visualizeRow(csvData[0]/1e5, axsP[0], r'\textrm{\textbf{\Large 1a: expected maximum pressure at sensor 1}}',
                     r'\textrm{\LARGE pressure [bar]}', group, color, offset)
        visualizeRow(csvData[1]/1e5, axsP[1], r'\textrm{\textbf{\Large 1b: expected maximum pressure at sensor 2}}',
                     r'\textrm{\LARGE pressure [bar]}', group, color, offset)

        visualizeRow(csvData[2]/60/60, axsT[0], r'\textrm{\textbf{\Large 2: maximum mobile gaseous CO$_2$ in Box A}}',
                     r'\textrm{\LARGE time [h]}', group, color, offset)
        visualizeRow(csvData[11]/60/60, axsT[1], r'\textrm{\textbf{\Large 5: $M(t)$ exceeds 110\% of Box C’s width}}',
                     r'\textrm{\LARGE time [h]}', group, color, offset)

        visualizeRow(1e3*csvData[3], axsA[0, 0], r'\textrm{\textbf{\large 3a: mobile gaseous CO$_2$ in Box A at 72\,h}}',
                     r'\textrm{\LARGE mass [g]}', group, color, offset)
        visualizeRow(1e3*csvData[4], axsA[0, 1], r'\textrm{\textbf{\large 3b: immobile gaseous CO$_2$ in Box A at 72\,h}}',
                     r'\textrm{\LARGE mass [g]}', group, color, offset)
        visualizeRow(1e3*csvData[5], axsA[1, 0], r'\textrm{\textbf{\large 3c: CO$_2$ dissolved in liquid phase in Box A at 72\,h}}',
                     r'\textrm{\LARGE mass [g]}', group, color, offset)
        visualizeRow(1e3*csvData[6], axsA[1, 1], r'\textrm{\textbf{\large 3d: CO$_2$ in the seal facies in Box A at 72\,h}}',
                     r'\textrm{\LARGE mass [g]}', group, color, offset)

        visualizeRow(1e3*csvData[7], axsB[0, 0], r'\textrm{\textbf{\large 4a: mobile gaseous CO$_2$ in Box B at 72\,h}}',
                     r'\textrm{\LARGE mass [g]}', group, color, offset)
        visualizeRow(1e3*csvData[8], axsB[0, 1], r'\textrm{\textbf{\large 4b: immobile gaseous CO$_2$ in Box B at 72\,h}}',
                     r'\textrm{\LARGE mass [g]}', group, color, offset)
        visualizeRow(1e3*csvData[9], axsB[1, 0], r'\textrm{\textbf{\large 4c: CO$_2$ dissolved in liquid phase in Box B at 72\,h}}',
                     r'\textrm{\LARGE mass [g]}', group, color, offset)
        visualizeRow(1e3*csvData[10], axsB[1, 1], r'\textrm{\textbf{\large 4d: CO$_2$ in the seal facies in Box B at 72\,h}}',
                     r'\textrm{\LARGE mass [g]}', group, color, offset)

        visualizeRow(1e3*csvData[12], axsS, r'\textrm{\textbf{\Large 6: total CO$_2$ mass in top seal facies in Box A at 120\,h}}',
                     r'\textrm{\Large mass [g]}', group, color, offset)

        offset = offset + 2.0

    axsP[0].set_ylim(1.09e0, 1.14e0)
    axsP[1].set_ylim(1.035e0, 1.065e0)
    axsP[1].set_yticks([1.03, 1.04, 1.05, 1.06, 1.07])
    handles, labels = axsP[1].get_legend_handles_labels()
    figP.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, 1.11), ncol=5)

    axsT[0].set_ylim(3.3, 6.2)
    axsT[1].set_ylim(1.3, 35.0)
    handles, labels = axsT[1].get_legend_handles_labels()
    figT.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, 1.06), ncol=5)

    axsS.set_ylim(-0.02, 0.8)
    handles, labels = axsS.get_legend_handles_labels()
    figS.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, 1.14), ncol=5)

    axsA[0][0].set_ylim(-0.1, 3e-0)
    axsA[0][0].set_yticks([0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0])
    axsA[0][1].set_ylim(-0.02, 5e-1)
    axsA[0][1].set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5])
    axsA[1][0].set_ylim(-0.2, 5e-0)
    axsA[1][0].set_yticks([0.0, 1.0, 2.0, 3.0, 4.0, 5.0])
    axsA[1][1].set_ylim(-0.05, 1e-0)
    axsB[0][0].set_ylim(-0.02, 2.5e-1)
    axsB[0][1].set_ylim(-0.002, 3e-2)
    axsB[1][0].set_ylim(-0.1, 2.2e-0)
    axsB[1][1].set_ylim(-0.05, 6e-1)
    handles, labels = axsA[1][1].get_legend_handles_labels()
    figA.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, 1.05), ncol=5)
    handles, labels = axsB[1][1].get_legend_handles_labels()
    figB.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, 1.05), ncol=5)

    figP.tight_layout()
    figP.savefig('sparse_data_pressure.pdf', bbox_inches='tight')
    figT.savefig('sparse_data_time.pdf', bbox_inches='tight')
    figA.savefig('sparse_data_boxA.pdf', bbox_inches='tight')
    figB.savefig('sparse_data_boxB.pdf', bbox_inches='tight')
    figS.savefig('sparse_data_seal.pdf', bbox_inches='tight')

if __name__ == "__main__":
    assembleSparseData()
