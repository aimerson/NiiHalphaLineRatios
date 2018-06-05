#! /usr/bin/env python
"""
Example script to demonstrate usage of Faisst et al. model to reproduce 
figure 5 from the Faisst et al. (2018) paper.

"""

import numpy as np
from lineRatios.plotting.utils import *
from lineRatios.faisst2018 import FaisstModel

# Initalize class with Faisst et al. (2018) model
FAISST = FaisstModel()

fig = figure(figsize=(4,4))
ax = fig.add_subplot(111)   

mass = np.linspace(8.5,11,100)

redshift = [0.0,1.6,2.3]
carr = ['b','k','r']
ls = ["-","--",':']
lw = [1.5,1.5,2.0]

for i,z in enumerate(redshift):
    nii = FAISST.getN2(mass,np.ones_like(mass)*z)
    ax.plot(mass,nii,c=carr[i],ls=ls[i],lw=lw[i],label="z = "+str(z))
ax.set_xlim(8.5,11.0)
ax.set_ylim(-1.5,-0.1)

ax.set_xlabel("$\log_{10}\left (M/\mathrm{M_{\odot}}\\right )$")
ax.set_ylabel("$\log_{10}\left (\left [\mathrm{NII}\\right ]/\mathrm{H\\alpha}\\right )$")
Legend(ax,loc=0)

savefig("Faisst2018_fig5.pdf",bbox_inches='tight')
