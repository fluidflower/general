#!/usr/bin/env python3
import os
import argparse
import numpy as np
import matplotlib.pyplot as plt

def assembleTimeSeries():
    """Visualize time series for the FluidFlower benchmark"""

    parser = argparse.ArgumentParser(
        description="This script visualizes the time series quantities "
                    "as required by the benchmark description."
    )

    fileNames = ["../../austin/time_series.csv",
                 "../../csiro/time_series.csv",
                 "../../delft/delft-DARSim/time_series.csv",
                 "../../delft/delft-DARTS/time_series.csv",
                 "../../imperial/time_series.csv",
                 "../../lanl/time_series.csv",
                 "../../melbourne/time_series.csv",
                 "../../stanford/dissol_low/time_series_.csv",
                 "../../stuttgart/spatial_maps_first_day/time_series.csv"]
    groups = ["Austin", "CSIRO", "Delft-DARSim", "Delft-DARTS", "Imperial", "LANL", "Melbourne", "Stanford", "Stuttgart"]

    figP, axsP = plt.subplots(1, 2, figsize=(12, 4))
    figPZ, axsPZ = plt.subplots(1, 2, figsize=(12, 4))
    figPT, axsPT = plt.subplots(1, 2, figsize=(12, 4))
    figA, axsA = plt.subplots(2, 2, figsize=(14, 9))
    figB, axsB = plt.subplots(2, 2, figsize=(14, 9))
    figC, axsC = plt.subplots(figsize=(6, 4))
    figT, axsT = plt.subplots(figsize=(6, 4))

    for fileName, group in zip(fileNames, groups):
        print(f'Processing {fileName}.')

        skip_header = 0
        with open(fileName, "r") as file:
            if not (file.readline()[0]).isnumeric():
                skip_header = 1

        delimiter = ','

        csvData = np.genfromtxt(fileName, delimiter=delimiter, skip_header=skip_header)
        t = csvData[:, 0]/3600

        axsP[0].plot(t, csvData[:, 1], label=group)
        axsP[0].set_title('sensor 1')
        axsP[0].set_xlabel('time [h]')
        axsP[0].set_ylabel('pressure [N/m2]')
        axsP[0].set_ylim(0.9e5, 1.3e5)
        axsP[0].set_xlim(-1.0, 25.0)

        axsP[1].plot(t, csvData[:, 2], label=group)
        axsP[1].set_title('sensor 2')
        axsP[1].set_xlabel('time [h]')
        axsP[1].set_ylim(0.9e5, 1.3e5)
        axsP[1].set_xlim(-1.0, 25.0)
        axsP[1].legend()

        axsPZ[0].plot(t, csvData[:, 1], label=group)
        axsPZ[0].set_title('sensor 1')
        axsPZ[0].set_xlabel('time [h]')
        axsPZ[0].set_ylabel('pressure [N/m2]')
        axsPZ[0].set_ylim(1.09e5, 1.115e5)
        axsPZ[0].set_xlim(-1.0, 25.0)

        axsPZ[1].plot(t, csvData[:, 2], label=group)
        axsPZ[1].set_title('sensor 2')
        axsPZ[1].set_xlabel('time [h]')
        axsPZ[1].set_ylim(1.035e5, 1.055e5)
        axsPZ[1].set_xlim(-1.0, 25.0)
        axsPZ[1].legend()

        axsPT[0].plot(t, csvData[:, 1], label=group)
        axsPT[0].set_title('sensor 1')
        axsPT[0].set_xlabel('time [h]')
        axsPT[0].set_ylabel('pressure [N/m2]')
        axsPT[0].set_xlim(-0.1, 10.0)
        axsPT[0].set_ylim(1.0e5, 1.2e5)

        axsPT[1].plot(t, csvData[:, 2], label=group)
        axsPT[1].set_title('sensor 2')
        axsPT[1].set_xlabel('time [h]')
        axsPT[1].set_xlim(-0.1, 10.0)
        axsPT[1].set_ylim(1.0e5, 1.2e5)
        axsPT[1].legend()

        axsA[0, 0].plot(t, csvData[:, 3], label=group)
        axsA[0, 0].set_title('mobile')
        axsA[0, 0].set_ylabel('CO2 [kg]')
        axsA[0, 0].set_xlim(-1.0, 25.0)
        axsA[0, 0].set_ylim(-0.0001, 0.003)

        axsA[0, 1].plot(t, csvData[:, 4], label=group)
        axsA[0, 1].set_title('immobile')
        axsA[0, 1].set_xlim(-1.0, 25.0)
        axsA[0, 1].set_ylim(-0.0001, 0.001)

        axsA[1, 0].plot(t, csvData[:, 5], label=group)
        axsA[1, 0].set_title('dissolved')
        axsA[1, 0].set_xlabel('time [h]')
        axsA[1, 0].set_ylabel('CO2 [kg]')
        axsA[1, 0].set_xlim(-1.0, 25.0)

        axsA[1, 1].plot(t, csvData[:, 6], label=group)
        axsA[1, 1].set_title('seal')
        axsA[1, 1].set_xlabel('time [h]')
        axsA[1, 1].legend()
        axsA[1, 1].set_xlim(-1.0, 25.0)
        axsA[1, 1].set_ylim(-0.0001, 0.002)

        axsB[0, 0].plot(t, csvData[:, 7], label=group)
        axsB[0, 0].set_title('mobile')
        axsB[0, 0].set_ylabel('CO2 [kg]')
        axsB[0, 0].set_xlim(-1.0, 25.0)
        axsB[0, 0].set_ylim(-0.0001, 0.0035)

        axsB[0, 1].plot(t, csvData[:, 8], label=group)
        axsB[0, 1].set_title('immobile')
        axsB[0, 1].set_xlim(-1.0, 25.0)
        axsB[0, 1].set_ylim(-0.0001, 0.0015)

        axsB[1, 0].plot(t, csvData[:, 9], label=group)
        axsB[1, 0].set_title('dissolved')
        axsB[1, 0].set_xlabel('time [h]')
        axsB[1, 0].set_ylabel('CO2 [kg]')
        axsB[1, 0].set_xlim(-1.0, 25.0)

        axsB[1, 1].plot(t, csvData[:, 10], label=group)
        axsB[1, 1].set_title('seal')
        axsB[1, 1].set_xlabel('time [h]')
        axsB[1, 1].legend()
        axsB[1, 1].set_xlim(-1.0, 25.0)
        axsB[1, 1].set_ylim(-0.0001, 0.002)

        axsC.plot(t, csvData[:, 11], label=group)
        axsC.set_title('convection in Box C')
        axsC.set_xlabel('time [h]')
        axsC.set_ylabel('M [m]')
        axsC.set_xlim(-1.0, 25.0)
        axsC.legend(loc='center left', bbox_to_anchor=(1, 0.5))

        axsT.plot(t, csvData[:, 12], label=group)
        axsT.set_title('total CO2 mass')
        axsT.set_xlabel('time [h]')
        axsT.set_ylabel('mass [kg]')
        axsT.set_xlim(-1.0, 25.0)
        axsT.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    figP.savefig('time_series_pressure.png', bbox_inches='tight')
    figPZ.savefig('time_series_pressure_zoom_values.png', bbox_inches='tight')
    figPT.savefig('time_series_pressure_zoom_time.png', bbox_inches='tight')
    figA.savefig('time_series_boxA.png', bbox_inches='tight')
    figB.savefig('time_series_boxB.png', bbox_inches='tight')
    figC.savefig('time_series_boxC.png', bbox_inches='tight')
    figT.savefig('time_series_co2mass.png', bbox_inches='tight')

if __name__ == "__main__":
    assembleTimeSeries()
