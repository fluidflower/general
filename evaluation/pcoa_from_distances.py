import numpy as np
import skbio
import matplotlib.pyplot as plt


groups = ["Austin", "CSIRO", "Delft-DARSim", "Delft-DARTS", "LANL", "Melbourne", "Stanford", "Stuttgart"]
colors = ["C0", "C1", "C2", "C3", "C6", "C7", "C8", "C9"]

numGroups = len(groups)

distances = np.loadtxt("distances.csv", delimiter=",")

pcoa = skbio.stats.ordination.pcoa(distances)

# scatter plot for the first four points in time
for i in range(4):
  plt.scatter(pcoa.samples['PC1'][i*numGroups:(i+1)*numGroups],  pcoa.samples['PC2'][i*numGroups:(i+1)*numGroups], s=96, c=colors, alpha=0.2*(i+1))

# treat the last one in a special way to add labels for the legend
for i in range(numGroups):
  plt.scatter(pcoa.samples['PC1'][4*numGroups+i],  pcoa.samples['PC2'][4*numGroups+i], s=96, c=colors[i], label=groups[i])

plt.tick_params(axis='both', which='both', bottom=False, left=False, labelbottom=False, labelleft=False)
plt.legend()
plt.savefig("pcoa_individual.png")
plt.clf()

accumulated = np.zeros((numGroups, numGroups))
for block in range(5):
  accumulated += np.square(distances[block*numGroups:(block+1)*numGroups, block*numGroups:(block+1)*numGroups])
accumulated = np.sqrt(accumulated)

pcoa = skbio.stats.ordination.pcoa(accumulated)

plt.scatter(pcoa.samples['PC1'],  pcoa.samples['PC2'], s=96, c=colors)

for i in range(numGroups):
  plt.text(pcoa.samples.loc[str(i), 'PC1'],  pcoa.samples.loc[str(i), 'PC2'], groups[i])

plt.tick_params(axis='both', which='both', bottom=False, left=False, labelbottom=False, labelleft=False)
plt.savefig("pcoa_accumulated.png")
