# D FOUCHE
# UCT CS HONS
# fchdyl001@myuct.ac.za

import logging
import traceback

import math

import numpy as np

from astropy.io import fits
from h5py import File as hdf5

import dask
import dask.array as da
import dask_image.ndfilters as di

class Image:

    def __init__(self, filename):
        """ Construct image object from given file """

        self.filename = filename
        self.filetype = filename[self.filename.rfind('.')+1:]

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
        return self.data[key]

    def __str__(self):
        s = ""
        s += ("Image %s of type %s \n" %(self.filename, self.filetype))
        s += ("%s dimensions of sizes %s \n" %(self.dimensions, self.shape))
        s += ("Data: %s \n" %(self.data))
        return s

    def get_mean(self):
        """ Compute mean over image data """
        try:
            if "mean" not in dir(self):
                self.mean = self.data.mean().compute()
            return self.mean
        except Exception as e:
            logging.error("[Image]\tFailed to compute mean.")
            traceback.print_exc()

    def get_min(self):
        """ Find min value of image data """
        try:
            if "min" not in dir(self):
                self.min = self.data.min().compute()
            return self.min
        except:
            logging.error("[Image]\tFailed to compute min.")
            traceback.print_exc()

    def get_argmin(self):
        """ Find argmin value of image data """
        try:
            if "argmin" not in dir(self):
                self.argmin = self.data.argmin().compute()
            return self.argmin
        except:
            logging.error("[Image]\tFailed to compute argmin.")
            traceback.print_exc()

    def get_max(self):
        """ Find max value of image data """
        try:
            if "max" not in dir(self):
                self.max = self.data.max().compute()
            return self.max
        except:
            logging.error("[Image]\tFailed to compute max.")
            traceback.print_exc()

    def get_argmax(self):
        """ Find argmax value of image data """
        try:
            if "argmax" not in dir(self):
                self.argmax = self.data.argmax().compute()
            return self.argmax
        except:
            logging.error("[Image]\tFailed to compute argmax.")
            traceback.print_exc()

    def get_range(self):
        """ Compute the range of image data values, if we haven't already """
        try:
            if "range" not in dir(self):
                self.range = [self.get_min(), self.get_max()]
            return self.range
        except:
            logging.error("[Image]\tFailed to compute range.")
            traceback.print_exc()

    def get_std_dev(self):
        """ Compute standard deviation over image data """
        try:
            if "std" not in dir(self):
                self.std = self.data.std().compute()
            return self.std
        except:
            logging.error("[Image]\tFailed to compute standard deviation.")
            traceback.print_exc()

    def get_sum(self):
        """ Compute sum over image data """
        try:
            if "sum" not in dir(self):
                self.sum = self.data.sum().compute()
            return self.sum
        except:
            logging.error("[Image]\tFailed to compute sum.")
            traceback.print_exc()

    def get_region_histogram(self, bins=None, range=None):
        """ Compute histrogram for image """
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
        try:
            return dask.compute(self.data.sum(), self.data.mean(), self.data.std(), self.data.min(), self.data.max())
        except:
            logging.error("[Image]\tFailed to compute region statistics.")
            traceback.print_exc()

    def get_smoothed(self, sigma=1):
        """ Apply a Gaussian filter over image """
        try:
            smoothed_arr = di.gaussian_filter(self.data, sigma)
            return smoothed_arr.compute()
        except:
            logging.error("[Image]\tFailed to compute smoothed image.")
            traceback.print_exc()

    def get_default_num_bins(self):
        """ Return the default number of bins as int(std::max(sqrt(_image_shape(0) * _image_shape(1)), 2.0)) """
        return int(max(2, math.sqrt(self.shape[0] * self.shape[1])))
