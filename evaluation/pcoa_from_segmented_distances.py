import numpy as np
import skbio
import matplotlib.pyplot as plt


groups = ["Austin", "CSIRO", "Delft-DARSim", "Delft-DARTS", "LANL", "Melbourne", "Stanford", "Stuttgart"]
colors = ["C0", "C1", "C2", "C3", "C6", "C7", "C8", "C9"]

numGroups = len(groups)
numExps = 5
numGroupsPlusExps = numGroups + numExps

distances = np.loadtxt("segmented_distances.csv", delimiter=",")

pcoa = skbio.stats.ordination.pcoa(distances)

# scatter plot for the first four points in time
for i in range(4):
    plt.scatter(pcoa.samples['PC1'][i*numGroupsPlusExps:i*numGroupsPlusExps+numGroups],  pcoa.samples['PC2'][i*numGroupsPlusExps:i*numGroupsPlusExps+numGroups], s=96, c=colors, alpha=0.2*(i+1))
    plt.scatter(pcoa.samples['PC1'][i*numGroupsPlusExps+numGroups],  pcoa.samples['PC2'][i*numGroupsPlusExps+numGroups], s=96, c='k', marker='d', alpha=0.2*(i+1))
    plt.scatter(pcoa.samples['PC1'][i*numGroupsPlusExps+numGroups+1],  pcoa.samples['PC2'][i*numGroupsPlusExps+numGroups+1], s=96, c='k', marker='^', alpha=0.2*(i+1))
    plt.scatter(pcoa.samples['PC1'][i*numGroupsPlusExps+numGroups+2],  pcoa.samples['PC2'][i*numGroupsPlusExps+numGroups+2], s=96, c='k', marker='>', alpha=0.2*(i+1))
    plt.scatter(pcoa.samples['PC1'][i*numGroupsPlusExps+numGroups+3],  pcoa.samples['PC2'][i*numGroupsPlusExps+numGroups+3], s=96, c='k', marker='v', alpha=0.2*(i+1))
    plt.scatter(pcoa.samples['PC1'][i*numGroupsPlusExps+numGroups+4],  pcoa.samples['PC2'][i*numGroupsPlusExps+numGroups+4], s=96, c='k', marker='<', alpha=0.2*(i+1))

# treat the last one in a special way to add labels for the legend
for i in range(numGroups):
    plt.scatter(pcoa.samples['PC1'][4*numGroupsPlusExps+i],  pcoa.samples['PC2'][4*numGroupsPlusExps+i], s=96, c=colors[i], label=groups[i])
plt.scatter(pcoa.samples['PC1'][4*numGroupsPlusExps+numGroups],  pcoa.samples['PC2'][4*numGroupsPlusExps+numGroups], s=96, c='k', marker='d', label='run 1')
plt.scatter(pcoa.samples['PC1'][4*numGroupsPlusExps+numGroups+1],  pcoa.samples['PC2'][4*numGroupsPlusExps+numGroups+1], s=96, c='k', marker='^', label='run 2')
plt.scatter(pcoa.samples['PC1'][4*numGroupsPlusExps+numGroups+2],  pcoa.samples['PC2'][4*numGroupsPlusExps+numGroups+2], s=96, c='k', marker='>', label='run 3')
plt.scatter(pcoa.samples['PC1'][4*numGroupsPlusExps+numGroups+3],  pcoa.samples['PC2'][4*numGroupsPlusExps+numGroups+3], s=96, c='k', marker='v', label='run 4')
plt.scatter(pcoa.samples['PC1'][4*numGroupsPlusExps+numGroups+4],  pcoa.samples['PC2'][4*numGroupsPlusExps+numGroups+4], s=96, c='k', marker='<', label='run 5')

plt.tick_params(axis='both', which='both', bottom=False, left=False, labelbottom=False, labelleft=False)
plt.legend()
plt.savefig("pcoa_segmented_individual.png", bbox_inches='tight')
plt.clf()

accumulated = np.zeros((numGroupsPlusExps, numGroupsPlusExps))
for block in range(5):
    accumulated += np.square(distances[block*numGroupsPlusExps:(block+1)*numGroupsPlusExps, block*numGroupsPlusExps:(block+1)*numGroupsPlusExps])
accumulated = np.sqrt(accumulated)

