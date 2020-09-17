# D FOUCHE
# UCT CS HONS
# fchdyl001@myuct.ac.za

import matplotlib.pyplot as plt

xs = [5, 17, 37, 65, 101, 145, 197, 257, 325, 401, 485, 577, 677, 785, 901, 1025, 1157, 1297, 1445, 1601]

means = []

with open("results.txt", "r") as f:
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

axs[0].plot(xs, carta_histo)
axs[0].plot(xs, dask_local_histo)
axs[0].plot(xs, dask_distributed_histo)
axs[0].legend(["CARTA", "Dask Local", "Dask Distributed"])
axs[0].set_xlabel("File size (MB)")
axs[0].set_ylabel("Time (s)")
axs[0].set_title("Region histogram computation")

axs[1].plot(xs, carta_stats)
axs[1].plot(xs, dask_local_stats)
axs[1].plot(xs, dask_distributed_stats)
axs[1].legend(["CARTA", "Dask Local", "Dask Distributed"])
axs[1].set_xlabel("File size (MB)")
axs[1].set_ylabel("Time (s)")
axs[1].set_title("Region statistics computation")

plt.show()
