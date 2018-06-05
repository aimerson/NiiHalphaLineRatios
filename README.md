# [NII] Halpha Line Ratios

Python package of model presented in [Faisst et al. (2018)](http://adsabs.harvard.edu/abs/2018ApJ...855..132F) to model the [NII]/Halpha line ratio fo galaxies as a function of their stellar mass and redshift. Package also allows interpolation of data from [Masters et al. (2016)](http://adsabs.harvard.edu/abs/2016ApJ...828...18M), as was done in [Merson et al. (2018)](http://adsabs.harvard.edu/abs/2018MNRAS.474..177M).

# Installation
```
git clone https://github.com/aimerson/NiiHalphaLineRatios.git
cd niihalphalineratios
python setup.py build
python setup.py install
```
Users without root access may need to replace the last step with `python setup.py install --user`.

# Example usage
Example scripts demonstrating the classes and functions in the Faisst et al. module are stored in the *examples* subdirectory.
