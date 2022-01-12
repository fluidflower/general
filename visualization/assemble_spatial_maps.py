#!/usr/bin/env python3
import subprocess
import sys

def cropImage(inFile, left, right, top, bottom, outFile):
    # get the current img' size
    data = subprocess.check_output(["identify", inFile]).decode("utf-8").strip().replace(inFile, "")
    size = [int(n) for n in data.replace(inFile, "").split()[1].split("x")]
    # calculate the command to resize
    w = str(size[0] - left - right)
    h = str(size[1] - top - bottom)
    x = str(left)
    y = str(top)
    # execute the command
    subprocess.run(["convert", inFile, "-crop", w+"x"+h+"+"+x+"+"+y, "+repage", outFile])

def assembleSpatialMaps():
    for field in ["saturation", "concentration"]:
        cropImage(f'../../austin/figures/spatial_map_{field}.png', 0, 989, 0, 258, 'austin_24.png')
        cropImage(f'../../csiro/figures/spatial_map_{field}.png', 0, 989, 0, 258, 'csiro_24.png')
        cropImage(f'../../delft/figures/spatial_map_{field}.png', 0, 989, 0, 258, 'delft_24.png')
        cropImage(f'../../herriot-watt/figures/20220105-HighCapDiffspatial_map_{field}.png', 0, 989, 0, 258, 'herriot-watt_24.png')
        cropImage(f'../../lanl/figures/spatial_map_{field}.png', 0, 989, 0, 258, 'lanl_24.png')
        cropImage(f'../../stanford/figures/spatial_map_{field}.png', 0, 989, 0, 258, 'stanford_24.png')
        cropImage(f'../../stuttgart/figures/spatial_map_{field}.png', 0, 989, 0, 258, 'stuttgart_24.png')
        subprocess.run(["montage", "-tile", "3x3", "-geometry", "500", "*_24.png", "temp.png"])
        subprocess.run(["convert", "temp.png", "-font", "helvetica", "-fill", "white", "-pointsize", "24",
                        "-annotate", "+60+190", "Austin", "-annotate", "+560+190", "CSIRO", "-annotate",
                        "+1060+190", "Delft", "-annotate", "+60+415", "Herriot-Watt", "-annotate", "+560+415",
                        "LANL", "-annotate", "+1060+415", "Stanford", "-annotate", "+60+640", "Stuttgart", f"{field}_24h.png"])
        subprocess.run(["rm", "austin_24.png", "csiro_24.png", "delft_24.png", "herriot-watt_24.png",
                        "lanl_24.png", "stanford_24.png", "stuttgart_24.png", "temp.png"])

        cropImage(f'../../austin/figures/spatial_map_{field}.png', 500, 499, 0, 258, 'austin_48.png')
        cropImage(f'../../csiro/figures/spatial_map_{field}.png', 500, 499, 0, 258, 'csiro_48.png')
        cropImage(f'../../delft/figures/spatial_map_{field}.png', 500, 499, 0, 258, 'delft_48.png')
        cropImage(f'../../herriot-watt/figures/20220105-HighCapDiffspatial_map_{field}.png', 500, 499, 0, 258, 'herriot-watt_48.png')
        cropImage(f'../../lanl/figures/spatial_map_{field}.png', 500, 499, 0, 258, 'lanl_48.png')
        cropImage(f'../../stanford/figures/spatial_map_{field}.png', 500, 499, 0, 258, 'stanford_48.png')
        cropImage(f'../../stuttgart/figures/spatial_map_{field}.png', 500, 499, 0, 258, 'stuttgart_48.png')
        subprocess.run(["montage", "-tile", "3x3", "-geometry", "500", "*_48.png", "temp.png"])
        subprocess.run(["convert", "temp.png", "-font", "helvetica", "-fill", "white", "-pointsize", "24",
                        "-annotate", "+55+195", "Austin", "-annotate", "+550+195", "CSIRO", "-annotate",
                        "+1050+195", "Delft", "-annotate", "+55+425", "Herriot-Watt", "-annotate", "+550+425",
                        "LANL", "-annotate", "+1050+425", "Stanford", "-annotate", "+55+655", "Stuttgart", f"{field}_48h.png"])
        subprocess.run(["rm", "austin_48.png", "csiro_48.png", "delft_48.png", "herriot-watt_48.png",
                        "lanl_48.png", "stanford_48.png", "stuttgart_48.png", "temp.png"])

        cropImage(f'../../austin/figures/spatial_map_{field}.png', 994, 5, 0, 258, 'austin_72.png')
        cropImage(f'../../csiro/figures/spatial_map_{field}.png', 994, 5, 0, 258, 'csiro_72.png')
        cropImage(f'../../delft/figures/spatial_map_{field}.png', 994, 5, 0, 258, 'delft_72.png')
        cropImage(f'../../herriot-watt/figures/20220105-HighCapDiffspatial_map_{field}.png', 994, 5, 0, 258, 'herriot-watt_72.png')
        cropImage(f'../../lanl/figures/spatial_map_{field}.png', 994, 5, 0, 258, 'lanl_72.png')
        cropImage(f'../../stanford/figures/spatial_map_{field}.png', 994, 5, 0, 258, 'stanford_72.png')
        cropImage(f'../../stuttgart/figures/spatial_map_{field}.png', 994, 5, 0, 258, 'stuttgart_72.png')
        subprocess.run(["montage", "-tile", "3x3", "-geometry", "500", "*_72.png", "temp.png"])
        subprocess.run(["convert", "temp.png", "-font", "helvetica", "-fill", "white", "-pointsize", "24",
                        "-annotate", "+55+195", "Austin", "-annotate", "+550+195", "CSIRO", "-annotate",
                        "+1050+195", "Delft", "-annotate", "+55+425", "Herriot-Watt", "-annotate", "+550+425",
                        "LANL", "-annotate", "+1050+425", "Stanford", "-annotate", "+55+655", "Stuttgart", f"{field}_72h.png"])
        subprocess.run(["rm", "austin_72.png", "csiro_72.png", "delft_72.png", "herriot-watt_72.png",
                        "lanl_72.png", "stanford_72.png", "stuttgart_72.png", "temp.png"])

        cropImage(f'../../austin/figures/spatial_map_{field}.png', 7, 992, 254, 8, 'austin_96.png')
        cropImage(f'../../csiro/figures/spatial_map_{field}.png', 7, 992, 254, 8, 'csiro_96.png')
        cropImage(f'../../delft/figures/spatial_map_{field}.png', 7, 992, 254, 8, 'delft_96.png')
        cropImage(f'../../herriot-watt/figures/20220105-HighCapDiffspatial_map_{field}.png', 7, 992, 254, 8, 'herriot-watt_96.png')
        cropImage(f'../../lanl/figures/spatial_map_{field}.png', 7, 992, 254, 8, 'lanl_96.png')
        cropImage(f'../../stanford/figures/spatial_map_{field}.png', 7, 992, 254, 8, 'stanford_96.png')
        cropImage(f'../../stuttgart/figures/spatial_map_{field}.png', 7, 992, 254, 8, 'stuttgart_96.png')
        subprocess.run(["montage", "-tile", "3x3", "-geometry", "500", "*_96.png", "temp.png"])
        subprocess.run(["convert", "temp.png", "-font", "helvetica", "-fill", "white", "-pointsize", "24",
                        "-annotate", "+55+190", "Austin", "-annotate", "+550+190", "CSIRO", "-annotate",
                        "+1050+190", "Delft", "-annotate", "+55+415", "Herriot-Watt", "-annotate", "+550+415",
                        "LANL", "-annotate", "+1050+415", "Stanford", "-annotate", "+55+640", "Stuttgart", f"{field}_96h.png"])
        subprocess.run(["rm", "austin_96.png", "csiro_96.png", "delft_96.png", "herriot-watt_96.png",
                        "lanl_96.png", "stanford_96.png", "stuttgart_96.png", "temp.png"])

        cropImage(f'../../austin/figures/spatial_map_{field}.png', 500, 499, 254, 8, 'austin_120.png')
        cropImage(f'../../csiro/figures/spatial_map_{field}.png', 500, 499, 254, 8, 'csiro_120.png')
        cropImage(f'../../delft/figures/spatial_map_{field}.png', 500, 499, 254, 8, 'delft_120.png')
        cropImage(f'../../herriot-watt/figures/20220105-HighCapDiffspatial_map_{field}.png', 500, 499, 254, 8, 'herriot-watt_120.png')
        cropImage(f'../../lanl/figures/spatial_map_{field}.png', 500, 499, 254, 8, 'lanl_120.png')
        cropImage(f'../../stanford/figures/spatial_map_{field}.png', 500, 499, 254, 8, 'stanford_120.png')
        cropImage(f'../../stuttgart/figures/spatial_map_{field}.png', 500, 499, 254, 8, 'stuttgart_120.png')
        subprocess.run(["montage", "-tile", "3x3", "-geometry", "500", "*_120.png", "temp.png"])
        subprocess.run(["convert", "temp.png", "-font", "helvetica", "-fill", "white", "-pointsize", "24",
                        "-annotate", "+55+190", "Austin", "-annotate", "+550+190", "CSIRO", "-annotate",
                        "+1050+190", "Delft", "-annotate", "+55+415", "Herriot-Watt", "-annotate", "+550+415",
                        "LANL", "-annotate", "+1050+415", "Stanford", "-annotate", "+55+640", "Stuttgart", f"{field}_120h.png"])
        subprocess.run(["rm", "austin_120.png", "csiro_120.png", "delft_120.png", "herriot-watt_120.png",
                        "lanl_120.png", "stanford_120.png", "stuttgart_120.png", "temp.png"])

if __name__ == "__main__":
    assembleSpatialMaps()
