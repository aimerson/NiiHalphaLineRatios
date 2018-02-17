#! /usr/bin/env python

from setuptools import setup, find_packages

datafiles = ['datasets/sdss_sample_final_cut_SNcut.fits','datasets/sdss_sample_final_cut_SNcut.npy']

setup(name='lineRatios',
      version='0.1',
      description='Scripts for computing [NII]/Halpha ratios from Masters et al. (2016) SDSS catalogue and model of Faisst et al. (2018).',
      url='http://bitbucket.org/aimerson/niihalphalineratios',
      author='Alex Merson',
      author_email='alex.i.merson@gmail.com',
      license='MIT',
      packages=find_packages(),
      package_dir={'lineRatios':'lineRatios'},
      package_data={'lineRatios':datafiles},
      zip_safe=False)

