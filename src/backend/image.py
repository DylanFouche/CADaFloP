# D FOUCHE
# UCT CS HONS
# fchdyl001@myuct.ac.za

import logging
import traceback

import math

from astropy.io import fits
from h5py import File as hdf5

import dask
import dask.array as da
import dask_image.ndfilters as di


class Image:
    """An image object that stores data in a Dask array and provides functions to perform various Dask computations."""

    def __init__(self, filename):
        """Construct image object from given file.

        :param filename: The path to the image file to be opened

        """
        self.filename = filename
        self.filetype = filename[self.filename.rfind('.') + 1:]

        try:
            if (self.filetype == "hdf5"):

                with hdf5(self.filename, 'r') as f:

                    if 'DATA' not in f['0']:
                        raise Exception("Unexpected format in hdf file.")
                    d = f['0']['DATA']
                    self.shape = d.shape
                    self.dimensions = len(self.shape)
                    chunk_size = 'auto' if self.shape[0] * self.shape[1] > 25000000 else (1000, 1000)
                    self.data = da.from_array(d, chunks=chunk_size)

            elif (self.filetype == "fits"):

                with fits.open(self.filename, memmap=True) as f:

                    if "data" not in dir(f[0]):
                        raise Exception("Unexpected format in fits file.")
                    d = f[0].data
                    self.shape = d.shape
                    self.dimensions = len(self.shape)
                    chunk_size = 'auto' if self.shape[0] * self.shape[1] > 25000000 else (1000, 1000)
                    self.data = da.from_array(d, chunks=chunk_size)

            else:
                raise Exception("Unsupported file type.")

        except Exception as e:
            logging.error("[Image]\tFailed to instantiate image object.")
            traceback.print_exc()
            raise e

    def __getitem__(self, key):
        """Access a slice of our image data.

        :param key: the index to access
        :return: returns the image slice at given index

        """
        return self.data[key]

    def __str__(self):
        """Get image metadata in string format.

        :return: string representation of the object

        """
        s = ""
        s += ("Image %s of type %s \n" % (self.filename, self.filetype))
        s += ("%s dimensions of sizes %s \n" % (self.dimensions, self.shape))
        s += ("Data: %s \n" % (self.data))
        return s

    def get_mean(self):
        """Compute mean over image data.

        :return: mean of image data

        """
        try:
            if "mean" not in dir(self):
                self.mean = self.data.mean().compute()
            return self.mean
        except:
            logging.error("[Image]\tFailed to compute mean.")
            traceback.print_exc()

    def get_min(self):
        """Compute minimum value of image data.

        :return: minimum value of image data

        """
        try:
            if "min" not in dir(self):
                self.min = self.data.min().compute()
            return self.min
        except:
            logging.error("[Image]\tFailed to compute min.")
            traceback.print_exc()

    def get_argmin(self):
        """Compute argmin value of image data.

        :return: argmin value of image data

        """
        try:
            if "argmin" not in dir(self):
                self.argmin = self.data.argmin().compute()
            return self.argmin
        except:
            logging.error("[Image]\tFailed to compute argmin.")
            traceback.print_exc()

    def get_max(self):
        """Compute maximum value of image data.

        :return: maximum value of image data

        """
        try:
            if "max" not in dir(self):
                self.max = self.data.max().compute()
            return self.max
        except:
            logging.error("[Image]\tFailed to compute max.")
            traceback.print_exc()

    def get_argmax(self):
        """Compute argmax value of image data.

        :return: argmax value of image data

        """
        try:
            if "argmax" not in dir(self):
                self.argmax = self.data.argmax().compute()
            return self.argmax
        except:
            logging.error("[Image]\tFailed to compute argmax.")
            traceback.print_exc()

    def get_range(self):
        """Compute the range of image data.

        :return: a tuple (minimum, maximum) of image data

        """
        try:
            if "range" not in dir(self):
                self.range = [self.get_min(), self.get_max()]
            return self.range
        except:
            logging.error("[Image]\tFailed to compute range.")
            traceback.print_exc()

    def get_std_dev(self):
        """Compute standard deviation over image data.

        :return: the standard deviation of image data

        """
        try:
            if "std" not in dir(self):
                self.std = self.data.std().compute()
            return self.std
        except:
            logging.error("[Image]\tFailed to compute standard deviation.")
            traceback.print_exc()

    def get_sum(self):
        """Compute sum over image data.

        :return: the sum of the image data

        """
        try:
            if "sum" not in dir(self):
                self.sum = self.data.sum().compute()
            return self.sum
        except:
            logging.error("[Image]\tFailed to compute sum.")
            traceback.print_exc()

    def get_region_histogram(self, bins=None, range=None):
        """Compute histrogram for image.

        If bins is none, will use get_default_num_bins()
        If range is none, will use get_range()

        :param bins: The integer number of bins for the histogram (Default value = None)
        :param range: The minimum and maximum values to count in the histogram (Default value = None)
        :return: the image histogram

        """
        try:
            if bins is None:
                bins = self.get_default_num_bins()
            if range is None:
                range = self.get_range()
            hist, bins = da.histogram(self.data, bins=bins, range=range)
            return hist.compute()
        except:
            logging.error("[Image]\tFailed to compute region histogram.")
            traceback.print_exc()

    def get_region_statistics(self):
        """Compute the sum, mean, std deviation, min, and max of image data in one pass.

        :return: a tuple (sum, mean, std deviation, min, max) of image data

        """
        try:
            return dask.compute(self.data.sum(), self.data.mean(), self.data.std(), self.data.min(), self.data.max())
        except:
            logging.error("[Image]\tFailed to compute region statistics.")
            traceback.print_exc()

    def get_smoothed(self, sigma=1):
        """Apply a Gaussian filter over image.

        :param sigma: The smoothing factor (Default value = 1)
        :return: a smoothed copy of the image

        """
        try:
            smoothed_arr = di.gaussian_filter(self.data, sigma)
            return smoothed_arr.compute()
        except:
            logging.error("[Image]\tFailed to compute smoothed image.")
            traceback.print_exc()

    def get_default_num_bins(self):
        """Get the default number of bins for histogram.

        :return: the default number of bins

        """
        return int(max(2, math.sqrt(self.shape[0] * self.shape[1])))
