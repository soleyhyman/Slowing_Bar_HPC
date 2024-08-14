
import numpy as np
import glob
import shutil

#import scipy as sc
from scipy.signal import argrelextrema
from scipy.optimize import brentq

import astropy
from astropy import units as u

from datetime import datetime, timezone

import argparse

import json

from galpy import __version__
from galpy.orbit import Orbit
from galpy.util import conversion
from galpy.potential import MWPotential2014,DehnenBarPotential, vcirc, lindbladR,omegac,verticalfreq

# paralizing imports
from joblib import Parallel, delayed, parallel_backend
import os
import time