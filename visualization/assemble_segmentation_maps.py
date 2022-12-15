#!/usr/bin/env python3
import subprocess
import numpy as np
import generate_segmented_images as seg

fileNames = ["../../austin/spatial_maps/spatial_map_24h.csv",
             "../../csiro/spatial_map_24h.csv",
             "../../delft/delft-DARSim/spatial_map_24h.csv",
             "../../delft/delft-DARTS/spatial_map_24h.csv",
             "../../herriot-watt/spatial_map_24h.csv",
             "../../lanl/spatial_map_24h.csv",
             "../../melbourne/spatial_map_24h.csv",
             "../../stanford/spatial_maps/spatial_map_24h.csv",
             "../../stuttgart/spatial_map_24h.csv"]
groups = ["austin", "csiro", "darsim", "darts", "heriot_watt", "lanl", "melbourne", "stanford", "stuttgart"]
numGroups = len(groups)

experimentalData = np.loadtxt("../../experiment/benchmarkdata/spatial_maps/run2/segmentation_24h.csv", dtype="int", delimiter=",")
# skip the first 30 rows as they are not contained in the modeling results
experimentalData = experimentalData[30:, :]

for fileName, group in zip(fileNames, groups):
    print(f"Processing {fileName}.")
    if group != "heriot_watt":
        modelResult = seg.generateSegmentMap(fileName, 0.0, 2.86, 0.0, 1.23, 1e-2, 1e-1)
    else:
        modelResult = seg.generateSegmentMap(fileName, 0.03, 2.83, 0.03, 1.23, 1e-2, 1e-1)

    seg.generateImages(modelResult, experimentalData, f"{group}_run2_24h", onlyModCont=True)

subprocess.run(["montage", "-tile", "3x3", "-geometry", "560x240+5+5", "*_run2_24h_mod_cont.png", "temp.png"])
subprocess.run(["convert", "temp.png", "-font", "helvetica-bold", "-fill", "yellow", "-pointsize", "48",
                "-stroke", "black",
                "-annotate", "+10+45", "Austin", "-annotate", "+580+45", "CSIRO", "-annotate",
                "+1150+45", "Delft-DARSim", "-annotate", "+10+295", "Delft-DARTS", "-annotate", "+580+295",
                "Heriot-Watt", "-annotate", "+1150+295", "LANL", "-annotate", "+10+545", "Melbourne",
                "-annotate", "+580+545", "Stanford", "-annotate", "+1150+545", "Stuttgart", f"compare_segmentation_24h.png"])
subprocess.run(["rm", "austin_run2_24h_mod_cont.png", "csiro_run2_24h_mod_cont.png", "darsim_run2_24h_mod_cont.png",
                "darts_run2_24h_mod_cont.png", "heriot_watt_run2_24h_mod_cont.png", "lanl_run2_24h_mod_cont.png",
                "melbourne_run2_24h_mod_cont.png", "stanford_run2_24h_mod_cont.png", "stuttgart_run2_24h_mod_cont.png",
                "temp.png"])
print("Generated compare_segmentation_24h.png.")
