"""
Post-process XFdtd-generated MAT-Files, regrid, and save results to disk.
"""

# Ensure python 2 and 3 compatibility
from __future__ import (absolute_import, division, generators,
                        print_function, unicode_literals)

import re, os
from scipy.io import loadmat, savemat
import scipy.interpolate as interp

class XFFieldNonUniformGrid(object):
    """A class to hold XF field data on non-uniform grid."""
    def __init__(self):
        self._grid_units = None

    @property
    def units(self):
        """Return the grid units."""
        return self._grid_units
    
    @units.setter
    def units(self, units):
        """Set the grid units."""
        self._grid_units = units
        

