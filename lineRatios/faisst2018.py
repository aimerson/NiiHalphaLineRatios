#! /usr/bin/env python

import sys
import numpy as np
from scipy.interpolate import RectBivariateSpline

class FaisstModel(object):

    def __init__(self):      
        classname = self.__class__.__name__
        funcname = self.__class__.__name__+"."+sys._getframe().f_code.co_name  
        self.hubble = 0.7
        self.MASS = None
        return

    def buildNiiRedshiftInterpolator(self,gridSize=500,**kwargs):
        funcname = self.__class__.__name__+"."+sys._getframe().f_code.co_name  
        niiMin = -2.0
        niiMax = -0.3
        zMin = 0.0
        zMax = 2.7
        niiRange = np.linspace(niiMin,niiMax,gridSize)
        zRange = np.linspace(zMin,zMax,gridSize)
        ZZ,NII = np.meshgrid(zRange,niiRange)
        xi = NII + 0.138 - 0.042*(1.0+ZZ)**2
        MM = 3.696*xi + 3.236*(1.0/xi) + 0.729*(1.0/xi**2) + 14.928 + 0.156*(1.0+ZZ)**2
        self.MASS = RectBivariateSpline(zRange,niiRange,MM,bbox=[zMin,zMax,niiMin,niiMax],**kwargs)
        return

    def getStellarMass(self,redshift,niiRatio,hubble=None,gridSize=500):
        funcname = self.__class__.__name__+"."+sys._getframe().f_code.co_name  
        zMask = np.logical_or(redshift<0.0,redshift>2.7)
        if any(zMask):
            raise ValueError(funcname+"(): one or more redshifts outside of allowed range 0 <= z <= 2.7.")
        if self.MASS is None:
            self.buildNiiRedshiftInterpolator(gridSize=gridSize)
        mass = self.MASS.ev(redshift,niiRatio)
        if hubble is not None:
            mass += np.log10(self.hubble/hubble)
        return mass
    



