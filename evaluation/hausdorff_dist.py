import cv2
import numpy as np
from matplotlib import pyplot as plt
from generate_contours import generateContourLine
from scipy.spatial.distance import directed_hausdorff
from PIL import Image, ImageDraw, ImageFont
from os.path import exists

groups = ['Austin', 'CSIRO', 'Delft-\nDARSim', 'Delft-\nDARTS',
          'Heriot-\nWatt', 'LANL', 'Melbourne', 'MIT', 'Stanford', 'Stuttgart']
figurepaths = ['../../austin/figures/austin_contour_',
         '../../csiro/figures/csiro_contour_',
         '../../delft/delft-DARSim/figures/delft_darsim_contour_',
         '../../delft/delft-DARTS/figures/delft_darts_contour_',
         '../../herriot-watt/figures/heriot_watt_contour_',
         '../../lanl/figures/lanl_contour_',
         '../../melbourne/Figures/melbourne_contour_',
         '../../mit/figures/mit_contour_',
         '../../stanford/figures/stanford_contour_',
         '../../stuttgart/figures/stuttgart_contour_']
mappaths = ['../../austin/spatial_maps',
         '../../csiro',
         '../../delft/delft-DARSim',
         '../../delft/delft-DARTS',
         '../../herriot-watt',
         '../../lanl',
         '../../melbourne',
         '../../mit',
         '../../stanford/spatial_maps',
         '../../stuttgart']
numGroups = np.size(groups)

for hours in [24, 48, 72, 96, 120]:
    contours = {}

    for path, group, figurebase in zip(mappaths, groups, figurepaths):
        xMin = 0.0
        xMax = 2.86
        yMin = 0.0
        yMax = 1.23
        if group == 'Heriot-\nWatt':
            xMin = 0.03
            xMax = 2.83
            yMin = 0.03

        inFileName = f'{path}/spatial_map_{hours}h.csv'
        outFileName = f'{figurebase}{hours}h.png'
        if hours > 48 and group == 'Heriot-\nWatt':
            contours[group] = [[0.0, 0.0]]
        else:
            contours[group] = np.column_stack(generateContourLine(xMin, xMax, yMin, yMax, inFileName, outFileName))

    hausdorff_dist = np.empty([numGroups, numGroups])

    for i, groupI in zip(range(numGroups), groups):
        for j, groupJ in zip(range(numGroups), groups):
            hausdorff_dist[i][j] = max(directed_hausdorff(contours[groupI], contours[groupJ])[0],
                                    directed_hausdorff(contours[groupJ], contours[groupI])[0])

    print(hausdorff_dist)

    im = Image.open('../../austin/figures/austin_contour_24h.png', 'r')
    pixelsX, pixelsY = im.size
    combinedIm = Image.new('RGB', ((numGroups+1)*pixelsX, (numGroups+1)*pixelsY), color='white')
    draw = ImageDraw.Draw(im=combinedIm)
    fnt = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 100)

    for i, group, figurebase in zip(range(1, numGroups+1), groups, figurepaths):
        startX, startY = i*pixelsX, i*pixelsY

        if exists(f'{figurebase}{hours}h.png'):
            im = Image.open(f'{figurebase}{hours}h.png', 'r')
            combinedIm.paste(im, (startX, startY))

        draw.line([(startX, 0), (startX, (numGroups+1)*pixelsY)], fill='black', width=1)
        draw.line([(0, startY), ((numGroups+1)*pixelsX, startY)], fill='black', width=1)
        draw.text(xy=((i + 0.5)*pixelsX, 0.5*pixelsY),
                text=f'{group}',
                font=fnt, fill='black', anchor='mm')
        draw.text(xy=(0.5*pixelsX, (i+0.5)*pixelsY),
                text=f'{group}',
                font=fnt, fill='black', anchor='mm')

        for j in range(1, numGroups+1):
            if i != j and (hours < 72 or group != 'Heriot-\nWatt') and (hours < 72 or j != 5):
                if hausdorff_dist[i-1][j-1] == max(hausdorff_dist[i-1]) or (hours > 48 and hausdorff_dist[i-1][j-1] == sorted(set(hausdorff_dist[i-1]))[-2]):
                    draw.text(xy=((j + 0.5)*pixelsX, startY + 0.5*pixelsY),
                            text='{:.1e}'.format(hausdorff_dist[i-1][j-1]),
                            font=fnt, fill='red', anchor='mm')
                elif hausdorff_dist[i-1][j-1] == sorted(set(hausdorff_dist[i-1]))[1]:
                    draw.text(xy=((j + 0.5)*pixelsX, startY + 0.5*pixelsY),
                            text='{:.1e}'.format(hausdorff_dist[i-1][j-1]),
                            font=fnt, fill='blue', anchor='mm')
                else:
                    draw.text(xy=((j + 0.5)*pixelsX, startY + 0.5*pixelsY),
                            text='{:.1e}'.format(hausdorff_dist[i-1][j-1]),
                            font=fnt, fill='black', anchor='mm')

    combinedIm.save(f'hausdorff_distances_{hours}h.png', format='png')
