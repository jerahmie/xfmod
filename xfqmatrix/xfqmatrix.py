"""
xfqmatrix.py creates Q matrix data from electric field data and grid data.
"""

# Ensure python 2 and 3 compatibility
from __future__ import (absolute_import, division, generators,
                        print_function, unicode_literals)

import sys, os
from scipy.io import loadmat, savemat

