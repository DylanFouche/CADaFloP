#!/usr/bin/env python3

# D FOUCHE
# UCT CS HONS
# fchdyl001@myuct.ac.za

import sys
import numpy as np
import matplotlib.pyplot as plt

xs = [str(n) for n in range(1,21)]

means = []

with open(sys.argv[1], "r") as f:
    for line in f:
        if line[0:5] == "Mean:":
            means.append(float(line[6:].rstrip()))

carta_histo_disk = means[0:20]
carta_stats_disk = means[20:40]
dask_local_histo_disk = means[40:60]
dask_local_stats_disk = means[60:80]
dask_distributed_histo_disk = means[80:100]
dask_distributed_stats_disk = means[100:120]

means = []

with open(sys.argv[2], "r") as f:
    for line in f:
        if line[0:5] == "Mean:":
            means.append(float(line[6:].rstrip()))

carta_histo_ram = means[0:20]
carta_stats_ram = means[20:40]
dask_local_histo_ram = means[40:60]
dask_local_stats_ram = means[60:80]
dask_distributed_histo_ram = means[80:100]
dask_distributed_stats_ram = means[100:120]

fig, axs = plt.subplots(2,2)

fig.suptitle('CADaFloP Performance Test Results')

x = np.arange(len(xs))
width = 0.25

axs[0,0].bar(x - width, carta_histo_disk, width, label='CARTA')
axs[0,0].bar(x, dask_local_histo_disk, width, label='Dask (local)')
axs[0,0].bar(x + width, dask_distributed_histo_disk, width, label='Dask (distributed)')
axs[0,0].set_xticks(x)
axs[0,0].set_xticklabels(xs)
axs[0,0].legend()
axs[0,0].set_title("(a) region histogram computation (from disk)")

axs[0,1].bar(x - width, carta_histo_ram, width, label='CARTA')
axs[0,1].bar(x, dask_local_histo_ram, width, label='Dask (local)')
axs[0,1].bar(x + width, dask_distributed_histo_ram, width, label='Dask (distributed)')
axs[0,1].set_xticks(x)
axs[0,1].set_xticklabels(xs)
axs[0,1].legend()
axs[0,1].set_title("(b) region histogram computation (from memory)")

axs[1,0].bar(x - width, carta_stats_disk, width, label='CARTA')
axs[1,0].bar(x, dask_local_stats_disk, width, label='Dask (local)')
axs[1,0].bar(x + width, dask_distributed_stats_disk, width, label='Dask (distributed)')
axs[1,0].set_xticks(x)
axs[1,0].set_xticklabels(xs)
axs[1,0].legend()
axs[1,0].set_title("(c) region statistics computation (from disk)")

axs[1,1].bar(x - width, carta_stats_ram, width, label='CARTA')
axs[1,1].bar(x, dask_local_stats_ram, width, label='Dask (local)')
axs[1,1].bar(x + width, dask_distributed_stats_ram, width, label='Dask (distributed)')
axs[1,1].set_xticks(x)
axs[1,1].set_xticklabels(xs)
axs[1,1].legend()
axs[1,1].set_title("(d) region statistics computation (from memory)")

for ax in axs.flat:
    ax.set(xlabel="Image size (1000n X 1000n pixels)", ylabel="Time (s)")

plt.show()
