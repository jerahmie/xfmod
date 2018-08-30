"""
XFdtd regridding helper function.
"""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import sys
import numpy as np
from scipy.interpolate import griddata

class XFRegridError(Exception):
    """Exception xf data regridding."""
    def __init__(self, message):
        self.message = message

def xf_regrid_3d_nearest(X1, X2, data3d):
    """
    Regrid the 3d data to on new grid.

    Keyword arguments:
    x1,y1,z1 -- list of original grid points
          [x1(1,xdim1), y1(1,ydim1), z1(1,zdim1)]
          x1, y1, z1 are arrays of length xdim1, ydim1, zdim1, respectively.

    x2,y2,z2 -- list of regrid points [x2(1,xdim2), y2(1,ydim2), z2(1,zdim2)]
          x2, y2, z2 are arrays of regrid points.

    data3D -- 3d data on original grid points.  The dimensions are
          (xdim1, ydim1, zdim1)

    Returns:
    regrid3D -- 3d data regridded on (x2, y2, z2) grid.

    """

    x1 = X1[0]
    y1 = X1[1]
    z1 = X1[2]
    x2 = X2[0]
    y2 = X2[1]
    z2 = X2[2]

    # check the original data dimensions
    if (np.size(x1), np.size(y1), np.size(z1)) != np.shape(data3d):
        raise XFRegridError("XF regrid dimension mismatch.")

    data3d_regrid = np.zeros((np.size(x2),
                              np.size(y2),
                              np.size(z2)), dtype=data3d.dtype)

    # generate a list of nearest-neighbor z-index values
    z_ind_nearest = []
    for zi in z2:
        z_ind_nearest.append(np.argmin(np.absolute(z1-zi)))

    print("\n[regrid3d] Regridding data.")        
    XX1, YY1 = np.meshgrid(x1, y1, indexing='ij')
    XX2, YY2 = np.meshgrid(x2, y2, indexing='ij')
    z_interp_ind = 0

    for z_ind in z_ind_nearest:
        data3d_regrid[:, :, z_interp_ind] = griddata((XX1.ravel(),
                                                      YY1.ravel()),
                                                     data3d[:, :, z_ind].ravel(),
                                                     (XX2, YY2),
                                                     method='nearest')
        z_interp_ind += 1

    return data3d_regrid
