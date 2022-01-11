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
    cmd = ["convert", inFile, "-crop", w+"x"+h+"+"+x+"+"+y, "+repage", outFile]
    subprocess.Popen(cmd)

def assembleSpatialMaps():
    cropImage('../../austin/figures/spatial_map_saturation.png', 0, 989, 0, 258, 'austin_sat_24.png')
    cropImage('../../csiro/figures/spatial_map_saturation.png', 0, 989, 0, 258, 'csiro_sat_24.png')
    cropImage('../../delft/figures/spatial_map_saturation.png', 0, 989, 0, 258, 'delft_sat_24.png')
    cropImage('../../herriot-watt/figures/20220105-HighCapDiffspatial_map_saturation.png', 0, 989, 0, 258, 'herriot-watt_sat_24.png')
    cropImage('../../lanl/figures/spatial_map_saturation.png', 0, 989, 0, 258, 'lanl_sat_24.png')
    cropImage('../../stanford/figures/spatial_map_saturation.png', 0, 989, 0, 258, 'stanford_sat_24.png')
    cropImage('../../stuttgart/figures/spatial_map_saturation.png', 0, 989, 0, 258, 'stuttgart_sat_24.png')

if __name__ == "__main__":
    assembleSpatialMaps()
