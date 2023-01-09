import matplotlib.pyplot as plt

from scipy import interpolate
from operator import methodcaller

import numpy as np

f = []
minX = -np.inf
maxX = np.inf

data = np.genfromtxt("../../experiment/benchmarkdata/time_series/mobile_box_a.csv", delimiter=",", skip_header=1)

for run in range(5):
    dataRun = data[:, 2*run:2*run+2]
    dataRun = dataRun[~np.isnan(dataRun).any(axis=1)]

    f.append(interpolate.interp1d(dataRun[:, 0], dataRun[:, 1]))
    minX = max(minX, dataRun[0, 0])
    maxX = min(maxX, dataRun[-1, 0])

ls = np.linspace(minX, maxX, num=1000)
interpolateddata = list(map(methodcaller('__call__', ls), f))
meanvalues = np.mean(interpolateddata, axis=0)
std = np.std(interpolateddata, axis=0)

plt.plot(ls, meanvalues, color='k', linewidth=2)
plt.fill_between(ls, meanvalues-std, meanvalues+std, color="gray")
plt.show()

