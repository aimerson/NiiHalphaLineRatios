#! /usr/bin/env python

from .plotting.utils import *
import sys
import numpy as np
from scipy.interpolate import interp1d,spline

class FaisstModel(object):

    def __init__(self):      
        classname = self.__class__.__name__
        funcname = self.__class__.__name__+"."+sys._getframe().f_code.co_name  
        self.hubble = 0.7
        self.MASS = None
        return
    
    def FaisstEq3(self,N2,z):
        xi = N2 + 0.138 - 0.042*((1.0+z)**2)
        M = 3.696*xi + 3.236*(xi**-1) + 0.729*(xi**-2) + 14.928 + 0.156*((1.0+z)**2)    
        return M

    def getStellarMass(self,niiRatio,redshift,hubble=None):                           
        funcname = self.__class__.__name__+"."+sys._getframe().f_code.co_name  
        mass = np.array([self.FaisstEq3(nii,z) for nii,z in zip(niiRatio,redshift)])
        if hubble is not None:
            mass += np.log10(self.hubble/hubble)
        return mass

    def interpolateN2Grid(self,redshift,mass):
        NII = np.linspace(-1.5,-0.1,100)
        Z = np.ones_like(NII)*redshift
        MASS = self.getStellarMass(NII,Z)
        f = interp1d(MASS,NII)
        return f(mass)

    def perturbNII(self,nii,z):
        redshifts = [0.0,1.6,2.3]
        errors = [0.13,0.21,0.22]
        zz = np.linspace(0.0,2.3,1000)
        err = spline(redshifts,errors,zz,order=2)
        f = interp1d(zz,err,kind='linear',fill_value='extrapolate')
        sigma = f(z)
        return np.random.normal(loc=nii,scale=sigma)
    
    def getN2(self,mass,redshift,hubble=None):
        if hubble is not None:
            mass += np.log10(hubble/self.hubble)
        nii = np.array([self.interpolateN2Grid(z,m) for z,m in zip(redshift,mass)])
        nii = self.perturbNII(nii,redshift)
        return nii

    def getNiiContamination(self,mass,redshift,hubble=None):
        nii = 10.0**self.getN2(mass,redshift,hubble=hubble)
        return nii/(nii+1.0)
