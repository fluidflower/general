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

    ax.plot(60*ls, meanvalues, color='k', linewidth=2, label="exp. mean")
    ax.fill_between(60*ls, meanvalues-std, meanvalues+std, color="gray")
    ax.grid(True, which="both")

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
            'size' : 14}
    matplotlib.rc('font', **font)

    figP, axsP = plt.subplots(1, 2, figsize=(12, 4))
    figPT, axsPT = plt.subplots(1, 2, figsize=(12, 4))
    figA, axsA = plt.subplots(2, 2, figsize=(14, 9))
    figB, axsB = plt.subplots(2, 2, figsize=(14, 9))
    figC, axsC = plt.subplots(figsize=(6, 4))
    figT, axsT = plt.subplots(figsize=(6, 4))

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

        t = csvData[:, 0]/60
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
    stdMobileA = np.std(interpMobileA, axis=0)
    axsA[0][0].plot(ls, medianMobileA, color='r', linewidth=2, label="forecast")
    axsA[0][0].fill_between(ls, medianMobileA-stdMobileA, medianMobileA+stdMobileA, color="xkcd:pale pink")

    interpDissolvedA = list(map(methodcaller('__call__', ls), fDissolvedA))
    medianDissolvedA = np.median(interpDissolvedA, axis=0)
    stdDissolvedA = np.std(interpDissolvedA, axis=0)
    axsA[1][0].plot(ls, medianDissolvedA, color='r', linewidth=2, label="forecast")
    axsA[1][0].fill_between(ls, medianDissolvedA-stdDissolvedA, medianDissolvedA+stdDissolvedA, color="xkcd:pale pink")

    interpSealA = list(map(methodcaller('__call__', ls), fSealA))
    medianSealA = np.median(interpSealA, axis=0)
    stdSealA = np.std(interpSealA, axis=0)
    axsA[1][1].plot(ls, medianSealA, color='r', linewidth=2, label="forecast")
    axsA[1][1].fill_between(ls, medianSealA-stdSealA, medianSealA+stdSealA, color="xkcd:pale pink")

    interpDissolvedB = list(map(methodcaller('__call__', ls), fDissolvedB))
    medianDissolvedB = np.median(interpDissolvedB, axis=0)
    stdDissolvedB = np.std(interpDissolvedB, axis=0)
    axsB[1][0].plot(ls, medianDissolvedB, color='r', linewidth=2, label="forecast")
    axsB[1][0].fill_between(ls, medianDissolvedB-stdDissolvedB, medianDissolvedB+stdDissolvedB, color="xkcd:pale pink")

    interpMixingC = list(map(methodcaller('__call__', ls), fMixingC))
    medianMixingC = np.median(interpMixingC, axis=0)
    stdMixingC = np.std(interpMixingC, axis=0)
    axsC.plot(ls, medianMixingC, color='r', linewidth=2, label="forecast")
    axsC.fill_between(ls, medianMixingC-stdMixingC, medianMixingC+stdMixingC, color="xkcd:pale pink")

    addExpData("../../experiment/benchmarkdata/time_series/mobile_box_a.csv", axsA[0][0])
    axsA[0][0].set_xscale("log")
    addExpData("../../experiment/benchmarkdata/time_series/dissolved_boxes_a_b.csv", axsA[1][0], numFields=2, fieldIdx=0)
    addExpData("../../experiment/benchmarkdata/time_series/dissolved_box_a_seal.csv", axsA[1][1])
    addExpData("../../experiment/benchmarkdata/time_series/dissolved_boxes_a_b.csv", axsB[1][0], numFields=2, fieldIdx=1)
    axsB[1][0].set_xscale("log")
    addExpData("../../experiment/benchmarkdata/time_series/mixing_box_c.csv", axsC)
    axsC.set_xscale("log")

    for fileName, group, color in zip(fileNames, groups, colors):
        print(f'Processing {fileName}.')

        skip_header = 0
        with open(fileName, "r") as file:
            if not (file.readline()[0]).isnumeric():
                skip_header = 1

        delimiter = ','

        csvData = np.genfromtxt(fileName, delimiter=delimiter, skip_header=skip_header)
        t = csvData[:, 0]/60

        axsP[0].plot(t, csvData[:, 1]/1e5, label=group, color=color)
        axsP[0].set_title('sensor 1')
        axsP[0].set_xlabel('time [min]')
        axsP[0].set_ylabel('pressure [bar]')
        axsP[0].set_ylim(1.09e0, 1.15e0)
        axsP[0].set_xlim(-1.0, 7260.0)

        axsP[1].plot(t, csvData[:, 2]/1e5, label=group, color=color)
        axsP[1].set_title('sensor 2')
        axsP[1].set_xlabel('time [min]')
        axsP[1].set_ylim(1.03e0, 1.09e0)
        axsP[1].set_xlim(-1.0, 7260.0)

        axsPT[0].plot(t, csvData[:, 1]/1e5, label=group, color=color)
        axsPT[0].set_title('sensor 1')
        axsPT[0].set_xlabel('time [min]')
        axsPT[0].set_ylabel('pressure [bar]')
        axsPT[0].set_xlim(-0.1, 610.0)
        axsPT[0].set_ylim(1.09e0, 1.15e0)

        axsPT[1].plot(t, csvData[:, 2]/1e5, label=group, color=color)
        axsPT[1].set_title('sensor 2')
        axsPT[1].set_xlabel('time [min]')
        axsPT[1].set_xlim(-0.1, 610.0)
        axsPT[1].set_ylim(1.03e0, 1.09e0)

