#!/usr/bin/env python3

""""
Script to calculate Wasserstein distances between segmented data.
"""

import sys
sys.path.append('../visualization/')
import generate_segmented_images as seg
import argparse
import numpy as np
import os.path
from PIL import Image
import emd


def calculateEMD(modelResult, experimentalData):
    modImage = Image.new('L', (280, 120))
    modPixels = modImage.load()
    for i in range(0, modImage.size[0]):
        for j in range(0, modImage.size[1]):
            if modelResult[j, i] == 1:
                modPixels[i, j] = 128
            elif modelResult[j, i] == 2:
                modPixels[i, j] = 255
            else:
                modPixels[i, j] = 0

    modImage.save('mod.png')

    expImage = Image.new('L', (280, 120))
    expPixels = expImage.load()
    for i in range(0, expImage.size[0]):
        for j in range(0, expImage.size[1]):
            if experimentalData[j, i] == 1:
                expPixels[i, j] = 128
            elif experimentalData[j, i] == 2:
                expPixels[i, j] = 255
            else:
                expPixels[i, j] = 0

    expImage.save('exp.png')

    return emd.calculateEMD('mod.png', 'exp.png')


parser = argparse.ArgumentParser()
parser.add_argument("-satmin", "--minimumsaturation", type=float, default=1e-2,
                    help="The minimum saturation above which gaseous CO2 is considered for the segmentation.")
parser.add_argument("-conmin", "--minimumconcentration", type=float, default=1e-1,
                    help="The minimum concentration above which CO2 is considered to be dissolved in the liquid phase for the segmentation.")

cmdArgs = vars(parser.parse_args())

baseFileNames = ['../../austin/spatial_maps/spatial_map_',
                 '../../csiro/spatial_map_',
                 '../../delft/delft-DARSim/spatial_map_',
                 '../../delft/delft-DARTS/spatial_map_',
                 '../../heriot-watt/spatial_map_',
                 '../../lanl/spatial_map_',
                 '../../melbourne/spatial_map_',
                 '../../stanford/spatial_maps/spatial_map_',
                 '../../stuttgart/spatial_map_']

numGroups = len(baseFileNames)
numExps = 5
numGroupsPlusExps = numGroups + numExps
distances = np.zeros(((numGroups + numExps)*5, (numGroups + numExps)*5))

for hourI in [24, 48, 72, 96, 120]:
    for hourJ in [hourI]: #[24, 48, 72, 96, 120]:
        if hourJ < hourI: continue

        for i, baseFileNameI in zip(range(numGroups), baseFileNames):
            fileNameI = baseFileNameI + str(hourI) + 'h.csv'
            if (not os.path.exists(fileNameI)): continue

            if 'watt' in fileNameI:
                modelResultI = seg.generateSegmentMap(fileNameI, 0.03, 2.83, 0.03, 1.23, cmdArgs["minimumsaturation"], cmdArgs["minimumconcentration"])
            else:
                modelResultI = seg.generateSegmentMap(fileNameI, 0.0, 2.86, 0.0, 1.23, cmdArgs["minimumsaturation"], cmdArgs["minimumconcentration"])
            row = int((hourI/24 - 1)*numGroupsPlusExps + i)

            for j, baseFileNameJ in zip(range(numGroups), baseFileNames):
                if j <= i and hourJ == hourI: continue

                fileNameJ = baseFileNameJ + str(hourJ) + 'h.csv'
                if (not os.path.exists(fileNameJ)): continue

                if 'watt' in fileNameJ:
                    modelResultJ = seg.generateSegmentMap(fileNameJ, 0.03, 2.83, 0.03, 1.23, cmdArgs["minimumsaturation"], cmdArgs["minimumconcentration"])
                else:
                    modelResultJ = seg.generateSegmentMap(fileNameJ, 0.0, 2.86, 0.0, 1.23, cmdArgs["minimumsaturation"], cmdArgs["minimumconcentration"])

                col = int((hourJ/24 - 1)*numGroupsPlusExps + j)
                distances[row][col] = calculateEMD(modelResultI, modelResultJ)

                print(f'{hourI}, {hourJ}, {i}, {j} -> ({row}, {col}): {distances[row][col]}')

            for j in range(numGroups, numGroups + numExps):
                if j <= i and hourJ == hourI: continue

                fileNameJ = '../../experiment/benchmarkdata/spatial_maps/run' + str(j - numGroups + 1) + '/segmentation_' + str(hourJ) + 'h.csv'
                experimentalDataJ = np.loadtxt(fileNameJ, dtype='int', delimiter=',')
                # skip the first 30 rows as they are not contained in the modeling results
                experimentalDataJ = experimentalDataJ[30:, :]

                col = int((hourJ/24 - 1)*numGroupsPlusExps + j)
                distances[row][col] = calculateEMD(modelResultI, experimentalDataJ)

                print(f'{hourI}, {hourJ}, {i}, {j} -> ({row}, {col}): {distances[row][col]}')

        for i in range(numGroups, numGroups + numExps):
            fileNameI = '../../experiment/benchmarkdata/spatial_maps/run' + str(i - numGroups + 1) + '/segmentation_' + str(hourI) + 'h.csv'
            experimentalDataI = np.loadtxt(fileNameI, dtype='int', delimiter=',')
            # skip the first 30 rows as they are not contained in the modeling results
            experimentalDataI = experimentalDataI[30:, :]
            row = int((hourI/24 - 1)*numGroupsPlusExps + i)

            for j, baseFileNameJ in zip(range(numGroups), baseFileNames):
                if j <= i and hourJ == hourI: continue

                fileNameJ = baseFileNameJ + str(hourJ) + 'h.csv'
                if (not os.path.exists(fileNameJ)): continue

                if 'watt' in fileNameJ:
                    modelResultJ = seg.generateSegmentMap(fileNameJ, 0.03, 2.83, 0.03, 1.23, cmdArgs["minimumsaturation"], cmdArgs["minimumconcentration"])
                else:
                    modelResultJ = seg.generateSegmentMap(fileNameJ, 0.0, 2.86, 0.0, 1.23, cmdArgs["minimumsaturation"], cmdArgs["minimumconcentration"])

                col = int((hourJ/24 - 1)*numGroupsPlusExps + j)
                distances[row][col] = calculateEMD(experimentalDataI, modelResultJ)

                print(f'{hourI}, {hourJ}, {i}, {j} -> ({row}, {col}): {distances[row][col]}')

            for j in range(numGroups, numGroups + numExps):
                if j <= i and hourJ == hourI: continue

                fileNameJ = '../../experiment/benchmarkdata/spatial_maps/run' + str(j - numGroups + 1) + '/segmentation_' + str(hourJ) + 'h.csv'
                experimentalDataJ = np.loadtxt(fileNameJ, dtype='int', delimiter=',')
                # skip the first 30 rows as they are not contained in the modeling results
                experimentalDataJ = experimentalDataJ[30:, :]

                col = int((hourJ/24 - 1)*numGroupsPlusExps + j)
                distances[row][col] = calculateEMD(experimentalDataI, experimentalDataJ)

                print(f'{hourI}, {hourJ}, {i}, {j} -> ({row}, {col}): {distances[row][col]}')

distances = distances + distances.T - np.diag(distances.diagonal())

np.savetxt("segmented_distances.csv", distances, delimiter=",")
