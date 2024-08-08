
import numpy as np

#import scipy as sc
from scipy.signal import argrelextrema

import astropy
from astropy import units as u

from datetime import datetime, timezone

import argparse

import json

from galpy import __version__
# import galpy.df
from galpy.orbit import Orbit
from galpy.util import conversion
from galpy.potential import MWPotential2014, vcirc, lindbladR#, evaluatePotentials
from galpy.potential import  DehnenBarPotential#, DehnenSmoothWrapperPotential#, TSolidBodyRotationWrapperPotential SoftenedNeedleBarPotential,
# from galpy.actionAngle import actionAngleAdiabatic, actionAngleStaeckel
# from galpy.potential.WrapperPotential import parentWrapperPotential

from matplotlib.pyplot import *
from matplotlib import pyplot as pl
pl.rc('text', usetex=False)
pl.rc('font', **{'family':'serif','size':20})
pl.rc('axes', labelsize=16)
pl.rc('xtick',labelsize=16)
pl.rc('ytick',labelsize=16)
from matplotlib import colors as mc
from matplotlib import cm
from matplotlib.colors import LogNorm

# paralizing imports
from multiprocessing import Pool
import os