# D FOUCHE
# UCT CS HONS
# fchdyl001@myuct.ac.za

import numpy
from astropy.io import fits
from h5py import File as hdf5

class image:
    def __init__(self):
        self.filename = ""
        self.filetype = ""
        self.dimensions = 0
        self.shape = []
        self.data = null

    def __init__(self,filename):
        self.filename = filename
        self.filetype = filename[self.filename.rfind('.')+1:]

        if(self.filetype == "hdf5"):
            f = hdf5(self.filename, 'r')
            if 'DATA' in f['0']:
                self.data = f['0']['DATA']
                self.dimensions = len(self.data.shape)
                self.shape = self.data.shape
            else:
                print("Unable to read in hdf5 file")

        elif(self.filetype == "fits"):
            self.data = fits.getdata(self.filename)
            self.dimensions = len(self.data.shape)
            self.shape = self.data.shape

        else:
            print("Filetype %s not supported" %self.filetype)

    def __getitem__(self,key):
        return self.data[key]

    def showStats(self):
        print("Image %s of type %s" %(self.filename, self.filetype))
        print("%s dimensions of sizes %s" %(self.dimensions, self.shape))
