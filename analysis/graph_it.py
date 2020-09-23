#!/usr/bin/env python3

# D FOUCHE
# UCT CS HONS
# fchdyl001@myuct.ac.za

import sys
import numpy as np
import matplotlib.pyplot as plt

for file in sys.argv[1:]:

    xs = [str(n) for n in range(1000, 21000, 1000)]

    means = []

    with open(file, "r") as f:
        for line in f:
            if line[0:5] == "Mean:":
                means.append(float(line[6:].rstrip()))

    carta_histo = means[0:20]
    carta_stats = means[20:40]

    dask_local_histo = means[40:60]
    dask_local_stats = means[60:80]

    dask_distributed_histo = means[80:100]
    dask_distributed_stats = means[100:120]

    fig, axs = plt.subplots(2)

    fig.suptitle('CADaFloP Performance Test Results')

    x = np.arange(len(xs))
    width = 0.25

    axs[0].bar(x - width, carta_histo, width, label='CARTA')
    axs[0].bar(x, dask_local_histo, width, label='Dask (local)')
    axs[0].bar(x + width, dask_distributed_histo, width, label='Dask (distributed)')
    axs[0].set_xlabel("Image dimensions (n X n pixels)")
    axs[0].set_ylabel("Time (s)")
    axs[0].set_xticks(x)
    axs[0].set_xticklabels(xs)
    axs[0].legend()
    axs[0].set_title("Region histogram computation")

    axs[1].bar(x - width, carta_stats, width, label='CARTA')
    axs[1].bar(x, dask_local_stats, width, label='Dask (local)')
    axs[1].bar(x + width, dask_distributed_stats, width, label='Dask (distributed)')
    axs[1].set_xlabel("Image dimensions (n X n pixels)")
    axs[1].set_ylabel("Time (s)")
    axs[1].set_xticks(x)
    axs[1].set_xticklabels(xs)
    axs[1].legend()
    axs[1].set_title("Region statistics computation")

    plt.show()
