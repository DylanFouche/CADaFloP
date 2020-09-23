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

        worksheet = workbook.add_worksheet(file[file.find('/')+1:file.find('.')]+'-histogram')

        worksheet.write(0,0,"Image dimensions")
        worksheet.write(0,1,"Runtime (seconds)")
        worksheet.write(1,1,"CARTA")
        worksheet.write(1,2,"Dask (local)")
        worksheet.write(1,3,"Dask (distributed)")

        for row, data in enumerate(dimensions):
            worksheet.write(row+2, 0, data)
        for row, data in enumerate(carta_histo):
            worksheet.write(row+2, 1, data)
        for row, data in enumerate(dask_local_histo):
            worksheet.write(row+2, 2, data)
        for row, data in enumerate(dask_distributed_histo):
            worksheet.write(row+2, 3, data)

        worksheet = workbook.add_worksheet(file[file.find('/')+1:file.find('.')]+'-statistics')

        worksheet.write(0,0,"Image dimensions")
        worksheet.write(0,1,"Runtime (seconds)")
        worksheet.write(1,1,"CARTA")
        worksheet.write(1,2,"Dask (local)")
        worksheet.write(1,3,"Dask (distributed)")

        for row, data in enumerate(dimensions):
            worksheet.write(row+2, 0, data)
        for row, data in enumerate(carta_stats):
            worksheet.write(row+2, 1, data)
        for row, data in enumerate(dask_local_stats):
            worksheet.write(row+2, 2, data)
        for row, data in enumerate(dask_distributed_stats):
            worksheet.write(row+2, 3, data)
