#!/usr/bin/env python3

""""
Script to generate arbitrary data that is conforming
with the format required by the benchmark description
"""

import sys
import os
import argparse
import subprocess
import numpy as np
import math

def generateBenchmarkData():
    """Generate arbitrary data for the FluidFlower benchmark"""

    parser = argparse.ArgumentParser(
        description="This script generates arbitrary data that is conforming "
                    "with the format required by the benchmark description."
    )

    cmdArgs = vars(parser.parse_args())

    with open("arbitrary_spatial_map_24h.csv", "w") as spatialMap:
        spatialMap.write("# x, y, gas saturation [-], CO2 concentration in water [kg/m3]\n")

        ySpace = np.arange(5.0e-3, 1.23e+0, 1.0e-2)
        xSpace = np.arange(5.0e-3, 2.86e+0, 1.0e-2)

        for y in ySpace:
            for x in xSpace:
                spatialMap.write(f'{x:.3e}, {y:.3e}, {x*y:.3e}, {x+y:.3e}\n')

    with open("arbitrary_time_series.csv", "w") as timeSeries:
        timeSeries.write("# t, p_1, p_2, mob_A, imm_A, diss_A, seal_A, <same for B>, M_C\n")

        for t in np.arange(0.0, 120*3600.0+1.0, 600.0):
            timeSeries.write(f'{t:.3e}, {math.sqrt(t):.3e}, {math.log(t+1):.3e}'
                             f', {0.1*t/3600.0:.3e}, {0.2*t/3600.0:.3e}, {0.3*t/3600.0:.3e}, {0.01*t/3600.0:.3e}'
                             f', {0.4*t/3600.0:.3e}, {0.5*t/3600.0:.3e}, {0.6*t/3600.0:.3e}, {0.02*t/3600.0:.3e}'
                             f', {1e-9*t*t:.3e}\n')

if __name__ == "__main__":
    generateBenchmarkData()
