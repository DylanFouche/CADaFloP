# D FOUCHE
# UCT CS HONS
# fchdyl001@myuct.ac.za

import timeit
import logging
import threading
import time
import statistics
import sys
import os

from src.frontend.client import *
from src.backend.server import *


class PerformanceTests():

    def __init__(self, cluster, carta, ramdisk, n=10):
        """ Instantiate the histogram performance testing class, launch a server and create client objects """

        self.n = n
        self.ramdisk = ramdisk

        self.directory = "/ramdisk/" if ramdisk else "/data/cadaflop/Data/"

        self.TEST_FILES = ['image-1000-1000.fits',
                           'image-2000-2000.fits',
                           'image-3000-3000.fits',
                           'image-4000-4000.fits',
                           'image-5000-5000.fits',
                           'image-6000-6000.fits',
                           'image-7000-7000.fits',
                           'image-8000-8000.fits',
                           'image-9000-9000.fits',
                           'image-10000-10000.fits',
                           'image-11000-11000.fits',
                           'image-12000-12000.fits',
                           'image-13000-13000.fits',
                           'image-14000-14000.fits',
                           'image-15000-15000.fits',
                           'image-16000-16000.fits',
                           'image-17000-17000.fits',
                           'image-18000-18000.fits',
                           'image-19000-19000.fits',
                           'image-20000-20000.fits']

        # Log results to file
        fileout = "data/performance-ram.log" if ramdisk else "data/performance-disk.log"
        file_handler = logging.FileHandler(fileout)
        file_handler.setLevel(logging.CRITICAL)
        logging.getLogger().addHandler(file_handler)
        logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

        if carta:
            # Instantiate carta client (assume carta server already running)
            self.client = Client(
                "CartaClient", 'localhost', 3002, is_carta_client=True)
            logging.critical(
                "Executing performance tests against CARTA back-end")
        else:
            # Start a Dask server
            serverThread = threading.Thread(target=Server, args=(
                'localhost', 3003, cluster, ramdisk), daemon=True)
            serverThread.start()
            time.sleep(15)

            # Instantiate dask client
            self.client = Client(
                "DaskClient", 'localhost', 3003, is_carta_client=False)

            dask_qualifier = 'distributed' if cluster else 'local'
            logging.critical(
                "Executing performance tests against dask {} server".format(dask_qualifier))

        # Register client as viewer
        self.client.register_viewer()

    def run_histogram_tests(self):
        self.__do_tests(self.client.get_region_histogram, "region histogram")

    def run_statistics_tests(self):
        self.__do_tests(self.client.get_region_statistics, "region statistics")

    def __do_tests(self, f, fname):
        """ Execute performance tests for some function f """
        logging.critical(
            "================================================================")

        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        if self.ramdisk:
            logging.critical(
                "{}: Beginning performance testing for the {} function with data from memory.".format(now, fname))
        else:
            logging.critical(
                "{}: Beginning performance testing for the {} function with data from disk.".format(now, fname))

        for test_file in self.TEST_FILES:

            if self.ramdisk:
                # Put test file in ramdisk
                os.system(
                    'echo "rm -f /ramdisk/* " | sudo bash')
                os.system(
                    'cp /data/cadaflop/Data/{} /ramdisk/ '.format(test_file))

            logging.critical("===File: {}===".format(test_file))

            os.system(
                'echo "sync && echo 3 > /proc/sys/vm/drop_caches" | sudo bash')
            self.__open_file_and_execute_function(f, test_file, self.directory)
            time.sleep(5)

            logging.critical("Computing {} {} times".format(fname, self.n))

            times = []

            for i in range(self.n):

                print('.', end='', flush=True)

                os.system(
                    'echo "sync && echo 3 > /proc/sys/vm/drop_caches" | sudo bash')

                times.append(timeit.timeit(lambda:
                                           self.__open_file_and_execute_function(
                                               f, test_file, self.directory),
                                           number=1))

            print()

            logging.critical("Execution times: {}".format(times))
            logging.critical("Mean: {}".format(statistics.mean(times)))
            logging.critical("Variance: {}".format(statistics.variance(times)))
            logging.critical("Std dev: {}".format(statistics.stdev(times)))

        logging.critical(
            "================================================================")

    def __open_file_and_execute_function(self, f, file, directory):
        self.client.open_file(file, directory)
        return f()
