"""
Post-process XFdtd-generated MAT-Files, regrid, and save results to disk.
"""

# Ensure python 2 and 3 compatibility
from __future__ import (absolute_import, division, generators,
                        print_function, unicode_literals)

import re, os
from scipy.io import loadmat, savemat
import scipy.interpolate as interp

# class XFFieldNonUniformGrid(object):
#     """A class to hold XF field data on non-uniform grid."""