pcoa = skbio.stats.ordination.pcoa(accumulated)

for i in range(numGroups):
    plt.scatter(pcoa.samples['PC1'][i],  pcoa.samples['PC2'][i], s=96, c=colors[i], label=groups[i])
plt.scatter(pcoa.samples['PC1'][numGroups],  pcoa.samples['PC2'][numGroups], s=96, c='k', marker='d', label='exp. run 1')
plt.scatter(pcoa.samples['PC1'][numGroups+1],  pcoa.samples['PC2'][numGroups+1], s=96, c='k', marker='^', label='exp. run 2')
plt.scatter(pcoa.samples['PC1'][numGroups+2],  pcoa.samples['PC2'][numGroups+2], s=96, c='k', marker='>', label='exp. run 3')
plt.scatter(pcoa.samples['PC1'][numGroups+3],  pcoa.samples['PC2'][numGroups+3], s=96, c='k', marker='v', label='exp. run 4')
plt.scatter(pcoa.samples['PC1'][numGroups+4],  pcoa.samples['PC2'][numGroups+4], s=96, c='k', marker='<', label='exp. run 5')

plt.tick_params(axis='both', which='both', bottom=False, left=False, labelbottom=False, labelleft=False)
plt.legend()
plt.savefig("pcoa_segmented_accumulated.png", bbox_inches='tight')

fig, axs = plt.subplots(1, 5, figsize=(15, 3))
pcoa = skbio.stats.ordination.pcoa(distances[:numGroupsPlusExps, :numGroupsPlusExps])

for i in range(numGroups):
    axs[0].scatter(pcoa.samples['PC1'][i],  pcoa.samples['PC2'][i], s=96, c=colors[i], label=groups[i])
axs[0].scatter(pcoa.samples['PC1'][numGroups],  pcoa.samples['PC2'][numGroups], s=96, c='k', marker='d', label='exp. run 1')
axs[0].scatter(pcoa.samples['PC1'][numGroups+1],  pcoa.samples['PC2'][numGroups+1], s=96, c='k', marker='^', label='exp. run 2')
axs[0].scatter(pcoa.samples['PC1'][numGroups+2],  pcoa.samples['PC2'][numGroups+2], s=96, c='k', marker='>', label='exp. run 3')
axs[0].scatter(pcoa.samples['PC1'][numGroups+3],  pcoa.samples['PC2'][numGroups+3], s=96, c='k', marker='v', label='exp. run 4')
axs[0].scatter(pcoa.samples['PC1'][numGroups+4],  pcoa.samples['PC2'][numGroups+4], s=96, c='k', marker='<', label='exp. run 5')
axs[0].tick_params(axis='both', which='both', bottom=False, left=False, labelbottom=False, labelleft=False)
axs[0].set_title('24 h')

for block in range(1, 5):
    pcoa = skbio.stats.ordination.pcoa(distances[block*numGroupsPlusExps:(block+1)*numGroupsPlusExps, block*numGroupsPlusExps:(block+1)*numGroupsPlusExps])

    for i in range(numGroups):
        axs[block].scatter(pcoa.samples['PC1'][i],  pcoa.samples['PC2'][i], s=96, c=colors[i])
    axs[block].scatter(pcoa.samples['PC1'][numGroups],  pcoa.samples['PC2'][numGroups], s=96, c='k', marker='d')
    axs[block].scatter(pcoa.samples['PC1'][numGroups+1],  pcoa.samples['PC2'][numGroups+1], s=96, c='k', marker='^')
    axs[block].scatter(pcoa.samples['PC1'][numGroups+2],  pcoa.samples['PC2'][numGroups+2], s=96, c='k', marker='>')
    axs[block].scatter(pcoa.samples['PC1'][numGroups+3],  pcoa.samples['PC2'][numGroups+3], s=96, c='k', marker='v')
    axs[block].scatter(pcoa.samples['PC1'][numGroups+4],  pcoa.samples['PC2'][numGroups+4], s=96, c='k', marker='<')
    axs[block].tick_params(axis='both', which='both', bottom=False, left=False, labelbottom=False, labelleft=False)
    axs[block].set_title(f'{24*(block+1)} h')

fig.legend()
fig.savefig(f"pcoa_segmented_snapshots.png", bbox_inches='tight')
