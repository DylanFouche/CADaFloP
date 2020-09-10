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

    def __init__(self, filename, chunk=1000):
        """ Construct image object from given file """
        self.filename = filename
        self.filetype = filename[self.filename.rfind('.')+1:]

        try:
            if (self.filetype == "hdf5"):

                f = hdf5(self.filename, 'r')
                if 'DATA' not in f['0']:
                    raise Exception("Unexpected format in hdf file.")
                d = f['0']['DATA']
                self.shape = d.shape
                self.dimensions = len(self.shape)
                self.data = da.from_array(d, chunks=([chunk] * self.dimensions))

            elif (self.filetype == "fits"):

                f = fits.open(self.filename, memmap=True)
                if "data" not in dir(f[0]):
                    raise Exception("Unexpected format in fits file.")
                d = f[0].data
                self.shape = d.shape
                self.dimensions = len(self.shape)
                self.data = da.from_array(d, chunks=([chunk] * self.dimensions))

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

    def get_range(self):
        """ Compute the range of image data values, if we haven't already """
        try:
            if "range" not in dir(self):
                min, max = dask.compute(self.data.min(), self.data.max())
                self.range = [min, max]
            return self.range
        except Exception as e:
            logging.error("[Image]\tFailed to instantiate image object.")
            traceback.print_exc()
            raise e

    def get_histogram(self, bins=None, range=None):
        """ Compute histrogram for image """
        try:
            if bins is None:
                bins = self.get_default_num_bins()
            if range is None:
                range = self.get_range()
            hist, bins = da.histogram(self.data, bins=bins, range=range)
            return hist.compute()
        except Exception as e:
            logging.error("[Image]\tFailed to compute histogram.")
            traceback.print_exc()

    def get_mean(self):
        """ Compute mean over image data """
        try:
            if "mean" not in dir(self):
                self.mean = self.data.mean().compute()
            return self.mean
        except Exception as e:
            logging.error("[Image]\tFailed to compute mean.")
            traceback.print_exc()

    def get_std_dev(self):
        """ Compute standard deviation over image data """
        try:
            if "std" not in dir(self):
                self.std = self.data.std().compute()
            return self.std
        except Exception as e:
            logging.error("[Image]\tFailed to compute standard deviation.")
            traceback.print_exc()

    def get_smoothed(self, sigma=1):
        """ Apply a Gaussian filter over image """
        try:
            smoothed_arr = di.gaussian_filter(self.data, sigma)
            return smoothed_arr.compute()
        except Exception as e:
            logging.error("[Image]\tFailed to compute smoothed image.")
            traceback.print_exc()

    def get_default_num_bins(self):
        """ Return the default number of bins as int(std::max(sqrt(_image_shape(0) * _image_shape(1)), 2.0)) """
        return int(max(2, math.sqrt(self.shape[0] * self.shape[1])))
