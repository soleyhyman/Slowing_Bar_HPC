
import numpy as np

#import scipy as sc
from scipy.signal import argrelextrema

import astropy
from astropy import units as u

from datetime import datetime, timezone

import argparse

import json

from galpy import __version__
from galpy.orbit import Orbit
from galpy.util import conversion
from galpy.potential import MWPotential2014, vcirc, lindbladR
from galpy.potential import  DehnenBarPotential

# paralizing imports
from multiprocessing import Pool
import os