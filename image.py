# D FOUCHE
# UCT CS HONS
# fchdyl001@myuct.ac.za

import numpy
from astropy.io import fits
from h5py import File as hdf5
import dask.array as da

class image:
    def __init__(self):
        self.filename = ""
        self.filetype = ""
        self.dimensions = 0
        self.shape = []
        self.data = null

    def __init__(self,filename, chunk=1000):
        self.filename = filename
        self.filetype = filename[self.filename.rfind('.')+1:]

        if(self.filetype == "hdf5"):
            f = hdf5(self.filename, 'r')
            if 'DATA' in f['0']:
                d = f['0']['DATA']
                self.dimensions = len(d.shape)
                self.shape = d.shape
                self.data = da.from_array(d, chunks=([chunk] * self.dimensions))
            else:
                print("Unable to read in hdf5 file")

        elif(self.filetype == "fits"):
            f = fits.open(self.filename, memmap=True)
            d = f[0].data
            self.dimensions = len(d.shape)
            self.shape = d.shape
            self.data = da.from_array(d, chunks=([chunk] * self.dimensions))

        else:
            print("Filetype %s not supported" %self.filetype)

    def __getitem__(self,key):
        return self.data[key]

    def showStats(self):
        print("Image %s of type %s" %(self.filename, self.filetype))
        print("%s dimensions of sizes %s" %(self.dimensions, self.shape))
