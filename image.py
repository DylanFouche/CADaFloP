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
    def __init__(self):
        self.filename = ""
        self.filetype = ""
        self.shape = []
        self.dimensions = 0
        self.data = null

    def __init__(self, filename, chunk=1000):
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

                if not hasattr(f[0], "data"):
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

    def getRange(self):
        if not hasattr(self,"range"):
            min, max = dask.compute(self.data.min(), self.data.max())
            self.range = [min, max]
        return self.range

    def histogram(self, bins=10, range=None):
        if not range:
            range = self.getRange()
        hist, bins = da.histogram(self.data, bins=bins, range=range)
        return hist.compute()

    def smooth(self, sigma=1):
        smoothed_arr = di.gaussian_filter(self.data, sigma)
        return smoothed_arr.compute()

    def showMetadata(self):
        print("Image %s of type %s" %(self.filename, self.filetype))
        print("%s dimensions of sizes %s" %(self.dimensions, self.shape))
