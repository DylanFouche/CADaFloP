#!/usr/bin/env python3

# D FOUCHE
# UCT CS HONS
# fchdyl001@myuct.ac.za

import sys
import numpy as np
import xlsxwriter

dimensions = [str(n)+'X'+str(n) for n in range(1000,21000,1000)]

with xlsxwriter.Workbook('data/results.xlsx') as workbook:

    for file in sys.argv[1:]:

        means = []
        devs = []

        with open(file, "r") as f:
            for line in f:
                if line[0:5] == "Mean:":
                    means.append(float(line[6:].rstrip()))
                elif line[0:8] == "Std dev:":
                    devs.append(float(line[9:].rstrip()))

        carta_histo_mean = means[0:20]
        carta_histo_dev = devs[0:20]
        carta_stats_mean = means[20:40]
        carta_stats_dev = devs[20:40]

        dask_local_histo_mean = means[40:60]
        dask_local_histo_dev = devs[40:60]
        dask_local_stats_mean = means[60:80]
        dask_local_stats_dev = devs[60:80]

        dask_distributed_histo_mean = means[80:100]
        dask_distributed_histo_dev = devs[80:100]
        dask_distributed_stats_mean = means[100:120]
        dask_distributed_stats_dev = devs[100:120]

        worksheet = workbook.add_worksheet(file[file.find('/')+1:file.find('.')]+'-histogram')

        worksheet.write(0,0,"Image dimensions")
        worksheet.write(0,1,"Runtime (seconds)")
        worksheet.write(1,1,"CARTA")
        worksheet.write(1,2,"Dask (local)")
        worksheet.write(1,3,"Dask (distributed)")

        for row, data in enumerate(dimensions):
            worksheet.write((row*2)+2, 0, data)
        for i in range(2, len(carta_histo_mean)*2 + 2):
            if i%2 == 0:
                worksheet.write(i, 1, "mean")
            else:
                worksheet.write(i, 1, "std dev")

        for row, data in enumerate(carta_histo_mean):
            worksheet.write((row*2)+2, 2, data)
        for row, data in enumerate(dask_local_histo_mean):
            worksheet.write((row*2)+2, 3, data)
        for row, data in enumerate(dask_distributed_histo_mean):
            worksheet.write((row*2)+2, 4, data)

        for row, data in enumerate(carta_histo_dev):
            worksheet.write((row*2)+3, 2, data)
        for row, data in enumerate(dask_local_histo_dev):
            worksheet.write((row*2)+3, 3, data)
        for row, data in enumerate(dask_distributed_histo_dev):
            worksheet.write((row*2)+3, 4, data)

        worksheet = workbook.add_worksheet(file[file.find('/')+1:file.find('.')]+'-statistics')

        worksheet.write(0,0,"Image dimensions")
        worksheet.write(0,1,"Runtime (seconds)")
        worksheet.write(1,1,"CARTA")
        worksheet.write(1,2,"Dask (local)")
        worksheet.write(1,3,"Dask (distributed)")

        for row, data in enumerate(dimensions):
            worksheet.write((row*2)+2, 0, data)
        for i in range(2, len(carta_histo_mean)*2 + 2):
            if i%2 == 0:
                worksheet.write(i, 1, "mean")
            else:
                worksheet.write(i, 1, "std dev")

        for row, data in enumerate(carta_stats_mean):
            worksheet.write((row*2)+2, 2, data)
        for row, data in enumerate(dask_local_stats_mean):
            worksheet.write((row*2)+2, 3, data)
        for row, data in enumerate(dask_distributed_stats_mean):
            worksheet.write((row*2)+2, 4, data)

        for row, data in enumerate(carta_stats_dev):
            worksheet.write((row*2)+3, 2, data)
        for row, data in enumerate(dask_local_stats_dev):
            worksheet.write((row*2)+3, 3, data)
        for row, data in enumerate(dask_distributed_stats_dev):
            worksheet.write((row*2)+3, 4, data)
