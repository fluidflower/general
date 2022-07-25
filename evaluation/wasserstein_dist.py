import cv2
import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import wasserstein_distance
from PIL import Image, ImageDraw, ImageFont
from os.path import exists

groups = ['Austin', 'CSIRO', 'Delft-\nDARSim', 'Delft-\nDARTS',
          'Heriot-\nWatt', 'LANL', 'Melbourne', 'MIT', 'Stanford', 'Stuttgart']
paths = ['../../austin/figures/austin_gray_',
         '../../csiro/figures/csiro_gray_',
         '../../delft/delft-DARSim/figures/delft_darsim_gray_',
         '../../delft/delft-DARTS/figures/delft_darts_gray_',
         '../../herriot-watt/figures/heriot_watt_gray_',
         '../../lanl/figures/lanl_gray_',
         '../../melbourne/Figures/melbourne_gray_',
         '../../mit/figures/mit_gray_',
         '../../stanford/figures/stanford_gray_',
         '../../stuttgart/figures/stuttgart_gray_']
numGroups = np.size(groups)

for hours in [24, 48, 72, 96, 120]:
    hst = {}

    for path, group in zip(paths, groups):
        if exists(f'{path}{hours}h.png'):
            img = cv2.imread(f'{path}{hours}h.png', cv2.IMREAD_GRAYSCALE)
            hst[group] = cv2.calcHist([img], [0], None, [256], [0,256])
            hst[group] = np.array(np.concatenate(hst[group]).flat)/(572*246)
        else:
            hst[group] = np.zeros(256)

        # plt.plot(hst[group], label=group)

    wass_dist = np.empty([numGroups, numGroups])

    for i, groupI in zip(range(numGroups), groups):
        for j, groupJ in zip(range(numGroups), groups):
            wass_dist[i][j] = wasserstein_distance(hst[groupI], hst[groupJ], np.arange(256), np.arange(256))

    print(wass_dist)

    im = Image.open('../../austin/figures/austin_gray_24h.png', 'r')
    pixelsX, pixelsY = im.size
    combinedIm = Image.new('RGB', ((numGroups+1)*pixelsX, (numGroups+1)*pixelsY), color='white')
    draw = ImageDraw.Draw(im=combinedIm)
    fnt = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 100)

    for i, group, figurebase in zip(range(1, numGroups+1), groups, paths):
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
                if wass_dist[i-1][j-1] == max(wass_dist[i-1]) or (hours > 48 and wass_dist[i-1][j-1] == sorted(set(wass_dist[i-1]))[-2]):
                    draw.text(xy=((j + 0.5)*pixelsX, startY + 0.5*pixelsY),
                            text='{:.1e}'.format(wass_dist[i-1][j-1]),
                            font=fnt, fill='red', anchor='mm')
                elif wass_dist[i-1][j-1] == sorted(set(wass_dist[i-1]))[1]:
                    draw.text(xy=((j + 0.5)*pixelsX, startY + 0.5*pixelsY),
                            text='{:.1e}'.format(wass_dist[i-1][j-1]),
                            font=fnt, fill='blue', anchor='mm')
                else:
                    draw.text(xy=((j + 0.5)*pixelsX, startY + 0.5*pixelsY),
                            text='{:.1e}'.format(wass_dist[i-1][j-1]),
                            font=fnt, fill='black', anchor='mm')

    combinedIm.save(f'weighted_wasserstein_distances_{hours}h.png', format='png')

# plt.gca().set_ylim(0, 0.01)
# plt.gca().legend(loc='center left', bbox_to_anchor=(1, 0.5))
# plt.title('Histograms for gray scale image')
# plt.show()

