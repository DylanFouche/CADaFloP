# D FOUCHE
# UCT CS HONS
# fchdyl001@myuct.ac.za

import numpy
from h5py import File as hdf5
import dask.array as da

class image:
    def __init__(self):
        self.filename = ""
        self.filetype = ""
        self.shape = []
        self.dimensions = 0
        self.data = null

    def __init__(self,filename, chunk=1000):
        self.filename = filename
        self.filetype = filename[self.filename.rfind('.')+1:]

        try:
            if (self.filetype != "hdf5"):
                raise Exception("Unsupported file type.")

            f = hdf5(self.filename, 'r')

            if 'DATA' not in f['0']:
                raise Exception("Unexpected format in hdf file.")

            d = f['0']['DATA']
            self.shape = d.shape
            self.dimensions = len(self.shape)
            self.data = da.from_array(d, chunks=([chunk] * self.dimensions))

        except Exception as e:
            print("Unable to read in image file:")
            print(str(e))

    def __getitem__(self,key):
        return self.data[key]

    def showStats(self):
        print("Image %s of type %s" %(self.filename, self.filetype))
        print("%s dimensions of sizes %s" %(self.dimensions, self.shape))
