#!/usr/bin/env python3
import subprocess
import numpy as np
import generate_segmented_images as seg

fileNames = ["../../austin/spatial_maps/spatial_map_120h.csv",
             "../../csiro/spatial_map_120h.csv",
             "../../delft/delft-DARSim/spatial_map_120h.csv",
             "../../delft/delft-DARTS/spatial_map_120h.csv",
             "../../lanl/spatial_map_120h.csv",
             "../../melbourne/spatial_map_120h.csv",
             "../../stanford/spatial_maps/spatial_map_120h.csv",
             "../../stuttgart/spatial_map_120h.csv"]
groups = ["austin", "csiro", "darsim", "darts", "lanl", "melbourne", "stanford", "stuttgart"]
numGroups = len(groups)

experimentalData = np.loadtxt("../../experiment/benchmarkdata/spatial_maps/run2/segmentation_120h.csv", dtype="int", delimiter=",")
# skip the first 30 rows as they are not contained in the modeling results
experimentalData = experimentalData[30:, :]

for fileName, group in zip(fileNames, groups):
    print(f"Processing {fileName}.")

    modelResult = seg.generateSegmentMap(fileName, 0.0, 2.86, 0.0, 1.23, 1e-2, 1e-1)

    seg.generateImages(modelResult, experimentalData, f"{group}_run2_120h", onlyModCont=True)

# create empty image as a substitute for the Heriot-Watt result
subprocess.run(["convert", "-size", "560x240", "xc:white", "heriot_watt_run2_120h_mod_cont.png"])

subprocess.run(["montage", "-tile", "3x3", "-geometry", "560x240+5+5", "*_run2_120h_mod_cont.png", "temp.png"])
subprocess.run(["convert", "temp.png", "-font", "helvetica-bold", "-fill", "yellow", "-pointsize", "48",
                "-stroke", "black",
                "-annotate", "+10+45", "Austin", "-annotate", "+580+45", "CSIRO", "-annotate",
                "+1150+45", "Delft-DARSim", "-annotate", "+10+295", "Delft-DARTS", "-annotate", "+1150+295", "LANL", "-annotate", "+10+545", "Melbourne",
                "-annotate", "+580+545", "Stanford", "-annotate", "+1150+545", "Stuttgart", f"compare_segmentation_120h.png"])
subprocess.run(["rm", "austin_run2_120h_mod_cont.png", "csiro_run2_120h_mod_cont.png", "darsim_run2_120h_mod_cont.png",
                "darts_run2_120h_mod_cont.png", "heriot_watt_run2_120h_mod_cont.png", "lanl_run2_120h_mod_cont.png",
                "melbourne_run2_120h_mod_cont.png", "stanford_run2_120h_mod_cont.png", "stuttgart_run2_120h_mod_cont.png",
                "temp.png"])
print("Generated compare_segmentation_120h.png.")
