#!/usr/bin/env python3
import os
import argparse
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy import interpolate
from operator import methodcaller

def addExpData(fileName, ax, numFields=1, fieldIdx=0):
    f = []
    minT = -np.inf
    maxT = np.inf

    data = np.genfromtxt(fileName, delimiter=",", skip_header=1)

    for run in range(5):
        dataRun = data[:, (numFields+1)*run:(numFields+1)*(run+1)]
        dataRun = dataRun[~np.isnan(dataRun).any(axis=1)]

        f.append(interpolate.interp1d(dataRun[:, 0], dataRun[:, fieldIdx+1]))
        minT = max(minT, dataRun[0, 0])
        maxT = min(maxT, dataRun[-1, 0])

    ls = np.linspace(minT, maxT, num=1000)
    interpolateddata = list(map(methodcaller('__call__', ls), f))
    meanvalues = np.mean(interpolateddata, axis=0)
    std = np.std(interpolateddata, axis=0)

    e1, = ax.plot(ls, meanvalues, color='k', linewidth=3, label="experiment")
    e2 = ax.fill_between(ls, meanvalues-std, meanvalues+std, color="gray")
    ax.grid(True, which="both")

    return (e1, e2)

def compareTimeSeries():
    """Compare time series for the FluidFlower benchmark"""

    parser = argparse.ArgumentParser(
        description="This script compares the time series quantities "
                    "as required by the benchmark description."
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
            'size' : 16}
    matplotlib.rc('font', **font)
    plt.rcParams.update({
        "text.usetex": True,
        "font.family": "monospace",
        "legend.columnspacing": 0.9,
        "legend.handlelength": 1.2
    })

    figA, axsA = plt.subplots(2, 2, figsize=(11, 7))
    figBC, axsBC = plt.subplots(1, 2, figsize=(11, 3.5))

    fMobileA = []
    fDissolvedA = []
    fSealA = []
    fDissolvedB = []
    fMixingC = []
    minT = -np.inf
    maxT = np.inf

    for fileName in fileNames:
        skip_header = 0
        with open(fileName, "r") as file:
            if not (file.readline()[0]).isnumeric():
                skip_header = 1

        csvData = np.genfromtxt(fileName, delimiter=',', skip_header=skip_header)

        t = csvData[:, 0]/3600
        minT = max(minT, t[0])
        maxT = min(maxT, t[-1])

        fMobileA.append(interpolate.interp1d(t, 1e3*csvData[:, 3]))
        fDissolvedA.append(interpolate.interp1d(t, 1e3*csvData[:, 5]))
        fSealA.append(interpolate.interp1d(t, 1e3*csvData[:, 6]))
        fDissolvedB.append(interpolate.interp1d(t, 1e3*csvData[:, 9]))
        fMixingC.append(interpolate.interp1d(t, csvData[:, 11]))

    ls = np.linspace(minT, maxT, num=1000)

    interpMobileA = list(map(methodcaller('__call__', ls), fMobileA))
    medianMobileA = np.median(interpMobileA, axis=0)
    q1MobileA = np.percentile(interpMobileA, 25, axis=0)
    q3MobileA = np.percentile(interpMobileA, 75, axis=0)
    p2 = axsA[0][0].fill_between(ls, q1MobileA, q3MobileA, color="xkcd:pale brown", label="forecast")

    interpDissolvedA = list(map(methodcaller('__call__', ls), fDissolvedA))
    medianDissolvedA = np.median(interpDissolvedA, axis=0)
    q1DissolvedA = np.percentile(interpDissolvedA, 25, axis=0)
    q3DissolvedA = np.percentile(interpDissolvedA, 75, axis=0)
    axsA[1][0].fill_between(ls, q1DissolvedA, q3DissolvedA, color="xkcd:pale brown")

    interpSealA = list(map(methodcaller('__call__', ls), fSealA))
    medianSealA = np.median(interpSealA, axis=0)
    q1SealA = np.percentile(interpSealA, 25, axis=0)
    q3SealA = np.percentile(interpSealA, 75, axis=0)
    axsA[1][1].fill_between(ls, q1SealA, q3SealA, color="xkcd:pale brown")

    interpDissolvedB = list(map(methodcaller('__call__', ls), fDissolvedB))
    medianDissolvedB = np.median(interpDissolvedB, axis=0)
    q1DissolvedB = np.percentile(interpDissolvedB, 25, axis=0)
    q3DissolvedB = np.percentile(interpDissolvedB, 75, axis=0)
    q2 = axsBC[0].fill_between(ls, q1DissolvedB, q3DissolvedB, color="xkcd:pale brown")

    interpMixingC = list(map(methodcaller('__call__', ls), fMixingC))
    medianMixingC = np.median(interpMixingC, axis=0)
    q1MixingC = np.percentile(interpMixingC, 25, axis=0)
    q3MixingC = np.percentile(interpMixingC, 75, axis=0)
    axsBC[1].fill_between(ls, q1MixingC, q3MixingC, color="xkcd:pale brown")

    for fileName, group, color in zip(fileNames, groups, colors):
        print(f'Processing {fileName}.')

        skip_header = 0
        with open(fileName, "r") as file:
            if not (file.readline()[0]).isnumeric():
                skip_header = 1

        delimiter = ','

        csvData = np.genfromtxt(fileName, delimiter=delimiter, skip_header=skip_header)
        t = csvData[:, 0]/3600

        axsA[0, 0].plot(t, 1e3*csvData[:, 3], label=group, color=color)
        axsA[0, 0].set_title(r'\textrm{\textbf{\Large Box A: mobile gaseous CO$_2$}}')
        axsA[0, 0].set_ylabel(r'\textrm{\LARGE mass [g]}')
        axsA[0, 0].set_xlim(0.1, 121.0)
        axsA[0, 0].set_ylim(-0.1, 3.0)

        axsA[0, 1].set_axis_off()

        axsA[1, 0].plot(t, 1e3*csvData[:, 5], label=group, color=color)
        axsA[1, 0].set_title(r'\textrm{\textbf{\Large Box A: CO$_2$ dissolved in liquid phase}}')
        axsA[1, 0].set_xlabel(r'\textrm{\LARGE time [h]}')
        axsA[1, 0].set_ylabel(r'\textrm{\LARGE mass [g]}')
        axsA[1, 0].set_xlim(0.1, 121.0)
        axsA[1, 0].set_ylim(-0.01, 6.0)

        axsA[1, 1].plot(t, 1e3*csvData[:, 6], label=group, color=color)
        axsA[1, 1].set_title(r'\textrm{\textbf{\Large Box A: CO$_2$ in the seal facies}}')
        axsA[1, 1].set_xlabel(r'\textrm{\LARGE time [h]}')
        axsA[1, 1].set_xlim(0.1, 121.0)
        axsA[1, 1].set_ylim(-0.01, 1.0)

        axsBC[0].plot(t, 1e3*csvData[:, 9], label=group, color=color)
        axsBC[0].set_title(r'\textrm{\textbf{\Large Box B: CO$_2$ dissolved in liquid phase}}')
        axsBC[0].set_xlabel(r'\textrm{\LARGE time [h]}')
        axsBC[0].set_ylabel(r'\textrm{\LARGE mass [g]}')
        axsBC[0].set_xlim(3.0, 121.0)
        axsBC[0].set_ylim(-0.01, 2.5)

        axsBC[1].plot(t, csvData[:, 11], label=group, color=color)
        axsBC[1].set_title(r'\textrm{\textbf{\Large Box C: convection}}')
        axsBC[1].set_xlabel(r'\textrm{\LARGE time [h]}')
        axsBC[1].set_ylabel(r'\textrm{\LARGE $M$ [m]}')
        axsBC[1].set_xlim(1.0, 121.0)

    (e1, e2) = addExpData("../../experiment/benchmarkdata/time_series/mobile_box_a.csv", axsA[0][0])
    axsA[0][0].set_xscale("log")
    addExpData("../../experiment/benchmarkdata/time_series/dissolved_boxes_a_b.csv", axsA[1][0], numFields=2, fieldIdx=0)
    axsA[1][0].set_xscale("log")
    addExpData("../../experiment/benchmarkdata/time_series/dissolved_box_a_seal.csv", axsA[1][1])
    axsA[1][1].set_xscale("log")
    (f1, f2) = addExpData("../../experiment/benchmarkdata/time_series/dissolved_boxes_a_b.csv", axsBC[0], numFields=2, fieldIdx=1)
    axsBC[0].set_xscale("log")
    addExpData("../../experiment/benchmarkdata/time_series/mixing_box_c.csv", axsBC[1])
    axsBC[1].set_xscale("log")

    p1, = axsA[0][0].plot(ls, medianMobileA, color="xkcd:brown", linewidth=3, label="forecast")
    axsA[1][0].plot(ls, medianDissolvedA, color="xkcd:brown", linewidth=3, label="forecast")
    axsA[1][1].plot(ls, medianSealA, color="xkcd:brown", linewidth=3, label="forecast")
    handles, labels = axsA[0][0].get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    del by_label["forecast"]
    by_label["forecast"] = (p2, p1)
    by_label[r"\textrm{forecast}"] = by_label.pop("forecast")
    del by_label["experiment"]
    by_label["experiment"] = (e2, e1)
    by_label[r"\textrm{experiment}"] = by_label.pop("experiment")
    figA.legend(by_label.values(), by_label.keys(), loc='upper right', bbox_to_anchor=(0.91, 0.85), ncol=2)
    axsA[0, 0].set_xticklabels([])
    figA.savefig('compare_time_series_boxA.pdf', bbox_inches='tight')

    q1, = axsBC[0].plot(ls, medianDissolvedB, color="xkcd:brown", linewidth=3, label="forecast")
    axsBC[1].plot(ls, medianMixingC, color="xkcd:brown", linewidth=3, label="forecast")
    handles, labels = axsBC[0].get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    del by_label["forecast"]
    by_label["forecast"] = (q2, q1)
    by_label[r"\textrm{forecast}"] = by_label.pop("forecast")
    del by_label["experiment"]
    by_label["experiment"] = (f2, f1)
    by_label[r"\textrm{experiment}"] = by_label.pop("experiment")
    figBC.legend(by_label.values(), by_label.keys(), loc='upper center', bbox_to_anchor=(0.5, 1.3), ncol=4)
    figBC.savefig('compare_time_series_boxBC.pdf', bbox_inches='tight')


if __name__ == "__main__":
    compareTimeSeries()
