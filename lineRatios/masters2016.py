#! /usr/bin/env python

import sys,os
import numpy as np
import pkg_resources
from scipy.spatial import cKDTree
from .utils.progress import Progress

def buildMastersSDSSNumpy():
    import pyfits
    npyfile = pkg_resources.resource_filename(__name__,"datasets/sdss_sample_final_cut_SNcut.npy")
    fitsfile = pkg_resources.resource_filename(__name__,"datasets/sdss_sample_final_cut_SNcut.fits")
    f = pyfits.open(fitsfile)
    data = f[1].data
    dtype = [("log10StellarMass",float),("log10NiiHalphaRatio",float),("log10OiiiHbetaRatio",float),("sSFRinGyr",float)]
    galaxies = np.zeros(len(data[:]),dtype=dtype).view(np.recarray)
    PROG = Progress(len(data[:]))
    for i in range(len(data)):
        galaxies.log10StellarMass[i] = np.copy(data[i][0])
        galaxies.log10NiiHalphaRatio[i] = np.copy(data[i][1])
        galaxies.log10OiiiHbetaRatio[i] = np.copy(data[i][2])
        galaxies.sSFRinGyr[i] = np.copy(data[i][3])
        PROG.increment()
        PROG.print_status_line()
    np.save(npyfile,galaxies)
    f.close()
    return


class MastersSDSS(object):

    def __init__(self,verbose=False):
        classname = self.__class__.__name__
        funcname = self.__class__.__name__+"."+sys._getframe().f_code.co_name
        self.verbose = verbose
        npyfile = pkg_resources.resource_filename(__name__,"datasets/sdss_sample_final_cut_SNcut.npy")
        if not os.path.exists(npyfile):
            if self.verbose:
                print(classname+"(): Unable to locate numpy version of Masters et al. SDSS datset. Attempting to build from FITS version.")
            buildMastersSDSSNumpy()
        if self.verbose:
            print("Reading in Masters et al. SDSS galaxies dataset...")
        self.galaxies = np.load(npyfile).view(np.recarray)
        self.hubble = 0.7
        self.tree = None
        return

    def buildKDTree(self,hubble=None):
        funcname = self.__class__.__name__+"."+sys._getframe().f_code.co_name
        if self.verbose:
            print("Building kd-tree for nearest neighbour look up...")
        data = np.zeros((len(self.galaxies.log10StellarMass),2),dtype=float)
        data[:,0] = self.galaxies.log10StellarMass
        data[:,1] = self.galaxies.sSFRinGyr
        if hubble is not None:
            data[:,0] += np.log10(self.hubble/hubble)
        self.tree = cKDTree(data)
        return

    def getLineRatio(self,stellarMass,starFormationRate,neighbours=10,statistic="mean",hubble=None):
        funcname = self.__class__.__name__+"."+sys._getframe().f_code.co_name
        if not self.tree:
            self.buildKDTree(hubble=hubble)        
        ratioNIIHa = np.zeros_like(np.copy(stellarMass))*np.nan
        mask = np.logical_and(stellarMass>0.0,starFormationRate>0.0)        
        data = np.zeros((len(stellarMass[mask]),2),dtype=float)
        data[:,0] = np.log10(stellarMass[mask])
        data[:,1] = np.log10(starFormationRate[mask]) - np.log10(stellarMass[mask])
        diff,idiff = self.tree.query(data,k=neighbours)
        if statistic.lower()  == "mean":
            ratio = np.log10(np.mean(10.0**self.galaxies.log10NiiHalphaRatio[idiff],axis=1))
        elif statistic.lower()  == "median":
            ratio = np.log10(np.median(10.0**self.galaxies.log10NiiHalphaRatio[idiff],axis=1))
        else:
            raise ValueError(funcname+"(): Statistic must be 'mean' or 'median'!")
        ratio = (1.0+10.0**ratio)
        np.place(ratioNIIHa,mask,ratio)
        return ratioNIIHa
    

