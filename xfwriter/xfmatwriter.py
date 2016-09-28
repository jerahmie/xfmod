"""
XFdtd Data writer base class.
"""

from __future__ import (absolute_import, division, generators,
                        print_function, unicode_literals)

import abc
import numpy as np

class XFMatWriter(object):
    """Base class for writing xfdata to Mat file."""
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def savemat(self):
        """Save XFdtd data to a Mat file."""
        pass

class XFMatWriterUniform(XFMatWriter):
    """Writer for xfdata to Mat file on uniformly spaced grid."""
    def set_grid_origin(self, x0, y0, z0):
        """Set the origin of the export region."""
        self._x0 = x0
        self._y0 = y0
        self._z0 = z0

    def set_grid_len(self, xlen, ylen, zlen):
        """Set the dimension of the export region."""
        self._xlen = xlen
        self._ylen = ylen
        self._zlen = zlen

    def set_grid_resolution(self, dx, dy, dz):
        """Set the grid step size of he uniformly interpolated grid."""
        self._dx = dx
        self._dy = dy
        self._dz = dz

    def _update_export_grid(self):
        """Updates xdim, ydim, zdim values."""
        self._xdim_uniform = np.arange(self._x0 - self._xlen/2.0,
                                       self._x0 + self._xlen/2.0,
                                       self._dx)
        self._ydim_uniform = np.arange(self._y0 - self._ylen/2.0,
                                       self._y0 + self._ylen/2.0,
                                       self._dy)
        self._zdim_uniform = np.arange(self._z0 - self._zlen/2.0,
                                       self._z0 + self._zlen/2.0,
                                       self._dz)

