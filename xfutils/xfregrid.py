"""
XFdtd regridding helper function.
"""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import numpy as np
from scipy.interpolate import griddata


def xf_regrid_3d_nearest(X1, X2, data3d):
    """Regrid the 3d data to on new grid.


    Keyword arguments:
    X1 -- list of original grid points [x1(1,xdim1), y1(1,ydim1), z1(1,zdim1)]
          x1, y1, z1 are arrays of length xdim1, ydim1, zdim1, respectively.
    
    X2 -- list of regrid points [x2(1,xdim2), y2(1,ydim2), z2(1,zdim2)]
          x2, y2, z2 are arrays of regrid points.
    
    data3D -- 3d data on original grid points.  The dimensions are
          (xdim1, ydim1, zdim1)
    
    """

    # check the original data dimensions
    


