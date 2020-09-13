# D FOUCHE
# UCT CS HONS
# fchdyl001@myuct.ac.za

import timeit
import logging
import threading
import time
import statistics
import sys

from src.frontend.client import *
from src.backend.server import *

class PerformanceTests():

    def __init__(self, n=10, fileout="performance.log"):
        """ Instantiate the histogram performance testing class, launch a server and create client objects """

        self.n = n
        self.directory = "/data/cadaflop/Data/"
        self.TEST_FILES = {"h_m51_b_s05_drz_sci.fits", "orion.fits"}

        # Log results to file
        file_handler = logging.FileHandler(fileout)
        file_handler.setLevel(logging.CRITICAL)
        logging.getLogger().addHandler(file_handler)
        logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

        # Start a Dask server (assume CARTA server already running)
        serverThread = threading.Thread(target=Server, args=('localhost', 3003), daemon=True)
        serverThread.start()
        time.sleep(1)

        # Instantiate dask client
        self.dask_client = Client("DaskClient", 'localhost', 3003)

        # Instantiate carta client
        self.carta_client = Client("CartaClient", 'localhost', 3002, is_carta_client=True)

        # Register clients as viewers
        self.dask_client.register_viewer()
        self.carta_client.register_viewer()

    def run_histogram_tests(self):
        """ Execute region histogram performance tests """
        logging.critical("================================================================")

        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        logging.critical("{}: Beginning performance testing for the region histogram function".format(now))

        for test_file in self.TEST_FILES:
            logging.critical("===File: {}===".format(test_file))

            # Warm-up
            self.dask_client.clear_cache_and_open_file_and_get_region_histogram(test_file, self.directory)
            self.carta_client.clear_cache_and_open_file_and_get_region_histogram(test_file, self.directory)

            # Test Dask server

            logging.critical("--- Dask Server ---")
            logging.critical("Computing region histogram {} times...".format(self.n))

            times = timeit.repeat(lambda:
                self.dask_client.clear_cache_and_open_file_and_get_region_histogram(test_file, self.directory),
                repeat = self.n, number = 1)

            logging.critical("Execution times: {}".format(times))
            logging.critical("Mean: {}".format(statistics.mean(times)))
            logging.critical("Variance: {}".format(statistics.variance(times)))
            logging.critical("Std dev: {}".format(statistics.stdev(times)))

            # Test Carta server

            logging.critical("--- Carta Back-end ---")
            logging.critical("Computing region histogram {} times...".format(self.n))

            times = timeit.repeat(lambda:
                self.carta_client.clear_cache_and_open_file_and_get_region_histogram(test_file, self.directory),
                repeat = self.n, number = 1)

            logging.critical("Execution times: {}".format(times))
            logging.critical("Mean: {}".format(statistics.mean(times)))
            logging.critical("Variance: {}".format(statistics.variance(times)))
            logging.critical("Std dev: {}".format(statistics.stdev(times)))

        logging.critical("================================================================")

    def run_statistics_tests(self, n=10):
        """ Execute region statistics performance tests """
        logging.critical("================================================================")

        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        logging.critical("{}: Beginning performance testing for the region statistics function".format(now))

        for test_file in self.TEST_FILES:
            logging.critical("===File: {}===".format(test_file))

            # Warm-up
            self.dask_client.clear_cache_and_open_file_and_get_region_statistics(test_file, self.directory)
            self.carta_client.clear_cache_and_open_file_and_get_region_statistics(test_file, self.directory)

            # Test Dask server

            logging.critical("--- Dask Server ---")
            logging.critical("Computing region statistics {} times...".format(self.n))

            times = timeit.repeat(lambda:
                self.dask_client.clear_cache_and_open_file_and_get_region_statistics(test_file, self.directory),
                repeat = self.n, number = 1)

            logging.critical("Execution times: {}".format(times))
            logging.critical("Mean: {}".format(statistics.mean(times)))
            logging.critical("Variance: {}".format(statistics.variance(times)))
            logging.critical("Std dev: {}".format(statistics.stdev(times)))

            # Test Carta server

            logging.critical("--- Carta Back-end ---")
            logging.critical("Computing region statistics {} times...".format(self.n))

            times = timeit.repeat(lambda:
                self.carta_client.clear_cache_and_open_file_and_get_region_statistics(test_file, self.directory),
                repeat = self.n, number = 1)

            logging.critical("Execution times: {}".format(times))
            logging.critical("Mean: {}".format(statistics.mean(times)))
            logging.critical("Variance: {}".format(statistics.variance(times)))
            logging.critical("Std dev: {}".format(statistics.stdev(times)))

        logging.critical("================================================================")
