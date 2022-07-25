import cv2
import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import wasserstein_distance

groups = ['Austin', 'CSIRO', 'Delft-DARSim', 'Delft-DARTS',
          'Heriot-Watt', 'LANL', 'Melbourne', 'MIT', 'Stanford', 'Stuttgart']
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
hst = {}

for path, group in zip(paths, groups):
    img = cv2.imread(f'{path}24h.png', cv2.IMREAD_GRAYSCALE)
    hst[group] = cv2.calcHist([img], [0], None, [256], [0,256])
    hst[group] = np.array(np.concatenate(hst[group]).flat)/(572*246)
    print(hst[group])

    plt.plot(hst[group], label=group)

wass_dist = np.empty([10, 10])

for i, groupI in zip(range(10), groups):
    for j, groupJ in zip(range(10), groups):
        wass_dist[i][j] = wasserstein_distance(hst[groupI], hst[groupJ])

print(wass_dist)

plt.gca().set_ylim(0, 0.01)
plt.gca().legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.title('Histograms for gray scale image')
plt.show()

