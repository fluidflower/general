#!/usr/bin/env python3
import argparse
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

def analyzeBoxC():
    """Analyze the temporal evolution of the quantity M for the FluidFlower benchmark"""

    parser = argparse.ArgumentParser(
        description="This script analyzes the temporal evolution of the quantity M "
                    "required by the benchmark description."
    )

    fileNames = ["../../austin/time_series.csv",
                 "../../csiro/time_series.csv",
                 "../../delft/delft-DARSim/time_series.csv",
                 "../../delft/delft-DARTS/time_series.csv",
                 "../../herriot-watt/HWU-FinalTimeSeries.csv",
                 "../../lanl/time_series.csv",
                 "../../melbourne/time_series.csv",
                 "../../stanford/time_series_final.csv",
                 "../../stuttgart/time_series.csv"]
    groups = ["Austin", "CSIRO", "Delft-DARSim", "Delft-DARTS", "Heriot-Watt", "LANL", "Melbourne", "Stanford", "Stuttgart"]
    colors = ["C0", "C1", "C2", "C3", "C4", "C6", "C7", "C8", "C9"]

    font = {'family' : 'normal',
            'weight' : 'normal',
            'size' : 14}
    matplotlib.rc('font', **font)
    plt.rcParams.update({
        "text.usetex": True,
        "font.family": "monospace",
    })

    figC, axsC = plt.subplots(figsize=(5, 3))

    for fileName, group, color in zip(fileNames, groups, colors):
        print(f'Processing {fileName}.')

        skip_header = 0
        with open(fileName, "r") as file:
            if not (file.readline()[0]).isnumeric():
                skip_header = 1

        delimiter = ','

        csvData = np.genfromtxt(fileName, delimiter=delimiter, skip_header=skip_header)
        t = csvData[:, 0]/60/60

        axsC.plot(t, csvData[:, 11], label=group, color=color)
        axsC.plot([0, 10], [1.65, 1.65], color='k', linestyle='dashed')
        axsC.plot([16200/60/60, 16200/60/60], [-0.1, 0.76771608987192], color='C0', linestyle='dashed')
        axsC.plot([10000/60/60, 10000/60/60], [-0.1, 1.47], color='C4', linestyle='dashed')
        axsC.plot([13059/60/60, 13059/60/60], [-0.1, 0.36], color='C7', linestyle='dashed')
        axsC.plot([13500/60/60, 13500/60/60], [-0.1, 1.672570], color='C8', linestyle='dashed')
        axsC.plot([33933/60/60, 33933/60/60], [-0.1, 1.56], color='C9', linestyle='dashed')
        axsC.set_title(r'\textrm{\textbf{\Large Box C: convection}}')
        axsC.set_xlabel(r'\textrm{time [h]}')
        axsC.set_ylabel(r'\textrm{$M$ [m]}')
        axsC.set_xlim(0, 10.0)
        axsC.set_ylim(-0.1, 2.5)
        axsC.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    figC.savefig('analyze_boxC.pdf', bbox_inches='tight')

if __name__ == "__main__":
    analyzeBoxC()