#        axsA[0, 0].plot(t, 1e3*csvData[:, 3], label=group, color=color)
        axsA[0, 0].set_title('mobile')
        axsA[0, 0].set_ylabel('CO2 [g]')
        axsA[0, 0].set_xlim(5.0, 7260.0)
        axsA[0, 0].set_ylim(-0.1, 3.0)

        axsA[0, 1].plot(t, 1e3*csvData[:, 4], label=group, color=color)
        axsA[0, 1].set_title('immobile')
        axsA[0, 1].set_xlim(-1.0, 7260.0)
        axsA[0, 1].set_ylim(-0.01, 0.3)

        axsA[1, 0].plot(t, 1e3*csvData[:, 5], label=group, color=color)
        axsA[1, 0].set_title('dissolved')
        axsA[1, 0].set_xlabel('time [min]')
        axsA[1, 0].set_ylabel('CO2 [g]')
        axsA[1, 0].set_xlim(-1.0, 7260.0)
        axsA[1, 0].set_ylim(-0.01, 6.0)

        axsA[1, 1].plot(t, 1e3*csvData[:, 6], label=group, color=color)
        axsA[1, 1].set_title('seal')
        axsA[1, 1].set_xlabel('time [min]')
        axsA[1, 1].set_xlim(-1.0, 7260.0)
        axsA[1, 1].set_ylim(-0.01, 1.0)

        axsB[0, 0].plot(t, 1e3*csvData[:, 7], label=group, color=color)
        axsB[0, 0].set_title('mobile')
        axsB[0, 0].set_ylabel('CO2 [g]')
        axsB[0, 0].set_xlim(-1.0, 7260.0)
        axsB[0, 0].set_ylim(-0.01, 0.6)

        axsB[0, 1].plot(t, 1e3*csvData[:, 8], label=group, color=color)
        axsB[0, 1].set_title('immobile')
        axsB[0, 1].set_xlim(-1.0, 7260.0)
        axsB[0, 1].set_ylim(-0.001, 0.07)

        axsB[1, 0].plot(t, 1e3*csvData[:, 9], label=group, color=color)
        axsB[1, 0].set_title('dissolved')
        axsB[1, 0].set_xlabel('time [min]')
        axsB[1, 0].set_ylabel('CO2 [g]')
        axsB[1, 0].set_xlim(200.0, 7260.0)
        axsB[1, 0].set_ylim(-0.01, 2.5)

        axsB[1, 1].plot(t, 1e3*csvData[:, 10], label=group, color=color)
        axsB[1, 1].set_title('seal')
        axsB[1, 1].set_xlabel('time [min]')
        axsB[1, 1].set_xlim(-1.0, 7260.0)
        axsB[1, 1].set_ylim(-0.01, 0.6)

        axsC.plot(t, csvData[:, 11], label=group, color=color)
        axsC.set_title('convection in Box C')
        axsC.set_xlabel('time [min]')
        axsC.set_ylabel('M [m]')
        axsC.set_xlim(5.0, 7260.0)
        axsC.legend(loc='center left', bbox_to_anchor=(1, 0.5))

        axsT.plot(t, 1e3*csvData[:, 12], label=group, color=color)
        axsT.set_title('total CO2 mass')
        axsT.set_xlabel('time [min]')
        axsT.set_ylabel('mass [g]')
        axsT.set_xlim(-1.0, 7260.0)
        axsT.set_ylim(-0.01, 10.0)
        axsT.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    handles, labels = axsP[1].get_legend_handles_labels()
    figP.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=5)
    figP.savefig('time_series_pressure.png', bbox_inches='tight')

    handles, labels = axsPT[1].get_legend_handles_labels()
    figPT.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=5)
    figPT.savefig('time_series_pressure_zoom_time.png', bbox_inches='tight')

    handles, labels = axsA[0][0].get_legend_handles_labels()
    figA.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, 1.01), ncol=5)
    figA.savefig('time_series_boxA.png', bbox_inches='tight')

    handles, labels = axsB[1][1].get_legend_handles_labels()
    figB.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, 1.01), ncol=5)
    figB.savefig('time_series_boxB.png', bbox_inches='tight')

    figC.savefig('time_series_boxC.png', bbox_inches='tight')
    figT.savefig('time_series_co2mass.png', bbox_inches='tight')

if __name__ == "__main__":
    compareTimeSeries()
