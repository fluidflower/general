#!/usr/bin/env python3
import subprocess
import sys

def cropImage(inFile, w, h, x, y, outFile):
    subprocess.run(["convert", inFile, "-crop", str(w)+"x"+str(h)+"+"+str(x)+"+"+str(y), "+repage", outFile])

def assembleSpatialMaps():
    for field in ["saturation", "concentration"]:
        cropImage(f'../../austin/figures/spatial_map_{field}.png', 399, 180, 42, 24, 'austin_24.png')
        cropImage(f'../../csiro/figures/spatial_map_{field}.png', 399, 180, 42, 24, 'csiro_24.png')
        cropImage(f'../../delft/delft-DARSim/figures/spatial_map_{field}.png', 399, 180, 42, 24, 'delft_darsim_24.png')
        cropImage(f'../../delft/delft-DARTS/figures/spatial_map_{field}.png', 399, 180, 42, 24, 'delft_darts_24.png')
        cropImage(f'../../herriot-watt/figures/spatial_map_{field}.png', 399, 180, 42, 24, 'herriot-watt_24.png')
        cropImage(f'../../lanl/figures/spatial_map_{field}.png', 399, 180, 42, 24, 'lanl_24.png')
        cropImage(f'../../melbourne/Figures/spatial_map_{field}.png', 399, 180, 42, 24, 'melbourne_24.png')
        cropImage(f'../../stanford/figures/spatial_map_{field}.png', 399, 180, 42, 24, 'stanford_24.png')
        cropImage(f'../../stuttgart/figures/spatial_map_{field}.png', 399, 180, 42, 24, 'stuttgart_24.png')
        subprocess.run(["montage", "-tile", "3x3", "-geometry", "500", "*_24.png", "temp.png"])
        subprocess.run(["convert", "temp.png", "-font", "helvetica-bold", "-fill", "yellow", "-pointsize", "36",
                        "-stroke", "black",
                        "-annotate", "+15+40", "Austin", "-annotate", "+515+40", "CSIRO", "-annotate",
                        "+1015+40", "Delft-DARSim", "-annotate", "+15+265", "Delft-DARTS", "-annotate", "+515+265",
                        "Heriot-Watt", "-annotate", "+1015+265", "LANL", "-annotate", "+15+490", "Melbourne",
                        "-annotate", "+515+490", "Stanford", "-annotate", "+1015+490", "Stuttgart", f"{field}_24h.png"])
        subprocess.run(["rm", "austin_24.png", "csiro_24.png", "delft_darsim_24.png", "delft_darts_24.png", "herriot-watt_24.png",
                        "lanl_24.png", "melbourne_24.png", "stanford_24.png", "stuttgart_24.png", "temp.png"])

        cropImage(f'../../austin/figures/spatial_map_{field}.png', 399, 180, 534, 24, 'austin_48.png')
        cropImage(f'../../csiro/figures/spatial_map_{field}.png', 399, 180, 534, 24, 'csiro_48.png')
        cropImage(f'../../delft/delft-DARSim/figures/spatial_map_{field}.png', 399, 180, 534, 24, 'delft_darsim_48.png')
        cropImage(f'../../delft/delft-DARTS/figures/spatial_map_{field}.png', 399, 180, 534, 24, 'delft_darts_48.png')
        cropImage(f'../../herriot-watt/figures/spatial_map_{field}.png', 399, 180, 534, 24, 'herriot-watt_48.png')
        cropImage(f'../../lanl/figures/spatial_map_{field}.png', 399, 180, 534, 24, 'lanl_48.png')
        cropImage(f'../../melbourne/Figures/spatial_map_{field}.png', 399, 180, 534, 24, 'melbourne_48.png')
        cropImage(f'../../stanford/figures/spatial_map_{field}.png', 399, 180, 534, 24, 'stanford_48.png')
        cropImage(f'../../stuttgart/figures/spatial_map_{field}.png', 399, 180, 534, 24, 'stuttgart_48.png')
        subprocess.run(["montage", "-tile", "3x3", "-geometry", "500", "*_48.png", "temp.png"])
        subprocess.run(["convert", "temp.png", "-font", "helvetica-bold", "-fill", "yellow", "-pointsize", "36",
                        "-stroke", "black",
                        "-annotate", "+15+40", "Austin", "-annotate", "+515+40", "CSIRO", "-annotate",
                        "+1015+40", "Delft-DARSim", "-annotate", "+15+265", "Delft-DARTS", "-annotate", "+515+265",
                        "Heriot-Watt", "-annotate", "+1015+265", "LANL", "-annotate", "+15+490", "Melbourne",
                        "-annotate", "+515+490", "Stanford", "-annotate", "+1015+490", "Stuttgart", f"{field}_48h.png"])
        subprocess.run(["rm", "austin_48.png", "csiro_48.png", "delft_darsim_48.png", "delft_darts_48.png", "herriot-watt_48.png",
                        "lanl_48.png", "melbourne_48.png", "stanford_48.png", "stuttgart_48.png", "temp.png"])

        cropImage(f'../../austin/figures/spatial_map_{field}.png', 399, 180, 1026, 24, 'austin_72.png')
        cropImage(f'../../csiro/figures/spatial_map_{field}.png', 399, 180, 1026, 24, 'csiro_72.png')
        cropImage(f'../../delft/delft-DARSim/figures/spatial_map_{field}.png', 399, 180, 1026, 24, 'delft_darsim_72.png')
        cropImage(f'../../delft/delft-DARTS/figures/spatial_map_{field}.png', 399, 180, 1026, 24, 'delft_darts_72.png')
        subprocess.run(["convert", "-size", "399x180", "xc:transparent", "herriot-watt_72.png"])
        # cropImage(f'../../herriot-watt/figures/spatial_map_{field}.png', 399, 180, 1026, 24, 'herriot-watt_72.png')
        cropImage(f'../../lanl/figures/spatial_map_{field}.png', 399, 180, 1026, 24, 'lanl_72.png')
        cropImage(f'../../melbourne/Figures/spatial_map_{field}.png', 399, 180, 1026, 24, 'melbourne_72.png')
        cropImage(f'../../stanford/figures/spatial_map_{field}.png', 399, 180, 1026, 24, 'stanford_72.png')
        cropImage(f'../../stuttgart/figures/spatial_map_{field}.png', 399, 180, 1026, 24, 'stuttgart_72.png')
        subprocess.run(["montage", "-tile", "3x3", "-geometry", "500", "*_72.png", "temp.png"])
        subprocess.run(["convert", "temp.png", "-font", "helvetica-bold", "-fill", "yellow", "-pointsize", "36",
                        "-stroke", "black",
                        "-annotate", "+15+40", "Austin", "-annotate", "+515+40", "CSIRO", "-annotate",
                        "+1015+40", "Delft-DARSim", "-annotate", "+15+265", "Delft-DARTS", "-annotate", "+1015+265", "LANL", "-annotate", "+15+490", "Melbourne",
                        "-annotate", "+515+490", "Stanford", "-annotate", "+1015+490", "Stuttgart", f"{field}_72h.png"])
        subprocess.run(["rm", "austin_72.png", "csiro_72.png", "delft_darsim_72.png", "delft_darts_72.png", "herriot-watt_72.png",
                        "lanl_72.png", "melbourne_72.png", "stanford_72.png", "stuttgart_72.png", "temp.png"])

        cropImage(f'../../austin/figures/spatial_map_{field}.png', 399, 180, 42, 276, 'austin_96.png')
        cropImage(f'../../csiro/figures/spatial_map_{field}.png', 399, 180, 42, 276, 'csiro_96.png')
        cropImage(f'../../delft/delft-DARSim/figures/spatial_map_{field}.png', 399, 180, 42, 276, 'delft_darsim_96.png')
        cropImage(f'../../delft/delft-DARTS/figures/spatial_map_{field}.png', 399, 180, 42, 276, 'delft_darts_96.png')
        subprocess.run(["convert", "-size", "399x180", "xc:transparent", "herriot-watt_96.png"])
        # cropImage(f'../../herriot-watt/figures/spatial_map_{field}.png', 399, 180, 42, 276, 'herriot-watt_96.png')
        cropImage(f'../../lanl/figures/spatial_map_{field}.png', 399, 180, 42, 276, 'lanl_96.png')
        cropImage(f'../../melbourne/Figures/spatial_map_{field}.png', 399, 180, 42, 276, 'melbourne_96.png')
        cropImage(f'../../stanford/figures/spatial_map_{field}.png', 399, 180, 42, 276, 'stanford_96.png')
        cropImage(f'../../stuttgart/figures/spatial_map_{field}.png', 399, 180, 42, 276, 'stuttgart_96.png')
        subprocess.run(["montage", "-tile", "3x3", "-geometry", "500", "*_96.png", "temp.png"])
        subprocess.run(["convert", "temp.png", "-font", "helvetica-bold", "-fill", "yellow", "-pointsize", "36",
                        "-stroke", "black",
                        "-annotate", "+15+40", "Austin", "-annotate", "+515+40", "CSIRO", "-annotate",
                        "+1015+40", "Delft-DARSim", "-annotate", "+15+265", "Delft-DARTS", "-annotate", "+1015+265", "LANL", "-annotate", "+15+490", "Melbourne",
                        "-annotate", "+515+490", "Stanford", "-annotate", "+1015+490", "Stuttgart", f"{field}_96h.png"])
        subprocess.run(["rm", "austin_96.png", "csiro_96.png", "delft_darsim_96.png", "delft_darts_96.png", "herriot-watt_96.png",
                        "lanl_96.png", "melbourne_96.png", "stanford_96.png", "stuttgart_96.png", "temp.png"])

        cropImage(f'../../austin/figures/spatial_map_{field}.png', 399, 180, 534, 276, 'austin_120.png')
        cropImage(f'../../csiro/figures/spatial_map_{field}.png', 399, 180, 534, 276, 'csiro_120.png')
        cropImage(f'../../delft/delft-DARSim/figures/spatial_map_{field}.png', 399, 180, 534, 276, 'delft_darsim_120.png')
        cropImage(f'../../delft/delft-DARTS/figures/spatial_map_{field}.png', 399, 180, 534, 276, 'delft_darts_120.png')
        subprocess.run(["convert", "-size", "399x180", "xc:transparent", "herriot-watt_120.png"])
        # cropImage(f'../../herriot-watt/figures/spatial_map_{field}.png', 399, 180, 534, 276, 'herriot-watt_120.png')
        cropImage(f'../../lanl/figures/spatial_map_{field}.png', 399, 180, 534, 276, 'lanl_120.png')
        cropImage(f'../../melbourne/Figures/spatial_map_{field}.png', 399, 180, 534, 276, 'melbourne_120.png')
        cropImage(f'../../stanford/figures/spatial_map_{field}.png', 399, 180, 534, 276, 'stanford_120.png')
        cropImage(f'../../stuttgart/figures/spatial_map_{field}.png', 399, 180, 534, 276, 'stuttgart_120.png')
        subprocess.run(["montage", "-tile", "3x3", "-geometry", "500", "*_120.png", "temp.png"])
        subprocess.run(["convert", "temp.png", "-font", "helvetica-bold", "-fill", "yellow", "-pointsize", "36",
                        "-stroke", "black",
                        "-annotate", "+15+40", "Austin", "-annotate", "+515+40", "CSIRO", "-annotate",
                        "+1015+40", "Delft-DARSim", "-annotate", "+15+265", "Delft-DARTS", "-annotate", "+1015+265", "LANL", "-annotate", "+15+490", "Melbourne",
                        "-annotate", "+515+490", "Stanford", "-annotate", "+1015+490", "Stuttgart", f"{field}_120h.png"])
        subprocess.run(["rm", "austin_120.png", "csiro_120.png", "delft_darsim_120.png", "delft_darts_120.png", "herriot-watt_120.png",
                        "lanl_120.png", "melbourne_120.png", "stanford_120.png", "stuttgart_120.png", "temp.png"])

if __name__ == "__main__":
    assembleSpatialMaps()
