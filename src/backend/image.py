# D FOUCHE
# UCT CS HONS
# fchdyl001@myuct.ac.za

import numpy as np
from astropy.io import fits
from h5py import File as hdf5
import dask
import dask.array as da
import dask_image.ndfilters as di

class image:

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
            print("Unable to read in image file:")
            print(str(e))

    def __getitem__(self, key):
        return self.data[key]

    def __str__(self):
        s = ""
        s += ("Image %s of type %s \n" %(self.filename, self.filetype))
        s += ("%s dimensions of sizes %s \n" %(self.dimensions, self.shape))
        s += ("Data: %s \n" %(self.data))
        return s

    def getRange(self):
        """ Compute the range of image data values, if we haven't already """
        if "range" not in dir(self):
            min, max = dask.compute(self.data.min(), self.data.max())
            self.range = [min, max]
        return self.range

    def histogram(self, bins=10, range=None):
        """ Compute histrogram for image """
        if range is None:
            range = self.getRange()
        hist, bins = da.histogram(self.data, bins=bins, range=range)
        return hist.compute()

    def smoothed(self, sigma=1):
        """ Apply a Gaussian filter over image """
        smoothed_arr = di.gaussian_filter(self.data, sigma)
        return smoothed_arr.compute()
