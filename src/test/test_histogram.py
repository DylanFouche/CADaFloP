# D FOUCHE
# UCT CS HONS
# fchdyl001@myuct.ac.za

import unittest
import timeit

import logging

import threading
import time

import statistics

import sys

from collections import Iterable

from src.frontend.client import *
from src.backend.server import *

class HistogramUnitTests(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        """ Called before tests, instantiate clients and server """

        self.directory = "/data/cadaflop/Data/"

        self.TEST_FILES = {"h_m51_b_s05_drz_sci.fits", "orion.fits"}

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

    def is_close(self, a, b):
        """ Assert that two numbers or lists are almost equal (accounting for floating point errors) """
        if isinstance(a, Iterable) and isinstance(b, Iterable):
            for ai, bi in zip(a, b):
                if bi > (ai + (0.001*ai)) or bi < (ai - (0.001*ai)):
                    raise AssertionError("{} is not close to {}".format(ai, bi))
        else:
            if b > (a + (0.001*a)) or b < (a - (0.001*a)):
                raise AssertionError("{} is not close to {}".format(a, b))
        return True

    def test_histogram_correct(self):
        """ Assert that histograms returned by carta and dask are equal """
        for test_file in self.TEST_FILES:
            with self.subTest(file = test_file):
                self.dask_client.open_file(test_file, self.directory)
                self.carta_client.open_file(test_file, self.directory)
                dask_histo, dask_mean, dask_std = self.dask_client.get_region_histogram()
                carta_histo, carta_mean, carta_std = self.carta_client.get_region_histogram()

                self.assertTrue(self.is_close(dask_histo, carta_histo))

    def test_mean_correct(self):
        """ Assert that means returned by carta and dask are close """
        for test_file in self.TEST_FILES:
            with self.subTest(file = test_file):
                self.dask_client.open_file(test_file, self.directory)
                self.carta_client.open_file(test_file, self.directory)
                dask_histo, dask_mean, dask_std = self.dask_client.get_region_histogram()
                carta_histo, carta_mean, carta_std = self.carta_client.get_region_histogram()

                self.assertTrue(self.is_close(dask_mean, carta_mean))

    def test_standard_deviation_correct(self):
        """ Assert that standard deviations returned by carta and dask are close """
        for test_file in self.TEST_FILES:
            with self.subTest(file = test_file):
                self.dask_client.open_file(test_file, self.directory)
                self.carta_client.open_file(test_file, self.directory)
                dask_histo, dask_mean, dask_std = self.dask_client.get_region_histogram()
                carta_histo, carta_mean, carta_std = self.carta_client.get_region_histogram()

                self.assertTrue(self.is_close(dask_std, carta_std))

class HistogramPerformanceTests():

    def __init__(self):
        """ Instantiate the histogram performance testing class, launch a server and create client objects """

        self.directory = "/data/cadaflop/Data/"

        self.TEST_FILES = {"h_m51_b_s05_drz_sci.fits", "orion.fits"}

        # Log results to file
        file_handler = logging.FileHandler('performance.log')
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

    def run(self, n=10, fileout="log.txt"):
        """ Execute histogram performance tests """
        logging.critical("================================================================")

        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        logging.critical("{}: Beginning performance testing for the histogram function".format(now))

        for test_file in self.TEST_FILES:
            logging.critical("===File: {}===".format(test_file))

            # Warm-up
            self.dask_client.clear_cache_and_open_file_and_get_region_histogram(test_file, self.directory)
            self.carta_client.clear_cache_and_open_file_and_get_region_histogram(test_file, self.directory)

            # Test Dask server

            logging.critical("--- Dask Server ---")
            logging.critical("Computing histogram {} times...".format(n))

            times = timeit.repeat(lambda:
                self.dask_client.clear_cache_and_open_file_and_get_region_histogram(test_file, self.directory),
                repeat = n, number = 1)

            logging.critical("Execution times: {}".format(times))
            logging.critical("Mean: {}".format(statistics.mean(times)))
            logging.critical("Variance: {}".format(statistics.variance(times)))
            logging.critical("Std dev: {}".format(statistics.stdev(times)))

            # Test Carta server

            logging.critical("--- Carta Back-end ---")
            logging.critical("Computing histogram {} times...".format(n))

            times = timeit.repeat(lambda:
                self.carta_client.clear_cache_and_open_file_and_get_region_histogram(test_file, self.directory),
                repeat = n, number = 1)

            logging.critical("Execution times: {}".format(times))
            logging.critical("Mean: {}".format(statistics.mean(times)))
            logging.critical("Variance: {}".format(statistics.variance(times)))
            logging.critical("Std dev: {}".format(statistics.stdev(times)))

        logging.critical("================================================================")
