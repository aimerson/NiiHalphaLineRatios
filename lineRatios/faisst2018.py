#! /usr/bin/env python

import numpy as np
from scipy.interpolate import interp2d


class FaisstModel(object):

    def __init__(self):        
        self.hubble = 0.7
        self.MASS = None
        return

    def buildNiiRedshiftInterpolator(self,gridSize=100):
        niiRange = np.linspace(-2.0,-0.3,gridSize)
        zRange = np.linspace(0.0,2.7,gridSize)
        ZZ,NII = np.meshgrid(zRange,niiRange)
        xi = NII + 0.138 - 0.042*(1.0+ZZ)**2
        MM = 3.696*xi + 3.236*(1.0/xi) + 0.729*(1.0/xi**2) + 14.928 + 0.156*(1.0+ZZ)**2
        self.MASS = interp2d(ZZ.flatten(),NII.flatten(),MM.flatten())
        return

    def getStellarMass(self,stellarMass,redshift,hubble=None,gridSize=100):
        if self.MASS is None:
            self.buildNiiRedshiftInterpolator(gridSize=gridSize)
        return self.MASS(stellarMass,redshift)
    



