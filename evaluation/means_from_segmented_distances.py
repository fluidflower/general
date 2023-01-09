import numpy as np
import matplotlib.pyplot as plt


groups = ["Austin", "CSIRO", "Delft-DARSim", "Delft-DARTS", "LANL", "Melbourne", "Stanford", "Stuttgart"]
colors = ["C0", "C1", "C2", "C3", "C6", "C7", "C8", "C9"]

numGroups = len(groups)
numExps = 5
numGroupsPlusExps = numGroups + numExps

distances = np.loadtxt("segmented_distances.csv", delimiter=",")

fig, axs = plt.subplots(2, 3, figsize=(9, 6))

# The calculated distances have the unit of normalized mass times meter.
# Multiply by 8.5, the injected mass of CO2 in g, and 100, to convert to g.cm.
A = 850*distances[:13, :13]

meanA_exp = np.mean(A[8:, :], axis=0) 
meanA_fore = np.mean(A[:8, :], axis=0) 

for i in range(numGroups):
    axs[0][0].scatter(meanA_exp[i],  meanA_fore[i], s=96, c=colors[i], label=groups[i])
axs[0][0].scatter(meanA_exp[8],  meanA_fore[8], s=96, c='k', marker='d', label='exp. run 1')
axs[0][0].scatter(meanA_exp[9],  meanA_fore[9], s=96, c='k', marker='^', label='exp. run 2')
axs[0][0].scatter(meanA_exp[10],  meanA_fore[10], s=96, c='k', marker='>', label='exp. run 3')
axs[0][0].scatter(meanA_exp[11],  meanA_fore[11], s=96, c='k', marker='v', label='exp. run 4')
axs[0][0].scatter(meanA_exp[12],  meanA_fore[12], s=96, c='k', marker='<', label='exp. run 5')
axs[0][0].set_title('24 h')
axs[0][0].set_xlim((-0.05*850, 0.65*850))
axs[0][0].set_ylim((0.1*850, 0.6*850))


for k, hour, ki, kj in zip(range(1, 5), [48, 72, 96, 120], [0, 0, 1, 1], [1, 2, 0, 1]):
    A = 850*distances[k*numGroupsPlusExps:(k+1)*numGroupsPlusExps, k*numGroupsPlusExps:(k+1)*numGroupsPlusExps]

    meanA_exp = np.mean(A[8:, :], axis=0) 
    meanA_fore = np.mean(A[:8, :], axis=0) 

    for i in range(numGroups):
        axs[ki][kj].scatter(meanA_exp[i],  meanA_fore[i], s=96, c=colors[i])
    axs[ki][kj].scatter(meanA_exp[8],  meanA_fore[8], s=96, c='k', marker='d')
    axs[ki][kj].scatter(meanA_exp[9],  meanA_fore[9], s=96, c='k', marker='^')
    axs[ki][kj].scatter(meanA_exp[10],  meanA_fore[10], s=96, c='k', marker='>')
    axs[ki][kj].scatter(meanA_exp[11],  meanA_fore[11], s=96, c='k', marker='v')
    axs[ki][kj].scatter(meanA_exp[12],  meanA_fore[12], s=96, c='k', marker='<')
    axs[ki][kj].set_title(f'{hour} h')
    axs[ki][kj].set_xlim((-0.05*850, 0.65*850))
    axs[ki][kj].set_ylim((0.1*850, 0.6*850))

axs[0][0].tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
axs[0][1].tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
axs[0][1].tick_params(axis='y', which='both', left=False, right=False, labelleft=False)
axs[0][2].tick_params(axis='y', which='both', left=False, right=True, labelleft=False, labelright=True)
axs[1][1].tick_params(axis='y', which='both', left=False, right=True, labelleft=False, labelright=True)
axs[1][2].set_axis_off()
axs[1][0].set_xlabel('dist. to experiments [gr.cm]')
axs[1][1].set_xlabel('dist. to experiments [gr.cm]')
axs[0][2].set_xlabel('dist. to experiments [gr.cm]')
axs[0][0].set_ylabel('dist. to forecasts [gr.cm]')
axs[1][0].set_ylabel('dist. to forecasts [gr.cm]')

fig.legend(loc='lower right', bbox_to_anchor=(1.0, 0.1), ncol=2)

fig.savefig(f"means_segmented_snapshots.png", bbox_inches='tight')

for k, hour, ki, kj in zip(range(0, 5), [24, 48, 72, 96, 120], [0, 0, 0, 1, 1], [0, 1, 2, 0, 1]):
    axs[ki][kj].set_xlim((-10, 150))
    axs[ki][kj].set_ylim((100, 200))

fig.savefig(f"means_segmented_snapshots_zoom.png", bbox_inches='tight')
