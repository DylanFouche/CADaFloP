# D FOUCHE
# UCT CS HONS
# fchdyl001@myuct.ac.za

import unittest

import threading
import time

from collections import Iterable

from src.frontend.client import *
from src.backend.server import *

class HistogramTests(unittest.TestCase):

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
