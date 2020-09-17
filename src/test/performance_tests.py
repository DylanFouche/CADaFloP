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

    def __init__(self, cluster, carta, n=10, fileout="performance.log"):
        """ Instantiate the histogram performance testing class, launch a server and create client objects """

        self.n = n
        self.directory = "/data/cadaflop/Data/"

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
        file_handler = logging.FileHandler(fileout)
        file_handler.setLevel(logging.CRITICAL)
        logging.getLogger().addHandler(file_handler)
        logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

        if carta:
            # Instantiate carta client (assume carta server already running)
            self.client = Client("CartaClient", 'localhost', 3002, is_carta_client=True)
            logging.critical("Executing performance tests against CARTA back-end")
        else:
            # Start a Dask server
            serverThread = threading.Thread(target=Server, args=('localhost', 3003, cluster), daemon=True)
            serverThread.start()
            time.sleep(15)

            # Instantiate dask client
            self.client = Client("DaskClient", 'localhost', 3003)

            dask_qualifier = 'distributed' if cluster else 'local'
            logging.critical("Executing performance tests against dask {} server".format(dask_qualifier))

        # Register client as viewer
        self.client.register_viewer()

    def run_histogram_tests(self):
        """ Execute region histogram performance tests """
        logging.critical("================================================================")

        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        logging.critical("{}: Beginning performance testing for the region histogram function".format(now))

        for test_file in self.TEST_FILES:
            logging.critical("===File: {}===".format(test_file))

            # Warm-up
            self.__clear_cache_and_open_file_and_execute_function(test_file, self.directory, self.client.get_region_histogram)

            # Do tests
            logging.critical("Computing region histogram {} times...".format(self.n))

            times = timeit.repeat(lambda:
                self.__clear_cache_and_open_file_and_execute_function(test_file, self.directory, self.client.get_region_histogram),
                repeat = self.n, number = 1)

            # Log results
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
            self.__clear_cache_and_open_file_and_execute_function(test_file, self.directory, self.client.get_region_statistics)

            # Do tests
            logging.critical("Computing region statistics {} times...".format(self.n))

            times = timeit.repeat(lambda:
                self.__clear_cache_and_open_file_and_execute_function(test_file, self.directory, self.client.get_region_statistics),
                repeat = self.n, number = 1)

            # Log results
            logging.critical("Execution times: {}".format(times))
            logging.critical("Mean: {}".format(statistics.mean(times)))
            logging.critical("Variance: {}".format(statistics.variance(times)))
            logging.critical("Std dev: {}".format(statistics.stdev(times)))

        logging.critical("================================================================")

    def __clear_cache_and_open_file_and_execute_function(self, file, directory, f):
        os.system('echo "sync && echo 3 > /proc/sys/vm/drop_caches" | sudo bash')
        self.client.open_file(file, directory)
        return f()
