import numpy as np
import matplotlib.pyplot as plt
import matplotlib

font = {'family' : 'normal',
        'weight' : 'normal',
        'size' : 12}
matplotlib.rc('font', **font)
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "monospace",
    "legend.columnspacing": 1.5,
    "legend.handlelength": 1.0
})

groups = ["Austin", "CSIRO", "Delft-DARSim", "Delft-DARTS", "Heriot-Watt", "LANL", "Melbourne", "Stanford", "Stuttgart"]
colors = ["C0", "C1", "C2", "C3", "C4", "C6", "C7", "C8", "C9"]

numGroups = len(groups)
numExps = 5
numGroupsPlusExps = numGroups + numExps

distances = np.loadtxt("segmented_distances.csv", delimiter=",")

fig, axs = plt.subplots(2, 3, figsize=(9, 6))

# The calculated distances have the unit of normalized mass times meter.
# Multiply by 8.5, the injected mass of CO2 in g, and 100, to convert to g.cm.
A = 850*distances[:numGroupsPlusExps, :numGroupsPlusExps]
# set LANL distances to zero
A[5, :] = 0
A[:, 5] = 0

meanA_exp = np.mean(A[numGroups:, :], axis=0) 
meanA_fore = np.mean(A[:numGroups, :], axis=0)*9/8  # take correct avg due to missing LANL data

for i in range(numGroups):
    if i == 5:
        continue
    axs[0][0].scatter(meanA_exp[i],  meanA_fore[i], s=96, c=colors[i], label=groups[i])
axs[0][0].scatter(meanA_exp[numGroups],  meanA_fore[numGroups], s=96, c='k', marker='d', label=r'\textrm{exp. run 1}')
axs[0][0].scatter(meanA_exp[numGroups+1],  meanA_fore[numGroups+1], s=96, c='k', marker='^', label=r'\textrm{exp. run 2}')
axs[0][0].scatter(meanA_exp[numGroups+2],  meanA_fore[numGroups+2], s=96, c='k', marker='>', label=r'\textrm{exp. run 3}')
axs[0][0].scatter(meanA_exp[numGroups+3],  meanA_fore[numGroups+3], s=96, c='k', marker='v', label=r'\textrm{exp. run 4}')
axs[0][0].scatter(meanA_exp[numGroups+4],  meanA_fore[numGroups+4], s=96, c='k', marker='<', label=r'\textrm{exp. run 5}')
axs[0][0].set_title(r'\textrm{\textbf{24 h}}')
axs[0][0].set_xlim((0, 320))
axs[0][0].set_ylim((60, 270))


for k, hour, ki, kj in zip(range(1, 5), [48, 72, 96, 120], [0, 0, 1, 1], [1, 2, 0, 1]):
    A = 850*distances[k*numGroupsPlusExps:(k+1)*numGroupsPlusExps, k*numGroupsPlusExps:(k+1)*numGroupsPlusExps]
    # set LANL distances to zero
    A[5, :] = 0
    A[:, 5] = 0

    meanA_exp = np.mean(A[numGroups:, :], axis=0) 
    if hour > 48:
        meanA_fore = np.mean(A[:numGroups, :], axis=0)*9/7 # take correct avg due to missing LANL and HW data
    else:
        meanA_fore = np.mean(A[:numGroups, :], axis=0)*9/8 # take correct avg due to missing LANL data

    for i in range(numGroups):
        if i == 5 or (i == 4 and hour > 48):
            continue
        axs[ki][kj].scatter(meanA_exp[i],  meanA_fore[i], s=96, c=colors[i])
    axs[ki][kj].scatter(meanA_exp[numGroups],  meanA_fore[numGroups], s=96, c='k', marker='d')
    axs[ki][kj].scatter(meanA_exp[numGroups+1],  meanA_fore[numGroups+1], s=96, c='k', marker='^')
    axs[ki][kj].scatter(meanA_exp[numGroups+2],  meanA_fore[numGroups+2], s=96, c='k', marker='>')
    axs[ki][kj].scatter(meanA_exp[numGroups+3],  meanA_fore[numGroups+3], s=96, c='k', marker='v')
    axs[ki][kj].scatter(meanA_exp[numGroups+4],  meanA_fore[numGroups+4], s=96, c='k', marker='<')
    if hour == 48:
        axs[ki][kj].set_title(r'\textrm{\textbf{48 h}}')
    if hour == 72:
        axs[ki][kj].set_title(r'\textrm{\textbf{72 h}}')
    if hour == 96:
        axs[ki][kj].set_title(r'\textrm{\textbf{96 h}}')
    if hour == 120:
        axs[ki][kj].set_title(r'\textrm{\textbf{120 h}}')
    axs[ki][kj].set_xlim((0, 320))
    axs[ki][kj].set_ylim((60, 270))

axs[0][0].tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
axs[0][1].tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
axs[0][1].tick_params(axis='y', which='both', left=False, right=False, labelleft=False)
axs[0][2].tick_params(axis='y', which='both', left=False, right=True, labelleft=False, labelright=True)
axs[1][1].tick_params(axis='y', which='both', left=False, right=True, labelleft=False, labelright=True)
axs[1][2].set_axis_off()
axs[1][0].set_xlabel(r'\textrm{dist. to experiments [gr.cm]}')
axs[1][1].set_xlabel(r'\textrm{dist. to experiments [gr.cm]}')
axs[0][2].set_xlabel(r'\textrm{dist. to experiments [gr.cm]}')
axs[0][0].set_ylabel(r'\textrm{dist. to forecasts [gr.cm]}')
axs[1][0].set_ylabel(r'\textrm{dist. to forecasts [gr.cm]}')

fig.legend(loc='lower right', bbox_to_anchor=(1.0, 0.1), ncol=2)

fig.savefig(f"means_segmented_snapshots.pdf", bbox_inches='tight')

for k, hour, ki, kj in zip(range(0, 5), [24, 48, 72, 96, 120], [0, 0, 0, 1, 1], [0, 1, 2, 0, 1]):
    axs[ki][kj].set_xlim((0, 120))
    axs[ki][kj].set_xticks([0, 20, 40, 60, 80, 100, 120])
    axs[ki][kj].set_ylim((70, 180))

fig.savefig(f"means_segmented_snapshots_zoom.pdf", bbox_inches='tight')
